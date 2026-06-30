---
name: knowledge-refactoring
description: Refactor Obsidian vault notes and other knowledge bases into linked sources of truth, and keep the vault clean. Use when the user asks to remove duplicates, consolidate notes, choose canonical notes, replace repeated explanations with [[Obsidian links]], audit stale facts against source files or code, reorganize technical knowledge without moving files, delete junk/temporary/backup files, or resolve sync "(conflict ...)" duplicate files.
---

# Knowledge Refactoring (Codex adapter)

Shared base skill: ../_base/skills/knowledge-refactoring/SKILL.md.

When this skill triggers, read that base SKILL.md completely and follow it together with any references/, scripts/, and assets/ next to the base file. Resolve relative resource paths from the shared base skill directory.

Keep this file as a Codex-specific thin adapter: frontmatter, trigger wording, and Codex-only metadata belong here; durable domain rules, reusable workflows, scripts, references, and lessons belong in the shared base skill.

Codex-specific notes:
- agents/openai.yaml is Codex UI metadata for this adapter.
- Update the shared base first for behavior changes, then adjust Codex/Claude adapters only when their platform-specific pointers or trigger descriptions need to change.