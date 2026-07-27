---
name: engineering-simulator-development
description: Design, implement, validate, package, and maintain source-faithful engineering simulators and digital twins. Use for симулятор, эмулятор, цифровой двойник, optomechanical/LiDAR/scanner/ray simulators, hardware or FPGA/firmware behavior emulation, calibration tables, fixed-point interpolation, device-protocol reconstruction, engineering GUI visualization, and reproducible Windows EXE delivery.
---

# Engineering Simulator Development (Codex adapter)

Shared base skill: ../_base/skills/engineering-simulator-development/SKILL.md.

When this skill triggers, read that base `SKILL.md` completely and follow it. Load the referenced fidelity, scanning/LiDAR, and Windows-release files according to the routing rules in the shared base. Resolve relative resource paths from the shared-base skill directory.

Keep this adapter thin. Store durable domain behavior, reusable workflows, references, scripts, and lessons in the shared base.

Codex-specific notes:
- `agents/openai.yaml` is Codex UI metadata for this adapter.
- Update the shared base first; change this adapter only when trigger wording, metadata, or platform-specific routing changes.
