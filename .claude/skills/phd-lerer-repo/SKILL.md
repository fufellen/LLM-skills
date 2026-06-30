---
name: phd-lerer-repo
description: Maintain the user's `fufellen/phd_lerer` GitHub repository for PhD/Lerer calculation programs. Use when you need to move, add, validate, document, commit, or push C, Python, COMSOL Java, EDP/EIM, plasmonic-waveguide, or other reproducible scientific calculation code into `phd_lerer`, keep README files current, or decide which generated artifacts belong in Git.
---

# PhD Lerer Repo (Claude Code adapter)

Shared base skill: ../../../_base/skills/phd-lerer-repo/SKILL.md.

When this skill triggers, read that base SKILL.md completely and follow it together with any references/, scripts/, and assets/ next to the base file. Resolve relative resource paths from the shared base skill directory.

Keep this file as a Claude-specific thin adapter: frontmatter and Claude-only trigger wording belong here; durable domain rules, reusable workflows, scripts, references, and lessons belong in the shared base skill.

Notes:
- Ignore agents/openai.yaml; it is Codex-only metadata in the Codex adapter.
- Update the shared base first for behavior changes, then adjust Codex/Claude adapters only when their platform-specific pointers or trigger descriptions need to change.