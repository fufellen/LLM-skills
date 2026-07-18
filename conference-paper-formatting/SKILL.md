---
name: conference-paper-formatting
description: Prepare, format, review, and validate compact two-column conference-paper manuscripts in DOCX using the user's stored example. Use for requests such as оформить доклад для конференции, текст доклада, рукопись доклада, убрать авторов и титульный блок, начать сразу с введения, закончить списком литературы, reproduce the CJE_KB_CMP layout, or check a DOCX against that layout. This skill is for a proceedings manuscript, not a slide presentation.
---

# Conference Paper Formatting (Codex adapter)

Shared base skill: ../_base/skills/conference-paper-formatting/SKILL.md.

When this skill triggers, read that shared-base `SKILL.md` completely and follow it together with the files it requires from `references/`, `scripts/`, and any other bundled folders. Resolve relative paths from the shared-base skill directory.

Keep this adapter thin. Store durable formatting rules, validators, examples, and lessons only in the shared base.

Codex-specific notes:
- `agents/openai.yaml` contains Codex UI metadata.
- Use the workspace document runtime when building or inspecting DOCX files.
