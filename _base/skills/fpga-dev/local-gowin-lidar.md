# Local Gowin Lidar FPGA Reference

Use this reference for the local lidar FPGA workspace.

## Main Paths

- FPGA repo: `C:\workspace\verilog`
- Main 20K project: `C:\workspace\verilog\20k\LDR_20K`
- Build wrapper: `C:\workspace\verilog\20k\LDR_20K\build_gowin.cmd`
- Build TCL: `C:\workspace\verilog\20k\LDR_20K\build_gowin.tcl`
- Gowin CLI: `C:\workspace\verilog\bin\IDE\bin\gw_sh.exe`
- Output directory: `C:\workspace\verilog\20k\LDR_20K\impl\pnr`
- Programmer batch: `C:\workspace\verilog\20k\programming20K.bat`
- ModelSim notes: `C:\workspace\verilog\docs\modelsim.md`

## LDR_20K Build

Run from `C:\workspace\verilog\20k\LDR_20K`:

```cmd
build_gowin.cmd
```

Equivalent explicit CLI:

```cmd
C:\workspace\verilog\bin\IDE\bin\gw_sh.exe build_gowin.tcl
```

The TCL flow sets:

- Device: `GW2A-18C` / `GW2A-LV18PG256C8/I7`
- Output base: `LDR_20K`
- Top module: `R120_M_1_1_0_brd_ifm`
- Verilog standard: `sysv2017`
- Synthesis tool: `gowinsynthesis`
- Include path: `C:\workspace\verilog\src`
- Key files:
  - `C:\workspace\verilog\20k\LDR_20K\src\o_pll_10_50\o_pll_10_50.v`
  - `C:\workspace\verilog\src\main\main.sv`
  - `C:\workspace\verilog\src\main\R120_M_1_1_0_brd_ifm.sv`
  - `C:\workspace\verilog\src\main\R120_M_1_1_0.cst`
  - `C:\workspace\verilog\20k\LDR_20K\src\20k_time_constraints.sdc`

Expected generated files include:

- `C:\workspace\verilog\20k\LDR_20K\impl\pnr\LDR_20K.fs`
- `C:\workspace\verilog\20k\LDR_20K\impl\pnr\LDR_20K.bin`
- `C:\workspace\verilog\20k\LDR_20K\impl\pnr\LDR_20K.rpt.txt`
- `C:\workspace\verilog\20k\LDR_20K\impl\gwsynthesis\LDR_20K.log`

Inspect these reports after a build before claiming success.

Test FPGA firmware builds should be copied to the shared server folder:

```text
\\192.168.2.50\e\YandexDisk\#Projects\ToF Lidar\!Firmware\FPGA\Тестовые прошивки
```

By default, copy only the generated `.bin` file to this server folder. Do not copy `.fs`,
`.rpt.txt`, timing HTML, or other build artifacts unless the user explicitly asks for them.

## 20K Soft-MCU LwIP Bench Target

Verified on 2026-06-17 on branch `dev_20k`:

- The active soft-MCU/LwIP bench top in `build_gowin.tcl` is `m20k_dev_uart_rmii_debug`, not the lidar production wrapper.
- `build_gowin.cmd` runs the `lwipdemo` firmware build first:
  `C:\msys64\usr\bin\make.exe -C C:\workspace\verilog\soft_mcu\dark_risc\src clean all APPLICATION=lwipdemo NOBANNER=1 CCPATH=C:/msys64/ucrt64/bin`
- The firmware image embedded by Gowin is `C:\workspace\verilog\soft_mcu\dark_risc\src\darksocv.mem`.
- The current 20K dev-board LwIP build produced `C:\workspace\verilog\20k\LDR_20K\impl\pnr\LDR_20K.fs` with size `7264087` bytes.
- Full-depth Gowin Analyzer Oscilloscope/RAO instrumentation can overuse BSRAM together with the soft-MCU/LwIP RAM footprint; keep analyzer profiles separate or reduce capture depth before enabling GAO in this target.

Verified on 2026-06-18 for the LwIP lidar simulator milestone:

- The same bench target now carries a soft-MCU lidar simulator in `lwipdemo`: UDP discovery/control plus TCP command/data servers for model `R120_FAKE` and firmware string `pegus_1`.
- Build-and-program still uses `C:\workspace\verilog\20k\build_and_program20K_volatile.bat`, default programmer speed, and volatile SRAM (`-r 2`).
- Successful SRAM programming evidence: `User Code: 0x00005B6C`, `Status Code: 0x00006020`, cost about 15.4 seconds.
- Generated bitstream: `C:\workspace\verilog\20k\LDR_20K\impl\pnr\LDR_20K.fs`, size `7264087` bytes, report timestamp `Thu Jun 18 11:15:43 2026`.
- PnR resources for this build: logic `3011/20736 14%`, registers `1089/16173 6%`, CLS `1917/10368 18%`, BSRAM `82%` (`SDPB 6`, `DPB 32`), PLL `0/4`.
- DDR3 is not needed for this verified build. If future simulator features outgrow internal BRAM, find and reuse an existing DDR3 example/controller before adding a new memory subsystem.
- Hardware network validation used raw Scapy/Npcap on `Ethernet 5` because adding a secondary Windows IP address to the adapter required administrator rights. UART `COM3` and packet captures confirmed ARP, broadcast discovery, UDP commands, TCP command, and TCP MSOP data.

Verified on 2026-06-18 for the TCP FPGA firmware-loader milestone:

- The same `m20k_dev_uart_rmii_debug` bench target now exposes a soft-MCU TCP firmware-loader server on port `50102` and writes the FPGA section of an lconf firmware package into external SPI FLASH.
- FLASH pins are part of the existing bench top and constraints: `FLASH_SPI_SO=P10`, `FLASH_SPI_SI=R10`, `FLASH_SPI_CS=M9`, `FLASH_SPI_CLK=L10`.
- The bitstream was still loaded to volatile SRAM for the loader itself through `C:\workspace\verilog\20k\build_and_program20K_volatile.bat`; successful evidence: `User Code: 0x00006EAC`, `Status Code: 0x00006020`, cost about `14.51` seconds.
- Gowin outputs for the loader build: `C:\workspace\verilog\20k\LDR_20K\impl\pnr\LDR_20K.fs` size `7264087`, `C:\workspace\verilog\20k\LDR_20K\impl\pnr\LDR_20K.bin` size `907418`, report timestamp `Thu Jun 18 12:21:22 2026`.
- PnR resources for the loader build: logic `3176/20736 15%`, registers `1266/16173 7%`, CLS `2094/10368 20%`, BSRAM `82%`, PLL `0/4`.
- Hardware JEDEC check through UART command `flashid` returned `fwloader flash_id=0b4016 ok=1`.
- Verified TCP FLASH upload command:
  `& 'C:\workspace\lidar\lconf\bin\Release\lconf.exe' --cli --file 'C:\workspace\verilog\20k\LDR_20K\impl\pnr\LDR_20K.bin' --channel tcp --host 192.168.15.20 --port 50102 --erase-timeout 300000 --reply-timeout 30000`
- The upload used the Windows `Ethernet 5` adapter at `192.168.15.13/24`; the board was temporarily set to `192.168.15.20` by UART and restored to `192.168.20.20` afterwards.
- Verified upload evidence: `lconf --cli` reported `FPGA=907520` bytes, erase to `100%`, `Send end`, and `OK: Данные загружена.` UART reported `fwloader end ok bytes=907520 crc=9bbd26fa flash_crc=9bbd26fa`.
- After the FLASH write, `lconf --lidar-smoke` against `192.168.15.20` passed discovery, UDP full-status, UDP/TCP firmware `pegus_1`, and TCP command, proving the SRAM-loaded firmware remained alive after the write.
- Booting from the newly written external FLASH was later power-cycle verified after the live `FLASH_SPI` readback milestone; see below.

Verified on 2026-06-18 for the live FLASH readback milestone:

- The bench firmware now handles lidar command `FLASH_SPI = 0x45` on live command port `50101`, matching the `lconf --flash-dump` path. Firmware upload still uses bootloader TCP port `50102`.
- Current build after adding `FLASH_SPI` readback: `14332 darksocv.mem`, `56816` bytes in `darksocv_uart.bin`; ModelSim 10.5b reported `Errors: 0`, `fwloader sim ok`, and `lidarsim ok`.
- Volatile SRAM programming was rechecked at default programmer speed with `User Code: 0x00006EAC`, `Status Code: 0x00006020`.
- If UART is unavailable after SRAM reload, send exact-MAC UDP `NET_CONFIG` broadcast to discovery port `50103` to move the board to the Windows bench subnet (`02:20:20:20:20:01` -> `192.168.15.20`, host `192.168.15.13`). Wait about one second before smoke tests.
- Full readback command:
  `& 'C:\workspace\lidar\lconf\bin\Release\lconf.exe' --flash-dump --flash-channel tcp --flash-host 192.168.15.20 --flash-port 50101 --flash-local-host 192.168.15.13 --flash-output $env:TEMP\ldr20k_flash_readback_907520.bin --flash-start 0 --flash-length 907520 --flash-chunk 256 --flash-timeout 30000 --flash-retries 5 --flash-connect-timeout 10000 --flash-overwrite`
- Readback evidence: `907520/907520` bytes, `retries=0`, elapsed about `204.4 s`; first `907418` bytes matched `LDR_20K.bin`, and the 102-byte lconf FPGA-only alignment tail was `0x00`.
- The default `lconf --flash-dump` chunk is `512`; with the 320-byte FPGA reply buffer, lconf receives short blocks of `303` bytes and continues correctly. For full-image reads prefer `--flash-chunk 256` to avoid warnings and reduce stress.
- Boot-from-FLASH was power-cycle verified after the user physically replugged board power: the old runtime IP `192.168.15.20` no longer answered, raw Scapy ARP found the board at default `192.168.20.20` with MAC `02:20:20:20:20:01`, then exact-MAC raw Ethernet/IP/UDP `NET_CONFIG` moved it to `192.168.15.20`.
- In that cold-boot check, ordinary Windows socket UDP broadcast `NET_CONFIG` did not move the board, while raw Scapy `sendp()` on `Ethernet 5` did. If the board boots at `192.168.20.20` and the PC adapter is only `192.168.15.13/24`, use a raw broadcast frame for `NET_CONFIG` before normal `lconf` socket tests.
- Post-boot `lconf --lidar-smoke --smoke-host 192.168.15.20 --smoke-local-host 192.168.15.13 --smoke-discovery-target 192.168.15.20 --smoke-skip-data` passed discovery, UDP full-status, UDP firmware `pegus_1`, TCP firmware `pegus_1`, and `PASS lidar-smoke`.
- Post-boot live FLASH readback also passed: `--flash-dump --flash-length 1024 --flash-chunk 256` read `1024/1024` bytes with `retries=0`, and the first 1024 bytes matched `LDR_20K.bin` (`first_mismatch=-1`, dump SHA256 `81775B43521257409089FE5F1E15B8BA92D0C097041092879A804869DAB9E48D`).

Verified on 2026-06-22 for the shared-switch Ethernet FLASH programming milestone:

- Active network: Windows `Ethernet` at `192.168.2.146`, FPGA at `192.168.2.240`, MAC `02:20:20:20:20:01`.
- Current non-DDR `LDR_20K` image built successfully, ModelSim passed, and volatile SRAM programming reported `User Code: 0x00006EAC`, `Status Code: 0x00006020`, cost `14.99` seconds. Timing was still not clean: setup violated endpoints `2`, hold `0`, `EthRefCLK` Fmax `49.735 MHz` against `50 MHz`, worst setup slack `-0.107 ns` in the DarkRISCV register-file path.
- Root `lconf --cli` bootloader upload to TCP port `50102` is not reliable in this image. With `--erase-timeout 900000`, it reached erase progress `35%` and then failed with `Send begin timeout`; the board stayed alive and post-fail smoke passed. Treat this as an open bootloader erase/main-loop starvation issue.
- The recovery and verified Ethernet programming path is the live command-port tool:
  `python C:\workspace\verilog\20k\flash_spi_live_program.py --host 192.168.2.240 --port 50101 --local-host 192.168.2.146 --file C:\workspace\verilog\20k\LDR_20K\impl\pnr\LDR_20K.bin --timeout 30 --chunk 256 --readback $env:TEMP\ldr20k_flash_live_readback_20260622.bin`
- Live programming evidence: raw `.bin` length `907418`, padded length `907520`, erase length `909312`, `.bin` SHA256 `E51E1F1CCFC114473FF2DCCE99878C0B3A196923051C9B321B7373BED54BFE41`, image CRC32 `EA28785A`, erase/write/verify all reached `100%`, readback matched the `.bin`, and the 102-byte tail was all zero.
- Independent `lconf --flash-dump` full readback from port `50101` also passed: `907520/907520`, `retries=0`, elapsed `41.3 s`, first mismatch `-1`, zero tail `True`.
- After `programmer_cli.exe -d GW2A-18C -r 1` reload from external FLASH, TCP ports `50101` and `50102` reopened and `lidar_switch_check.py --smoke --skip-data --no-net-config` passed, proving the Ethernet-written external FLASH image boots.

## Simulation And Compile Checks

Use `C:\workspace\verilog\docs\modelsim.md` as the source of truth for local ModelSim checks. It specifies ModelSim Intel FPGA Edition 10.5b:

```powershell
$MSIM = 'C:\intelFPGA\18.1\modelsim_ase\win32aloem'
```

Before programming hardware, prefer running the relevant ModelSim 10.5b testbench. If no testbench exists yet, run at least a fresh-library ModelSim compile/elaboration check for the firmware top; for simple bench firmware, add a small testbench rather than programming an un-simulated bitstream.

For a fast top compile check, run from `C:\workspace\verilog\src\main` with a fresh work library name and compile:

- `C:/workspace/verilog/20k/LDR_20K/src/o_pll_10_50/o_pll_10_50.v`
- `main.sv`
- `R120_M_1_1_0_brd_ifm.sv`

Expected syntax result is `Errors: 0`. Existing warnings in shared modules may be tolerated, but new warnings near edited files should be investigated.

For real simulation/elaboration with Gowin primitives, compile:

```powershell
C:/workspace/verilog/bin/IDE/simlib/gw2a/prim_sim.v
```

## Programming

Do not program hardware unless explicitly requested.

For local 20K bench work, use the tracked programmer batch:

```text
C:\workspace\verilog\20k\programming20K.bat
```

For Codex-friendly one-shot bench loading, prefer the tracked build-and-program wrapper when it exists:

```text
C:\workspace\verilog\20k\build_and_program20K_volatile.bat
```

It rebuilds `LDR_20K.fs` and programs it once to volatile memory (`-r 2`) without using Ethernet or entering the interactive programmer loop.

The tracked programmer batch writes the fixed `.fs` file:

```text
C:\workspace\verilog\20k\LDR_20K\impl\pnr\LDR_20K.fs
```

It then runs:

```cmd
programmer_cli.exe -d GW2A-18C -r %choice% -f "%fs_path%"
```

Memory choices used by the batch:

- `2`: volatile memory, default
- `5`: nonvolatile memory for 9K
- `37`: external flash memory for 20K

For Gowin Programmer CLI, `-r 5` is `embFlash Erase,Program`: erase and program embedded flash. This was the old nonvolatile mode used for 9K-style targets with embedded flash; it is not the same as 20K external SPI FLASH programming. For 20K dev-board persistent programming use the verified external FLASH/GAO-Bridge mode `-r 37` unless a separate diagnostic proves another exFlash mode.

Prefer `2` for ordinary bench tests: it loads the FPGA into temporary power-dependent memory and avoids changing persistent flash. Use `37` for 20K external flash only when the user explicitly asks for persistent/nonvolatile programming.

Before programming, confirm the selected `.fs` file, target `GW2A-18C`, and memory choice.

For the local 20K dev board, keep the programmer at its default speed unless there is fresh evidence pointing to JTAG signal integrity. Slowing the programmer with manual frequency options did not fix the observed `Cable lost!` failure; after replugging the FTDI cable so both `USB Serial Converter A` and `USB Serial Converter B` were `OK`, default-speed volatile programming succeeded with `Status Code: 0x00006020`.

For persistent 20K external-FLASH programming from Codex, do not run a bare long-lived `programmer_cli.exe` command. Use a tracked one-shot wrapper with a timeout/watchdog, and check for stale `programmer_cli` processes before retrying. A 60-second timeout is enough for detecting a stuck programmer attempt; do not wait 120 or 300 seconds. On 2026-06-19 an external-FLASH attempt left `programmer_cli` running at high CPU after the Codex command was interrupted; the process had to be killed before any safe retry.

Do not synchronously redirect `programmer_cli.exe` stdout/stderr unless the wrapper drains the pipes asynchronously. The CLI prints many progress updates; a direct redirected `System.Diagnostics.Process` wait hit the 60-second watchdog and had to be killed even though the board had already reloaded. For Codex wrappers, prefer `Start-Process -NoNewWindow -PassThru` with a watchdog so logs stream to the terminal and cannot fill a pipe.

The local 20K external-FLASH script historically used `programmer_cli.exe -d GW2A-18C -r 37 -f LDR_20K.fs`, and the user confirmed this mode had worked for programming. Although `programmer_cli --help` labels `-r 37` as `exFlash Erase,Program,Verify thru GAO-Bridge`, do not replace it with `-r 8` or `-r 9` without a separate short diagnostic proving the alternate mode works on this bench. If `-r 37` hangs, first check stale programmer processes, USB cable enumeration, `--scan-cables`, and a short read-code/scan command with a watchdog.

The `programmer_cli.exe` binaries under `C:\workspace\verilog\9k\Programmer\bin` and `C:\workspace\verilog\bin\Programmer\bin` were byte-identical on 2026-06-19, but 20K scripts should prefer the neutral `C:\workspace\verilog\bin\Programmer\bin` path. Do not let the legacy `9k` directory name become evidence that the wrong FPGA family is being programmed.

Use the neutral Programmer path in both tracked 20K wrappers:

- Volatile SRAM: `C:\workspace\verilog\20k\build_and_program20K_volatile.bat`, operation `-r 2`, 60-second watchdog.
- Persistent external FLASH: `C:\workspace\verilog\20k\program20K_external_flash.bat`, operation `-r 37`, 60-second watchdog.

Never run multiple `programmer_cli.exe` commands in parallel, even for read-only diagnostics such as `--scan-cables` and `-r 0`. The FTDI/programmer path is single-client; parallel calls can cause `Cable open failed`, stale zero-CPU `programmer_cli` processes, or misleading scan results. Run programmer diagnostics sequentially and clean up any leftover process before the next attempt.

Before retrying 20K programming after a hang, check Windows device state for both FTDI channels. If `USB Serial Converter B` is in `Error` while `USB Serial Converter A` is `OK`, do not retry FLASH/SRAM programming yet; `programmer_cli --scan-cables` can fail with only `Error: Error found!` and programming attempts can hang. Replug or restart the FTDI programmer device, then require both channels to return to `OK` before programming. Windows can keep stale `Unknown` FTDI entries for old USB ports; what matters for this check is an active matching `USB Serial Converter A` and `USB Serial Converter B` pair with status `OK`.

Verified on 2026-06-19 after an SRAM attempt failed with `Cable lost!` at 76%: Windows PnP showed one `USB Serial Converter A` as `OK` while all `USB Serial Converter B` entries were `Unknown`, but sequential programmer diagnostics still succeeded. `programmer_cli.exe --scan-cables` found `USB Debugger A`, and `programmer_cli.exe -d GW2A-18C -r 0` returned ID `0x0000081B`, User Code `0x00006EAC`, Status `0x00006020`; a single follow-up SRAM `-r 2` retry then completed in `15.24` seconds. Do not launch programming based on PnP alone after a failed attempt, but if scan and read-code both pass with a 15-second watchdog and no stale `programmer_cli` process exists, one SRAM retry is reasonable before asking for a physical replug.

Verified on 2026-06-19 after physically replugging the programmer: both `USB Serial Converter A` and `USB Serial Converter B` returned to `OK`, `programmer_cli --scan-cables` found `USB Debugger A`, and read-code `programmer_cli.exe -d GW2A-18C -r 0` returned ID `0x0000081B`, User Code `0x00006EAC`, Status `0x00006020`. The tracked external-FLASH wrapper using neutral path `C:\workspace\verilog\bin\Programmer\bin\programmer_cli.exe -d GW2A-18C -r 37 -f C:\workspace\verilog\20k\LDR_20K\impl\pnr\LDR_20K.fs` then completed `Program and Verify flash successfully` in `36.06` seconds, confirming that the 60-second watchdog is sufficient when the programmer is healthy.

Verified on 2026-06-19: `programmer_cli.exe -d GW2A-18C -r 1` performs a real FPGA reconfiguration from external FLASH. Before `-r 1`, the board was runtime-configured to `192.168.2.240`; after `-r 1` completed in `1.16` seconds, ARP for `192.168.2.240` stopped answering and the FLASH default `192.168.20.20` answered from MAC `02:20:20:20:20:01`. Use `-r 1` as a controlled soft reboot/reload-from-FLASH check.

Verified on 2026-06-19: the tracked volatile wrapper `C:\workspace\verilog\20k\build_and_program20K_volatile.bat` rebuilds the 20K project, uses the neutral Programmer path, and programs SRAM with `-r 2` under a 60-second watchdog. The SRAM programming phase reported User Code `0x00006EAC`, Status `0x00006020`, and cost `14.13` seconds; after the load, the board answered ARP at default `192.168.20.20`. A direct no-redirect `-r 2` run also completed in `13.31` seconds; before the run the board answered at runtime IP `192.168.15.20`, and after the run `192.168.15.20` stopped answering while default `192.168.20.20` answered. Treat `-r 2` as a real FPGA reload into SRAM that clears volatile runtime network config.

Verified on 2026-06-19: the tracked external-FLASH wrapper `C:\workspace\verilog\20k\program20K_external_flash.bat` completed `-r 37` again in `36.33` seconds and the board reloaded the user design from FLASH. Before `-r 37`, the board had been runtime-configured to `192.168.15.20`; immediately after `Program and Verify flash successfully`, ARP for `192.168.15.20` stopped and default `192.168.20.20` answered. This proves that on the current 20K bench board/image, `-r 37` through GAO-Bridge does not preserve the running runtime config and effectively returns the design to FLASH defaults. Still verify with ARP or `lconf --lidar-smoke` after every persistent write before claiming the device is operational.

Verified on 2026-06-19 for the shared switch network: after moving the board Ethernet cable from direct USB-Ethernet bench to the common switch, the old `Ethernet 5` bench interface stopped seeing the board and the Windows `Ethernet` interface at `192.168.2.146/24` could configure and test it at `192.168.2.240`. Use `C:\workspace\verilog\20k\lidar_switch_check.py --iface Ethernet --host-ip 192.168.2.146 --lidar-ip 192.168.2.240 --smoke` for this scenario. The helper first checks that `.240` is not occupied by a non-target MAC, sends raw exact-MAC `NET_CONFIG` to board MAC `02:20:20:20:20:01`, verifies ARP, then runs `lconf --lidar-smoke`.

Verified on 2026-06-19 for the discovery-compatible persistent lidar simulator image:

- The firmware defaults directly to the shared switch network: MAC `02:20:20:20:20:01`, IP `192.168.2.240`, host/remote IP `192.168.2.146`, ports `50100/50101/50103`, model `R120_FAKE`, firmware `pegus_1`.
- ModelSim 10.5b passed with `Errors: 0`, `lidarsim discovery reply broadcast=0 direct=0`, `fwloader sim ok`, and `lidarsim ok`.
- Volatile SRAM programming through `C:\workspace\verilog\20k\build_and_program20K_volatile.bat` completed with `User Code: 0x00006EAC`, `Status Code: 0x00006020`, cost about `13.1` seconds.
- Normal Windows socket discovery on `192.168.2.146 -> 255.255.255.255:50103` received `LIDAR_RESP` from `192.168.2.240:50103`; `poll_lidar_discovery.py --adapter-ip 192.168.2.146 --broadcast 255.255.255.255 --timeout 1 --json` returned the FPGA device.
- `lconf --lidar-smoke --smoke-host 192.168.2.240 --smoke-local-host 192.168.2.146 --smoke-discovery-target 255.255.255.255 --smoke-timeout 5000` passed discovery, UDP full-status, UDP/TCP firmware `pegus_1`, TCP command, and TCP MSOP data. MSOP frames were `758` bytes with `180` points and `angle_res=2000`.
- Persistent external-FLASH programming through `C:\workspace\verilog\20k\program20K_external_flash.bat` completed `Program and Verify flash successfully` in `36.18` seconds.
- Controlled reload-from-FLASH with `programmer_cli.exe -d GW2A-18C -r 1` completed in `1.04` seconds. Wait about two seconds after this reload before the first socket discovery; after that, `poll_lidar_discovery.py` and full `lconf --lidar-smoke` passed again from the FLASH-loaded image.
- Physical power-cycle was verified after the user replugged board power. After waiting about two seconds, `poll_lidar_discovery.py --adapter-ip 192.168.2.146 --broadcast 255.255.255.255 --timeout 2 --json` found the FPGA at `192.168.2.240`; ARP showed `192.168.2.240 -> 02:20:20:20:20:01`; full `lconf --lidar-smoke --smoke-host 192.168.2.240 --smoke-local-host 192.168.2.146 --smoke-discovery-target 255.255.255.255 --smoke-timeout 5000` passed discovery, UDP full-status, UDP/TCP firmware `pegus_1`, TCP command, and TCP MSOP data from the external-FLASH boot image.

## IS66WVS1M8 SerialRAM Bring-up

Use this section for the old R120_M board with a soldered ISSI
`IS66WVS1M8ALL/BLL` 8 Mbit SPI/QPI SerialRAM.

Local files:

- Before using web search for this board, check the local vault/repo first. The
  user keeps board notes, datasheets, DSView captures, and task checkpoints
  locally, and these should be treated as the primary source for R120_M
  hardware work unless they are missing or internally inconsistent.
- Datasheet: `C:\Users\User\...\Obsidian\...\RAM\IS66WVS1M8ALLBLL.pdf`
- Pin note: `R120_M + IS66WVS1M8BLL-104NLI (connections).md`
- Local repo sandbox: `C:\workspace\verilog\src\RAM\is66wvs1m8`
- Bring-up task note: `C:\workspace\verilog\CODEX\is66wvs1m8_psram_bringup.md`

Board connections recorded from the user's note:

- `CE#` -> `J5`
- `SIO1/SO/MISO` -> `G12`
- `SIO2` -> `H13`
- `SIO0/SI/MOSI` -> `H14`
- `SCLK` -> `J13`
- `SIO3` -> `N10`
- `VDD` -> `+3V3_D`
- `VSS` -> `GND`

Important datasheet facts:

- The chip is byte-addressable, organized as 1M x 8, address bits `A19:0`.
- Power-up default is SPI mode; wait at least `150 us` after VDD is stable.
- Provide at least one clock pulse while `CE#` is high before normal operation.
- Page length is 1024 bytes, and read/write operations wrap within the page.
- Useful bring-up commands:
  - SPI write `02h`
  - SPI read `03h`
  - SPI fast read `0Bh`, 8 wait cycles
  - SPI Quad I/O write `38h`
  - SPI Quad I/O read `EBh`, 6 wait cycles
  - Enter QPI `35h`
  - Exit QPI `F5h`
  - Reset enable/reset `66h` then `99h`

Performance baseline from ModelSim on 2026-07-01:

- The current R120 LwIP/MSOP integration uses `darkpsram_mmio.sv` with
  ordinary SPI `02h` write and `03h` read, 32-bit operations only, and
  firmware polling through MMIO. In the integrated image, `clk_50` drives
  `EF_PSRAM_CTRL`, whose SCK is `clk/2`, so PSRAM SCLK is about `25 MHz`.
- `EF_PSRAM_CTRL_is66wvs1m8_tb.do` now prints raw controller benchmark lines.
  Verified fast regression log:
  `C:\Users\User\AppData\Local\Temp\r120_ext_ram_regression_psram_bench_fast_20260701_130047.log`.
- Raw controller throughput at `clk_50`, before CPU/MMIO/LwIP overhead:
  ordinary SPI `02h+03h` write/read32 pair: `8 bytes / 262 cycles = 1.527 MB/s`;
  QSPI `38h+EBh` pair: `8 bytes / 106 cycles = 3.774 MB/s`;
  QPI `38h+EBh` pair: `8 bytes / 82 cycles = 4.878 MB/s`.
- Treat these as simulator ceilings, not hardware throughput. A real hardware
  benchmark must report effective bytes/s, `op_count`, elapsed cycles/time, and
  readback pass/fail from the actual board. Still, the numbers show that a
  QSPI adapter mode is a better first optimization than only raising SCK in
  the current 1-bit SPI mode.

Open-source controller candidate:

- `https://github.com/efabless/EF_PSRAM_CTRL`
- The controller was designed after the ISSI WVS family, supports SPI, QSPI,
  and QPI modes, and has a small low-level core plus an AHB-Lite wrapper.
- A local sandbox copy of the low-level core is in
  `src/RAM/is66wvs1m8/EF_PSRAM_CTRL.v`; it keeps the Apache-2.0 header and has
  two local bring-up fixes:
  - read sampling uses `counter < final_count` to avoid one extra data sample;
  - QPI short commands use 2 cycles, while SPI short commands use 8 cycles.

Simulation:

```powershell
cd C:\workspace\verilog\src\RAM\is66wvs1m8
& 'C:\intelFPGA\18.1\modelsim_ase\win32aloem\vsim.exe' -c -do EF_PSRAM_CTRL_is66wvs1m8_tb.do
```

Expected final line:

```text
IS66WVS1M8 controller simulation PASS
```

Verified on 2026-06-29 with ModelSim Intel FPGA Edition 10.5b:
compile `Errors: 0, Warnings: 0`; simulation `Errors: 0, Warnings: 0`.

Next hardware tasks:

- Add board-level pin names and `.cst` constraints for `J5/G12/H13/H14/J13/N10`.
- Start with a standalone low-speed SPI RAM self-test before using Quad I/O or QPI.
- Add the 150 us power-up delay and a simple write/read walking-pattern test.
- Program volatile SRAM only for first hardware checks; do not touch persistent
  FPGA flash unless explicitly requested.

## R120_M Ethernet Physical Bring-up

Use this section for the old R120_M/GW2A board Ethernet PHY checks.

Verified on 2026-06-30:

- The working R120 RMII TX clocking mode drives `Ethclkin/R13` from the FPGA
  50 MHz PLL (`H11` 10 MHz -> `o_pll_10_50`), leaves `EthRefCLK/P8` high-Z,
  leaves `EthnlntSel/T6` high-Z, and registers RMII TX outputs on the falling
  edge of `clk_50`.
- Static UDP image
  `C:\workspace\verilog\20k\LDR_20K\impl\pnr\R120_STATIC_UDP_SCOPE_R13CLK.fs`
  was volatile-programmed successfully (`User Code: 0x00005AC1`,
  `Status Code: 0x00006020`) and produced `4873` UDP frames in 5 seconds in
  capture `C:\Users\User\AppData\Local\Temp\r120_static_udp_physics_20260630_1330.pcapng`.
  Source MAC was `02:20:20:20:20:01`, payload was
  `FPGA_STATIC_UDP_R120_20260629!`.
- The same static UDP physical path was rechecked later the same day after
  integration work. Volatile SRAM programming again reported
  `User Code: 0x00005AC1`, `Status Code: 0x00006020`; capture
  `C:\Users\User\AppData\Local\Temp\r120_static_udp_physics_recheck_20260630_141112.pcapng`
  saw `4938` FPGA frames in 5 seconds from `02:20:20:20:20:01`,
  `192.168.2.240 -> 192.168.2.255`, UDP `50100 -> 50100`, payload
  `FPGA_STATIC_UDP_R120_20260629!`. This confirms cable/switch/PHY TX/RMII TX
  and the `Ethclkin/R13` mode are still working; it does not prove PHY RX.
- A third static UDP/R13CLK physical recheck on 2026-06-30 15:48 after the
  user's "check physics first" request used the same volatile SRAM image and
  again reported `User Code: 0x00005AC1`, `Status Code: 0x00006020`. Capture
  `C:\Users\User\AppData\Local\Temp\r120_static_udp_physics_recheck_20260630_154848.pcapng`
  on Windows `Ethernet` saw `5177` total packets and `4957` FPGA UDP frames in
  5 seconds from `02:20:20:20:20:01`, `192.168.2.240 -> 192.168.2.255`, UDP
  `50100 -> 50100`, payload `FPGA_STATIC_UDP_R120_20260629!`. Treat the R120
  cable/switch/PHY TX/RMII TX/R13CLK path as healthy until contradicted by new
  hardware evidence; this still does not prove the PHY-to-FPGA RX path.
- Reproduce the static UDP verdict with:
  `python C:\workspace\verilog\scripts\analyze_r120_static_udp_pcap.py C:\Users\User\AppData\Local\Temp\r120_static_udp_physics_recheck_20260630_154848.pcapng --min-frames 4900 --min-duration 4.9`.
  Verified output: `PASS`, backend `scapy`, matching frames `4957`, total UDP
  frames `4965`, duration `4.989225 s`, first frame `1`, last frame `5177`,
  payload `FPGA_STATIC_UDP_R120_20260629!`.
- The R120 board on this bench has no usable UART path for Codex hardware
  diagnostics. Do not wait for UART evidence; use packet capture, LEDs,
  scope/DSView/GAO, or user-confirmed physical behavior.
- In the LwIP/PSRAM integration image, CPU `netif_up` and FPGA RMII TX were
  proven by diagnostic UDP marker source MAC `02:20:20:20:20:01`, but raw
  `EthCrsDv` marker `02:20:20:20:20:04` stayed at zero during broadcast
  discovery and during 200 raw unicast Ethernet frames sent directly to
  `02:20:20:20:20:01`.
- The RXSCOPE/LwIP diagnostic image
  `C:\workspace\verilog\20k\LDR_20K\impl\pnr\R120_LIDAR_EXT_RAM_RXSCOPE.fs`
  was volatile-programmed on 2026-06-30 15:52 (`User Code: 0x000052FE`,
  `Status Code: 0x00006020`). Passive capture
  `C:\Users\User\AppData\Local\Temp\r120_rxscope_passive_20260630_155322.pcapng`
  saw marker `...:01 = 49`, `...:02..06 = 0`. Active probe capture
  `C:\Users\User\AppData\Local\Temp\r120_rxscope_active_probe_20260630_155418.pcapng`
  confirmed the host put `50` broadcast NET_CONFIG frames and `200` unicast UDP
  frames on `Ethernet`, while FPGA markers were still `...:01 = 79`,
  `...:02..06 = 0`.
- In `R120_lidar_ext_ram_brd_ifm.sv`, marker `02:20:20:20:20:04` is latched
  directly from `if (rmii_rst_n && EthCrsDv) diag_crs_seen <= 1'b1`; it does
  not depend on LwIP, MAC filtering, `eth_rx_check`, or PSRAM.
- A later FPGA-only RX pin monitor clarified the physical picture. Build
  `R120_STATIC_UDP_RXMON.fs` from top `R120_static_udp_rxmon_brd_ifm` with
  `R120_STATIC_UDP_CST=R120_static_udp_rxmon_brd_ifm.cst` and
  `R120_STATIC_UDP_SDC=R120_static_udp_rxmon.sdc`. The top sends UDP reports
  from source MAC `02:20:20:20:20:10` with payload
  `R120_RXMON L=x R=xxxxxxxx H=xxxxxxxx E0=xxxxxxxx E1=xxxxxxxx`, where
  `L={CRS_DV,RXD1,RXD0}`, `R/H` count CRS rises/high cycles, and `E0/E1`
  count any `RXD0/RXD1` transitions. Keep `PSRAM_CE_N=1` on `J5` in this
  profile so Gowin reports bank 4 (`EthRXD0/T4`) as BankVccio `3.3`, matching
  the real R120 integration build.
- RXMON hardware evidence on 2026-06-30 16:13: volatile SRAM programming of
  `R120_STATIC_UDP_RXMON.fs` reported `User Code: 0x0000A9C9`,
  `Status Code: 0x00006020`. Active capture
  `C:\Users\User\AppData\Local\Temp\r120_rxmon_active_probe_vccio33_20260630_161340.pcapng`
  contained all `250` host raw Ethernet probe frames and `390` FPGA RXMON
  reports. First/last payloads were
  `R120_RXMON L=3 R=000005BA H=00094A26 E0=00000001 E1=00000001` and
  `R120_RXMON L=3 R=00000825 H=000E1431 E0=00000001 E1=00000001`, so
  `delta_R=619`, `delta_H=313867`, `delta_E0=0`, `delta_E1=0`.
- Reproduce the RXMON pcap verdict with:
  `python C:\workspace\verilog\scripts\analyze_r120_rxmon_pcap.py C:\Users\User\AppData\Local\Temp\r120_rxmon_active_probe_vccio33_20260630_161340.pcapng --min-reports 300 --expect-crs-activity --expect-rxd-static`.
  Verified output: `PASS`, backend `scapy`, reports `390`, duration
  `7.780852 s`, `delta R=619 H=313867 E0=0 E1=0`, `L distribution {'0x3': 390}`.
  The inverse check with `--expect-rxd-activity` exits `1` and prints
  `expected RXD0/RXD1 activity`, which is the intended fail evidence for the
  current hardware blocker.
- Use the combined physical-evidence gate when both captures are available:
  `powershell -NoProfile -ExecutionPolicy Bypass -File C:\workspace\verilog\scripts\check_r120_physics_evidence.ps1 -StaticUdpPcap C:\Users\User\AppData\Local\Temp\r120_static_udp_physics_recheck_20260630_154848.pcapng -RxmonPcap C:\Users\User\AppData\Local\Temp\r120_rxmon_active_probe_vccio33_20260630_161340.pcapng -Mode current-blocker`.
  `current-blocker` must pass for the present known-bad hardware state: static
  UDP TX works, `CRS_DV` is active, and `RXD0/RXD1` stay static. After hardware
  rework or a strap/reset fix, rerun the same command with `-Mode hardware-pass`;
  that mode currently fails with `expected RXD0/RXD1 activity` and should pass
  only when `RXD0/T4` and `RXD1/R11` transitions are present in RXMON.

Resolved RX blocker:

- Before the hardware rework, the FPGA saw some `EthCrsDv/P11` activity, but
  saw `EthRXD0/T4` and `EthRXD1/R11` as static high during real
  broadcast/unicast probes. This was below LwIP, `darketh_mmio`, and PSRAM:
  static UDP TX success by itself was not proof that PHY-to-FPGA RX worked.
- After the user soldered all RXD0/RXD1 jumpers on 2026-07-01, volatile RXMON
  evidence resolved this blocker. `R120_STATIC_UDP_RXMON.fs` was programmed to
  SRAM with `User Code: 0x0000A9C9`, `Status Code: 0x00006020`; active capture
  `C:\Users\User\AppData\Local\Temp\r120_rxmon_after_jumpers_20260701_114305.pcapng`
  produced `389` RXMON reports in `7.760784 s`, with
  `delta_R=588`, `delta_H=209479`, `delta_E0=62650`, and `delta_E1=66518`.
  The combined gate
  `check_r120_physics_evidence.ps1 -Mode hardware-pass` passed using that pcap
  and the known-good static UDP TX pcap from 2026-06-30.
- The same post-rework bench check then volatile-programmed
  `R120_LIDAR_EXT_RAM.fs` (`User Code: 0x00007563`,
  `Status Code: 0x00006020`). `Test-NetConnection` showed TCP ports `50100`
  and `50101` open at `192.168.2.240`, and `run_r120_lconf_smoke.ps1` passed
  real `lconf --lidar-smoke`: discovery, UDP full-status, UDP/TCP firmware
  `pegus_1`, TCP command, and TCP MSOP data. The MSOP proof included frames
  `758` bytes long, `180` points, `angle_res=2000`, `dist_bytes=2`,
  `echo=3/2`. Smoke log:
  `C:\Users\User\AppData\Local\Temp\r120_lconf_smoke_after_jumpers_20260701_114447.log`.
- Persistent external-FLASH programming of the same
  `R120_LIDAR_EXT_RAM.fs` was later verified at the FPGA configuration level:
  after a user power-cycle, read-code returned `ID 0x0000081B`,
  `User Code: 0x00007563`, and `Status Code: 0x00006020`. Treat this as
  proof that the FPGA loads the expected image from FLASH, not as proof that
  the LwIP application is healthy after cold boot. The post-power-cycle
  application check on 2026-07-01 failed discovery:
  `C:\Users\User\AppData\Local\Temp\r120_lconf_smoke_after_power_replug_20260701_123505.log`.
  A simultaneous active-probe pcap
  `C:\Users\User\AppData\Local\Temp\r120_after_power_replug_probe_20260701_123527.pcapng`
  saw `100` FPGA heartbeat frames from `02:20:20:20:20:01`,
  `192.168.2.240:50100 -> 192.168.2.255:50100`, payload
  `FPGA_STATIC_UDP_R120_20260629!`, but no FPGA discovery response and no
  diagnostic marker sources `02:20:20:20:20:04`/`:05` for raw
  `EthCrsDv`/`eth_rx_byte_valid`. TCP connects to ports `50100`, `50101`, and
  `50102` timed out. Current open blocker: persistent/cold-boot configuration
  and RMII TX are alive, but the integrated image does not show a working
  receive/application path in this pcap; compare `EthRST`, `EthCrsDv/P11`,
  `EthRXD0/T4`, and `EthRXD1/R11` on the `0x7563` image or load RXMON/RXSCOPE
  as a deliberate diagnostic step before changing LwIP logic.
- A repeat cold-boot check on 2026-07-01 after another user power replug
  reproduced the same split. Read-code returned `ID 0x0000081B`,
  `User Code: 0x00007563`, and `Status Code: 0x00006020`. TCP ports
  `50100`/`50101`/`50102` on `192.168.2.240` timed out, and
  `C:\Users\User\AppData\Local\Temp\r120_lconf_smoke_after_power_replug_active_20260701_125153.log`
  failed discovery, seeing only the real `R120_BM1` at `192.168.2.225`.
  Active pcap
  `C:\Users\User\AppData\Local\Temp\r120_after_power_replug_active_20260701_125153.pcapng`
  contained `90` FPGA heartbeat UDP frames from `02:20:20:20:20:01`,
  `192.168.2.240:50100 -> 192.168.2.255:50100`, payload
  `FPGA_STATIC_UDP_R120_20260629!`, but no FPGA `R120_FAKE` discovery/TCP
  response and no diagnostic marker sources `...:04`/`:05`.
- Immediately volatile-programming the identical
  `C:\workspace\verilog\20k\LDR_20K\impl\pnr\R120_LIDAR_EXT_RAM.fs`
  (`SHA256 F246456614737DBCA7E7996B8D2730CFC259B26AD07145547AB59FD39717A2C9`)
  with `program20K_volatile_fs.bat` returned `User Code: 0x00007563`,
  `Status Code: 0x00006020`, and the same bench passed full
  `lconf --lidar-smoke` in
  `C:\Users\User\AppData\Local\Temp\r120_lconf_smoke_after_volatile_reload_20260701_125333.log`
  including discovery, UDP status/firmware, TCP command, and TCP MSOP frames
  `758 bytes`, `180 points`, `angle_res=2000`, `dist_bytes=2`, `echo=3/2`.
  Treat the present blocker as a cold power-up/reset/init sequencing issue
  around soft-MCU, PHY RX, or PSRAM startup, not as a bad persistent image,
  cable/link failure, or missing RXD jumper.
- The post-rework acceptance audit passed with `-AllowLocalBundleOnly`. For a
  remote-clean handoff, `soft_mcu/dark_risc` commit
  `e02e5511e0cc786ab8d83d965379e76c522dad92` still must be published to the
  configured remote or the superproject gitlink must be moved to an equivalent
  reachable commit.
- `rdch.asc` shows the relevant R120 routing as jumpers/series links, not
  direct pin names: `LAN8742A D9 pin 8 RXD0/MODE0 -> R83 51R -> EthRXD0 ->
  J12 -> FPGA T4`; `D9 pin 7 RXD1/MODE1 -> R85 51R -> EthRXD1 -> J14 ->
  FPGA R11`; `D9 pin 11 CRS_DV/MODE2 -> R81 51R -> EthCrsDv -> J18 -> FPGA
  P11`. `EthRXD0/EthRXD1/EthCrsDv` can also be strapped toward the STM32 via
  `R159/R160/R158 0R`. Hardware rework/population of `J12/J14/J18` and these
  resistors matters.
- First scope checks during raw unicast/broadcast traffic: probe `D9 pin 11`,
  both sides of `R81`, both sides of `J18`, and FPGA `P11` as the known CRS
  control path. Then probe `D9 pin 8`, both sides of `R83`, both sides of
  `J12`, and FPGA `T4`; repeat for `D9 pin 7`, `R85`, `J14`, and FPGA `R11`.
  If the PHY/R83/R85 sides toggle but FPGA `T4/R11` do not, inspect
  `J12/J14` solder and board rework. If PHY `RXD0/RXD1` pins themselves do not
  toggle while `CRS_DV` does, inspect PHY reset/strap/RMII mode or receive
  state.
- Also verify `EthRST/T8` goes low for about 10 ms after programming and then
  high, and that `EthnlntSel/T6` is held high by the board strap while the FPGA
  leaves it high-Z.
- Keep `EthRXD0/T4`, `EthRXD1/R11`, and `EthCrsDv/P11` with `PULL_MODE=NONE`:
  these LAN8742A pins are strap pins `MODE0/1/2`, so FPGA pull-ups can perturb
  PHY mode during reset.
- The standalone RX logic is not the current suspect by itself. ModelSim 10.5b
  command
  `vsim.exe -c -do "do C:/workspace/verilog/src/Ethernet/RMII/eth_rx_check/eth_rx_check_tb.do; quit -f"`
  passed on 2026-06-30 with compile `Errors: 0`, simulation `Errors: 0`, and
  final `ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО`. It covers valid RMII frames, bad CRC
  reject, consecutive frames, non-4-byte-aligned frames, loopback through
  `rmii_tx_w_buf`, and destination-MAC filter classes. If scope proves activity
  at FPGA pins `P11/T4/R11` but the R120 diagnostic marker for raw `EthCrsDv`
  still stays absent, inspect the R120 board wrapper/constraints/diagnostic
  latch wiring before rewriting `eth_rx_check`.
- The R120 board-interface RX path itself was strengthened on 2026-06-30 16:29.
  `R120_lidar_ext_ram_diag_tb` now injects a valid 60-byte Ethernet frame into
  physical wrapper inputs `EthCrsDv/EthRXD0/EthRXD1` through
  `rmii_tx_w_buf #(.WITH_PR_AND_CRC32(1))`, checks that all 60 bytes reach
  `eth_rx_check`, and waits for diagnostic UDP source MACs `...:02`
  (`eth_rx_frame_valid`), `...:04` (raw `EthCrsDv`), and `...:05`
  (`eth_rx_byte_valid`). Verified command:
  `cd C:\workspace\verilog\src\main; vsim.exe -c -do "do R120_lidar_ext_ram_diag_tb.do; quit -f"`.
  Result: compile/runtime `Errors: 0`; proof lines included
  `R120 eth_rx_frame_valid seen at FPGA wrapper`,
  `R120 valid RMII frame reached eth_rx_check: 60 bytes match`,
  `R120 diag marker source MAC 02:20:20:20:20:02 seen`, and
  `R120_lidar_ext_ram_diag_tb PASS`. This means that if scope proves real
  RMII transitions at FPGA `P11/T4/R11`, the current HDL wrapper can accept
  them; this was the active blocker until the 2026-07-01 RXD0/RXD1 jumper
  rework and RXMON hardware-pass evidence above.

## Lconf Integration Notes

The `lconf` Qt app is not the FPGA build project, but it contains FPGA-facing docs and tools:

- `COMPENSATION_TABLES.md` documents runtime FPGA compensation table selectors and source HDL paths.
- `FLASH_BIN_BLOB_RULES.md` documents protected FPGA firmware area handling and BIN blob writes.
- `third_party\comp_export` converts compensation CSV files into `.hex` and `.bin` payloads.

When working on compensation tables, connect changes across:

- HDL defaults in `C:\workspace\verilog\src`
- generated `.hex` or `.bin` files
- lconf upload/flash behavior

## MSOP TCP Stream Debugging

Use these checks before changing HDL when the GUI point cloud looks wrong.

Quick port probe from the shared switch bench:

```powershell
Test-NetConnection -ComputerName 192.168.2.220 -Port 50100
Test-NetConnection -ComputerName 192.168.2.220 -Port 50101
Test-NetConnection -ComputerName 192.168.2.220 -Port 50102
```

`lconf --lidar-stream` is useful for GUI-equivalent parsed batches and telemetry,
but its `batch` JSON lines are emitted from `DataReaderTcp` storage flushes. One
line can contain points from one or more MSOP frames. Use it for a quick
application-level view, not for proving frame boundaries:

```powershell
& 'C:\workspace\lidar\lconf\bin\Release\lconf.exe' --lidar-stream `
  --smoke-host 192.168.2.220 `
  --smoke-local-host 192.168.2.146 `
  --smoke-discovery-target 192.168.2.220 `
  --smoke-skip-discovery `
  --smoke-timeout 5000
```

For protocol-level MSOP TCP frame debugging, use the skill script. It parses
`TcpHeaderV1` directly from the TCP stream, cuts packets by `FF FE ... FF 9B`,
prints header angle range, point count, echo format, and first/last body points,
and can save raw frame packets:

```powershell
python C:\workspace\verilog\.agents\skills\fpga-dev\scripts\msop_tcp_sniff.py `
  --host 192.168.2.220 `
  --local-host 192.168.2.146 `
  --frames 20 `
  --timeout 5 `
  --jsonl $env:TEMP\msop_192_168_2_220.jsonl `
  --raw-dir $env:TEMP\msop_192_168_2_220_frames
```

Interpretation notes:

- `first_point_angle_mdeg` and `angle_res_mdeg` are in millidegrees.
- `last_point_angle_mdeg = first_point_angle + (point_count - 1) * angle_res`.
- For `echo_num=2`, the script reports primary distance and second echo/width
  fields separately. The second field meaning depends on `echo_mode`.
- A mismatch between body point order and `first_point_angle/angle_res` can make
  the GUI cloud look mirrored, bent, or split even when packet markers and point
  counts are valid.
- If the direct MSOP stream shows a physical reference in the expected low-angle
  sector but the GUI shows it on the opposite side, inspect `lconf` rendering
  before changing FPGA. In `C:\workspace\lidar\lconf`, the parser assigns
  `angle_deg = first_point_angle + index * angle_res`; Cartesian side placement
  is controlled later by `MainWindow::newData` in `mainwindow_data_flow.cpp`.
  Check saved `HKCU:\Software\R-Lidar\lconf` values such as `MirrorX`,
  `MirrorY`, `StartAngle`, `GraphType`, and `MirrorsMode`. The default
  non-mirrored Cartesian convention should match session playback:
  `sfx = mirror_x ? -1.0 : 1.0`.

To reproduce the GUI-side left/right check from raw frames saved by
`msop_tcp_sniff.py`, render the captured packets through the old and fixed
`lconf` Cartesian sign conventions:

```powershell
python C:\workspace\verilog\.agents\skills\fpga-dev\scripts\msop_lconf_xy_check.py `
  --raw-dir $env:TEMP\msop_192_168_15_15_direct_frames `
  --frames 4 `
  --png $env:TEMP\lconf_msop_xy_old_vs_fixed.png
```

With `MirrorX=false`, the low-angle reference centroid should move from
negative X under the old formula to positive X under the fixed formula.

## Live FPGA FLASH Checks

Before any live FLASH write on a production lidar, do read-only checks first.
For the local `0x45` fixed FLASH command, `MemoryPresense::OK` is decimal `103`
and `MemoryPresense::ERROR` is decimal `105`. Do not treat `status=103` as a
failed erase/write response; it means the MCU-side operation reported OK.

Read-only memory presence check:

```powershell
python C:\workspace\verilog\20k\flash_spi_live_program.py `
  --host 192.168.2.220 `
  --port 50101 `
  --local-host 192.168.2.146 `
  --timeout 30 `
  --check-memory
```

Read-only full-image verify against the current local Gowin `.bin`, without
erase or write:

```powershell
python C:\workspace\verilog\20k\flash_spi_live_program.py `
  --host 192.168.2.220 `
  --port 50101 `
  --local-host 192.168.2.146 `
  --file C:\workspace\verilog\20k\LDR_20K\impl\pnr\LDR_20K.bin `
  --timeout 30 `
  --chunk 256 `
  --skip-erase `
  --skip-write `
  --readback $env:TEMP\ldr20k_flash_verify_readback.bin
```

If an earlier live write stopped after an erase, verify the affected sector
before doing anything else. For sector 0, a dump whose first `4096` bytes are all
`0xFF` means the sector is erased. If the rest of the dump matches the intended
image from offset `0x001000`, recover narrowly by writing only the first sector
from the matching `.bin` with `--skip-erase`, then run the full read-only verify.

## R120 UART Debug Channel (verified 2026-07-02)

- The R120 debug connector pads route to FPGA balls `D3` and `C1` (confirmed
  electrically with a fabric UART banner generator streamed on both pads and a
  USB-TTL FT232R at the user side, plus a sticky low-detector probe).
- Working pinout in `src/main/R120_lidar_ext_ram.cst`: `UART_TX -> D3`,
  `UART_RX -> C1`, LVCMOS33; USB-TTL: adapter RX -> D3 contact, adapter TX ->
  C1 contact, common GND required.
- The USB-TTL adapter on this bench is FT232R serial `A5069RR4` = `COM4`
  (115200 8N1). `COM3` is channel B of the Gowin FT2CH programmer cable and is
  NOT wired to the board.
- darkuart at `BOARD_CK=50 MHz` gives a clean 115200 stream; the boot banner
  is `lidarsim start`.
- CAUTION: with a live UART every `printf` busy-waits ~87 us/char. Unthrottled
  prints on per-frame events (e.g. RX overflow flags on a busy LAN) form a
  print storm that slows the main loop enough to distort behaviour -
  rate-limit such prints (see `lidarsim rx flags` 5 s limiter in lwipdemo).
- Fabric probes that proved the path (reusable patterns): UART banner
  generator (~30 lines SV, clk/434 divider) and sticky low-seen detectors
  reported via IPORT/beacon.

## R120 wedge investigation status (2026-07-02)

- Original wedge root causes found and fixed: (1) lwIP MEM heap too small
  (1024) for 758-byte tcp_write(COPY) MSOP frames - raised to 2560; (2) a heap
  pbuf double-free caught by MEM_OVERFLOW_CHECK at mem.c "double free" during
  real lconf exchanges (etharp PENDING hand-off vicinity, `ARP_QUEUEING=0`).
- Mitigations in lwipdemo: periodic `etharp_request` host refresh (first after
  2 s of uptime - earlier requests desync the scripted ModelSim TB);
  `net_self_heal()` full lwIP re-init when `pbuf_alloc(PBUF_POOL)` fails 32x
  in a row (proven on hardware: recovers a wedge within one soak cycle).
- Fabric watchdog in the R120 wrapper: firmware toggles `OPORT[0]` each main
  loop; the wrapper pulses darksocv `XRES` after 5 s of no toggling. MUST be
  arm-on-first-toggle: a watchdog армed from reset caused a permanent
  reset-loop (fabric alive, CPU never served).
- Best verified run: 12/12 soak cycles STABLE (lconf smoke + 200-frame MSOP
  through PSRAM), self-heal observed recovering mid-soak. A rare residual
  freeze under combined load (MSOP client + ambient large frames) remains
  under investigation; isolated large-frame no-pbuf drains are exonerated
  (bracket prints prove drain completes).

## R120 PSRAM CDC bridge / psram100 profile (verified 2026-07-03)

- `darkpsram_ctrl_cdc.sv` (dark_risc rtl) moves `EF_PSRAM_CTRL` into its own
  clock domain: toggle req/rsp handshake, quasi-static latched command fields
  (darkddr3_ui_cdc pattern). `done` must be masked with the incoming start
  (`assign done = done_r & ~start`) or the darkpsram_mmio FSM samples the
  stale done level on the same edge it issues a new start.
- `darkpsram_mmio` has `USE_CDC` parameter (generate cdc/direct; direct path
  is verbatim the original controller instance). `darksocv` forwards
  `PSRAM_USE_CDC` + `PSRAM_CLK`/`PSRAM_RST_N` ports (under DARKPSRAM_MMIO).
- Gowin profile: `R120_LIDAR_EXT_RAM_PROFILE=psram100` builds thin top
  `R120_lidar_ext_ram_psram100_brd_ifm` (CDC=1, PLL `o_pll_10_100`, 10->100
  MHz: FBDIV_SEL=9, ODIV_SEL=8, VCO 800 MHz). PnR verified: Setup/Hold
  violated = 0, clk_psram actual Fmax 271 MHz (headroom up to 160 MHz domain).
- SDC gotcha: nets inside the thin-top hierarchy need the instance prefix -
  `get_nets {core/clk_psram}`; bare `clk_psram` fails with TA2003/TA2004
  (while bare `clk_50` happens to resolve at top level). Separate
  `R120_lidar_ext_ram_psram100.sdc` adds the 100 MHz clock and
  `set_clock_groups -asynchronous` for clk_50/clk_psram.
- SoC-level sim of the full lidar exchange incl. MSOP through PSRAM:
  firmware must be built with `LIDARSIM_PSRAM_MMIO=1
  LIDARSIM_PSRAM_TCP_SIM_SELFTEST=1` (else main() exits after the UDP flags
  and the TB TCP phase never runs); TB defines
  `+define+DARKETH_LWIP_FRAME +define+DARKETH_LWIP_TCP_DATA_FRAME
  +define+DARKPSRAM_MMIO [+define+DARKPSRAM_CDC]`. Pass criterion:
  `darketh sim tcp data msop payload ok` + `lidarsim ok`.
- Stack budget recurrence: selftest firmware with MEM_SIZE 2560 leaves <300 B
  of stack (false-failure zone, need >=600 B) - lwipopts.h trims MEM_SIZE to
  2048 for the sim selftest builds only. Always re-check COMMON/bss end vs
  0x10000 in `src/darksocv.map` after changing build flags.
- Restore `src/darksocv.mem` after sim experiments:
  `git -C soft_mcu/dark_risc restore -- src/darksocv.mem`.

## R120M.BM2BF1X1 Board Layer (verified 2026-07-03)

New board revision R120M.BM2BF1X1; board layer files (branch
`codex/r120m-bm2bf1x1-brd-ifm`):

- `src/main/R120M_BM2BF1X1_brd_ifm.sv` + `src/main/R120M_BM2BF1X1.cst`.
- Pin map source: DipTrace ASCII export
  `\192.168.2.50\e\YandexDisk\#Projects\ToF Lidar\Схемы\РЖД\R120\R120_M\R120M.BM2BF1X1\Schematic.asc`
  (FPGA refdes `D7`). Extract pin->net tables with
  `python docs/skills/fpga-dev/scripts/parse_diptrace_asc.py <asc> D7,D8,...`
  (file is cp1251; each `(Pin ...)` carries `StringNumber` = ball and
  `NetNumber`; net names come from `(Net "...") (Number N)` blocks).
- Key board facts vs R120_M-1.1.0:
  - FPGA clock: 10 MHz on `H11` from a TLV3502-based oscillator shared with
    the STM32H723 HSE, through solder jumper `J4`; `o_pll_10_50` still applies.
  - Ethernet is a W5500 (SPI), no RMII PHY. W5500 SPI routes to FPGA via
    J10..J15 or to MCU SPI1 via J22..J27. `~RST` is pulled to GND by R58 —
    the FPGA must drive `WIZNET_RST_N` high to enable the chip.
  - PSRAM IS66WVS1M8 is now factory-routed: SCLK=C1, CE_N=D3, SIO0..3 =
    C2/D1/D2/E3.
  - LTDC-X3 (ScioSense lidar TDC, D19) on QSPI: SCK=E14, SS_N=F14,
    D0..D3=E16/E15/D16/D15, INTERRUPT=F15, REINIT=D14, STOPMASK=C16,
    FIRE (STARTP) from G14. Registers, opcodes, startup sequence, and the
    eval-proven register config are in `ltdc-x3.md` next to this file.
  - Two TDC7201 (D23/D24, channel groups 12/34); FPGA `TDC7201_FIRE`/L14
    drives START1/2 of both chips through R140 (net `7201_FIRE_AR`).
  - MCU command SPI: STM32 SPI2 is Full_Duplex_Master (per `.ioc`), FPGA is
    slave: SCK=P13, MOSI=T14, MISO=T15, HSS_N=N14 — mapped to `if_SPI3`
    (CMD slot) of `interface_MCU_FPGA`.
  - External FLASH pins unchanged: P10/R10/M9/L10 (MSPI dual-purpose).
  - Debug UART header X1: FPGA_TX=M11, FPGA_RX=T13.
  - All IO banks are +3V3_F -> LVCMOS33 everywhere.
- Fast ModelSim compile check needs the src include root and separate
  compilation units, otherwise `Eth_common.svh` fails to open
  `machines/machine_header.sv` and `$unit` types collide:
  `vlog -sv +incdir+.. <o_pll_10_50.v>; vlog -sv +incdir+.. main.sv;`
  `vlog -sv +incdir+.. R120M_BM2BF1X1_brd_ifm.sv` (run from `src/main`,
  fresh work lib). Verified: Errors: 0.
- Gowin PnR check (throwaway tcl, device GW2A-LV18PG256C8/I7, options
  `use_mspi/ready/done/reconfign_as_gpio`): bitstream generated,
  Setup/Hold violated endpoints = 0, PLL clk Fmax 73.6 MHz @ 50 MHz,
  all 101 ports Constraint=Y.

## R120M: повтор функционала старого лидара на 2x TDC7201 (сим PASS 2026-07-06)

- Milestone: боевой `main` (TDC_4_1) работает через прослойку
  `R120M_BM2BF1X1_brd_ifm` с двумя TDC7201; LTDC-X3 отложена (чип не введён).
  ТБ: `src/main/R120M_BM2BF1X1_tdc_tb.sv` + `.do` (модели `class_TDC7201`,
  энкодер стоит -> автоподжиг ~20 кГц, LTDC_INTERRUPT неактивен, SPI2 молчит).
  PASS-факты: 2 валидных MSOP-кадра (маркеры FF FE/FF 9B, 500/246 точек,
  angle_res=360, echo=3/2), 1258 поджигов, дистанция первой точки
  3766 мм = 0.14989 x 25125 пс — аналитически сходится с TIME1 модели.
- **Маппинг чипов**: в актуальном `tdc_processing` рабочая пара интерфейсов —
  56 (TDC переднего фронта, дистанция) и 34 (TDC среза, ширина);
  `if_TDC7201_12` в TDC_4_1 ЗАГЛУШЕН (en=0, cs=11). На R120M чип D23
  (пины TDC_*12/CS1/CS2) -> if_56, D24 (пины *34/CS3/CS4) -> if_34.
  Какой из D23/D24 ловит передний фронт — сверить по цепям компараторов.
- **Sim-vs-synth ловушка (боевой RTL)**: в `TDC7201_v2` порт `set_config_stb`
  SPI-контроллера был не подключён, а он входит в busy-выражение →
  в симуляции busy=X и `TDC7201_logic` вечно ждёт `!busy` (первый симптом:
  поджиги идут, стартовый конфиг TDC прошёл, а prep/чтений нет). На железе
  работало — синтезатор вяжет висящий вход в 0. Исправлено `.set_config_stb(1'b0)`.
  Урок: при переносе живого RTL в симуляцию проверять неподключённые входы,
  участвующие в управляющих выражениях.
- **Модель TDC7200 не умела auto-increment**: контроллер читает CAL1+CAL2
  одной транзакцией 6 байт (бит7 команды), модель отдавала только 3 байта —
  хвост повторял последний байт (симптом: cal2=0x9E9E9E, TOF в ~120 раз
  меньше). Исправлено в `class_TDC7200`: `read_reg(regAddr + out_cnt/3)`
  при cont_read_flag. Также параметризован TIME1 (конструктор), чтобы фронт
  и срез давали разные TOF — при равных тракт честно даёт дистанцию ~0.
- Выход MSOP: `MSOP_TCP_SPI_sender` (внутри TDC_4_1) — ПЛИС SPI-мастер,
  1 CS-транзакция = 1 кадр, из `if_mcu_fpga.if_SPI2`; на R120M выведен на
  пины `MSOP_SPI_SCK/MOSI/CS_N` = R6/T5/R5 (бывшие MCU_FPGA_6/7/8).
  Соответствие SPI-slave ножкам STM32 — открытый вопрос.
- PnR прослойки после правок: Setup/Hold=0, Fmax 62.3 МГц, 101 порт constrained.
- Формула TOF тракта: TOF[пс] = TIME1 x 900000/(CAL2-CAL1) при
  CALIBRATION_PERIODS=10, TDC_DIGIT_FREQ=10 МГц; DST[мм] ≈ 0.149896 x TOF;
  LSB ≈ 10.47 пс при модельных CAL 2206/88175.

## R120M: заход в железо №1 — TDC-тракт запущен (verified 2026-07-06)

- Milestone на плате: поджиг ~21 кГц, оба TDC7201 отдают INT, вычитка идёт,
  ~86 MSOP-кадров/с на выходном SPI (R6/T5/R5). Доказательство — счётчики
  UART-репортера на COM4, без логanalyzer'а.
- **Корень отказа «TDC молчит»: подтяжки INTB.** INTB у TDC7201 — open-drain,
  MISO при CS=1 — Hi-Z. В новом cst стояло явное `PULL_MODE=NONE` → INTB
  повис в 0: i/j замерли на 1, уровни INT1/INT3=0, при живом SPI (c рос
  с частотой поджига). Старая плата (R120_M_1_1_0.cst) молча жила на
  **дефолте Gowin PULL_MODE=UP** — там строки закомментированы. Урок:
  для open-drain входов подтяжку писать ЯВНО (`PULL_MODE=UP`), а при
  портировании cst не заменять «пусто» на `NONE` — это разные вещи.
- **Диагностика через UART-репортер-«мультиметр»** (`r120m_dbg_uart_reporter`):
  строка `R120M f=.. i=.. m=.. c=.. j=.. s=..` раз в 0.5 с — счётчики
  поджигов/INT1/MSOP/CS1/INT3 + байт мгновенных уровней
  {EN12,INT1,INT3,MISO1,MISO3,fire,CS1,SCLK12}. Паттерны:
  c растёт, i стоит, уровень INT=0 → нет подтяжки/чип не отвечает;
  c стоит малым → SPI-контроллер застрял; всё растёт → тракт жив.
- **Стороны UART на гребёнке X14**: подписи пользователя «E1 - tx uart,
  E2 - rx uart» были со стороны USB-TTL адаптера → ПЛИС слушает E1,
  передаёт на E2. Та же ловушка, что D3/C1 на старом стенде: имена
  RX/TX всегда уточнять «чей TX».
- **Артефакт драйвера FTDI (COM4, FT232R)**: после перепрошивки порт может
  отдавать реплей устаревшего куска буфера на «невозможной» скорости
  (~73 кБ/с при 115200; одна и та же строка тысячами копий + обрезки).
  Лечится перециклом: открыть порт на другом бауде (230400), прочитать,
  закрыть, снова открыть на 115200. Настоящие строки узнаются по
  инкременту счётчиков. Не путать с отказом ПЛИС.
- Вачдог INTB (`TDC_INTB_monitor`, WD 4 с) в боевом RTL перезапускает цикл
  измерения при пропаже INT — поэтому при мёртвом INTB поджиги продолжаются,
  а конвейер тихо стоит: без счётчиков это выглядит как «всё работает».

## R120M: полная проверка корректности данных на железе (verified 2026-07-06)

- **DSView (сторона MOSI фронт-чипа D23)** подтвердил командный тракт SPI:
  ПЛИС шлёт `40 81` = write CONFIG1(0x00)=0x81 (FORCE_CAL+START_MEAS),
  затем `10 00 00 00` = read TIME1(0x10)+3 dummy, затем `9B 00 00 00 00 00 00`
  = auto-increment (бит7) read CAL1(0x1B)+CAL2, 6 dummy. Ровно как в симуляции.
  data-байты на MOSI = 0x00 (ПЛИС тактирует нули, читая ответ); настоящие
  TIME1/CAL приходят по MISO (H1) — их этот декод не показывает.
- **Снайфер выходного MSOP-SPI в прослойке** (без правки боевого RTL): тем же
  способом, что примет STM32, реконструирует байты кадра и достаёт дистанцию
  первой точки (offset 36..37 LE) + интенсивность (байт 38) в UART-репортёр.
  Сверен в главном ТБ бит-в-бит с независимым декодером (3766 мм в обоих).
- **Результат на стенде**: дистанция стабильна 12008..12033 мм (±12 мм),
  80 нс TOF = 12020/0.149896. Стабильность и точное совпадение с боевой
  константой 0.149896 мм/пс доказывают исправность тракта TDC → расчёт TOF →
  MSOP-упаковка → SPI-провод. Абсолютные 12 м на стенде БЕЗ мишени и с
  выключенным лазером (LSR_CHRG_CTRL=0) — электрический самозапуск STOP на
  перебросе START/FIRE, а не оптическое эхо; ширина импульса ≈0 (срез в тот же
  миг). Реальный оптический дальномер проверять с зарядом лазера + мишенью.
- **Оба чипа живы**: MSOP-кадры формируются, а tdc_data_ready требует
  готовности И D23 (фронт), И D24 (срез) — значит оба TDC завершают измерение.
- **Ловушка PnR: рулетка разводки на плотном дизайне.** База (регистры 76%)
  разводится стабильно, но маргинальная добавка снайфера дала PR0004
  «unrouted nets», причём НЕДЕТЕРМИНИРОВАННО (114 -> 329 при *меньшей* логике).
  Признак — не жёсткий потолок ёмкости, а перегрузка роутера. Лечение:
  освободить логику (убрать отладочные счётчики решённых проблем) + ужать
  добавку (счётчик байт 6 бит с насыщением, запись прямо в финальные регистры
  вместо промежуточных + защёлки). Не полагаться на перезапуск PnR.
- **«Cable lost» программатора** (FT2232 канал A) — снять зависший
  `programmer_cli.exe`, проверить `Get-PnpDevice` (канал A должен быть OK),
  повторить. Обычно транзиент после серии прошивок.

## W5500 на ПЛИС: SoC-сим PASS, standalone-топ bring-up заблокирован (2026-07-06)

- **Архитектурное решение**: релизный тракт — ПЛИС SPI-МАСТЕР шлёт MSOP в
  STM32 (fabric TDC7201 → MSOP → SPI, сборка R120M_BM2BF1X1, HWOK), а
  W5500/Ethernet держит STM32. W5500-на-ПЛИС (soft-MCU DarkRISCV + W5500
  bit-bang) — bench/fallback, **отложен** на этом блокере.
- **SoC-сим W5500 — PASS** (чистый submodule-коммит 656f2ef, прошивка
  w5500demo): version=04, netcfg 192.168.2.240, listen 50100, established,
  2 MSOP-кадра x758 байт, w5500demo ok. Транспорт логически исправен.
- **Блокер на железе — ядро darkriscv в НОВОМ standalone-топе
  (R120M_w5500_brd_ifm) не стартует.** Доказанная бисекция:
  - клок 50 МГц и конфиг ПЛИС ЖИВЫ — фабричный heartbeat даёт на DSLogic
    чистый меандр ровно 24.41 кГц (2048/50МГц = 40.96 мкс);
  - ROM ЗАГРУЖЕН — в нетлисте `defparam MEM_*_s.INIT_RAM_XX=256'h...` с
    реальным кодом (НЕ нули; формат — `256'h`, не `INIT_RAM="..."`);
  - darkpll для Gowin — passthrough (`assign CLK=XCLK`), двойного PLL нет;
  - пробованы XRES=0 (внутр. IRES, как в m20k_dev_uart_rmii_debug) и явный
    reset-hold — оба не помогли;
  - darkuart молчит на всех бодах; сеть 192.168.2.240 недоступна (нет ARP).
  - Итог: CPU имеет клок+сброс+ROM, но не исполняет. Причина не найдена
    (standalone darksocv-топ в этом worktree на железе ранее не гонялся;
    подозрение — выборка инструкций/интеграция BRAM или недостающий дефайн).
  - Диагностика для след. захода: cpu_ran = sticky «OPORT хоть раз != 0»
    (LED2 + DSLogic-F2, ровный уровень), + ФАБРИЧНЫЙ UART-репортёр на E2
    (UART_tx, работает, читается на COM4) сообщает cpu_ran/oport_seen —
    self-service, без походов к стенду. Битстрим собран, НЕ прошит.
- **Ловушка: светодиоды модуля W5500 горят ВСЕГДА** (power/PHY-LED модуля),
  даже без прошивки — НЕ признак, что CPU поднял OPORT[9]. Живость CPU
  проверять только по OPORT/fabric-защёлкам, не по LED модуля.
- **DARKETH_MMIO**: если топ его определяет — добавить `darketh_mmio.sv` в
  список файлов сборки (иначе EX3937 unknown module 'darketh_mmio').
- **FT2232 JTAG «Cable lost»/статус Unknown** после серии прошивок —
  снять зависший programmer_cli не всегда хватает; глубокий залип лечится
  только физическим перетыком USB (disable/enable требует админа).

## Публикация тестовых прошивок (сетевая шара, verified 2026-07-09)

Готовые тестовые битстримы для лидара складываются на сетевую SMB-шару (не в
git — `.fs`/`.bin` это generated artifacts):

```
\\192.168.2.50\e\YandexDisk\#Projects\ToF Lidar\!Firmware\FPGA\Тестовые прошивки
```

- **`.fs`/`.bin` НЕ коммитить в git** — только на эту шару.
- **Выкладывать на шару только по явному запросу пользователя** (как прошивка
  железа — не по своей инициативе).

- Доступна напрямую из PowerShell по UNC-пути (`Test-Path -LiteralPath`,
  `Copy-Item -LiteralPath`; путь с пробелами/`#`/`!`/кириллицей — только
  `-LiteralPath`). Это YandexDisk-папка на хосте 192.168.2.50.
- **Конвенция имён** (по существующим файлам в папке):
  `<TOP>_<YYYYMMDD>_<HHMM>_<git8>_<описание>_<STATUS>.fs`
  - `<TOP>` — имя проекта/битстрима (`R120M_LTDC_MSOP`, `LDR_20K`, …);
  - дата/время — `LastWriteTime` файла `.fs` (напр. `20260709_1137`);
  - `<git8>` — короткий хэш коммита сборки; если рабочее дерево грязное,
    добавляй суть незакоммиченного в `<описание>`;
  - `<STATUS>` — `HWOK` (проверено на железе и работает), `BUILDOK`
    (только собралось), `HWRUN` (крутится на железе, фича ещё не подтверждена);
  - полезно вложить `UC0x….` (User Code) в имя — сверять по fingerprint,
    какой битстрим реально прошит (см. gowin-usercode-fingerprint).
- Рядом можно класть одноимённый `.rpt.txt`/`.bin`, как уже сделано в папке.

## Грабли стенда LTDC/Gowin (проверено 2026-07-09)

Повторяющиеся ловушки — чтобы не жечь токены заново:

- **CWD gw_sh дрейфует вглубь → вложенные `impl/pnr/impl/pnr/...`.** Если запускать
  `& gw_sh.exe build.tcl` подряд, вывод каждый раз оказывается на уровень глубже
  (gw_sh не восстанавливает CWD после `run all`, а PowerShell-сессия его хранит).
  **Симптом:** UserCode НЕ меняется между сборками при реальных правках — значит
  читаешь устаревший `.fs`. **Фикс:** перед каждой сборкой `Set-Location
  C:\workspace\verilog`; свежий `.fs` искать рекурсивно по всему дереву
  (`Get-ChildItem -Recurse -Filter R120M_LTDC_MSOP.fs | Sort LastWriteTime`) и
  сверять UserCode/время, а не по фиксированному `impl/pnr`.
- **SPI-транзиент LTDC после каждой прошивки.** После заливки (SRAM/FLASH) конфиг
  чипа иногда не проходит: `cfg_error`→`LS_ERROR`, либо FSM залипает `dev=0,busy=1,
  f=0`. FSM выхода из `LS_ERROR` не имеет. **Фикс:** просто перешить ещё раз (сброс
  FPGA перезапускает power_up+config). Диагностировать по полю `s=`(line_status).
- **COM-порт репортёра переномеровывается после прошивки.** Общий FT2232
  (`VID_0403 PID_6010`) переэнумерируется, COM репортёра (был COM4) может пропасть
  или сменить номер. Канал B FT2232 (UART программатора) — НЕ репортёр (молчит).
  Репортёр — отдельный USB-UART донгл на `FPGA_TX`(M11/X1) или `DBG_E2`(E2/X14).
  Пересканировать порты и опознать по устройству.
- **Потолок фабрики GW2A-18 ~ниже 250 МГц.** Обычная логика не влезает в 250 МГц
  надёжно. Тяжёлую арифметику (сумматоры/mux) держать в медленном домене, в
  быстрый передавать уже готовые СТАБИЛЬНЫЕ значения (там только счётчик+сравнения).
  Даже так захват квазистатического вектора через CDC стоит ~0.5нс роутинга.
  **200 МГц (5 нс/такт) — безопасная цель фабрики** (0 нарушений, запас +1нс).
  Худший путь смотреть в `impl/pnr/.../R120M_LTDC_MSOP.timing_paths` (блоки `SETUP`,
  первая строка после — slack; отрицательный = нарушение).
- **PowerShell sandbox блокирует `& cmd.exe /c "..."` внутри условий/функций**
  (ошибка вида «Remove-Item on system path '/c' is blocked»). Запускать `.bat`
  прошивки отдельной верхнеуровневой командой, не в `if/function`.
- **Gowin sim-примитивы** (OSER/rPLL/CLKDIV) лежат в `bin/IDE/simlib/gw2a/`. Но
  проще для сима не тянуть их, а **заглушить PLL в ТБ** поведенчески (генерить
  нужную частоту `always #<半period> c=~c`), синтез подставит реальный примитив.
- **pdftotext** — в `/mingw64/bin` (Git-for-Windows), НЕ в msys64; `-layout` для
  таблиц даташита.
- **Мульти-хит на ОДИН канал LTDC на этом стенде не набирается** (ловится 1 хит/
  канал и на STOP2, и на ch1 в combine). 2 эха берём как 2 канала × 1 хит
  (`CHANNEL_COMBINE`); 3 эха (2 хита на ch1) упираются в тот же аналоговый лимит
  входа. Детали — заметка Obsidian [[LTDC-X3 режимы STOP]].

## Заливка FPGA в R120M через lconf CLI (проверено 23.07.2026)

Заливка на боевой лидар R120M (МК STM32 пишет FPGA-флеш) идёт через бутлоадер-порт
`50102`. Прямой вызов БЕЗ `--reset-before-flash` на 192.168.2.206 воспроизводимо
падал: после шага «Send boot» блок закрывает TCP, переподключение проходит, второй
вход в загрузчик снова обрывается → `Не дождались ответа от блока (New step timeout)`,
прогресс 0%, флеш не тронут.

Рабочий вариант — послать лидару UDP `LIDAR_ACTION RESET` перед заливкой; при этом
lconf сам отключает шаг JmpBoot (`Runtime profile: JmpBoot step disabled because
--reset-before-flash is active`):

```powershell
& 'C:\workspace\lidar\lconf\bin\Release\lconf.exe' --cli --file <образ.bin> `
  --channel tcp --host 192.168.2.206 --port 50102 `
  --reset-before-flash --reset-mac 00:80:E1:07:00:11 `
  --reset-target 192.168.2.206 --reset-local-host 192.168.2.145 `
  --reset-delay 4000 --reconnect-after-boot `
  --erase-timeout 300000 --reply-timeout 30000
```

С lconf `54b256d` (ветка dev, 23.07.2026) ключи больше не нужны — сброс включён
ПО УМОЛЧАНИЮ для каналов tcp/udp, MAC запрашивается у лидара UDP-обнаружением
по `--host`, цель сброса = сам лидар, пауза после сброса 4000 мс. Достаточно:

```powershell
& 'C:\workspace\lidar\lconfin\Release\lconf.exe' --cli --file <образ.bin> `
  --channel tcp --host 192.168.2.206 --port 50102
```

Вернуть прежнее поведение (шаги JmpBoot профиля) — ключ `--no-reset-before-flash`.
Пауза 1500 мс (старый дефолт) не работала: блок не успевал поднять сеть,
заливка падала на `Ошибка TCP connect: timeout`.

- MAC можно задать и явно (`--reset-mac`), например из ARP:
  `arp -d <ip>; ping -n 2 <ip>; arp -a <ip>`.
- Признак успеха: `Send end` и `OK: Данные загружены.`, 886 кБ при `.bin` 907418 Б
  (lconf сам добивает образ до 907776 Б, blockSize=256, 3546 блоков).
- Лидар автоматически перезагружается после заливки — это норма. Через ~10 с снова
  отвечают порты 50100/50101/50102.
- ПО собирается из ветки `dev` репозитория `ak-tech-electronics/TOF_lidar_GUI`
  (`MSBuild lconf.vcxproj /p:Configuration=Release /p:Platform=x64`), exe —
  `C:\workspace\lidar\lconf\bin\Release\lconf.exe`.
