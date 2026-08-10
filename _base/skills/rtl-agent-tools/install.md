# Установка инструментов

Читать только когда нужного бинарника нет по путям из `workflow.md`.
Ставить в `C:\workspace\tools\` — вне репозитория, в Git не коммитить.
Проверено 2026-08-08 на Windows 10 x64.

## wavepeek — запросы к VCD/FST (2.4 МБ, ~2 с)

Готовый бинарник, сборка не нужна.

- Репозиторий: <https://github.com/kleverhq/wavepeek>
- Релизы: <https://github.com/kleverhq/wavepeek/releases>
- Ассет для Windows: `wavepeek-x86_64-pc-windows-msvc.zip` (+ `.sha256`)

```powershell
$dst = 'C:\workspace\tools'
$ver = 'v2.2.0'   # актуальную версию взять из /releases/latest
curl.exe -sL -o "$dst\dl\wavepeek.zip" `
  "https://github.com/kleverhq/wavepeek/releases/download/$ver/wavepeek-x86_64-pc-windows-msvc.zip"
Expand-Archive "$dst\dl\wavepeek.zip" -DestinationPath "$dst\wavepeek" -Force
& "$dst\wavepeek\wavepeek.exe" --version
```

Контрольную сумму из соседнего `.sha256` сверять обязательно. У бинарника есть
встроенный агентский навык: `wavepeek skill`.

FSDB поддерживается только в Linux-сборке с Verdi SDK — у нас недоступен,
работаем через VCD/FST.

## slang — быстрая элаборация и линт (5.1 МБ, ~2 с)

- Репозиторий: <https://github.com/MikePopoloski/slang>
- Ассет: `slang-windows-x86_64.zip` в <https://github.com/MikePopoloski/slang/releases>

```powershell
curl.exe -sL -o 'C:\workspace\tools\dl\slang-win.zip' `
  'https://github.com/MikePopoloski/slang/releases/download/v11.0/slang-windows-x86_64.zip'
Expand-Archive 'C:\workspace\tools\dl\slang-win.zip' -DestinationPath 'C:\workspace\tools\slang' -Force
```

## slang-netlist — граф связности (готовых бинарников НЕТ, сборка ~10 мин)

- Репозиторий: <https://github.com/jameshanlon/slang-netlist>
- Документация: <https://www.jameswhanlon.com/slang-netlist/user-guide.html>

Требуется CMake ≥ 3.20, Ninja и компилятор C++20. На этой машине берём MSVC из
Visual Studio 2022 Community; slang подтягивается сборкой сам.

```powershell
git clone --depth 1 --branch v0.11.0 `
  https://github.com/jameshanlon/slang-netlist.git C:\workspace\tools\slang-netlist-src
```

Собирать из `cmd` через `vcvars64.bat` (в PowerShell окружение MSVC не
подхватится):

```bat
call "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat"
cd /d C:\workspace\tools\slang-netlist-src
cmake -B build -G Ninja -DCMAKE_BUILD_TYPE=Release -DENABLE_PY_BINDINGS=OFF -DBUILD_DOCS=OFF ^
      -DCMAKE_MAKE_PROGRAM=C:/workspace/CMake/Ninja/ninja.exe
cmake --build build -j
```

Замер: configure 2 мин, компиляция 7.5 мин (446 целей), каталог `build` 1.2 ГБ.
Результат: `build\tools\driver\slang-netlist.exe` (и `slang-report.exe`).

Python-биндинги (`-DENABLE_PY_BINDINGS=ON`) нам не нужны; для CLI выключены
ради времени сборки.

## OSS CAD Suite — vcd2fst, yosys+slang, eqy (592 МБ, ~90 с)

Нужен как минимум ради `vcd2fst`. Заодно даёт yosys 0.68, плагин `slang.so`,
eqy, sby, verilator, iverilog, gtkwave-утилиты, SMT-решатели.

- Релизы: <https://github.com/YosysHQ/oss-cad-suite-build/releases>
- Ассет: `oss-cad-suite-windows-x64-<YYYYMMDD>.tgz`

```powershell
curl.exe -sL -o 'C:\workspace\tools\dl\oss-cad-suite.tgz' `
  'https://github.com/YosysHQ/oss-cad-suite-build/releases/download/2026-08-08/oss-cad-suite-windows-x64-20260808.tgz'
tar xzf 'C:\workspace\tools\dl\oss-cad-suite.tgz' -C 'C:\workspace\tools'
```

**Бинарники не запускаются напрямую** — падают с кодом 127 без своих DLL.
Всегда через окружение:

```bat
call C:\workspace\tools\oss-cad-suite\environment.bat
yosys -V
```

Для вызова из агента удобнее держать рядом обёртку `.cmd`, которая делает
`call environment.bat`, `cd` в рабочий каталог и запускает нужный бинарь.

## Чего не ставим

- **WaveCrux** (<https://wavecrux.app/>) — десктопный GUI-вьюер. CLI и headless
  режима нет, агентский ассистент в платной версии. Для агента бесполезен:
  нужен `wavepeek`, а не вьюер. Сайт отдаёт 403 на автоматические запросы.
- **verilator** как отдельная установка — уже есть в OSS CAD Suite.
- Python-пакет `pyslang` — дублирует `slang.exe`, для наших задач не нужен.
