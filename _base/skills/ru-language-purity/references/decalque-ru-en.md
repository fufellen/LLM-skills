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
6. **Убирай слова-филлеры и книжные обороты (заумность).** Если
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

## Class 2 - invented calque adjectives and compounds

The word does not exist in Russian; it was coined to mirror an English
compound. Hyphenated participle compounds copied from English
("X-loaded", "X-free", "X-aware") are the typical shape.

| English source | Coined calque (wrong) | Natural Russian |
| --- | --- | --- |
| metal-free cut | бесметалльный / безметалльный срез | срез без металла |
| PCM-loaded waveguide | PCM-нагруженный волновод | волновод с PCM-нагрузкой |
| full-vector (FEM) | полно-векторный | полновекторный (одно слово) |
| full-wave | полно-волновой | полноволновой (одно слово); или «строгий численный» |
| lossier | лоссовее | с большими потерями; потери выше |
| failure-aware | отказоустойчивый (wrong sense) / файлур-эвер | с учетом областей неприменимости |

What is NOT a calque here (do not "fix"):
- established adverb+participle terms: «диэлектрически нагруженный
  волновод» (DLSPPW) - standard in Russian literature;
- noun compounds with an abbreviation head: «PCM-нагрузка»,
  «PCM-фазовращатель», «ВЧ-фильтр» - normal Russian word formation;
- spelling note: «бес-» is impossible before voiced consonants (б, в, г,
  д, ж, з, л, м, н, р) - a coined «бесметалльный» is misspelled twice over.

## Class 3 - imported metaphors and idiom shapes

| English source | Calque (wrong) | Natural Russian |
| --- | --- | --- |
| anchor (reference solution) | якорь | эталон; эталонное решение (и в подписях/легендах фигур EN-текста - "reference", не "anchor") |
| corresponds to the infinite-width limit | отвечает пределу бесконечной ширины | описывает бесконечно широкую структуру |
| failure-aware / regions of inapplicability | с учетом областей неприменимости; карта областей неприменимости | границы применимости |
| the first robust observation is | первое устойчивое наблюдение | «Первое: ...» (parallel enumeration) |
| computational window | расчетное окно | расчетная область |
| lateral substrate cladding | боковая подложечная | боковая оболочка из <материала> |
| overlap measures | меры перекрытия | интегралы перекрытия |
| visually compares | визуально сравнивает | наглядно сравнивает |
| decision layer | слой принятия решений | уровень принятия решений |

## Class 4 - raw English words in Russian prose (суржик)

English words are allowed ONLY: (a) in parentheses when first defining a
term or abbreviation, (b) as established abbreviations (PCM, FEM, SPP,
PML, TM, COMSOL), (c) inside reference titles. Everything else is a
defect. Forbidden list to grep for, with replacements:

| English in RU text | Replacement |
| --- | --- |
| workflow | схема, методика |
| screening | предварительный отбор |
| sweep | серия параметрических расчетов |
| solver | решатель, программа поиска мод |
| eigenmode solver | программа поиска собственных мод |
| overlap | перекрытие |
| insertion loss | вносимые потери |
| lossy | с потерями, поглощающий |
| leaky mode | вытекающая мода |
| near cutoff | вблизи отсечки |
| claim | утверждение, заявляемый результат |
| reduced-order / reduced model | приближенный (редуцированный) |
| branch tracking | отслеживание модовой ветви |
| hold-out, state-paired, failure-aware, phase-trend | rephrase in Russian |

## Deliberate keeps (do not over-correct)

- «метрики» - kept: «характеристика» collides with ФЧХ (frequency
  response), «показатель» collides with показателем преломления in
  photonics texts. Modern usage accepts «метрики».
- Established borrowings: «ранжирование», «диагностический»,
  «локализация», «валидация» (in methods context).
- Domain terms verified in Russian literature: «длиннопробежный ППП»,
  «вытекающая мода», «отсечка», «модовая ветвь».

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
   `отвечает пределу`, `быстрый инструмент`.
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
