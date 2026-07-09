---
name: scientific-article-writing
description: Universal venue-agnostic discipline for preparing, reviewing, and QA-ing scientific manuscripts and conference papers. Use for написание статьи, подготовка рукописи, review or proofread an article draft, checking citation order and renumbering references, verifying table numbers against data files, syncing bilingual (RU/EN) drafts, pre-submission checklists, safe bulk edits of manuscript files, and DOCX artifact QA. Venue-specific rules (APEDE/IEEE conference via apede-ieee-conference-article, Оптика и спектроскопия via optics-spectroscopy-article, russian НТО/GOST 7.32 reports via nto-formatting) live in their dedicated skills and override this one; this skill is the shared base that prevents common manuscript mistakes.
---

# Scientific Article Writing (universal base)

## Purpose

Shared, venue-agnostic rules for manuscript work. Written imperatively so
that ANY model - including weaker ones - can follow them without judgment
calls. When a dedicated venue skill exists, read it too; its rules override
this skill on conflicts. Known venue skills:
- `apede-ieee-conference-article` - APEDE / IEEE two-column conference
  papers (IEEE Xplore);
- `optics-spectroscopy-article` - journal «Оптика и спектроскопия» and
  similar Ioffe journals;
- `nto-formatting` - Russian НТО / отчет о НИР materials per
  GOST 7.32-2017 (lives in the corporate skills submodule
  `nto-formatting/_base/skills/nto-formatting/`).
Conversion mechanics live in `markdown-to-docx`; domain claim rules in
`plasmonics-photonics` / `scientific-work`; RU/EN language purity
(де-кальке) in `ru-language-purity`.

## Non-Negotiable Rules

Violating any of these is a defect, not a style choice.

1. **Never invent facts.** No invented e-mails, affiliations, ORCIDs, grant
   numbers, DOIs, page numbers, material constants, or reviewer names.
   Search the vault and the article's data files first. If not found,
   insert a visible placeholder `[УТОЧНИТЬ: <what exactly>]` and list every
   placeholder at the end of your report. Never delete a placeholder
   without filling it with user-confirmed data.
2. **Never change science while formatting.** Rewording, translating, or
   converting a draft must not alter claims, numbers, signs, or hedges
   ("in the considered cases" must not become "always"). If a formatting
   rule seems to require a science change, stop and report.
3. **Newest validated draft wins.** When several drafts of one paper exist
   (RU/EN, old/new), first determine the scientific source of truth: the
   draft carrying the latest validation results and edit log. Sync the
   others FROM it. Never format a stale draft.
4. **Every number must trace.** Every quantitative value in text and tables
   traces to a data file, script output, or citation. Before trusting any
   table: recompute values derivable from formulas given in the same paper
   and cross-check rows against the source CSVs. Report mismatches; do not
   silently "correct" either side.
5. **Bulk edits only by count-asserted script.** Renumbering references,
   renaming an author, changing units - anything with more than ~3
   occurrences or spanning several files - must be done by a script where
   EVERY replacement asserts its expected occurrence count and the script
   verifies the result (e.g. re-extracts citation order). Never hand-edit
   repeated tokens.
6. **QA the artifact, not the source.** After producing a DOCX/PDF, inspect
   the artifact itself (unzip DOCX, read `word/document.xml`): no raw TeX
   (`\mathrm`, `$`, `operatorname`), no Markdown leftovers (`[[`, `####`,
   `**`), no template guidance text, no `TODO`. Verify tables, figures, and
   required blocks are physically present. **Headings must be black**:
   python-docx/Word default Heading and Title styles are blue - every build
   script that assigns Word heading styles must also force RGB(0,0,0) on
   those style definitions, and QA must verify it by parsing
   `word/styles.xml` (check EVERY build script of the article, including
   secondary-language ones - this is where the rule gets missed).
   Also reject collapsed formula artifacts created by naive TeX stripping:
   missing fraction bars, lost subscripts, and adjacency that changes the
   meaning of equations (for example `beta/k0` becoming `betak0`, or
   `1/(2 Im beta)` becoming `12Imbeta`) are content defects, not typography.
7. **Look at the rendered pages, do not only parse the XML.** Parsing
   `word/document.xml` proves attributes (a `both` value, a border `nil`);
   it does NOT show how the page actually looks - unbalanced columns, a
   caption split from its table, an equation that renders too large, a
   figure that overflows the column, an author line that wrapped badly.
   These are only visible by eye. After building the DOCX, render it to
   per-page images and ACTUALLY VIEW them, comparing against the venue
   template's own example page/table/figure. This is mandatory before
   calling layout done - the user should never be the one catching visual
   nuances by hand. Recipe below.
8. **Report everything unresolved.** The final report must list every
   remaining rule violation and every placeholder. Never call a manuscript
   "ready" or "camera-ready" while placeholders or known violations remain.

## Visual Proof (render and look) - mandatory for any templated document

Two QA layers, both required: (a) XML artifact scan (rule 6), and (b) a
visual render you actually look at (rule 7). One does not replace the other.

Render DOCX -> PDF -> per-page PNG, then read each PNG as an image:

```
python <this skill>/scripts/render_docx_pages.py "<file.docx>" "<out_dir>" --dpi 110
```

The script converts DOCX->PDF (LibreOffice `soffice --headless` if present,
else MS Word COM on Windows via PowerShell/`ExportAsFixedFormat`, format 17)
and renders pages with PyMuPDF. It also accepts a PDF directly. Then open
each PNG and check, against the template's example:
- overall two-column balance, no half-empty columns or orphaned headings;
- every table looks like the template's table example (rule style, header,
  fit) and its caption sits with it; wide floats truly span both columns;
- equations are the body text size and render as real fractions, not raw
  TeX or oversized glyphs;
- figures fit their column/span, axis labels legible, caption below;
- title/author/affiliation block wraps sensibly (e-mail not stranded).

Note: a DOCX open in Word locks the file; close it (or render a `_v2`
copy). Do this render every time layout code changes, not just once.

## Standard Workflow

1. Identify the venue and read its dedicated skill (if any) fully.
2. Identify the source-of-truth draft (rule 3). Read its edit log.
3. Check the submission deadline against today's date; flag if passed.
4. Number/claim QA (rule 4) on the source draft.
5. Apply venue formatting rules; run the Universal Checks below.
6. Convert (via `markdown-to-docx` or the article's build script), then QA
   the artifact in TWO layers: the XML scan (rule 6) and the visual render
   you look at (rule 7 / Visual Proof section).
7. Sync secondary-language drafts from the corrected source; keep reference
   numbering identical across languages; append a dated entry to the
   draft's edit log describing what was synced.
8. Report: what was fixed, what remains, all placeholders.

## Universal Checks (automate; recipes included)

Run these on every manuscript regardless of venue:

- **Citation order.** Extract bracket citations in body reading order with
  `\[(\d+)\](?:[-–]\[(\d+)\])?` (expand ranges). The first-appearance
  sequence must be exactly `1..N` when the venue numbers by appearance
  (IEEE does). Also: one work = one number; every cited number exists in
  the list and vice versa. To renumber: build old->new map, apply in one
  regex pass, re-sort the list block, re-run the check.
- **Abbreviations.** Every acronym is expanded at its FIRST body use
  (abstract does not count), once, and used consistently after.
- **Placeholders.** Grep for `УТОЧНИТЬ`, `TODO`, `FIXME`, `XXX`, `???` -
  each hit must be intentional and reported.
- **Typography.** Decimal points with leading zeros (`0.25`, never `.25`);
  no e-notation in prose (`9e-4` -> `0.0009` or a power of ten); real
  units symbols (`µm`, not `um`); dashes per venue (em/en for IEEE, plain
  hyphen for Ioffe journals - check the venue skill).
- **Floats.** Every table/figure is cited in text BEFORE it appears;
  table captions above tables, figure captions below figures (IEEE
  convention; venue skill may differ). Figure axis labels are
  `Quantity (unit)`, figures meet the venue dpi minimum, each figure also
  exists as a separate file.
- **Wikilinks and vault artifacts.** `[[...]]`, Obsidian frontmatter,
  local-note sections ("Локальные источники", GPT notes, edit logs) must
  never leak into the submission artifact.
- **Names.** Cyrillic-to-Latin transliteration is verified per author
  (щ -> shch, ч -> ch, ж -> zh); author-preferred spellings win over
  standard transliteration - ask if unknown.
- **Language purity (RU and EN).** Use the `ru-language-purity` skill - the
  shared source of truth for де-кальке, referenced by every writing skill so
  the checklist is not duplicated here. Russian scientific prose must not
  carry English words (суржик), false friends (careful -> «аккуратный»),
  invented calque compounds («PCM-нагруженный», «бесметалльный»,
  «полно-векторный», «лоссовее»), or imported metaphors (anchor -> «якорь»);
  English is allowed ONLY (a) in parentheses when first defining a term or
  abbreviation, (b) in established abbreviations (PCM, FEM, SPP, PML, COMSOL,
  TM), (c) in reference titles. Register: научный стиль уровня опытного
  ученого. MANDATORY before writing or editing Russian manuscript prose, and
  as a full pass over any RU text translated from an (AI-written) English
  draft: read `ru-language-purity` and its `references/decalque-ru-en.md`
  (strategic rules, replacement tables by defect class, deliberate keeps,
  grep recipe) and apply it. The mirror direction applies too: an English
  version written from a Russian working draft must not keep insider calques
  ("local" = in-house runs, "referred to locally as", unintroduced
  working-title jargon, "COMSOL-side step") - `ru-language-purity` covers
  that direction as well.

## Authoring A Venue Skill From The Journal/Conference Template

This applies when BUILDING a new venue skill (e.g. `apede-...`,
`optics-...`) from the journal's or conference's official template or
author guidelines - not when writing a paper.

- **Inspect the official template/rules document visually, not only by
  extracted text.** Reading the text of a template `.docx`/`.pdf` captures
  the prose rules but MISSES the visual conventions, which are usually the
  ones that get a paper bounced or that the user later has to point out by
  hand: the table rule style (e.g. horizontal rules only vs a full grid),
  heading appearance, one/two-column layout, caption placement, figure/axis
  style, equation numbering position, and non-body parts (page footer
  copyright line, sponsors/funding text box, running headers). Render the
  template to images and LOOK at it (scripts/render_docx_pages.py for
  DOCX/PDF; screenshot the live rules web page), then encode those visual
  rules in the skill and its `references/`.
- Keep the template's own example table and example figure as the reference
  the skill tells future runs to compare their output against.
- Recheck the live author-guidelines page before real submissions; template
  files bundled in a repo go stale.

## Multi-Language Drafts

- The pair (RU draft, EN draft) must stay scientifically identical; only
  language and venue-required blocks differ.
- Reference numbering must be identical in both. After renumbering one,
  renumber the other with the same old->new map.
- Author lists, affiliations, and e-mails must match across all files of
  the article (drafts, build scripts, metadata blocks) - fix with one
  script over all files.
- Every sync gets a dated entry in the draft's edit-log section stating
  exactly what was changed and why. Historical log entries are never
  rewritten - they describe the past.

## Practical Environment Lessons

- A DOCX open in Microsoft Word locks its path (PermissionError on save):
  build to a `_v2` name, tell the user, regenerate the canonical name
  after Word is closed, then delete the stale copy.
- Some publisher DOCX files are ISO Strict OOXML (`purl.oclc.org`
  namespaces); pandoc and python-docx fail on them - parse
  `word/document.xml` directly with the strict namespace.
- Keep the manuscript source in Markdown next to a reproducible build
  script; regenerate the DOCX from source instead of editing the DOCX.
- Keep dated backups of prior camera-ready versions instead of
  overwriting.

## Self-Improvement And Publishing

When manuscript work reveals a durable, reusable, venue-AGNOSTIC lesson,
use the `skill-learning` policy and save it here (compact rule, no session
narrative). Venue-specific lessons go to the venue skill instead. Do not
store secrets, credentials, unpublished manuscript content, referee
correspondence, copyrighted text, generated logs, or one-off facts.

Before materially editing this skill, run the owning repository's
freshness check: fetch `origin main`, compare local `HEAD` with
`origin/main`, fast-forward if behind and clean, inspect dirty/ahead/
diverged states before continuing.

After materially updating this skill, validate the shared base and
adapters when feasible, then commit and push to the owning repository by
default unless the user says not to. Stage only relevant skill files;
split commits by semantic block; avoid vague rollups.

If publishing hits remote changes or merge conflicts, resolve them
autonomously when the intended final meaning is determinable from files,
history, and the user's instruction; otherwise stop and report.

## Guardrails

- Do not submit anywhere; prepare materials and stop.
- Do not delete or overwrite user drafts; create new files or edit with
  the user's explicit direction.
- When this skill and a venue skill disagree, the venue skill wins - but
  say so explicitly in the report.
