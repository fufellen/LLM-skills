---
name: skill-authoring
description: Create, update, validate, self-improve, publish, and maintain the user's personal skills with their defaults. Use when asked to create a new skill, update an existing skill, scaffold SKILL.md/resources metadata, add durable skill lessons, set up self-learning behavior, run skill validation, commit and push skill repository changes, or resolve skill repository merge conflicts.
---

# Skill Authoring (Claude Code pointer)

Canonical source of truth (Codex skill): `../../../skill-authoring/SKILL.md` (relative to this repo root).

When this skill triggers, **read that file and follow it fully**, together with any `references/`, `scripts/`, and `assets/` next to it. Don't restate its rules here — always defer to the canonical Codex `SKILL.md` so Codex and Claude Code stay in sync.

Notes:
- Ignore `agents/openai.yaml` (Codex-only metadata).
- This is a meta-skill. When authoring/updating a skill, edit the canonical Codex `SKILL.md` and keep its matching `.claude/skills` pointer in sync.
