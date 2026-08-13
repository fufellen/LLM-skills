---
name: dsview
description: Capture and read logic-analyzer data from a DreamSourceLab DSLogic Plus headlessly via sigrok-cli, without the DSView GUI. Use for .sr/.dsl captures, choosing sample rate, decoding UART/SPI from a capture, and for diagnosing a DSLogic that stops responding (dark LED, "No devices found", scan hanging, LIBUSB_ERROR_NOT_SUPPORTED).
---

# DSLogic Plus из CLI (Claude Code pointer)

Canonical source of truth (shared with Codex): `.codex/skills/_base/skills/dsview/SKILL.md`

When this skill triggers, **read that file and follow it fully**. Do not restate
its rules here — always defer to the canonical file so Codex and Claude Code
stay in sync.

Adaptations for this environment:
- Ignore `agents/openai.yaml` (Codex-only metadata, lives in the Codex adapter).
- Проектная копия с конкретными путями и скриптами — репозиторий
  `C:\workspace\verilog`: вход `docs/skills/dsview/workflow.md`, подробности
  `docs/skills/dsview/dslogic-plus-cli.md`, скрипты `scripts/dsview/`.
  Новые проверенные факты писать в ОБА места: сюда (знание об инструменте) и в
  репозиторий (пути, скрипты, привязка к стенду).
