---
name: pdf-textbook-to-markdown
description: Convert, extract, segment, clean up, and review PDF textbooks into Markdown or Obsidian notes. Use when Codex needs to process born-digital or scanned textbook PDFs, preserve page anchors, extract figures, handle OCR, split chapters into .md notes, clean headers/footers/hyphenation, convert formulas and tables where possible, or prepare source-backed study/research notes from a .pdf book.
---

# PDF Textbook To Markdown

## Core Goal

Turn a PDF textbook into useful, source-backed Markdown without silently losing structure. Preserve the original PDF, keep page-level traceability, prefer a faithful draft before cleanup, and mark uncertain OCR, formulas, tables, or figure captions instead of inventing missing content.

## Repository Model

This skill is stored in both the user's personal skills repository and the corporate skills repository. Keep the personal repository copy as the safety copy so work is not lost if corporate publishing, permissions, sync, or merge resolution fails. Keep both copies aligned when the user asks to publish or synchronize this skill across repositories, but do not delete the personal copy merely because the skill is mirrored to corporate.

## Workflow

1. Identify the source PDF, target folder, output style, language, and split policy: one Markdown file, one file per chapter, or an Obsidian index plus chapter notes.
2. Triage the PDF before conversion:

```powershell
python ".\scripts\extract_pdf_textbook.py" inspect "input.pdf"
```

3. Choose the extraction route:
   - Born-digital text: use the bundled script for a page-anchored draft and extracted images.
   - Scanned or low-text PDF: create a separate OCR copy first, then extract from the OCR PDF.
   - Math-heavy or table-heavy book: read `references/pdf-tooling.md` and choose a specialized route; keep screenshots or image fallbacks for content that cannot be converted safely.
4. Extract a first-pass Markdown draft:

```powershell
python ".\scripts\extract_pdf_textbook.py" extract "input.pdf" --output "book.md" --media-dir "book_media"
```

5. Restructure the draft into textbook notes. Use the PDF table of contents, bookmarks, or visible headings to create stable chapter/section boundaries. Keep page markers such as `<!-- source-page: 42 -->` near converted content.
6. Clean the Markdown: remove repeated running headers, page numbers, broken line wraps, OCR artifacts, bad hyphenation, and duplicate boilerplate. Convert formulas to KaTeX only when the result can be checked against the PDF.
7. Verify against the source. Compare representative pages, check image links, inspect headings, and keep a short source note with the PDF filename, page ranges, extraction/OCR method, and remaining manual-review items.

## Obsidian Conventions

- The extracted conversion note MUST link its source PDF with an Obsidian `[[filename.pdf]]` wikilink in the header (the `extract` command emits `> Source: [[<name>.pdf]]`), never a bare backtick path - a path string is not a backlink, so the source document shows no incoming links even though the whole study derives from it. When a separate analysis/paper note exists, cross-link it too. This mirrors the `obsidian-style.md` "Paper Notes" rule (explicit user requirement, 2026-07-09).
- Store media in a nearby folder such as `<book-stem>_media/`.
- Keep Obsidian attachment filenames short and stable, especially on Windows. Prefer names such as `<book-key>-fig-02-02.png` over caption-derived names; long full paths can fail in Obsidian/Electron even when the same files open in external viewers.
- Visually inspect extracted figure crops before relinking or translation. Page-region crops can accidentally include neighboring formulas, paragraphs, or captions; recrop/regenerate the PNG so only the figure artwork and its own internal labels remain.
- For Obsidian image embeds, use wikilinks with only the attachment filename, for example `![[Figure 2.2 - Geometry.png]]`; do not include `attachments/` or another media-folder prefix inside the wikilink. If filenames would collide in the vault, rename the extracted media files to unique descriptive names instead of path-qualifying the embed.
- When renaming or relinking extracted media for a book, update and verify every sibling or derived Markdown folder under the book root, including translations. Do not stop after the source Markdown folder; scan the full book root for old image embeds and validate that every linked filename exists and is unique in the vault.
- Use an index note for the book when splitting chapters. Link chapter files with `[[...]]` and include source page ranges.
- Prefer descriptive chapter filenames with stable ordering, for example `01 - Fundamentals.md`.
- Do not replace technical definitions with Obsidian links until canonical notes have been found or created.
- For Russian or multilingual textbooks, preserve the source language unless the user explicitly asks for translation.

## Tooling Reference

Read `references/pdf-tooling.md` when OCR is needed, formulas/tables are important, the PDF has weak text extraction, or the best toolchain is not obvious.

## Extraction Script

Use `scripts/extract_pdf_textbook.py` for repeatable local work:

- `inspect` reports page count, metadata, text-layer coverage, pages with little or no extractable text, and PDF outline entries when available.
- `extract` writes a page-anchored Markdown draft and, with PyMuPDF available, extracts embedded images.
- `check` verifies local Markdown image links and reports page-anchor counts.

The script prefers PyMuPDF (`pymupdf`) and falls back to `pypdf`/`PyPDF2` for text-only extraction when possible. If dependencies are missing, install the relevant package in the active Python environment instead of rewriting the workflow.

## Self-Improvement And Publishing

When PDF textbook work reveals a durable, reusable lesson, use the `skill-learning` policy. Save compact domain rules, command patterns, parser improvements, validation checks, or tooling notes in this skill or `references/pdf-tooling.md`; create `references/pdf-textbook-lessons.md` if lessons start to accumulate. Do not store private book text, copyrighted chapter content, credentials, extracted full chapters, or one-off project facts in the skill.

After materially updating this skill, validate it when feasible, then commit and push the relevant skill changes to the owning repository by default unless the user explicitly says not to. Stage only relevant skill files; never stage `secrets/`, API keys, local credentials, generated logs, extracted textbook text, or copyrighted source material.

Before materially editing this skill, applying self-learning updates, or publishing changes, run a lightweight freshness check like the NTO skill policy: fetch `origin main`, compare local `HEAD` with `origin/main`, fast-forward if local is behind and the relevant working tree is clean, and inspect dirty/ahead/diverged states before continuing. Leave unrelated user changes unstaged; stop and report only when target skill files or repository state make the intended update unsafe to determine.

If publishing encounters remote changes or merge conflicts, resolve them autonomously when the intended final meaning can be determined from the local changes, remote changes, commit history, and the user's instruction. Preserve compatible rules from both sides, consolidate duplicates, rerun validation, commit the resolved result, and push. Stop only when resolution would require guessing unavailable technical meaning, exposing protected content, discarding user work, or using unavailable repository permissions.
