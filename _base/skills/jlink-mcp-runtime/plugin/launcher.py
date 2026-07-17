"""Portable launcher for the bundled J-Link MCP runtime.

This file is intentionally self-contained so the whole jlink-mcp-runtime
directory can be copied into another project and used as a Codex plugin.
"""

from __future__ import annotations

import argparse
import atexit
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from typing import Any


RUNTIME_ROOT = Path(__file__).resolve().parent
RUNTIME_SITE = RUNTIME_ROOT / "site"
RUNTIME_PACKAGE = RUNTIME_SITE / "jlink_mcp"

PROJECT_DEVICE = os.environ.get("JLINK_MCP_DEVICE", "STM32H723ZG")
PROJECT_INTERFACE = os.environ.get("JLINK_MCP_INTERFACE", "SWD").upper()
PROJECT_SPEED = os.environ.get("JLINK_MCP_SPEED", "auto")
PROJECT_GDB_PORT = int(os.environ.get("JLINK_MCP_GDB_PORT", "54526"))
PROJECT_GDB_SELECT = os.environ.get("JLINK_MCP_GDB_SELECT", "USB")
PROJECT_PATCH_DIR = Path(os.environ.get("JLINK_PATCH_DIR", str(RUNTIME_ROOT / "Patches")))


def _default_gdbserver_command() -> str:
    if os.name == "nt":
        return r"C:\Program Files\SEGGER\JLink\JLinkGDBServerCL.exe"
    return "JLinkGDBServerCLExe"


PROJECT_GDB_EXE = os.environ.get("JLINK_MCP_GDBSERVER_CL", _default_gdbserver_command())

_gdb_process: subprocess.Popen[bytes] | None = None
_gdb_log_handle: Any | None = None


def _module_available(name: str) -> bool:
    return importlib.util.find_spec(name) is not None


def _read_bundled_version() -> str:
    init_path = RUNTIME_PACKAGE / "__init__.py"
    if not init_path.is_file():
        return "missing"

    match = re.search(
        r"^__version__\s*=\s*['\"]([^'\"]+)['\"]",
        init_path.read_text(encoding="utf-8", errors="replace"),
        re.MULTILINE,
    )
    return match.group(1) if match else "unknown"


def _prepare_environment() -> str:
    if not RUNTIME_PACKAGE.is_dir():
        raise RuntimeError(f"Bundled package is missing: {RUNTIME_PACKAGE}")

    runtime_site = str(RUNTIME_SITE)
    if runtime_site not in sys.path:
        sys.path.insert(0, runtime_site)

    os.environ.setdefault("JLINK_DEFAULT_INTERFACE", PROJECT_INTERFACE)
    os.environ.setdefault("JLINK_PATCH_DIR", str(PROJECT_PATCH_DIR))

    svd_dir = _find_svd_dir()
    if svd_dir:
        os.environ["JLINK_SVD_DIR"] = svd_dir

    return _read_bundled_version()


def _find_svd_dir() -> str | None:
    configured = os.environ.get("JLINK_SVD_DIR")
    if configured and Path(configured).exists():
        return configured

    candidates = [
        RUNTIME_ROOT / "svd",
        Path.home() / ".platformio" / "platforms" / "ststm32" / "misc" / "svd",
        Path(r"C:\Program Files\STMicroelectronics\STM32Cube\STM32CubeProgrammer\SVD"),
    ]

    for candidate in candidates:
        if (candidate / "STM32H723.svd").exists():
            return str(candidate)

    return configured


def _normalise_device_name(name: str) -> str:
    return "".join(ch for ch in name.upper() if ch.isalnum())


def _register_project_device_patch() -> None:
    from jlink_mcp.device_patch_interface import DevicePatchInterface
    from jlink_mcp.device_patch_manager import device_patch_manager

    class ProjectDevicePatch(DevicePatchInterface):
        @property
        def vendor_name(self) -> str:
            return "STMicroelectronics"

        @property
        def patch_version(self) -> str:
            return "portable-runtime"

        def is_available(self) -> bool:
            return True

        @property
        def devices(self) -> list[dict[str, Any]]:
            return [
                {
                    "name": PROJECT_DEVICE,
                    "vendor": self.vendor_name,
                    "core": "ARM Cortex-M7",
                    "interface": PROJECT_INTERFACE,
                    "gdb_port": PROJECT_GDB_PORT,
                }
            ]

        @property
        def device_names(self) -> list[str]:
            return [PROJECT_DEVICE]

        def match_device_name(self, partial_name: str) -> str | None:
            if not partial_name:
                return PROJECT_DEVICE

            requested = _normalise_device_name(partial_name)
            project_device = _normalise_device_name(PROJECT_DEVICE)
            aliases = {
                project_device,
                "STM32H723",
                "STM32H723ZG",
                "STM32H723ZGT6",
                "STM32H723ZGTX",
                "STM32H723XX",
            }

            if requested in aliases or project_device.startswith(requested):
                return PROJECT_DEVICE

            return None

        def find_similar_devices(self, partial_name: str, limit: int = 10) -> list[str]:
            if self.match_device_name(partial_name):
                return [PROJECT_DEVICE][:limit]
            return []

        def get_device_name_suggestions(self, partial_name: str) -> str:
            return f"Use {PROJECT_DEVICE} with {PROJECT_INTERFACE}."

    if not device_patch_manager.is_device_supported(PROJECT_DEVICE):
        device_patch_manager.register_patch(ProjectDevicePatch())


def _gdb_log_path() -> Path:
    log_dir = RUNTIME_ROOT / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir / "jlink-gdb-server.log"


def _gdb_is_running() -> bool:
    return _gdb_process is not None and _gdb_process.poll() is None


def _stop_gdb_process() -> None:
    global _gdb_process, _gdb_log_handle

    if _gdb_process is not None and _gdb_process.poll() is None:
        _gdb_process.terminate()
        try:
            _gdb_process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            _gdb_process.kill()
            _gdb_process.wait(timeout=2)

    _gdb_process = None

    if _gdb_log_handle is not None:
        _gdb_log_handle.close()
        _gdb_log_handle = None


def _resolve_gdbserver_exe() -> str | None:
    configured = Path(PROJECT_GDB_EXE)
    if configured.is_absolute():
        return str(configured) if configured.exists() else None

    found = shutil.which(PROJECT_GDB_EXE)
    return found


def _register_project_tools() -> None:
    from jlink_mcp import server as jlink_server
    from jlink_mcp.config_manager import config_manager
    from jlink_mcp.tools.connection import connect_device as _connect_device

    config_manager.update_config(default_interface=PROJECT_INTERFACE)

    @jlink_server.mcp.tool()
    async def get_project_debug_defaults() -> dict[str, Any]:
        """Return the J-Link debug defaults used by this plugin instance."""

        return {
            "device": PROJECT_DEVICE,
            "interface": PROJECT_INTERFACE,
            "speed": PROJECT_SPEED,
            "gdb_port": PROJECT_GDB_PORT,
            "gdb_select": PROJECT_GDB_SELECT,
            "jlink_gdbserver_cl": PROJECT_GDB_EXE,
            "jlink_gdbserver_cl_resolved": _resolve_gdbserver_exe(),
            "svd_dir": os.environ.get("JLINK_SVD_DIR"),
            "connect_tool": "connect_project_mcu",
            "gdb_server_start_tool": "start_project_jlink_gdb_server",
        }

    @jlink_server.mcp.tool()
    async def connect_project_mcu(serial_number: str | None = None) -> dict[str, Any]:
        """Connect to the configured project MCU using the configured interface."""

        return _connect_device(serial_number, PROJECT_INTERFACE, PROJECT_DEVICE)

    @jlink_server.mcp.tool()
    async def start_project_jlink_gdb_server(port: int = PROJECT_GDB_PORT) -> dict[str, Any]:
        """Start JLinkGDBServerCL with the configured project defaults."""

        global _gdb_process, _gdb_log_handle

        if _gdb_is_running():
            return {
                "success": True,
                "message": "J-Link GDB server is already running",
                "pid": _gdb_process.pid if _gdb_process else None,
                "port": port,
                "log": str(_gdb_log_path()),
            }

        exe = _resolve_gdbserver_exe()
        if exe is None:
            return {
                "success": False,
                "message": f"J-Link GDB server executable not found: {PROJECT_GDB_EXE}",
                "hint": "Install SEGGER J-Link or set JLINK_MCP_GDBSERVER_CL.",
            }

        command = [
            exe,
            "-select",
            PROJECT_GDB_SELECT,
            "-device",
            PROJECT_DEVICE,
            "-speed",
            PROJECT_SPEED,
            "-if",
            PROJECT_INTERFACE,
            "-port",
            str(port),
        ]

        _gdb_log_handle = _gdb_log_path().open("ab")
        flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
        _gdb_process = subprocess.Popen(
            command,
            stdout=_gdb_log_handle,
            stderr=subprocess.STDOUT,
            creationflags=flags,
        )

        return {
            "success": True,
            "message": "J-Link GDB server started",
            "pid": _gdb_process.pid,
            "port": port,
            "command": command,
            "log": str(_gdb_log_path()),
        }

    @jlink_server.mcp.tool()
    async def stop_project_jlink_gdb_server() -> dict[str, Any]:
        """Stop the J-Link GDB server started by this launcher."""

        was_running = _gdb_is_running()
        _stop_gdb_process()
        return {
            "success": True,
            "message": "J-Link GDB server stopped" if was_running else "J-Link GDB server was not running",
        }


def _build_server() -> str:
    version = _prepare_environment()
    _register_project_device_patch()
    _register_project_tools()
    atexit.register(_stop_gdb_process)
    return version


def _check() -> int:
    version = _read_bundled_version()
    payload: dict[str, Any] = {
        "ok": True,
        "runtime_root": str(RUNTIME_ROOT),
        "runtime_package": str(RUNTIME_PACKAGE),
        "runtime_package_exists": RUNTIME_PACKAGE.is_dir(),
        "jlink_mcp_version": version,
        "device": PROJECT_DEVICE,
        "interface": PROJECT_INTERFACE,
        "speed": PROJECT_SPEED,
        "gdb_port": PROJECT_GDB_PORT,
        "jlink_gdbserver_cl": PROJECT_GDB_EXE,
        "jlink_gdbserver_cl_resolved": _resolve_gdbserver_exe(),
        "svd_dir": os.environ.get("JLINK_SVD_DIR") or _find_svd_dir(),
        "dependencies": {
            "mcp": _module_available("mcp"),
            "pylink": _module_available("pylink"),
        },
    }

    try:
        payload["loaded_version"] = _build_server()
    except Exception as exc:
        payload["ok"] = False
        payload["error"] = f"{type(exc).__name__}: {exc}"

    print(json.dumps(payload, indent=2))
    return 0 if payload["ok"] else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Start the portable J-Link MCP server.")
    parser.add_argument("--check", action="store_true", help="Validate launcher setup and exit.")
    args = parser.parse_args()

    if args.check:
        return _check()

    _build_server()

    from jlink_mcp import server as jlink_server

    jlink_server.init_server_config()
    jlink_server.mcp.run(transport="stdio")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
