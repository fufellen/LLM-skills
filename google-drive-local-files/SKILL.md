---
name: google-drive-local-files
description: Work with the user's Google Drive through the local synced filesystem rooted at `C:\Users\User\Мой диск`, not through the native Google Drive/Docs/Sheets/Slides connector. Use when the user asks to inspect, search, clean, organize, audit, delete, move, deduplicate, inventory, or find junk in Google Drive, My Drive, `Мой диск`, `гугл диск`, or `гугл хранилище`, especially when they say to work through files on the PC.
---

# Google Drive Local Files (Codex adapter)

Shared base skill: ../_base/skills/google-drive-local-files/SKILL.md.

When this skill triggers, read that base SKILL.md completely and follow it together with any references/, scripts/, and assets/ next to the base file. Resolve relative resource paths from the shared base skill directory.

Keep this file as a Codex-specific thin adapter: frontmatter, trigger wording, and Codex-only metadata belong here; durable domain rules, reusable workflows, scripts, references, and lessons belong in the shared base skill.

Codex-specific notes:
- agents/openai.yaml is Codex UI metadata for this adapter.
- Update the shared base first for behavior changes, then adjust Codex/Claude adapters only when their platform-specific pointers or trigger descriptions need to change.
