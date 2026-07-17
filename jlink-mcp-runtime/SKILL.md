---
name: jlink-mcp-runtime
description: Use when Codex needs the portable SEGGER J-Link MCP runtime copied from the ToF-LIDAR MCU repository to inspect or control an embedded target, read memory or registers, use RTT, or start the configured J-Link GDB server.
---

# J-Link MCP Runtime (Codex Adapter)

The shared workflow is in `../_base/skills/jlink-mcp-runtime/SKILL.md`. Read that file completely before using this skill and resolve all relative paths from its directory.

The runnable plugin snapshot is stored at `../_base/skills/jlink-mcp-runtime/plugin/`. It must remain a complete directory because the skill depends on its bundled Python MCP server, launcher, metadata, device patch, and instructions.

Use the registered `jlink` MCP tools when they are available. If the server is not registered or the installation is uncertain, follow the non-hardware check in the shared workflow. Always preserve its hardware-safety gates before reset, CPU-state changes, memory/register writes, erase, programming, or GDB-server startup.
