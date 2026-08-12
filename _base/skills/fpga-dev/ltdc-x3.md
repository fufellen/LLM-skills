# LTDC-X3 (ScioSense) — 2-канальный лидарный TDC

Справочник для работы с LTDC-X3 на плате R120M.BM2BF1X1 (D19).
Источники (изучены 2026-07-03):

- Даташит rev 2 (2025-04-09, Production): локально
  `C:\Users\User\Мой диск\Obsidian\Работа\Лидар\ВЦП TDC\TDC\LTDC-X3\LTDC-X3-Datasheet.pdf`,
  онлайн <https://www.sciosense.com/wp-content/uploads/2024/11/LTDC-X3-Datasheet.pdf>
- Dev Kit User Guide: <https://www.sciosense.com/wp-content/uploads/2025/07/LTDC-X3-Development-Kit-User-Guide.pdf>
- Evaluation software (эталонный конфиг + .NET DLL протокола):
  <https://downloads.sciosense.com/Files/LTDC-X3_Dashboard_v1.0.0.zip>
- Открытых драйверов НЕТ: github.com/sciosense не содержит LTDC-X3;
  единственный референс — `Presets/Ltdcx3.cfg` и `ScioSense.Devices.Ltdcx3.dll`
  из Dashboard-архива.

## Суть чипа

Архитектура TDC-GPX2, но старт-стоповая последовательность: init → ожидание
START → до 8 хитов на STOP (rising+falling) → INTERRUPT (низкий уровень) →
вычитка → reinit. Считает на кристалле откалиброванные разности STOP−START
(TOF) и ширину импульса (PW), 24 бита каждая. Диапазон до 16 мкс, rms 30 пс
(20 пс с HIGHRES=2). Один START, два STOP (LVDS или CMOS single-ended).
Референс-кварц 4–12.5 МГц (типично 10; на dev-kit 5 МГц). QSPI до 50 МГц
(single/dual/quad, SDR/DDR). Есть генератор триггера лазера (пин TRIGGER)
с programmable jitter.

## Подключение на R120M.BM2BF1X1

| Сигнал LTDC | Пин ПЛИС | Порт brd_ifm |
|---|---|---|
| SCK | E14 | LTDC_QSPI_SCK |
| ~SS | F14 | LTDC_QSPI_SS_N |
| D0/MOSI | E16 | LTDC_QSPI_D0 |
| D1/MISO | E15 | LTDC_QSPI_D1 |
| D2 | D16 | LTDC_QSPI_D2 |
| D3 | D15 | LTDC_QSPI_D3 |
| INTERRUPT | F15 | LTDC_INTERRUPT (низкий = данные готовы) |
| REINIT | D14 | LTDC_REINIT (импульс = перевзвод, pull-down в чипе) |
| STOPMASK | C16 | LTDC_STOPMASK (1 = стопы замаскированы, pull-down) |
| STARTP | — | от LTDC_FIRE/G14 через R109 → цепь LTDC_FIRE_AR |
| STOP1/2 P/N | — | с аналогового фронтенда (компараторы) |
| REFOSCI/REFOSCO | — | кварц или внешний LTDC_CLK через перемычки J35/J36/J37 |

MCU к LTDC не подключён — QSPI-мастер только ПЛИС.

## Опкоды SPI (mode 0 или 3, MSB first)

| Опкод | Hex | Назначение |
|---|---|---|
| power_up | 0x30 | POR-сброс, конфиг → заводские дефолты; reset держится пока SSN не уйдёт вверх |
| init | 0x18 | старт измерений с сохранением конфига; каналы откроются через 19 Tref |
| tdc_reinit | 0x19 | сброс hit-буферов, перевзвод (5 Tref); счётчики/калибровка не трогаются |
| tdc_stop | 0x20 | остановить измерение (для перезаписи конфига) |
| tdc_cal_dly1_stm | 0x21 | калибровка линии задержки stop mask (ждать 50 мс) |
| tdc_cal_dly2_tri | 0x22 | калибровка линии задержки триггера (ждать 50 мс) |
| write_config_std | 0x80 | запись: опкод + 8-бит адрес + байты (инкрементально пока SSN=0) |
| read_short_sdr | 0x60 | чтение: опкод + 8-бит адрес + байты (инкрементально) |
| read_24bit_sdr / *_ddr | 0x61/0x62/0x63 | варианты адресации/DDR |
| quad_read_short_sdr | 0x6B | quad-чтение, 8-бит адрес (нужен EN_QUAD=1 и dummy cycles) |
| quad_*_24bit_sdr/ddr | 0x6C/0x6D/0x6E | прочие quad-варианты |
| dual_read_* | 0x6F/0x70/0x71/0x72 | dual-варианты (EN_DUAL=1) |

Запись — только в стандартном 1-бит SPI; quad/dual — только чтение данных.
DDR на 50 МГц ограничен (полноценно — до 20 МГц шины).

## Последовательность запуска (даташит 7.2 + Dashboard: «Power On Reset → Write Config → Init Reset → Start»)

1. Питание стабильно → опкод `power_up 0x30`, SSN вверх (tPOR ≤ 10 мс).
2. `write_config_std 0x80` c адреса 0x00 — вся карта конфигурации одним
   инкрементальным доступом (WRN_LOCK=1 должен разрешать запись).
3. Если используется TRIGGER: `tdc_cal_dly2_tri 0x22`, ждать 50 мс.
4. Если используется внутренний stop mask: `tdc_cal_dly1_stm 0x21`, ждать 50 мс.
   Калибровки повторять при изменении температуры.
5. `init 0x18` — чип ждёт синхронизации REFCLK, +19 Tref, открывает START.
6. Цикл измерения: FIRE → START; хиты на STOP; INTERRUPT ↓ (буфер полон или
   TIMEOUT) → вычитать TOF/PW → reinit (см. ниже) → следующий цикл.
7. `DEV_STATE (0x21)`: 1 = POR отпущен, 2 = ждёт конфиг, 3 = откалиброван,
   можно измерять — удобный health-check после init.

Варианты reinit: автоматом по подъёму SSN после вычитки (SSN_INIT_ENA=1),
импульс на пин REINIT, либо опкод 0x19. Все — 5 Tref до открытия стопов.

## СКО единичного измерения (проверено на железе 15.07.2026, мишень 41 м)

Даташит Table 5 (single-shot RMS самого TDC): HIGHRES=0 — 30 пс тип./45 макс;
HIGHRES=1 (стоп меряется x2) — 25/37; HIGHRES=2 (x4) — 20/30. HIGHRES=CFG0[5:4],
§7.3.5 — повышает точность ЕДИНИЧНОГО измерения (внутренние повторные измерения
одного стопа), trade-off: pulse-pair resolution 15/30/45 нс (наши эха ~30 нс —
на грани для HIGHRES=2, работало).

Замеры системы (одиночные выстрелы, UART-телеметрия):
- база (HIGHRES=0, eval-конфиг): σ = 83 пс;
- HIGHRES=2: σ = 70–71.5 пс — **рабочий режим**;
- rev2-«магия» Production-даташита (CFG10..14=3F E0 65 DE E3, CFG15=0x27,
  ANALOG_CFG0/1=C0/4F): σ = 77 пс — ХУЖЕ eval-набора, откатили;
- walk-компенсация по интенсивности (corr(TOF,int) = −0.52…−0.57,
  b ≈ −0.88 мм/ед): резидуал 59–62 пс — поправка единичного измерения в ПО.

Бюджет σ² (по corr двух эх = 0.59): TDC 20 пс ⊕ общий джиттер START/лазерного
драйвера ~54 пс ⊕ аналог приёмника ~41 пс/канал. Проверено burst'ом: UART-
активность и темп выстрелов (20 кГц vs 285 кГц) на σ НЕ влияют, шум белый
(без дрейфа даже на окне 3.5 мс). Ниже ~60 пс — только аналоговый тракт платы.

Токи ножек (подобраны по σ, 15.07.2026): FIRE/HF1 — фронты ИЗМЕРЯЕМЫХ
сигналов (HF1→кабель 70нс→LVDS→STOP2), для них DRIVE=16 FAST — оптимум:
4мА SLOW → 82–83 пс (и int падает до ~1, ноль +82 мм); 8мА FAST → 65–70;
**16мА FAST → 61–64 (лучшее)**; 24мА → 65–71 (перегиб, звон). Остальные
выходы (UART/MSOP/LED/DBG/QSPI SCK) — 4мА SLOW (минимум SSN, даёт −2..−5 пс);
QSPI SCK 25 МГц на 4мА SLOW читается стабильно. НЕ ставить всем одинаково.

Для `intensity_to_color` значения 2500/4500 пс являются стартовыми значениями
runtime-полей `ltdc_min_intensity_ps`/`ltdc_max_intensity_ps`, а не HDL-
параметрами. Конвертер принимает их обычными входами
`in_min_intensity`/`in_max_intensity`. Источник командной записи будет определён
отдельно. Со шкалой TDC7201 (MIN=5000) интенсивность LTDC была бы всегда 0.

Burst-телеметрия (r120m_point_uart_stream, DECIM=1000): копим 1000 НЕПРЕРЫВНЫХ
выстрелов в BRAM на ~285 кГц (~3.5 мс), затем сливаем в UART (кадр 11 байт,
SEQ=индекс, сброс в 0 = граница пакета); при наборе UART молчит.

## Карта регистров (эталон из Ltdcx3.cfg Dashboard v1.0.0)

| Адрес | Имя | Eval | Расшифровка |
|---|---|---|---|
| 0x00 | CFG0 | 0x43 | SSN_INIT_ENA=1, HIGHRES=0, COMBINE=0, HIT_ENA_STOP2/1=1 |
| 0x01 | CFG1 | 0x00 | HITBUFSIZE1/2 (0 = 1 хит) |
| 0x02 | CFG2 | 0xFF | TIMEOUT=255 Tref (0=off; 2 мкс ≈ 300 м при 10 МГц: 20) |
| 0x03/0x04 | CFG3/4 | 0x00 | DELSTM_DLY[11:0] — задержка stop mask |
| 0x05..0x07 | CFG5..7 | 48 E8 01 | REFCLKDIV=0x01E848=125000; LSB=Tref/REFCLKDIV |
| 0x08 | CFG8 | 0x0C | DELSTM_LSB=3 (10/1024 Tref), DELTRIG_LSB=0, mask off |
| 0x09 | CFG9 | 0x00 | TRIG_MAX_DEL |
| 0x0A..0x0E | CFG10..14 | 9C E1 61 E1 E1 | магия; ⚠ даташит даёт 3F E0 65 DE E3 |
| 0x0F | CFG15 | 0x07 | ⚠ даташит требует 0x27 |
| 0x11 | WRN_LOCK | 0x01 | 1 = запись в функциональные регистры разрешена |
| 0x12 | ENC_SET | 0x00 | |
| 0x13 | COM_SET | 0x00 | DUMMY_CYCLE=0, TR_MODE=0 (6 байт), single SPI |
| 0x14 | CH_CFG | 0xFF | MASK_OV=1, BUFF_SIZE=15, CH_CFG=3 (оба канала), ACCMODE=1 (инкрементально) |
| 0x15..0x17 | TOF_CH1 H/M/L | RO | 24-бит TOF канала 1 |
| 0x18..0x1A | PW_CH1 H/M/L | RO | 24-бит ширина импульса канала 1 |
| 0x1B..0x1D | TOF_CH2 | RO | |
| 0x1E..0x20 | PW_CH2 | RO | |
| 0x21 | DEV_STATE | RO | 1/2/3 см. выше |
| 0x22..0x25 | TDC_STAT_REG1..4 | RO | empty/full флаги FIFO, счётчики хитов |
| 0x2A..0x2D | ANALOG_CFG0..3 | 4F 57 16 42 | ⚠ даташит: C0 4F 16 42 |
| 0x2E | ANALOG_CFG4 | 0x00 | |
| 0x2F | ANALOG_CFG5 | 0xE3 | eval: CMOS-входы; для R120M в контроллере 0x3B — см. ниже |
| 0x30..0x33 | CALIB_CFG0..3 | 0A 00 00 00 | |
| 0x3A/0x3B/0x3C | TRIG_ID/NOISE/PERIOD | 0x00 | триггер выключен |

⚠ = расхождение даташита rev 2 и эталонного конфига eval-софта; конфиг
сохранён самим Dashboard (2024-11-15) и предположительно проверен на железе
вендора — при bring-up начинать с eval-значений, расхождения перепроверить
чтением DEV_STATE/результатов.

ANALOG_CFG5 битово: 7 CMOS_STOP2, 6 CMOS_STOP1, 5 CMOS_START, 4 LVDS_STOP2,
3 LVDS_STOP1, 2 LVDS_START, 1 OSC_ENA, 0 IREF_ENA.

Ответы пользователя по железу R120M (2026-07-03):
- REFCLK: кварц 10 МГц → REFCLKDIV=100000 → LSB=1 пс (в контроллере уже так);
- START И STOP1/2 — LVDS (на R120M START тоже через LVDS-конвертер:
  LTDC_FIRE→LVDS→START) → в `ltdc_x3_spi_hdlr` ANALOG_CFG5=**0x1F**
  (LVDS_START+LVDS_STOP1/2=1, OSC_ENA=1, IREF_ENA=1). Ранее было 0x3B
  (CMOS_START) — на железе НЕ давало стартовать измерение (исправлено 2026-07-08);
- DVDD18 — от внутреннего LDO (RVDD33), внешнего 1.8 В нет.

## Результат и пересчёт

`t_stop = TOF_CHx * LSB`, `LSB = Tref_ps / REFCLKDIV`. REFCLKDIV подбирают
под удобный LSB (1/5/10 пс), он должен быть мельче собственного разрешения.
Пропавшие стопы читаются как 0xFFFFFF (при MASK_OV=1 PW маскируется 0xFFFE).
Чтение hit-буфера — FIFO: пара TOF+PW перезаряжается после вычитки пары.
TR_MODE: 0 = 3+3 байта, 1 = 2+2 (без младших байт), 2 = только TOF.
Порядок вычитки и режимы single/incremental (ACCMODE) — даташит 7.6
(готовые последовательности опкодов для всех TR_MODE).

## HDL-контроллер (симуляция ПРОЙДЕНА 2026-07-03)

- `src/TDC_LTDC_X3/ltdc_x3_spi_hdlr/ltdc_x3_spi_hdlr.sv` — обработчик
  SPI-транзакций по образцу `tdc_gpx2_spi_hdlr` (обычный SPI mode 0 через
  `SPI_Master_overhead`, в ТБ SCK ≈ 8.3 МГц). Команды: set_config
  (power_up + 4 блока конфига + контрольное чтение → cfg_error),
  init (0x18 + DEV_STATE), reinit (0x19), read_meas (12 байт с 0x15 →
  tof/pw обоих каналов + no_hit_chx при 0xFFFFFF).
- Ключевое отличие протокола от GPX2: после опкода 0x80/0x60 идёт
  ОТДЕЛЬНЫЙ байт 8-битного адреса (у GPX2 адрес зашит в опкод).
- `ltdc_x3_model.sv` — поведенческая модель чипа (SPI slave mode 0,
  регистры, измерение из реального модельного времени, TIMEOUT,
  авто-перевзвод по подъёму SSN при SSN_INIT_ENA=1). Переиспользуема
  в SoC-уровневых ТБ.
- Запуск ТБ:
  `vsim.exe -c -do "do <repo>/src/TDC_LTDC_X3/ltdc_x3_spi_hdlr/ltdc_x3_spi_hdlr_tb.do; quit -f"`.
  Пройдено: конфиг с readback, DEV_STATE=3, TOF/PW точь-в-точь при
  LSB=1 пс (660000/20000/1002000/30000), авто-перевзвод, TIMEOUT →
  0xFFFFFF + no_hit_ch2. Финальная строка: `ltdc_x3_spi_hdlr_tb PASS`.
  3 warnings — старые TFMPC в общем SPI_Master_overhead.
- Оживление на ЖЕЛЕЗЕ ПОДТВЕРЖДЕНО 2026-07-08 (bench-топ
  `R120M_ltdc_bringup_brd_ifm` + аппаратный FSM, SRAM-образ UserCode 0x2C40,
  валидация running-config через `programmer -r 0`):
  - DEV_STATE=3 (LED2 горит) + cfg_error=0 (LED3 погашен) — запись конфига и
    контрольное чтение сошлись на реальном кремнии, значит MISO чипа работает.
    FSM без ошибок (LED4 погашен), цикл измерения крутится (LED5).
  - SPI-трафик (пачки SCK/CS) виден на анализаторе X14; трафик LTDC — редкие
    короткие бёрсты (конфиг один раз после 10-мс tPOR + чтения ~1/мс), не
    непрерывный поток как MSOP → ловить ТРИГГЕРОМ на спад CS, не free-run.
  - MISO чипа СНЯТ ВЖИВУЮ на анализаторе (DSLogic, декодер SPI mode 0, MSB):
    на контрольном чтении `0x60`@`0x00` чип отдаёт ЭХО записанного конфига
    байт-в-байт (`43 00 FF 00 00 A0 86 01 0C 00 9C E1 61 …`), а на `0x60`@`0x21`
    возвращает `DEV_STATE=0x03`. Ответ приходит на dummy-байте ПОСЛЕ адреса.
    Это прямое (не косвенное по LED/cfg_error) доказательство живого MISO.
  - Пауза ~10 мс между `power_up 0x30` и `write_config 0x80` на проводе — это
    и есть tPOR (POWER_ON_DELAY=10 мс). Можно ускорить опросом DEV_STATE=1
    («POR released») вместо фиксированной задержки, но это разовый старт.
  - REFCLK: кварц 10 МГц на LTDC → REFCLKDIV=100000 → LSB=1 пс.
  - Конфиг оставлен 2-канальным (LVDS оба стопа); физически подключён только
    STOP2 → CH2, CH1 = no_hit. Лазер при bring-up выключен.
  - ПЕРВЫЙ РЕАЛЬНЫЙ TOF снят на железе 2026-07-08 (стенд с кабельной задержкой
    ~70 нс: FIRE→кабель→LVDS→STOP2): TOF_CH2=`0x013466`=78950 (LSB=1пс → 78.95 нс,
    сходится с ~70 нс + оффсеты чипа/LVDS), PW_CH2 ненулевой; TOF_CH1=FFFFFF
    (STOP1 не подключён). Понадобилось ДВА фикса, которых сим не ловит:
    1. ANALOG_CFG5 `0x3B → 0x1F` (all-LVDS): и START, и STOP на R120M приходят на
       чип как LVDS. CMOS_START не давал стартовать измерение.
    2. Драйвить ВЧ-выходы `FPGA_HF1/HF2` (K12/K13) = FIRE — на стенде это ИСТОЧНИК
       STOP. В bench-топе их надо ЯВНО объявить и завести на fire, иначе пин, к
       которому подключён STOP-кабель, висит без сигнала → сплошной no_hit.
  - Диагностика без осциллографа: UART-репортер шлёт fire_cnt/int_cnt. Если
    int_cnt≈fire_cnt — чип стартует и завершает измерение прерыванием каждый цикл
    (START работает), а сплошной no_hit при этом = проблема на ВХОДЕ STOP.
  - ИНТЕГРАЦИЯ LTDC->MSOP ПОДТВЕРЖДЕНА НА ЖЕЛЕЗЕ 2026-07-08 (топ
    `R120M_ltdc_msop_brd_ifm`, SRAM UserCode 0x3C29): измерение LTDC -> TOF_to_DST
    (пс->мм, dst=TOF*0.149896) + intensity_to_color -> точка -> msop_tcp_pack_filler
    -> MSOP_TCP_SPI_sender -> пины MSOP SPI (R6/T5/R5). На анализаторе снят
    БАЙТ-В-БАЙТ кадр: `FF FE` head (point_count=0x5A=90, angle_res=0x00C8=200,
    dist_byte=2, intensity_flag=1, echo=first), 90 точек `dist(LE 2Б) + int(1Б)`
    = `XX 2E FF` (dst≈0x2E1X≈11.8м на кабеле ~78.7нс, int=FF), tail `FF 9B`, 1 CS/
    кадр, SCK 25 МГц. Боевой TDC7201-MSOP (lidar_measurement_pipeline) при этом не трогали.
    Ключ: MSOP-цепочка generic — свой фронт-энд (LTDC->dst/color) вместо
    tdc_processing, дальше pack_filler+sender без изменений.
  - 2 ЭХА (мульти-хит) 2026-07-08: контроллер параметризован `HITS_PER_CHANNEL`
    (1..8, масштаб до 8 хитов/канал в одном месте); CFG1 HITBUFSIZE=N-1, читаем 12*N
    байт одной инкрементальной транзакцией (ACCMODE=1, §7.6.1). В MSOP: echo_mode=3
    (first+last), echo_count=2, точка = dist1+int1+dist2+int2 (6 байт). ⚠ Багфикс
    в ОБЩЕМ sender'е: `body_bytes_per_point_from_head` НЕ учитывал echo_count →
    6-байтовую точку реверс трактовал как две 3-байтовые (эхо переставлялись);
    + body_builder ранее echo-2 вообще не выкладывал. Сим PASS байт-в-байт;
    на железе кадр верный (point_count=90, echo_count=2, 6Б/точка), эхо-1 реальный
    (~0x2E0X≈11.8м), эхо-2=0xFFFF — на стенде нет 2-го фронта на STOP2 (переотражение
    кабеля не доходит; прошивка примет, как только он появится). UART: d=эхо-1,
    c=эхо-2 (COM4 @115200).
  - Контракт 2 ЭХА уточнён 2026-07-29: `HITS_PER_CHANNEL` — число сырых хитов
    в каждом физическом канале, а не число логических эхо на выходе. В боевом
    `CHANNEL_COMBINE` значение `HITS_PER_CHANNEL=1` даёт два логических эха:
    `echo1=ch1[0]`, `echo2=ch2[0]`. Нельзя выставлять `HITS_PER_CHANNEL=2` только
    ради двух выходных эхо: это запрос двух хитов в каждом канале, то есть четырёх
    сырых результатов и 24-байтной вычитки; такой режим требует отдельного контракта
    обработки данных.
  - Приёмка двухэхового LTDC-тракта обязана проверять в TB не значение параметра
    hit-буфера, а `echo_mode=3`, `echo_count=2` в MSOP и две разные выходные
    дистанции. Эталон 2026-07-29: handler TB — `660000/800000 ps`; полный
    `R120M_BM2BF1X1_ltdc_tb` — `44968/89937 mm`, два пакета по 2006 байт,
    509 поджигов / 509 прерываний.
  - Каждый логический echo имеет собственную пару `TOF/PW`. Для
    `HITS_PER_CHANNEL=1` активная 12-байтная карта результата:
    `0..2=TOF1`, `3..5=PW1`, `6..8=TOF2`, `9..11=PW2`.
    `ltdc_measurement_engine` обязан декодировать и защёлкивать все четыре
    значения, а `ltdc_point_builder` — преобразовывать оба PW через одно
    runtime-окно порогов. Один экземпляр `intensity_to_color` обслуживает их
    последовательно; PW2 и пороги защёлкиваются на всю транзакцию, а состояние
    явно связывает каждый результат с его echo. В MSOP `intensity1` и
    `intensity2` являются настоящими 8-битными результатами этих двух
    преобразований. Номер зеркала хранится отдельным состоянием ассоциации
    точки и не занимает биты `intensity2`.
  - Регрессия этого контракта должна задавать различающиеся PW обоих эх и менять
    номер зеркала независимо. До исправления полный TB при `PW1=5000 ps`,
    `PW2=20000 ps` и окне `6000..19000 ps` воспроизводил
    `intensity1=0, intensity2=0` вместо ожидаемого `0/255`. После коммита
    `564f4afc` focused point-builder/MSOP TB, полный LTDC TB и command-SPI TB
    прошли с `Errors=0`; полный тракт выдал два пакета по 2006 байт,
    `44968/89937 mm`, `intensity1=0`, `intensity2=255` и
    509 поджигов / 509 прерываний.
  - Коммит `4664450f` разделяет один `intensity_to_color` между обоими эхами.
    Свежий PnR активного top: UserCode `0x0000D9CB`, setup/hold `0/0`, Fmax
    `74.810 MHz` при `50 MHz`, logic `10704`, registers `9920`, BSRAM `56%`,
    все 101 pin constraints. Против прямого дублирования конвертера это
    `-523` logic, `-208` registers и `+19.289 MHz` Fmax. Железо не прошивалось.
    В MSOP по-прежнему передаётся масштабированная 8-битная intensity; передача
    сырого 24-битного PW этим изменением не реализована.

## План bring-up на R120M (ПЛИС-мастер)

1. Обычный 1-бит SPI ≤10 МГц, mode 0. power_up → write config (эталонные
   значения) → read-back конфигурации опкодом 0x60 с адреса 0x00 —
   первое hardware-доказательство живого чипа.
2. DEV_STATE=3 после init 0x18.
3. Одиночное измерение: FIRE (импульс ≥5 нс CMOS) → INTERRUPT ↓ →
   вычитка TOF_CH1/PW_CH1 → tdc_reinit.
4. Потом ускорять: quad SDR (EN_QUAD=1, DUMMY_CYCLE=1), TR_MODE по нужде.
5. STOPMASK/REINIT с пинов ПЛИС — уже разведены (C16/D14).

## Архитектурный принцип: FIRE — свободный такт, ВЦП декуплированы

Ключевая модель боевого измерительного тракта (проверено на bring-up 2026-07-08):

**FIRE (START/лазер) — единый свободнобегущий такт всей системы.** Он НЕ гейтится
ни на одном ВЦП: ни на инициализации, ни на подключении, ни на «здоровье» модуля.
Лазер стреляет по своему расписанию всегда. Система не имеет права ждать всех
модулей перед стартом измерений или тормозить FIRE/остальные каналы, если один
ВЦП отвалился или не поднялся.

Каждый ВЦП **живёт своей жизнью**: после собственной инициализации его задача —
«встать в строй» и начать защёлкивать измерения по общему FIRE. Модулей может быть
до **8** (смесь TDC7201 / LTDC-X3). Отвалившийся/неинициализированный ВЦП просто не
даёт валидных данных (no_hit / stale / флаг «не готов»), но НЕ блокирует FIRE и
соседей. Агрегатор кадра читает у каждого модуля его последний результат
асинхронно и помечает отсутствующие — не ждёт их.

Следствия для RTL:
- Генератор FIRE — отдельный независимый таймер/счётчик, ВНЕ FSM любого ВЦП.
- Контроллер каждого ВЦП: собственный init-FSM + защёлка результата по общему
  FIRE/INTERRUPT; публикует пару {результат, valid/alive}.
- Слой сбора кадра — неблокирующее per-модуль чтение; дырки → флаг, а не стоп.
- Health/init/reinit модуля — фоново и самовосстанавливаемо (reinit по SSN),
  НЕ на критическом пути FIRE.

Контраст с bring-up FSM: секвенсер `R120M_ltdc_bringup_brd_ifm` намеренно
ПОСЛЕДОВАТЕЛЬНЫЙ (config → init → FIRE → wait → read → delay), FIRE идёт после
init — это удобно для оживления ОДНОГО чипа и проверки тракта. Для боевой
N-канальной системы модель другая: FIRE свободный, ВЦП декуплированы (этот раздел).

## LTDC в БОЕВОМ тракте лидара (ltdc_processing, ветка R120M.BF2)

`src/TDC_LTDC_X3/ltdc_processing/ltdc_processing.sv` — замена `tdc_processing`
(2×TDC7201) с тем же контрактом наружу: `dst`/`dst_cmp`/`color`/`pulse_width`
плюс `if_ldr_cdtr.tdc_data_ready`. Всё остальное в `lidar_measurement_pipeline` (энкодер, углы,
зеркала, кадры, команды МК, MSOP по SPI2) от типа ВЦП не зависит — шов чистый.

Отличие от стендового топа `R120M_ltdc_msop_brd_ifm`: выстрелами управляет
`lidar_conductor`, а не свободнобегущий FSM. Цикл на выстрел:

1. `ndl_make_fire_prep` → перевзвод пином REINIT (4 такта) + re-arm ~500 нс
   (окно подготовки конductor'а 1.9 мкс — укладывается);
2. `fire` (STARTP чипа заведён с `LTDC_FIRE` в прослойке платы);
3. спад INTERRUPT либо таймаут 8 мкс (watchdog конductor'а 10 мкс, TIMEOUT чипа
   CFG2 = 10 Tref = 1 мкс — INT приходит заведомо раньше);
4. quad-чтение 0x6B (12 байт) → защёлка → `tdc_data_ready`;
5. TOF→DST и PW→intensity на оба эха CHANNEL_COMBINE.

Соглашение боевого тракта: «нет эха» отдаётся дистанцией **0** (как в тракте
TDC7201, где TOF=0 даёт dst=0), НЕ 0xFFFFFF — ПО такую точку не рисует.

Выбор источника — параметр `USE_LTDC` в `lidar_measurement_pipeline`/`main`/прослойке платы
(1 = LTDC, линия `R120M.BF2`; 0 = прежний тракт 2×TDC7201). При `USE_LTDC=1`
интерфейсы TDC7201 держатся в покое (`TDC_EN=0`), а шина LTDC уходит на пины.

ВАЖНО: при активном LTDC UART-репортёр уводится с `DBG_E2` на `X1/FPGA_TX`
(M11), а E2 держится статично — поток на E2 наводит помеху на шину LTDC
(см. раздел про богус-измерение).

Проверка в ModelSim 10.5b: `src/main/R120M_BM2BF1X1_ltdc_tb.sv` — модель чипа на
шине, эхо 300 нс после поджига → 44968 мм при расчётных 44969, 2 валидных
MSOP-кадра, сниффер прослойки сошёлся с независимым декодером ТБ.

## Runtime-поля порогов интенсивности (рефакторинг 2026-07-29)

- Пороги называются `ltdc_min_intensity_ps` и `ltdc_max_intensity_ps`; стартовые
  значения `2500/4500 пс` сохраняют прежнее поведение. Источник командной записи
  пока намеренно не реализован: не выдумывать для него адрес до отдельного
  решения по карте команд.
- В активном тракте поля принадлежат `interface_MCU_FPGA`, и `MCU_FPGA` задаёт
  их стартовые значения. Далее обычные сигналы проходят по цепочке
  `lidar_measurement_pipeline` → `ltdc_processing` → `ltdc_point_builder` →
  `intensity_to_color`; в `R120M_BM2BF1X1_brd_ifm` и `main` пороговых
  параметров больше нет.
- В standalone-топе `R120M_ltdc_msop_brd_ifm` локальные runtime-поля поданы
  обоим экземплярам `intensity_to_color`, для эхо-1 и эхо-2. Пока реальный
  источник записи не подключён, Gowin закономерно сворачивает их в стартовые
  константы; такой bitstream ещё не доказывает изменение порогов на железе.
- `intensity_to_color` фиксирует интенсивность и оба порога одной транзакции
  перед интерполяцией, поэтому смена поля во время вычисления не смешивает два
  разных окна.
- Приёмочный TB обязан менять поля в одном уже элаборированном DUT и проверять
  функциональный результат. Проверено: `intensity_to_color_tb` меняет окно
  `4000..6000` → `100000..200000` → `0..1` и получает для `PW=5000`
  соответственно `127` → `0` → `255`; `ltdc_point_builder_tb` подтверждает
  `127` → `0`; standalone MSOP TB после опустошения переходной очереди
  подтверждает для обоих эхо `0` → `255`. Полный активный TB принял два
  2006-байтовых MSOP-пакета с интенсивностью 0 при runtime-окне
  `100000..200000`.
- PnR после коммита `7712b47e` завершён с setup/hold `0/0`. Активный
  `R120M_BM2BF1X1`: UserCode `0x0000F5D8`, Fmax `63.596 MHz` при `50 MHz`,
  logic `10805`, registers `9783`. Standalone `R120M_LTDC_MSOP`: UserCode
  `0x00006C5A`, Fmax `106.839 MHz`, logic `2905`, registers `2084`.

## Ширина эха: признак ложного отклика (осциллограф 22.07.2026)

На LVDS-паре STOP реальное эхо узкое — PW ≈ 4–5 нс. Ложный отклик заметно
ШИРЕ: на снимке 22.07.2026 второе эхо имело PW ≈ 40 нс (разнос 74.5 нс).
Нормальная пара эх выглядит иначе: оба импульса узкие, разнос ≈ 10 нс.

Следствие для HIGHRES: pulse-pair resolution 15/30/45 нс для HIGHRES 0/1/2.
Пара с разносом ~10 нс при HIGHRES=2 (45 нс) не разделяется вовсе, поэтому в
`ltdc_processing` по умолчанию **HIGHRES=0** (σ единичного 83 пс против 70 пс —
для картинки это ~12 мм, приемлемо). Отбраковку по ширине в ПЛИС НЕ делаем
(решение 22.07.2026): что чип выдал, то и уходит в кадр; `PW` уже передаётся как
интенсивность, и порог при необходимости ставится в ПО.

## Детектор спада LTDC_INTERRUPT (рефакторинг 2026-07-29)

Спад `LTDC_INTERRUPT` в боевом `ltdc_measurement_engine` и в standalone-топах
`R120M_ltdc_bringup_brd_ifm` / `R120M_ltdc_msop_brd_ifm` детектируется общим
`src/edge_detector/edge_detector.sv` с `is_fast=1`, а не локальной конструкцией
`int_q && !interrupt`. Не возвращать частную копию: перед созданием небольшого
helper-блока сначала искать и проверять готовые модули проекта. При замене
учитывать дополнительное синхронное семплирование и задержку выбранного режима.

Эталон приёмки после замены: bring-up TB — `TOF=600000 ps`, `PW=30000 ps`;
standalone MSOP TB — 38 корректных двухэховых кадров и восстановление после
принудительного illegal state; полный `R120M_BM2BF1X1_ltdc_tb` — 509 поджигов /
509 спадов прерывания, два пакета по 2006 байт, дистанции `44968/89937 mm`.
PnR: UserCode `0x0000ECC4`, setup/hold `0/0`, Fmax `62.242 MHz` при ограничении
50 MHz, logic `10829`, registers `9756`. Относительно предыдущего результата:
`+136` logic, `+1` register, `-0.900 MHz`; это стандартизация и повторное
использование кода, а не оптимизация площади или частоты.

## Типизация LTDC FSM (рефакторинг 2026-07-29)

Все затронутые LTDC-FSM должны объявлять состояния через
`typedef enum { ... } state_t` без явного базового типа и размерности, а регистр
состояния — как `state_t`, не как безымянный битовый вектор. Боевая FSM
`ltdc_measurement_engine` уже соответствует этому контракту. Standalone-FSM
в `R120M_ltdc_bringup_brd_ifm` и `R120M_ltdc_msop_brd_ifm` приведены к нему
с сохранением прежних явных кодов состояний, включая пропуск кода в bring-up.

Приёмка: bring-up TB — `PASS`, `DEV_STATE=3`, `TOF=600000 ps`,
`PW=30000 ps`; standalone MSOP TB — `PASS`, 38 корректных двухэховых кадров
и восстановление после 1301 измерения. Gowin build обоих standalone-топов
завершил bitstream с setup/hold `0/0`: bring-up — Fmax `103.945 MHz`,
logic `918`, registers `537`; MSOP — Fmax `110.274 MHz`, logic `2891`,
registers `2031` при рабочей частоте 50 MHz. Первый MSOP PnR также выявил
устаревшие constraints удалённого порта `FPGA_TX2`; они удалены из
`R120M_ltdc_msop.cst`, после чего physical constraints и PnR прошли.

## LTDC QSPI master internals (verified 2026-07-29)

`qspi_1_4_4_sdr_read_master` uses directional public signal names
`in_*`/`out_*`, local connections `lcl_*`, instances `obj_*`, and a typed
`state_t` FSM. Size its phase counter for the longest opcode, address, dummy,
or data phase across every legal value of `COMMAND`, `DUMMY_CYCLE_COUNT`,
`CLOCK_DIVIDER`, and `BYTE_COUNT`. Illegal-state recovery must return the FSM
to idle and release QSPI ownership in the same branch: clear `busy`, deactivate
`SS_n`, stop SCK, and clear output-enable.

The focused
`src/SPI/QSPI/qspi_1_4_4_sdr_read_master/qspi_1_4_4_sdr_read_master_tb.do`
checks command `0x6B` MSB-first on one lane, quad address order, DQ release
during dummy/data, returned byte order, exact SCK cycle/divider behavior,
one-cycle `valid`, reset during a transaction, and illegal-state recovery.
ModelSim 10.5 cannot reliably force a hierarchical enum through a TB type cast;
force the individual `lcl_state[N]` bits and release the complete `lcl_state`.

Упаковка `lcl_data_bytes[0:BYTE_COUNT-1]` в `out_read_data`, где байт `k`
занимает `[k*8 +: 8]`, выполняется как `{<<8{lcl_data_bytes}}`: направление
`<<` разворачивает поток блоками по 8 бит и помещает элемент 0 в младший байт.
Приёмка коммита `b78aeb17`: focused TB и 12-байтовый standalone MSOP TB —
`PASS`; GowinSynthesis/PnR приняли streaming по unpacked-массиву, а UserCode
`0x0000F3C3`, ресурсы и Fmax совпали с предыдущим образом.

## LTDC QSPI transport split (2026-07-29)

`quad_read_short_sdr` (`0x6B`) is not a complete universal QSPI standard. The
verified LTDC-X3 wire contract is mode-0 `1-4-4 SDR`: an 8-bit command is sent
MSB-first on DQ0, an 8-bit register address is sent as two quad nibbles, the
master releases DQ during the configured dummy cycles, and payload nibbles are
sampled on all four lanes. `EN_QUAD` and the matching dummy-cycle setting remain
part of LTDC device configuration.

The reusable wire engine is
`src/SPI/QSPI/qspi_1_4_4_sdr_read_master/qspi_1_4_4_sdr_read_master.sv`.
It owns SCK/SS, DQ output-enable, the typed FSM, byte capture, reset, and safe
illegal-state recovery. Its deliberately narrow public contract has a
parameterized fixed `COMMAND`, an 8-bit address, dummy count, clock divider, and
byte count. Bind `COMMAND=8'h6B` directly in `ltdc_measurement_engine` and
`R120M_ltdc_msop_brd_ifm`; both use register address `8'h15`. Do not restore a
pass-through LTDC wrapper only to bind these constants or rename ports. Do not
add runtime command selection or wider addresses until an active consumer and
its protocol TB require them.

The transport TB proves the reusable wire contract. The standalone MSOP and
full active integration TBs prove the LTDC command/address binding and both
returned echoes. Do not retain a wrapper-only TB after deleting a wrapper that
has no independent behavior.

The first generalized draft passed simulation but cost 52 LUT instead of the
original 48 LUT; a shift-register address experiment also raised the full
design to 10839 logic / 9760 registers. The accepted narrow core synthesizes to
exactly 48 LUT / 14 DFF.

Commit `d7fa85e4` removed the zero-behavior LTDC wrapper and its wrapper-only
TB. Acceptance: transport TB and `ltdc_x3_spi_hdlr_tb` passed with zero errors;
standalone MSOP passed with 38 good two-echo frames and illegal-state recovery;
full `R120M_BM2BF1X1_ltdc_tb` passed with 509 fires / 509 interrupt falls, two
2006-byte packets, and distances `44968/89937 mm`. Fresh Gowin PnR was
bit-identical to the pre-removal build. `R120M_BM2BF1X1`: UserCode
`0x0000F5D8`, Fmax `63.596 MHz` at 50 MHz, logic `10805`, registers `9783`,
BSRAM `56%`, setup/hold `0/0`. `R120M_LTDC_MSOP`: UserCode `0x00006C5A`,
Fmax `106.839 MHz`, logic `2905`, registers `2084`, BSRAM `34%`, setup/hold
`0/0`. No hardware was programmed.
