---
name: skill-management
description: Create and update the user's shared skill base and AI-specific thin adapters for Codex, Claude, and other agents. Use when the user asks to add, edit, persist, synchronize, relocate, or organize skills, especially when deciding where skills should live across PCs and Google Drive.
---

# Skill Management (Claude Code adapter)

Shared base skill: ../../../_base/skills/skill-management/SKILL.md.

When this skill triggers, read that base SKILL.md completely and follow it together with any references/, scripts/, and assets/ next to the base file. Resolve relative resource paths from the shared base skill directory.

Keep this file as a Claude-specific thin adapter: frontmatter and Claude-only trigger wording belong here; durable domain rules, reusable workflows, scripts, references, and lessons belong in the shared base skill.

Notes:
- Ignore agents/openai.yaml; it is Codex-only metadata in the Codex adapter.
- Update the shared base first for behavior changes, then adjust Codex/Claude adapters only when their platform-specific pointers or trigger descriptions need to change.