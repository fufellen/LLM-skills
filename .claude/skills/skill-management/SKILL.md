---
name: skill-management
description: Create and update the user's personal skills, references, scripts, and assets. Use when the user asks to add, edit, persist, synchronize, relocate, or organize skills, especially when deciding where skills should live across PCs and Google Drive.
---

# Skill Management (Claude Code pointer)

Canonical source of truth (Codex skill): `../../../skill-management/SKILL.md` (relative to this repo root).

When this skill triggers, **read that file and follow it fully**, together with any `references/`, `scripts/`, and `assets/` next to it. Don't restate its rules here — always defer to the canonical Codex `SKILL.md` so Codex and Claude Code stay in sync.

Notes:
- Ignore `agents/openai.yaml` (Codex-only metadata).
- This is a meta-skill. When a canonical skill is added/moved/renamed, update its matching `.claude/skills` pointer too.
