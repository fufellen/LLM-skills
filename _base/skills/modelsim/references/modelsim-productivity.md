# ModelSim Productivity Reference

Command inventory distilled from the ModelSim 10.5b User's Manual (page numbers = PDF pages of the vault conversion; open with `[[ModelSim users manual 10_5b.pdf#page=N]]`). Everything below is applicable to ModelSim ASE 10.5b unless a Starter-edition caveat is stated.

## Run Modes And Automation

- Three modes: GUI, command line (`vsim -c`, interactive prompt), batch (`vsim -batch`, non-interactive, stdout). `-batch` with output redirection gives the best performance for `$display`-heavy runs (pp. 40, 45-46). `BatchMode = 1` / `BatchTranscriptFile` in modelsim.ini make it the default; `vsim -logfile <f>` names the log, `-nolog` sends everything to stdout.
- `batch_mode` Tcl command returns 1 under `-c`/`-batch`: `if {![batch_mode]} { do wave.do }` — one `.do` for GUI and regression (p. 43).
- Robust scripts: `onerror {quit -code 1}`, `onElabError {quit -code 12}`, `onbreak {resume}` must appear BEFORE `run` (pp. 570, 574). Without them an error strands `vsim -c` at the prompt. `set OnErrorDefaultAction {quit -code 1}` is the global fallback.
- Exit codes (pp. 775-777): 0 ok, 1 bad invocation, 2 previous errors, 4 licensing, 5/6 library/design-unit access, 7 file I/O, 8 corrupted file, 12 load/elaboration, 16 version mismatch, 19/42-45 license manager, 90 SEVERITY_QUIT, 99 internal, 202 SIGINT, 211 segfault. `quit -code <n>` sets a custom code — pair with `$LASTEXITCODE` in PowerShell.
- DO-file parameters: `$1..$9`, `$argc`, `shift` (pp. 571-572): `do run_tb.do tb_name 42`. Environment channel: `$env(NAME)` in any command/DO file, `set env(NAME) val`, `printenv` (pp. 560, 819). Note: vlog/vcom/vsim do NOT expand env vars inside file-name arguments — expand in the shell; ini values DO expand `$NAME`; literal `$` escapes as `$$`.
- SV plusargs without recompilation (pp. 237, 242): `vsim ... +verbose +SEED=42`; `if ($test$plusargs("verbose"))`, `$value$plusargs("SEED=%d", seed)`. `CheckPlusargs = 1` (ini) catches misspelled plusargs.
- Record a session as a script: `transcript on` after loading — every typed command lands in the transcript, which replays as a DO file (comment out design `$display` lines first; rename before the next run overwrites) (pp. 43-44).
- One-shot stdin runs (here-docs) work: `vsim -c top < commands.txt` (pp. 42-43).
- `Startup = do setup.do` in modelsim.ini auto-runs after design load; explicit `-do` overrides it (p. 42).
- Interrupt toolkit: `run -continue`, `status`, `abort`, `pause`/`resume` (p. 574).
- `-stats=time,perf` on vlog/vcom/vsim logs elapsed time and memory per command; `+list` emits Tcl-parseable form (pp. 49-50).

## Compile Faster

- `vlog -incr`: pass the full file list every time; only changed modules recompile (p. 191). Whole-command argument changes force full recompile.
- Precompiled resource libraries (pp. 33-34): compile unchanging code (Gowin primitives, packages) once into its own library (`vlib gowin_lib; vlog -work gowin_lib prim_sim.v`), reference at elaboration with `vsim -L gowin_lib` or permanently via `LibrarySearchPath` (ini, p. 657). Stops re-vlogging vendor models in every testbench script.
- `vlog -mfcu` / `MultiFileCompilationUnit = 1`: all files of one vlog call share one compilation unit — `define`s, typedefs, `$unit` declarations and `timescale` propagate across files (pp. 193, 204, 672). Default SFCU makes macros die at end of each file. `-mfcu=macro` propagates only macros.
- `vlog -timescale "1ns / 1ps"` sets the default for modules without `` `timescale `` — fixes elaboration error vsim-3009 with vendor primitives (p. 203).
- Source libraries for auto-resolution of missing modules: `vlog -y <dir> +libext+.v+.sv`, `-v <file>` (pp. 187, 195).
- Multi-library flow: `vlog -work <lib>`, `vsim -L <lib>` / `-Lf` (pp. 192, 202).
- `vlog -lint` adds extra checks; `vlog -pedanticerrors` = portability audit (non-LRM ModelSim extensions become errors) (pp. 183-184, 777-778).
- Flat libraries are the vlib default (small file count — faster create/delete on Windows and friendlier to Drive sync); `vmake` needs legacy `vlib -type directory` (p. 34).
- `vmap logical {path with spaces}` — Tcl braces beat PowerShell/Tcl quoting battles (p. 35). `vmap` values may use env vars for portable mappings (pp. 824-825).

## Log Everything, Decide Later

- `add log -r /*` right after `vsim`, before `run`: every signal change goes to the WLF; any signal can be added to Wave or `examine`d AFTER the run without re-simulating (pp. 423, 434-435). The core post-mortem debug enabler for headless runs.
- Trap 1 — `WildcardFilter` (ini/`set WildcardFilter`, p. 742): by default wildcards exclude `Memory` (plus Variable, Constant, Parameter, ...). FIFO/histogram/calibration arrays are silently NOT logged. Remove `Memory` from the list or `log /path/to/mem` explicitly.
- Trap 2 — `WildcardSizeThreshold` (pp. 743-744): objects ≥ 8192 bits are silently dropped from wildcard matches. `set WildcardSizeThreshold 0` disables; `...Verbose 1` warns per drop.
- SV virtual interfaces and class objects need `log -class` / `vsim -classdebug` for class debugging (pp. 251-253, 400-401).

## Keep And Compare Runs (WLF/Datasets)

- Per-run WLF instead of overwritten `vsim.wlf`: `vsim -wlf tb_x.wlf` or `WLFFilename` (ini); save a finished live sim with `dataset save sim gold.wlf` (pp. 329-331, 749-750).
- Compare against a golden run: `vsim -view gold=gold.wlf` (repeatable), or `dataset open`; signals address as `gold:/top/...` vs `sim:/top/...` in one Wave window. Resolutions must match (`wlfman` converts) (pp. 327-338). Split Wave panes help side-by-side viewing (p. 385).
- Size control for long runs: `vsim -wlfslim <MB>`, `-wlftlim {5000 ns}` (sliding window), ini `WLFSizeLimit`/`WLFTimeLimit`; stricter one wins (pp. 331-334). `-wlfdeleteonquit` auto-removes throwaway regression WLFs (pp. 331-332).
- Event detail vs speed: `WLFCollapseMode` — `-nowlfcollapse` (0) records every delta event (needed for race/glitch debug and expanded-time view), default delta-collapse (1), `-wlfcollapsetime` (2) = smallest/fastest (pp. 339-340, 360, 746).
- Unclosed WLF (`vsim` killed before `quit`) → "bad magic number" on next open; repair with `wlfrecover <file>` (p. 329).
- `dataset snapshot` — periodic autosave of the live WLF (pp. 329-330).
- VCD bridge: `vcd file f.vcd; vcd add /tb/dut/*` (or SV `$dumpfile`/`$dumpvars`); `.gz` name → gzip on the fly; `vcd off/on` window-of-interest dumping; `vcd2wlf` converts external VCD (e.g. from iverilog) into a viewable dataset (pp. 534-545). EVCD with driver data: `vcd dumpports`; replay stimuli from EVCD: `vsim -vcdstim` (pp. 536-539).

## Wave Efficiency

- `add wave -group "TDC ch0" sig1 sig2` — named nestable collapsible groups; repeat command appends; saved in wave format files (pp. 386-390). Upgrade from plain `-divider`.
- Save/restore the whole debug session: `write format restart session.do` recreates windows, wave contents, file and `when` breakpoints; `ShutdownFile = restart#.do` (ini) writes it automatically on exit (`#` = version counter) (pp. 394, 418, 463-464, 706).
- `DefaultRestartOptions = -force` (ini): bare `restart` reloads the recompiled design instantly, keeping Wave layout, groups, radixes — the fastest edit-compile-look loop (pp. 617, 764).
- Virtual signals: rebuild synthesis-flattened buses or combine scattered taps into one bus — `virtual signal`, GUI Combine echoes the reusable command to the Transcript; `virtual save`/`virtuals.do` persists definitions; virtual functions compute expressions; virtual types map bit patterns to FSM state names (pp. 341-343, 392, 403-405).
- Radix: `radix -hex`, per-signal `add wave -radix hex`, global `DefaultRadix` (+ `DefaultRadixFlags` for enums), custom radices for named values (pp. 382-383, 585, 615-616).
- Expanded time (pp. 359-367): `wave expand mode deltas|events` shows intra-timestep ordering (blue = per delta, green = per event, red dot = multiple changes). Requires `-nowlfcollapse` data. `examine -delta <n>` / `-event <n>` and `searchlog -event` script the same queries in batch.
- Cursors: interval readout as frequency (Grid and Timeline tab, pp. 352-353); bookmarks save zoom+scroll (pp. 369-370); timeline can count clock cycles instead of time (pp. 379-380).
- `searchlog -expr {<expr>}` finds multi-signal conditions ('rising/'falling qualifiers) across the log without a checker (pp. 371-376).
- `WaveSignalNameWidth` (ini) / Display Signal Path — short leaf names in Wave (pp. 351-352, 741).

## Debug Without Rerunning

- `examine [-hex|-delta|-event] <obj>`, `describe <obj>` from CLI/DO files; `[examine ...]` command substitution enables self-checking scripts: `if {[examine -hex sig] == "3F"} {...}` (pp. 453, 558).
- Signal breakpoints: `when {errorFlag = '1' OR $now = 2 ms} {stop}` — whitespace before the time unit is REQUIRED (pp. 413, 416).
- File-line breakpoints: `bp file.sv 60`, conditional `-cond {this.id == 9}` (class instances via CIID `@class@n`), `-inst` per instance, and a Tcl body `{examine ...; run -continue}` = scripted logging without editing RTL (pp. 269-270, 459-467, 568-569).
- `change` edits task/function local variables at a breakpoint (p. 234).
- Race hunting: `vlog -hazards` + `vsim -hazards` reports WRITE/WRITE, READ/WRITE order hazards (limits: no bit-selects, NBAs excluded; implies `-compat`) (pp. 210-211).
- Zero-delay infinite loop: raise `IterationLimit`, or `vsim +autofindloop` names oscillating instances (pp. 149-150, 586, 654).
- `drivers`/`readers` CLI commands list signal sources/sinks (p. 443) — usable even though full Dataflow tracing is limited in ASE.
- SIGSEGV on null class handle: transcript names the line; `vsim -classdebug` + `classinfo` inspect instances (pp. 211-213, 251-253).
- `$signal_force("/tb/dut/reset", "1", 0, 3, 200000, 1)` / `$signal_release` (Signal Spy): runtime-string hierarchical paths (buildable with `$sformatf` in loops over channels), scheduled value with auto-cancel — one line replaces an always block; freeze/drive/deposit types (pp. 488-493).
- `mti_Cmd`: `import "DPI-C" function int mti_Cmd(input string cmd);` — execute any simulator command (force, log, change) from SV code at the exact simulation moment; precompiled imports in `<install>/verilog_src/dpi_cpack/dpi_cpackages.sv` (pp. 790-791).

## Time Correctness

- `vsim -t 1ps` (or `Resolution` in ini): delays finer than the resolution silently round — a 4 ps delay at `-t 10ps` becomes 0. Choose the coarsest resolution that does not round; too-fine slows the run and caps max reachable time (64-bit integer time) (pp. 145-146, 202-205, 693, 730). `report simulator state` shows the active setting.
- `` `timescale 1ns / 1ps ``: default resolution = smallest precision among all timescales. Mixed presence of timescale directives → error vsim-3009; fix with `vlog -timescale` (p. 203).
- Tcl time comparisons MUST use the 64-bit commands past 2^31 resolution units (~2.1 ms at 1 ps): `gtTime/eqTime/addTime/...`, unit-suffixed literals (`10ns`) (pp. 563-567). Plain `>` silently breaks.
- SDF values round to the annotated module's `timescale` precision: keep gate-level netlists/testbench at 1 ps precision for ps-scale timing (p. 525).

## Message Hygiene

- `verror <num>` explains any message number offline (`** Error: (vsim-3009) ...` → `verror 3009`) (pp. 772-773). Syntax-error flow: fix the FIRST error; check the previous line for missing `;`/bracket.
- Reclassify per run: `-suppress <n,n>`, `-error <n>`, `-warning <n>`, `-note`, `-fatal` on vlog/vcom/vsim; permanent in ini `[msg_system]` `suppress = ...` / `error = ...`. Promote dangerous warnings to errors so regressions fail loudly (p. 773).
- Named categories: `vsim +nowarnTFMPC` (too few port connections), `vlog +nowarnDECAY`, `vlog -nowarn 12` (pp. 774-775).
- `vsim -msglimit <n,...>` / `MsgLimitCount`: cap repeats of noisy messages at 5 (p. 775).
- `TranscriptFile = logs/transcript#.log` (ini): `#` auto-numbers logs per run; `transcript sizelimit` guards the disk; `transcript file ""` disables (pp. 727, 762).
- `SVPrettyPrintFlags` makes `%p` output of structs/arrays readable (pp. 723-724).

## Project modelsim.ini

- Lookup order (pp. 815-818): `-modelsimini <path>` → env `MODELSIM` → `$(MGC_WD)/modelsim.ini` → `./modelsim.ini` → installation file. `where` shows which ini/mpf is actually in use — first diagnostic when mappings "disappear".
- Keep a project ini in the repo (e.g. `C:\workspace\verilog\modelsim.ini`); all tools accept `-modelsimini`. Env vars work inside values (`work = $HOME/work_lib`, `test_lib = ./$TESTNUM/work`) — matrix regressions from PowerShell without editing the file (p. 761).
- `[DefineOptionset]` names bundles of command-line arguments (p. 582).
- Useful `[vsim]` defaults: `OnFinish = exit` (batch) / `stop` (GUI post-`$finish` inspection) / `final` (run SV final blocks) (p. 684); `DefaultRestartOptions = -force`; `ShutdownFile = restart#.do`; `DefaultRadix = hex`; `NoQuitOnFinish`; `IterationLimit`; `WLFFilename`/`WLFSizeLimit`/`WLFTimeLimit`/`WLFCollapseMode`.
- `CreateDirForFileAccess = 1`: `$fopen` auto-creates missing directories (p. 610).
- Personal Tcl autoload: `modelsim.tcl` / `MODELSIM_TCL` env var; GUI prefs to a file via `MODELSIM_PREFERENCES`; `DOPATH` = DO-file search path; `EDITOR`/`PrefSource(Editor)` external editor (pp. 817-822).
- External-editor sync: `PrefSource(CheckModifiedFiles) = 1`, `PrefSource(AutoReloadModifiedFiles) = 1` — VS Code edits auto-reload in the Source window (p. 451).

## DPI-C

- Simplest flow: C/C++ files directly on the vlog line — `vlog -sv tb.sv dut.sv dpi_model.c`; the right compiler is invoked per file type, objects land in `work`, vsim auto-loads at elaboration. No manual gcc/DLL step (pp. 786, 789).
- `vlog -dpiheader dpiheader.h files.sv` + `#include "dpiheader.h"` in the C: interface mismatches become C compile errors instead of elaboration warning vsim-3770 / runtime fatal vsim-160. Without the header on Windows, every DPI routine needs `DPI_DLLESPEC` (pp. 788-789).
- Custom flags: `vlog -ccflags`, `vsim -ldflags` (p. 789). External DLL flow: `-sv_lib`/`-sv_liblist`/`-sv_root` — DLL must be 32-bit for ASE (pp. 786-787, 798-799).
- Imported DPI tasks must return `int` (1 = disable-return, 0 = normal); mark imports `context`/`automatic` appropriately for reentrancy (pp. 786, 800, 250).
- Debugging DPI C: attach gdb to the `vsimk` process (the kernel that actually loads user C), not `vsim` (pp. 813-814). `MTI_COSIM_TRACE` traces HDL-interface calls (p. 823).
- Working examples ship in `<install_dir>/examples/systemverilog/dpi` (pp. 799-800).

## Gate-Level / SDF

- Annotate from the command line: `vsim -sdfmax /tb/dut=design.sdf` (also `-sdfmin`, `-sdftyp`; one option per file; paths in the SDF are relative to the annotated instance) (pp. 509-510, 528). In-source alternative: `$sdf_annotate` with corner selectable from the command line (pp. 515-517).
- Wrong-path diagnosis: `environment` command + the instance suggested in error vsim-SDF-3442 (pp. 528-530). Unannotated-object report: `vsim -sdfreport=<file>` (pp. 530-532).
- Reset-time false violations / X-pollution control: `+no_tchk_msg` (silence messages), `+no_notifier` (no X flips from violations), `+notimingchecks` (off entirely), `+nospecify` (also kills path delays — fastest functional gate sim), `+no_neg_tchk` (pp. 214-224, 526-527).
- Delay modes for Verilog-XL-style cells: `+delay_mode_zero|unit|path|distributed` (pp. 230-233).

## Include Resolution

A relative `` `include `` resolves against the **directory of the including file**, not against the current working directory (measured 10.5b, 2026-08-07, on a purpose-built two-hop chain compiled from a third directory: absolute path to the TB, no `+incdir`, `Errors: 0`, both hops resolved).

Consequences worth knowing before reaching for `+incdir`:

- `Cannot open \`include file` means the FILE moved away from its dependency, not that the shell is in the wrong place. Copying a testbench into a scratch directory while keeping its original `../../../` prefix is the usual cause; the same file compiled in place works from any CWD.
- Adding `+incdir` to make a copied file compile hides a wrong path and moves the dependency from the source into the command line — the file then builds under one invocation and fails under another. Use `+incdir` only for a genuinely shared search root.
- The design rule this supports: every file includes what it references, by a path relative to itself, and never waits for a dependency to arrive because another file was compiled earlier. Combined with `` `ifndef `` guards, being explicit costs nothing — a repeated include is free, a missing one is a latent file-order dependency that surfaces far from its cause.

## Known Traps

- ASE license boundary (measured 10.5b, 2026-08-07): `vlog -sv` silently compiles `rand`/`constraint` classes and covergroups (soft vlog-2186 warning only), but `vsim` refuses — `covergroup` kills design load ("only supported with QuestaSim"), `randomize()` dies Fatal even without covergroups. Classes as such, `$urandom_range`, associative arrays, and queues DO work. So no UVM and no constrained-random/covergroup benches on ASE; substitute `$urandom_range` + value tables for stimulus and associative-array "seen" sets for coverage, or move to cocotb+iverilog.
- Stale `_lock` file in a library after a killed compile → next compile hangs "waiting for lock". Verify no vlog/vsim process uses the dir, then delete `_lock` (p. 778). More likely on Drive-synced folders; per-run uniquely-named work libraries (existing convention in `C:\workspace\verilog\docs\modelsim.md`) avoid it entirely.
- `project compileall` in a `.do` is redundant when the `vlog` line already compiles the bench and its includes (existing user finding — keep scripts library-based, not project-based).
- Tcl 4-state comparisons need quotes: `== "001Z"`, `== "X"`; `'X'` single quotes are illegal; multi-line `if` needs `{` at end of line (pp. 559-560).
- `checkpoint`/`restore` exists but has platform caveats — verify locally before building a workflow on it (pp. 243-244).
- Waveform Editor stimulus generation does not support SystemVerilog types (p. 495+) — use it only for plain Verilog/VHDL signals; export to `force`-format `.do` or Verilog testbench works (`wave export`).
- ModelSim Tcl `exec` on Windows runs compiled executables only, not shell builtins (pp. 560, 568).
- Bind statements in their own file live in `$unit` and silently never elaborate; compile with `vlog -cuname bind_pkg -mfcu bind.sv` and load `vsim tb bind_pkg` as an extra top (pp. 296-298). Multiple top units on the vsim line toggle checker wrappers per run (pp. 294-295).
- `` `ifdef QUESTA `` is predefined in ModelSim — clean guard for sim-only code vs Gowin synthesis (p. 247).
- Escaped identifiers in Tcl need careful quoting (pp. 227-228).
- `force` on a value that references an `automatic` variable is rejected: `Automatic variable not allowed in force statement` (verified 10.5b, 2026-07-31). A `task automatic check(input ... value); force dut.sig = value; ...` fails to compile — drop `automatic` so the arguments become static, or force from a module-level variable. Bites when parameterizing a force-based testbench that otherwise never needs re-entrancy.
