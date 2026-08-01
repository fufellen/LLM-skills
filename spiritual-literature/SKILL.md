---
name: spiritual-literature
description: Read, write, review, and quote from Christian spiritual literature — sermons, teacher notes, devotionals, Bible studies, systematic theology, catechesis, homiletics, apologetics, and church camp/Sunday-school materials. Use for проповедь, конспект проповеди, богословие, толкование, библейское исследование, курс библейского института, воскресная школа, лагерь, катехизация, or any note under `Церковь/`, `Литература/духовная/`, or with a `Проповедь …` prefix, especially when the text must quote Scripture accurately. All Bible references are resolved from the user's local Synodal Bible at `Церковь/Библия/Библия/`.
---

# Spiritual Literature (Codex adapter)

Shared base skill: ../_base/skills/spiritual-literature/SKILL.md.

When this skill triggers, read that base SKILL.md completely and follow it together with any references/, scripts/, and assets/ next to the base file. Resolve relative resource paths from the shared base skill directory.

Keep this file as a Codex-specific thin adapter: frontmatter, trigger wording, and Codex-only metadata belong here; durable domain rules, reusable workflows, scripts, references, and lessons belong in the shared base skill.

Codex-specific notes:
- agents/openai.yaml is Codex UI metadata for this adapter.
- Update the shared base first for behavior changes, then adjust Codex/Claude adapters only when their platform-specific pointers or trigger descriptions need to change.
