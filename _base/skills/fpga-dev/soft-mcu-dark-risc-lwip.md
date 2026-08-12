# Soft MCU, DarkRISCV, And LwIP

Read this reference for tasks about `dark_risc`, soft-MCU firmware, LwIP, UDP parsing on FPGA, or the FPGA/MCU Ethernet boundary.

## Self-Learning Rule

- Keep this file as the durable memory for soft-MCU work. If a reusable detail is discovered and confirmed, update this file before the final response.
- Record only confirmed facts. Good evidence: exact command output, source file inspection, simulation result, hardware observation, packet capture, or user confirmation.
- Do not store guesses as facts. Mark unproven design ideas as "open" or keep them in the Obsidian checklist.
- Keep transient task state in `C:\Users\User\Мой диск\Obsidian\Проекты\FPGA soft MCU UDP LwIP.md`; keep stable procedures, maps, paths, commands, and traps here.
- After editing `SKILL.md` or this reference, validate the skill with:
  `python C:\Users\User\.codex\skills\.system\skill-creator\scripts\quick_validate.py C:\workspace\verilog\.agents\skills\fpga-dev`
- Build checks can modify tracked generated files inside the `dark_risc` submodule. Restore those artifacts unless the task intentionally updates the firmware image.

## Repositories And References

- Main FPGA repo: `C:\workspace\verilog`.
- Soft-MCU source repo: `C:\workspace\dark_risc`.
- Main repo submodule path: `C:\workspace\verilog\soft_mcu\dark_risc`.
- Repo LwIP submodule path: `C:\workspace\verilog\third_party\lwip`, pinned
  at `3d896ba0a37ff3ce73270ca5e230707fe47f60e3` on 2026-06-24.
- `dark_risc` source remote observed on 2026-06-17: `https://github.com/fufellen/dark_risc.git`, HEAD `25b18fe`.
- Submodule recovery gotcha verified on 2026-06-23: `.gitmodules` must use
  `https://github.com/fufellen/dark_risc.git` with `branch = master`.
  A local URL such as `C:/workspace/dark_risc` makes
  `git submodule update --init` fail on machines where that sibling repo is absent. The superproject
  gitlink must also point at a commit reachable from that remote; stale gitlink
  `d17585adfc8e5388444f87b81fa6832df30e9ea1` is not present in the GitHub
  remote as of 2026-06-23.
- R120 external-PSRAM branch gotcha verified on 2026-06-30:
  superproject branch `codex/r120-lidar-ext-ram-tcp-msop` currently points
  `soft_mcu/dark_risc` at `71a91ab76c2df171bb5020b12c9d86082ff886df`.
  That commit is the local `codex/r120-psram-lwip` submodule work and is not
  advertised by `https://github.com/fufellen/dark_risc.git` yet. The branch is
  locally regression-passing, but it is not clean-clone handoff-ready until the
  submodule commit is pushed or the gitlink is moved to a reachable commit
  without losing the PSRAM/TCP MSOP behavior. Use
  `powershell -NoProfile -ExecutionPolicy Bypass -File C:\workspace\verilog\scripts\check_submodule_reachability.ps1`
  as the handoff gate. Do not push the submodule or superproject unless the
  user explicitly asks.
  As an interim no-push handoff bridge, the superproject tracks
  `patches\dark_risc\r120-psram-lwip\r120-psram-lwip-dark_risc.bundle`
  plus the nine `format-patch --binary` files for review. Run
  `powershell -NoProfile -ExecutionPolicy Bypass -File C:\workspace\verilog\scripts\restore_r120_dark_risc.ps1`
  to fetch the exact commit from the bundle and check out the submodule at the
  gitlink SHA. This restores local reproducibility, but the remote reachability
  gate should still fail until the submodule commit is published or the gitlink
  is moved to a remote-backed SHA.
- Local STM32 F4 + LwIP reference: `C:\workspace\ToF-LIDAR-MCU-F401`, a clone of the
  corporate repo `github.com/ak-tech-electronics/ToF-LIDAR-MCU-F401`. The former local
  path `C:\workspace\stm32_f401ccu6_platformio` and its personal GitLab remote are gone
  (2026-08-10); the bench firmware lives on branch `gpx`.
- Repo LwIP source submodule: `C:\workspace\verilog\third_party\lwip`.
- Minimal LwIP raw UDP example: `C:\workspace\verilog\third_party\lwip\contrib\apps\udpecho_raw\udpecho_raw.c`.

## DarkRISCV Build On Windows

Verified on 2026-06-17:

- `make` is available at `C:\msys64\usr\bin\make.exe`.
- RISC-V toolchain is available at `C:\msys64\ucrt64\bin\riscv32-unknown-elf-gcc.exe`.
- ModelSim is available at `C:\intelFPGA\18.1\modelsim_ase\win32aloem\vsim.exe`.
- A clean firmware build succeeds from PowerShell with Windows-style tool paths:
  `& 'C:\msys64\usr\bin\make.exe' -C 'C:/workspace/verilog/soft_mcu/dark_risc/src' clean all CCPATH='C:/msys64/ucrt64/bin'`
- The successful default build produces `src\darksocv.mem` with 1987 32-bit words and `src\darksocv_uart.bin` with 7436 bytes.
- The linker may warn: `darksocv.o has a LOAD segment with RWX permissions`; this warning was present in the successful default build.
- Do not rely on `riscv32-unknown-elf-gcc` being present in MSYS bash `PATH`.
- A pure MSYS bash invocation using `/ucrt64/bin` failed during `boot.S` compilation in this environment. Prefer the verified PowerShell command above unless the environment has been fixed and re-verified.
- `src\darksocv.mem` is tracked by the `dark_risc` repo. A verification build changes it because the firmware embeds build-time data; restore it after exploratory builds if no firmware update is intended:
  `git -C C:\workspace\verilog\soft_mcu\dark_risc restore -- src/darksocv.mem`

Observed on 2026-06-24 in the current Codex desktop environment:

- `C:\msys64\usr\bin\make.exe`, `C:\msys64\ucrt64\bin\riscv32-unknown-elf-gcc.exe`,
  Gowin CLI/Programmer under `C:\workspace\verilog\bin`, repo submodule
  `third_party\lwip\src\include\lwip\init.h`, and
  `soft_mcu\dark_risc\src\Makefile` are present.
- `C:\msys64\ucrt64\bin\riscv64-unknown-elf-gcc.exe` is absent, but that is not
  a blocker while `RISCV_CROSS` auto-detects `riscv32-unknown-elf`.
- `scripts\check_build_env.ps1` and `20k\LDR_20K\build_gowin.cmd` both honor
  `GWSH`, `MSYS_MAKE`, `RISCV_CCPATH`, `RISCV_CROSS`, and optional
  `LWIP_ROOT`. By default LwIP comes from `third_party\lwip`. The wrapper
  checks required tools and LwIP before running `make clean`, so the tracked
  `src\darksocv.mem` is not deleted by a failed environment check.
- After explicit user approval on 2026-06-24, submodule commit
  `b54c45907035ea2bea54c38b643bcf159674990a` was pushed to GitHub
  `fufellen/dark_risc` on `master`; later `81ef46ad4bd6b29376e9f813889f897edfeac5c8`
  was pushed to make `lwipdemo` default to the superproject LwIP submodule.
  The superproject `dev_20k` was pushed to GitLab. A strict remote-backed clone
  at `C:\workspace\verilog_lwip_pull_check_20260624_114441` then passed
  `git submodule update --init --recursive`, `scripts\check_build_env.ps1`, and
  `20k\LDR_20K\build_gowin.cmd` with `BUILD_EXIT=0` and no `LWIP_ROOT`
  override.
- A previous MSYS2 `pacman -S --needed ... riscv64-unknown-elf ...` install
  attempt on this PC failed with package `404` errors and cache `.part` rename
  permission errors. If another PC hits that path, update/repair MSYS2 with
  `C:\msys64\usr\bin\bash.exe -lc "pacman -Syu"` before retrying package
  installation.

## Firmware Layout

- Firmware entry and boot UART loader: `src\boot.S`.
- Default application: `APPLICATION = darkshell` in `src\Makefile`.
- SPI demo application: set `APPLICATION = spidemo`; the Makefile then defines `SPI`, `SPIBB`, and `SPI3WIRE`.
- Toolchain defaults in `src\config.mk`: `CROSS=riscv32-unknown-elf`, `CCPATH=/ucrt64/bin`, `ARCH=rv32i_zicsr`, `ABI=ilp32`, little-endian, `-Os`, `-mno-div`, `-mcmodel=medany`.
- Linker script template: `src\darksocv.lds`; generated linker script: `src\darksocv.ld`.
- Linker memory: `MEM` origin `0x00000000`, length `MLEN` from `rtl\config.vh`.
- Linker places boot text first, then sets `. = 512`, then normal text/data. `_stack` is top of `MEM`; `_global` is `_data + 0x800`.
- Default upstream RTL config in `rtl\config.vh` used `MLEN 13` (8 KiB), but the local LwIP UDP bring-up requires `MLEN 15` (32 KiB). Other relevant defaults: `__3STAGE__`, `__HARVARD__`, `__PERFMETER__`, and default `BOARD_CK 100000000` when no board define is provided.
- For the 20K dev board, do not let the default 100 MHz board clock leak into UART/timer math if the SoC is clocked from the board's 50 MHz source or a derived PLL clock. Define the board clock/reset behavior explicitly in the integration.

## SoC Memory Map And IO

`rtl\darksocv.v` decodes `XADDR[31:30]`:

- `00`: BRAM through `darkram`.
- `01`: IO through `darkio`, base address `0x40000000`.
- `10`: SDRAM when enabled, otherwise unmapped readback `0xdeadbeef`.
- `11`: unmapped readback `0xdeadbeef`.
- `rtl\darkmac.v` is not an Ethernet MAC; it is the optional DSP multiply-accumulate custom instruction block.

`src\darklibc\include\io.h` maps `struct DARKIO` at `0x40000000`:

- `0x00`: `board_id`, `board_cm`, `core_id`, `irq`.
- `0x04`: UART status/fifo/baud (`uart.stat`, `uart.fifo`, `uart.baud`).
- `0x08`: LED register.
- `0x0c`: timer divider.
- `0x10`: microsecond counter.
- `0x14`: `iport`.
- `0x18`: `oport`.
- `0x1c`: SPI register block when `SPI` is enabled.

UART notes:

- `src\darklibc\stdio.c` implements `putchar`/`getchar` through `io->uart`.
- `putchar` waits while `io->uart.stat & 1`, then writes `io->uart.fifo`.
- `getchar` waits for `io->uart.stat & 2`, then reads `io->uart.fifo`.
- In simulation, `rtl\darkuart.v` prints UART TX to the simulator console and the `>` character can request simulation finish when interactive mode is disabled.

SPI notes:

- `rtl\darkspi.v` is an SPI master wrapper. It supports 16-bit and 24-bit transfers plus reserved 32-bit internal configuration writes.
- `src\spidemo\main.c` demonstrates both hardware SPI and bit-banged SPI over `OPORT/IPORT`.
- Do not assume SPI is the right FPGA/soft-MCU Ethernet transport. For an internal FPGA Ethernet path, a memory-mapped frame FIFO/register block may be simpler and faster.

## FPGA RX Path Facts

Confirmed on 2026-06-17 from source inspection:

- The existing FPGA RX chain `rmii_rx_strm -> crc32_check -> eth_rx_check -> rmii_rx` already converts RMII into Ethernet frame bytes.
- `eth_rx_check` outputs bytes without FCS and includes the Ethernet header, which matches the LwIP `ethernet_input()` frame shape.
- `eth_rx_check` supports destination-MAC filtering for local unicast, broadcast, and multicast.
- `rmii_rx` releases the buffered frame only after `ndl_crc_valid`; wrong CRC or MAC reject resets/drops the buffered frame through `fifo_sender_1`.
- `rmii_rx` does not expose explicit output frame start/end to downstream consumers. For soft-MCU/LwIP, either use `eth_rx_check` directly with a commit/drop-aware buffer, or extend the reusable RX path deliberately.

## DarkETH MMIO Prototype

Verified on 2026-06-17:

- New prototype peripheral: `C:\workspace\verilog\soft_mcu\dark_risc\rtl\darketh_mmio.sv`.
- Testbench: `C:\workspace\verilog\soft_mcu\dark_risc\sim\darketh_mmio_tb.sv`.
- It stores one complete RX Ethernet frame without preamble/SFD/FCS and exposes it through a memory-mapped byte-pop register. TX accepts a firmware-written frame and emits bytes for the FPGA Ethernet TX path.
- RX frame publication is explicit: stream bytes are buffered first, then `rx_frame_valid` commits the frame; `rx_frame_drop` drops it.
- Register map, relative to the future peripheral base:
  - `0x00 STATUS`: bit0 `rx_frame_available`, bit1 `rx_overflow`, bit2 `rx_dropped`, bit3 `rx_busy`, bit8 `rx_ready_for_frame`.
  - `0x04 RX_LEN`: committed frame length in bytes.
  - `0x08 RX_DATA`: read pops one byte in bits `[7:0]`; the last byte auto-releases the frame.
  - `0x0c RX_CTRL`: write bit0 releases current frame; write bit1 clears sticky overflow/drop flags.
  - `0x10 TX_STATUS`: bit0 `tx_ready_for_frame`, bit1 `tx_busy`, bit2 `tx_overflow`, bit3 `tx_done`, bit4 staged bytes equal `TX_LEN`.
  - `0x14 TX_LEN`: firmware-written TX frame length in bytes.
  - `0x18 TX_DATA`: write one TX byte in bits `[7:0]`.
  - `0x1c TX_CTRL`: write bit0 starts TX, bit1 aborts current/staged TX, bit2 clears TX done/overflow flags.
  - `0x20 CFG_MAC_LO`: firmware-written local MAC bits `[31:0]`, corresponding to bytes 2..5 of the Ethernet MAC.
  - `0x24 CFG_MAC_HI`: firmware-written local MAC bits `[47:32]`, corresponding to bytes 0..1 of the Ethernet MAC in bits `[15:0]`.
  - `0x28 CFG_FLAGS`: bit0 enables destination-MAC filtering, bit1 accepts broadcast, bit2 accepts multicast.
- Verified ModelSim 10.5b command:
  `vlib work; vlog -sv C:/workspace/verilog/soft_mcu/dark_risc/rtl/darketh_mmio.sv C:/workspace/verilog/soft_mcu/dark_risc/sim/darketh_mmio_tb.sv; vsim -c -t 1ns work.darketh_mmio_tb -do "run -all; quit -f"`
- Verification result after RX/TX expansion: `Errors: 0, Warnings: 0`, testbench output `TEST PASS: darketh_mmio rx tx`.
- Integrated into `darksocv` behind `DARKETH_MMIO`. When enabled and SDRAM is disabled, the peripheral occupies the `XADDR[31:30] == 2'b10` region, so the firmware base address is `0x80000000`.
- `sim\darksimv.v` injects a test frame `de ad be ef 08 00` into the `DARKETH_MMIO` RX stream.
- Firmware test application: `src\ethdemo`.
- Verified firmware build command:
  `& 'C:\msys64\usr\bin\make.exe' -C 'C:/workspace/verilog/soft_mcu/dark_risc/src' clean all APPLICATION=ethdemo NOBANNER=1 CCPATH='C:/msys64/ucrt64/bin'`
- Verified SoC simulation command:
  `C:\intelFPGA\18.1\modelsim_ase\win32aloem\vsim.exe -c -do "do C:/workspace/verilog/soft_mcu/dark_risc/sim/darksimv_modelsim.do; quit -f"`
- Verified SoC simulation output includes:
  - `Errors: 0` during compile and run.
  - `ethdemo len=6 data=deadbeef0800`.
  - `ethdemo status=0100`.
  - `ethdemo tx staged=11`.
  - `darketh tx data=deadbeef0800`.
  - `ethdemo tx status=09`.
  - `ethdemo ok`.
- The SoC simulation still reports existing missing-port warnings for optional/internal debug/IRQ/DLEN ports; these are not from `darketh_mmio`.
- 20K hardware integration now wires the RX/TX MMIO boundary into the existing RMII path for the `m20k_dev_uart_rmii_debug` bench target; keep this peripheral reusable and avoid adding task-specific Ethernet parser duplicates.

## DarkRISCV DDR3 MMIO Prototype

Verified on 2026-06-22 after the standalone nand2mario Tang Primer 20K DDR3 reference passed hardware UART tests:

- New diagnostic adapter: `C:\workspace\verilog\soft_mcu\dark_risc\rtl\darkddr3_mmio.sv`.
- Testbench: `C:\workspace\verilog\soft_mcu\dark_risc\sim\darkddr3_mmio_tb.sv`.
- Purpose: first CPU-facing DDR3 step only. It is a command/register MMIO peripheral for 32-bit diagnostic reads/writes through nand2mario's 16-bit user interface, not executable external RAM and not a heap/LwIP pbuf target yet.
- Register map:
  - `0x00 STATUS`: bit0 init done, bit1 write-level done, bit2 read-calib done, bit3 DDR busy, bit4 adapter/op busy, bit5 op done, bit6 op error, bit7 refresh pending, bit8 ready for command.
  - `0x04 ADDR`: nand2mario 16-bit word address for a 32-bit two-word operation.
  - `0x08 WDATA`: 32-bit write payload; low halfword writes to `ADDR`, high halfword writes to `ADDR+1`.
  - `0x0c RDATA`: 32-bit read payload assembled from `ADDR` and `ADDR+1`.
  - `0x10 CTRL`: bit0 start read32, bit1 start write32, bit2 start refresh, bit8 clear done, bit9 clear error.
  - `0x14 REFRESH_COUNT`: completed adapter refresh operations.
- The adapter waits for `write_level_done && read_calib_done`, uses one-cycle `rd`, `wr`, and `refresh` pulses, waits for `busy` to drop between halfword commands, and captures read data on `data_ready`.
- When instantiated from `darksocv` behind `DARKDDR3_MMIO`, the adapter refresh interval is overridden as ``REFRESH_INTERVAL_CYCLES = BOARD_CK / 128000``. This keeps the conservative refresh cadence roughly constant when a board top runs the CPU slower than the 100 MHz DDR pclk.
- The adapter accepts a new CPU command while in `ST_IDLE` or `ST_REFRESH_WAIT`, provided no command is already pending. This avoids an operation error if firmware observes ready and then auto-refresh starts just before `CTRL_START_*`; the command is queued and issued after refresh.
- Verified ModelSim 10.5b command:
  `vlib work; vlog -sv C:/workspace/verilog/soft_mcu/dark_risc/rtl/darkddr3_mmio.sv C:/workspace/verilog/soft_mcu/dark_risc/sim/darkddr3_mmio_tb.sv; vsim -c -t 1ns work.darkddr3_mmio_tb -do "run -all; quit -f"`
- Verification result after adding refresh-overlap coverage: `Errors: 0, Warnings: 0`, testbench output `TEST PASS: darkddr3_mmio`. The test queues a write of `0xcafe_babe` during refresh and verifies it completes without `OP_ERROR`.
- Verified SoC-level simulation on 2026-06-22:
  - `rtl\darksocv.v` can expose this adapter behind `DARKDDR3_MMIO` in the `XADDR[31:30] == 2'b10` slot, with the firmware base address `0x80000000`.
  - `sim\darksimv.v` has a `DARKDDR3_MMIO` mock nand2mario-style UI backend with write-level/read-calib completion, 16-bit writes/reads, data-ready, busy, and refresh behavior.
  - `sim\darksimv_modelsim.do` accepts `DARKSIMV_BASE_DEFINES` to replace the default `+define+DARKETH_MMIO`; use it when switching the SoC sim between Ethernet and DDR3 external-slot peripherals.
  - Firmware test application: `src\ddr3demo`. It writes `0x55667788` at word address `0x10`, reads it back, writes `0xa5a55a5a` at word address `0x40`, reads it back, runs a refresh, and prints `ddr3demo ok` before the final simulator finish marker.
- Verified firmware build command:
  `& 'C:\msys64\usr\bin\make.exe' -C 'C:/workspace/verilog/soft_mcu/dark_risc/src' clean all APPLICATION=ddr3demo NOBANNER=1 CCPATH='C:/msys64/ucrt64/bin'`
- Verified build result after removing mock-only preload dependence: `984 darksocv.mem`, `3424 bytes` in `darksocv_uart.bin`; the known RWX LOAD segment linker warning remains.
- Verified SoC simulation command:
  `$env:DARKSIMV_BASE_DEFINES='+define+DARKDDR3_MMIO'; $env:DARKSIMV_NOWAVES='1'; & 'C:\intelFPGA\18.1\modelsim_ase\win32aloem\vsim.exe' -c -do "do C:/workspace/verilog/soft_mcu/dark_risc/sim/darksimv_modelsim.do; quit -f"`
- Verified SoC simulation output includes:
  - `Errors: 0` during compile and run.
  - `dpram: unified BRAM w/ 16384x32-bit`.
  - `ddr3demo start`.
  - `ddr3demo status=0107`.
  - `ddr3demo rw addr=10 data=55667788`.
  - `ddr3demo rw addr=40 data=a5a55a5a`.
  - `ddr3demo refresh 12 to 13`.
  - `ddr3demo ok`.
- In this simulator, `darkuart` treats `>` as the finish marker when interactive mode is disabled. Do not print `>` in intermediate firmware text such as arrows; keep it only as the final completion marker.
- Verified standalone 20K DarkRISCV+DDR3 hardware target on 2026-06-22:
  - Project: `C:\workspace\verilog\20k\DARKRISCV_DDR3_20K`.
  - DDR controller: vendored `nand2mario/ddr3-tang-primer-20k` commit `a6d866d`.
  - CPU clocking: DarkRISCV on `27 MHz` board `sys_clk`; DDR3 controller on nand2mario PLL `clk/clk_x4`; bridge `src\darkddr3_ui_cdc.sv` crosses CPU command/response to DDR pclk.
  - `build_gowin.tcl` builds firmware before Gowin; the default is now `APPLICATION=ddr3memtest`, and the short smoke can still be selected with `DARKRISCV_DDR3_APP=ddr3demo`. The Tcl `exec` keeps `2>@1` on the `make` command because the successful RISC-V link prints the known RWX LOAD segment warning to stderr.
  - Gowin timing passed with setup/hold violated endpoints `0`; post-refresh-race-fix Max Frequency Summary was `clk 125.731 MHz` actual against `100 MHz`, `clk_x4 2016.129 MHz` against `400 MHz`, `sys_clk 46.957 MHz` against `27 MHz`.
  - Pin report confirmed `DDR3_nCS=P5/4`, constrained `Y`, `SSTL15`, `BANK_VCCIO=1.5`.
  - Volatile SRAM programming used `C:\workspace\verilog\20k\program20K_volatile_fs.bat` on `DARKRISCV_DDR3_20K.fs`, target `GW2A-18C`, `-r 2`; final post-fix result `User Code: 0x0000A843`, `Status Code: 0x00006020`, cost `14.11` seconds.
  - UART on `COM3` at `115200` printed 13 full hardware passes in 35 seconds: `ddr3demo status=0107`, `ddr3demo rw addr=10 data=55667788`, `ddr3demo rw addr=40 data=a5a55a5a`, refresh count increment, and `ddr3demo ok`, with no `timeout`, `mismatch`, or `error` lines.
  - A pre-fix repeated-run capture exposed `timeout read-done status=0147`; the accepted fix is the `ST_REFRESH_WAIT` command-queue behavior above plus testbench coverage.
- Broader diagnostic firmware now exists at `C:\workspace\verilog\soft_mcu\dark_risc\src\ddr3memtest`. It exercises the same CPU MMIO DDR3 adapter with data-bus walking ones/zeros, address-line alias checks, sparse boundary probes, read-after-write, address-as-data, inverted-address, checkerboard, PRBS/LFSR, MATS/March-like order-sensitive passes, stride/random access, a safe software subword RMW model, and retention/refresh delay.
- Critical firmware polling rule for `darkddr3_mmio`: after writing `CTRL_CLEAR_DONE | CTRL_CLEAR_ERROR`, wait until both `STATUS_OP_DONE` and `STATUS_OP_ERROR` read back as `0` before issuing the next `CTRL_START_*`. Fast firmware that starts a read/write immediately after clear can observe stale `OP_DONE`/`RDATA`; this was reproduced as a false `ddr3memtest` mismatch before the helper was fixed. Keep `src\ddr3demo` and future test apps on the same helper pattern.
- Verified `ddr3memtest` ModelSim profile on 2026-06-22 built as `2036 darksocv.mem` / `7632` UART bytes and reached `ddr3memtest ok` with `low-probe warnings=00`; the existing optional-port simulation warnings remain unrelated.
- Verified `ddr3memtest` hardware profile on 2026-06-22 built as `3012 darksocv.mem` / `11536` UART bytes. Gowin generated `20k\DARKRISCV_DDR3_20K\impl\pnr\DARKRISCV_DDR3_20K.fs` (`7264087` bytes), timing still had setup/hold violated endpoints `0`, and volatile SRAM programming through `20k\program20K_volatile_fs.bat` reported `User Code: 0x0000A843`, `Status Code: 0x00006020`, cost `13.41` seconds.
- Clean UART capture `C:\Users\User\AppData\Local\Temp\ddr3memtest_uart_clean_20260622_192405.log` ran repeated full hardware passes for about 90 seconds. Each pass reported all phases `ok`, including `retention ok` and final `ddr3memtest ok`; `mismatch_count=0`, `timeout_count=0`, `error_count=0`.
- The same capture consistently had a nonfatal `low-probe` warning at DDR3 16-bit word address `0x00`, while the main verified test window starts at `DDR3MEMTEST_BASE_ADDR=0x30` and sparse address probes pass out to bit 25. Treat address `0x00` behavior as an open diagnostic until explained; do not claim the whole DDR3 address space as general RAM from this result alone.
- The standalone DarkRISCV+DDR3 top ties `.UART_RXD(1'b1)`, so the upstream boot UART loader can print `u.....b` but cannot receive uploaded firmware. Rebuild the bitstream to change firmware unless the top is later changed to wire UART RX into DarkRISCV.
- In the active `m20k_dev_uart_rmii_debug` / `20k\LDR_20K` DDR3 diagnostic profile, `darketh_mmio` still owns CS2 at `0x80000000` and `darkddr3_mmio` is mapped to CS3 at `0xc0000000` when both `DARKETH_MMIO` and `DARKDDR3_MMIO` are defined. This keeps the existing Ethernet/LwIP firmware path alive while adding DDR3 diagnostics.
- Verified LDR_20K Ethernet+DDR3 SoC simulation on 2026-06-22 used:
  `$env:DARKSIMV_BASE_DEFINES='+define+DARKETH_MMIO +define+DARKDDR3_MMIO'; $env:DARKSIMV_DEFINES='+define+DARKETH_LWIP_FRAME'; $env:DARKSIMV_NOWAVES='1'; & 'C:\intelFPGA\18.1\modelsim_ase\win32aloem\vsim.exe' -c -do "do C:/workspace/verilog/soft_mcu/dark_risc/sim/darksimv_modelsim.do; quit -f"`
  It passed with `Errors: 0`, `fwloader sim ok`, `lidarsim ddr3 status=0107 base=c0000000`, `lidarsim ddr3 ok refresh=af to b0`, UDP control replies, and `lidarsim ok`.
- Verified LDR_20K Ethernet+DDR3 hardware on 2026-06-22 built as `14724 darksocv.mem` / `58384` bytes in `darksocv_uart.bin`. The DDR3 diagnostic firmware profile reduces LwIP memory pressure only under `LIDARSIM_DDR3_DIAG`: smaller `MEM_SIZE`, pbuf pool, TCP send buffer, one MSOP TX buffer, and smaller control/firmware buffers. This left `.bss` ending around `0xf32c`, about `0xcd4` bytes below `_stack=0x10000`.
- Before that RAM profile, the same DDR3+LwIP image left only about `0x1ac` bytes of stack headroom. Hardware accepted discovery/UDP, then TCP command printed `lidarsim tcp cmd=7e rw=0 reply=18 err=-11`, after which repeated application restarts printed `lidarsim netif fail`. Treat `err=-11` plus later `netif fail` in this tiny image as a likely stack/heap/LwIP-state corruption symptom before changing DDR3 HDL.
- The fixed hardware image was programmed to volatile SRAM with `C:\workspace\verilog\20k\program20K_volatile_fs.bat C:\workspace\verilog\20k\LDR_20K\impl\pnr\LDR_20K.fs`; programmer evidence was `User Code: 0x0000049A`, `Status Code: 0x00006020`, cost `16.61` seconds. UART then showed `lidarsim ddr3 ok`, all UDP/TCP listeners, UDP full-status and firmware replies with `err=0`, and TCP command firmware reply `err=0`.
- Hardware network check for that image passed:
  `python C:/workspace/verilog/20k/lidar_switch_check.py --iface Ethernet --host-ip 192.168.2.146 --lidar-ip 192.168.2.240 --smoke --skip-data --no-net-config --smoke-timeout 8000`
  A separate TCP data capture from `192.168.2.146` to `192.168.2.240:50100` received `192` valid `758`-byte `ff fe ... ff 9b` MSOP frames in about four seconds. This proves the current lidar services survive DDR3 diagnostic startup, not DDR-as-heap or DDR-as-pbuf storage.

## LwIP Porting Direction

- Use the STM32 project's LwIP profile as the first local reference: `NO_SYS=1`, IPv4, ARP, UDP, raw API, no sockets, no netconn, no TCP.
- The STM32 project keeps LwIP under `src\lwip`, has `src\lwipopts.h`, `src\arch\cc.h`, `src\arch\sys_arch.h`, and `src\sys_arch.c`.
- The STM32 project's `mac_sender` exchanges full Ethernet frames without preamble/SFD/CRC over SPI. This is the desired packet shape for an LwIP `netif` boundary.
- For FPGA soft-MCU LwIP RX, pass a complete Ethernet frame without preamble, SFD, or FCS into a pbuf and then into `ethernet_input`.
- For TX, implement `netif->linkoutput` so LwIP hands a complete Ethernet frame to the FPGA Ethernet TX path.
- Implement `sys_now()` from the SoC timer, for example from `io->timeus / 1000`, after verifying the board clock configuration.
- Expect the default 8 KiB `MLEN` to be too small for a useful LwIP UDP build. Verify map size before raising `MLEN` or adding RAM.
- Keep HDL responsible for RMII, CRC/FCS, frame buffering, link/MAC filtering, and runtime config registers. Keep ARP/IP/UDP parsing in soft-MCU firmware through LwIP unless hardware acceleration is explicitly required.
- MAC address, IP address, UDP ports, multicast enables/groups, and similar fields should be runtime-configurable. HDL parameters are acceptable as reset defaults or temporary bring-up values only.

## LwIP Demo Firmware

Verified on 2026-06-17:

- Firmware application: `C:\workspace\verilog\soft_mcu\dark_risc\src\lwipdemo`.
- It uses the repo LwIP submodule at `third_party\lwip\src` instead of copying the stack into `dark_risc` or depending on a local-only checkout.
- Minimal source set used by `lwipdemo`: `core/init.c`, `def.c`, `inet_chksum.c`, `ip.c`, `mem.c`, `memp.c`, `netif.c`, `pbuf.c`, `stats.c`, `sys.c`, `timeouts.c`, `udp.c`; IPv4 `etharp.c`, `ip4.c`, `ip4_addr.c`; netif `ethernet.c`.
- Port headers live under `src\lwipdemo\arch`: `cc.h`, `sys_arch.h`, `perf.h`, `stdint.h`, `stddef.h`, `stdlib.h`, `string.h`.
- `darklibc` has no standard `stdlib.h`; `lwipdemo` supplies a local header for `atoi`.
- `darklibc` lacks `uintptr_t`/`intmax_t`/`ptrdiff_t` in its small standard headers; `lwipdemo` supplies local `stdint.h` and `stddef.h`.
- LwIP's `def.c` required `memmove`; `lwipdemo\compat.c` supplies it locally.
- `lwipdemo` options: `NO_SYS=1`, IPv4, ARP, UDP raw API, no TCP, no sockets, no netconn, no DNS, no DHCP.
- `sys_now()` is implemented from `io->timeus / 1000`.
- RX path: `darketh_mmio` RX frame -> `pbuf_alloc(PBUF_RAW, len, PBUF_POOL)` -> `ethernet_input`.
- TX path: `netif->linkoutput` writes complete Ethernet frames to `darketh_mmio` `TX_LEN`/`TX_DATA`/`TX_CTRL`.
- The first `MLEN=13` build failed at link with `region MEM overflowed by 17732 bytes`. Raising `MLEN` to 15 made the build fit.
- Verified build command:
  `& 'C:\msys64\usr\bin\make.exe' -C 'C:/workspace/verilog/soft_mcu/dark_risc/src' clean all APPLICATION=lwipdemo NOBANNER=1 CCPATH='C:/msys64/ucrt64/bin'`
- Initial verified build result before runtime-config refactor: `5658 darksocv.mem`, `22120 bytes` in `darksocv_uart.bin`; linker still reports the known RWX LOAD segment warning.
- After moving reset defaults into `runtime_config`, the verified build result is `5720 darksocv.mem`, `22368 bytes` in `darksocv_uart.bin`; the same RWX LOAD segment warning remains.
- `src\lwipdemo\main.c` keeps reset defaults in one `runtime_config` structure: local MAC `02:20:20:20:20:01`, IPv4 `192.168.20.20`, netmask `255.255.255.0`, gateway `192.168.20.1`, UDP listen port `5005`.
- `darketh_netif_init()` copies `runtime_config.mac` into `netif->hwaddr`; `main()` derives `ipaddr`, `netmask`, and `gw` from `runtime_config`; `udp_server_init()` binds to `runtime_config.udp_port`.
- `lwipdemo` has a nonblocking UART control path on top of the existing `io->uart` status/fifo registers. Supported line commands: `show`/`cfg`, `mac <12 hex digits or colon-separated bytes>`, `ip <a.b.c.d>`, `mask <a.b.c.d>`/`netmask <a.b.c.d>`, `gw <a.b.c.d>`/`gateway <a.b.c.d>`, `port <0..65535>`, and `apply`.
- After a valid UART config command, firmware applies the current `runtime_config` to the LwIP netif, updates `netif.hwaddr`, calls `netif_set_addr()`, removes the old UDP PCB, and binds a new PCB to `runtime_config.udp_port`.
- Firmware also applies the same runtime MAC address to `darketh_mmio` hardware filter registers: `cfg_mac_lo`, `cfg_mac_hi`, and `cfg_flags = 0x7` for MAC filter enabled with broadcast and multicast accepted. HDL parameters remain reset defaults only.
- The firmware main loop stays alive after the first UDP packet. It prints `lwipdemo ok` and `>` for simulation completion, but on hardware it keeps polling UART, RX frames, and LwIP timeouts.
- The current `darkuart` RTL has no enabled RX queue (`__UARTQUEUE__` is commented out). In the verified ModelSim UART-config stimulus, commands are sent one line at a time with pauses between lines to avoid overrunning the single-byte RX buffer while firmware prints apply diagnostics.
- After adding UART runtime config, the verified build result is `6230 darksocv.mem`, `24408 bytes` in `darksocv_uart.bin`; the same RWX LOAD segment warning remains.
- After adding runtime MAC-filter registers, the verified build result is `6262 darksocv.mem`, `24536 bytes` in `darksocv_uart.bin`; the same RWX LOAD segment warning remains.
- `sim\darksimv_modelsim.do` accepts extra compile defines through `DARKSIMV_DEFINES`.
- Verified LwIP SoC simulation command:
  `$env:DARKSIMV_DEFINES='+define+DARKETH_LWIP_FRAME'; C:\intelFPGA\18.1\modelsim_ase\win32aloem\vsim.exe -c -do "do C:/workspace/verilog/soft_mcu/dark_risc/sim/darksimv_modelsim.do; quit -f"`
- Verified LwIP SoC simulation output includes:
  - `Errors: 0` during compile and run.
  - `dpram: unified BRAM w/ 8192x32-bit`.
  - `lwipdemo cfg mac=022020202001 ip=192.168.20.20 port=5005`.
  - `lwipdemo cfg apply=0 port=5005` followed by `lwipdemo cfg mac=022020202002 ip=192.168.20.21 port=5005`.
  - `lwipdemo cfg apply=0 port=5006` followed by `lwipdemo cfg mac=022020202002 ip=192.168.20.21 port=5006`.
  - `lwipdemo udp bind=0 port=5005`.
  - `lwipdemo udp len=4 port=4000 data=70696e67`.
  - Runtime-configured echo frame after UART commands: `darketh tx data=02aabbccddee02202020200208004500002000000000ff11115ec0a81415c0a8140a138e0fa0000c546770696e67`.
  - `lwipdemo udp echo=0`.
  - `lwipdemo ok`.
- In the LwIP simulation, feed an ARP request before the UDP test frame. LwIP does not learn the sender MAC from the IPv4 packet alone in this configuration; ARP fills the cache so the UDP echo leaves as a UDP frame instead of only triggering an ARP request.
- When injecting multiple frames in `darksimv.v`, wait for `ETH_RX_FRAME_AVAILABLE` and then `ETH_RX_READY_FOR_FRAME`. Waiting only for `ETH_RX_READY_FOR_FRAME` immediately after `rx_frame_valid` can race before nonblocking assignments publish the frame and can cause overflow/drop on the second injected frame.

## 20K Dev Board LwIP Hardware Result

Verified on 2026-06-17 on the 20K dev board:

- Active bench top: `m20k_dev_uart_rmii_debug` in `C:\workspace\verilog\src\main\m20k_dev_uart_deadbeef.sv`.
- The board clock for this target is treated as 50 MHz through `M20K_DEV_BOARD`; do not let the upstream `BOARD_CK=100000000` default leak into UART/timer math.
- `C:\workspace\verilog\20k\LDR_20K\build_gowin.cmd` first builds `lwipdemo` through `C:\msys64\usr\bin\make.exe`, then Gowin embeds the fresh `soft_mcu\dark_risc\src\darksocv.mem`.
- Full build-and-program command:
  `& 'C:\workspace\verilog\20k\build_and_program20K_volatile.bat'`
- Programming target: `GW2A-18C`, volatile SRAM option `-r 2`, bitstream `C:\workspace\verilog\20k\LDR_20K\impl\pnr\LDR_20K.fs`.
- Use the default programmer speed for normal work. Slowing the programmer with manual frequency options did not solve the earlier `Cable lost!` symptom; after the FTDI cable was replugged and both channels were healthy, the default-speed SRAM program succeeded.
- Successful default-speed programming evidence: `User Code: 0x0000E1FE`, `Status Code: 0x00006020`, cost about 13.6 seconds.
- UART on `COM3` at 115200 8N1 answers `cfg` with `lwipdemo cfg mac=022020202001 ip=192.168.20.20 port=5005`.
- Windows test adapter: `Ethernet 5`, D-Link DUB-E100, 100 Mbps, MAC `F4-8C-EB-4B-6F-F0`.
- Scapy/Npcap raw Ethernet test from host MAC `f4:8c:eb:4b:6f:f0`, host IP `192.168.20.10`, board MAC `02:20:20:20:20:01`, board IP `192.168.20.20` proved:
  - ARP request to `192.168.20.20` receives ARP reply from `02:20:20:20:20:01`.
  - UDP to board MAC and port `5005` echoes payload `ping` from board port `5005` back to source port `4000`.
  - UDP to board MAC but wrong port `5006` reaches RX/LwIP but produces no UDP echo.
  - UDP to unrelated unicast destination MAC `02:aa:bb:cc:dd:ee` produces no board response, proving the hardware MAC reject path.
  - UDP with multicast destination MAC `01:00:5e:00:00:01` and board IP/port is accepted when sent with enough spacing for the one-frame MMIO RX buffer; the board echoed payload `mcok` from port `5005` to source port `4011`.
- UART evidence for the hardware path included `lwipdemo rx len=60 status=01`, `lwipdemo udp len=4 port=4010 data=6f6b6179`, `lwipdemo udp len=4 port=4011 data=6d636f6b`, `lwipdemo tx len=46 status=09`, and `lwipdemo udp echo=0`.
- When testing multiple packets manually, leave a pause between frames or wait for the firmware to release the MMIO RX frame. A too-fast follow-up packet can look like a multicast/filter failure while the single-frame RX buffer is still occupied.

## 20K Dev Board Lidar Simulator Result

Verified on 2026-06-18 on the 20K dev board:

- The lidar simulator still reuses `src\lwipdemo` and the existing soft-MCU/RMII/MMIO path; no new HDL parser, interface, board top, or constraint target was added for the protocol layer.
- The firmware enables LwIP TCP in addition to UDP and implements three server ports: UDP discovery/control on `50103`/`50101`, TCP command on `50101`, and TCP MSOP data on `50100`.
- Default identity: MAC `02:20:20:20:20:01`, IP `192.168.20.20`, host/remote IP `192.168.20.10`, model `R120_FAKE`, firmware string `pegus_1`.
- The 32 KiB `MLEN=15` build was too small for the TCP lidar simulator (`region MEM overflowed by 29632 bytes`). Raising `MLEN` to 16 (64 KiB) made the firmware fit; verified clean build result: `12800 darksocv.mem`, `50688 bytes` in `darksocv_uart.bin`, with the known RWX LOAD segment warning.
- `src\darksocv.mem` embeds build-time data and can become dirty after a rebuild. Restore it after purely exploratory builds unless the firmware image update is intentional.
- Fast ModelSim command for this firmware:
  `$env:DARKSIMV_DEFINES='+define+DARKETH_LWIP_FRAME'; $env:DARKSIMV_NOWAVES='1'; & 'C:\intelFPGA\18.1\modelsim_ase\win32aloem\vsim.exe' -c -do "do C:/workspace/verilog/soft_mcu/dark_risc/sim/darksimv_modelsim.do; quit -f"`
- Verified ModelSim output included `Errors: 0`, `dpram: unified BRAM w/ 16384x32-bit`, `lidarsim cfg mac=022020202001 ip=192.168.20.20 data=50100 cmd=50101 discovery=50103 model=R120_FAKE fw=pegus_1`, discovery reply `err=0`, UDP command reply `err=0`, and `lidarsim ok`.
- Full build-and-program command remained:
  `& 'C:\workspace\verilog\20k\build_and_program20K_volatile.bat'`
- Programming target: `GW2A-18C`, volatile SRAM option `-r 2`, default programmer speed. Successful 2026-06-18 programming evidence: `User Code: 0x00005B6C`, `Status Code: 0x00006020`, cost about 15.4 seconds.
- Gowin output after this build: `C:\workspace\verilog\20k\LDR_20K\impl\pnr\LDR_20K.fs`, size `7264087` bytes, report timestamp `Thu Jun 18 11:15:43 2026`.
- PnR resource report for the lidar simulator: logic `3011/20736 14%`, registers `1089/16173 6%`, CLS `1917/10368 18%`, BSRAM `82%` (`SDPB 6`, `DPB 32`), PLL `0/4`.
- Internal BSRAM is enough for the verified lidar simulator build. Do not pull in DDR3 just for this milestone; if larger TCP buffers, captured images, or point clouds push BRAM over budget, look for and reuse existing DDR3 examples before adding a new memory controller.
- UART on `COM3` at 115200 8N1 answered `cfg` with `lidarsim cfg mac=022020202001 ip=192.168.20.20 data=50100 cmd=50101 discovery=50103 model=R120_FAKE fw=pegus_1`.
- Windows could not add a secondary `192.168.20.10/24` address to `Ethernet 5` without administrator rights (`New-NetIPAddress: Access is denied`). Raw Scapy/Npcap tests still work by sending Ethernet frames with host MAC `f4:8c:eb:4b:6f:f0` and source IP `192.168.20.10`.
- The user's networks can contain at least one real lidar besides the FPGA board. Broadcast discovery is allowed and may return multiple devices. For hardware tests, bind captures/sends to the intended adapter when possible, collect all replies, filter the FPGA board by MAC `02:20:20:20:20:01` and model `R120_FAKE`, and use direct raw frames for `NET_CONFIG`/write commands when a reproducible bench-only target is needed.
- Scapy/Npcap hardware checks on `Ethernet 5` proved:
  - ARP request for `192.168.20.20` receives ARP reply from `02:20:20:20:20:01`.
  - Broadcast UDP discovery to port `50103` with payload `FF FE LIDAR_REQS 00 01 11 FF 9B` receives an 80-byte `LIDAR_RESP` reply with model `R120_FAKE`, MAC `02:20:20:20:20:01`, IP `192.168.20.20`, data port `50100`, command port `50101`, discovery port `50103`.
  - A follow-up multi-device-safe discovery check collected all `LIDAR_RESP` packets for a time window on `Ethernet 5`; one response was present in that bench setup, and filtering by Ethernet source MAC plus payload model/IP selected the FPGA board.
  - UDP `FULL_STATUS` command on port `50101` receives a 25-byte fixed reply.
  - UDP varlen `LIDAR_FIRMWARE (0x7e)` command on port `50101` receives `pegus_1`.
  - Raw TCP handshake to command port `50101` succeeds and varlen `LIDAR_FIRMWARE` returns `pegus_1`.
  - Raw TCP handshake to data port `50100` succeeds. The MSOP stream arrives split by TCP MSS into `256, 256, 246` byte segments per packet; ACK segments while capturing and reassemble the TCP stream.
  - Reassembled MSOP packets are 758 bytes, start `FF FE`, end `FF 9B`, protocol version/type `1/1`, point count `180`, angle resolution `2000`, distance byte count `3`, intensity enabled `1`, echo mode/count `1/1`. Consecutive frames increment the frame number and shift sample distances, proving the rotating-square style telemetry changes over time.
- UART evidence after network tests included `lidarsim discovery rx len=17 port=4000`, `lidarsim discovery reply err=0`, `lidarsim udp cmd=00 rw=0 reply=25 err=0`, `lidarsim udp cmd=7e rw=0 reply=18 err=0`, `lidarsim tcp command connected`, `lidarsim tcp cmd=7e rw=0 reply=18 err=0`, and `lidarsim tcp data connected`.
- `lconf` now has a non-GUI smoke CLI for this simulator: `C:\workspace\lidar\lconf\bin\Release\lconf.exe --lidar-smoke --smoke-host <ip> --smoke-local-host <pc-ip> --smoke-timeout 5000`. It collects discovery replies as a list, filters the expected FPGA board by model/MAC/IP, checks UDP `FULL_STATUS`, UDP/TCP `LIDAR_FIRMWARE`, and validates two TCP MSOP frames through the existing `msop_parser`.
- Verified 2026-06-18 with the FPGA temporarily runtime-configured to `192.168.15.20` for normal Windows sockets and restored to `192.168.20.20` afterwards. Debug and Release builds of `lconf` passed `--lidar-smoke`; Release needed `windeployqt --release C:\workspace\lidar\lconf\bin\Release\lconf.exe` before it could run outside the Qt build environment.
- Verified Release smoke output included `PASS discovery`, `PASS udp-full-status`, `PASS udp-firmware text=pegus_1`, `PASS tcp-command`, two MSOP frames of 758 bytes with 180 points and `angle_res=2000`, and final `PASS lidar-smoke`.

Verified on 2026-06-19 through the shared `192.168.2.0/24` switch network:

- Windows switch adapter: `Ethernet`, IP `192.168.2.146/24`, MAC `88:88:88:88:87:88`; direct bench adapter `Ethernet 5` no longer saw the board after the cable move.
- Selected FPGA runtime IP: `192.168.2.240`; ARP before configuration had no reply, proving the address was not occupied in this test window.
- Helper script: `C:\workspace\verilog\20k\lidar_switch_check.py`. Verified command:
  `python C:/workspace/verilog/20k/lidar_switch_check.py --iface Ethernet --host-ip 192.168.2.146 --lidar-ip 192.168.2.240 --smoke`
- The helper sent exact-MAC raw `NET_CONFIG` to `02:20:20:20:20:01` with lidar IP `192.168.2.240`, host IP `192.168.2.146`, data port `50100`, command port `50101`.
- ARP after `NET_CONFIG`: `192.168.2.240 -> 02:20:20:20:20:01`; `Ethernet 5` no longer answered for `192.168.15.20` or `192.168.20.20`.
- Full switch `lconf --lidar-smoke` passed: discovery `R120_FAKE`, firmware `pegus_1`, UDP full-status, UDP firmware, TCP command, and TCP MSOP data. Data frames were 758 bytes, 180 points, `angle_res=2000`, distance byte count `3`, echo `1/1`.
- Broadcast discovery on `255.255.255.255` in the shared network returned one matching FPGA response and the simulator stayed alive afterwards:
  `python C:/workspace/verilog/20k/lidar_switch_check.py --iface Ethernet --host-ip 192.168.2.146 --lidar-ip 192.168.2.240 --no-net-config --smoke --skip-data --broadcast-discovery`.
- Negative filter check with wrong expected MAC `02:20:20:20:20:02` failed as expected (`FAIL discovery`, no matching response), proving the smoke path does not accept an arbitrary/first response when MAC/model/IP filters do not match.

Troubleshooting notes from the 2026-06-19 `NET_CONFIG`/post-reconfiguration ModelSim work:

- Before blaming the FPGA, LwIP, or hardware, inspect the exact testbench frame bytes and ports. A simulator packet can silently hit the wrong UDP PCB if the destination port bytes are swapped: discovery is `50103` (`0xc3b7`), command/control is `50101` (`0xc3b5`), and data/MSOP is `50100` (`0xc3b4`). `NET_CONFIG` is a command packet and should go to the command/control port unless the real protocol source proves otherwise.
- Treat `sdram: unmapped addr=ff...` in this DarkRISCV simulation as a likely bad pointer, return-address corruption, or stack/heap collision symptom first. Do not jump straight to DDR3 or HDL changes; inspect `src\darksocv.map`, compare `_edata` against `_stack`, and estimate stack headroom before changing memory architecture.
- The 64 KiB LwIP lidar simulator image is stack-sensitive. Large local callback buffers such as `packet[320]` and `reply[320]`, nested LwIP calls, and `printf` can consume the remaining top-of-RAM stack quickly. If `_edata` is close to `0x10000`, first reduce LwIP heap/pool pressure, move buffers deliberately, or simplify callback stack use, then rerun ModelSim.
- Source inspection of the local LwIP tree shows `netif_set_addr()` and `netif_set_up()` can issue IPv4 reports/gratuitous ARP on an up Ethernet netif. In this one-frame MMIO Ethernet model, runtime IP reconfiguration should be tested carefully around those reports; prefer a deferred, controlled apply path and verify with ModelSim before hardware programming.
- Verified on 2026-06-19 in ModelSim: broadcast `NET_CONFIG` must be received by the command/control UDP PCB, so set `SOF_BROADCAST` on the command PCB as well as discovery. Send the `NET_CONFIG` ACK first, mark reconfiguration pending, and apply the new MAC/IP/ports from the main loop. For this one-frame MMIO model, update the netif IPv4 fields directly and call `etharp_cleanup_netif(&fpga_netif)` before changing them; this avoids the post-reconfiguration `sdram: unmapped addr=ff...` failure and lets the board answer ARP plus `FULL_STATUS` at the new IP.
- Verified on 2026-06-19 from real MCU source (`C:\workspace\ToF-LIDAR-R\Common\LidarDiscovery\LidarDiscovery.cpp`): discovery replies are sent to limited broadcast `255.255.255.255:<peer_port>`, not to the requester's unicast IP. Keep that broadcast reply in the simulator for protocol compatibility.
- Verified on 2026-06-19 in ModelSim and on 20K hardware: a broadcast-only reply appears on the wire, but Windows/Qt sockets bound to a concrete adapter IP can miss limited-broadcast replies. The simulator therefore sends both the real broadcast reply and a compatibility direct reply to the requester's Ethernet source MAC/IP/UDP port.
- Do not implement that direct discovery reply through a cold LwIP `udp_sendto()` unicast path. On the first packet it can emit ARP instead of an immediately usable UDP response. Capture the source MAC/IP from the just-received Ethernet/IP frame and send the direct compatibility reply as a complete Ethernet/IP/UDP frame through the existing `darketh_linkoutput` path.
- Verified on 2026-06-19 on Windows `Ethernet` in the shared `192.168.2.0/24` network: ordinary socket broadcast discovery can present two back-to-back identical RX frames to the one-frame MMIO buffer. If `ETH_STATUS_RX_AVAILABLE` is set and `rx_len` is valid, process the current frame even when sticky overflow/drop flags are set; clear those flags after processing. Dropping the available frame merely because overflow is set can make `poll_lidar_discovery.py` and `lconf --lidar-smoke` miss the FPGA while raw Scapy single-frame discovery still works.
- After a `programmer_cli -r 1` reload from external FLASH, wait a couple of seconds before the first socket discovery or `lconf --lidar-smoke`. An immediate first smoke can race startup and report zero discovery responses; a repeat after the board answers ARP/discovery passes.
- Verified on 2026-06-19 after a physical board power-cycle with the Ethernet cable in the shared `192.168.2.0/24` switch network: the external-FLASH image booted with MAC `02:20:20:20:20:01`, IP `192.168.2.240`, model `R120_FAKE`, firmware `pegus_1`; `poll_lidar_discovery.py` found it by `255.255.255.255` broadcast and full `lconf --lidar-smoke` passed through TCP MSOP data.

MSOP smoothness notes verified on 2026-06-19:

- The visible rotating-square stutter in `lconf` matched the original firmware throttle: `service_msop_tcp()` emitted one 758-byte MSOP frame every `50 ms`, so the GUI showed about `15 KiB/s` of MSOP data. The old square phase also advanced from `msop_frame_num`, so the apparent motion was tied to the dropped/slow frame cadence.
- Reducing the application period to `20 ms` is not enough by itself when using `tcp_write(..., TCP_WRITE_FLAG_COPY)` with `TCP_MSS=256` and `TCP_SND_BUF=1024`. One 758-byte frame consumes most of the send buffer and is split into three TCP segments; on the Windows client this still measured about `20 FPS`, with MSOP timestamps advancing by `50 ms`, because the next whole frame could not be queued until ACK/backpressure cleared.
- The verified smooth path keeps the shape phase time-based, not frame-count-based: `phase = ((sys_now() % 1500) * 90) / 1500`, while `LIDARSIM_MSOP_PERIOD_MS=20`.
- The verified TCP data stream disables Nagle on the data PCB, uses `TCP_MSS=512`, `TCP_WND=2*TCP_MSS`, `TCP_SND_BUF=4*TCP_MSS`, and `TCP_OVERSIZE=0`.
- The verified MSOP sender uses two static 758-byte TX buffers with `tcp_write(..., 0)` zero-copy and a `tcp_sent()` ACK callback before reusing a buffer. Keep ordinary command/firmware replies on `TCP_WRITE_FLAG_COPY`; zero-copy is only for the continuous MSOP stream with stable static buffers.
- Current verified firmware build for this MSOP fix: `14737 darksocv.mem`, `58436` bytes in `darksocv_uart.bin`. Map headroom from the end of common data around `0xf9a0` to `_stack=0x10000` is about `0x660` bytes, so keep future stack/local buffers small and re-run ModelSim after changes.
- Verified ModelSim command remained `$env:DARKSIMV_DEFINES='+define+DARKETH_LWIP_FRAME'; $env:DARKSIMV_NOWAVES='1'; & 'C:\intelFPGA\18.1\modelsim_ase\win32aloem\vsim.exe' -c -do "do C:/workspace/verilog/soft_mcu/dark_risc/sim/darksimv_modelsim.do; quit -f"` and passed with `Errors: 0`, `fwloader sim ok`, and `lidarsim ok`.
- Verified SRAM hardware load used `programmer_cli.exe -d GW2A-18C -r 2 -f C:\workspace\verilog\20k\LDR_20K\impl\pnr\LDR_20K.fs` and completed with `User Code: 0x00006EAC`, `Status Code: 0x00006020`, cost `15.24` seconds.
- Verified 20K hardware on `192.168.2.240`: `poll_lidar_discovery.py` found `R120_FAKE` and `lconf --lidar-smoke --smoke-host 192.168.2.240 --smoke-local-host 192.168.2.146 --smoke-discovery-target 255.255.255.255 --smoke-timeout 5000` passed discovery, UDP status/firmware, TCP command, and TCP MSOP data.
- Verified 15-second TCP MSOP stress after the fix: `751` frames, `50.00 FPS`, `37.06 KiB/s`, RX intervals average `20.00 ms`, trimmed interval range about `19.50..20.56 ms`, MSOP timestamp intervals average `20.00 ms`, no TCP reset. A follow-up `lconf --lidar-smoke` still passed.

Decorative MSOP shape notes verified on 2026-06-19:

- The lidar simulator shape generator lives in `src\lwipdemo\main.c` inside the existing MSOP packet builder. For visual simulator targets, keep using that existing soft-MCU MSOP path; do not add HDL modules, board wrappers, or protocol duplicates just to change the displayed figure.
- The verified pig-head figure keeps the first echo as the head contour and puts the snout into the second echo. For TCP MSOP V1, `echo_mode=3` means two echoes and `echo_num=2`; invalid second-echo samples use the distance-width-specific marker, currently `0xffff` for 2-byte distances.
- To keep the stream smooth on the 64 KiB soft-MCU image, the verified second-echo snout format uses `distance_byte_count=2`, `intens=0`, `echo_mode=3`, `echo_num=2`. This keeps the packet at `758` bytes (`2 + 34 + 180 * 2 echoes * 2 bytes + 2`), the same size as the older single-echo 3-byte-distance/intensity format. `lconf` parses `intens=0` and still renders echo 2 when the second distance is valid.
- Do not switch to a 3-byte-distance two-echo packet (`1478` bytes) or a 2-byte two-echo packet with intensity (`1118` bytes) casually. Hardware tests showed those larger streams can trigger long pauses or stack/LwIP pressure with the current tiny RAM budget, even when basic parsing works.
- `lconf` currently gives only one sample per echo at each angle. Attempts to draw a closed snout plus separate nostril circles only in the second echo produced sparse diagonal/arc fragments, and the user rejected the later second-echo outer/inner alternation as not looking like a snout. For nested contours such as "a circle inside a circle", use point-index interleaving in one echo first: even MSOP points can draw the outer radius and odd MSOP points can draw the inner radius. This gives two readable 90-point circles from the 180-point scan without increasing packet size or adding HDL.
- The 20K soft-MCU is built for `rv32i_zicsr` with `-mno-div`; avoid division or modulo inside the 180-point MSOP loop. The verified pig-head implementation uses angle-distance checks and integer slopes in mm/degree for ears, cheeks, saddle, and snout. A phase calculation with division once per frame is acceptable; per-point division is not. If a future decorative shape stutters, inspect `src\darksocv.S` around the inlined MSOP loop and confirm there are no `__udivsi3`/`__umodsi3` calls in the hot point path.
- The TCP data port currently behaves as a single-client MSOP stream. If `lconf` GUI and a custom capture CLI connect to `50100` at the same time, one client can see a TCP reset; close the GUI or avoid overlapping data connections before measuring cadence.
- Verified firmware build for the alternating second-echo snout image: `14818 darksocv.mem`, `58760` bytes in `darksocv_uart.bin`; the known RWX LOAD segment linker warning remains.
- Verified ModelSim command remained `$env:DARKSIMV_DEFINES='+define+DARKETH_LWIP_FRAME'; $env:DARKSIMV_NOWAVES='1'; & 'C:\intelFPGA\18.1\modelsim_ase\win32aloem\vsim.exe' -c -do "do C:/workspace/verilog/soft_mcu/dark_risc/sim/darksimv_modelsim.do; quit -f"` and passed with `Errors: 0`, `fwloader sim ok`, and `lidarsim ok`.
- Verified SRAM hardware load used the tracked `C:\workspace\verilog\20k\build_and_program20K_volatile.bat` wrapper and programmed `GW2A-18C` with `-r 2`: `User Code 0x00006EAC`, `Status Code 0x00006020`, programming cost `13.94 s`.
- Verified hardware smoke in the shared `192.168.2.0/24` network with `python C:/workspace/verilog/20k/lidar_switch_check.py --iface Ethernet --host-ip 192.168.2.146 --lidar-ip 192.168.2.240 --smoke --skip-data --broadcast-discovery --no-net-config`; it filtered the FPGA among real lidar responses and passed discovery, UDP full-status/firmware, and TCP command. The stock smoke data check is still hardcoded for single-echo 3-byte-distance MSOP, so use a custom parser for this multi-echo format unless the smoke tool is updated.
- Verified real TCP MSOP capture after SRAM load: `260` frames, frame span `0..259`, frame size `758`, RX interval average `19.97 ms`, `p95 32.00 ms`, max `32.00 ms`; header fields were `distance_byte_count=2`, `intens=0`, `echo_mode=3`, `echo_num=2`. The second echo had `49..50` valid snout points per frame, `130..131` invalid markers, distance range `1476..2360 mm` on the checked frame, and near/far alternation ratio `1.00`.
- Verified intermediate baseline for the user's intended snout geometry: first echo alternates by point index between an outer `1800 mm` circle and an inner `1100 mm` circle; second echo is `0xffff` invalid. Build `14714 darksocv.mem`, `58344` bytes; ModelSim passed with `Errors: 0`, `fwloader sim ok`, `lidarsim ok`; SRAM load with `programmer_cli -d GW2A-18C -r 2` succeeded after one cable-lost retry (`User Code 0x00006EAC`, `Status Code 0x00006020`, cost `13.56 s`); TCP MSOP capture verified `160` frames, `758` bytes, `90` outer and `90` inner first-echo points per frame, second echo `180/180` invalid, RX interval average `20.05 ms`, max `32.00 ms`.
- Verified final snout-circle compromise for the user's "circle with circles inside" requirement: keep the 758-byte two-echo packet, draw the outer snout circle as `1800 mm`, and use point-index interleaving plus precomputed near/far nostril-intersection tables for two inner circles. With only two echoes, odd samples in the nostril angular windows borrow echo 1 for the near nostril intersection while neighboring even samples keep the outer circle readable; echo 2 carries the remaining near/far nostril points. The real 20K SRAM image built as `14828 darksocv.mem`, `58800` bytes; ModelSim passed with `Errors: 0`, `fwloader sim ok`, `lidarsim ok`; tracked volatile wrapper programmed `GW2A-18C` with `-r 2` (`User Code 0x00006EAC`, `Status Code 0x00006020`, `14.82 s`); direct and repeat broadcast `lconf --lidar-smoke --smoke-skip-data` passed; custom TCP MSOP capture verified `160` frames, exact geometry `mismatches=0`, echo-1 near-intersection count `46..48`, echo-2 valid count `92..94`, RX interval average `19.96 ms`, max `20.21 ms`. PNG from real hardware frame: `C:\Users\User\AppData\Local\Temp\fpga_pig_snout_circles_msop.png`.
- Verified full pig-head version after the user clarified that the task was the whole pig, not only the snout: echo 1 is a rotating head/ear outline, echo 2 is a round snout with two inner circles. Keep both shapes as `uint8` unit tables (`distance = base + unit * 8` for the head, `distance = unit * 8` for the snout, `0xff` invalid) rather than 16-bit distance tables or per-point circle math. The first 16-bit snout-table attempt built as `14913 darksocv.mem`, `59140` bytes and failed ModelSim after `NET_CONFIG` with an `sdram: unmapped addr=ff...` symptom; a compressed snout-only table built as `14874`, `58984` bytes but still missed the simulator full-status deadline. The verified table-compressed head+snout build is `14835 darksocv.mem`, `58828` bytes; ModelSim passed with `Errors: 0`, `fwloader sim ok`, `lidarsim ok`; tracked volatile SRAM wrapper programmed `GW2A-18C` with `-r 2` (`User Code 0x00006EAC`, `Status Code 0x00006020`, `15.73 s`); broadcast smoke passed in the shared network while filtering real `R120_BM1` replies; custom TCP MSOP capture verified `160` frames, exact geometry `mismatches=0`, head distance range `1780..2676 mm`, snout valid points `49/180`, RX interval average `20.00 ms`, max `20.21 ms`. PNG from real hardware frame: `C:\Users\User\AppData\Local\Temp\fpga_pig_head_round_snout_msop.png`.

## 20K TCP FPGA Firmware Loader To FLASH

Verified on 2026-06-18 on the 20K dev board:

- The TCP firmware loader reuses the existing `src\lwipdemo` soft-MCU/LwIP firmware and listens on TCP port `50102`; no new HDL Ethernet parser or board top was added for the loader.
- The loader accepts the existing `lconf --cli` Default Bootloader frame format: `12 34`, little-endian payload length, little-endian packet number, payload, `55 AA`, little-endian sum16 over preceding frame bytes.
- Implemented firmware commands match the lconf bootloader path: `JmpBoot=61`, `CpuPrgBegin=55`, `CpuPrgData=56`, `CpuPrgEnd=57`. Replies use payload `[cmd, status]`; erase progress uses `[55, 9, percent]`.
- `lconf` wraps a raw FPGA `.bin` as FPGA-only when no package header exists. The verified upload reported: `FPGA=907520` bytes, `3546` blocks, total package size `907776` bytes.
- The FPGA-only firmware package header fields used by the loader are: `mcuLen` at offset `0`, `mcuCrc` at `4`, `fpgaLen` at `8`, `fpgaCrc` at `12`, version string area at `16..127`, FPGA magic `0xDEADBEEF` at `128`; sections are 256-byte aligned.
- The soft-MCU writes only the FPGA section to external SPI FLASH address `0`, computes CRC32 while streaming, and after `CpuPrgEnd` reads FLASH back over SPI and compares readback CRC before returning OK.
- SPI FLASH access uses the existing `dark_risc` bit-bang SPI path (`SPI` + `SPIBB`) through `OPORT/IPORT`: MOSI bit `0`, SCK bit `1`, CSN bit `2`, enable bit `3`, MISO observed at `IPORT[6]`.
- Active 20K FLASH pins in `m20k_dev_uart_rmii_debug`: `FLASH_SPI_SO=P10`, `FLASH_SPI_SI=R10`, `FLASH_SPI_CS=M9`, `FLASH_SPI_CLK=L10`.
- UART command `flashid` (alias `fwid`) reads JEDEC ID without erase/write. Hardware returned `fwloader flash_id=0b4016 ok=1`.
- Firmware build after adding the loader and readback verification fits in 64 KiB: `14087 darksocv.mem`, `55836` bytes in `darksocv_uart.bin`; the known RWX LOAD segment linker warning remains.
- ModelSim 10.5b command:
  `$env:DARKSIMV_DEFINES='+define+DARKETH_LWIP_FRAME'; $env:DARKSIMV_NOWAVES='1'; & 'C:\intelFPGA\18.1\modelsim_ase\win32aloem\vsim.exe' -c -do "do C:/workspace/verilog/soft_mcu/dark_risc/sim/darksimv_modelsim.do; quit -f"`
- Verified ModelSim output included `Errors: 0`, `fwloader begin mock=1 flash_id=ef4018 fpga=512 crc=ef5f180f`, `fwloader end ok bytes=512 crc=ef5f180f flash_crc=ef5f180f`, `fwloader sim ok`, and `lidarsim ok`.
- Gowin build result for the loader image: `LDR_20K.fs` size `7264087`, `LDR_20K.bin` size `907418`, logic `3176/20736 15%`, registers `1266/16173 7%`, CLS `2094/10368 20%`, BSRAM `82%`, PLL `0/4`.
- Successful volatile SRAM programming before the TCP FLASH upload used `C:\workspace\verilog\20k\build_and_program20K_volatile.bat` and reported `User Code: 0x00006EAC`, `Status Code: 0x00006020`, cost about `14.51` seconds.
- Normal Windows TCP upload used the bench adapter `Ethernet 5` at `192.168.15.13/24`; the FPGA was temporarily runtime-configured by UART to `192.168.15.20` and restored to `192.168.20.20` afterwards.
- Verified upload command:
  `& 'C:\workspace\lidar\lconf\bin\Release\lconf.exe' --cli --file 'C:\workspace\verilog\20k\LDR_20K\impl\pnr\LDR_20K.bin' --channel tcp --host 192.168.15.20 --port 50102 --erase-timeout 300000 --reply-timeout 30000`
- Verified `lconf --cli` output included `Стирание флэш: 100%`, `Send end`, and `OK: Данные загружена.`
- UART evidence for the real FLASH write included `fwloader begin mock=0 flash_id=0b4016 fpga=907520 crc=9bbd26fa` and `fwloader end ok bytes=907520 crc=9bbd26fa flash_crc=9bbd26fa`.
- After the TCP FLASH write, `lconf --lidar-smoke --smoke-host 192.168.15.20 --smoke-local-host 192.168.15.13 --smoke-discovery-target 192.168.15.20 --smoke-skip-data` passed discovery, UDP full status, UDP firmware, and TCP command.
- `darkuart` still has no RX queue; for UART configuration commands on hardware, send characters slowly (about 35 ms per char was verified). A fast `ip 192.168.20.20` send dropped the first digit and configured `92.168.20.20`.
- Verified FLASH write/readback does not prove power-cycle boot from external FLASH. Treat boot-after-power-cycle as a separate hardware check when persistent boot behavior is the milestone.

## 20K Live FLASH_SPI Readback Through Lidar Command Port

Verified on 2026-06-18 on the 20K dev board:

- The live lidar FLASH path uses control command `FLASH_SPI = 0x45` on command port `50101`, not the firmware-loader TCP port `50102`. `lconf --flash-dump` talks to this live command channel and expects the production packet shape used by `ControlChannel::sendFlashSpiPacket`, `requestFlashSpiBlock`, and `writeFlashSpiBlock`.
- The soft-MCU implementation reuses the existing `lwipdemo` SPIBB FLASH helpers. Fixed `A0` op values are: `0` write byte, `1` read byte, `2` erase sector, `3` status. Varlen `A1` op values are: `0` write block and echo written bytes, `1` read block. Do not add a second FLASH driver unless the existing bit-bang path is insufficient.
- RAM is tight in the 64 KiB DarkRISCV image. The verified build keeps `LIDARSIM_CONTROL_BUF_MAX` and `LIDARSIM_CONTROL_REPLY_MAX` at `320`; that leaves `303` data bytes for a varlen FLASH block reply (`320 - 11` frame overhead - `6` FLASH block header). Prefer `--flash-chunk 256` for full dumps.
- `lconf --flash-dump` default chunk was `512` in this build. The FPGA may legally return short blocks (`303` bytes here); `lconf` continues from the returned length and completed a 1024-byte default-chunk read with byte-for-byte match. Full 907520-byte readback was still run with `--flash-chunk 256` to reduce stress.
- Current firmware build after adding live FLASH_SPI readback: `14332 darksocv.mem`, `56816` bytes in `darksocv_uart.bin`; the known RWX LOAD segment warning remains.
- Verified ModelSim command remained:
  `$env:DARKSIMV_DEFINES='+define+DARKETH_LWIP_FRAME'; $env:DARKSIMV_NOWAVES='1'; & 'C:\intelFPGA\18.1\modelsim_ase\win32aloem\vsim.exe' -c -do "do C:/workspace/verilog/soft_mcu/dark_risc/sim/darksimv_modelsim.do; quit -f"`
- Verified ModelSim output included `Errors: 0`, `fwloader sim ok`, and `lidarsim ok`.
- Verified volatile SRAM programming after the FLASH_SPI change used the existing bitstream and default-speed programmer: `programmer_cli.exe -d GW2A-18C -r 2 -f C:\workspace\verilog\20k\LDR_20K\impl\pnr\LDR_20K.fs`, with `User Code: 0x00006EAC`, `Status Code: 0x00006020`, cost about `13.7` seconds.
- After SRAM reload, if UART is not available, the board can be moved from default `192.168.20.20` to the Windows bench subnet by sending exact-MAC `NET_CONFIG` as UDP broadcast to discovery port `50103`. Use MAC `02:20:20:20:20:01`, target IP `192.168.15.20`, host IP `192.168.15.13`, data port `50100`, command port `50101`. Wait about one second before the first `lconf --lidar-smoke`; the first immediate discovery can race ARP/netif reconfiguration.
- The verified Ethernet write command was:
  `& 'C:\workspace\lidar\lconf\bin\Release\lconf.exe' --cli --file 'C:\workspace\verilog\20k\LDR_20K\impl\pnr\LDR_20K.bin' --channel tcp --host 192.168.15.20 --port 50102 --erase-timeout 300000 --reply-timeout 30000`
- The verified live FLASH readback command was:
  `& 'C:\workspace\lidar\lconf\bin\Release\lconf.exe' --flash-dump --flash-channel tcp --flash-host 192.168.15.20 --flash-port 50101 --flash-local-host 192.168.15.13 --flash-output $env:TEMP\ldr20k_flash_readback_907520.bin --flash-start 0 --flash-length 907520 --flash-chunk 256 --flash-timeout 30000 --flash-retries 5 --flash-connect-timeout 10000 --flash-overwrite`
- Full readback evidence: `907520/907520` bytes, `retries=0`, elapsed about `204.4 s`. The first `907418` bytes matched `LDR_20K.bin` exactly (`first_mismatch=-1`, SHA256 `558E12BA3C84B1BC8FAEA8FCAC4733EF8D394B938152FE9BE63894576A08F639`); the 102-byte FPGA-only alignment tail read back as `0x00`.
- This proves Ethernet write to FLASH through the bootloader path and Ethernet readback through the live lidar `FLASH_SPI` path.

Verified on 2026-06-22 on the shared switch network (`Ethernet`, host `192.168.2.146`, FPGA `192.168.2.240`):

- The current non-DDR `LDR_20K` build after FLASH-loader adjustments built as `14847 darksocv.mem` / `58876` bytes in `darksocv_uart.bin`; ModelSim passed with `Errors: 0`, `fwloader sim ok`, and `lidarsim ok`.
- Gowin build completed PnR and bitstream generation, but timing was not clean: setup violated endpoints `2`, hold violated endpoints `0`, `EthRefCLK` Fmax `49.735 MHz` against `50 MHz`, worst setup slack `-0.107 ns` inside the DarkRISCV register-file path. Treat this as a separate timing TODO even when hardware smoke passes.
- Volatile SRAM load used `C:\workspace\verilog\20k\program20K_volatile_fs.bat C:\workspace\verilog\20k\LDR_20K\impl\pnr\LDR_20K.fs` and reported `User Code: 0x00006EAC`, `Status Code: 0x00006020`, cost `14.99` seconds.
- The existing bootloader upload path from root `lconf` still can stall in this shared-switch image:
  `& 'C:\workspace\lidar\bin\Release\lconf.exe' --cli --file 'C:\workspace\verilog\20k\LDR_20K\impl\pnr\LDR_20K.bin' --channel tcp --host 192.168.2.240 --port 50102 --erase-timeout 900000 --reply-timeout 30000`
  It reached erase progress `35%`, then failed after the erase timeout with `Send begin timeout`; UART showed `fwloader begin mock=0 flash_id=0b4016 fpga=907520 crc=274a2b7e`, many `lidarsim rx flags=0104/0106/010a`, then `fwloader tcp err=-14` / `fwloader tcp closed`. The board services stayed alive afterwards. Keep this as an open bootloader-erase/main-loop starvation issue, not as proof that SPI FLASH or live readback is bad.
- After that failed bootloader attempt, a 1024-byte live readback through `lconf --flash-dump` succeeded but returned all `0xff`, proving the failed attempt had erased the beginning of external FLASH. Do not leave the board in that state before shutdown if a recovery path is available.
- Added `C:\workspace\verilog\20k\flash_spi_live_program.py` as a reproducible live-command-port programming tool. It uses the existing `FLASH_SPI=0x45` command on TCP port `50101`: fixed `A0` op `2` for 4 KiB sector erase, varlen `A1` op `0` for 256-byte write blocks, and varlen `A1` op `1` for readback/verify. This keeps network servicing between erase/write/read commands and avoids the long synchronous bootloader erase window.
- Verified live FLASH programming command:
  `python C:\workspace\verilog\20k\flash_spi_live_program.py --host 192.168.2.240 --port 50101 --local-host 192.168.2.146 --file C:\workspace\verilog\20k\LDR_20K\impl\pnr\LDR_20K.bin --timeout 30 --chunk 256 --readback $env:TEMP\ldr20k_flash_live_readback_20260622.bin`
- Verified live programming evidence: raw `.bin` length `907418`, padded FPGA length `907520`, erase length `909312`, `.bin` SHA256 `E51E1F1CCFC114473FF2DCCE99878C0B3A196923051C9B321B7373BED54BFE41`, image CRC32 `EA28785A`, erase/write/verify all reached `100%`, `verify ok bytes=907520 crc32=EA28785A`, and the 102-byte tail was zero.
- Independent root `lconf --flash-dump` full readback then passed on the same image:
  `& 'C:\workspace\lidar\bin\Release\lconf.exe' --flash-dump --flash-channel tcp --flash-host 192.168.2.240 --flash-port 50101 --flash-local-host 192.168.2.146 --flash-output $env:TEMP\ldr20k_flash_lconf_full_readback_20260622_212240.bin --flash-start 0 --flash-length 907520 --flash-chunk 256 --flash-timeout 30000 --flash-retries 5 --flash-connect-timeout 10000 --flash-overwrite`
  It read `907520/907520` bytes with `retries=0`, elapsed `41.3 s`, `first_mismatch=-1` against the first `907418` bytes of `LDR_20K.bin`, and `TAIL_ALL_ZERO=True`.
- Post-write service smoke passed through `C:\workspace\verilog\20k\lidar_switch_check.py --iface Ethernet --host-ip 192.168.2.146 --lidar-ip 192.168.2.240 --smoke --skip-data --no-net-config --smoke-timeout 8000`.
- Controlled reload from external FLASH with `programmer_cli.exe -d GW2A-18C -r 1` completed in `1.03` seconds. After a three-second wait, TCP ports `50101` and `50102` were open and the same smoke test passed, proving the Ethernet-programmed external FLASH image boots.

## 20K Boot From External FLASH After Power Cycle

Verified on 2026-06-18 on the 20K dev board:

- After the user physically replugged board power, the old runtime IP `192.168.15.20` no longer answered `lconf --lidar-smoke`, proving the volatile runtime configuration was gone.
- Raw Scapy ARP on `Ethernet 5` then found the board at its default FLASH-boot configuration: MAC `02:20:20:20:20:01`, IP `192.168.20.20`.
- Because the Windows bench adapter was only `192.168.15.13/24`, a normal Windows socket UDP broadcast `NET_CONFIG` did not move the board in this run. A raw Scapy Ethernet/IP/UDP broadcast frame on `Ethernet 5`, carrying exact-MAC `NET_CONFIG`, did move the board to `192.168.15.20`; ARP for `192.168.15.20` replied from `02:20:20:20:20:01`.
- Post-boot `lconf --lidar-smoke --smoke-host 192.168.15.20 --smoke-local-host 192.168.15.13 --smoke-discovery-target 192.168.15.20 --smoke-skip-data` passed discovery, UDP full-status, UDP firmware `pegus_1`, TCP firmware `pegus_1`, and `PASS lidar-smoke`.
- Post-boot live FLASH readback also passed through command port `50101`: `--flash-dump --flash-length 1024 --flash-chunk 256` read `1024/1024` bytes, `retries=0`, elapsed about `0.3 s`; the first 1024 bytes matched `LDR_20K.bin` (`first_mismatch=-1`, dump SHA256 `81775B43521257409089FE5F1E15B8BA92D0C097041092879A804869DAB9E48D`).
- With this evidence, persistent boot from external FLASH, live lidar services, and live `FLASH_SPI` readback are all hardware-verified for the current image.
- The `lconf` discovery table firmware column is GUI-side text. Older `lconf` builds display the state flag as `MAIN FW` even when the FPGA command `LIDAR_FIRMWARE (0x7e)` returns `pegus_1`. The simulator now packs the 32-byte discovery model field as two NUL-separated C strings, `R120_FAKE\0pegus_1\0`; update `lconf` to parse the optional second string and show it in the firmware column.
- When testing the user-facing `lconf` GUI, rebuild through the root solution so the executable at `C:\workspace\lidar\bin\Release\lconf.exe` is updated. Building `C:\workspace\lidar\lconf\lconf.vcxproj` directly can emit a separate `C:\workspace\lidar\lconf\bin\Release\lconf.exe`. If the root `bin\Release` tree lacks Qt DLLs, run `C:\Qt\Qt6.4.2\6.4.2\msvc2019_64\bin\windeployqt.exe --release C:\workspace\lidar\bin\Release\lconf.exe` before CLI smoke tests.

## R120 External PSRAM TCP MSOP Integration

Use this section for the old R120_M/GW2A board when the lidar simulator needs
LwIP TCP services plus the soldered `IS66WVS1M8BLL` SerialRAM as an MSOP buffer.
Before using web search for the RAM or board, check the local Obsidian vault and
repo notes first; the ISSI datasheet, pin note, DSView captures, and R120 task
checkpoints already exist locally.

Verified integration milestone on 2026-06-30:

- Working superproject branch: `codex/r120-lidar-ext-ram-tcp-msop`, created
  from `codex/r120-static-udp-r13clk`, then merged with
  `codex/flash-ram-is66wvs1m8` and `dev_20k`.
- Previous real RAM evidence: DSView CSV
  `C:\workspace\verilog\CODEX\captures\dsview_spi_decode_miso4_20260630_120540.csv`
  showed plain-SPI readback pass for addresses `0x000000`, `0x000004`,
  `0x000400`, and `0x000ffc`.
- R120 top hierarchy follows the local file-layer rule:
  - CST physical layer: `src\main\R120_lidar_ext_ram.cst`.
  - Board-interface wrapper: `src\main\R120_lidar_ext_ram_brd_ifm.sv`.
  - Helper hardware: `soft_mcu\dark_risc\rtl\darkpsram_mmio.sv`,
    `darketh_mmio.sv`, PLL/RMII support, and the PSRAM low-level core.
  - Application/main logic: `soft_mcu\dark_risc\src\lwipdemo\main.c`.
- Clocking: the R120 top uses board `H11` 10 MHz into `o_pll_10_50` and runs
  the SoC/RMII logic at 50 MHz. The hardware-verified RMII TX mode drives
  `Ethclkin/R13` from FPGA `clk_50`, leaves `EthRefCLK/P8` high-Z, leaves
  `EthnlntSel/T6` high-Z, and registers RMII TX outputs on `negedge clk_50`.
  The user confirmed by oscilloscope that `Ethclkin/R13` carries the 50 MHz
  clock into the PHY `CLKIN/XTAL1` path; do not revert this target to the old
  `EthRefCLK/P8` clock-output assumption without new scope evidence.
- PSRAM pins in the R120 top: `CE#=J5`, `SIO1/MISO=G12`, `SIO2=H13`,
  `SIO0/MOSI=H14`, `SCLK=J13`, `SIO3=N10`.
- Flash SPI pins are preserved for the live/firmware-loader path:
  `SO=P10`, `SI=R10`, `CS=M9`, `CLK=L10`.
- The current R120 bench board has no usable UART path for Codex diagnostics.
  Treat `darkuart` output as ModelSim/simulation evidence only; use packet
  captures, LEDs, scope/DSView, GAO, or user-confirmed physical behavior for
  hardware evidence.

`darkpsram_mmio` details:

- Source: `soft_mcu\dark_risc\rtl\darkpsram_mmio.sv`.
- It is instantiated from `rtl\darksocv.v` behind `DARKPSRAM_MMIO` at CS3,
  base address `0xc0000000`, when SDRAM is not occupying that slot.
- Register map:
  - `0x00 STATUS`: bit0 init done, bit4 op busy, bit5 op done,
    bit6 op error, bit8 ready for command.
  - `0x04 ADDR`: byte address.
  - `0x08 WDATA`: 32-bit write payload.
  - `0x0c RDATA`: 32-bit read payload.
  - `0x10 CTRL`: bit0 start read32, bit1 start write32, bit8 clear done,
    bit9 clear error.
  - `0x14 ID`: returns `0x49533636`.
  - `0x18 OP_COUNT`: completed operations.
- The helper performs a conservative power-up/init sequence: wait, clocks with
  `CE#` high, reset-enable `0x66`, reset `0x99`, recovery wait, then ordinary
  SPI `0x03` read and `0x02` write operations.
- The local `src\RAM\is66wvs1m8\is66wvs1m8_model.sv` simulation model must
  accept `0x66` reset-enable and `0x99` reset commands. `0x99` clears QPI state
  in the model; unsupported-command prints here usually mean the model drifted
  from the real init sequence rather than a firmware failure.
- Gowin/SystemVerilog gotcha verified while integrating this file: with
  ``default_nettype none`` and Gowin, declare input ports as `input wire logic`
  where a net kind is required. Plain `input logic` can be rejected in some
  contexts.

Firmware PSRAM MSOP behavior:

- Build define: `LIDARSIM_PSRAM_MMIO=1`.
- Firmware base address defaults to `DARKPSRAM_BASE=0xc0000000`.
- PSRAM diagnostics are deferred until a TCP data client is connected, so UDP
  discovery/control can come up even if the external RAM path is still under
  debug.
- Under the PSRAM profile, the firmware keeps four MSOP slots in external RAM
  starting at PSRAM byte address `0x1000` with `1024`-byte stride.
- `service_msop_tcp()` generates the same pig-head test MSOP frame, writes the
  758-byte packet into a PSRAM ring slot through 32-bit MMIO operations, reads
  the next queued packet back into a small internal staging buffer, and sends it
  with `tcp_write(..., TCP_WRITE_FLAG_COPY)`.
- This is real external-RAM buffering, but not no-copy TCP from PSRAM: the ISSI
  SerialRAM is accessed through a command MMIO adapter, not as a linear CPU
  memory window.
- The PSRAM LwIP profile reduced control/reply/firmware buffers to `160` bytes
  and uses `LIDARSIM_MSOP_TX_BUFFERS=4`; this fixed an initial `.bss` overflow
  of 240 bytes in the 64 KiB DarkRISCV image.

Windows build commands verified for the R120 PSRAM LwIP image:

```powershell
& 'C:\msys64\usr\bin\make.exe' -C 'C:\workspace\verilog\soft_mcu\dark_risc\src\lwipdemo' clean all LIDARSIM_PSRAM_MMIO=1 CCPATH='C:/msys64/ucrt64/bin'
& 'C:\msys64\usr\bin\make.exe' -C 'C:\workspace\verilog\soft_mcu\dark_risc\src\darklibc' clean all CCPATH='C:/msys64/ucrt64/bin'
& 'C:\msys64\ucrt64\bin\riscv32-unknown-elf-gcc.exe' -E -x c -P -DMLEN=65536 'C:\workspace\verilog\soft_mcu\dark_risc\src\darksocv.lds' -o 'C:\workspace\verilog\soft_mcu\dark_risc\src\darksocv.ld'
& 'C:\msys64\usr\bin\make.exe' -C 'C:\workspace\verilog\soft_mcu\dark_risc\src' APPLICATION=lwipdemo LIDARSIM_PSRAM_MMIO=1 CCPATH='C:/msys64/ucrt64/bin'
```

Verified normal production-ish firmware result after the firmware-buffer
self-test fix and deferred PSRAM diagnostic: `14878 darksocv.mem`, `59000`
bytes in `darksocv_uart.bin`; the existing linker warning
`darksocv.o has a LOAD segment with RWX permissions` remains.

PSRAM-backed MSOP ModelSim evidence added on 2026-06-30:

```powershell
& 'C:\msys64\usr\bin\make.exe' -C 'C:\workspace\verilog\soft_mcu\dark_risc\src' clean all APPLICATION=lwipdemo LIDARSIM_PSRAM_MMIO=1 LIDARSIM_PSRAM_SIM_SELFTEST=1 NOBANNER=1 CCPATH='C:/msys64/ucrt64/bin'

$env:DARKSIMV_BASE_DEFINES='+define+DARKETH_MMIO +define+DARKPSRAM_MMIO'
$env:DARKSIMV_DEFINES='+define+DARKETH_LWIP_FRAME'
$env:DARKSIMV_NOWAVES='1'
& 'C:\intelFPGA\18.1\modelsim_ase\win32aloem\vsim.exe' -c -do "do C:/workspace/verilog/soft_mcu/dark_risc/sim/darksimv_modelsim.do; quit -f"
```

Expected proof lines: `lidarsim psram status=0101 id=49533636 base=c0000000`,
`lidarsim psram ok ops=02`,
`lidarsim psram msop selftest ok slots=04 len=02f6 ops=02 to 05f2`,
`lidarsim tcp data listen=0 port=50100`, and final `lidarsim ok` with
ModelSim `Errors: 0`. The verified run built as `15055 darksocv.mem` /
`59708` UART bytes and ended after `781013` clocks, `492199` instructions,
`CPI = 1.59`.

`LIDARSIM_PSRAM_SIM_SELFTEST` is simulation-only. It eagerly runs the PSRAM
diag at startup, writes four 758-byte MSOP packets to the external-RAM ring,
reads them back, and byte-compares the `ff fe ... ff 9b` packet envelope. Do
not set it for a production firmware image; build again without this define
before Gowin or hardware programming.

TCP-data PSRAM simulation evidence added on 2026-06-30:

```powershell
& 'C:\msys64\usr\bin\make.exe' -C 'C:\workspace\verilog\soft_mcu\dark_risc\src' clean all APPLICATION=lwipdemo LIDARSIM_PSRAM_MMIO=1 LIDARSIM_PSRAM_TCP_SIM_SELFTEST=1 NOBANNER=1 CCPATH='C:/msys64/ucrt64/bin'

$env:DARKSIMV_BASE_DEFINES='+define+DARKETH_MMIO +define+DARKPSRAM_MMIO'
$env:DARKSIMV_DEFINES='+define+DARKETH_LWIP_FRAME +define+DARKETH_LWIP_TCP_DATA_FRAME'
$env:DARKSIMV_NOWAVES='1'
& 'C:\intelFPGA\18.1\modelsim_ase\win32aloem\vsim.exe' -c -do "do C:/workspace/verilog/soft_mcu/dark_risc/sim/darksimv_modelsim.do; quit -f"
```

`DARKETH_LWIP_TCP_DATA_FRAME` sends a minimal SYN to TCP data port `50100`,
captures the real SYN-ACK sequence number from the simulated Ethernet TX frame,
then sends the final ACK. Incoming TCP/IP checksums are disabled in
`lwipopts.h`, so the testbench leaves those checksum fields at zero just like
the existing UDP simulation frames.

`LIDARSIM_PSRAM_TCP_SIM_SELFTEST` is also simulation-only. It extends
`SIM_FLAGS_DONE` so `lidarsim ok` waits until `service_msop_tcp()` has accepted
a real LwIP TCP data client, run the deferred PSRAM diagnostic, read a
758-byte MSOP packet back from the PSRAM ring, and called `tcp_write()` /
`tcp_output()`. Expected proof lines from the verified run:
`darketh sim tcp data synack iss=0000196e`,
`lidarsim tcp data connected`, `lidarsim psram recovered`,
`lidarsim psram tcp msop ok len=02f6 slot=00 ops=017e`, and final
`lidarsim ok`. ModelSim ended with compile `Errors: 0`, runtime `Errors: 0`,
`Warnings: 8`, after `561262` clocks and `350998` instructions. The test
firmware built as `14924 darksocv.mem` / `59184` UART bytes.

The `DARKETH_LWIP_TCP_DATA_FRAME` testbench also validates the outgoing TCP
data stream, not only the firmware-side `tcp_write()` call. It captures
Ethernet TX frames from `darketh_mmio`, filters IPv4/TCP segments from source
port `50100` to the simulated client port `40000`, reassembles the TCP payload
across segments, and checks the 758-byte MSOP envelope and fixed header fields
(`ff fe`, point count `180`, angle resolution `2000`, distance bytes `2`, echo
mode/count `3/2`, tail `ff 9b`). The expected proof line is
`darketh sim tcp data msop payload ok len=02f6`; the current LwIP/MSS split is
two segments (`512 + 246` bytes), but the main proof is the reassembled payload
length and content.

After running this TCP-data simulation, rebuild the ordinary image without
`LIDARSIM_PSRAM_TCP_SIM_SELFTEST`; the verified normal PSRAM firmware returns
to `14878 darksocv.mem` / `59000` UART bytes. A base PSRAM/LwIP simulation
with only `+define+DARKETH_LWIP_FRAME` still passed with `lidarsim ok`,
runtime `Errors: 0`, `Warnings: 8`, after `281854` clocks.

The standalone ISSI controller regression should still pass after model edits:

```powershell
& 'C:\intelFPGA\18.1\modelsim_ase\win32aloem\vsim.exe' -c -do 'do C:/workspace/verilog/src/RAM/is66wvs1m8/EF_PSRAM_CTRL_is66wvs1m8_tb.do; quit -f'
```

Verified pass list: SPI `02h/03h`, SPI fast-read `0Bh`, quad-IO `38h/EBh`,
QPI `38h/EBh`, QPI `03h`, exit-QPI, and SPI read after QPI exit, with
`Errors: 0`, `Warnings: 0`.

Confirmed firmware traps from this milestone:

- Under the PSRAM profile `LIDARSIM_FIRMWARE_BUF_MAX` can be `160`, while the
  firmware-loader self-test page is `256` bytes. Guard `firmware_selftest()`
  so it skips the 256-byte local buffer exercise when the buffer is smaller;
  otherwise it corrupts globals before networking starts.
- Keep debug LED bits independent from UART: CPU alive, netif up, PSRAM ok, and
  TCP data client are useful on the R120 board where UART is unavailable.
  Treat `darksocv_uart.bin` and `darkuart` prints as build/simulation artifacts
  only; this R120 table setup has no usable hardware UART evidence path.

Build traps from this milestone:

- Use Windows-style `CCPATH='C:/msys64/ucrt64/bin'` with
  `C:\msys64\usr\bin\make.exe`. In this environment, the pure MSYS bash path
  using `/ucrt64/bin` failed silently during `boot.S` compilation.
- `make clean` inside `soft_mcu\dark_risc\src` deletes tracked
  `src\darksocv.mem`; rebuild it before committing the submodule firmware image.
- `src\Makefile` has a linker-script rule shaped like `CPP input output`, while
  `gcc -E` needs `-o output`. If overriding `CPP` with `gcc -E -x c`, generate
  `src\darksocv.ld` explicitly as shown above before the final make.
- If Gowin reports `Net 'spi_miso' does not have a driver` in the SPIBB path,
  check that `darksocv.v` includes `assign spi_miso = SPI_MISO;` when the
  internal bit-bang SPI input is exposed as an SoC output/debug net.

R120 Gowin build verified on 2026-06-30:

```powershell
cd C:\workspace\verilog\20k\LDR_20K
& 'C:\workspace\verilog\20k\LDR_20K\build_r120_lidar_ext_ram.cmd'
```

Use the `.cmd` wrapper as the authoritative entrypoint. It rebuilds the normal
`lwipdemo` firmware with `LIDARSIM_PSRAM_MMIO=1` and without simulation-only
self-test flags before Gowin embeds `soft_mcu\dark_risc\src\darksocv.mem`.
The raw `gw_sh.exe build_r120_lidar_ext_ram.tcl` path only describes the FPGA
file list and can accidentally embed a stale or simulation-test firmware image.

No-hardware regression entrypoint for this R120 external-RAM target:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File C:\workspace\verilog\scripts\run_r120_ext_ram_regression.ps1
```

The script does not run Gowin Programmer and does not touch FPGA SRAM/FLASH.
It checks the local build environment, runs the ISSI `IS66WVS1M8` controller
ModelSim regression, runs the R120 board-wrapper RMII RX regression, optionally
runs the DarkRISCV/LwIP TCP-data PSRAM self-test, rebuilds the normal
non-self-test firmware afterward, then builds the Gowin debug and production
profiles. It verifies `setup=0` and `hold=0` from Gowin timing reports and
checks that `R120_LIDAR_EXT_RAM_PROD.vg` contains no temporary diagnostic UDP
marker text. `LogPath` is a real tee log for child command stdout/stderr, so
ModelSim proof lines are kept in the log file. Use `-Fast` for the short
environment + two ModelSim checks only.

Verified on 2026-06-30:

- `-Fast` passed environment check, ISSI controller simulation, and R120
  wrapper RMII RX simulation.
- `-SkipTcpSim` passed the same checks plus Gowin debug/prod builds; both
  profiles reported `setup=0`, `hold=0`, normal firmware rebuilt as
  `14878 darksocv.mem` / `59000` UART bytes, and the production netlist marker
  search passed.
- Full default regression passed with log
  `C:\Users\User\AppData\Local\Temp\r120_ext_ram_regression_20260630_164839.log`.
  It includes the TCP-data PSRAM self-test step, rebuilt normal firmware, and
  finished with `R120 external PSRAM TCP/MSOP regression PASS`.
- After the tee-log fix, `-Fast` passed again with detailed log
  `C:\Users\User\AppData\Local\Temp\r120_ext_ram_regression_fast_logged_20260630_1652.log`;
  the log contains `IS66WVS1M8 controller simulation PASS`,
  `R120 valid RMII frame reached eth_rx_check: 60 bytes match`, and final
  `status=PASS`.
- PowerShell 5.1 can turn native-command stderr into a terminating error when
  `$ErrorActionPreference='Stop'`. The full tee-log run at `16:54` exposed this
  on the known RISC-V linker warning `darksocv.o has a LOAD segment with RWX
  permissions`; the wrapper now temporarily uses `Continue` around native
  command capture and relies on `$LASTEXITCODE` for pass/fail.
- Full default regression then passed again with detailed tee log
  `C:\Users\User\AppData\Local\Temp\r120_ext_ram_regression_full_logged_20260630_1656.log`.
  Proof lines in that log include `IS66WVS1M8 controller simulation PASS`,
  `R120 valid RMII frame reached eth_rx_check: 60 bytes match`,
  `darketh sim tcp data synack iss=0000196e`,
  `lidarsim tcp data connected`, `lidarsim psram recovered`,
  `lidarsim psram tcp msop ok len=02f6 slot=00 ops=017e`, `lidarsim ok`,
  `Artifacts OK for R120_LIDAR_EXT_RAM: setup=0 hold=0`,
  `Artifacts OK for R120_LIDAR_EXT_RAM_PROD: setup=0 hold=0`, and final
  `End: 2026-06-30 16:57:32 status=PASS`.
- After adding the TCP payload reassembly assertion, `-SkipGowin` passed with
  detailed log
  `C:\Users\User\AppData\Local\Temp\r120_ext_ram_regression_tcp_payload_20260630_1710.log`.
  The script now explicitly checks the ModelSim transcript for
  `darketh sim tcp data msop payload ok len=02f6`,
  `lidarsim psram tcp msop ok len=02f6`, and `lidarsim ok`. The run rebuilt
  the normal non-self-test firmware afterward as `14878 darksocv.mem` /
  `59000` UART bytes. This is still simulation/tool evidence; it does not prove
  the real R120 PHY RXD0/RXD1 path.
- Full default regression with that payload assertion also passed with log
  `C:\Users\User\AppData\Local\Temp\r120_ext_ram_regression_full_tcp_payload_20260630_1715.log`.
  It includes the same transcript proof line, the explicit script
  `Evidence OK` check, normal firmware rebuild, and Gowin debug/prod builds.
  Debug and production bitstreams were regenerated at `17:11:04` and
  `17:11:53`, respectively, both `7264087` bytes; both timing reports had
  `setup=0`, `hold=0`.
- Submodule reachability check was added on 2026-06-30:
  `scripts\check_submodule_reachability.ps1`. Expected current output for this
  branch is `[MISS] soft_mcu/dark_risc` with SHA
  `4caf55bb79aacfba5d268eb477f63457980d6d09` and message
  `commit is not advertised by remote refs; local recovery bundle:
  scripts\restore_r120_dark_risc.ps1`, plus `[OK ] third_party/lwip`.
  This is a handoff blocker, not a logic failure: the no-hardware regression
  above still passes locally. Resolve by publishing the submodule commit or by
  moving the superproject gitlink to a reachable submodule commit that preserves
  the same PSRAM/TCP MSOP behavior.
- A no-push recovery bridge was added with
  `scripts\restore_r120_dark_risc.ps1` and
  `patches\dark_risc\r120-psram-lwip\`. The bundle verifies as containing
  `refs/heads/codex/r120-psram-lwip ->
  4caf55bb79aacfba5d268eb477f63457980d6d09` and requiring base
  `81ef46ad4bd6b29376e9f813889f897edfeac5c8`. The script refuses to touch a
  dirty `dark_risc` worktree, clones the submodule from `.gitmodules` if needed,
  fetches the exact target from the tracked bundle, and checks out the target
  SHA. It was verified in a temporary clone at
  `C:\Users\User\AppData\Local\Temp\verilog_r120_restore_check_20260630_173010`:
  the script cloned `dark_risc` from GitHub, fetched the bundle, and
  `git submodule status -- soft_mcu/dark_risc` reported the then-current target
  SHA without a leading `-`. After the TCP-three-frame self-test commit, bundle
  verification and `restore_r120_dark_risc.ps1` were rechecked on the working
  checkout: the bundle contains
  `c4476ddbf125a364e5f78739a2f3583bfa04b4f8` and the script reports
  `OK: soft_mcu/dark_risc restored to c4476ddbf125a364e5f78739a2f3583bfa04b4f8`.
  After the TCP5 parameterization commit, the bundle and patch set were
  regenerated for `4caf55bb79aacfba5d268eb477f63457980d6d09`; the handoff
  directory now contains seven `format-patch --binary` files. The regenerated
  bundle was restore-tested from a fresh `dark_risc` clone at
  `C:\Users\User\AppData\Local\Temp\dark_risc_bundle_restore_4caf55b_20260630_193419`:
  fetching the bundle and detaching at
  `4caf55bb79aacfba5d268eb477f63457980d6d09` succeeded, with `HEAD` on
  `test: параметризовать TCP MSOP self-test`.
  After the compact-header proof-line commit, the bundle and patch set were
  regenerated again for `ddc23608312f810ea52a1ee42bd75d488d7dd455`; the
  handoff directory now contains eight `format-patch --binary` files, and
  `scripts\restore_r120_dark_risc.ps1` verifies the bundle and reports
  `OK: soft_mcu/dark_risc restored to ddc23608312f810ea52a1ee42bd75d488d7dd455`.
  Use it only as a local recovery bridge until the submodule is published.
- A committed clean-clone handoff check was also verified from
  `C:\Users\User\AppData\Local\Temp\verilog_r120_clean_handoff_20260630_173414`
  with `GWSH` and `PROGRAMMER_CLI` pointing to the external Gowin tools under
  `C:\workspace\verilog\bin`. Full no-hardware regression passed with log
  `C:\Users\User\AppData\Local\Temp\r120_ext_ram_regression_clean_full_handoff_20260630_173654.log`.
  Proof lines include `darketh sim tcp data msop payload ok len=02f6
  segments=2`, `lidarsim psram tcp msop ok len=02f6`, `lidarsim ok`,
  `Artifacts OK for R120_LIDAR_EXT_RAM: setup=0 hold=0`,
  `Artifacts OK for R120_LIDAR_EXT_RAM_PROD: setup=0 hold=0`, and final
  `End: 2026-06-30 17:39:29 status=PASS`.

Generated artifacts:

- `C:\workspace\verilog\20k\LDR_20K\impl\pnr\R120_LIDAR_EXT_RAM.fs`,
  size `7264087` bytes.
- `C:\workspace\verilog\20k\LDR_20K\impl\pnr\R120_LIDAR_EXT_RAM.bin`,
  size `907418` bytes.
- The diagnostic RX-marker build on 2026-06-30 14:58 passed timing with setup
  violated endpoints `0` and hold violated endpoints `0`; `clk_50` actual Fmax
  was `53.563 MHz` against the `50.000 MHz` constraint. Resources were about
  logic `4306/20736` (`20%`), registers `1792/16173` (`11%`), I/O ports `27`,
  BSRAM `82%`, PLL `1/4` (`25%`).
- Temporary UDP diagnostic markers in `R120_lidar_ext_ram_brd_ifm.sv` are gated
  by parameter `ENABLE_DIAG_UDP_MARKERS`, default `1'b1` for bench RX debug
  without UART. The production top wrapper `R120_lidar_ext_ram_prod_brd_ifm`
  instantiates the same core with `ENABLE_DIAG_UDP_MARKERS=1'b0`.
- `build_r120_lidar_ext_ram.tcl` selects the R120 profile through environment
  variable `R120_LIDAR_EXT_RAM_PROFILE`: unset or `debug` builds
  `R120_LIDAR_EXT_RAM.*` with diagnostic UDP marker instances; `rxscope` builds
  `R120_LIDAR_EXT_RAM_RXSCOPE.*` with top
  `R120_lidar_ext_ram_rxscope_brd_ifm`; `prod` builds
  `R120_LIDAR_EXT_RAM_PROD.*` with top `R120_lidar_ext_ram_prod_brd_ifm`.
  Keep the profile output bases separate so debug packet-capture evidence is
  not overwritten by the clean production image.
- Verified on 2026-06-30 15:01 with the current rebuilt `darksocv.mem`: both
  debug and production profiles completed PnR and bitstream generation with
  setup/hold violated endpoints `0/0`.
  Debug artifacts were
  `C:\workspace\verilog\20k\LDR_20K\impl\pnr\R120_LIDAR_EXT_RAM.fs`
  (`7264087` bytes) and `.bin` (`907418` bytes), with worst setup slack
  `1.330 ns`.
  Production artifacts were
  `C:\workspace\verilog\20k\LDR_20K\impl\pnr\R120_LIDAR_EXT_RAM_PROD.fs`
  (`7264087` bytes) and `.bin` (`907418` bytes); production `clk_50` actual
  Fmax was `54.704 MHz`, worst setup slack was `1.720 ns`, resources were
  logic `3561/20736` (`17%`), registers `1580/16173` (`9%`), I/O ports `27`,
  BSRAM `82%`, PLL `1/4` (`25%`).
  Searching `impl\gwsynthesis\R120_LIDAR_EXT_RAM_PROD.vg` for
  `static_udp`, diagnostic MAC fragments, and `diag_` returned no matches,
  confirming that the temporary UDP marker transmitters are absent from the
  production netlist.
- Verified again on 2026-06-30 15:21-15:22 through the new wrapper entrypoint:
  firmware rebuilt as `14878 darksocv.mem` / `59000` UART bytes; debug output
  `R120_LIDAR_EXT_RAM.fs` timestamp `15:21:14`, `.bin` `907418` bytes,
  setup/hold `0/0`, `clk_50` Fmax `53.563 MHz`; prod output
  `R120_LIDAR_EXT_RAM_PROD.fs` timestamp `15:22:08`, `.bin` `907418` bytes,
  setup/hold `0/0`, `clk_50` Fmax `54.704 MHz`; production netlist search for
  `static_udp|diag_|02_20_20_20_20_0[2-6]` returned no matches.
- RX-scope profile added and verified on 2026-06-30 15:39-15:41. Build with:
  `cd C:\workspace\verilog\20k\LDR_20K; $env:R120_LIDAR_EXT_RAM_PROFILE='rxscope'; & .\build_r120_lidar_ext_ram.cmd; Remove-Item Env:R120_LIDAR_EXT_RAM_PROFILE`.
  It uses the same PSRAM/LwIP firmware and diagnostic UDP markers, but remaps
  LEDs for raw PHY RX visibility: `FPGA_LED2` heartbeat, `FPGA_LED3` stretched
  `EthCrsDv/P11`, `FPGA_LED4` stretched `EthRXD0/T4` transitions,
  `FPGA_LED5` stretched `EthRXD1/R11` transitions. Stretch is
  `2_500_000` cycles of `clk_50`, about `50 ms`.
- RX-scope ModelSim proof uses
  `cd C:\workspace\verilog\src\main; & 'C:\intelFPGA\18.1\modelsim_ase\win32aloem\vsim.exe' -c -do "do R120_lidar_ext_ram_diag_tb.do; quit -f"`.
  The verified run had compile/runtime `Errors: 0` and proof lines
  `R120 rxscope LEDs saw CRS_DV/RXD0/RXD1 activity`,
  `R120 diag marker source MAC 02:20:20:20:20:04 seen`, and
  `R120_lidar_ext_ram_diag_tb PASS`.
- RX-scope Gowin artifacts:
  `C:\workspace\verilog\20k\LDR_20K\impl\pnr\R120_LIDAR_EXT_RAM_RXSCOPE.fs`
  (`7264087` bytes) and `.bin` (`907418` bytes), timestamp `15:41:06`.
  PnR log includes `Placement and routing completed` and
  `Bitstream generation completed`; setup/hold violated endpoints `0/0`;
  `clk_50` Fmax `51.953 MHz`; resources logic `4464/20736` (`21%`),
  registers `1860/16173` (`11%`), BSRAM `82%`, PLL `1/4` (`25%`).

Hardware Ethernet evidence on 2026-06-30:

- Static UDP physical check on `codex/r120-static-udp-r13clk` proved the R120
  TX path. Volatile SRAM programming of
  `R120_STATIC_UDP_SCOPE_R13CLK.fs` reported `User Code: 0x00005AC1`,
  `Status Code: 0x00006020`. Capture
  `C:\Users\User\AppData\Local\Temp\r120_static_udp_physics_20260630_1330.pcapng`
  saw `4873` UDP frames in 5 seconds from `02:20:20:20:20:01`,
  `192.168.2.240 -> 192.168.2.255`, UDP `50100 -> 50100`, payload
  `FPGA_STATIC_UDP_R120_20260629!`.
- A later same-day physical recheck at `2026-06-30 14:40` again loaded
  `R120_STATIC_UDP_SCOPE_R13CLK.fs` to volatile SRAM with `User Code:
  0x00005AC1`, `Status Code: 0x00006020`. Capture
  `C:\Users\User\AppData\Local\Temp\r120_static_udp_physics_recheck_20260630_144045.pcapng`
  saw `5068` total packets in 5 seconds, including `4857` FPGA UDP frames from
  `02:20:20:20:20:01`; fields were `192.168.2.240 -> 192.168.2.255`, UDP
  `50100 -> 50100`, payload `FPGA_STATIC_UDP_R120_20260629!`.
- The LwIP/PSRAM image then used temporary static UDP diagnostic source MACs:
  `...:01` means CPU reached `netif_up`; `...:02` means `eth_rx_frame_valid`;
  `...:03` means CPU wrote TX bytes; `...:04` means raw `EthCrsDv` reached FPGA;
  `...:05` means RMII byte decode; `...:06` means RX drop.
- Diagnostic captures after volatile SRAM programming showed `...:01` present
  but no RX markers: `r120_diag_rx_tx_markers_20260630_1352.pcapng` had
  `...:01 = 119`, `...:02 = 0`, `...:03 = 0`; lower-level RX marker captures
  had `...:01 = 118/119`, `...:02..06 = 0`.
- Removing FPGA pull-ups from `EthRXD0/T4`, `EthRXD1/R11`, and `EthCrsDv/P11`
  was the correct strap-hygiene change because these LAN8742A pins are
  `MODE0/1/2` straps, but it did not restore RX by itself.
- A raw unicast stress capture sent 200 Ethernet frames directly to
  `eth.dst == 02:20:20:20:20:01`; `...:04` still remained `0`. Therefore the
  then-current blocker was below LwIP/darketh/PSRAM: the packet-marker image
  did not observe `EthCrsDv` from the PHY even while the network sent broadcast
  and direct unicast frames and the FPGA TX marker remained visible.
- After the 14:40 static check, the board was restored to
  `R120_LIDAR_EXT_RAM.fs` (`User Code: 0x00007563`, `Status Code: 0x00006020`).
  Passive capture
  `C:\Users\User\AppData\Local\Temp\r120_lwip_after_physics_recheck_20260630_144213.pcapng`
  saw `...:01 = 29` in 3 seconds and `...:02..06 = 0`. Active probe
  `C:\Users\User\AppData\Local\Temp\r120_lwip_active_rx_probe_20260630_144320.pcapng`
  captured all `20` host NET_CONFIG broadcast frames on UDP `50103`, but FPGA
  still produced only `...:01 = 59`; `...:04` stayed `0`.
- Board-interface diagnostic simulation was added on 2026-06-30:
  `C:\workspace\verilog\src\main\R120_lidar_ext_ram_diag_tb.sv` with runner
  `C:\workspace\verilog\src\main\R120_lidar_ext_ram_diag_tb.do`.
  Command:
  `cd C:\workspace\verilog\src\main; & 'C:\intelFPGA\18.1\modelsim_ase\win32aloem\vsim.exe' -c -do "do R120_lidar_ext_ram_diag_tb.do; quit -f"`.
  The test stubs the PLL and SoC, pulses the physical wrapper input `EthCrsDv`,
  decodes RMII TX, and passed with compile/runtime `Errors: 0`. Proof lines:
  `R120 diag marker source MAC 02:20:20:20:20:04 seen` and
  `R120_lidar_ext_ram_diag_tb PASS`.
- That simulation proves the debug HDL does not mask raw `EthCrsDv`: a pulse at
  the board-interface input reaches `diag_crs_seen` and emits the expected
  marker. If hardware captures still lack `...:04`, keep the primary suspect
  at the physical PHY RX boundary: LAN8742A CRS_DV/RXD0/RXD1 pins, FPGA
  P11/T4/R11 pins, board rework/traces, reset/strap mode, or PHY receive state.
- The same R120 board-interface diagnostic test was extended on 2026-06-30
  16:29 to cover a full valid RMII receive frame, not only a raw `CRS_DV`
  pulse. It drives `EthCrsDv/EthRXD0/EthRXD1` from
  `rmii_tx_w_buf #(.WITH_PR_AND_CRC32(1))`, sends a 60-byte Ethernet frame to
  local MAC `02:20:20:20:20:01`, byte-compares the `eth_rx_check` output, and
  waits for diagnostic marker MACs `...:02`, `...:04`, and `...:05`.
  Verified ModelSim result: compile/runtime `Errors: 0`, with proof lines
  `R120 eth_rx_frame_valid seen at FPGA wrapper`,
  `R120 valid RMII frame reached eth_rx_check: 60 bytes match`, and
  `R120_lidar_ext_ram_diag_tb PASS`. Therefore LwIP/PSRAM work should not be
  the first suspect until scope/logic-analyzer evidence proves real toggling at
  FPGA pins `P11/T4/R11`.
- FPGA-only RXMON physical check on 2026-06-30 16:13 clarified this blocker.
  `R120_STATIC_UDP_RXMON.fs` was built from top
  `R120_static_udp_rxmon_brd_ifm`, with `PSRAM_CE_N=1` on `J5` so bank 4 and
  `EthRXD0/T4` report BankVccio `3.3`. The image was volatile-programmed with
  `User Code: 0x0000A9C9`, `Status Code: 0x00006020`. Active pcap
  `C:\Users\User\AppData\Local\Temp\r120_rxmon_active_probe_vccio33_20260630_161340.pcapng`
  contained all `250` host raw Ethernet probe frames and `390` FPGA UDP reports
  from source MAC `02:20:20:20:20:10`. RXMON payload changed from
  `R120_RXMON L=3 R=000005BA H=00094A26 E0=00000001 E1=00000001` to
  `R120_RXMON L=3 R=00000825 H=000E1431 E0=00000001 E1=00000001`, i.e.
  `CRS_DV/P11` had activity (`delta_R=619`, `delta_H=313867`) but
  `RXD0/T4` and `RXD1/R11` stayed static high (`delta_E0=0`, `delta_E1=0`).
- The reusable pcap gate is
  `python C:\workspace\verilog\scripts\analyze_r120_rxmon_pcap.py C:\Users\User\AppData\Local\Temp\r120_rxmon_active_probe_vccio33_20260630_161340.pcapng --min-reports 300 --expect-crs-activity --expect-rxd-static`.
  It passed with backend `scapy`, `390` reports, duration `7.780852 s`, and
  `delta R=619 H=313867 E0=0 E1=0`. The negative guard
  `--expect-rxd-activity` exits `1` with `expected RXD0/RXD1 activity`, proving
  the script catches the current no-RXD-transition condition.
- The combined physical-evidence gate is
  `powershell -NoProfile -ExecutionPolicy Bypass -File C:\workspace\verilog\scripts\check_r120_physics_evidence.ps1 -StaticUdpPcap C:\Users\User\AppData\Local\Temp\r120_static_udp_physics_recheck_20260630_154848.pcapng -RxmonPcap C:\Users\User\AppData\Local\Temp\r120_rxmon_active_probe_vccio33_20260630_161340.pcapng -Mode current-blocker`.
  It runs the static UDP TX pcap analyzer and RXMON analyzer together. Use
  `-Mode current-blocker` to reproduce the present known-bad state, and
  `-Mode hardware-pass` as the post-rework acceptance check that requires
  `RXD0/RXD1` activity.
- Treat static UDP evidence as proof of the cable/switch/link/clock/RMII-TX
  path, not as proof of PHY-to-FPGA RX. Until `RXD0/RXD1` activity is proven at
  the FPGA side, do not spend more time on LwIP/TCP/PSRAM packet handling as
  the primary failure mode.
- `rdch.asc` shows the R120 RX path as populated links, not simple direct
  nets: `LAN8742A D9 pin 8 RXD0/MODE0 -> R83 51R -> EthRXD0 -> J12 -> FPGA
  T4`; `D9 pin 7 RXD1/MODE1 -> R85 51R -> EthRXD1 -> J14 -> FPGA R11`;
  `D9 pin 11 CRS_DV/MODE2 -> R81 51R -> EthCrsDv -> J18 -> FPGA P11`.
  `EthRXD0/EthRXD1/EthCrsDv` may also go toward STM32 `PC4/PC5/PA7` through
  `R159/R160/R158 0R`. If CRS works but RXD0/RXD1 do not, inspect `J12/J14`,
  `R83/R85`, and board rework/population first.

Scope/logic-analyzer checks for the current R120 blocker:

- During raw unicast or broadcast traffic, use `CRS_DV` as the control path:
  probe LAN8742A `D9 pin 11`, both sides of `R81`, both sides of `J18`, and
  FPGA `P11/EthCrsDv`; this path should show packet activity and RXMON already
  suggests FPGA sees it.
- Probe LAN8742A `D9 pin 8 RXD0/MODE0`, both sides of `R83`, both sides of
  `J12`, and FPGA `T4/EthRXD0`. Repeat for LAN8742A `D9 pin 7 RXD1/MODE1`,
  both sides of `R85`, both sides of `J14`, and FPGA `R11/EthRXD1`.
- If `R83/R85` PHY-side nodes toggle but FPGA `T4/R11` do not, suspect
  `J12/J14` solder jumpers, missing/changed population, or board rework. If
  LAN8742A `RXD0/RXD1` pins themselves do not toggle while `CRS_DV` does,
  inspect PHY reset/strap/RMII mode and receive state.
- Check `EthRST/T8` and the PHY reset pin: after FPGA programming it should be
  low for about 10 ms, then high.
- Recheck `Ethclkin/R13` and PHY `CLKIN/XTAL1` together with RX if behavior
  changes; expected is continuous 50 MHz CMOS-level clock.
- Keep `EthnlntSel/T6` high-Z from FPGA and verify the board strap holds it
  high during reset.

## R120 External PSRAM Acceptance Audit

Current status on branch `codex/r120-lidar-ext-ram-tcp-msop`, checked on
2026-06-30:

- Goal logic is locally implemented and regression-passing: R120 branch +
  confirmed `IS66WVS1M8` PSRAM + `dev_20k` DarkRISCV/LwIP are integrated, and
  the simulated TCP data stream carries the pig-head MSOP payload through the
  PSRAM-backed ring.
- Clean-clone no-hardware evidence is
  `C:\Users\User\AppData\Local\Temp\r120_ext_ram_regression_clean_full_handoff_20260630_173654.log`.
  Required proof lines are `IS66WVS1M8 controller simulation PASS`,
  `R120 valid RMII frame reached eth_rx_check: 60 bytes match`,
  `darketh sim tcp data msop payload ok len=02f6 segments=2`,
  `lidarsim psram tcp msop ok len=02f6`, `lidarsim ok`,
  `Artifacts OK for R120_LIDAR_EXT_RAM: setup=0 hold=0`,
  `Artifacts OK for R120_LIDAR_EXT_RAM_PROD: setup=0 hold=0`, and final
  `End: 2026-06-30 17:39:29 status=PASS`.
- Current-workspace no-Gowin regression after the pcap/acceptance audit also
  passed:
  `C:\Users\User\AppData\Local\Temp\r120_ext_ram_regression_current_skip_gowin_20260630_180004.log`.
  This run used `run_r120_ext_ram_regression.ps1 -SkipGowin`, so it proves the
  simulator/firmware/TCP-MSOP/PSRAM chain without rebuilding bitstreams. Proof
  lines include `IS66WVS1M8 controller simulation PASS`,
  `R120 valid RMII frame reached eth_rx_check: 60 bytes match`,
  `darketh sim tcp data msop payload ok len=02f6 segments=2`,
  `lidarsim psram tcp msop ok len=02f6 slot=00 ops=017e`, `lidarsim ok`, and
  final `End: 2026-06-30 18:00:49 status=PASS`.
- After strengthening the TCP self-test to require three MSOP frames through
  the PSRAM-backed TCP path, `-SkipGowin` passed with log
  `C:\Users\User\AppData\Local\Temp\r120_ext_ram_regression_tcp3_skip_gowin_20260630_181329.log`.
  The ModelSim TCP client now ACKs payload segments so LwIP can advance beyond
  one `TCP_SND_BUF` window. Proof lines are
  `darketh sim tcp data msop frame ok count=1 len=02f6 frame=0 segments=2`,
  `darketh sim tcp data msop frame ok count=2 len=02f6 frame=1 segments=2`,
  `darketh sim tcp data msop frame ok count=3 len=02f6 frame=2 segments=2`,
  `darketh sim tcp data msop payload ok len=02f6 frames=3 segments=6`,
  `lidarsim psram tcp msop frame ok count=01 len=02f6 slot=00`,
  `lidarsim psram tcp msop frame ok count=02 len=02f6 slot=01`,
  `lidarsim psram tcp msop frame ok count=03 len=02f6 slot=02`,
  `lidarsim psram tcp msop ok len=02f6 frames=03`, and `lidarsim ok`. This
  proves sequential pig-head MSOP frames traversed PSRAM slots `00/01/02` and
  were emitted as TCP payload; it is still no-hardware evidence.
- The same new target was verified from a committed clean local clone at
  `C:\Users\User\AppData\Local\Temp\verilog_r120_tcp3_clean_20260630_182252`.
  The sequence was: clone branch `codex/r120-lidar-ext-ram-tcp-msop`, run
  `scripts\restore_r120_dark_risc.ps1` to restore
  `c4476ddbf125a364e5f78739a2f3583bfa04b4f8` from the tracked bundle, run
  `git submodule update --init -- third_party/lwip`, set external Gowin tool
  overrides, then run `run_r120_ext_ram_regression.ps1 -SkipGowin`. Log:
  `C:\Users\User\AppData\Local\Temp\r120_ext_ram_regression_tcp3_clean_20260630_182252.log`.
  Required proof lines were present and final status was
  `End: 2026-06-30 18:26:45 status=PASS`.
- Current workspace full no-hardware regression after the TCP-three-frame
  self-test also passed with Gowin debug and production bitstream builds:
  `C:\Users\User\AppData\Local\Temp\r120_ext_ram_regression_tcp3_full_20260630_183656.log`.
  It was run without `-SkipGowin`, so it covered the environment check,
  `IS66WVS1M8` controller simulation, R120 board-wrapper RMII RX simulation,
  the DarkRISCV/LwIP TCP-data PSRAM self-test, normal firmware rebuild, and
  both R120 Gowin profiles. Proof lines include
  `darketh sim tcp data msop payload ok len=02f6 frames=3 segments=6`,
  `lidarsim psram tcp msop frame ok count=03 len=02f6 slot=02`,
  `lidarsim psram tcp msop ok len=02f6 frames=03`,
  `Artifacts OK for R120_LIDAR_EXT_RAM: setup=0 hold=0`,
  `Artifacts OK for R120_LIDAR_EXT_RAM_PROD: setup=0 hold=0`, and final
  `End: 2026-06-30 18:42:18 status=PASS`. Generated bitstreams were
  `R120_LIDAR_EXT_RAM.fs` and `R120_LIDAR_EXT_RAM_PROD.fs`, both `7264087`
  bytes, with matching `.bin` files of `907418` bytes.
- The standard TCP-data PSRAM self-test was then parameterized and raised to
  five frames by default. `scripts\run_r120_ext_ram_regression.ps1` accepts
  `-TcpSelfTestFrames` (default `5`), passes
  `LIDARSIM_PSRAM_TCP_SIM_FRAMES=<N>` into the self-test firmware build, and
  passes `+define+DARKETH_LWIP_TCP_DATA_TARGET_FRAMES=<N>` into
  `sim\darksimv.v`. `scripts\check_r120_goal_acceptance.ps1` has the same
  default and computes the expected final PSRAM ring slot as `(N - 1) % 4`.
  Full no-hardware regression with Gowin passed with log
  `C:\Users\User\AppData\Local\Temp\r120_ext_ram_regression_tcp5_full_20260630_1919.log`.
  Proof lines include `darketh sim tcp data msop payload ok len=02f6 frames=5
  segments=10`, PSRAM frame slots `00/01/02/03/00`, final
  `lidarsim psram tcp msop frame ok count=05 len=02f6 slot=00`, final
  `lidarsim psram tcp msop ok len=02f6 frames=05 slot=00`,
  `Artifacts OK for R120_LIDAR_EXT_RAM: setup=0 hold=0`,
  `Artifacts OK for R120_LIDAR_EXT_RAM_PROD: setup=0 hold=0`, and final
  `End: 2026-06-30 19:27:10 status=PASS`.
- The TCP-data ModelSim self-test now emits and the regression/acceptance
  scripts require an explicit compact pig-head header proof line:
  `darketh sim tcp data msop header ok points=180 angle_res=2000 dist_bytes=2 echo=3/2`.
  This is in addition to byte-level checks inside `sim\darksimv.v` for the MSOP
  markers, frame number, point count, scan mode, shot period, rotation speed,
  angle resolution, distance byte count, echo mode/count, and tail marker.
  Verified current full no-hardware regression log:
  `C:\Users\User\AppData\Local\Temp\r120_ext_ram_regression_header_full_20260630_200936.log`;
  final status `End: 2026-06-30 20:17:51 status=PASS`.
- The `ddc2360` bundle/restore path was then verified from a fresh local clone
  at `C:\Users\User\AppData\Local\Temp\verilog_r120_ddc2360_restore_20260630_202700`.
  The clone used `scripts\restore_r120_dark_risc.ps1` to clone `dark_risc`
  from GitHub, fetch `ddc23608312f810ea52a1ee42bd75d488d7dd455` from the
  tracked bundle, and initialize `third_party/lwip` from its remote. The
  no-Gowin clean-clone regression passed with log
  `C:\Users\User\AppData\Local\Temp\r120_ext_ram_regression_ddc2360_clean_skip_gowin_20260630_202733.log`.
  Required proof lines included `IS66WVS1M8 controller simulation PASS`,
  `R120 valid RMII frame reached eth_rx_check: 60 bytes match`,
  `darketh sim tcp data msop header ok points=180 angle_res=2000 dist_bytes=2 echo=3/2`,
  `darketh sim tcp data msop payload ok len=02f6 frames=5 segments=10`,
  `lidarsim psram tcp msop frame ok count=05 len=02f6 slot=00`, and final
  `End: 2026-06-30 20:33:57 status=PASS`. The temp clone shows a dirty
  `soft_mcu/dark_risc/src/darksocv.mem` after the run because the verification
  build regenerates tracked firmware artifacts; this is expected temp-clone
  build output, not source drift in the main checkout.
- The same current superproject state was then verified from a clean local
  clone at
  `C:\Users\User\AppData\Local\Temp\verilog_r120_tcp3_full_clean_20260630_184529`.
  The clone restored `dark_risc` from the tracked bundle, initialized
  `third_party/lwip`, used external tool overrides
  `GWSH=C:\workspace\verilog\bin\IDE\bin\gw_sh.exe` and
  `PROGRAMMER_CLI=C:\workspace\verilog\bin\Programmer\bin\programmer_cli.exe`,
  and passed full `run_r120_ext_ram_regression.ps1` without `-SkipGowin`.
  Log:
  `C:\Users\User\AppData\Local\Temp\r120_ext_ram_regression_tcp3_clean_full_20260630_184529.log`.
  Required proof lines were present, including three TCP MSOP frames through
  PSRAM, both Gowin artifact checks, and final
  `End: 2026-06-30 18:51:11 status=PASS`. The temp clone's `soft_mcu/dark_risc`
  may show lowercase `m` after the regression because the firmware/Gowin build
  generates artifacts inside the submodule; do not treat that temp-clone status
  as source drift in the main checkout.
- A read-only goal acceptance gate was added as
  `scripts\check_r120_goal_acceptance.ps1`. It does not program hardware. It
  verifies a full `run_r120_ext_ram_regression.ps1` log for the required
  `IS66WVS1M8`, board-wrapper RX, compact pig-head MSOP header proof, TCP MSOP
  PSRAM frame count selected by `-TcpSelfTestFrames` (default five), `lidarsim`, and
  debug/prod Gowin artifact proof lines. It then runs
  `scripts\check_r120_constraints.ps1`, which checks R120 `.cst` pin LOC,
  `IO_TYPE=LVCMOS33`, and critical pull modes for `R120_lidar_ext_ram`,
  static UDP, RXMON, and PSRAM self-test profiles. The constraint audit covers
  `Ethclkin/R13`, TX pins `T7/P6/R8`, `EthRST/T8`, high-Z strap pins
  `EthRefCLK/P8` and `EthnlntSel/T6`, RX pins `EthRXD0/T4`,
  `EthRXD1/R11`, `EthCrsDv/P11`, and the `IS66WVS1M8` pins. After that it
  runs the physical pcap gate and the submodule reachability gate. It also
  checks a real
  `lconf --lidar-smoke` transcript through `-LconfSmokeLog` when
  `-Mode acceptance` is selected. The smoke log must include `PASS discovery`,
  `PASS udp-full-status`, `PASS udp-firmware text=pegus_1`, `PASS tcp-command`,
  at least two `msop frame=... bytes=758 points=180 angle_res=2000
  dist_bytes=2 echo=3/2` lines for the compact two-echo pig-head payload,
  `PASS tcp-data`, and `PASS lidar-smoke`.
  Use `-Mode acceptance` only for a final post-rework check: it requires
  physical `hardware-pass`, lconf TCP/MSOP smoke, and no skipped final gates.
  Use `scripts\run_r120_lconf_smoke.ps1` after the RXD0/RXD1 hardware fix to
  capture the real `lconf --lidar-smoke` transcript and optionally feed it
  straight into the acceptance audit with `-RunAcceptanceAudit`. On 2026-06-30
  the `lconf` smoke CLI source was updated to accept both the old single-echo
  simulator format and the current compact pig-head format; the R120 acceptance
  gate intentionally requires the compact pig-head `dist_bytes=2 echo=3/2`
  lines.
  Use
  `-Mode current-blocker -AllowLocalBundleOnly` for the present no-push audit
  where no-hardware regression passes, the RXD0/RXD1 blocker is reproduced, and
  `soft_mcu/dark_risc` is recoverable only from the tracked bundle.
  Verified current command:
  `powershell -NoProfile -ExecutionPolicy Bypass -File C:\workspace\verilog\scripts\check_r120_goal_acceptance.ps1 -RegressionLog C:\Users\User\AppData\Local\Temp\r120_ext_ram_regression_e02e551_full_20260630_2132.log -Mode current-blocker -StaticUdpPcap C:\Users\User\AppData\Local\Temp\r120_static_udp_physics_recheck_20260630_154848.pcapng -RxmonPcap C:\Users\User\AppData\Local\Temp\r120_live_rxmon_no_program_20260630_183409.pcapng -AllowLocalBundleOnly`.
  Verified result: `CURRENT-BLOCKER AUDIT PASS`. The same command with
  `-Mode acceptance -SkipSubmoduleReachability` currently exits `1` at
  `expected RXD0/RXD1 activity`, which is the intended guard against closing
  the hardware goal early. If `-SkipPhysical`, `-SkipNetworkSmoke`, or
  `-SkipSubmoduleReachability` are used in acceptance mode, the script prints
  `ACCEPTANCE PARTIAL AUDIT PASS ... This is not final acceptance` instead of a
  final `ACCEPTANCE PASS`.
- Physical evidence is split by direction. Static UDP pcap proves the R120
  cable/switch/link/R13CLK/RMII-TX path. RXMON pcap proves `CRS_DV/P11`
  activity but also proves `RXD0/T4` and `RXD1/R11` are static in the current
  hardware state. Reproduce with:
  `powershell -NoProfile -ExecutionPolicy Bypass -File C:\workspace\verilog\scripts\check_r120_physics_evidence.ps1 -StaticUdpPcap C:\Users\User\AppData\Local\Temp\r120_static_udp_physics_recheck_20260630_154848.pcapng -RxmonPcap C:\Users\User\AppData\Local\Temp\r120_rxmon_active_probe_vccio33_20260630_161340.pcapng -Mode current-blocker`.
- The real R120 TCP/MSOP network goal is not complete until fresh hardware
  evidence proves `RXD0/RXD1` transitions at the FPGA side and then the
  `R120_LIDAR_EXT_RAM` image passes the normal lidar network smoke/data check.
  The post-fix physical acceptance command is the same pcap gate with
  `-Mode hardware-pass`; it currently fails with `expected RXD0/RXD1 activity`.
- Handoff is locally recoverable but not remote-clean: `soft_mcu/dark_risc`
  gitlink `71a91ab76c2df171bb5020b12c9d86082ff886df` is not advertised by
  `https://github.com/fufellen/dark_risc.git`. The tracked bundle plus
  `scripts\restore_r120_dark_risc.ps1` restores the local submodule for clean
  clones, but `scripts\check_submodule_reachability.ps1` must keep failing
  until the submodule commit is published or the gitlink is moved to an
  equivalent reachable commit.
- The committed superproject state `c803c7123c3f44a0bc7e44c7aabe3fc9142db55e`
  was verified from a fresh local clone with a full no-hardware Gowin
  regression. Clone:
  `C:\Users\User\AppData\Local\Temp\verilog_r120_c803c712_full_clean_20260630_203700`.
  Restore log:
  `C:\Users\User\AppData\Local\Temp\r120_c803c712_restore_20260630_203700.log`.
  Regression log:
  `C:\Users\User\AppData\Local\Temp\r120_ext_ram_regression_c803c712_clean_full_20260630_203736.log`.
  The run restored `dark_risc` commit
  `ddc23608312f810ea52a1ee42bd75d488d7dd455` from the tracked bundle,
  initialized `third_party/lwip` at `3d896ba0...`, used external Gowin/toolchain
  overrides from `C:\workspace\verilog\bin` and `C:\msys64`, and ended with
  `End: 2026-06-30 20:45:42 status=PASS`. Required proof lines included
  `IS66WVS1M8 controller simulation PASS`,
  `R120 valid RMII frame reached eth_rx_check: 60 bytes match`,
  `darketh sim tcp data msop header ok points=180 angle_res=2000 dist_bytes=2 echo=3/2`,
  `darketh sim tcp data msop payload ok len=02f6 frames=5 segments=10`,
  `lidarsim psram tcp msop ok len=02f6 frames=05 slot=00 ops=076e`, and both
  Gowin artifact checks with `setup=0 hold=0`. The same clean full log passed
  `scripts\check_r120_goal_acceptance.ps1 -Mode current-blocker
  -AllowLocalBundleOnly` against the known static UDP and RXMON pcaps, with
  result `CURRENT-BLOCKER AUDIT PASS`. Final goal acceptance still requires a
  fresh hardware-pass where `RXD0/RXD1` toggle at the FPGA side plus a real
  `lconf --lidar-smoke` TCP/MSOP transcript.
- On 2026-06-30, the optional TCP/MSOP PSRAM stress target was raised to
  `-TcpSelfTestFrames 16` after fixing the ModelSim watchdog in
  `sim/darksimv.v` to scale with `DARKETH_LWIP_TCP_DATA_TARGET_FRAMES`.
  The new submodule commit is `e02e5511e0cc786ab8d83d965379e76c522dad92`
  (`test: масштабировать TCP MSOP sim timeout`). The 16-frame no-Gowin
  regression log is
  `C:\Users\User\AppData\Local\Temp\r120_ext_ram_regression_tcp16_skip_gowin_20260630_2110.log`;
  it ended with `End: 2026-06-30 21:28:29 status=PASS` and proved
  `darketh sim tcp data msop payload ok len=02f6 frames=16 segments=32`,
  `lidarsim psram tcp msop frame ok count=10 len=02f6 slot=03 ops=17c2`, and
  `lidarsim psram tcp msop ok len=02f6 frames=10 slot=03 ops=17c2`. This
  covers four full wraps of the four-slot PSRAM ring. The bundle and patch
  bridge were regenerated as `0001..0009`; `scripts\restore_r120_dark_risc.ps1`
  restored `e02e551...` in the working checkout, and a fresh GitHub
  `dark_risc` clone at
  `C:\Users\User\AppData\Local\Temp\dark_risc_bundle_restore_e02e551_20260630_213109`
  fetched the bundle and checked out the same SHA. A full no-hardware Gowin
  regression on the current checkout passed with log
  `C:\Users\User\AppData\Local\Temp\r120_ext_ram_regression_e02e551_full_20260630_2132.log`,
  final `End: 2026-06-30 21:39:14 status=PASS`, and both debug/prod artifact
  checks `setup=0 hold=0`. The current-blocker acceptance audit on that log
  also passed with `CURRENT-BLOCKER AUDIT PASS`.
- The committed superproject state `91ca57ccd3954a4a19409bf2c4522d7f7c7afd5d`
  was then verified from a fresh local clone with the full no-hardware Gowin
  regression. Clone:
  `C:\Users\User\AppData\Local\Temp\verilog_r120_91ca57cc_clean_20260630_214438`.
  Restore log:
  `C:\Users\User\AppData\Local\Temp\r120_91ca57cc_restore_20260630_214438.log`.
  Regression log:
  `C:\Users\User\AppData\Local\Temp\r120_ext_ram_regression_91ca57cc_clean_full_20260630_2145.log`.
  The run restored `dark_risc` commit
  `e02e5511e0cc786ab8d83d965379e76c522dad92` from the tracked bundle,
  initialized `third_party/lwip` at `3d896ba0...`, used the external Gowin and
  MSYS2 tool overrides, and ended with `End: 2026-06-30 21:55:48 status=PASS`.
  Required proof lines included `IS66WVS1M8 controller simulation PASS`,
  `R120 valid RMII frame reached eth_rx_check: 60 bytes match`,
  `darketh sim tcp data msop header ok points=180 angle_res=2000 dist_bytes=2 echo=3/2`,
  `darketh sim tcp data msop payload ok len=02f6 frames=5 segments=10`,
  `lidarsim psram tcp msop ok len=02f6 frames=05 slot=00 ops=076e`, and both
  Gowin artifact checks with `setup=0 hold=0`. The same clean full log passed
  `scripts\check_r120_goal_acceptance.ps1 -Mode current-blocker
  -AllowLocalBundleOnly`, reproducing the split physical verdict: static UDP
  proves TX/link/R13CLK/RMII-TX, while RXMON still proves `CRS_DV/P11`
  activity with static `RXD0/T4` and `RXD1/R11`.

## R120 PSRAM SPI/QSPI Hardware Verdict

Verified on 2026-07-01 after the user returned the Ethernet cable:

- The QSPI-capable PSRAM MMIO path is parameterized through
  `darksocv.PSRAM_USE_QSPI` and `darkpsram_mmio.USE_QSPI`. In QSPI mode it uses
  PSRAM command `38h` for quad write and `EBh` for quad read with six wait
  cycles. Simulation/benchmark evidence showed the QSPI path is faster than the
  conservative SPI `02h/03h` path, but this is not sufficient hardware evidence
  for the R120 bench.
- Real QSPI hardware evidence is negative/blocked for the current R120 image.
  A QSPI image with `User Code: 0x0000AFEE` first passed short
  `lconf --lidar-smoke` after volatile reload, but a direct 200-frame TCP MSOP
  capture stopped at `89/200` frames with `stop_reason=socket-timeout`, one
  corrupted frame-number jump `12 -> 3024 -> 14`, and then TCP ports
  `50100/50101/50102` timed out while the FPGA static UDP heartbeat continued.
  Logs:
  `C:\Users\User\AppData\Local\Temp\r120_qspi_msop_200_diag_20260701_134213.log`
  and
  `C:\Users\User\AppData\Local\Temp\r120_qspi_msop_200_diag_20260701_134213.jsonl`.
- A later QSPI/fault-backoff image with `User Code: 0x0000AFEE` did not answer
  discovery immediately after volatile programming. Passive pcap
  `C:\Users\User\AppData\Local\Temp\r120_faultbackoff_qspi_after_smoke_fail_passive_20260701_135833.pcapng`
  still saw `48` FPGA heartbeat packets in `4.7 s` from
  `02:20:20:20:20:01`, payload `FPGA_STATIC_UDP_R120_20260629!`, proving the
  Ethernet TX/link/FPGA heartbeat layer was alive while soft-MCU/LwIP was not.
- The accepted R120 hardware baseline is conservative SPI mode:
  `src\main\R120_lidar_ext_ram_brd_ifm.sv` defaults
  `PSRAM_USE_QSPI = 1'b0`. The SPI fallback build
  `C:\workspace\verilog\20k\LDR_20K\impl\pnr\R120_LIDAR_EXT_RAM.fs`
  (`SHA256 71379530E08E36253144A365EE7E8B245C719F9E31164F2DCA1EDB7C539A5D91`)
  passed timing with setup/hold violated endpoints `0/0`, was volatile-loaded
  with `User Code: 0x00007563`, `Status Code: 0x00006020`, passed full
  `lconf --lidar-smoke`, captured direct TCP MSOP `200/200` frames, and passed
  a second `lconf --lidar-smoke` after that load. Logs:
  `C:\Users\User\AppData\Local\Temp\r120_lconf_smoke_spi_fallback_20260701_140244.log`,
  `C:\Users\User\AppData\Local\Temp\r120_spi_fallback_msop_200_20260701_140309.log`,
  `C:\Users\User\AppData\Local\Temp\r120_spi_fallback_msop_200_20260701_140309.jsonl`,
  and
  `C:\Users\User\AppData\Local\Temp\r120_lconf_smoke_spi_fallback_after_msop200_20260701_140354.log`.
- The aligned no-Gowin regression for the SPI baseline also passed:
  `C:\Users\User\AppData\Local\Temp\r120_ext_ram_regression_spi_baseline_skip_gowin_20260701_140844.log`,
  final `End: 2026-07-01 14:15:14 status=PASS`. Required evidence included
  `darkpsram_mmio mode=SPI`, five TCP MSOP frames through PSRAM, and the normal
  R120 PSRAM firmware rebuild.
- Future R120 acceptance/regression should prove the working SPI baseline unless
  the task explicitly targets QSPI. Treat QSPI as experimental until a separate
  hardware capture proves stable `38h/EBh` transactions and a long TCP MSOP
  stream without frame corruption or LwIP loss. If higher PSRAM throughput is
  still required, prefer a deliberate PSRAM clock-domain/CDC design and a
  DSView/oscilloscope capture over raising the shared 50 MHz RMII/CPU clock.

## Open Integration Work

- Add a runtime-controlled remote UDP peer/port policy only if the application needs more than echoing to the incoming packet source.
- Keep extending the same runtime config path for future protocol fields instead of hardcoding new constants in HDL.
- For deeper soak, extend beyond the verified 16-frame TCP/MSOP PSRAM stress
  test only when the extra ModelSim runtime is worth it.
- Fix the TCP bootloader FLASH erase path so `lconf --cli` on port `50102` can complete again in the shared-switch image. The live `FLASH_SPI` programmer is hardware-verified, but it is a fallback, not a replacement for the GUI/bootloader file-select flow.
- If internal visibility is needed, use a reduced-depth Gowin Analyzer Oscilloscope profile; full-depth GAO plus soft-MCU BRAMs can exceed the 20K BSRAM budget.

## darkio timer / sys_now trap (verified on hardware 2026-07-03)

- `io->timeus` (and therefore lwIP `sys_now()`) advances ONLY while
  `io->timer` (TIMERFF, reg 0x0C) is non-zero: in darkio.v the whole
  microsecond-counter block is gated by `if(TIMERFF)`.
- lwipdemo historically never wrote `io->timer`, so on hardware
  `sys_now()` stayed 0 forever: every `sys_now()`-based rate limiter
  printed on each event (UART print storm of `lidarsim rx flags`),
  `service_arp_refresh` never fired its 2 s / 30 s gates, and
  `sys_check_timeouts()` never ran any lwIP cyclic timer (TCP
  retransmissions dead). Soak tests still passed because the defenses
  that mattered are count-based, and a quiet bench LAN has ~no loss.
- Fix: write `io->timer` once at the start of `main()` (any non-zero
  value; `io->board_cm * 2000000u - 1u` gives a 1 Hz IRQ divider).
  With `__INTERRUPT__` commented out in `rtl/config.vh` the IRQ toggle
  only sets a status bit and is harmless to the core.
- Symptom to recognize: rate-limited prints flooding the UART = frozen
  `sys_now()`; check `io->timer` before debugging the limiter logic.

## SoC ModelSim gotchas (R120M LTDC/W5500 work, verified 2026-07-06)

- **Firmware busy-waits hang the SoC sim for HOURS.** A bare-metal wait loop
  with a large iteration cap (e.g. `for(i=0;i<50000000u;i++) if(cond) break;`)
  is harmless on hardware, but in ModelSim every iteration is many clock
  cycles; if `cond` never becomes true the simulator grinds through tens of
  millions of cycles and looks hung (observed: a run stuck >1 h vs the normal
  few minutes). Always (1) run SoC sims under a wall-clock watchdog and kill
  past a few minutes, and (2) bound firmware wait loops to a realistic sim
  budget so an unmet condition FAILs fast instead of spinning. Symptom: sim
  wall-time far exceeds normal with no new transcript output = an unmet
  firmware wait, not slow compute.
- **MFCU is required** (`vlog -sv -mfcu ...`) when the SoC sim compiles `src/`
  modules that include `../machines/machine_header.sv` (packages
  `package_types`, `package_TDC_types`) alongside the dark_risc RTL. Without
  `-mfcu` each file is its own compilation unit and the packages collide;
  vsim reports `Recompile ... because package_types ... changed`. Added to
  `sim/darksimv_modelsim.do`.
- **EF_PSRAM_CTRL.v must be LAST in the compile list.** It sets
  `` `default_nettype none ``; under MFCU that directive leaks into every file
  compiled after it, so a later file with implicit-net ports fails with
  `EX3094 Net type must be explicitly specified`. The same ordering rule
  already applies in the Gowin build tcl.
- **Submodule in a git worktree with a local `file://` URL** needs
  `git -c protocol.file.allow=always submodule update --init soft_mcu/dark_risc`;
  plain `git submodule update` fails with `transport 'file' not allowed`. The
  worktree `.git/config` submodule URL points at the sibling checkout.
