# FPGA Development

Use this skill to make FPGA work reproducible: inspect the project first, identify the exact toolchain and target device, make narrow HDL/constraint edits, and verify with the lightest check that proves the change.

For long-running or high-stakes FPGA tasks, create an active goal when goal tools are available and write a compact plan/checkpoint before substantive work starts. Record the objective, target branch, files in scope, user constraints, planned simulations/builds, baseline observations, and next steps so context compaction cannot erase task state. After compaction, interruption, or a long gap, read the active goal/plan and the checkpoint before continuing.

## Workflow

1. Identify the active FPGA project before editing.
   - Look for `.gprj`, `.xpr`, `.qpf`, `.qsf`, `.cst`, `.xdc`, `.sdc`, `.tcl`, `.do`, `impl/`, `sim/`, and top modules.
   - Read existing build scripts before inventing commands.
   - Treat generated implementation outputs as artifacts unless the user asks to inspect them.

2. If the user says a project is incomplete after `git pull`, a clone is missing dependencies, or a previous commit/TODO asks to fix dependencies, resolve it autonomously.
   - Inspect the newest relevant commit first: commit message, TODOs, touched files, submodule pointer changes, and build-script changes.
   - Check `.gitmodules`, `git submodule status --recursive`, submodule remotes, and whether the exact pinned submodule commits exist on the configured non-local remote with `git ls-remote` or equivalent.
   - Replace local-only submodule URLs such as `C:/workspace/...` with the intended shareable remote when it is knowable from the submodule remotes. If the pinned commit only exists locally, do not silently leave the superproject pointing at an unreachable SHA; either move to a reachable commit only when that preserves the requested behavior, or record the exact unpublished submodule commits and state that pushing that submodule is required. Do not push unless the user explicitly asks.
   - Search project files, build scripts, TCL, `.gprj`, `.do`, docs, and active source for references to untracked `.v/.sv/.svh/.vh`, `.cst`, `.sdc`, `.ipc/.mod`, `.hex/.mem`, firmware, scripts, and vendor sources. Add missing source dependencies to version control when they are required to open/build/simulate the active project.
   - Keep generated outputs out of version control: `impl/`, `work/`, ModelSim `wlft*`, `vsim.wlf`, `.vcd`, PnR/synthesis reports, temporary PDFs, OS shortcuts, copied batch files, and local GUI/user files. Extend `.gitignore` when noisy generated files obscure the dependency audit.
   - Prefer making project paths relative and script-derived from the repository root. Avoid checked-in absolute paths to `C:\workspace\verilog` in active project files or build entrypoints unless the tool format truly requires them.
   - Document external tool dependencies that cannot be vendored, such as Gowin EDA, ModelSim, MSYS2 make, RISC-V GCC, `lconf`, Npcap/Scapy, and hardware/programmer requirements, including the exact wrapper command that proves the setup.
   - Verify the fix from a clean checkout shape when feasible: clone or worktree into a temporary directory, initialize submodules, run the lightest build/simulation check that covers the active target, and confirm no required file is present only because it was untracked in the original workspace.

3. Classify the task.
   - HDL edit: inspect the module, its interfaces, testbench, included packages, and call sites.
   - Constraint edit: inspect pin, clock, timing, and IO-standard constraints together with the board/top wrapper.
   - Build/debug: find the project script and latest logs/reports before changing code.
   - Simulation: prefer existing `.do` or documented ModelSim/Questa flow.
   - Programming/flash: require an explicit user request before invoking programmer tools or writing hardware.

4. Make scoped changes.
   - Prefer existing project modules, IP wrappers, helpers, and known-good implementations before writing new HDL. Add new modules only when no suitable reusable block exists or reuse would make the change riskier.
   - Before hand-writing a local edge detector, synchronizer, pulse generator,
     timer, counter, FIFO, CRC, serializer, or similar helper, search the
     repository with `rg` by both function and likely module names and inspect
     its existing call sites. A private implementation is not justified merely
     because it takes only a register and an `assign`: reuse the canonical
     module when its latency, reset, clock-domain, and synthesis semantics fit.
     If they do not fit, record the concrete mismatch and cover the new helper
     with a focused TB. When correcting this pattern, audit and replace the
     obvious duplicates in the same functional scope instead of fixing only
     the first quoted occurrence.
   - Define every FSM state set with a SystemVerilog enum such as
     `typedef enum { ... } state_t`, and declare both current- and next-state
     registers with that enum type. Do not specify an explicit base type or
     packed width such as `logic [N-1:0]` for an FSM enum; leave its
     representation to the compiler and synthesis tool. Do not model an FSM
     with state `localparam` values plus an untyped `logic [N-1:0]` register.
     Preserve explicit enumerator values when an encoding is externally
     observed, used for diagnostics, or must remain stable; otherwise allow
     the enum to assign sequential values. When correcting legacy code, audit
     the obvious FSM copies in the same functional scope and prove the typed
     version with the affected TB and synthesis/PnR flow.
   - For a configurable serial or protocol engine, derive phase-counter widths
     from the longest legal phase across its public parameters, not only from
     the largest current default. Its focused TB must check wire order,
     per-phase output-enable/turnaround, exact cycle count, completion-strobe
     width, reset during a transaction, and safe illegal-state recovery. The
     recovery path must release bus ownership (`busy`, chip-select, clock, and
     output-enable as applicable), not merely assign the idle enum value.
   - Do not describe QSPI as one universal transaction protocol. State the
     exact verified lane/edge contract in the module name and documentation,
     for example mode-0 `1-4-4 SDR`: command on one lane, address and data on
     four lanes. Opcode meaning, address width, dummy/turnaround selection,
     register layout, SDR/DDR choice, and device setup are separate contracts.
     Put the reusable wire transaction in a transport module and bind the
     device-specific values in a thin wrapper.
   - Do not generalize a serial transport beyond its known consumers merely
     because a parameter can be added. Search current call sites first and
     implement the narrowest reusable contract that they actually require.
     Add runtime commands, additional address widths, lane modes, or DDR only
     with a real consumer and a focused protocol test for that variant.
     Parameterized indexed part-selects and shift serializers can infer more
     logic than a fixed proven path in Gowin, even when behavioral simulation
     is identical.
   - Accept a protocol-engine extraction only after the transport TB, the
     device-wrapper TB, affected integration TBs, and synthesis/PnR all pass.
     Compare registers, logic, Fmax, setup/hold, and bitstream freshness with a
     build of the exact pre-refactor commit. When a global PnR delta obscures
     the cause, compare primitive counts for the affected modules in the two
     synthesized netlists. A file-boundary refactor should not silently buy
     unused flexibility with LUTs.
   - Preserve existing module style, naming, reset polarity, clock-domain conventions, and package/interface structure.
   - Indent Verilog and SystemVerilog with four spaces per nesting level. Do not use literal tab characters or two-space indentation. Keep continuation indentation on four-space boundaries. For an indentation-only change, confirm that the diff is whitespace-only and rerun the relevant testbench before committing.
   - Follow these HDL naming rules in new and edited module contracts:
     - Prefix ordinary input ports with `in_` and output ports with `out_`; `clk`, `rst`, and interface ports are exceptions.
     - Prefix every interface port and interface instance with `if_`; use `if_lcl_<name>` for a local interface.
     - End every one-cycle strobe name with `_stb`; do not use `_1t` as the public strobe suffix.
     - Mark internal interconnects that do not cross the current module boundary with the `lcl_` prefix (`lcl_<name>`), and do not give them `in_` or `out_` prefixes. `lcl` goes at the front of the name, never at the end: the trailing `_lcl` form found in older code (`crc_lcl`, `if_rmii_lcl`, `real_rib_detected_lcl_stb`) is legacy and must not be used in new or edited declarations; rename it when the surrounding lines are being reworked anyway, not as a standalone sweep.
     - For a local strobe, use `lcl_<name>_stb` so `lcl_` stays the prefix and `_stb` remains the final suffix.
     - Prefix every module instance name with `obj_`, normally `obj_<module_name>` (`ref_encoder_z_rib_detector #() obj_ref_encoder_z_rib_detector (...)`); add a distinguishing suffix when one module is instantiated several times. Short forms such as `o_<module_name>` are legacy and must not be used in new code. Interface instances keep the `if_` prefix instead.
     - Update every named port map and relevant testbench in the same change when renaming a port.
   - Declare parameters, ports, and variables in column form whenever the language allows one keyword/type to introduce several names: write the keyword (`parameter`, `input`, `output`, `logic[23:0]`, ...) once, then put each name on its own indented line, one comma-separated item per line. Do not repeat the type keyword on every line and do not pack a long list onto one line. Alternative values kept for bench work stay as commented-out lines inside the same block, next to the active one, and a trailing `//` comment belongs on the line of the name it describes. Two closely related names may share a line only when they are a pair (a value and its copy).

     ```systemverilog
     parameter
         INIT_VALUE = 100_000,
         // INIT_VALUE = 1500,
         FEEDBACK_COEFFICIENT = 4,
         INIT_VALUE_IIR = (INIT_VALUE * (FEEDBACK_COEFFICIENT - 1) / FEEDBACK_COEFFICIENT);

     logic[23:0]
         rib_period_rought,
         instant_period_cnt, instant_period_cnt_cpy = 0,
         rib_cnt,  // теперь генерируется из ref_enc_phase_counter
         max_rib_cnt = 0,
         avg_rib_period, // значение после двух фильтров баттерворта
         real_period = 0,
         virtual_rib_period,
         virtual_rib_precise_cnt;
     ```

     The bit width is part of the shared declaration head, so group variables by width: one `logic[23:0]` block for all 24-bit signals instead of a separate declaration per name. The same applies to the port list — one `input` / `output` keyword, then the ports in a column, with a nested type keyword only where the type actually changes. Reference implementation: `src/ref_encoder/ref_encoder_v4/ref_encoder_v4/ref_encoder_v4.sv`.
   - Prefer a SystemVerilog streaming concatenation over a generate loop for
     pure static packing, unpacking, or element reordering when it expresses
     the mapping directly. Specify both direction and slice size explicitly
     (for example, `{<<8{bytes}}`), document which element occupies the least-
     significant slice, and verify the order in a focused TB with distinct,
     non-symmetric element values. Compile and synthesize the expression with
     the target toolchain before adopting it; fall back to explicit indexed
     assignments when streaming support or the mapping is ambiguous.
   - Do not bury product, calibration, or conversion thresholds as numeric literals in leaf-module instantiations. Expose them as named parameters at the owning configuration boundary and thread the same values through every intermediate module to the consumer. Until the real source of a threshold is defined, keep the current value only as a clearly documented default; do not invent runtime detection or calibration logic ahead of that decision. A verification test must override the parameter with a non-default value and assert the changed functional result. Checking only the default behavior, the elaborated parameter value, or a hierarchical constant does not prove that the parameter is actually propagated and consumed.
   - Keep FPGA board firmware split into a strict file-layer hierarchy when creating or substantially changing a target:
     1. CST/XDC/QSF constraints are the first and lowest physical layer: package pins, IO standards, pullups, and raw package/connector names only.
     2. The board-interface wrapper translates constraint-level port names into meaningful hardware interfaces, `wire`, and `logic` signals; keep pin directions, tri-state behavior, straps, and board-role comments here.
     3. Helper-hardware files contain reusable plumbing such as PLLs, clock dividers, reset generators, serializers, FIFOs, CRC blocks, multipliers, counters, and pin-safe adapters.
     4. Main/application logic files contain the actual behavior and protocol modules, analogous to `main`. Do not hide package pins, CST naming, board straps, PLL/divider plumbing, or pin adapters inside the main logic layer.
   - For board-level dev-board firmware, inspect and reuse existing board wrappers and constraints such as `m20k_dev_brd_ifm.sv` / `m20k_dev_brd.cst` before creating a new top-level pin/interface layer.
   - For one-off dev-board checks, do not add new `m20k_dev_*` top, `.cst`, or `.sdc` files just to isolate a small test. Fold the test into an existing board wrapper/constraint flow, or explain why reusing the existing wrapper would be unsafe before adding files.
   - Do not create a new SystemVerilog interface or interface wrapper for every small bench task. Use plain ports for simple one-off firmware unless the surrounding design already expects an interface.
   - Before declaring a signal live, grep for where it is READ, not only where it is declared and port-mapped. A port can be wired through several levels and never consumed: `out_frame_started_stb` travelled `frame_detector` → `angle_sinc_frame` → `angle_calculator` → `encoder_processing` → `TDC_4_1` and was never read there, while MSOP frames were actually cut by a different signal. A dead path costs nothing at runtime but sends every reader of the code down the wrong causal chain, and a testbench may even `force` it to hide the confusion.
   - Avoid broad rewrites of HDL that could perturb timing unless the user asked for refactoring.
   - For CDC, async reset, generated clocks, PLLs, IO, and RAM/IP primitives, verify the intended vendor/tool behavior instead of assuming generic Verilog semantics.

5. Отладка неожиданного поведения железа: СНАЧАЛА воспроизвести в симуляции.

   Когда плата ведёт себя не так, как ожидалось, не начинать с перепрошивок и
   переносов индикации. Взять снятый анализатором/осциллографом стимул (байты,
   тайминги, частоты) и подать его в тестбенч на реальный топ платы, наблюдая
   внутренние сигналы. Один прогон занимает около минуты против пяти-шести на
   цикл «сборка + заливка», и показывает то, чего на пинах не видно.

   Урок 23.07.2026 (стоил десяти циклов сборки и прошивки железа): команды МК не
   доезжали до регистров ПЛИС. На плате менялись пины индикации, биты счётчиков,
   источники стробов — всё вслепую. Первый же тестбенч, подавший снятый кадр на
   командный SPI, сразу показал причину: адрес 0x438 читался как 0x870, то есть
   весь кадр сдвинут на бит из-за несовпадения режима SPI мастера и слейва.

   Признак, по которому надо сразу идти в симулятор: на шине сигнал есть и
   выглядит корректно, а внутренняя реакция отсутствует. Такое расхождение
   почти всегда про фазу/выравнивание, и на пинах его не увидеть.

   Индикацию на светодиод/пин добавлять ПОСЛЕ того, как гипотеза проверена в
   симуляции — чтобы на железе подтверждать уже понятое, а не искать вслепую.

6. Verify progressively.
   - First run syntax/compile checks when available.
   - Run relevant testbenches for behavioral changes.
   - ModelSim ASE DOES run several simulations concurrently — do not serialize testbenches on a licensing assumption. Measured 2026-07-28: two `vsim -c` runs launched together kept two live `vsimk` kernels for ~2 min of real overlap and both finished with exit 0, Errors: 0.
   - Treat `** Fatal: vish lost connection to vsim process` / `** Fatal: Exiting VSIM license process` / `Kernel lost connection to front end process` as "this run proved nothing", not as a design defect and not as a diagnosed cause. A run reported as "completed, exit code 0" whose output ends in those lines did NOT verify anything — rerun it and check the verdict line. Observed once (2026-07-28) when two heavy project testbenches ran in parallel and the longer one had been pushed off the foreground by a 600 s harness timeout; the actual cause was never established. Do not repeat the licensing explanation as fact: the concurrency measurement above refutes it for light designs, and memory pressure (`win32aloem` is a 32-bit binary, ~2 GB address space) or the timeout handling remain untested candidates for heavy ones.
   - Compile a testbench from ITS OWN directory, or pass `+incdir+<repo>/src`. Project sources use relative `` `include `` paths resolved against the current working directory, so compiling from a scratch directory fails with `Cannot open \`include file` deep inside an unrelated header — again not a code defect. The project `.do` files already `cd` to the script directory; prefer them.
   - Give long simulations a realistic time budget before treating silence as a hang: check that `vsimk` is actually burning CPU (`Get-Process vsimk | Select CPU`). Scale from a known run — one `encoder_processing` instance covers ~3 ms of model time per 1.5 min, so a 40 ms two-instance sweep such as `encoder_processing_sector_tb` needs ~40-45 min and prints its verdict only at the very end.
   - Match evidence to the claim being made. Simulation can prove packet bytes, state-machine behavior, CRC/FCS, timing of internal handshakes, or other logic-level properties; tool evidence can prove build, pin placement, timing, bitstream generation, and programmer operations; hardware evidence can be Ethernet capture, UART output, LEDs, link state, oscilloscope/logic-analyzer/GAO capture, or user-confirmed physical behavior. Require Ethernet capture only when the claim is that packets actually traversed the network.
   - Before programming hardware, prefer a ModelSim Intel FPGA Edition 10.5b simulation or at least a ModelSim compile/elaboration check for the firmware top.
   - Run synthesis/implementation only when the change can affect hardware build, timing, pinout, or generated firmware.
   - If a GUI/CLI tool gives surprising or inconsistent hardware behavior, inspect the tool and firmware source that builds/parses the packet before changing HDL or firmware. Treat screenshots and GUI labels as symptoms; confirm the actual protocol bytes, offsets, ports, bind addresses, and parser expectations from source or packet capture.
   - For bench-board firmware tasks, do not stop at simulation and `.fs` generation. After a clean build, verify on the actual hardware unless the user explicitly asks for build-only work or the board/tool is unavailable.
   - Step zero of hardware bring-up: do NOT start debugging configuration or RTL for a stuck function until every required signal is confirmed physically present and correct on the wires. Probe/scope each stimulus, clock, trigger, the stimulus SOURCE, and the DUT response along the whole signal path, and confirm the bench top actually drives the pin a bench cable is wired to. An undriven pin, a top-level port the wrapper never declared/drove, an unconstrained pin, or a dead source masquerades as a config/logic bug and can burn an entire debug session. (Concrete: an LTDC-X3 bring-up returned only `no_hit` for a long time while config was repeatedly changed — the real cause was that the bench top never drove `FPGA_HF` (K12/K13), the pin the STOP cable was wired to, so the STOP source had no signal at all.)
   - For hardware verification, program volatile memory when possible, then capture real observable evidence such as UART terminal output, packet capture, LEDs, link state, logic-analyzer/DSView bytes, or user-confirmed physical behavior.
   - Treat DSView and other logic-analyzer screenshots or exported captures as hardware evidence. If an image or capture file is available, inspect it directly instead of asking the user to transcribe bytes. Record the probe-to-signal mapping, sample rate, decoder settings, and which lines are expected to be active for the selected protocol mode.
   - Summarize errors by root cause and cite the log/report file paths.

7. Report hardware outputs clearly.
   - Name generated files such as `.fs`, `.bin`, `.bit`, `.sof`, `.pof`, or reports.
   - Include target device, top module, build command, result path, and whether timing/build passed.
   - State when programming or hardware verification was not performed, and do not present a hardware-targeted task as complete if only simulation/build passed.
   - Create a local git commit after each meaningful intermediate milestone that passed verification. A milestone is commit-worthy when there is feedback from real hardware, a packet/UART/LED/capture observation, or correct simulator/tool output that proves the current stage. Treat the whole task as complete only after hardware observation, terminal/capture evidence, simulator evidence for simulation-only work, or user confirmation proves it worked. Do not push unless explicitly asked.

## Commit Handling

At the end of each completed FPGA task, create a local commit with a concise Russian commit message. Use the conventional form when it fits.

Split commits by semantic block when the work contains independent concerns. Avoid vague rollups such as "skill update" or one commit mixing an RTL feature with an unrelated docs move; prefer separate concise commits, each describing one concrete change.

In the final response, also present the commit message as a fenced `text` code block containing only the commit message, with no bullet, prefix, or extra prose inside the block, so the user can copy it with one click.

```text
<тип>: <краткое описание>
```

Examples:

- `test: добавить проверки формата MSOP TCP`
- `fix: исправить ширину поля расстояния в tdc_processing`
- `docs: уточнить порядок сборки LDR_20K`

Create a new commit after a completed task or a verified intermediate milestone. Verification means real hardware feedback, packet/UART/LED/capture evidence, or correct simulator/tool output for software/simulation stages. Do not commit unverified guesses or half-built code. Do not amend commits and do not push unless explicitly requested.

## Local Lidar Gowin Project

When the task mentions this lidar workspace, Gowin, LDR_20K, GW2A-18C, ModelSim, FPGA tables, firmware flash, or paths under `C:\workspace\verilog`, read `local-gowin-lidar.md`.

For Gowin Analyzer Oscilloscope, GAO, `.rao`, `.gao`, or internal hardware signal capture tasks, also read `gowin-analyzer-cli.md`.

For `lconf` tasks involving FPGA table uploads or FLASH blobs, also inspect:

- `C:\workspace\lidar\lconf\COMPENSATION_TABLES.md`
- `C:\workspace\lidar\lconf\FLASH_BIN_BLOB_RULES.md`

## Soft MCU And LwIP

For soft-MCU Ethernet work, treat firmware and HDL as one system.

- Do not commit local filesystem paths such as `C:\workspace\...` or
  `C:/workspace/...` into `.gitmodules`. Submodules must use a portable remote
  URL that another machine can fetch. If a local sibling checkout is useful on
  one workstation, keep it as a personal override in `.git/config` with
  `git submodule set-url` or `git config`, not in tracked project metadata.
- Before working on `dark_risc`, LwIP, soft-MCU firmware, memory maps, or FPGA/MCU Ethernet boundaries, read `soft-mcu-dark-risc-lwip.md`.
- Treat the soft-MCU reference as a self-learning project notebook: when a command, gotcha, register map, build constraint, toolchain quirk, memory-size limit, simulation result, or hardware observation becomes a reusable confirmed fact, update that reference in the same task. Keep transient task checklists in Obsidian and stable procedures in the skill reference.
- Local soft-MCU repo: `C:\workspace\dark_risc`; in the `verilog` repo it should be used as the `soft_mcu/dark_risc` submodule.
- Local STM32 F4 + LwIP reference: `C:\workspace\stm32_f401ccu6_platformio`. It uses LwIP with `NO_SYS=1`, IPv4, ARP, UDP, raw API, and no sockets/netconn.
- Repo LwIP source submodule: `C:\workspace\verilog\third_party\lwip`; `contrib\apps\udpecho_raw\udpecho_raw.c` is a minimal raw UDP callback example.
- Prefer moving L3/L4 parsing such as IP/UDP handling into soft-MCU firmware through LwIP. Keep HDL focused on RMII/MAC filtering, frame buffering, CRC/FCS handling, runtime config registers, and the frame transport boundary.
- For the LwIP netif boundary, pass full Ethernet frames without preamble/SFD/FCS into `ethernet_input`; implement TX through `netif->linkoutput` back to the FPGA Ethernet TX path.
- Track the soft-MCU UDP/LwIP integration checklist in `C:\Users\User\Мой диск\Obsidian\Проекты\FPGA soft MCU UDP LwIP.md`.

## 20K Dev Board Ethernet Checks

When testing Ethernet on the 20K dev board:

- Reuse the existing board files first: `src/main/m20k_dev_brd_ifm.sv`, `src/main/m20k_dev_brd.cst`, and `20k/LDR_20K/src/Eth_time_constraints.sdc`. Do not leave task-specific top/constraint/timing files in the repo unless the user explicitly wants a separate firmware target.
- Reuse existing RMII/UDP modules such as `static_udp_rmii` or `staticUDP_pack_former`; fix them in place when they are the intended reusable block instead of creating duplicates.
- For RMII transmit tests, validate packet bytes in wire order. Ethernet bytes are sent in packet order, while each byte's RMII dibits are sent least-significant bits first. A testbench that reconstructs data with the same indexing bug as the DUT is not a valid proof.
- For PHY bring-up, follow the existing board wrapper's reset behavior. On the 20K dev board, `m20k_dev_brd_ifm.sv` keeps `EthRST` deasserted high; if a NIC shows `Disconnected` or captures zero packets, check `EthRST`, link state, pinout, and clock before changing UDP payloads.
- For packet capture on Windows, prefer the adapter name with `tshark -i "Ethernet 5"` instead of a numeric interface id. Npcap interface numbers can change after the link comes up. Confirm with `Get-NetAdapter` and capture fields such as `eth.src`, `eth.dst`, `ip.src`, `ip.dst`, `udp.srcport`, `udp.dstport`, and payload.
- For RX destination-MAC filtering, validate the usual hardware classes explicitly: local unicast, broadcast, multicast, and a rejected unrelated unicast. When Windows cannot add static neighbor entries without elevation, Scapy/Npcap `sendp` to `Ethernet 5` can send raw Ethernet frames; accept/reject is proven by the FPGA UART output, not by local packet capture alone.
- For new Ethernet RX filtering and later protocol fields, prefer runtime configuration over hardcoded constants. MAC addresses, EtherType, IP addresses, UDP ports, multicast enables/groups, and similar fields should be driven by an existing control path or a small reusable register/config block; HDL parameters are acceptable only as reset defaults, testbench defaults, or temporary bring-up fallbacks.
- The user's networks can contain real working lidars in addition to the FPGA dev board. Broadcast discovery is allowed, but treat it as a multi-device operation: prefer an explicit adapter, collect all responses, filter the FPGA board by MAC/model/IP, and never treat the first discovery response as the target. For reproducible bench tests, send `NET_CONFIG`/write commands directly to the intended FPGA board MAC after confirming the current board config.

## Logic Analyzer And DSView

Use DSView screenshots, `.dsl` captures, CSV exports, or decoder tables as first-class hardware evidence.

- Inspect available screenshots or capture files directly before asking the user for manual transcription.
- Local DSView 1.3.2 is primarily a GUI. `DSView.exe --help` shows only file-open plus `--loglevel`, `--version`, `--storelog`, and `--help`; do not assume it can perform headless capture/export. If `sigrok-cli.exe` is not installed separately, use screenshots, saved `.dsl` captures, CSV exports, or controlled GUI inspection.
- For scriptable DSLogic Plus work, check `LISTENAI/dsview-cli` release bundles. Keep the extracted bundle intact; do not copy only the `.exe`. Useful commands include `dsview-cli devices list`, `dsview-cli devices options --handle 1`, `dsview-cli capture --handle 1 --sample-rate-hz <hz> --sample-limit <n> --channels 0,1,2,3,4,5 --output <file.vcd>`, and `dsview-cli decode list/inspect/run`.
- Treat `LIBUSB_ERROR_ACCESS` from DSView/libsigrok as likely exclusive USB ownership by the DSView GUI or another process. Ask the user to close DSView or stop the competing process before CLI capture; do not change HDL because of this error.
- Decoder IDs can be namespaced, such as `0:spi` or `1:spi`; run `decode list` before `decode inspect/run` instead of assuming the ID is plain `spi`.
- Start by reconstructing the channel map from the capture and the HDL/CST pin map. If the decoder works, trust the decoded bytes only after the channel labels match the real pins.
- For SPI RAM/Flash checks, explicitly identify `CS#`, `SCK`, `MOSI`, `MISO`, `IO2`, and `IO3`. In plain SPI mode, only `CS#`, `SCK`, `MOSI`, and `MISO` are expected to toggle; `IO2` and `IO3` can stay idle or pulled high. Six connected probes with four active lines is normal for SPI and is not by itself a fault.
- Configure SPI decoders with active-low chip select, MSB first, and the mode implied by the HDL or datasheet. If the byte stream is shifted or empty, try the adjacent clock phase as a decoder-setting check before changing HDL.
- Separate evidence classes: MOSI command/address bytes prove FPGA-to-device output; MISO bytes that match a prior write prove device response; static or floating MISO with valid `CS#`/`SCK`/`MOSI` points to power, soldering, mode, direction, or pin mapping.
- Record expected protocol bytes from the HDL/testbench, then compare DSView decoded MOSI/MISO against those bytes before declaring the hardware pass/fail.

## Safety

- Do not run `programmer_cli.exe`, erase flash, write SPI flash, or program volatile/nonvolatile FPGA memory unless the user explicitly asks for programming.
- Before hardware programming, restate the selected device, memory target, and firmware file.
- When the active user task targets a connected bench board and asks to verify firmware behavior, treat volatile FPGA programming as part of the requested verification. Still avoid nonvolatile flash unless explicitly requested.
- For local 20K programming, prefer the tracked `C:\workspace\verilog\20k\programming20K.bat` flow and volatile memory (`choice=2`, power-dependent SRAM) for bench tests. Use permanent/nonvolatile/external flash only when the user explicitly asks for persistent programming.
- From Codex, program the 20K board through a versioned project script/batch file rather than a one-off manual programmer command or the programmer GUI. Use the existing tracked volatile wrapper for SRAM tests and a tracked external-FLASH wrapper for persistent writes; if a new programmer flow is needed, add the script under version control before relying on it.
- Prefer read-only inspection for logs, reports, generated netlists, and bitstreams unless a build is requested.
