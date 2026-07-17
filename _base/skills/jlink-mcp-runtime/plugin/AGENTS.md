# J-Link MCP Runtime Agent Notes

This plugin gives Codex access to a physical SEGGER J-Link probe and an attached target. Treat tools that reset, halt, write memory, erase flash, program flash, or start external debug servers as hardware-affecting operations.

Start with `get_project_debug_defaults`, `list_jlink_devices`, and `get_connection_status` when orienting. Prefer `connect_project_mcu` for this repository's default STM32H723ZG target, or `connect_device` when the user supplies another device/interface pair.

The runtime defaults can be overridden through environment variables in `.mcp.json` or the host process:

- `JLINK_MCP_DEVICE`
- `JLINK_MCP_INTERFACE`
- `JLINK_MCP_SPEED`
- `JLINK_MCP_GDB_PORT`
- `JLINK_MCP_GDB_SELECT`
- `JLINK_MCP_GDBSERVER_CL`
- `JLINK_SVD_DIR`

Use `python launcher.py --check` for a non-hardware startup check before debugging a new installation.
