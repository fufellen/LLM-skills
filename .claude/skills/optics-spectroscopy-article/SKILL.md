---
name: optics-spectroscopy-article
description: Prepare, format, review, and package a journal article for «Оптика и спектроскопия» (Optics and Spectroscopy, Ioffe Institute) and structurally similar Ioffe journals (ЖТФ, ФТТ, ФТП). Use for статья в Оптика и спектроскопия, правила для авторов journals.ioffe.ru, структура рукописи, СПИСОК ЛИТЕРАТУРЫ по правилам ОиС, подача через OJS, сопроводительные документы, submission package/checklist, converting an Obsidian draft note into a submission-ready DOCX manuscript with correctly formatted title block, abstract, formulas, tables, figures, and references.
---

# Optics And Spectroscopy Article (Claude Code adapter)

Shared base skill: ../../../_base/skills/optics-spectroscopy-article/SKILL.md.

When this skill triggers, read that base SKILL.md completely and follow it together with any references/, scripts/, and assets/ next to the base file. Resolve relative resource paths from the shared base skill directory.

Keep this file as a Claude-specific thin adapter: frontmatter and Claude-only trigger wording belong here; durable domain rules, reusable workflows, scripts, references, and lessons belong in the shared base skill.

Notes:
- Ignore agents/openai.yaml; it is Codex-only metadata in the Codex adapter.
- Update the shared base first for behavior changes, then adjust Codex/Claude adapters only when their platform-specific pointers or trigger descriptions need to change.
