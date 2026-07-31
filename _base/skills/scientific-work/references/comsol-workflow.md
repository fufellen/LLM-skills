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

## Java Model API — Recurrent Traps

Lessons from writing a headless 3D scattering model on COMSOL 6.2 (learned 2026-07-31, driving `sphere_vacuum.java` for Level-1 Mie validation). Batch typically prints exit code 0 on model-build errors — always read the tail of `-batchlog` for `/*Error*/` and expected output files.

- **Material `refractiveindex` / `refractiveindexkappa` are scalars for isotropic media.** Passing a 9-element `String[]` tensor gives `A scalar value expected. Parameter: Refractive index (null) - Owner: Basic (def)` and the run dies before mesh. Use `.set("refractiveindex", "n_expr")` and `.set("refractiveindexkappa", "k_expr")`.
- **Interpolation function calls need consistent argument units.** With `argunit="nm"` and `nargs=1`, call `n_Au(ewfd.lambda0)` directly — COMSOL converts the SI-meters argument. Do not hand-multiply `*1[1/nm]`; the double conversion silently gives wrong numbers.
- **Scattering boundary feature is `"Scattering"`, not `"ScatteringBoundary"`.** The wrong name errors as `Unknown feature ID: ScatteringBoundary` after the mesh visualization step (misleading location).
- **The mesh has a built-in `size` node at creation.** `mesh1.create("size", "Size")` errors as `An object with the given name already exists. Tag: size`. Modify `mesh1.feature("size")` in place; only `create` for additional local sizes (`sz_au`, etc.) with different tags.
- **Physics-controlled mesh (`autoMeshSize(N)` + `mesh1.run()`) can fail as `Failed to set up physics-controlled mesh. Failed to set mesh size automatically.`** in a scattered-field EWFD scattering setup when called before or without a properly wired study. Fall back to user-controlled: modify the default `size` node, add one `FreeTet`, run.
- **`Sphere` needs `createselection="on"` to expose the auto-named selections** `geom1_<tag>_dom`, `geom1_<tag>_bnd`, and for a layered sphere `geom1_<tag>_lyr_<layer_name>_dom`. Without it these selection names do not exist and downstream `.selection().named(...)` calls fail cryptically.
- **Frequency-domain `plist` must be a real numeric list, not an expression.** `plist = "c_const/(range(400,25,800)*1e-9)"` warns `Inconsistent unit 'm/s' is ignored, 'Hz' is used instead` and silently sweeps only ONE point (the range expression collapses). Build the list numerically in Java (loop, `String.format(Locale.US, ...)`, space-separated), set `punit="THz"` or `"Hz"` to match.
- **A spherical `Sphere` with `layername` decomposes the PML shell into multiple sub-domains.** Point-`Ball` selections to identify PML by coordinates miss most sub-domains. Use the auto-named domain selection `geom1_<sph_tag>_lyr_<layer_name>_dom` (requires `createselection="on"` on that sphere).
- **PML remains an open trap on COMSOL 6.2 Model API.** Both `model.component("comp1").coordSystem().create("pml1", "PML", "geom1")` with `.set("PMLgeom", "Spherical")` and without that property error identically as `Unknown geometry. Tag: PML` after visualization mesh completes. Workarounds: (a) use `Scattering` BC on the outer boundary as a diagnostic (accept modest reflection artefacts), (b) build the model in GUI and save-as Java to see the actual PML tag/property set that COMSOL emits. Do not spend more than one iteration on Java-only PML guessing — GUI reverse-engineer is faster.
- **Solve cost for a 3D Au-in-vacuum scatterer, R=25 nm, `hmax=40[nm]`, `hmax=3[nm]` on Au surface, PML shell = λ_max/2, r_domain ≈ 1 μm, first-order elements: about 4.3 million DOFs, ≈28 s per frequency, ≈1.4 GB RAM.** Full 17-point λ-sweep ≈8–10 min on the user's Windows machine. Halve the domain, coarsen to `hmax=60[nm]` for smoke tests before committing to fine grids.

## Data-Hygiene For Material Tables

- **Tabulated optical constants are downloaded once and treated as source of truth.** Fetch scripts must be idempotent: refuse to overwrite the local CSV unless `--force` is passed, and every downstream script (Mie reference, COMSOL interpolation, plotting) must read the local file with no network call. Re-fetching on every run breaks reproducibility and hides silent format changes from refractiveindex.info / other upstream sources. Include a spot-check of a known value (e.g. Au Johnson-Christy: `n≈0.43, k≈2.455 at 548.6 nm`) at the top of the fetch script and in the README so a corrupted file is caught immediately (learned 2026-07-31).
- **refractiveindex.info raw endpoint has changed URL scheme.** As of 2026-07: the working URL for tabulated Au(Johnson-Christy 1972) is `https://refractiveindex.info/tmp/database/data-nk/main/Au/Johnson.txt` and the file contains two consecutive blocks headed `wl\tn` and `wl\tk` (identical wavelength grids). The older `.../database/data-nk/main/Au/Johnson.yml` and `.../database/data/main/Au/Johnson.yml` return HTTP 404. Parse the two blocks by tracking the current mode after each `wl\t...` header row.
