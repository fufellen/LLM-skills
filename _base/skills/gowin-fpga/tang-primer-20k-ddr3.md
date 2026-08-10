# Tang Primer 20K DDR3 Gowin Notes

## nand2mario DDR3 Dry Build

Observed on 2026-06-22 with `nand2mario/ddr3-tang-primer-20k` commit `a6d866d`, cloned under:

```text
C:\Users\User\AppData\Local\Temp\codex_tang_primer20k_sources\ddr3-tang-primer-20k
```

The upstream project has `ddr3.gprj` but no Tcl build script. A temporary Tcl mirror of the `.gprj` built successfully with Gowin CLI after adding SSPI regular-IO mode.

Working options:

```tcl
set_device -name GW2A-18C GW2A-LV18PG256C8/I7
set_option -output_base_name ddr3_codex
set_option -top_module ddr3_top
set_option -verilog_std sysv2017
set_option -synthesis_tool gowinsynthesis
set_option -write_apr_constraint 1
set_option -use_mspi_as_gpio 1
set_option -use_sspi_as_gpio 1
```

With only `set_option -use_mspi_as_gpio 1`, synthesis passed but PnR failed:

```text
ERROR (PR2028): The constrainted location is useless in current package
ERROR (PR2017): 'led2[7]' cannot be placed according to constraint, for the location is a dedicated pin (SSPI)
```

The README says to set `Project -> Configuration -> Dual Purpose Pin -> Use SSPI as regular IO`; for CLI, use `set_option -use_sspi_as_gpio 1`.

Successful dry-build evidence after adding the `DDR3_nCS` constraint:

- PnR log: `Placement and routing completed`
- PnR log: `Bitstream generation completed`
- Output `.fs`: `impl\pnr\ddr3_codex.fs`, `7264087` bytes
- Output `.bin`: `impl\pnr\ddr3_codex.bin`, `907418` bytes
- Timing: setup violated endpoints `0`, hold violated endpoints `0`
- PnR resources: logic `1382/20736 6%`, registers `476/16173 2%`, BSRAM `2%`, PLL `1/4`, DQS `2/9`
- Pin report: `DDR3_nCS` on `P5/4`, constrained `Y`, `SSTL15`, `BANK_VCCIO=1.5`

## CS_N Constraint Trap

The unmodified nand2mario `src\tang20k.cst` does not constrain `DDR3_nCS`.

In the dry build above, Gowin auto-placed `DDR3_nCS` on `A9/7` with `Constraint N`, leaving official DDR3 `P5` unused. That bitstream should not be treated as hardware-ready.

The controller does drive the signal:

```verilog
assign DDR3_nCS = 1'b0;
```

Official Sipeed examples repeatedly constrain DDR3 CS_N to `P5`, for example:

```text
IO_LOC "ddr_cs" P5;
IO_PORT "ddr_cs" IO_TYPE=SSTL15 PULL_MODE=NONE DRIVE=8 BANK_VCCIO=1.5;
```

Before programming a nand2mario-derived hardware test, add the equivalent constraint for the actual top-level port name:

```text
IO_LOC "DDR3_nCS" P5;
IO_PORT "DDR3_nCS" IO_TYPE=SSTL15 PULL_MODE=NONE DRIVE=8 BANK_VCCIO=1.5;
```

Then rebuild and recheck the pin report confirms `DDR3_nCS` is on `P5`.

After adding this constraint in the temp clone, the 2026-06-22 dry build passed PnR/timing and the pin report moved `DDR3_nCS` to `P5/4`.

## nand2mario DDR3 Hardware Check

Observed on 2026-06-22 after physically replugging the USB/JTAG cable so both FTDI channels were healthy:

- `programmer_cli --scan-cables`: `Cable found: USB Debugger A/0/289/null`
- JTAG read: `ID code is: 0x0000081B`, `Status code is: 0x00006020`
- Programmed through `C:\workspace\verilog\20k\program20K_volatile_fs.bat`
- Target: `GW2A-18C`
- Memory target: volatile SRAM only, `-r 2`
- Firmware: temp clone `impl\pnr\ddr3_codex.fs`, built from nand2mario commit `a6d866d` with `DDR3_nCS` constrained to `P5`
- Programmer result: `Operation "SRAM Program"`, `User Code: 0x00004825`, `Status Code: 0x00006020`, `Cost 11.66 second(s)`

UART was captured on `COM3` at `115200` baud. The acceptance evidence was:

```text
Write leveling and read calib successful.

1 - Single write/read tests:

0000=1122
0001=3344
0002=5566

2 - Bulk write/read tests: SUCCESS.

Final address=00800000
Error=00
Expected=ffbb
Actual=ffbb
```

Lines from the previously-loaded lidar firmware can appear before the DDR3 UART text if capture starts before SRAM programming. Ignore those earlier lines and use the post-programming DDR3 calibration/test output as evidence.

## DarkRISCV + nand2mario DDR3 Smoke

Observed on 2026-06-22 in `C:\workspace\verilog\20k\DARKRISCV_DDR3_20K`:

- The target vendors `nand2mario/ddr3-tang-primer-20k` commit `a6d866d`, adds the missing `DDR3_nCS=P5` constraint, and uses `set_option -use_sspi_as_gpio 1`.
- A DarkRISCV top that clocked the CPU from the DDR pclk (`clkoutd`, about `99.5625 MHz`) built a bitstream but failed timing: setup violated endpoints `818`, `clk` actual Fmax about `49.943 MHz`. Treat this as not hardware-ready even if PnR and bitstream generation complete.
- The timing-clean build clocks DarkRISCV from board `sys_clk` (`27 MHz`) and keeps nand2mario DDR3 on the verified PLL domains (`clk` about `99.5625 MHz`, `clk_x4` about `398.25 MHz`). A small `darkddr3_ui_cdc.sv` command/response bridge crosses between the CPU MMIO adapter and the DDR3 user port.
- `build_gowin.tcl` first builds `src\ddr3demo` through `C:\msys64\usr\bin\make.exe`. Keep `2>@1` on that Tcl `exec`; without it, the successful RISC-V link can look like a Tcl error because the known RWX LOAD segment warning is printed to stderr.
- Timing after the CDC split and refresh-race fix: setup violated endpoints `0`, hold violated endpoints `0`; Max Frequency Summary reported `clk` constraint `100.000 MHz`, actual `125.731 MHz`; `clk_x4` constraint `400.000 MHz`, actual `2016.129 MHz`; `sys_clk` constraint `27.000 MHz`, actual `46.957 MHz`.
- Pin report confirmed `DDR3_nCS` on `P5/4`, constrained `Y`, `SSTL15`, `BANK_VCCIO=1.5`.
- Generated hardware files: `impl\pnr\DARKRISCV_DDR3_20K.fs` (`7264087` bytes) and `.bin` (`907418` bytes).
- Volatile SRAM programming used the tracked `C:\workspace\verilog\20k\program20K_volatile_fs.bat` wrapper, target `GW2A-18C`, memory target `-r 2`. Result after the final post-fix build: `User Code: 0x0000A843`, `Status Code: 0x00006020`, cost `14.11` seconds.
- UART hardware evidence on `COM3` at `115200`: 13 full `ddr3demo ok` passes in a 35-second capture, repeated `ddr3demo status=0107`, `ddr3demo rw addr=10 data=55667788`, `ddr3demo rw addr=40 data=a5a55a5a`, refresh count increment, and no `timeout`, `mismatch`, or `error` lines.
- When the CPU clock is changed, verify refresh math. The DarkRISCV instantiation now overrides `darkddr3_mmio.REFRESH_INTERVAL_CYCLES` with ``BOARD_CK / 128000``; at `27 MHz` Gowin elaborated it as `210` cycles.
- A previously observed `timeout read-done status=0147` during repeated hardware restarts was fixed in `darkddr3_mmio.sv` by allowing one command to be queued during `ST_REFRESH_WAIT`; `darkddr3_mmio_tb` now covers that refresh-overlap case.

## DarkRISCV DDR3 Memtest Hardware Check

Observed on 2026-06-22 in `C:\workspace\verilog\20k\DARKRISCV_DDR3_20K`:

- The default firmware is now `APPLICATION=ddr3memtest`; set `DARKRISCV_DDR3_APP=ddr3demo` for the earlier short smoke.
- `src\ddr3memtest` covers data-bus walking ones/zeros, address-line alias checks, sparse boundary probes, read-after-write, address-as-data, inverted-address, checkerboard, PRBS/LFSR, MATS/March-like passes, stride/random access, software subword RMW modeling, and retention.
- The firmware helper must clear `OP_DONE/OP_ERROR` and wait until those bits read back as cleared before issuing a new command. Otherwise fast loops can consume stale `RDATA` and report a false mismatch.
- The hardware profile built as `3012 darksocv.mem` / `11536` UART bytes. Gowin timing had setup/hold violated endpoints `0`; `DARKRISCV_DDR3_20K.fs` was `7264087` bytes.
- Volatile SRAM programming used `C:\workspace\verilog\20k\program20K_volatile_fs.bat`, target `GW2A-18C`, memory target `-r 2`, and reported `User Code: 0x0000A843`, `Status Code: 0x00006020`, cost `13.41` seconds.
- UART capture on `COM3` at `115200` for about 90 seconds reached repeated `ddr3memtest ok` passes with `mismatch_count=0`, `timeout_count=0`, and `error_count=0`.
- Open caveat: the low-address probe still warns at DDR3 16-bit word address `0x00`; the main test window starts at `0x30`.
- This proves the CPU MMIO diagnostic window and nand2mario user port, not native byte-enable, true CPU misaligned load/store behavior, DMA, an independent FPGA bus master, executable DDR, cache, heap, frame buffers, or LwIP pbufs.

## LDR_20K Ethernet + DDR3 Diagnostic Hardware Check

Observed on 2026-06-22 in `C:\workspace\verilog\20k\LDR_20K` with `LDR_20K_DDR3=1`:

- The active lidar/LwIP top reuses nand2mario commit `a6d866d` and `darkddr3_ui_cdc.sv`, keeps Ethernet MMIO in CS2 at `0x80000000`, and exposes DDR3 diagnostic MMIO in CS3 at `0xc0000000`.
- The Gowin build uses one combined DDR3/Ethernet CST and one combined DDR3/Ethernet SDC: `src\m20k_dev_uart_ddr3_pins.cst` and `src\m20k_dev_uart_ddr3.sdc`. The pin report confirmed `DDR3_nCS=P5/4`, `DDR3_A[13]=C8/6`, `sys_clk=H11/0`, and the existing Ethernet/UART/Flash pins constrained.
- Firmware built as `14724 darksocv.mem` / `58384` UART bytes after enabling a DDR3-specific LwIP RAM profile. This profile was needed because the first DDR3+LwIP image left only about `0x1ac` bytes of stack headroom and failed TCP command with `err=-11`; the fixed profile left about `0xcd4` bytes.
- Gowin timing passed with setup/hold violated endpoints `0`; `LDR_20K.fs` was `7264087` bytes and `LDR_20K.bin` was `907418` bytes. Resource use remained about logic `3586/20736 17%`, registers `1809/16173 11%`, BSRAM `82%`, PLL `1/4`, DQS `2/9`.
- Volatile SRAM programming through `C:\workspace\verilog\20k\program20K_volatile_fs.bat` reported `User Code: 0x0000049A`, `Status Code: 0x00006020`, cost `16.61` seconds.
- UART post-programming evidence: `lidarsim ddr3 status=0107 base=c0000000`, `lidarsim ddr3 ok`, all UDP/TCP listeners started, UDP full-status/firmware replies returned `err=0`, and TCP command firmware reply returned `err=0`.
- Network smoke passed with direct discovery:
  `python C:/workspace/verilog/20k/lidar_switch_check.py --iface Ethernet --host-ip 192.168.2.146 --lidar-ip 192.168.2.240 --smoke --skip-data --no-net-config --smoke-timeout 8000`
- A short custom TCP data capture to `192.168.2.240:50100` received `192` valid `758`-byte MSOP frames in about four seconds.
- This verifies that the active LDR/lidar services survive DDR3 diagnostic startup. It still does not prove DDR3 as general system RAM, heap, LwIP pbuf storage, DMA memory, native byte-enable memory, or executable memory.

## rPLL ODIV_SEL trap (verified on R120 hardware 2026-07-03)

- `ODIV_SEL` accepts ONLY {2, 4, 8, 16, 32, 48, 64, 80, 96, 112, 128}.
  An invalid value (e.g. 12) passes GowinSynthesis and PnR with NO error or
  warning and produces a bitstream — but on silicon the PLL misbehaves so
  badly that the WHOLE design is disturbed, not just the PLL's own output
  (observed: an o_pll_10_66 with ODIV_SEL=12 for a secondary PSRAM domain
  made the soft-MCU fail `netif_add` at boot and garbled UART output;
  changing only ODIV_SEL to 8 fixed everything).
- Rule: fVCO = fCLKOUT * ODIV_SEL must be in the legal VCO range; pick ODIV
  from the valid list first, then check VCO (e.g. 66.67 MHz * 8 = 533 MHz).
- Symptom to recognize: a design that passes timing 0/0 but behaves insanely
  on hardware after adding/retuning a PLL — re-check every defparam against
  the datasheet value list before debugging anything else.
