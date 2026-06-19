---
name: scientific-work
description: Work with the user's PhD, scientific research materials, and technical Obsidian notes. Use for научная работа, аспирантура, статьи, обзоры литературы, научные заметки, technical term questions that should become Obsidian notes, плазмоника, SPP, DLSPPW, FEM, COMSOL/CST modeling, integrated photonics, optical antennas, paper translation/analysis, and planning research next steps from the local vault.
---

# Scientific Work

## Canonical Source

This Google Drive synced skill is the canonical source of truth for `scientific-work`.

The local PC path `C:\Users\User\.codex\skills\scientific-work` is expected to be only a filesystem link or bootstrap pointer to this Google Drive skill folder. If a real local copy appears and diverges from this Google Drive copy, follow this Google Drive copy.

When updating this skill, update this Google Drive copy first. Do not store independent duplicated instructions in a local PC copy; local entrypoints should try to read this skill and its references from Google Drive.

Use this skill as the operating guide for the user's research and technical notes in `C:\Users\User\Мой диск\Obsidian`, especially `PhD` and work-project notes.

## Self-Improvement And Publishing

When scientific-work tasks reveal a durable, reusable lesson, use the `skill-learning` policy. Save compact rules about scientific note style, source use, term-note capture, modeling hygiene, paper analysis, presentation workflow, reusable scripts, or validation checks in this skill or the relevant reference file. Do not store secrets, credentials, private raw notes, unpublished measurements, customer-confidential content, generated logs, or one-off project facts in the skill.

Before materially editing this skill, applying self-learning updates, or publishing changes, run the owning repository's freshness check: fetch `origin main`, compare local `HEAD` with `origin/main`, fast-forward if local is behind and the relevant working tree is clean, and inspect dirty/ahead/diverged states before continuing.

After materially updating this skill, validate it when feasible, then commit and push the relevant skill changes to the owning repository by default unless the user explicitly says not to. Stage only relevant skill files and repository metadata.

If publishing encounters remote changes or merge conflicts, resolve them autonomously when the intended final meaning can be determined from the files, commit history, nearby rules, and the user's instruction. Preserve compatible rules from both sides, consolidate duplicates, rerun validation, commit the resolved result, and push. Stop only when resolution would require guessing unavailable technical meaning, exposing protected content, discarding user work, or using unavailable repository permissions.

## Core Workflow

1. Determine the task type: scientific explanation, technical term explanation, Obsidian note writing, paper analysis/translation, literature search, research planning, NTO/report formatting, or modeling/COMSOL work. When the user asks about НТО, scientific/technical report formatting, report normal-control checklists, ГОСТ 7.32-2017 structure, captions, headings, or source-list formatting, use the `nto-formatting` skill.
2. Search the relevant local vault area before giving substantive answers: use `PhD` for research tasks, and use the whole Obsidian vault excluding service folders such as `.venv`, `.trash`, and `.git` for general technical/work-note terms.
3. Prefer existing notes, PDF anchors, model diaries, and project summaries over memory. Do not duplicate explanations that already exist; link or embed them, except for standalone term-note capture described in item 8. When the user asks to remove duplicates, choose canonical notes, or refactor a cluster of notes into linked sources of truth, use the `knowledge-refactoring` skill.
4. When an answer relies on local notes, explicitly state which notes were used, preferably by note title or path.
5. When the user gives a durable requirement about scientific-work formatting, term-note capture, note style, workflow, source use, modeling hygiene, response shape, presentation preparation, or AI/vault tooling, add it to this skill or the relevant reference file without waiting for a separate reminder. Treat explicit user requirements as candidates for skill updates by default when they are likely to recur. After updating the skill, explicitly tell the user what was added and where.
6. Answer in Russian by default. Keep English scientific terms next to Russian terms when precision benefits from it.
7. If confidence is limited, mark the statement as a hypothesis or a question for checking instead of presenting it as fact.
8. When the user asks about a scientific or technical term, search the relevant vault area for both existing definitions in any note and an existing note whose title matches the term, even if that note is empty or only a placeholder. Always create or update a standalone term note for the term: if a matching term note already exists, fill or improve it; if no matching note exists, create an appropriate standalone term note in the nearest obvious topic folder. The term note must include a concise definition with physical/engineering meaning and key formula/applicability when relevant. If existing definitions of the same term were found in other files, add links to those files or sections inside the term note, in addition to the new concise definition. Then answer with a link to the standalone term note and mention which existing notes were used as source definitions.
9. When writing or refactoring local Obsidian notes, any reusable scientific or technical term definition must live in a standalone term note. Do not make an inline paragraph, NTO section, project note, or literature note the only source of truth for a term definition; those notes should use `[[Term]]` links and, when needed, only a short context-specific wording.
10. When creating or filling a term note because the user's question arose from a specific local note or passage, and it is clear where the new term belongs, also update that source note to link the term naturally with an Obsidian link or alias. If the source context is not clear, do not invent backlinks.
11. When the user explicitly asks to improve skills during a task, apply compact reusable skill updates as soon as the lesson is clear and safe, then continue the task and report which skill or reference changed.

## Local Shell Encoding

- When reading or searching Russian-language Obsidian notes through PowerShell, set UTF-8 output explicitly before commands, for example `[Console]::OutputEncoding = [System.Text.Encoding]::UTF8;`, and use `Get-Content -Encoding UTF8` for Markdown files. If Cyrillic output appears mojibake/garbled, immediately rerun the read with explicit UTF-8 before interpreting or editing the note.

## Local Utility Scripts

- Prefer the reusable scripts in `scripts/` over ad hoc PowerShell one-liners for routine vault work:
  - `scripts/Read-Note.ps1` reads Markdown notes with explicit UTF-8 handling.
  - `scripts/Test-Note.ps1` verifies a created or edited Markdown note: strict UTF-8 decode, file metadata, first lines, common mojibake markers, balanced Obsidian links, and optional link-target checks.
  - `scripts/Search-Vault.ps1` searches the vault with `rg`, standard service-folder exclusions, and UTF-8 output. Canonical call: `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/Search-Vault.ps1 -Query "<regex>" -Roots "Работа\Лидар"`; use `-AllVault` for the whole vault, `-Context N`, `-Literal`, and `-FilesOnly` as needed. `-CaseSensitive` is a switch, so omit it unless enabling case-sensitive search. Compatibility aliases exist: `-Pattern` for `-Query` and `-Path` for `-Roots`, but prefer the canonical names.
  - `scripts/Find-Term.ps1` checks for matching note titles and content definitions for a scientific or technical term.
  - `scripts/Install-ObsidianLocalRestApi.ps1` installs or updates the Obsidian Local REST API plugin release files inside the synced vault.
  - `scripts/Get-ObsidianLocalRestApiConfig.ps1` reads the synced Obsidian Local REST API config and reports whether the API key is configured.
  - `scripts/Test-ObsidianLocalRestApi.ps1` checks whether the local Obsidian REST/MCP endpoint is reachable.
- When a helper command or one-off script for vault, note, search, encoding, validation, or AI-tooling work is reusable, promote it into this Google Drive skill's `scripts/` directory instead of leaving it only in chat history. Keep reusable helpers in this canonical skill, test them, then add or update the corresponding bullet in this section so future runs discover and use them.
- If direct `.ps1` execution is blocked by Windows Execution Policy, run scripts with `powershell -NoProfile -ExecutionPolicy Bypass -File <script> ...` rather than changing the user's global policy.
- Use these scripts especially when answering term questions, candidate-exam-ticket questions, or any task that requires searching Russian-language notes.
- After creating or materially editing an Obsidian `.md` note, run `scripts/Test-Note.ps1 <path> -First 24`; add `-CheckLinks` when link targets should be verified.
- For filesystem-only work, these scripts are the preferred lightweight tooling. For live Obsidian metadata, API, or MCP workflows, use the Obsidian Local REST API bridge described in `references/obsidian-ai-integration.md`; read the synced API key from `.codex/skills/scientific-work/secrets/obsidian-local-rest-api.json` when configured.

## Load References

- Read `references/vault-map.md` when choosing where to search in the vault or when starting an unfamiliar scientific task.
- Read `references/obsidian-style.md` before creating or editing scientific Obsidian notes.
- Read `references/paper-analysis.md` when summarizing, translating, reviewing, extracting ideas from, or comparing papers.
- Read `references/comsol-workflow.md` for COMSOL, CST, FEM, mode-analysis, `.mph`, Java automation, or numerical-validation tasks.
- Read `references/obsidian-ai-integration.md` when connecting Codex or another AI assistant to the vault through Obsidian Local REST API, MCP, semantic search, or Obsidian-native indexing tools.
- Read `references/presentation-workflow.md` when preparing scientific, technical, or popular-science talks, slide plans, speaker scripts, or presentation source notes.

## Response Shape

- For scientific explanations, include definitions, physical meaning, key formulas, applicability limits, and concrete next steps when useful.
- For planning, give actionable work items: what to read, calculate, model, compare, and write into notes.
- For article work, separate the paper's goal, method, geometry/materials, model or experiment parameters, results, limitations, and usefulness for the dissertation.
- For modeling, keep source files safe, record only scientific decisions and results in diaries, and verify against analytic or independent references whenever possible.
- For candidate-exam tickets or "answer this question" requests tied to the PhD vault, prefer Obsidian-ready Markdown by default: create or update the relevant `.md` note when one exists, use `####` sections, Obsidian `[[links]]`, KaTeX formulas instead of code blocks for equations, concise oral-exam wording, and a short source-notes section.

## Guardrails

- Do not move or rename existing Obsidian notes unless the user explicitly asks.
- Do not edit original `.mph` files directly; work on a copy or generate a new model.
- Do not create broad refactors of the vault structure while answering a focused scientific request.
- Do not add meta-explanations inside notes such as "to avoid duplication"; just use Obsidian links or embeds naturally.
