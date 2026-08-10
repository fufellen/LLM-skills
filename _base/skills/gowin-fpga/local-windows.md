# Local Windows Gowin Setup

## Main Paths

- Gowin CLI: `C:\workspace\verilog\bin\IDE\bin\gw_sh.exe`
- Gowin multipurpose pin config: `C:\workspace\verilog\bin\IDE\data\config\multipurposeconfig.xml`
- Gowin Programmer CLI: `C:\workspace\verilog\bin\Programmer\bin\programmer_cli.exe`
- Generic 20K volatile SRAM wrapper: `C:\workspace\verilog\20k\program20K_volatile_fs.bat`
- Generic 20K UART capture helper: `C:\workspace\verilog\20k\capture_uart.ps1`
- Main 20K project: `C:\workspace\verilog\20k\LDR_20K`
- Main 20K build wrapper: `C:\workspace\verilog\20k\LDR_20K\build_gowin.cmd`
- Main 20K build Tcl: `C:\workspace\verilog\20k\LDR_20K\build_gowin.tcl`
- Main 20K output directory: `C:\workspace\verilog\20k\LDR_20K\impl\pnr`

Observed on 2026-06-23: `gw_sh.exe` and `programmer_cli.exe` exist at the
paths above in the current workspace, but `git ls-files -- bin/IDE/bin/gw_sh.exe
bin/Programmer/bin/programmer_cli.exe` returns no tracked files. A clean clone on
another PC will not receive these binaries from Git. Either install/copy Gowin
into the expected workspace paths, or make the project wrappers and
`scripts\check_build_env.ps1` accept explicit environment variables such as
`GOWIN_GWSH` and `GOWIN_PROGRAMMER_CLI`. Do not commit machine-specific absolute
paths into tracked project files.

## Offline Bundle Path And MSYS2 Temp

Verified on 2026-07-15 while building the portable 20K handoff bundle:

- Keep the extracted bundle at the short root `C:\F20K`. With the same files
  under `C:\workspace\FPGA_BUILD_BUNDLE_20260715\project\verilog`, ModelSim
  10.5b and GowinSynthesis failed to open deeply nested relative includes.
  ModelSim reported `Cannot find include file`; GowinSynthesis reported
  `ERROR (EX1985)`. The same ModelSim test and Gowin builds passed from
  `C:\F20K`.
- A portable MSYS2 copy may exclude the contents of user/cache/log/temp
  directories, but it must still contain an empty `msys64\tmp` directory.
  Without it, bundled bash repeatedly reports `could not find /tmp` and the
  LDR_20K Gowin wrapper can return `-1` during bitstream generation. Recreating
  the empty directory removed the warnings and the full DarkRISCV/LwIP +
  Gowin build passed.

## Local Device Defaults

- Tang Primer 20K / LDR_20K device: `GW2A-18C`
- Package/orderable part: `GW2A-LV18PG256C8/I7`
- Common local Verilog standard option: `set_option -verilog_std sysv2017`
- Common local synthesis tool option: `set_option -synthesis_tool gowinsynthesis`
- Verified 2026-07-29: local GowinSynthesis in `sysv2017` mode accepts a
  byte-sliced streaming concatenation from an unpacked array, for example
  `assign packed = {<<8{bytes}}` for `logic[7:0] bytes[0:N-1]`. The
  `R120M_BM2BF1X1` PnR result was bit-identical to the prior indexed-generate
  implementation. Still prove element order in simulation before relying on
  the operator.

## LDR_20K Build Command

Run from `C:\workspace\verilog\20k\LDR_20K`:

```powershell
& 'C:\workspace\verilog\bin\IDE\bin\gw_sh.exe' build_gowin.tcl
```

Or use the tracked wrapper:

```powershell
& 'C:\workspace\verilog\20k\LDR_20K\build_gowin.cmd'
```

The current local LDR_20K script already uses:

```tcl
set_option -use_mspi_as_gpio 1
set_option -use_ready_as_gpio 1
set_option -use_done_as_gpio 1
```

Add `set_option -use_sspi_as_gpio 1` when the design uses SSPI-package pins as regular IO.

## Programming Boundary

Do not run `programmer_cli.exe` unless the user explicitly asks to program hardware. For local 20K hardware programming rules, also read the `fpga-dev` skill references.

For one-off Tang Primer 20K `.fs` hardware checks, use the tracked volatile SRAM wrapper instead of a raw `programmer_cli.exe` command:

```powershell
& 'C:\workspace\verilog\20k\program20K_volatile_fs.bat' 'C:\path\to\firmware.fs'
```

The wrapper fixes `-d GW2A-18C -r 2`; it does not write external Flash.

## FTDI Cable Diagnostics

Before programming, require the active FTDI pair to be healthy:

- `USB Serial Converter A`: `OK`
- `USB Serial Converter B`: `OK`

If channel B is `Error`, do not retry SRAM/FLASH programming yet. Sequential `programmer_cli --scan-cables` may return no cable, and `programmer_cli -d GW2A-18C -r 0` may report `Unknown Cable` or `Cable open failed`.

Observed on 2026-06-22: `pnputil /restart-device "USB\VID_0403&PID_6010\FACTORYAIOT_PRO"` failed with `Access is denied` in the Codex shell. Use a physical USB/JTAG replug or an administrator-level device restart, then recheck both FTDI channels before programming.

## Validate the loaded image by User Code fingerprint

Do not trust the programmer's `Program and Verify ... successfully` line by itself. On a flaky FTDI link the CLI can print success (or a truncated/anomalous log — e.g. two `Compatible cable found` and **no** `User Code` line) while the FPGA keeps running the old image. Validate from the tool output, not from claims.

Gowin auto-generates a per-bitstream **User Code** (default mode: the build TCL has no `set_option -user_code`, so Gowin computes a checksum-like value from the bitstream). It is written into the `.fs` header, so you have an independent expected value:

- expected (from the file you built): `grep -a UserCode <base>.fs` → `//UserCode: 0x0000XXXX`
- running (from the chip): `programmer_cli -d GW2A-18C -r 0` → `User code is: 0x0000XXXX`

Match → the running bitstream is byte-identical to the `.fs` you built (so the RTL you edited is live). Mismatch → the write did not take effect; re-program. Properties: same `.fs` always yields the same code; a different design yields a different code (checksum — tiny theoretical collision chance, negligible in practice). This is how you tell **different firmware images apart** and confirm which one is loaded. The code fingerprints the *bitstream*, not the pin/logic intent — pair it with the build report (pins constrained, timing clean) to trust the intent.

Where the code lives when read: `-r 0` reads the User Code from the FPGA's on-chip USERCODE register, which is loaded **at configuration time** — so it reflects the *currently running* configuration (the image in the config SRAM cells), **not** the Flash contents directly. That is exactly why it validates "what is actually live" and why it is a reliable running-image fingerprint.

A clean `-r 0` also proves link health in one shot: `ID code 0x0000081B` (GW2A-18C), `Status code 0x00006020`, a single `Compatible cable found`, sub-second cost.

Gotcha with external Flash (`-r 37`): a successful flash *write* does not guarantee the FPGA reloaded the new image — the running config stays whatever is in SRAM until a reload (`-r 1`) or power-cycle, so `-r 0` can still show the old User Code right after a "successful" `-r 37`. For an immediate on-bench check prefer volatile SRAM (`-r 2`), which reconfigures the FPGA directly; then confirm with `-r 0` that the User Code matches the `.fs`.

## Confirm the build actually regenerated the bitstream

A failed `gw_sh` synthesis does **not** delete or overwrite the previous `.fs` — and Gowin leaves the generated `.fs` read-only (`-r--r--r--`). So when a build errors out before bitstream generation, the **old `.fs` stays in place**, and every subsequent program flashes the stale image while the build "looks done". `gw_sh` can also exit 0 with synthesis errors. Do not trust the exit code or a stale report — validate every build:

- The log has **`Bitstream generation completed`** (and `Placement and routing completed`) and **no `ERROR`** line: `grep -c ERROR <log>` → 0. The real root error is the first `ERROR` that is **not** `... ignored due to previous errors` (those are cascades); filtering the log by an "error" keyword can hide it, so read the first errors in order.
- The `.fs` **timestamp/size changed** this build, and its `//UserCode` differs from the previous design. Same `//UserCode` after an intended change = the `.fs` did not regenerate.
- If a rebuild refuses to update the `.fs`, remove the read-only artifacts first: `chmod -R u+w impl && rm -rf impl/pnr impl/gwsynthesis`, then rebuild clean.

GowinSynthesis is stricter than a ModelSim `.do` single-compile flow, so a design that simulates fine can still fail synthesis. Concrete case (2026-07-07): a header with **no include guard** (`SPI_Master.sv`) that got `` `include ``d both directly and through a guarded wrapper produced `ERROR (EX3794): Overwriting previous definition of module` in GowinSynthesis while ModelSim tolerated it — the failed builds were masked for several iterations by the stale read-only `.fs`. Give every `.sv`/`.svh` an `` `ifndef `` include guard.
