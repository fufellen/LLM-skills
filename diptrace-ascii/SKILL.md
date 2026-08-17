---
name: diptrace-ascii
description: Inspect, audit, safely edit, and validate DipTrace Schematic ASCII .asc files. Use for DipTrace ASCII netlist reconstruction, component and pin mapping, Cyrillic-to-Latin normalization, encoding-preserving edits, footprint/pad and component-height checks, datasheet-backed electrical review, BOM metadata checks, or diagnosing logical schematic errors beyond visible wire connectivity.
---

# DipTrace ASCII (Codex adapter)

Shared base skill: ../_base/skills/diptrace-ascii/SKILL.md.

When this skill triggers, read that base `SKILL.md` completely and follow it together with the necessary files under its `references/` and `scripts/` directories. Resolve relative resource paths from the shared-base skill directory.

Keep this adapter thin. Codex UI metadata belongs in `agents/openai.yaml`; durable format knowledge, audit rules, scripts, and reusable lessons belong in the shared base.
