---
name: modelsim
description: Work efficiently in ModelSim (Intel FPGA Starter Edition 10.5b) for Verilog/SystemVerilog testbench simulation. Use for vsim, vlog, vlib, vmap, .do files, headless/batch simulation runs, wave/WLF workflows, dataset comparison, VCD export, modelsim.ini tuning, transcript/exit-code automation, DPI-C builds, SDF/gate-level timing runs, ModelSim error diagnosis (verror, _lock, bad magic number), and any "how do I do X in ModelSim" question.
---

# ModelSim Productivity (Claude Code pointer)

Canonical source of truth (shared with Codex): `.codex/skills/_base/skills/modelsim/SKILL.md`

When this skill triggers, **read that file and follow it fully**, together with `references/modelsim-productivity.md` and `assets/run_tb_template.do` in that folder. Do not restate its rules here — always defer to the canonical file so Codex and Claude Code stay in sync.

Adaptations for this environment:
- Ignore `agents/openai.yaml` (Codex-only metadata, lives in the Codex adapter).
- Absolute paths written as `C:\Users\User\Мой диск\Obsidian\...` refer to this vault; here the root is the current working directory.
- Repo-specific ModelSim facts for `C:\workspace\verilog` stay canonical in `C:\workspace\verilog\docs\modelsim.md` and the `fpga-dev` skill.
