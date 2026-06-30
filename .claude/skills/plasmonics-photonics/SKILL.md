---
name: plasmonics-photonics
description: Specialized PhD/research workflow for plasmonics, nanophotonics, integrated photonics, SPP/ППП, DLSPP/DLSPPW, LR-DLSPP/LR-DLSPPW, MDM/MIM/IMI plasmonic waveguides, optical antennas, phase-change-material photonics and modulators (PCM, GST, GSST, Sb2S3, Sb2Se3, IST), EIM/ЭДП/effective-index screening, COMSOL/FEM/CST mode analysis, branch tracking, propagation loss, L_pi, insertion loss, and source-backed article or literature-review work in this domain.
---

# Plasmonics Photonics (Claude Code adapter)

Shared base skill: ../../../_base/skills/plasmonics-photonics/SKILL.md.

When this skill triggers, read that base SKILL.md completely and follow it together with any references/, scripts/, and assets/ next to the base file. Resolve relative resource paths from the shared base skill directory.

Keep this file as a Claude-specific thin adapter: frontmatter and Claude-only trigger wording belong here; durable domain rules, reusable workflows, scripts, references, and lessons belong in the shared base skill.

Notes:
- Ignore agents/openai.yaml; it is Codex-only metadata in the Codex adapter.
- Update the shared base first for behavior changes, then adjust Codex/Claude adapters only when their platform-specific pointers or trigger descriptions need to change.