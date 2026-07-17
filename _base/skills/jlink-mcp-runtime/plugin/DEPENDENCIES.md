# Dependencies

The plugin vendors the `jlink_mcp` Python package source under `site/jlink_mcp`, but it does not vendor host-level or binary dependencies.

Required on the machine that runs the MCP server:

- Python 3.10 or newer.
- The Python packages `mcp` and `pylink-square`.
- SEGGER J-Link software and drivers.
- A connected SEGGER J-Link probe.

Optional but useful:

- An SVD directory containing the target MCU SVD file. Set `JLINK_SVD_DIR` when the automatic PlatformIO and STM32CubeProgrammer paths do not apply.
- `JLinkGDBServerCL.exe` on Windows, or the platform equivalent on PATH. Override with `JLINK_MCP_GDBSERVER_CL`.

Run this from the plugin root to verify imports and configuration without connecting to hardware:

```powershell
python launcher.py --check
```
