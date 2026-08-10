# Gowin CLI Build Notes

## `gw_sh.exe` Behavior

- Local observed `gw_sh.exe` does not provide a useful interactive `help` command: `help set_option` returned `invalid command name "help"` on 2026-06-22.
- Prefer searching existing project Tcl files and Gowin config XML files for option names.
- Dual-purpose pin option labels are visible in `bin\IDE\data\config\multipurposeconfig.xml`; CLI aliases observed working include `set_option -use_mspi_as_gpio 1` and `set_option -use_sspi_as_gpio 1`.
- Do not enable `set_option -use_reconfign_as_gpio 1` when the MCU uses `RECONFIG_N` to reset the FPGA.  That option turns the dedicated configuration/reset pin into GPIO; leave it unset after `reset_option` to retain its dedicated role.
- Tcl `exec` can treat child stderr output as an error even when the child command succeeds. If a known-good build step prints harmless warnings to stderr, redirect it in Tcl, for example `exec {*}$cmd 2>@1`, and still check the command's real exit behavior.

## Minimal Tcl Skeleton

Use this shape for a reproducible build script:

```tcl
set project_dir [file dirname [file normalize [info script]]]

reset_option

set_device -name GW2A-18C GW2A-LV18PG256C8/I7

set_option -output_base_name <output_base>
set_option -top_module <top_module>
set_option -verilog_std sysv2017
set_option -synthesis_tool gowinsynthesis
set_option -write_apr_constraint 1

# Add only when the design really uses these dual-purpose pins.
set_option -use_mspi_as_gpio 1
set_option -use_sspi_as_gpio 1
set_option -use_ready_as_gpio 1
set_option -use_done_as_gpio 1

add_file [file join $project_dir path/to/top.v]
add_file [file join $project_dir path/to/pins.cst]
add_file [file join $project_dir path/to/timing.sdc]

run all
exit
```

Run it from PowerShell with:

```powershell
& 'C:\workspace\verilog\bin\IDE\bin\gw_sh.exe' path\to\build.tcl
```

## Mirroring A `.gprj`

When an upstream example has only `.gprj`:

1. Read the XML `Device` and `FileList`.
2. Use `set_device` for the same device and package.
3. Add every enabled Verilog/SystemVerilog, `.cst`, `.sdc`, and generated IP wrapper file with `add_file`.
4. Set the top module explicitly.
5. Add dual-purpose pin options that match the README or IDE project settings.
6. Run `run all`.

Do not assume a clean CLI build proves hardware readiness. Always inspect the generated pin report for unconstrained ports.

## Outputs To Check

Common output paths use the selected output base:

- `impl\gwsynthesis\<base>.log`
- `impl\gwsynthesis\<base>.vg`
- `impl\gwsynthesis\<base>_syn.rpt.html`
- `impl\pnr\<base>.log`
- `impl\pnr\<base>.rpt.txt`
- `impl\pnr\<base>.tr.html`
- `impl\pnr\<base>_tr_content.html`
- `impl\pnr\<base>.pin.html`
- `impl\pnr\<base>.fs`
- `impl\pnr\<base>.bin`

Minimum verification before reporting success:

- `gw_sh.exe` exits with code `0`.
- PnR log includes `Placement and routing completed`.
- PnR log includes `Bitstream generation completed`.
- `.fs` exists, and `.bin` exists when expected.
- Timing report has `Numbers of Setup Violated Endpoints = 0` and `Numbers of Hold Violated Endpoints = 0`. In some Gowin outputs `<base>.tr.html` is only a frameset; search `<base>_tr_content.html` too for the actual timing tables.
- PnR report resources are plausible for the target.

Useful search patterns:

```powershell
rg -n "ERROR|WARN|Placement and routing completed|Bitstream generation completed" impl
rg -n "Numbers of Setup Violated Endpoints|Numbers of Hold Violated Endpoints|Max Frequency|Total Negative Slack" impl\pnr\*tr*.html
rg -n "Resource Usage Summary|Logic|Register|BSRAM|PLL|DQS" impl\pnr\*.rpt.txt
```

## Local LDR_20K DDR3 Flow Gotchas

Verified on 2026-06-22 while building `C:\workspace\verilog\20k\LDR_20K` with `LDR_20K_DDR3=1`:

- In this Tcl flow, treat the active CST/SDC set as a single selected pair. Adding the original Ethernet CST/SDC and then adding DDR3-only CST/SDC caused constraints to be missed, such as `EthRefCLK` not being found by the final SDC. The working flow selects either the original non-DDR pair or the combined DDR3/Ethernet pair:
  - DDR: `20k\LDR_20K\src\m20k_dev_uart_ddr3_pins.cst` and `20k\LDR_20K\src\m20k_dev_uart_ddr3.sdc`
  - non-DDR: `src\main\m20k_dev_uart_deadbeef.cst` and `src\main\m20k_dev_uart_deadbeef.sdc`
- Avoid Tcl-style backslash line continuations inside Gowin SDC command text for this local CLI. `set_clock_groups -asynchronous ...` with backslash continuations failed; the working `m20k_dev_uart_ddr3.sdc` keeps the command on one line.
- The combined DDR3/Ethernet SDC clocks `EthRefCLK`, `sys_clk`, `clk`, and `clk_x4`, then groups them asynchronous in one command. The verified build reported setup/hold violated endpoints `0`.
- The combined DDR3/Ethernet CST includes the base Ethernet/UART/Flash pins plus Tang Primer 20K DDR3 pins, `sys_clk=H11`, `DDR3_nCS=P5`, `DDR3_A[13]=C8`, and `INS_LOC "pll/rpll_inst" PLL_L[0]`. Always recheck `LDR_20K.pin.html` after a DDR3 build.

## BSRAM Bank Wrappers: Infer, Do Not Hand-Instantiate

Verified on hardware 2026-08-04 (R120M.BF2_TDC7201_pwdiag, GW2A-18C): a
hand-rolled byte-RAM wrapper built from 16x `SDPB` primitives (2 KiB banks,
CE gating by bank compare, fabric mux on registered `read_bank_q`) corrupted
the FIRST byte read after every 2048-byte bank-boundary crossing — the mux
handover emitted the last byte of the previous bank instead. Symptoms and
traps:

- Invisible in RTL simulation (functional model of the wrapper is correct);
  placement-independent (survived rebuilds, seed changes, timing margins,
  `READ_MODE` bypass, SCK/2 output rate, registered write port, same-bank
  write guards, bank read priming). Only the data pattern on hardware showed
  it: corruption strictly every 256 points x 8 bytes = 2048 bytes, single
  phase mod 256.
- Fix: replace the whole bank structure with a plain inferred array
  (`logic [7:0] mem [0:N-1]` + registered read). Gowin synthesis maps it to
  BSRAM itself, handles bank stitching correctly, and the defect vanished
  (0 corrupted bytes in 400 frames vs 221/400 before).
- Root status: the lone SDPB inside one bank is flawless (megabytes
  bit-exact); the wrapper is correct per the vendor functional model (clean
  RTL sim, green black-box TB) yet silicon returns a foreign byte in the
  same scenario. Hard conclusion: the SDPB simulation model diverges from
  silicon in the "CE-gated bank + read handover to the next bank" corner.
  The exact silicon micro-mechanism was not isolated (no bare-primitive
  minimal repro) — treat "primitive bug" as a qualified hypothesis. Nothing
  documented was violated; Gowin simply does not specify this corner.
- Rule: for RAMs that cross BSRAM-block capacity, prefer inference over
  manual multi-primitive banking — inference stays on the vendor-tested
  BLKSEL cascade instead of an unspecified corner. If a hand wrapper already exists and a
  streaming consumer sees rare byte-level corruption on a fixed power-of-two
  grid — suspect the bank-boundary read handover first.
- No "better" simulation models exist (checked 2026-08-05). Gowin ships only
  the functional `prim_sim` libraries — the same optimistic models our clean
  RTL sim used; post-PnR timing sim reuses them with delays, so a functional
  divergence stays invisible. Community evidence that silicon has corners the
  models lack: apicula PR #479 — "CE and OCE in Dual Port mode in 9C and 18C
  chips are dependent" (our GW2A-18C!); apicula doc/bsram-fix.md — BLKSEL
  "doesn't work as expected" (they decode banks via CE instead), and the
  Gowin IDE itself inserts undocumented compensation primitives around BSRAM
  in some configs — logic present neither in UG285 nor in the sim models.
  Practical stance: treat prim_sim as optimistic; the silicon knowledge lives
  in vendor synthesis (inference) and in apicula's fuzzing notes; for
  critical streams add on-silicon self-checking (deterministic ramp +
  write/read checkers) — that is what actually caught this bug.

## Directionless Interface Port: Gowin Silently Drops The Wire

ПОПРАВКА 07.08.2026: раздел изначально приписывал отказ ВЛОЖЕННОСТИ
интерфейсов. Измерение синтезом (таблица в «Измеренная граница обрыва
интерфейсов» ниже) это опровергло. Настоящая причина — порт интерфейса
БЕЗ УКАЗАНИЯ НАПРАВЛЕНИЯ:

```systemverilog
interface interface_ref_encoder #()(logic ch_A);      // ОБОРВЁТСЯ
interface interface_ref_encoder #()(input logic ch_A); // работает
```

Вложенность невиновна: та же вложенная конструкция с `input` во внутреннем
интерфейсе работает, а без направления не работает даже ПРЯМОЕ чтение
`if_i.ch_A`, безо всякой вложенности. В сломанном случае вложенность лишь
сопутствовала, потому что боевой `interface_ref_encoder` объявлен голым
портом.

Языковая причина ПОДТВЕРЖДЕНА второй серией микротопов (07.08.2026):

- голый порт = неявный `inout`: интерфейс с ЯВНЫМ `inout logic ch_A`
  обрывается идентично голому (DFF=0, unused);
- направление НАСЛЕДУЕТСЯ последующими портами: `(input logic ch_A,
  logic ch_B)` — оба живут (DFF=2, IBUF=3). Опасен только порт, выше
  которого в списке нет ни одного направленного;
- дефект НЕ во внутренних inout вообще: `inout logic p` у обычного МОДУЛЯ
  Gowin корректно схлопывает (DFF=1, IBUF=2). Ломается ровно пересечение
  «inout × порт ИНТЕРФЕЙСА»;
- дополнительный след в логе: `WARN (NL0002) The module ... is swept in
  optimizing` на модуле-потребителе — получив константу, он выметается
  целиком; работает и для внутренних связей, где CV0016 молчит;
- почему сим зелёный: симулятор реализует порт слиянием сетей (port
  collapsing) и не проверяет направления как контракт (port coercion —
  ModelSim принял assign даже в явный `input`-порт интерфейса, 0 ошибок).

Verified on hardware 2026-08-05 (R120M.BF2 LTDC, GW2A-18C): the failure
elaborates fine in ModelSim (all TBs green) but Gowin synthesis SILENTLY
drops the connection: the source pin becomes `Input X is unused`, the
consumer reads a dangling net, and it shows up only as wrong runtime
behavior (here: encoder dead -> motor considered stopped -> no frames while
rotating).

- Detector: watch the synthesis log for `Input <pin> is unused` on pins that
  must be alive. Grep it in every build; its appearance/disappearance is a
  reliable regression bisector (clean at 9f63134f, broken at 0ce6f010).
- Fix pattern (дешёвый, одно слово): указывать направление у КАЖДОГО порта
  интерфейса — `input logic ch_A`. Голый `logic имя` в списке портов
  интерфейса не писать никогда.
- Fix pattern (запасной, применён в 4d17ab67): вести скалярные сигналы
  обычными портами модулей, интерфейс держать для группового протокола.
- Related known gap: sim-vs-synth divergences are a Gowin theme (see BSRAM
  bank wrapper above; unconnected port read as X in sim vs tied 0 in
  synthesis, 2026-07-06).


## Грабли делителей и фоновых сборок (06.08.2026, R120M)

- **fxp_div_pipe (MODE="FXP_PIPE" у divider) — площадная бомба**: конвейер
  глубиной Q_WIDTH+3 из полноширинных регистров. На частном 29 бит PnR упал
  с `ERROR (PR0003): 1871 REG(s) unPlaced` (GW2A-18C переполнен). Для
  редких делений (раз в десятки тактов) использовать MODE="SERIAL"
  (divider_uint_with_reminder): ~WIDTH тактов латентности, площадь на два
  порядка меньше. Конвейер оправдан только при делении каждый такт.
- **Ловушка ширин interface_divider в SERIAL-режиме**: обёртка соединяет
  поля интерфейса с портами делителя ширины MAX_WIDTH НАПРЯМУЮ. Более узкое
  поле (например B_WIDTH=24 при MAX=29) оставляет старшие биты порта в Z →
  защёлка b1 = Z → частное мусор (ноль/грязь) при внешне здоровых
  аргументах. Задавать ВСЕ ширины интерфейса равными MAX_WIDTH.
- **fxp_div_pipe на точно делящихся отношениях отдаёт floor−1** (594.0 →
  593); неточные усечены верно. Серийный делитель даёт честный floor.
- **fxp_div_pipe без include-guard**: повторный `include = redefinition;
  включать только через divider.sv (у того guard есть).
- **Детект «аргументы изменились» для перезапуска вычислителя травится X-ом**:
  первое же сравнение с неинициализированным значением даёт X, и ветка
  мертва навсегда (X != X = X). Для боковых вычислителей — свободно бегущий
  перезапуск по !busy, без сравнения аргументов.
- **`| head -N` на живой сборке убивает её**: head закрывает пайп после N
  строк — gw_sh умирает по SIGPIPE посреди PnR (ушло в лог как обрыв на
  «run all» без текста ошибки). Фильтровать вывод сборки только `tail`
  или писать полный лог в файл и грепать файл.

## Правка «не доехала» до железа: проверять ДО прошивки (07.08.2026)

Стоило нескольких циклов сборка→заливка→замер на живом лидаре. Упреждение
угла не работало на железе при идеально зелёной симуляции модуля; причин
оказалось две, обе молчаливые.

**1. Тип параметра наследуется от предыдущего в списке.**

```systemverilog
module encoder_processing #(parameter
    bit FRESH_GATE_EN  = 1,
    LEAD_TAU_TICKS = 16'd1650   // <- ОДНОБИТНЫЙ! наследует `bit`
)
```

Значение молча обрезается до 1 бита: 1650 → 0, 30000 → 0, 1 → 1. Ветвь,
зависящая от параметра, синтезируется мёртвой и вырезается целиком.
Ни одного предупреждения ни от Gowin, ни от ModelSim.

ModelSim ведёт себя ТАК ЖЕ — расхождения «сим против синтеза» нет
(проверено минимальным примером 07.08.2026):

| инстанс | результат |
|---|---|
| дефолт, тип наследует `bit` | TAU = 0 |
| дефолт, объявлен `int` | TAU = 1650 |
| `#(.TAU(1650))` у заражённого модуля | TAU = 0 |

Обрезание происходит В САМОМ модуле: ширину задаёт объявление параметра, и
даже явно переданное сверху значение приводится к этой ширине. Прежнее
объяснение «в ТБ параметр объявлен с типом, поэтому там верно» — ОШИБОЧНО.

Почему не поймали симуляцией — вопрос ПОКРЫТИЯ: фокусный ТБ проверял модуль
`angle_360_to_mirror_180`, где параметр стоит ПЕРВЫМ в списке и заражения
нет; а тесты уровня `encoder_processing` (где он и портился) величину
упреждения не наблюдали вовсе. Тестировать надо ту единицу иерархии,
откуда значение реально берётся, и проверять наблюдаемый ЭФФЕКТ величины.

Про стиль: неявный тип параметра остаётся нормой и сам по себе удобен —
менять стиль всего проекта не требуется. Следить нужно за СОСЕДСТВОМ: если
выше в списке стоит типизированный параметр (особенно `bit`, а также `byte`
= 8 бит, `shortint` = 16, `string`), следующий обязан объявить свой тип.
Тип «прилипает» сверху вниз до ближайшего объявления с типом, поэтому
смотреть надо весь список, а не свою строку.

Быстрый способ поймать: собрать с двумя разными значениями параметра и
сравнить SHA битстрима (см. ниже). Одинаковый SHA = значение не влияет,
и первый подозреваемый — именно тип в списке параметров.

ЛОЖНОЕ «ВСЁ ЧИСТО» при проверке `$bits` (ModelSim, боевой RTL, 07.08.2026):
усечение происходит в списке параметров ЗАРАЖЁННОГО модуля, а ниже по цепочке
параметр объявлен `int`. Изнутри `angle_calculator` и `angle_360_to_mirror_180`
он выглядит честным 32-разрядным НУЛЁМ (`$bits = 32`, значение 0) — следов
обрезки не видно. Значит `$bits = 1` доказывает ловушку, а `$bits = 32` НЕ
доказывает её отсутствия: печатать надо в том модуле, чей список реально
задаёт величину.

Воспроизведение на боевом RTL (две обёртки над настоящим `angle_calculator`,
отличаются только объявлением параметра; диск 50 зубов, ФАПЧ ловится за 3
оборота): заражённая ветка — `advance_mgrad = 0` во всех 480 отсчётах;
исправленная — 5940 при периоде ребра 2000 и 11880 при 1000, ровно
`7200*N_tau/rib_period`, min = max. Разность выходного угла = 11880 при
advance 5940, то есть ровно 2x — удвоение свёрткой подтверждено. Контроль
`#(.LEAD_TAU_TICKS(30000))` сквозь полную цепочку приходит нулём. Ни одного
предупреждения об усечении ни от ModelSim, ни от Gowin.

Сплошной аудит: `python scripts/check_param_type_inheritance.py src`. Скрипт
разбирает каждый `parameter_port_list` и печатает все нетипизированные
параметры, стоящие после типизированных, с унаследованной шириной. Проверен
на больном состоянии (`encoder_processing.sv` из `d60d9a68`): находит
`LEAD_TAU_TICKS наследует 'bit' (ширина 1)`. По текущему дереву — 6
срабатываний, все `int` (32), все намеренная колоночная форма. Держать этот
список как БЕЛЫЙ: новое имя в выводе = либо новая колоночная группа, либо
новая ловушка.

Как отличить намеренное наследование от случайного: в колоночной форме тип
стоит своей строкой и возглавляет группу имён (`int` + три параметра в
`qspi_1_4_4_sdr_read_master` — так и задумано). В ловушке новый параметр
ДОПИСАН в конец чужого списка, а между ним и типизированным соседом лежат
пустая строка и блок комментария: они создают видимость новой группы,
которой у языка нет. Именно поэтому дифф `d60d9a68` читается как безобидный.

**2. Правка не в том месте цепочки (ошибка инженера, не языка).**
Переопределение параметра обёрткой — штатная семантика Verilog: значение
берётся из САМОГО ВЕРХНЕГО модуля, который его задаёт. Я правил дефолт в
нижнем модуле (свёртка), а действовал дефолт `encoder_processing`, который
его переопределял, — правка не имела эффекта по определению. Перед правкой
пройти цепочку инстансов сверху вниз и менять значение там, где оно реально
задаётся; в нижних модулях держать нейтральный дефолт, чтобы место задания
было единственным и очевидным.

**Дешёвая проверка перед заливкой — сравнить отпечаток битстрима:**

```bash
# собрать с двумя РАЗНЫМИ значениями параметра и сравнить
sha256sum impl/pnr/<top>.bin
```

Одинаковый SHA при изменённом значении = правка НЕ влияет на логику
(перекрыта, обрезана или ветвь вырезана). Прошивать в этом состоянии
бессмысленно: железо покажет «эффекта нет», и время уйдёт на поиск
несуществующей физической причины. Тот же приём ловит и кэш сборки.

**Порядок проверки правки, дающей измеримый эффект:**
1. фокусный ТБ модуля — логика верна;
2. ДВЕ сборки с разными значениями + сравнение SHA — правка доходит;
3. по возможности сим полного тракта (реплей записи энкодера) — эффект
   виден на выходе, а не только внутри модуля;
4. только теперь железо, и первым — ЗАВЕДОМО ГИГАНТСКОЕ значение
   (для упреждения 600 мкс дало 17° сдвига): его видно сразу, и оно
   отличает «механизм не работает» от «величина не та».


## Интерфейсы Gowin: правило проектирования, а не только диагностика (07.08.2026)

Раздел про молчаливый обрыв интерфейс-портов выше был записан как ПРИЗНАК
(«ищи `Input <pin> is unused`»). Этого мало: 07.08.2026 я сам написал новый
код с чтением поля структуры сквозь интерфейс
(`if_enc_v4.ENC.rib_period`) — ровно то, от чего раздел предостерегает, —
потому что читал его как способ диагностики, а не как запрет.

ПРАВИЛО для нового кода (формулировка пользователя, 07.08.2026):
**ради одного поля не заводить в модуль весь интерфейс — разыменовать его
ПЕРЕД инстансом и передать внутрь само поле, а не интерфейс.**

```systemverilog
// ХОРОШО: разыменование прямо в порт-мапе родителя
obj_consumer obj_consumer (
    .in_rib_period(if_enc_v4.ENC.rib_period),   // внутрь идёт значение
    ...
);

// ПЛОХО: интерфейс уехал вглубь ради одного поля
obj_consumer obj_consumer (
    .if_enc_v4(if_enc_v4),                      // и чтение поля где-то внутри
    ...
);
```

Промежуточный `assign lcl_x = if_v4.ENC.x;` тоже допустим, но без нужды не
плодить локальный сигнал: короче и нагляднее разыменовать сразу в порт-мапе.

Интерфейс при этом остаётся уместным там, где им пользуются как групповым
протоколом (хоть через десять модулей верхней иерархии); разыменование
делается один раз — перед последним потребителем, которому нужно поле.
Побочная польза: место разыменования единственное и видимое — именно на нём
Gowin обрывает связь, туда и смотреть при мёртвом поведении.

Практика 07.08.2026: `rib_period` шёл в свёртку угла через интерфейс до
самого низа; переведён на разыменование у потребителя
(`ref_encoder_v4` → `ENC_1` → `angle_calculator`).

Границы применимости признака: `Input <pin> is unused` появляется только
для внешних ПИНОВ. Для внутреннего сигнала, обнулённого таким же образом,
синтез не печатает НИЧЕГО — обрыв виден лишь по мёртвому поведению на
железе. Поэтому для внутренних величин признак не работает, и проверять
надо иначе: две сборки с разными значениями + сравнение SHA битстрима
(см. раздел «Правка не доехала до железа»).

Отдельно: в той же отладке подозрение на интерфейс оказалось ЛОЖНЫМ —
после перевода на порт битстрим не изменился, а настоящей причиной был
однобитный параметр (тип, унаследованный от `bit`). Вывод для процесса:
не останавливаться на первой правдоподобной гипотезе из навыка, а
подтверждать её тем же тестом SHA до похода на железо.

Оговорка к этому опровержению: сам по себе тест «перевёл на порт — SHA не
изменился» тогда НИЧЕГО не доказывал, потому что однобитный параметр уже
обнулял всю ветвь, и оба варианта давали одинаково мёртвую схему. Порядок
обязателен: сначала снять заведомую причину (тип параметра), убедиться,
что величина двигает битстрим, и только потом A/B-тестировать способ
доставки. Иначе опровержение конфаундировано.

### Измеренная граница обрыва интерфейсов (07.08.2026, GW2A-18C)

Проверено микротопами на `run syn` (проект `C:\workspace\_probe`), по
десятку строк на вариант, чтобы вопрос решался netlist'ом, а не железом.

| Конструкция | DFF | IBUF | `Input … is unused` | Итог |
|---|---|---|---|---|
| порт интерфейса `logic ch_A`, чтение из модуля | 0 | 0 | ДА | ОБОРВАНО |
| порт интерфейса `input logic ch_A`, чтение из модуля | 1 | 2 | нет | ЖИВО |
| ЧЛЕН интерфейса `logic ch_A`, драйвится модулем изнутри | 1 | 2 | нет | ЖИВО |
| прямое чтение `if_i.ch_A` при голом порте | 0 | 0 | ДА | ОБОРВАНО |
| сквозь вложенный интерфейс, внутренний порт голый | 0 | 0 | ДА | ОБОРВАНО |
| сквозь вложенный интерфейс, внутренний порт `input` | 1 | 2 | нет | ЖИВО |
| поле структуры `if_e.ENC.rib_period` (ЧЛЕН интерфейса) | 19 | 21 | нет | ЖИВО |
| та же величина обычным выходным портом подмодуля | 19 | 21 | нет | ЖИВО |

ПРАВИЛО ОДНОЙ ФРАЗОЙ: всё, что является ЧЛЕНОМ интерфейса, синтезируется
нормально; теряется только сигнал, входящий в интерфейс через его
собственный ПОРТ БЕЗ НАПРАВЛЕНИЯ. Способ чтения роли не играет.

Это же объясняет, почему `interface_divider` работает: у него списка портов
нет вообще, все сигналы — члены.

Два последних netlist'а совпали побайтово (различалась только строка с датой
в шапке `.vg`) — для GowinSynthesis это буквально одна и та же схема.
Наглядный опыт: в топе, где ОДИН модуль читает и член интерфейса, и сигнал
сквозь голый порт, в единственной схеме первое живёт (19 REG, вход
подключён), второе свёрнуто в константу, вход помечен неиспользуемым.
Отдельно снято подозрение с вложенности: та же вложенная конструкция с
`input` во внутреннем интерфейсе работает (строка 6 таблицы), а без
направления не работает даже прямое чтение (строка 4). Вложенность в
сломанном случае лишь сопутствовала настоящей причине.

То же повторено НА БОЕВОМ МОДУЛЕ, чтобы снять возражение «микротоп не
показателен»: два синтеза `angle_calculator` целиком (ENC_1 +
`ref_encoder_v4` + ФАПЧ + свёртка), отличающиеся РОВНО одной строкой —
источником `in_rib_period` (`C:\workspace\_probe\ac`, параметр
типизирован в обоих):

| источник `in_rib_period` | DFF | LUT | ALU | реакция netlist на `LEAD_TAU_TICKS` 1650→3300 |
|---|---|---|---|---|
| обычный порт `lcl_rib_period` | 2460 | 1216 | 1728 | 308 строк |
| `{5'b0, if_lcl_enc_v4.ENC.rib_period}` | 2450 | 1228 | 1723 | 308 строк |

Реакция на параметр ОДИНАКОВАЯ — интерфейсный вариант жив ровно так же.
Разница 10 REG / 12 LUT объясняется разрядностью, а не обрывом: поле
структуры `logic[18:0]`, порт `logic[23:0]`. Потолок 19 разрядов = 524 287
тактов = 10.5 мс на ребро; на рабочих скоростях (20 000…100 000 тактов)
переполнения нет, оно возможно только ниже ~7.6 Гц кадра (разгон/выбег), где
обёрнутый период даёт большое частное и упреждение упирается в клэмп 65 535.
Перевод на 24-разрядный порт этот край снимает — правка полезная, но
лечением отказа она не была.

ВАЖНО ДЛЯ АТРИБУЦИИ: из-за этой разницы в разрядности перевод `rib_period`
на порт САМ ПО СЕБЕ меняет отпечаток битстрима. Если в одном рабочем дереве
лежат обе правки (тип параметра + способ доставки), изменившийся SHA НЕ
говорит, какая из них подействовала — он говорит только «правка влияет на
логику». Приписывать эффект конкретной правке можно лишь раздельным A/B с
одной переменной.

Тем же способом снято подозрение с `interface_divider`: A/B-синтез боевого
`angle_360_to_mirror_180` дал 259 DFF / 240 LUT через интерфейс против
260 DFF / 231 LUT на прямых портах, и netlist ОБОИХ вариантов меняется при
смене `LEAD_TAU_TICKS` (1650 → 3300: 220 и 308 различающихся строк). Если бы
`done_stb` был константой, частное стало бы ненаблюдаемым, делитель выпал бы
вместе с константой числителя, и netlist на параметр не реагировал бы.
Значит `busy`/`done_stb`, драйвимые изнутри подмодуля, живы.

Практический вывод: спорную конструкцию дешевле проверить микротопом
(`set_option -top_module <probe>` + `run syn`, секунды) и посчитать
примитивы в `.vg`, чем спорить о ней или ловить её на плате.

## Инициализатор члена интерфейса молча теряется (07.08.2026, GW2A-18C)

Измерено микротопами (`C:\workspace\_probe\minit_probe.sv`, значение A5 =
1010_0101 — если INIT доезжает, у 8 триггеров биты 0,2,5,7 получают
`INIT=1'b1`):

| конструкция | судьба инициализатора `8'hA5` |
|---|---|
| обычный регистр МОДУЛЯ + условная запись | доезжает: 4 x INIT=1'b1 + 4 x INIT=1'b0 |
| член ИНТЕРФЕЙСА + условная запись | ВЫБРОШЕН молча: 16 DFF/DFFE, ноль defparam INIT -> старт 0x00 |
| член ИНТЕРФЕЙСА без драйвера | ВЫБРОШЕН молча: читатель выметен (NL0002), все выходы GND |
| `output logic out_v = 0` (порт модуля) | игнорируется с WARN EX2478 |

Симуляция во всех случаях видит A5 — немое расхождение сим/железо, WARN
только у порта модуля.

Следствие для дефолтов конфигурации (MCU_FPGA.sv): паттерн `flag_init`
(запись дефолтов в члены if_mcu_fpga первым тактом из того же always_ff,
что и командные записи) — НЕ костыль, а единственный из двух способов,
который доезжает до железа. Опирается только на power-up 0 самого
flag_init — то, что Gowin даёт всем триггерам независимо от поддержки
INIT; после реконфигурации ПЛИС дефолты переприменяются сами. Дефолты
обязаны жить в том же процессе, что командные записи (один процедурный
драйвер у переменной).

Аудит дерева: ненулевых инициализаторов в интерфейсах два, оба в мёртвом
коде (sigma_delta_ADC — include закомментирован; interface_EthPh.EthnlntSel
= 'bz — потребитель и констрейны закомментированы). Инициализаторы `= 0` в
интерфейсах безвредны по совпадению.

Правило: дефолт, обязанный пережить синтез, — инициализатор ОБЫЧНОГО
регистра модуля, запись первого такта или reset-ветка. Инициализатор члена
интерфейса — документация для симуляции. Ненулевой инициализатор внутри
interface при ревью — повод для вопроса.

## Относительные `include` упираются в MAX_PATH — «файла нет», хотя он есть

GowinSynthesis не нормализует пути включений: он СКЛЕИВАЕТ их по цепочке.
Файл, до которого добрались через пять уровней `..`, получает путь вида
`src\main\..\TDC\lidar_measurement_pipeline\..\encoder_processing\...`, и к
нему дописывается следующий относительный include целиком. Когда сумма
переваливает за 260 символов (Windows MAX_PATH), синтез падает на
существующем файле:

```
ERROR (EX1985) : Cannot open include file
'..\..\..\error_compensation\walk_error_compensation\sync_table_mem\sync_table_mem.sv'
```

Замер на живом отказе (07.08.2026, ветка паспорта энкодера): база цепочки
178 символов, соседний include `../../../math/divider_uint_with_reminder.sv`
даёт 222 и открывается, а `../../../error_compensation/walk_error_compensation/
sync_table_mem/sync_table_mem.sv` даёт 263 и не открывается. Тот же
`sync_table_mem` из `TDC/encoder_processing/mirror_calib_lut/` подключается
без проблем — короче цепочка.

Диагностика: сложить длину пути из текста ошибки, а не искать опечатку.
Признак — ошибка «cannot open» на файле, который лежит на месте и уже
подключается из другого модуля.

Обходы, по убыванию предпочтительности:
1. подключить общий модуль ВЫШЕ по дереву (у родителя цепочка короче);
2. описать нужные три строки локально, если это тривиальная память/регистр;
3. держать глубоко вложенные модули ближе к корню `src`.

ModelSim такой цепочки не строит и компилирует нормально — расхождение
сим/синтез снова немое.
