# COMSOL Workflow

Use this reference for COMSOL, CST, FEM, mode analysis, `.mph`, Java automation, and numerical validation tasks.

## Safety

- Do not edit original `.mph` files directly.
- Work on a copy or generate a new model.
- Keep raw simulation files separate from concise Obsidian decision notes.

## Modeling Hygiene

- Record geometry, materials, boundary conditions, mesh settings, solver settings, and swept parameters.
- Record units explicitly.
- Note what changed between simulation runs.
- Validate against analytic estimates, convergence checks, or an independent reference when possible.

## Reporting

- Distinguish observed results from hypotheses.
- Include plots or exported values only when they support a decision.
- Write conclusions as next modeling actions: what to refine, compare, sweep, or verify.

## Automation

- Prefer scripts for repeatable parameter sweeps or model generation.
- Keep generated files named by date, model variant, or parameter set so results are traceable.
- On Windows, prefer `comsolbatch.exe` for non-interactive runs. Avoid `comsol.exe batch` unless a visible interactive COMSOL session is explicitly needed.
- For Java model scripts, compile with `comsolcompile.exe <ModelScript>.java` first, then run `comsolbatch.exe -inputfile <ModelScript>.class -batchlog <run>.log`. Do not rely on `comsolbatch.exe -inputfile <ModelScript>.java`: COMSOL can try to open the Java source as a model file, write an error to the log, and still return process exit code `0`.
- Treat the batch log and expected output files as the success signal, not only the shell exit code. After every COMSOL run, inspect the tail of the `.log`, check that exported `.csv` or status files exist, and verify the model saved under the intended final name.
- When a script calls `model.save("final_name.mph")`, COMSOL may also create a duplicate `<ClassName>_Model.mph` plus `.status` or `.recovery` files. After confirming the intended `.mph` and exported tables are present, remove redundant generated duplicates so later work does not confuse them with authoritative results.
- Export numerical results directly from the Java script with `model.result().table(...).save(...)` and write a small UTF-8 status or summary file. This makes headless runs auditable without opening the `.mph`.
- For `ModeAnalysis`, set the eigenvalue shift near an analytic or previous numerical estimate, request enough eigenmodes, and choose the physical branch by an explicit rule such as field localization, continuity through a sweep, or closest complex `n_eff`. Do not assume the first table row is the mode of interest.
- Record the complex-material sign convention used in COMSOL, especially for metals. If source code or tables use a different convention for loss, state whether COMSOL used `eps=(n+i*k)^2` or another equivalent representation.
- In COMSOL mode-analysis tables, the displayed sign of `Im(n_eff)` or `Im(beta)` can follow the chosen time-dependence convention. When converting to attenuation, propagation length, or insertion loss, use the positive attenuation value, usually `abs(Im(n_eff))` or `abs(Im(beta))`, and state this convention in the note.
- For finite/open plasmonic waveguide checks without a full boundary-convergence study, label the result as diagnostic. Record domain size, boundary treatment, mesh settings, and the missing convergence checks before comparing it to analytic or EDP results.
