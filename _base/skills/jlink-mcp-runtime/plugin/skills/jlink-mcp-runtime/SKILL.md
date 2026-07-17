---
name: jlink-mcp-runtime
description: Use when the task needs Codex to access a SEGGER J-Link probe through the bundled MCP runtime, inspect or control an embedded target, read memory or registers, use RTT, or start the configured J-Link GDB server.
---

# J-Link MCP Runtime

This skill accompanies the `jlink` MCP server in this plugin. Use it for embedded debugging work that needs a SEGGER J-Link probe.

## Startup

1. Use `get_project_debug_defaults` to inspect the active device, interface, speed, GDB port, SVD path, and executable configuration.
2. Use `list_jlink_devices` before connecting when the user has not named a probe serial number.
3. Use `connect_project_mcu` for the default configured target. Use `connect_device` only when the user gives a different target/interface or asks for generic J-Link access.
4. Use `get_connection_status` after connect, reset, halt, run, or disconnect operations.

## Hardware Safety

Ask for clear user intent before operations that can change target state or flash contents:

- `reset_target`
- `halt_cpu`
- `run_cpu`
- `write_memory`
- `write_register`
- `erase_flash`
- `program_flash`
- `start_project_jlink_gdb_server`

Read-only inspection such as listing devices, checking status, reading registers, reading memory, and fetching target info is safe when it matches the user's debugging request.

## Defaults And Overrides

The launcher defaults are:

- Device: `STM32H723ZG`
- Interface: `SWD`
- Speed: `auto`
- GDB server port: `54526`

Override them with:

- `JLINK_MCP_DEVICE`
- `JLINK_MCP_INTERFACE`
- `JLINK_MCP_SPEED`
- `JLINK_MCP_GDB_PORT`
- `JLINK_MCP_GDB_SELECT`
- `JLINK_MCP_GDBSERVER_CL`
- `JLINK_SVD_DIR`

## Suggested Flows

For first contact:

```text
get_project_debug_defaults -> list_jlink_devices -> connect_project_mcu -> get_target_info -> get_connection_status
```

For CPU state inspection:

```text
get_connection_status -> halt_cpu -> read_registers -> get_cpu_state
```

For SVD register inspection:

```text
connect_project_mcu -> list_svd_devices -> get_svd_peripherals -> get_svd_registers -> read_register_with_fields
```

For GDB server handoff:

```text
get_project_debug_defaults -> start_project_jlink_gdb_server -> stop_project_jlink_gdb_server
```
