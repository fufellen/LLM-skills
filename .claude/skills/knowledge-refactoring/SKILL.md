---
name: knowledge-refactoring
description: Refactor Obsidian vault notes and other knowledge bases into linked sources of truth. Use when the user asks to remove duplicates, consolidate notes, choose canonical notes, replace repeated explanations with [[Obsidian links]], audit stale facts against source files or code, or reorganize technical knowledge without moving files.
---

# Knowledge Refactoring (Claude Code pointer)

Canonical source of truth (Codex skill): `../../../knowledge-refactoring/SKILL.md` (relative to this repo root).

When this skill triggers, **read that file and follow it fully**, together with any `references/`, `scripts/`, and `assets/` next to it. Don't restate its rules here — always defer to the canonical Codex `SKILL.md` so Codex and Claude Code stay in sync.

Notes:
- Ignore `agents/openai.yaml` (Codex-only metadata).
- This `.claude/skills/` tree mirrors the Codex skills of this repo as Claude Code pointers; the Codex `SKILL.md` files remain the single source of truth.
