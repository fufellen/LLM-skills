---
name: skill-learning
description: Shared self-learning and reusable-lesson policy for the user's skills. Use when creating or updating a skill that should persist durable lessons, user preferences, reusable commands, failure modes, validation rules, or self-improvement behavior without duplicating the same learning instructions in every domain skill.
---

# Skill Learning (Claude Code pointer)

Canonical source of truth (Codex skill): `../../../skill-learning/SKILL.md` (relative to this repo root).

When this skill triggers, **read that file and follow it fully**, together with any `references/`, `scripts/`, and `assets/` next to it. Don't restate its rules here — always defer to the canonical Codex `SKILL.md` so Codex and Claude Code stay in sync.

Notes:
- Ignore `agents/openai.yaml` (Codex-only metadata).
- This is a meta-skill (shared self-learning policy). Persist durable lessons in the canonical Codex `SKILL.md`; keep the matching `.claude/skills` pointer in sync if a description changes.
