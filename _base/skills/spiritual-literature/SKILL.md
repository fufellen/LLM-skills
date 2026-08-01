---
name: spiritual-literature
description: Read, write, review, and quote from Christian spiritual literature — sermons, teacher notes, devotionals, Bible studies, systematic theology, catechesis, homiletics, apologetics, and church camp/Sunday-school materials. Use for проповедь, конспект проповеди, богословие, толкование, библейское исследование, курс библейского института, воскресная школа, лагерь, катехизация, or any note under `Церковь/`, `Литература/духовная/`, or with a `Проповедь …` prefix, especially when the text must quote Scripture accurately. All Bible references are resolved from the user's local Synodal Bible at `Церковь/Библия/Библия/`.
---

# Spiritual Literature

## Scope

This is the general skill for working with Christian spiritual and theological texts in the user's vault: writing new material, reviewing existing notes, resolving Bible references, and keeping citations honest.

**Related skills — don't duplicate their scope:**
- `christian-presentations` — slide decks and .pptx safety. When making a deck, use both skills together; that one owns visual layout, this one owns Scripture accuracy.
- `presentation-creation` — deck mechanics.
- `knowledge-refactoring` — deduplication, canonicalization, `[[wiki-link]]` reshaping.
- `scientific-article-writing` — academic manuscripts (do not apply that skill's conventions here).

## Bible: source of truth

The user's local Synodal Bible is at `Церковь/Библия/Библия/` with this layout:

```
Церковь/Библия/Библия/
├── Ветхий завет/<abbr>/<abbr> Глава <N>.md
└── Новый завет/<abbr>/<abbr> Глава <N>.md
```

Each chapter file uses this exact structure — verses are `###### N:V` headings followed by the verse text:

```markdown
---
cssclasses:
  - synodal-bible-chapter
---
#### Ин
##### Глава 3
###### 3:1
Между фарисеями был некто, именем Никодим, …
###### 3:2
Он пришёл к Иисусу ночью и сказал Ему: …
```

**Absolute rule:** never quote a Bible verse from memory. Every direct quote must be read from the chapter file. If the reference doesn't resolve (unknown book, missing chapter, missing verse) — say so plainly and stop; do not fabricate wording, do not silently substitute a nearby verse.

## Reference syntax

Supported reference forms (used both in user notes and in your output):

| Form | Meaning |
|---|---|
| `Ин 3:16` | single verse |
| `Ин 3:16-18` | inclusive range |
| `Ин 3:16, 18` | discontinuous verses in one chapter |
| `Ин 3:16-4:2` | range crossing a chapter boundary (read both files) |
| `Ин 3:16; Рим 5:8` | multiple independent references |
| `Пс 22` | whole chapter (avoid quoting; give a pointer only) |
| `1 Кор 13:4-8` | numbered book |

Whitespace and dashes are forgiving: `1Кор.3:16-18`, `1 кор 3:16–18` (en-dash), and `1 Кор 3:16—18` (em-dash) all normalise to `1 Кор 3:16-18`.

## Resolver algorithm

To resolve a reference `<book> <chapter>:<verse-spec>`:

1. **Normalise the book name** using `references/bible-abbreviations.md`:
   - strip trailing dots, collapse whitespace, lowercase for matching;
   - map any synonym (`Иоан.`, `От Иоанна`, `Ев. Иоанна`, `1-е Петра`, `Первое послание Коринфянам`) to the canonical abbreviation used as a folder name (`Ин`, `1 Пет`, `1 Кор`);
   - reject unknown books — do not guess.
2. **Locate the chapter file** at `Церковь/Библия/Библия/<testament>/<canon>/<canon> Глава <N>.md`. The testament (`Ветхий завет` / `Новый завет`) is fixed per book — see the table.
3. **Extract verses**: read the file, find the `###### <chapter>:<verse>` heading, take every line up to the next `###### ` heading (or end of file). Strip trailing whitespace; keep the exact Synodal wording, including archaic forms (`лице`, `тобою`, `рождённое`).
4. **For cross-chapter ranges** (`Ин 3:16-4:2`), read both files and concatenate.
5. **Never** normalise the verse text — no modernising spelling, no punctuation edits, no "corrections" of `[один]` bracket-style clarifications.

## Output formats

**In vault notes** — use an Obsidian wiki-link with block anchor so the reader can jump straight to the verse in the chapter file:

```markdown
> [[Ин Глава 3#3:16|Ин 3:16]] Ибо так возлюбил Бог мир, что отдал Сына Своего Единородного, дабы всякий верующий в Него, не погиб, но имел жизнь вечную.
```

Multi-verse quote — group under one link, keep verse numbers inline:

```markdown
> [[1 Кор Глава 13#13:4|1 Кор 13:4-7]]
> ⁴ Любовь долготерпит, милосердствует, любовь не завидует, любовь не превозносится, не гордится, ⁵ не бесчинствует, не ищет своего, не раздражается, не мыслит зла, ⁶ не радуется неправде, а сорадуется истине; ⁷ всё покрывает, всему верит, всего надеется, всё переносит.
```

Verse numbers as superscript unicode (`¹²³⁴⁵⁶⁷⁸⁹⁰`) or plain `(4)` — match what the note already uses; don't invent a third style.

**In chat** — cite with a plain reference and put the quoted text below, no wiki-brackets:

```
Ин 3:16 — Ибо так возлюбил Бог мир…
```

## Operations

**Expand a reference into a quote.** Given a bare `Ин 3:16` in a note, replace with the wiki-link quote block above. Ask before editing more than a handful in one pass.

**Collapse a quote back to a reference.** Given a full quote block, replace with `[[Ин Глава 3#3:16|Ин 3:16]]` alone. Useful when a draft has ballooned.

**Audit a note.** Walk the text, extract every candidate reference, resolve each, and report:
- refs that don't resolve (bad book, missing chapter/verse);
- quoted text that doesn't match the Synodal wording at the cited reference;
- refs written in an unusual abbreviation that should be normalised to the folder-name canon for consistency.

Do not silently rewrite the note during an audit — return a list first.

## Writing spiritual prose

- **Quote vs. paraphrase.** If a sentence says what God, Christ, an angel, prophet, apostle, or biblical narrator said, use a direct quote in quotation marks with the verse reference. If simplifying (children's lesson, application), keep it clearly as your own words — do not put a paraphrase inside quotation marks.
- **Don't soften.** Keep the connection to God, Christ, sin, repentance, faith, obedience, prayer, and grace explicit when the passage requires it. Generic moralism ("будь добрым") is not the same as the biblical claim.
- **Don't speculate.** Adding scene details the text doesn't give ("Никодим нервно оглянулся…") is only OK when clearly labelled as illustrative imagination, not as what happened.
- **Reverent tone, light touch.** Serious subject, readable prose. Avoid both stiff churchly Russian and casual flippancy.

## Local sources beyond the Bible

The vault has substantial theological material worth consulting before writing:
- `Литература/духовная/` — books, courses, PDFs (курс библейского института: Библиология, Христология, Апологетика Трещев, …).
- `Церковь/Исследования/` — the user's own topical studies (о деньгах, о долгах, …).
- `Церковь/Труд в церкви/` — teaching materials, Sunday-school lessons, camp plans.
- `Церковь/Библия/Библейская энциклопедия Брокгауза.pdf` — reference encyclopedia.
- Existing `Проповедь …` notes at the vault root — the user's own past sermons; useful for tone and cross-references.

When a claim needs a source, prefer local material. Reach for the web only for background the vault clearly lacks.

## Vault safety

- **[[feedback-confirm-before-delete]]**: never delete or move existing notes without asking. This includes "cleaning up" outdated проповедь files.
- **[[feedback-no-ai-watermarks]]**: no "Generated with", no 🤖, no Co-Authored-By in commits or note bodies.
- **[[feedback-lessons-as-obsidian-notes]]**: durable lessons from a study session become notes in the project's `Уроки/` folder, not chat-only text.
- Bible chapter files (`Церковь/Библия/Библия/**/*.md`) are **read-only** from this skill's perspective — never edit verse text or headings.

## Self-improvement and publishing

When work reveals a durable, reusable rule (new synonym for the abbreviation table, a common failure mode when quoting, a lesson about which local source is authoritative), use the `skill-learning` policy. Save compact rules here or in `references/`. Do not store private pastoral content, personal counseling details, copyrighted book text beyond short necessary excerpts, or one-off facts.

Before materially editing this skill, run the owning repo's freshness check: fetch `origin main`, compare `HEAD` with `origin/main`, fast-forward if clean. After material updates, commit and push by default unless the user says otherwise. Stage only relevant files; split commits by semantic block.
