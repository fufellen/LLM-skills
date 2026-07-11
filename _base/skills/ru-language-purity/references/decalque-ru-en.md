# RU De-Calque Checklist (естественный русский научный текст)

Read this BEFORE writing or editing Russian manuscript prose, and run the
full pass whenever the Russian text is (or descends from) a translation of
an English draft - especially an AI-generated one. Written imperatively so
any model, including weaker ones, can apply it without judgment calls.

## Strategic rules (apply first, they beat word-by-word fixes)

1. **Rewrite from facts, not from sentences.** If the RU text is a
   translation of an (AI-written) EN draft, do NOT polish it sentence by
   sentence - the polish inherits the source's defects. Rewrite each
   section from the validated facts, data files, and results; use the EN
   source only as a coverage plan ("what must be mentioned"), not as a
   text template.
2. **Resolve sense against the source.** For every awkward RU phrase,
   find the EN original, identify which SENSE of the English word is
   meant in this domain, then choose the natural Russian for that sense -
   never the first dictionary equivalent. (Example: for phase-change
   materials, "programming" means writing a state, not писание кода.)
3. **Existence test for coined words.** Before using a coined compound
   adjective or an imported metaphor, verify the exact word is actually
   used in real Russian scientific literature. If you cannot recall real
   usage, DO NOT invent it - rephrase with normal syntax (prepositional
   phrase, verb, or two words).
4. **History is not edited.** Apply fixes to the manuscript body,
   captions, and titles; never rewrite edit logs, checkpoints, or
   rejected-alternatives lists.
5. **Bulk fixes are count-asserted.** More than ~3 occurrences - replace
   by a script that asserts the expected occurrence count per file and
   verifies zero leftovers, then rebuild artifacts and re-verify inside
   the built DOCX/PDF text.
6. **Согласуй определения с расшифровкой аббревиатуры по числу и роду.**
   Аббревиатура наследует грамматику своей расшифровки. Если в тексте
   введено «плазмонные наночастицы (ПНЧ)» (мн. ч.), то дальше только
   «золотых ПНЧ», «этих ПНЧ» - НЕ «золотой ПНЧ». Проверяй все определения
   перед аббревиатурой грепом по шаблону «(прилагательное в ед. ч.) +
   АББР» и сверяй с тем, как аббревиатура раскрыта при первом упоминании.
   Если нужен единственный объект - пиши слово полностью
   («проницаемость наночастицы»), а не аббревиатуру
   (explicit user correction, 2026-07-09).
7. **Убирай слова-филлеры и книжные обороты (заумность).** Если
   прилагательное можно убрать без потери смысла («тщательный компромисс»
   -> «компромисс») - это слово ради слова, убирай. Если оборот звучит
   по-книжному сложнее самой мысли («отвечает пределу бесконечной
   ширины», «обосновывают схему проектирования с учетом областей
   неприменимости») - перепиши простым глаголом и существительным
   («описывает бесконечно широкую структуру», «определяют границы
   применимости»). Признак ставь при действии, а не при предмете:
   «инструмент для быстрого предварительного отбора», а не «быстрый
   инструмент предварительного отбора»; предмет не может БЫТЬ действием:
   «модель для быстрого отбора», а не «модель как быстрый отбор»
   (explicit user corrections, 2026-07-09).
8. **Раскрывай сжатые формулировки через наблюдаемый или рассчитанный
   результат.** В аннотации и выводах не заменяй физический смысл
   неопределёнными ярлыками вроде «тонкое ранжирование», «явный лидер»,
   «фазовый контраст» или «направление фазовой перестройки». Пиши, что
   именно показывает расчёт: «порядок близких вариантов может меняться»,
   «знак изменения действительной части эффективного показателя» или
   «материал с наименьшей длиной фазового сдвига». Установившийся термин
   допустим, но если без отдельного пояснения он непонятен целевой
   аудитории, раскрой его физический смысл: например, вместо перечисления
   «вытекающих мод» напиши о проверке удержания поля в волноводе или об
   излучении энергии в окружающую среду; вместо «окончательного выбора
   модовой ветви» - о подтверждении того, что при изменении параметра
   сравнивается одна и та же физическая мода (explicit user corrections,
   2026-07-11).
9. **Считай вопрос о значении фразы сигналом к правке рукописи.** Если при
   редактировании статьи пользователь спрашивает «что такое X?» или «что
   здесь значит X?», не ограничивайся ответом в чате. Объясни термин,
   проверь исходное место и в той же задаче перепиши его через физический
   смысл, если формулировка неочевидна без отдельного пояснения. Например,
   вместо «широкозонные фазоизменяемые материалы» укажи, что у материалов
   шире запрещённая зона и поэтому мало межзонное поглощение на рабочей
   длине волны. Сохраняй специальный термин только там, где он определён
   или нужен как ключевое слово (explicit user correction, 2026-07-11).
10. **После введения сокращения пользуйся им последовательно.** В пределах
   самостоятельной части текста сначала дай полное название и сокращение в
   скобках, затем используй сокращение, не чередуя его без причины с полным
   названием или синонимами. Для частей, которые читаются отдельно,
   сокращение вводи заново по требованиям издания: в статье IEEE аннотация
   и основной текст являются отдельными областями. Если термин встречается
   только один раз, не вводи лишнее сокращение. Заголовок, ключевые слова и
   подписи проверяй отдельно по правилам издания (explicit user correction,
   2026-07-11).
11. **Не придумывай научную терминологию.** Перед переводом специального
   термина сначала проверь `verified-russian-terminology.md`. Если записи
   нет, ищи точную русскую форму в русскоязычных научных источниках в
   интернете и проверяй употребление по полному тексту, а не по поисковому
   фрагменту или машинному переводу. Подтверждённую форму сразу занеси в
   реестр вместе с английским соответствием, сокращением, источником и
   датой проверки. Если форма не подтверждена, не создавай буквальную
   кальку: сохрани международное обозначение, при первом упоминании дай
   английское раскрытие и объясни термин обычной русской фразой. Отрицательный
   результат тоже занеси в реестр, чтобы не повторять тот же поиск без новой
   причины (explicit user correction, 2026-07-11).

## Class 1 - false friends and wrong-sense translations

The Russian word exists, but it renders the wrong sense of the English one.

| English source | Calque (wrong) | Natural Russian |
| --- | --- | --- |
| careful balance / careful trade-off | аккуратный баланс; тщательный компромисс | компромисс (прилагательное не переводить - слово ради слова) |
| balance / trade-off between X and Y | баланс между | компромисс между X и Y |
| the design must balance X and Y | конструкция должна балансировать X и Y | геометрия должна давать X и удерживать малым Y (переформулировать) |
| roadmap (papers) | программные работы | дорожные карты; обзорные работы |
| fast screening tool | быстрый инструмент предварительного отбора | инструмент для быстрого предварительного отбора |
| multilevel programming (PCM) | многоуровневое программирование | запись нескольких промежуточных состояний |
| actual | актуальный | фактический, реальный |
| performance | перформанс | характеристики, показатели работы |
| robust (outside statistics) | робастный | устойчивый, надежный |
| in terms of X | в терминах X | в пересчете на X; по X |
| candidates (design variants) | кандидаты | варианты |
| aggressive (design/estimate) | агрессивный | жесткий, завышенный, интенсивный |
| signature (of a shift / an effect) | подпись (сдвига) | признак, характерный признак |
| bleaching (of absorption) | выцветание; выцветает | просветление; ослабевает, уменьшается |
| time traces (pump-probe) | временные трассы | временные зависимости |
| preserve material ranking (model comparison) | модель сохраняет ранжирование материалов | модель даёт тот же порядок материалов по <явному критерию>, что и контрольный расчёт; порядок материалов по <критерию> совпадает с результатом контрольного расчёта |
| switching characteristics / switching metrics (static comparison of PCM states) | переключательные характеристики; переключательные метрики | назвать рассчитанные величины: «длина фазового сдвига и потери»; при необходимости — «характеристики перехода между аморфным и кристаллическим состояниями». Форму «характеристики переключения» оставлять только для расчёта самого процесса переключения: времени, энергии, импульса управления и т. п. |

## Class 2 - invented calque adjectives and compounds

The word does not exist in Russian; it was coined to mirror an English
compound. Hyphenated participle compounds copied from English
("X-loaded", "X-free", "X-aware") are the typical shape.

| English source | Coined calque (wrong) | Natural Russian |
| --- | --- | --- |
| metal-free cut | бесметалльный / безметалльный срез | срез без металла |
| PCM-loaded waveguide | PCM-нагруженный волновод | волновод с PCM; волновод с буферным слоем из PCM |
| dielectric-loaded waveguide | диэлектрически нагруженный волновод (без проверки источника) | волновод с диэлектрической нагрузкой |
| long-range / short-range mode | длиннопробежная / короткопробежная мода (без проверки источника) | мода с большой / малой длиной распространения |
| metal-containing stack | металлсодержащая стопка | многослойная структура с металлическим слоем |
| full-vector (FEM) | полно-векторный | полновекторный (одно слово) |
| full-wave | полно-волновой | полноволновой (одно слово); или «строгий численный» |
| lossier | лоссовее | с большими потерями; потери выше |
| failure-aware | отказоустойчивый (wrong sense) / файлур-эвер | с учетом областей неприменимости |
| derivative-like (lineshape) | производноподобная форма | форма, напоминающая производную контура |

What is NOT automatically a calque here (still check the terminology
registry and venue usage):
- established abbreviation compounds such as «ВЧ-фильтр»; an unfamiliar
  abbreviation compound such as «PCM-нагрузка» or «PCM-фазовращатель» is not
  justified by morphology alone and should default to «с PCM»;
- spelling note: «бес-» is impossible before voiced consonants (б, в, г,
  д, ж, з, л, м, н, р) - a coined «бесметалльный» is misspelled twice over.

## Class 3 - imported metaphors and idiom shapes

| English source | Calque (wrong) | Natural Russian |
| --- | --- | --- |
| anchor (reference solution) | якорь | эталон; эталонное решение (и в подписях/легендах фигур EN-текста - "reference", не "anchor") |
| referred to locally as / locally called | локально называемый; локальное название | известный в русскоязычной литературе как; русскоязычное название |
| corresponds to the infinite-width limit | отвечает пределу бесконечной ширины | описывает бесконечно широкую структуру |
| failure-aware / regions of inapplicability | с учетом областей неприменимости; карта областей неприменимости | границы применимости |
| the first robust observation is | первое устойчивое наблюдение | «Первое: ...» (parallel enumeration) |
| computational window | расчетное окно | расчетная область |
| lateral substrate cladding | боковая подложечная | боковая оболочка из <материала> |
| overlap measures | меры перекрытия | интегралы перекрытия |
| visually compares | визуально сравнивает | наглядно сравнивает |
| decision layer | слой принятия решений | уровень принятия решений |
| planar limit (when it is a control calculation) | планарный предел | строгий планарный расчёт центрального среза |
| horizontal reduction | горизонтальная редукция | замена поперечного сечения горизонтальной планарной моделью |
| mode-branch tracking | отслеживание модовой ветви | подтверждение того, что при изменении параметра выбирается одна и та же физическая мода |
| phase reconfiguration / phase trend | фазовая перестройка; направление фазовой перестройки | знак изменения действительной части эффективного показателя; изменение фазы при кристаллизации |
| at the vertical / horizontal stage (EIM) | на вертикальном / горизонтальном этапе | назвать действие: «при расчёте вертикального среза», «при замене поперечного сечения горизонтальной планарной моделью»; не подменять вычислительную операцию пространственным ярлыком этапа |

## Class 4 - raw English words in Russian prose (суржик)

English words are allowed ONLY: (a) in parentheses when first defining a
term or abbreviation, (b) as established abbreviations (PCM, FEM, SPP,
PML, TM, COMSOL), (c) inside reference titles. Everything else is a
defect. Forbidden list to grep for, with replacements:

| English in RU text | Replacement |
| --- | --- |
| workflow | схема, методика |
| screening | предварительный отбор |
| sweep | расчёты для последовательных значений изменяемого параметра |
| solver | решатель, программа поиска мод |
| eigenmode solver | программа поиска собственных мод |
| overlap | перекрытие |
| insertion loss | вносимые потери |
| lossy | с потерями, поглощающий |
| leaky mode | мода с излучательными потерями; при первом пояснении — мода, из которой энергия уходит в окружающее пространство; «вытекающая мода» только после проверки по реестру |
| near cutoff | вблизи отсечки |
| claim | утверждение, заявляемый результат |
| reduced-order / reduced model | приближенный (редуцированный) |
| branch tracking | подтверждение того, что при изменении параметра выбирается одна и та же физическая мода |
| hold-out, state-paired, failure-aware, phase-trend | rephrase in Russian |
| Z-scan | Z-сканирование; при первом упоминании «Z-сканирование (Z-scan)» |
| pump-probe | «накачка-зондирование» (pump-probe) при первом упоминании |
| decoupled (approximation) | без самосогласования (НЕ «расцепленное (screening)» - скобка поясняет не то слово) |

## Deliberate keeps (do not over-correct)

- «метрики» - kept: «характеристика» collides with ФЧХ (frequency
  response), «показатель» collides with показателем преломления in
  photonics texts. Modern usage accepts «метрики».
- Established borrowings: «ранжирование», «диагностический»,
  «локализация», «валидация» (in methods context).
- Domain term retained in this workflow: «отсечка». Do not call it
  literature-verified unless a source is
  recorded in `verified-russian-terminology.md`.
- Do not present a literal expansion such as «длиннопробежный
  диэлектрически нагруженный плазмон-поляритонный волновод» as an
  established Russian term without evidence from Russian-language primary
  literature. For LR-SPP/LR-DLSPP, retain the international abbreviation and,
  when explanation is needed, use a descriptive phrase such as «мода большой
  длины распространения»; give the English expansion at first use if the
  venue permits it.

## Automation recipe

1. Slice the manuscript body (cut references, edit logs, service
   sections, backup-title lists).
2. Grep the body for, at minimum:
   `[a-zA-Z]{3,}` runs outside parentheses/abbreviations (Class 4);
   `нагруженн` preceded by a Latin/hyphen compound head (Class 2);
   `полно-` (полно-векторный, полно-волновой - все слитно), `лоссов`,
   `якор`, `робастн`, `перформанс`, `в терминах`, `кандидат`,
   `аккуратн\w* баланс`, `тщательн\w* компромисс`, `подложечн`,
   `расчетн\w* окн`, `мер\w* перекрытия`, `устойчивое наблюдение`,
   `программн\w* работ`, `балансир`, `област\w+ неприменимости`,
   `отвечает пределу`, `быстрый инструмент`, `локальн` (локально
   называемый / локальное название - вне смысла «локализация поля»),
   `на\s+(вертикальн|горизонтальн)\w*\s+этап` (назвать расчётную операцию),
   `выцвет` (bleaching -> просветление), `производноподобн`,
   `подпись\w*\s+(сдвига|эффекта)` (signature -> признак),
   `временн\w*\s+трасс` (time traces -> временные зависимости),
   `переключательн\w*\s+(характеристик|метрик)` (для статического сравнения
   состояний назвать конкретные рассчитанные величины),
   `Z-scan`, `pump-probe` (сырые - раскрыть по-русски со скобкой);
   согласование аббревиатур: `(ой|ая|ую|ого|ому)\s+(ПНЧ|ЭДП|ППП)`
   при множественной расшифровке (strategic rule 6).
3. For each hit: find the EN source phrase, resolve the intended sense
   (rule 2), fix with the tables above or rephrase.
4. Fix in ALL title locations at once (working title, title block,
   Russian metadata in every language version, build-script fallbacks) -
   count-asserted.
5. Rebuild every DOCX artifact and verify inside the artifact text that
   the calques are absent and the new wording is present.
6. Add a dated entry to the draft's edit log listing what changed.

## Maintenance

When a new calque is caught (by the user or by review), add the pair to
the matching class table here - not as prose in SKILL.md - and keep the
grep list in step 2 current. This file is the single source of truth for
RU de-calque pairs.
