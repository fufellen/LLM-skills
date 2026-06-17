---
name: nto-formatting
description: Prepare, format, review, and polish Russian NTO / scientific and technical report / otchet o NIR materials. Use for NTO formatting rules, GOST 7.32-2017 report structure, title pages, abstracts, contents, headings, figure and table captions, formulas, source lists, normal-control checklists, and Lidar NTO sections in Obsidian, Markdown, Word, Google Docs, or exported PDF.
---

# NTO Formatting

## Canonical Local Note

When working in the user's Obsidian vault, read this note before applying detailed rules:

```text
C:\Users\User\Мой диск\Obsidian\Работа\Лидар\НТО\Правила оформления НТО.md
```

Treat that note as the local checklist for NTO formatting. If the note is missing, use the fallback rules below and tell the user.

## Repository Synchronization

Keep the user's personal and corporate NTO formatting skill copies synchronized:

- Personal repo: `https://github.com/fufellen/codex-skills`
- Corporate repo: `https://github.com/ak-tech-electronics/codex-skills`

When this `nto-formatting` skill is materially updated, commit and push the personal repo first, then duplicate the same `nto-formatting` folder to the corporate repo and push it there too. Keep the corporate repo limited to the NTO formatting skill unless the user explicitly asks to add more. Report both commit hashes.

## Sources

Use these standards as the basis:

- GOST 7.32-2017 for NIR/NTO report structure and presentation.
- GOST R 7.0.100-2018 for bibliographic descriptions in the source list.
- A customer, institute, or project template overrides generic formatting details when explicitly provided.

If the user asks for current official requirements, verify against current sources before answering.

## Workflow

1. Determine the task type: explain rules, create a checklist, draft a section, review an existing draft, convert notes into NTO prose, or prepare final formatting.
2. For Obsidian work, search/read nearby NTO notes first, especially under `Работа\Лидар\НТО`.
3. Load the canonical local note above for exact checklist details.
4. Preserve technical meaning. Rewrite rough notes into formal report prose, but do not invent measurements, tests, dates, or results.
5. When reviewing, report concrete issues first: missing structure, wrong captions, absent text references, inconsistent units, draft language, missing sources.
6. Remove semantic duplication: keep full explanations in one best place, use short cross-references or summaries elsewhere, and preserve repeats only when they add a new role.
7. When editing Markdown notes, keep Obsidian links natural and run the note validator if available.

## Required Report Shape

Use this order unless a project template says otherwise:

1. Title page.
2. List of contributors.
3. Abstract.
4. Contents.
5. Terms and definitions.
6. Abbreviations and symbols.
7. Introduction.
8. Main body.
9. Conclusion.
10. Source list.
11. Appendices.

Include optional elements only when useful. If there are fewer than three abbreviations or symbols, a separate abbreviation list is usually unnecessary.

## Formatting Checklist

- Page: A4; left margin 30 mm, right 15 mm, top/bottom 20 mm.
- Text: Times New Roman, at least 12 pt; 14 pt acceptable; 1.5 line spacing; 1.25 cm paragraph indent; justified alignment.
- Page numbers: Arabic numerals, continuous numbering, centered at bottom, no dot; title page counted but not numbered.
- Structural headings: centered, uppercase, no final dot, no underline.
- Numbered headings: Arabic numerals; no dot after the section/subsection number.
- Each structural element and each main section starts on a new page in the final document.
- Figures: every figure needs a text reference and a caption like `Risunok 1 - Title`.
- Tables: every table needs a text reference and a caption above the table like `Tablitsa 1 - Title`.
- Formulas: explain variables and units; number only formulas referenced in text.
- Sources: order by first mention in text; format descriptions by GOST R 7.0.100-2018.

## NTO Prose Style

Prefer formal engineering prose:

- structure each major section as task -> problem -> solution methods -> implemented solution -> result/verification;
- treat task -> problem -> solution/methods as the central content spine of an NTO section;
- describe purpose, input data, processing, output data, limitations, and verification;
- use SI units and keep units consistent;
- define abbreviations at first use;
- prefer impersonal/report style over diary style.
- avoid semantic duplicates; one claim, calculation, module description, limitation, or result should not be fully retold in multiple sections.

Avoid:

- chatty wording and raw brainstorming fragments;
- unsupported claims such as "fast", "accurate", or "optimal" without numbers or method;
- dangling placeholders such as "add figure", "check", or "TODO";
- copying rough design notes into final report prose.

## Review Output

For a review, lead with actionable findings. Include:

- location or quoted short fragment;
- what rule or expectation it violates;
- concrete replacement or next action.

Keep the final summary brief and mention any remaining missing inputs, such as absent figures, source data, or customer templates.
