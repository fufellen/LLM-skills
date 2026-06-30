---
name: markdown-to-docx
description: Create, convert, polish, and validate Microsoft Word .docx documents from Markdown .md drafts, Obsidian notes, scientific/technical articles, reports, and conference materials. Use when Codex needs to turn Markdown into a clean DOCX, apply a Word reference/template, preserve headings/lists/tables/images where possible, sanitize Markdown or LaTeX-like artifacts such as escaped pipes, raw underscores in formulas like SiO_2 or lambda_0, or QA a generated Word document before delivery.
---

# Markdown To DOCX

## Core Workflow

1. Preserve the source `.md`; write the generated `.docx` beside it or to the explicitly requested path.
2. Inspect whether the user expects a template/reference document. If a `.docx` template is supplied, use it as Pandoc `--reference-doc` or match its style manually.
3. Prefer Pandoc for production conversion when available:

```powershell
python ".\scripts\convert_md_to_docx.py" "input.md" --output "output.docx" --reference-doc "template.docx"
```

4. If Pandoc is unavailable and a simple document is acceptable, use the script's basic DOCX writer. It supports headings, paragraphs, simple lists, simple pipe tables, captions, code blocks, and formula-like subscripts.
5. After conversion, validate the generated DOCX. Treat raw Markdown/LaTeX leftovers as defects, especially escaped pipes, raw formula underscores, raw `$...$` math, broken captions, and image-only placeholders.

## Artifact Rules

- Never let Markdown escape syntax become visible Word text. Convert `air\ |\ PCM\ |\ SiO_2` into readable text such as `air | PCM | SiO_2` with the `2` rendered as a subscript or Word equation text.
- Do not place layer-stack, equation, or list lines immediately after a figure caption unless they are part of the caption. If Markdown conversion causes them to appear under the caption, move them back into the body text before or after the figure.
- Render scientific tokens such as `SiO_2`, `lambda_0`, `k_0`, `n_eff`, `L_pi`, and `L_power` as Word subscripts, Unicode-safe text, or equation objects. Plain underscores are acceptable only in file names, code, identifiers, or explicit user-requested literal text.
- For final scientific papers, replace important display equations with Word equation objects when feasible. If that is not feasible in the current run, leave a clear follow-up note in the document or report it to the user.
- When generating a camera-ready document, unzip or programmatically inspect `word/document.xml` and search for `\|`, `\ |`, raw formula underscores, and raw Markdown markers before saying the DOCX is ready.

## Detailed Guidance

Read `references/conversion-checklist.md` when the task involves a publication, report, thesis material, image captions, equations, tables, or a user complaint about bad DOCX formatting.

Use the conversion script for repeatable work:

```powershell
python ".\scripts\convert_md_to_docx.py" "input.md" --output "output.docx" --method auto --strict
```

Useful options:

- `--reference-doc <file.docx>`: apply a Word reference document when Pandoc is available.
- `--method pandoc`: require Pandoc and fail if it is missing.
- `--method basic`: use the built-in lightweight DOCX writer.
- `--keep-sanitized`: save the sanitized Markdown beside the output for inspection.
- `--strict`: return a nonzero exit code if post-conversion artifact checks find suspicious text.

## Self-Improvement And Publishing

When Markdown-to-DOCX work reveals a durable, reusable lesson, use the `skill-learning` policy. Save compact domain rules, command patterns, parser improvements, validation checks, reusable examples, or tooling notes in this skill or a focused `references/` file. Do not store secrets, credentials, private content, copyrighted source text, generated logs, raw project/customer material, unpublished measurements, or one-off facts in the skill.

Before materially editing this skill, applying self-learning updates, or publishing changes, run the owning repository's freshness check: fetch `origin main`, compare local `HEAD` with `origin/main`, fast-forward if local is behind and the relevant working tree is clean, and inspect dirty/ahead/diverged states before continuing.

After materially updating this skill, validate it when feasible, then commit and push the relevant skill changes to the owning repository by default unless the user explicitly says not to. Stage only relevant skill files and repository metadata.

If publishing encounters remote changes or merge conflicts, resolve them autonomously when the intended final meaning can be determined from the files, commit history, nearby rules, and the user's instruction. Preserve compatible rules from both sides, consolidate duplicates, rerun validation, commit the resolved result, and push. Stop only when resolution would require guessing unavailable technical meaning, exposing protected content, discarding user work, or using unavailable repository permissions.
