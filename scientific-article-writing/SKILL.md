---
name: scientific-article-writing
description: Universal venue-agnostic discipline for preparing, reviewing, and QA-ing scientific manuscripts and conference papers. Use for написание статьи, подготовка рукописи, review or proofread an article draft, checking citation order and renumbering references, verifying table numbers against data files, syncing bilingual (RU/EN) drafts, pre-submission checklists, safe bulk edits of manuscript files, and DOCX artifact QA. Venue-specific rules (APEDE/IEEE, Оптика и спектроскопия) live in their dedicated skills and override this one; this skill is the shared base that prevents common manuscript mistakes.
---

# Scientific Article Writing (Codex adapter)

Shared base skill: ../_base/skills/scientific-article-writing/SKILL.md.

When this skill triggers, read that base SKILL.md completely and follow it together with any references/, scripts/, and assets/ next to the base file. Resolve relative resource paths from the shared base skill directory.

Keep this file as a Codex-specific thin adapter: frontmatter, trigger wording, and Codex-only metadata belong here; durable domain rules, reusable workflows, scripts, references, and lessons belong in the shared base skill.

Codex-specific notes:
- agents/openai.yaml is Codex UI metadata for this adapter.
- Update the shared base first for behavior changes, then adjust Codex/Claude adapters only when their platform-specific pointers or trigger descriptions need to change.
