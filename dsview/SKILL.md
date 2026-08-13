---
name: dsview
description: Capture and read logic-analyzer data from a DreamSourceLab DSLogic Plus headlessly via sigrok-cli, without the DSView GUI. Use for .sr/.dsl captures, choosing sample rate, decoding UART/SPI from a capture, and for diagnosing a DSLogic that stops responding (dark LED, "No devices found", scan hanging, LIBUSB_ERROR_NOT_SUPPORTED).
---

# DSLogic Plus из CLI (Codex adapter)

Shared base skill: ../_base/skills/dsview/SKILL.md.

When this skill triggers, read that base SKILL.md completely and follow it together with any references/, scripts/, and assets/ next to the base file. Resolve relative resource paths from the shared base skill directory.

Keep this file as a Codex-specific thin adapter: frontmatter, trigger wording, and Codex-only metadata belong here; durable domain rules, reusable workflows, scripts, references, and lessons belong in the shared base skill.

Проектная копия с путями и скриптами конкретного стенда — репозиторий `C:\workspace\verilog`: `docs/skills/dsview/workflow.md`, `docs/skills/dsview/dslogic-plus-cli.md`, `scripts/dsview/`.
