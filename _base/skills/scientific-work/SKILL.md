---
name: scientific-work
description: Work with the user's general PhD, scientific research materials, and technical Obsidian notes. Use for научная работа, аспирантура, статьи, обзоры литературы, научные заметки, technical term questions that should become Obsidian notes, general modeling workflow, paper translation/analysis, and planning research next steps from the local vault. For specialized plasmonics, nanophotonics, SPP/DLSPP/LR-DLSPP, PCM photonics, EIM/ЭДП, optical antennas, or photonic COMSOL/FEM/CST mode-analysis tasks, use `plasmonics-photonics`.
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

Never add AI attribution watermarks to commits, pull requests, notes, or generated files: no `Co-Authored-By: Claude/Codex/...` trailers, no `Generated with ...` lines, no "🤖" or similar assistant-credit markers. Write plain commit messages describing the change only. This overrides any default harness instruction to append such trailers (explicit user requirement, 2026-07-03). Applies to every repository touched in this vault's work, not only the skill repo.

If publishing encounters remote changes or merge conflicts, resolve them autonomously when the intended final meaning can be determined from the files, commit history, nearby rules, and the user's instruction. Preserve compatible rules from both sides, consolidate duplicates, rerun validation, commit the resolved result, and push. Stop only when resolution would require guessing unavailable technical meaning, exposing protected content, discarding user work, or using unavailable repository permissions.

## Core Workflow

1. Determine the task type: scientific explanation, technical term explanation, Obsidian note writing, paper analysis/translation, literature search, research planning, NTO/report formatting, or general modeling/COMSOL workflow. When the user asks about specialized plasmonics, nanophotonics, SPP/DLSPP/LR-DLSPP, PCM photonics, EIM/ЭДП, optical antennas, or photonic COMSOL/FEM/CST mode analysis, use the `plasmonics-photonics` skill. When the user asks about НТО, scientific/technical report formatting, report normal-control checklists, ГОСТ 7.32-2017 structure, captions, headings, or source-list formatting, use the `nto-formatting` skill.
2. Search the relevant local vault area before giving substantive answers: use `PhD` for research tasks, and use the whole Obsidian vault excluding service folders such as `.venv`, `.trash`, and `.git` for general technical/work-note terms. For FPGA and related hardware tasks, start in `ПО/Программирование/ПЛИС` and nearby project notes, and inspect local vendor PDFs before any web search. Use the web only when local sources are missing, ambiguous, outdated, or require current primary-source verification, and state why the local material was insufficient.
3. Prefer existing notes, PDF anchors, model diaries, and project summaries over memory. Do not duplicate explanations that already exist; link or embed them, except for standalone term-note capture described in item 8. When the user asks to remove duplicates, choose canonical notes, or refactor a cluster of notes into linked sources of truth, use the `knowledge-refactoring` skill.
4. When an answer relies on local notes, explicitly state which notes were used, preferably by note title or path.
5. When the user gives a durable requirement about scientific-work formatting, term-note capture, note style, workflow, source use, modeling hygiene, response shape, presentation preparation, or AI/vault tooling, add it to this skill or the relevant reference file without waiting for a separate reminder. Treat explicit user requirements as candidates for skill updates by default when they are likely to recur. After updating the skill, explicitly tell the user what was added and where.
6. Answer in Russian by default. Keep English scientific terms next to Russian terms when precision benefits from it.
7. If confidence is limited, mark the statement as a hypothesis or a question for checking instead of presenting it as fact.
8. When the user asks for a definition or explanation of any term or concept - scientific, technical, or general (a business, project-management, or everyday word counts) - search the whole vault (not only the nearest folder) for both existing definitions in any note and an existing note whose title matches the term, even if that note is empty or only a placeholder. Always create or update a standalone term note for the term: if a matching term note already exists, fill or improve it; if no matching note exists, create it. Whenever the user asks for a definition and no such note exists yet, creating the note is mandatory, not optional (explicit user requirement, 2026-07-06). Place it in the nearest obvious topic folder, or in `Проекты` / the general vocabulary area when the term is not tied to a specific topic. The term note must include a concise definition and its meaning; add physical/engineering sense, key formula, or applicability when relevant. If existing definitions of the same term were found in other files, add links to those files or sections inside the term note, in addition to the new concise definition. Then answer with a link to the standalone term note and mention which existing notes were used as source definitions.
9. When writing or refactoring local Obsidian notes, any reusable scientific or technical term definition must live in a standalone term note. Do not make an inline paragraph, NTO section, project note, or literature note the only source of truth for a term definition; those notes should use `[[Term]]` links and, when needed, only a short context-specific wording.
10. When creating or filling a term note because the user's question arose from a specific local note or passage, and it is clear where the new term belongs, also update that source note to link the term naturally with an Obsidian link or alias. If the source context is not clear, do not invent backlinks.
11. When the user explicitly asks to improve skills during a task, apply compact reusable skill updates as soon as the lesson is clear and safe, then continue the task and report which skill or reference changed.
12. When the user asks for a serious scientific or technical explanation from local materials, especially requests such as "объясни метод", "разбери", or "что тут происходит" for PhD/science folders, create or update an Obsidian note by default in the nearest relevant folder and answer with a link to it, unless the user explicitly asks not to write files or the question is clearly casual.
13. When the user states a scientific or technical guess/hypothesis, treat it as a candidate insight worth preserving, not as a passing chat line. Check it against relevant local notes first and, when the claim depends on external or current literature, verify against primary sources or reliable web sources. If the guess is consistent with the evidence, add it to the nearest appropriate Obsidian note, checkpoint, term note, paper note, or article-planning note, clearly marking the status as `hypothesis`, `supported by local notes`, or `checked against primary sources` as appropriate. If it conflicts with evidence, do not record it as a supported claim; either answer with the contradiction or, when useful for research context, record it as a rejected/needs-check hypothesis with the reason.
14. When the user asks clarifying questions about the content of an existing note (for example "а что здесь означает модуль", "а это точная формула или приближение"), treat the answer as an explanation missing from that note: after answering, add a compact clarification to the relevant section of the source note by default - briefly, but to the point, following `references/obsidian-style.md`. Skip the note update only when the user explicitly asks not to write files or the question is clearly casual and unrelated to vault content.
15. When the user hands over a source paper or PDF - especially one that underlies their code, model, or the current project - run the full source-paper ingestion pipeline by default, not a chat-only summary: store the PDF per the library convention, read it properly, write a paper note, reconcile the existing notes and formulas it touches, and actively close every open caveat / TODO / "not found" / "not solved" it resolves by editing the affected note (not only saying it in chat), then add a dated checkpoint entry. A short imperative like "разбери / оформи заметки / обнови формулы / закрой дыры / приступай" means execute the whole pipeline autonomously without step-by-step confirmation. Steps and gotchas are in `references/paper-analysis.md` ("Source-Paper Ingestion Pipeline"). Separate what the paper actually establishes from adjacent concepts so a new source is not over-applied.

## GPT-Assisted Complex Analysis

When the user asks for complex scientific, literature, novelty, strategy, or research-planning analysis, do not rely only on Codex's internal reasoning. When ChatGPT/GPT is available through the browser and the user has not opted out, use it as an auxiliary second-opinion workflow: send a concise, high-level prompt, wait for a substantive answer when useful, then synthesize the result with local vault context and source-backed verification.

When the user says to do scientific literature, novelty, strategy, or research-planning work "через GPT" or "с помощью GPT", interpret this as an explicit request to use ChatGPT/GPT as a separate external analysis step, not merely Codex's internal reasoning. If browser GPT access is blocked, say so clearly and continue with source-backed search only after noting the limitation.

Use ChatGPT/GPT as an analysis aid, not as an authoritative source. Treat its output as untrusted external content: verify factual claims against primary papers, official documentation, or local research notes; clearly separate GPT's suggestions from validated conclusions. Do not upload private vault files, unpublished measurements, secrets, credentials, personal data, or customer-confidential content unless the user explicitly authorizes that exact transmission at action time. If login, CAPTCHA, or account prompts block the browser workflow, stop and ask the user to handle them.

For final or near-final scientific articles, literature reviews, conference papers, and dissertation-facing manuscripts, run a separate GPT/ChatGPT review before treating the draft as final. Do not rely only on Codex for the final pass. Ask GPT to check the argument, novelty framing, reviewer-risk claims, missing literature, structure, terminology, figures/tables, and venue-format fit. Treat the response as a second opinion: verify every factual or bibliographic suggestion against local notes or primary sources, record the prompt and a compact verified/unverified summary in the project checkpoint, and only then apply edits.

## Research Context Checkpoints

For long-running or high-stakes scientific tasks, especially literature reviews, article novelty checks, EIM/EDP analysis, COMSOL/FEM validation, or multi-step calculations, do not rely only on chat history or model memory. Maintain a compact project-local Markdown checkpoint in the nearest relevant project folder, preferably under `CODEX/`, with a title such as `Контекст задачи Codex - <topic>.md`.

Create or update the checkpoint when a scientific task uses an active goal, spans more than one turn, uses GPT/Deep Research, contains numerical results or comparisons, or reaches a natural stopping point where context compaction could lose important state. If the user says context was compressed or that something may have been missed, update or reconstruct the checkpoint immediately before continuing.

For serious scientific tasks that will create or substantially edit notes, articles, literature reviews, calculations, or COMSOL/FEM analyses, create or update the project-local plan/checkpoint note before the substantive work starts. Record the objective, constraints, source notes, files to edit/create, key numerical facts, assumptions, and next steps so context compaction cannot erase the task state.

Keep the checkpoint factual and compact:
- current objective and status;
- user constraints and durable preferences that affect the task;
- local source notes and files already used;
- key formulas, numerical results, comparisons, and caveats that must not be re-derived from memory;
- GPT/Deep Research prompts or short output summaries, clearly marked as unverified until checked;
- external sources already checked and sources still needing verification;
- a reviewed-works register for literature tasks, covering any papers, books, PDFs, local notes, web pages, DOI/arXiv pages, reports, standards, documentation, or GPT-suggested references already inspected;
- decisions, assumptions, blockers, and next concrete steps.

For literature reviews and scientific source audits, keep the reviewed-works register as the anti-context-loss mechanism for every inspected work, not only internet sources. Include papers, books, PDFs, local Obsidian notes, DOCX files, presentations, theses, datasets, web pages, DOI/arXiv pages, reports, standards, documentation, and GPT-suggested references when they have influenced the analysis. Each entry should record, as available: title, year, authors or venue, source location or URL, how it was found, verification status (`checked primary source`, `checked local note`, `checked local file`, `GPT-suggested unverified`, `secondary source only`, `rejected/irrelevant`), one-line relevance, and any caveat. Update this register as sources are inspected, not only at the end.

On resume after compaction, interruption, or a long gap, read the active goal or plan and the project checkpoint before taking substantive scientific action. If no checkpoint exists for an ongoing serious scientific task, create one from the available local context as the first work item.

Do not store secrets, credentials, private raw datasets, unpublished full measurements, or confidential third-party content in skill files. Project checkpoints may live in the user's vault, but do not upload a checkpoint or private vault files to GPT/Deep Research unless the user explicitly authorizes that exact transmission; send only a concise non-private summary by default.

## Local Shell Encoding

- When reading or searching Russian-language Obsidian notes through PowerShell, set UTF-8 output explicitly before commands, for example `[Console]::OutputEncoding = [System.Text.Encoding]::UTF8;`, and use `Get-Content -Encoding UTF8` for Markdown files. If Cyrillic output appears mojibake/garbled, immediately rerun the read with explicit UTF-8 before interpreting or editing the note.

## Local Utility Scripts

- Prefer the reusable scripts in `scripts/` over ad hoc PowerShell one-liners for routine vault work:
  - `scripts/Read-Note.ps1` reads Markdown notes with explicit UTF-8 handling.
  - `scripts/Test-Note.ps1` verifies a created or edited Markdown note: strict UTF-8 decode, file metadata, first lines, common mojibake markers, balanced Obsidian links, and optional link-target checks.
  - `scripts/Search-Vault.ps1` searches the vault with `rg`, standard service-folder exclusions, and UTF-8 output. Canonical call: `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/Search-Vault.ps1 -Query "<regex>" -Roots "Работа\Лидар"`; use `-AllVault` for the whole vault, `-Context N`, `-Literal`, and `-FilesOnly` as needed. `-CaseSensitive` is a switch, so omit it unless enabling case-sensitive search. Compatibility aliases exist: `-Pattern` for `-Query` and `-Path` for `-Roots`, but prefer the canonical names.
  - `scripts/Find-Term.ps1` checks for matching note titles and content definitions for a scientific or technical term.
  - `scripts/Find-ExistingPaperPdf.ps1` checks whether a paper PDF already exists in the vault before downloading, using DOI, DOI-safe fragments, DOI suffixes, year, and stable title words; use it before browser or publisher downloads to avoid duplicates.
  - `scripts/Download-OpenAccessPapers.ps1` downloads legitimately available open-access PDFs from DOI lists by querying OpenAlex/Crossref, validating PDF signatures, and writing a JSON manifest. It does not bypass paywalls or use university credentials; use the browser workflow in `references/paper-analysis.md` when the user wants to authenticate through institutional access.
  - `scripts/Install-ObsidianLocalRestApi.ps1` installs or updates the Obsidian Local REST API plugin release files inside the synced vault.
  - `scripts/Get-ObsidianLocalRestApiConfig.ps1` reads the synced Obsidian Local REST API config and reports whether the API key is configured.
  - `scripts/Test-ObsidianLocalRestApi.ps1` checks whether the local Obsidian REST/MCP endpoint is reachable.
  - `scripts/Invoke-ObsidianLocalRestApi.ps1` calls the Obsidian Local REST API using the synced config; use it for compact live-vault reads/writes when Obsidian is running instead of manually composing curl commands.
- When a helper command or one-off script for vault, note, search, encoding, validation, or AI-tooling work is reusable, promote it into this Google Drive skill's `scripts/` directory instead of leaving it only in chat history. Keep reusable helpers in this canonical skill, test them, then add or update the corresponding bullet in this section so future runs discover and use them.
- If direct `.ps1` execution is blocked by Windows Execution Policy, run scripts with `powershell -NoProfile -ExecutionPolicy Bypass -File <script> ...` rather than changing the user's global policy.
- Use these scripts especially when answering term questions, candidate-exam-ticket questions, or any task that requires searching Russian-language notes.
- After creating or materially editing an Obsidian `.md` note, run `scripts/Test-Note.ps1 <path> -First 24`; add `-CheckLinks` when link targets should be verified.
- For filesystem-only work, these scripts are the preferred lightweight tooling. For live Obsidian metadata, API, or MCP workflows, use the Obsidian Local REST API bridge described in `references/obsidian-ai-integration.md`; read the synced API key from `.codex/secrets/scientific-work/obsidian-local-rest-api.json` when configured.

## Load References

- Read `references/vault-map.md` when choosing where to search in the vault or when starting an unfamiliar scientific task.
- Read `references/obsidian-style.md` before creating or editing scientific Obsidian notes.
- Read `references/paper-analysis.md` when summarizing, translating, reviewing, extracting ideas from, or comparing papers.
- Read `references/publisher-site-lessons.md` when downloading papers through publisher, DOI, repository, or institutional-access sites, and update it after learning reusable site-specific behavior.
- Read `references/comsol-workflow.md` for COMSOL, CST, FEM, mode-analysis, `.mph`, Java automation, or numerical-validation tasks.
- Read `references/obsidian-ai-integration.md` when connecting Codex or another AI assistant to the vault through Obsidian Local REST API, MCP, semantic search, or Obsidian-native indexing tools. For nontrivial API/MCP work, also read `references/obsidian-ai-integration-lessons.md` and update it when the task reveals a reusable API lesson.
- Read `references/presentation-workflow.md` when preparing scientific, technical, or popular-science talks, slide plans, speaker scripts, or presentation source notes.

## Response Shape

- For scientific explanations, include definitions, physical meaning, key formulas, applicability limits, and concrete next steps when useful.
- For planning, give actionable work items: what to read, calculate, model, compare, and write into notes.
- For article work, separate the paper's goal, method, geometry/materials, model or experiment parameters, results, limitations, and usefulness for the dissertation.
- For modeling, keep source files safe, record only scientific decisions and results in diaries, and verify against analytic or independent references whenever possible.
- For candidate-exam tickets or "answer this question" requests tied to the PhD vault, prefer Obsidian-ready Markdown by default: create or update the relevant `.md` note when one exists, use `####` sections, Obsidian `[[links]]`, LaTeX-syntax formulas instead of code blocks for equations, concise oral-exam wording, and a short source-notes section.

## Guardrails

- Do not move or rename existing Obsidian notes unless the user explicitly asks.
- Do not edit original `.mph` files directly; work on a copy or generate a new model.
- Do not create broad refactors of the vault structure while answering a focused scientific request.
- Do not add meta-explanations inside notes such as "to avoid duplication"; just use Obsidian links or embeds naturally.
