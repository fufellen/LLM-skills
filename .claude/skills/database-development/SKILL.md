---
name: database-development
description: Design, specify, build, and deploy databases and the applications around them. Use for база данных, БД, ТЗ на базу данных, SQL schema design, ER diagrams, PostgreSQL/SQLite/MySQL, CRUD record-keeping apps (students, teachers, lessons, payments, inventory, clients), server deployment of a database on a rented VPS, backups, migrations, and PC/mobile/web client apps over a database.
---

# Database Development (Claude Code adapter)

Shared base skill: ../../../_base/skills/database-development/SKILL.md.

When this skill triggers, read that base SKILL.md completely and follow it together with any references/, scripts/, and assets/ next to the base file. Resolve relative resource paths from the shared base skill directory.

Keep this file as a Claude-specific thin adapter: frontmatter and Claude-only trigger wording belong here; durable domain rules, reusable workflows, scripts, references, and lessons belong in the shared base skill.

Notes:
- Ignore agents/openai.yaml; it is Codex-only metadata in the Codex adapter.
- Update the shared base first for behavior changes, then adjust Codex/Claude adapters only when their platform-specific pointers or trigger descriptions need to change.
