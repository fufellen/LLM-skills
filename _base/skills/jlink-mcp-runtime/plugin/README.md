# J-Link MCP Runtime

This folder is a portable Codex plugin for the J-Link MCP server used by this firmware repository. Copy the whole `jlink-mcp-runtime` directory into another project's plugin location or local marketplace source to bring the same MCP server, launcher, and usage instructions with it.

## Contents

- `.codex-plugin/plugin.json` describes the plugin for Codex import.
- `.mcp.json` registers the `jlink` MCP server.
- `launcher.py` starts the bundled runtime from `site/jlink_mcp`.
- `site/jlink_mcp` contains the vendored Python MCP server package.
- `skills/jlink-mcp-runtime/SKILL.md` tells Codex when and how to use the tool.
- `AGENTS.md` contains hardware-safety and configuration notes.
- `DEPENDENCIES.md` lists host dependencies that are not vendored.

## Quick Check

From the plugin root:

```powershell
python launcher.py --check
```

The check imports the bundled runtime, verifies the launcher configuration, reports dependency status, and exits without connecting to the target.

## Defaults

The launcher defaults match this repository:

- Device: `STM32H723ZG`
- Interface: `SWD`
- Speed: `auto`
- GDB server port: `54526`
- GDB server select: `USB`

Override these values with environment variables:

- `JLINK_MCP_DEVICE`
- `JLINK_MCP_INTERFACE`
- `JLINK_MCP_SPEED`
- `JLINK_MCP_GDB_PORT`
- `JLINK_MCP_GDB_SELECT`
- `JLINK_MCP_GDBSERVER_CL`
- `JLINK_SVD_DIR`

## Importing Into Another Project

Use this directory itself as the plugin root. The import target must preserve the relative paths below:

```text
jlink-mcp-runtime/
  .codex-plugin/plugin.json
  .mcp.json
  launcher.py
  site/jlink_mcp/
  skills/jlink-mcp-runtime/SKILL.md
```

After copying, run `python launcher.py --check` from the copied plugin root. If the target project uses a different MCU, set `JLINK_MCP_DEVICE` and related variables in that project's MCP environment.
