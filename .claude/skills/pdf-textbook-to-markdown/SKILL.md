---
name: pdf-textbook-to-markdown
description: Convert, extract, segment, clean up, and review PDF textbooks into Markdown or Obsidian notes. Use when you need to process born-digital or scanned textbook PDFs, preserve page anchors, extract figures, handle OCR, split chapters into .md notes, clean headers/footers/hyphenation, convert formulas and tables where possible, or prepare source-backed study/research notes from a .pdf book.
---

# PDF Textbook To Markdown (Claude Code adapter)

Shared base skill: ../../../_base/skills/pdf-textbook-to-markdown/SKILL.md.

When this skill triggers, read that base SKILL.md completely and follow it together with any references/, scripts/, and assets/ next to the base file. Resolve relative resource paths from the shared base skill directory.

Keep this file as a Claude-specific thin adapter: frontmatter and Claude-only trigger wording belong here; durable domain rules, reusable workflows, scripts, references, and lessons belong in the shared base skill.

Notes:
- Ignore agents/openai.yaml; it is Codex-only metadata in the Codex adapter.
- Update the shared base first for behavior changes, then adjust Codex/Claude adapters only when their platform-specific pointers or trigger descriptions need to change.