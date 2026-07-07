---
name: presentation-creation
description: Create, review, improve, regenerate, and verify presentations and slide decks. Use when Claude works with PowerPoint .pptx files, Google Slides, Canva decks, slide plans, speaker notes, visual prompts, or requests in Russian such as "презентация", "слайды", "переделай презентацию", "посмотри презентацию", or "создай презентацию", especially when local vault knowledge, existing decks, GPT/browser image work, or copy-preserving edits are involved.
---

# Presentation Creation (Claude Code adapter)

Shared base skill: ../../../_base/skills/presentation-creation/SKILL.md.

When this skill triggers, read that base SKILL.md completely and follow it together with any references/, scripts/, and assets/ next to the base file. Resolve relative resource paths from the shared base skill directory.

Keep this file as a Claude-specific thin adapter: frontmatter and Claude-only trigger wording belong here; durable domain rules, reusable workflows, scripts, references, and lessons belong in the shared base skill.

Notes:
- Ignore agents/openai.yaml; it is Codex-only metadata in the Codex adapter.
- Update the shared base first for behavior changes, then adjust Codex/Claude adapters only when their platform-specific pointers or trigger descriptions need to change.
