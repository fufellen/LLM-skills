---
name: knowledge-refactoring
description: Refactor Obsidian vault notes and other knowledge bases into linked sources of truth. Use when the user asks to remove duplicates, consolidate notes, choose canonical notes, replace repeated explanations with [[Obsidian links]], audit stale facts against source files or code, or reorganize technical knowledge without moving files.
---

# Knowledge Refactoring

## Core Rule

Make knowledge DRY without making it cryptic. Each durable fact should have one canonical home; other notes should mention the concept briefly and link to the canonical note or section.

Reusable scientific and technical term definitions should be canonical standalone term notes. If a note defines a term inline, extract or consolidate the reusable definition into the term note and replace repeated explanations elsewhere with `[[Term]]` links plus only the local context needed by that note.

## Self-Improvement And Publishing

When knowledge-refactoring work reveals a durable, reusable lesson, use the `skill-learning` policy. Save compact canonicalization rules, anti-duplication heuristics, validation checks, or reusable search/refactor workflows in this skill or a focused reference file. Do not store private note content, customer material, credentials, generated logs, or one-off project facts in the skill.

Before materially editing this skill, applying self-learning updates, or publishing changes, run the owning repository's freshness check: fetch `origin main`, compare local `HEAD` with `origin/main`, fast-forward if local is behind and the relevant working tree is clean, and inspect dirty/ahead/diverged states before continuing.

After materially updating this skill, validate it when feasible, then commit and push the relevant skill changes to the owning repository by default unless the user explicitly says not to. Stage only relevant skill files and repository metadata.

If publishing encounters remote changes or merge conflicts, resolve them autonomously when the intended final meaning can be determined from the files, commit history, nearby rules, and the user's instruction. Preserve compatible rules from both sides, consolidate duplicates, rerun validation, commit the resolved result, and push. Stop only when resolution would require guessing unavailable technical meaning, exposing protected content, discarding user work, or using unavailable repository permissions.

## Workflow

1. Search the relevant folder first, then widen the search only as needed.
2. Identify duplicated claims, tables, code layouts, procedures, and checklists.
3. Assign a role to each note before editing:
   - canonical specification;
   - route map or workflow;
   - audience summary;
   - diagnostic checklist;
   - archive or historical context.
4. Keep complete details only in the canonical note. In other notes, replace duplicated details with `[[Note]]` or `[[Note#Section]]`.
5. Preserve unique context: decisions, caveats, chronology, diagnostics, and project-specific warnings should not be deleted just because related facts are canonical elsewhere.
6. When a note describes software, protocols, schemas, hardware behavior, or APIs, verify the canonical facts against the actual source files before treating them as truth.
7. Do not move or rename notes unless the user explicitly asks.
8. After material edits, run the vault note validator when available.

When reorganizing term notes, do not assume every term note already lives in a folder named `terms`, `Термины`, or `thermins`. Search for scattered standalone term notes in the relevant vault area, including project folders and root folders, but do not move paper notes, reports, course notes, modeling diaries, or other context-rich notes merely because they contain definitions.

## Canonicalization Heuristics

- Put byte layouts, packet formats, constants, enum mappings, and selectors in one specification note.
- Put reusable term definitions in standalone term notes; project notes, report sections, and literature notes should link to them rather than becoming the only definition source.
- Put end-to-end procedures in a route-map note that links to the specification sections.
- Put troubleshooting in a diagnostic note or section, linking to the relevant specs instead of copying field lists.
- Put human-facing briefings in short summary notes with links to the authoritative details.
- If two notes both look canonical, choose the one whose title names the concept most directly, then turn the other into a workflow, index, or summary.
- For a tutorial or lesson series, keep one overview/route-map note (e.g. a course plan) that links to the detailed lessons instead of re-explaining them, and make each lesson the canonical home for its own topic. Extract tooling/API/language primitives that recur across sibling lessons (e.g. CMake `OBJECT`/`INTERFACE` libraries, `PUBLIC`/`PRIVATE` visibility, toolchain files, presets) into standalone concept notes; in each lesson replace the inline definition with a short context phrase plus a `[[concept]]` link.

## Obsidian Links

Use exact wiki links for local notes:

```text
[[Canonical Note]]
[[Canonical Note#Section]]
[[Canonical Note|display text]]
```

Prefer the shortest resolvable wiki link. If the note title is unique in the vault, use `[[Note]]` or `[[Note|display text]]` instead of a vault-root path. Add only the minimal folder path needed to disambiguate duplicate filenames.

Do not write meta-comments inside notes such as "removed duplication here". Make the note read naturally.

## Verification

For technical refactors:

- cite source paths inside the note when they are useful for future checking;
- distinguish verified facts from hypotheses;
- remove or qualify stale statements that no longer match source code;
- prefer source code, primary docs, and generated artifacts over memory.
