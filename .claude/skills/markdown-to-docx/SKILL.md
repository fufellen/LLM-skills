---
name: markdown-to-docx
description: Create, convert, polish, and validate Microsoft Word .docx documents from Markdown .md drafts, Obsidian notes, scientific/technical articles, reports, and conference materials. Use when you need to turn Markdown into a clean DOCX, apply a Word reference/template, preserve headings/lists/tables/images where possible, sanitize Markdown or LaTeX-like artifacts such as escaped pipes, raw underscores in formulas like SiO_2 or lambda_0, or QA a generated Word document before delivery.
---

# Markdown To DOCX (Claude Code adapter)

Shared base skill: ../../../_base/skills/markdown-to-docx/SKILL.md.

When this skill triggers, read that base SKILL.md completely and follow it together with any references/, scripts/, and assets/ next to the base file. Resolve relative resource paths from the shared base skill directory.

Keep this file as a Claude-specific thin adapter: frontmatter and Claude-only trigger wording belong here; durable domain rules, reusable workflows, scripts, references, and lessons belong in the shared base skill.

Notes:
- Ignore agents/openai.yaml; it is Codex-only metadata in the Codex adapter.
- Update the shared base first for behavior changes, then adjust Codex/Claude adapters only when their platform-specific pointers or trigger descriptions need to change.