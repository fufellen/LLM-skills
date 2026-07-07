---
name: christian-presentations
description: Prepare, review, improve, and verify Christian, church, Bible, Sunday school, youth, sermon, camp, and devotional presentations. Use for decks about Scripture, biblical stories, Christian teaching, воскресная школа, церковь, библейский урок, христианская презентация, Рожкао, ВШ, проповедь, or church children/youth materials, especially when slide text should quote the Bible accurately and use the user's local church/vault materials.
---

# Christian Presentations (Claude Code adapter)

Shared base skill: ../../../_base/skills/christian-presentations/SKILL.md.

When this skill triggers, read that base SKILL.md completely and follow it together with any references/, scripts/, and assets/ next to the base file. Resolve relative resource paths from the shared base skill directory.

Keep this file as a Claude-specific thin adapter: frontmatter and Claude-only trigger wording belong here; durable domain rules, reusable workflows, scripts, references, and lessons belong in the shared base skill.

Notes:
- Ignore agents/openai.yaml; it is Codex-only metadata in the Codex adapter.
- Update the shared base first for behavior changes, then adjust Codex/Claude adapters only when their platform-specific pointers or trigger descriptions need to change.
