# RTL agent tools — прямой запрос вместо косвенной отладки

Три инструмента, которые заменяют дорогие обходные пути: перезапуск симуляции
ради ещё одного `$display`, цепочки `grep` по иерархии, ручную проверку «а не
сломал ли я поведение». Все проверены на лидарном проекте 2026-08-08 — числа и
проектные особенности в `../fpga-dev/agent-tooling.md`.

Бинарники живут вне репозитория, по умолчанию `C:\workspace\tools\`:

| Инструмент | Путь | Если нет |
|---|---|---|
| `wavepeek.exe` | `C:\workspace\tools\wavepeek\` | `install.md` |
| `slang.exe` | `C:\workspace\tools\slang\` | `install.md` |
| `slang-netlist.exe` | `C:\workspace\tools\slang-netlist-src\build\tools\driver\` | `install.md` (сборка ~10 мин) |
| `vcd2fst`, `yosys`, `eqy` | `C:\workspace\tools\oss-cad-suite\bin\` | `install.md` |

Читай `install.md` только когда нужного бинарника нет на месте.

## 1. Вопрос к волнограмме вместо перезапуска симуляции

Признак, что пора сюда: нужен ещё один внутренний сигнал, и рука тянется
дописать `$display` и пересимулировать.

Снять дамп один раз (в `.do` тестбенча, перед `run -all`):

```tcl
vcd file C:/path/dump.vcd
vcd add -r /<tb>/*
run -all
vcd flush
```

**Сразу конвертировать в FST** — 26× по диску, 10× по скорости запросов:

```powershell
& 'C:\workspace\tools\oss-cad-suite\environment.bat'   # даёт PATH к vcd2fst
vcd2fst -v dump.vcd -f dump.fst
```

Дальше спрашивать, а не читать. Дамп в контекст не втягивать никогда:

```powershell
$WP = 'C:\workspace\tools\wavepeek\wavepeek.exe'
& $WP info   --waves dump.fst --json
& $WP scope  --waves dump.fst --filter '.*<модуль>.*' --max 20
& $WP signal --waves dump.fst --scope <SCOPE> --max 60
& $WP change --waves dump.fst --scope <SCOPE> --signals <sig> `
             --on '*' --sample-mode native --from 5800000ns --max 20
```

- `--on '*'` требует `--sample-mode native`; `pre-edge` (по умолчанию) работает
  только с `posedge`/`negedge`/`edge`.
- Для синхронной логики правильная модель — `--on "posedge <clk>" --eval "<условие>"`.
- Встроенные `extract` есть только для AHB/APB/ATB. SPI/QSPI/RMII декодировать
  вручную: `change --on "posedge <sck>"` по MOSI, байты собирать самому.
- Не смешивать `--scope top.cpu` и полные пути в одном запросе.
- Точный синтаксис — у самого бинарника: `wavepeek help <команда>`,
  `wavepeek docs show commands/<команда>`, `wavepeek skill`.

## 2. Структурный вопрос вместо цепочки grep

Признак: «куда идёт этот сигнал», «кто это драйвит», «через какие интерфейсы
проходит». Одна команда вместо 5–6 `grep` и ~80× меньше выдачи в контекст.

```powershell
$NL = 'C:\workspace\tools\slang-netlist-src\build\tools\driver\slang-netlist.exe'
$F  = '--std 1800-2017 --timescale 1ns/1ps --top <top> --allow-use-before-declare',
      '-Wno-multiple-always-assigns -Wno-mixed-var-assigns --error-limit 0'

& $NL @F -I . -I .. <top>.sv --drivers  <top>.<путь>.<сигнал>   # кто драйвит, побитно
& $NL @F -I . -I .. <top>.sv --fan-out  <top>.<путь>.<пин>      # куда уходит
& $NL @F -I . -I .. <top>.sv --find     '**.*<фрагмент>*'       # найти узел
& $NL @F -I . -I .. <top>.sv --report-registers --comb-loops
```

- Запускать из каталога топа: относительные `` `include `` резолвятся от файла.
- Warning'и сыплются в stderr и топят выдачу — писать таблицу через `-o файл`
  и глушить `2>$null`.
- **`--from/--to` ищет только комбинационные пути.** Между пином протокола и
  регистром честно вернёт `no path`, потому что путь пересекает регистры.
  Многотактовый тракт собирать по шагам через `--drivers`/`--fan-out`.

Быстрый линт/элаборация без симулятора (секунды против минут синтеза):

```powershell
& 'C:\workspace\tools\slang\slang.exe' --std 1800-2017 --timescale 1ns/1ps `
    --top <top> --error-limit 0 -I . -I .. <top>.sv
```

## 3. Доказать, что правка не изменила поведение

Признак: правка по линту, переименование, реструктуризация — поведение меняться
не должно, а тестбенч это докажет только частично.

```
# check.eqy
[gold]
plugin -i slang
read_slang --allow-use-before-declare --top <mod> gold.sv
prep -top <mod> -flatten

[gate]
plugin -i slang
read_slang --allow-use-before-declare --top <mod> new.sv
prep -top <mod> -flatten

[strategy sat]
use sat
depth 10
```

Запускать через `environment.bat`, затем `eqy -f check.eqy`.

- Штатный фронтенд yosys наш SystemVerilog не читает (падает на
  `type`-параметрах) — только `-m slang` / `read_slang`.
- **`eqy` на Windows врёт в итоге:** печатает `DONE (FAIL)`, даже когда все
  партиции прошли — сводка не может прочитать свои же файлы статусов. Верить
  только им: `Get-Content <run>\strategies\*\sat\status`.
- Партиции локализуют изменение: при реальной функциональной правке падают
  ровно затронутые выходы, остальные остаются PASS.

## Когда эти инструменты не помогут

Они отвечают на вопросы о связности, о значениях в дампе и об эквивалентности
двух версий RTL. Они ничего не говорят о том, правильно ли поведение по
физике — калибровки, геометрия, эталон на стенде. Там доказательство только
железное; см. правила эвиденса в `../fpga-dev/workflow.md`.
