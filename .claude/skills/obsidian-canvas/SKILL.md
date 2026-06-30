---
name: obsidian-canvas
description: Create, edit, reorganize, validate, and maintain Obsidian .canvas files. Use when you need to turn notes, outlines, tables, protocols, architectures, or process descriptions into Obsidian Canvas nodes and edges; adjust Canvas layouts such as top-down trees or horizontal main splits with deeper detail levels; repair Canvas JSON; or inspect/validate .canvas structure.
---

# Obsidian Canvas (Claude Code adapter)

Shared base skill: ../../../_base/skills/obsidian-canvas/SKILL.md.

When this skill triggers, read that base SKILL.md completely and follow it together with any references/, scripts/, and assets/ next to the base file. Resolve relative resource paths from the shared base skill directory.

Keep this file as a Claude-specific thin adapter: frontmatter and Claude-only trigger wording belong here; durable domain rules, reusable workflows, scripts, references, and lessons belong in the shared base skill.

Notes:
- Ignore agents/openai.yaml; it is Codex-only metadata in the Codex adapter.
- Update the shared base first for behavior changes, then adjust Codex/Claude adapters only when their platform-specific pointers or trigger descriptions need to change.