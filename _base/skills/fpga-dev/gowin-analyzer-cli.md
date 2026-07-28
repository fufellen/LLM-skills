# Gowin Analyzer Oscilloscope CLI Notes

Use this reference when debugging internal FPGA signals with Gowin Analyzer Oscilloscope (GAO), `.rao`, `.gao`, or JTAG capture on the local Gowin toolchain.

## Local Paths

- GAO GUI: `C:\workspace\verilog\bin\IDE\bin\gao_analyzer.exe`
- GAO command runner candidate: `C:\workspace\verilog\bin\IDE\bin\gao_sh.exe`
- Gowin IDE CLI: `C:\workspace\verilog\bin\IDE\bin\gw_sh.exe`
- Programmer CLI: `C:\workspace\verilog\bin\Programmer\bin\programmer_cli.exe`
- Local manual: `C:\workspace\verilog\bin\IDE\doc\ENG\SUG114-2.5E_Gowin Analyzer Oscilloscope User Guide.pdf`
- Example projects with GAO config:
  - `C:\workspace\verilog\bin\IDE\data\examples\game`
  - `C:\workspace\verilog\bin\IDE\data\examples\vga_text_generator`
  - `C:\workspace\verilog\bin\IDE\data\examples\FIFO_HS`

## Verified Facts

- `.rao` is the RTL-level GAO config used before synthesis.
- `.gao` is the post-synthesis netlist GAO config.
- Gowin `.gprj` stores both `.rao` and `.gao` with `type="file.gao"`.
- Keep only one active `.rao`/`.gao` config per target build unless a project has already proven a multi-config flow.
- GAO captures through JTAG from an analyzer-enabled bitstream.
- Standard GAO supports trigger match units, trigger expressions, capture windows, capture amount, trigger position, and CSV/VCD/PRN export.
- Lite GAO is simpler and can capture initial values.
- Existing local `.rao` examples under `src/main` are XML `GAO_CONFIG` files and can be used as format references.
- Useful local Obsidian notes live under `C:\Users\User\Мой диск\Obsidian\ПО\Программирование\ПЛИС\Gowin\Встроенный анализатор\`.

## Current CLI Findings

- `gao_sh.exe` without `-gao` or with `--help` reports `Error: invalid gao file.`
- The binary contains `-gao` and `--fsFile` strings.
- These invocations are accepted without the invalid-file error, and the `--fsFile` form has produced a `*_core0_window0.csv` capture export in the current working directory:

```powershell
& 'C:\workspace\verilog\bin\IDE\bin\gao_sh.exe' -gao '<config.rao-or.gao>'
& 'C:\workspace\verilog\bin\IDE\bin\gao_sh.exe' -gao '<config.rao-or.gao>' --fsFile '<analyzer-enabled.fs>'
```

- `gao_analyzer.exe -gao <config.rao-or.gao>` is accepted and should open/load the GUI when a desktop is available.
- `gao_sh.exe` may print nothing to stdout even when it captures successfully; inspect recent `*_core*_window*.csv` files and timestamps.
- After CSV export, `gao_sh.exe` can keep a JTAG session alive. If programming or a new capture cannot access JTAG, check and stop stale `gao_sh`/`gao_analyzer` processes.
- If `programmer_cli.exe` hangs or `--scan-cables` stops finding the cable after a replug, inspect the FTDI device state. `USB Serial Converter B` with `ProblemCode 10` prevents Gowin from seeing the cable; physically replug until `programmer_cli.exe --scan-cables` reports a `USB Debugger A/.../<location>/...` entry.
- When `--scan-cables` reports a concrete USB location such as `USB Debugger A/0/417/null`, pass that location to programming commands with `--location 417`. This avoided cable auto-selection problems during 20K SRAM programming.
- Treat the trigger/control semantics as still under investigation until forced-trigger, wait-for-trigger, and timeout behavior are proven on the target project.

## Build Integration Checklist

1. Start from an existing board top and existing constraints. Do not create a new top just to expose GAO signals.
2. Add a narrow `.rao` or `.gao` config only for the debug scope being captured.
3. Prefer top-level ports and interfaces declared directly in the top module for the first capture. They are the most reliable names.
4. Use `/` for hierarchy paths. Plain hierarchy through modules without SV interface ports can work.
5. Be careful with hierarchy through modules that have SystemVerilog interface ports; Gowin can specialize/rename instances. For those signals, use Search Nets after synthesis or expose a small debug signal upward through normal ports.
6. In Tcl projects, try adding the config with normal `add_file <path-to-config.rao>` and verify the generated artifacts instead of assuming it worked.
7. After build, check for GAO insertion artifacts:
   - RTL-level: `impl/gwsynthesis/RTL_GAO/`
   - post-synthesis: `impl/gao/`
   - GAO wrapper: `gw_gao_top.v`
   - analyzer bitstream often named `impl/pnr/ao_0.fs`
8. Inspect the synthesis and PnR logs for GAO files and JTAG analyzer modules such as `gw_gao`, `GW_JTAG`, `GW_AO_*`, and `GW_CON`.
9. Do not let an old programming wrapper blindly program `LDR_20K.fs` if the GAO-enabled bitstream is `ao_0.fs`; verify the exact latest `.fs` path.
10. Program volatile SRAM for bench captures unless persistent programming is explicitly requested.

## Resource Heuristics

- `Storage Size` consumes hardware memory and affects build/routing.
- `Capture Amount` is a runtime capture length and must satisfy `Capture Amount * Window Number <= Storage Size`.
- Small storage sizes can be implemented in LUT/FF instead of BSRAM and may make routing worse.
- Large storage sizes reduce BSRAM width and can consume many BSRAM blocks.
- A previously working GW2A-18C example used `Storage Size = 2048` for a wide 73-bit capture; `4096+` was too expensive for that width. For longer captures, first reduce signal width drastically.

## Capture Workflow

1. Build the analyzer-enabled bitstream and record the exact `.fs` path.
2. Program that `.fs` into volatile SRAM.
3. Run a capture through GAO over JTAG.
4. Export or locate waveform output as `.csv`, `.vcd`, or `.prn`; headless `gao_sh` CSV output may appear in the shell working directory.
5. Parse the exported file locally and summarize real signal values, trigger position, and whether the expected event was seen.
6. If no capture file appears, inspect recent files and logs before changing HDL.

## 20K RMII/UART Debug Targets

For the 20K dev-board UART/RMII bridge, useful first capture signals are:

- sample clock: `EthRefCLK` or the internal RMII clock used by the top
- external inputs: `uart_rx`, `EthRXD0`, `EthRXD1`, `EthCrsDv`
- external outputs: `uart_tx`, `EthTXD0`, `EthTXD1`, `EthTXEN`
- internal RMII interface signals: `if_rmii.rxd[1:0]`, `if_rmii.crs_dv`, `if_rmii.txd[1:0]`, `if_rmii.txen`

Prefer triggers on edges of `uart_rx`, `EthCrsDv`, or `if_rmii.txen` depending on which side of the tract is being isolated.

## Validated 20K RMII/UART Findings

- `C:\workspace\verilog\20k\LDR_20K\impl\pnr\ao_0.fs` was the fresh GAO-enabled bitstream in the current LDR_20K flow; `LDR_20K.fs` can be older.
- For `m20k_dev_uart_rmii_debug`, programming `ao_0.fs` to SRAM with `programmer_cli.exe -d GW2A-18C -r 2 -f <fs>` worked.
- A UART-to-RMII hardware proof used a 60-byte Ethernet frame before FCS:
  - dst `ff:ff:ff:ff:ff:ff`
  - src `02:20:20:20:20:20`
  - ethertype `0x88b5`
  - payload starts `de ad be ef`
  - `tshark -i "Ethernet 5" -f "ether proto 0x88b5"` captured 3 matching packets.
- An RMII-to-UART hardware proof used UDP broadcast from `192.168.15.13` to `192.168.15.255:48879` with payload starting `de ad be ef`; `tshark` saw the packets and COM3 UART output contained the same marker.
- Do not treat Scapy/Npcap `sendp` plus local `tshark` as proof that a raw packet reached the FPGA. It can appear in the local capture while GAO and UART show the FPGA did not see that frame.
- The existing RMII RX CRC checker had a packet-length alignment trap: tests padded to multiples of four can hide a bug that drops valid non-4-byte-aligned frames. Add or keep a simulation case with a valid 65-byte payload and correct FCS.
- Destination-MAC filtering in `m20k_dev_uart_rmii_debug` was validated with `LOCAL_MAC = 02:20:20:20:20:20`, broadcast enabled, and multicast enabled. ModelSim `eth_rx_check_tb` covers local unicast, `ff:ff:ff:ff:ff:ff`, `01:00:5e:00:00:fb`, and rejected unrelated unicast. Hardware proof used COM3 UART: broadcast and multicast UDP payload markers appeared, Scapy raw local-unicast frames appeared, and Scapy raw unrelated-unicast frames did not.
