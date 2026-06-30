---
name: skill-authoring
description: Create, update, validate, self-improve, publish, and maintain user-owned shared skills plus Codex/Claude thin adapters with the user's defaults. Use when asked to create a new skill, update an existing skill, scaffold shared-base SKILL.md resources or AI-specific adapters, add durable skill lessons, set up self-learning behavior, run skill validation, commit and push skill repository changes, or resolve skill repository merge conflicts.
---

# Skill Authoring (Codex adapter)

Shared base skill: ../_base/skills/skill-authoring/SKILL.md.

When this skill triggers, read that base SKILL.md completely and follow it together with any references/, scripts/, and assets/ next to the base file. Resolve relative resource paths from the shared base skill directory.

Keep this file as a Codex-specific thin adapter: frontmatter, trigger wording, and Codex-only metadata belong here; durable domain rules, reusable workflows, scripts, references, and lessons belong in the shared base skill.

Codex-specific notes:
- agents/openai.yaml is Codex UI metadata for this adapter.
- Update the shared base first for behavior changes, then adjust Codex/Claude adapters only when their platform-specific pointers or trigger descriptions need to change.