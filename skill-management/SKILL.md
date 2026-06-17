---
name: skill-management
description: Create and update Codex user skills, skill references, scripts, and assets. Use when the user asks to add, edit, persist, synchronize, relocate, or organize skills, especially when deciding where skills should live across PCs and Google Drive.
---

# Skill Management

## Canonical Location

Create and update user-owned Codex skills in the Google Drive synced Obsidian vault by default:

```text
C:\Users\User\Мой диск\Obsidian\.codex\skills
```

This synced folder is the canonical source of truth for the user's personal skills. It lets the user keep the same skill instructions, scripts, references, assets, and tool notes across PCs through Google Drive synchronization.

## GitHub Mirror

The Google Drive skill folder is also mirrored to GitHub:

```text
https://github.com/fufellen/codex-skills
```

Local git repository path:

```text
C:\Users\User\Мой диск\Obsidian\.codex\skills
```

After materially creating or updating user-owned skills, commit and push the skill changes to this repository by default unless the user explicitly says not to. Before committing:

1. Check `git status --short`.
2. Make sure `secrets/`, API keys, tokens, local credentials, caches, and generated logs are not staged.
3. Stage only relevant skill files and repo metadata.
4. Use a concise commit message describing the skill update.
5. Push to `origin main`.

If push fails because credentials, network, or remote permissions are unavailable, keep the local commit if it was created and report the exact blocker.

## Corporate NTO Mirror

The `nto-formatting` skill must stay synchronized between the personal and corporate skill repositories:

```text
https://github.com/fufellen/codex-skills
https://github.com/ak-tech-electronics/codex-skills
```

When `nto-formatting` is materially updated, push the update to the personal repo first, then duplicate the same `nto-formatting` folder to the corporate repo and push it there too. Keep the corporate repo limited to `nto-formatting` unless the user explicitly asks to add more. Report both commit hashes.

## Default Rule

- When creating a new user skill, place it under the Google Drive synced skill folder above unless the user explicitly asks for another location.
- When updating an existing user skill, prefer the Google Drive copy if one exists.
- Do not create independent duplicated skill instructions under `C:\Users\User\.codex\skills` unless the user explicitly asks.
- Treat local non-synced skill folders as temporary bootstrap pointers, cache, or system-managed content, not as the durable home for user preferences.
- Do not commit or push synced secrets; keep `secrets/` folders and local credential files ignored.
- If a user gives a durable preference about how skills should be created, updated, named, synced, or used, add it to this skill or the relevant domain skill without waiting for another reminder.

## Existing Google Drive Skills

- `scientific-work` currently lives at:

```text
C:\Users\User\Мой диск\Obsidian\.codex\skills\scientific-work
```

- `knowledge-refactoring` currently lives at:

```text
C:\Users\User\Мой диск\Obsidian\.codex\skills\knowledge-refactoring
```

- `nto-formatting` currently lives at:

```text
C:\Users\User\Мой диск\Obsidian\.codex\skills\nto-formatting
```

- Presentation workflow rules for scientific/popular-science decks currently live at:

```text
C:\Users\User\Мой диск\Obsidian\.codex\skills\scientific-work\references\presentation-workflow.md
```

## Creating New Skills

When creating a new skill from scratch:

1. Use the system `skill-creator` guidance.
2. Initialize the skill in:

```text
C:\Users\User\Мой диск\Obsidian\.codex\skills
```

3. Keep `SKILL.md` concise.
4. Put detailed workflows in `references/`.
5. Put deterministic utilities in `scripts/`.
6. Put templates and reusable media in `assets/`.
7. Validate the skill with the skill-creator validation script when feasible.

## Updating Existing Skills

Before editing a skill:

1. Check whether a Google Drive version exists.
2. Edit the Google Drive version first.
3. Avoid editing system skills under `.system` unless the user explicitly asks and the file is intended to be user-modifiable.
4. After updating, tell the user exactly which skill or reference file changed.

## Cross-PC Expectations

For a skill to be useful on another PC:

- its folder should be inside the synced Google Drive skill root;
- scripts and references should use relative paths where possible;
- absolute paths may mention the expected vault root, but should explain that Google Drive sync must place the vault at the same or adapted path;
- secrets should not be duplicated unless the user explicitly requests synced secrets for convenience;
- if a local connector or plugin is required, document how to test it from the synced skill.

## Relationship To Domain Skills

Use this skill for general rules about skill storage and synchronization. Use domain skills for domain behavior:

- scientific notes, papers, PhD work, Obsidian research workflows: `scientific-work`;
- scientific and technical report / NTO formatting: `nto-formatting`;
- presentation-specific behavior for research talks: `scientific-work/references/presentation-workflow.md`;
- Obsidian REST/MCP bridge details: `scientific-work/references/obsidian-ai-integration.md`.
