---
name: markdown-to-docx
description: Create, convert, polish, and validate Microsoft Word .docx documents from Markdown .md drafts, Obsidian notes, scientific/technical articles, reports, and conference materials. Use when Codex needs to turn Markdown into a clean DOCX, apply a Word reference/template, preserve headings/lists/tables/images where possible, sanitize Markdown or LaTeX-like artifacts such as escaped pipes, raw underscores in formulas like SiO_2 or lambda_0, or QA a generated Word document before delivery.
---

# Markdown To DOCX (Codex adapter)

Shared base skill: ../_base/skills/markdown-to-docx/SKILL.md.

When this skill triggers, read that base SKILL.md completely and follow it together with any references/, scripts/, and assets/ next to the base file. Resolve relative resource paths from the shared base skill directory.

Keep this file as a Codex-specific thin adapter: frontmatter, trigger wording, and Codex-only metadata belong here; durable domain rules, reusable workflows, scripts, references, and lessons belong in the shared base skill.

Codex-specific notes:
- agents/openai.yaml is Codex UI metadata for this adapter.
- Update the shared base first for behavior changes, then adjust Codex/Claude adapters only when their platform-specific pointers or trigger descriptions need to change.