---
name: plasmonics-photonics
description: Specialized PhD/research workflow for plasmonics, nanophotonics, integrated photonics, SPP/ППП, DLSPP/DLSPPW, LR-DLSPP/LR-DLSPPW, MDM/MIM/IMI plasmonic waveguides, optical antennas, phase-change-material photonics and modulators (PCM, GST, GSST, Sb2S3, Sb2Se3, IST), EIM/ЭДП/effective-index screening, COMSOL/FEM/CST mode analysis, branch tracking, propagation loss, L_pi, insertion loss, and source-backed article or literature-review work in this domain.
---

# Plasmonics Photonics

## Purpose

Use this skill for the user's specialized plasmonic and photonic research context. It narrows broad scientific work into domain-specific reasoning about guided optical modes, plasmonic waveguides, PCM photonics, reduced-order models, and full-wave validation.

For general Obsidian note style, checkpoint discipline, paper-note structure, term-note capture, and PhD vault hygiene, use the general `scientific-work` rules when available. This skill adds the plasmonics/photonics physics and claim-control layer.

## Note Capture (non-negotiable)

Plasmonics/photonics conceptual work must be captured back into the vault by default, applying `scientific-work` note-capture rules 12-14 even when that skill is not separately loaded. Do not wait to be asked, and do not answer only in chat:
- for "объясни / разбери / что тут происходит / как это получается" explanations of PhD/vault material, create or update the nearest relevant note and answer with a link (scientific-work rule 12);
- for a clarifying question about the content of an existing note - for example "это точная формула или приближение", "откуда берётся эта формула", "почему одна формула, если параметр/χ⁽³⁾ не универсален", "что здесь означает этот множитель" - after answering, add a compact clarification to the relevant section of the source note, following `references/obsidian-style.md` from the shared `scientific-work` skill (rule 14);
- for a stated physical guess or hypothesis, record it in the nearest appropriate note with an explicit status (rule 13).

Skip the note update only when the user explicitly asks not to write files, or the question is clearly casual and unrelated to vault content. When a task begins touching vault notes, load the `scientific-work` note-capture and `obsidian-style` rules if they are not already in context, so this behavior does not depend on remembering to open that skill.

## Self-Improvement And Publishing

When plasmonics-photonics work reveals a durable, reusable lesson, use the `skill-learning` policy. Save compact domain rules, validation checks, reusable modeling patterns, source-audit lessons, or formula conventions in this skill or a focused `references/<topic>.md` file. Do not store secrets, credentials, private raw datasets, unpublished full measurements, copyrighted source text, generated logs, raw project/customer material, or one-off project facts in the skill.

Before materially editing this skill, applying self-learning updates, or publishing changes, run the owning repository's freshness check: fetch `origin main`, compare local `HEAD` with `origin/main`, fast-forward if local is behind and the relevant working tree is clean, and inspect dirty/ahead/diverged states before continuing.

After materially updating this skill, validate it when feasible, then commit and push the relevant skill changes to the owning repository by default unless the user explicitly says not to. Stage only relevant skill files and repository metadata.

If publishing encounters remote changes or merge conflicts, resolve them autonomously when the intended final meaning can be determined from the files, commit history, nearby rules, and the user's instruction. Preserve compatible rules from both sides, consolidate duplicates, rerun validation, commit the resolved result, and push. Stop only when resolution would require guessing unavailable technical meaning, exposing protected content, discarding user work, or using unavailable repository permissions.

## Start Of Work

For nontrivial domain work, first preserve context:
- read or create the nearest project-local `CODEX/Контекст задачи Codex - <topic>.md` or `CODEX/План задачи Codex - <topic>.md`;
- record the objective, current status, local source notes/files, key formulas, numerical facts, caveats, assumptions, and next steps;
- keep reviewed-works registers for literature and source audits;
- after compaction, interruption, or a long gap, read the active goal/plan and project checkpoint before substantive reasoning.

For reusable plasmonics/photonics calculation code, mode-analysis scripts, and validated diagnostics, make intermediate git commits when a repository is available and the user has not opted out. A commit is useful when the code is reproducible and scientifically interpretable: it either agrees with an analytic estimate, literature value, previous COMSOL/FEM/CST result, or another check, or it exposes a meaningful discrepancy. Commit messages or nearby notes should state what the result was compared against and whether the status is `validated`, `diagnostic`, `discrepant`, or `unverified`. Do not commit bulky raw solver artifacts such as large `.mph` files unless the user explicitly wants them versioned.

Search local PhD/vault context before giving scientific conclusions. Prefer local notes, model diaries, PDFs, extracted tables, scripts, and COMSOL/CST logs over memory. Mark uncertain statements as hypotheses.

## Domain Workflow

Separate every task into four layers:
- **physics:** SPP/DLSPP/LR-DLSPP mode type, confinement, light-line position, cutoff/leaky behavior, material overlap;
- **materials:** optical constants, PCM state, wavelength, composition, crystallization assumption, metal loss convention;
- **method:** analytic dispersion, EIM/ЭДП, transfer matrix, FEM/COMSOL, CST, volume integral, FDTD, or experiment;
- **claim:** what the result can and cannot support in an article, report, or dissertation.

For PCM/plasmonic phase shifter work, compare state-paired metrics rather than isolated states:
- $Re(n_\mathrm{eff})$, $Im(n_\mathrm{eff})$, and $\beta=k_0n_\mathrm{eff}$;
- $\Delta Re(n_\mathrm{eff})$ between amorphous and crystalline states;
- $L_\pi=\lambda_0/(2\Delta Re(n_\mathrm{eff}))$;
- propagation length and loss per length;
- insertion loss on $L_\pi$;
- branch identity and field overlap.

## Validation Rules

For EIM/ЭДП and other reduced-order models:
- treat them as screening/pre-design tools unless full validation supports stronger claims;
- use them confidently for phase-trend checks only after confirming the mode branch is meaningful;
- never present agreement in $L_\pi$ as proof of accurate absolute loss;
- mark no-root or fallback values as `EIM-breakdown / no valid root`, not ordinary numerical results;
- when a manuscript discusses a missing local EIM root and a fallback material index, state three facts explicitly: which local mode was not found, which numerical value was substituted, and that the resulting value is diagnostic rather than a physical mode. Do not compress this into phrases such as «the region is replaced by the cladding» or «not an ordinary operating point»;
- retain negative examples as part of a failure atlas.

For COMSOL/FEM/CST mode analysis:
- define the sign convention for $Im(n_\mathrm{eff})$, $\operatorname{Im}\beta$, propagation length, dB/length, and dB/$\pi$;
- validate mesh, domain size, PML/boundary settings, and material assignments before calling a solver result a reference;
- track modes by field profile, overlap integral, confinement factor, and power distribution rather than by fixed mode number alone;
- check whether residual loss comes from PCM, metal absorption, radiation/leaky channels, boundaries/PML, or numerical artifacts.
- If mesh/domain/PML convergence, wavelength sweep, or field-based branch
  tracking has not actually been performed, describe the solver comparison as
  diagnostic or preliminary. Do not leave a manuscript placeholder for this
  inside the article body, and do not upgrade a fixed-mode-label run into a
  final FEM benchmark by wording alone.
- Do not introduce PML, scattering-boundary, or other solver-implementation terminology into a manuscript that does not use that full-vector model. State the general validation requirement (mesh, domain size, and external-boundary sensitivity) in the paper; keep concrete future solver settings in the project checkpoint until they are actually used and reported.

For manuscript and DOCX work in this domain:
- describe each planar reference by its actual layer stack and invariant direction before using a short label such as S3. If the planar model is invariant perpendicular to the slice plane, say so explicitly and state the resulting infinite layer width. Avoid undefined phrases such as «central active slice»: use «the vertical stack through the metal strip and ridge» at first mention, then the defined slice label;
- translate mesh refinement concretely as «последовательное уменьшение размера элементов расчётной сетки». Do not write «измельчение сетки» or imply that only one generic cell is reduced; mesh convergence requires repeated calculations on successively finer finite-element meshes;
- protect the physical divisions in the standard guided-mode formulas:
  $n_\mathrm{eff}=\beta/k_0$, $k_0=2\pi/\lambda_0$,
  $L_\mathrm{power}=1/(2\operatorname{Im}\beta)=
  \lambda_0/(4\pi\operatorname{Im}n_\mathrm{eff})$, and
  $L_\pi=\lambda_0/(2\Delta\operatorname{Re}n_\mathrm{eff})$;
- reject generated text where TeX cleanup collapses these into multiplication
  or adjacency, such as `n_eff=betak0`, `k0=2pilambda0`, `12Imbeta`, or
  `lambda04piImn_eff`.

For literature and article claims:
- do not claim a first PCM modulator, first PCM phase shifter, first plasmonic PCM device, or first EIM use for DLSPP unless primary literature verification supports it;
- frame EIM/ЭДП work as a failure-aware screening workflow when loss metrics diverge from FEM;
- distinguish EIM/effective-index waveguide reduction from EMA/effective-medium approximation only when partial crystallization, intermediate PCM states, or an EMA material model is actually in scope; do not introduce an EMA disclaimer into a paper that compares only amorphous and crystalline states;
- cite primary papers or official solver documentation for claims about device performance, solver behavior, or method limitations.
- before finalizing a plasmonics/photonics article or conference paper, follow the `scientific-work` final GPT/ChatGPT review rule; a final manuscript should not be treated as ready after Codex-only review.

## Detailed Reference

Read `references/workflow.md` for substantial work involving articles, literature reviews, EIM/ЭДП benchmarking, PCM material audits, COMSOL/FEM validation, or mode-branch troubleshooting.
