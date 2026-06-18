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

## Corporate Skills Submodule

The corporate skills repository is stored as a Git submodule inside the personal skills repository. Its root is the `nto-formatting` skill, and separately requested corporate skills may live as top-level skill folders inside that same checkout.

```text
Corporate source of truth: https://github.com/ak-tech-electronics/codex-skills
Personal repo with submodule: https://github.com/fufellen/codex-skills
Submodule path in personal repo: nto-formatting
```

The corporate repo root is the skill folder itself: it must contain `SKILL.md` at repo root, plus optional `agents/`, `references/`, `scripts/`, and `assets/` folders. Do not nest it as `nto-formatting/SKILL.md` inside the corporate repo.

Keep personal-repo details out of the corporate `nto-formatting` skill. The personal repository knows that it consumes the corporate repo as a submodule; the corporate repo should only describe itself as the NTO skill source of truth and may refer generically to downstream mirrors or submodules.

Use corporate skills in-place from the Git checkout where they were cloned. Do not copy corporate skill folders into a system skills directory as independent duplicates. If a system-level skills repository, registry, bootstrap folder, or local Codex configuration needs to expose a corporate skill, store only a lightweight pointer to the checked-out skill path, such as a path entry, manifest entry, symlink, or submodule pointer. Edit, validate, commit, and push the corporate checkout itself.

Do not pull the NTO submodule on every ordinary skill use. Use this freshness model instead:

- For normal NTO drafting or review, use the local submodule checkout as-is.
- Before editing the NTO skill, applying self-learning updates, or publishing changes, run `git -C nto-formatting fetch origin main`.
- Compare `git -C nto-formatting rev-parse HEAD` with `git -C nto-formatting rev-parse origin/main`.
- If the submodule is behind and clean, fast-forward it with `git -C nto-formatting merge --ff-only origin/main`.
- If the submodule is dirty, ahead, or diverged, stop and report the state before editing.
- Use `git submodule update --remote nto-formatting` only when the user explicitly asks to sync to the latest corporate version without making a skill edit.

If a merge conflict occurs while updating or publishing the corporate `nto-formatting` skill, resolve it autonomously when the intended result can be determined from the files, commit history, and the user's current instruction. Validate the corporate skill, then commit and push the corporate repo. Commit and push the updated submodule pointer only when the current workspace is a parent repository that actually consumes the corporate repo as a submodule. If the current workspace contains only the standalone corporate repo, no parent pointer exists and no pointer commit is needed. Stop only when the conflict requires guessing unavailable technical meaning, choosing between incompatible user instructions, exposing confidential data, or using unavailable repository permissions.

When `nto-formatting` is materially updated:

1. Work inside the submodule path or a fresh corporate repo clone.
2. Validate the skill in the corporate repo root.
3. Commit and push the corporate repo first.
4. If working inside a parent repo with `nto-formatting` as a submodule, return to that parent repo and verify that `nto-formatting` points at the new corporate commit.
5. Commit and push the updated submodule pointer only when such a parent repo exists.
6. Report the corporate commit hash and, when applicable, the parent repo pointer commit hash.

Do not duplicate the corporate NTO skill as ordinary tracked files in the personal repo. On a fresh clone of the personal repo, initialize submodules with `git submodule update --init --recursive`; when updating from the corporate `main` branch, use `git submodule update --remote nto-formatting`.

## Corporate LTspice Skill

The `ltspice-simulation` skill is corporate-primary and lives inside the corporate checkout at:

```text
C:\Users\User\Мой диск\Obsidian\.codex\skills\nto-formatting\ltspice-simulation
```

Do not keep an independent top-level duplicate at:

```text
C:\Users\User\Мой диск\Obsidian\.codex\skills\ltspice-simulation
```

For LTspice skill reads, edits, validation, commits, and pushes, work in the corporate checkout path. After publishing corporate changes, commit and push only the updated submodule pointer in the personal repository.

## Default Rule

- When creating a new user skill, place it under the Google Drive synced skill folder above unless the user explicitly asks for another location.
- When updating an existing user skill, prefer the Google Drive copy if one exists.
- Do not create independent duplicated skill instructions under `C:\Users\User\.codex\skills` unless the user explicitly asks.
- Treat local non-synced skill folders as temporary bootstrap pointers, cache, or system-managed content, not as the durable home for user preferences.
- Do not commit or push synced secrets; keep `secrets/` folders and local credential files ignored.
- If a user gives a durable preference about how skills should be created, updated, named, synced, or used, add it to this skill or the relevant domain skill without waiting for another reminder.
- When a new or existing skill needs self-learning, reusable lessons, or durable preference persistence, use the `skill-learning` skill instead of copying the full learning policy into every domain skill.

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

- `ltspice-simulation` currently lives inside the corporate checkout at:

```text
C:\Users\User\Мой диск\Obsidian\.codex\skills\nto-formatting\ltspice-simulation
```

- `skill-learning` currently lives at:

```text
C:\Users\User\Мой диск\Obsidian\.codex\skills\skill-learning
```

- Presentation workflow rules for scientific/popular-science decks currently live at:

```text
C:\Users\User\Мой диск\Obsidian\.codex\skills\scientific-work\references\presentation-workflow.md
```

## Creating New Skills

When creating a new skill from scratch:

1. Use the system `skill-creator` guidance.
2. Use `skill-learning` when the skill should persist reusable lessons, failure modes, commands, durable user preferences, or self-improvement behavior.
3. Initialize the skill in:

```text
C:\Users\User\Мой диск\Obsidian\.codex\skills
```

4. Keep `SKILL.md` concise.
5. Put detailed workflows in `references/`.
6. Put deterministic utilities in `scripts/`.
7. Put templates and reusable media in `assets/`.
8. Validate the skill with the skill-creator validation script when feasible.

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
- LTspice schematic and netlist simulation workflows: `nto-formatting/ltspice-simulation`;
- shared self-learning and reusable-lesson policy for skills: `skill-learning`;
- presentation-specific behavior for research talks: `scientific-work/references/presentation-workflow.md`;
- Obsidian REST/MCP bridge details: `scientific-work/references/obsidian-ai-integration.md`.
