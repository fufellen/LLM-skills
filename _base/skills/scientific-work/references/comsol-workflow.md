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
- **Frequency-domain `plist` must be a `range()` expression string, NOT space-separated literal list, NOT setIndex-per-value.** All three of `set("plist","749.481 705.394 ...")`, `set("plist","749.481, 705.394, ...")` and `for i: setIndex("plist", value_i, i)` visibly save all N tokens in `p:plist.valueMatrix` in the XML but the solver reads `p:plist.value` (the expression) and sees an empty/single-token evaluation — sweeps ONE point. GUI-generated Java always emits `set("plist", "range(a[unit], step[unit], b[unit])")` — that is the only form the solver parses correctly. For a NON-uniform freq sweep, either resample to uniform-in-frequency (accept non-uniform wavelength) or use a separate `Parametric` study feature with `plistarr = "range(400,25,800)"` and `punit="nm"`, driving Frequency's `plist` from a global param `f_curr = c_const/lam0` (learned 2026-08-01).
- **PML — the working COMSOL 6.2 Model API pattern**, reverse-engineered from `Wave_Optics_Module/Couplers_Filters_and_Mirrors/single_mode_fiber_coupling.mph` XML:
    ```java
    model.component("comp1").coordSystem().create("pml1", "PML");  // 2 args, NOT 3
    model.component("comp1").coordSystem("pml1").selection().geom("geom1", 3);
    model.component("comp1").coordSystem("pml1").selection().named("geom1_<sph_out_tag>_lyr_<layer_name>_dom");
    model.component("comp1").coordSystem("pml1").set("coord", new String[]{"x","y","z"});
    model.component("comp1").coordSystem("pml1").set("d",     new String[]{"x","y","z"});
    model.component("comp1").coordSystem("pml1").set("dmax",  new String[]{"d_pml","d_pml","d_pml"});
    ```
    Prior failure `Unknown geometry. Tag: PML` came from passing `"geom1"` as third arg to `.create()`. It's a Coordsys `op="PML"` node (2-arg create), not a coordSystem-with-geom node. `p:coord`/`p:d`/`p:dmax` are String[] with unit-carrying items. Layered spheres decompose the PML shell into multiple sub-domains — use the auto-named `geom1_<sph_out>_lyr_<pml_layer_name>_dom` selection to catch all of them (requires `createselection="on"` on the outer sphere). Keep a `Scattering` BC on the outermost boundary as a residual-reflection sink alongside PML — that is the standard closure.
- **A spherical `Sphere` with `layername` decomposes the PML shell into multiple sub-domains.** Point-`Ball` selections to identify PML by coordinates miss most sub-domains. Use the auto-named domain selection `geom1_<sph_tag>_lyr_<layer_name>_dom` (requires `createselection="on"` on that sphere).
- **Solve cost for a 3D Au-in-vacuum scatterer, R=25 nm, `hmax=40[nm]`, `hmax=3[nm]` on Au surface, PML shell = λ_max/2, r_domain ≈ 1 μm, first-order elements: about 4.3 million DOFs, ≈28 s per frequency, ≈1.4 GB RAM.** Full 17-point λ-sweep ≈8–10 min on the user's Windows machine. Halve the domain, coarsen to `hmax=60[nm]` for smoke tests before committing to fine grids.
- **When the model is correctly configured with materials that have real losses (Au with n,k) and dispersive material assignment, MUMPS direct solver silently falls back to iterative multigrid due to memory pressure.** In that regime, per-point cost rises to 3–7 min and RAM usage climbs to 8+ GB (of 16 GB), and near LSPR (~525 nm for Au R=25 nm) iterations stall for 10–20 min at ~57% "Solving linear system". Full 16-point sweep took ≈70 min on the user's Ryzen 5 2500U. Symptom `Warning: MUMPS is switching to out-of-core mode` in `-batchlog` is the tell; consider halving the domain or accepting slow solve for the validation pass.
- **`ewfd.Qh` does NOT exist in Wave Optics EWFD physics — use `ewfd.Qrh` (resistive heat).** Trying `ewfd.Qh` yields `Failed to evaluate expression / Undefined variable: ewfd.Qh` at the EvalGlobal stage (or silent zero if wrapped in an integration). Other candidates: `ewfd.Qav`, `ewfd.Qsrh`, `ewfd.Qsh` all fail; only `ewfd.Qrh` works. Numerically verified against analytic ω/2·ε₀·ε''·|E|² integrand. (learned 2026-08-01)
- **EWFD physics reads `n, ki` from a dedicated `RefractiveIndex` property group, NOT from `def.refractiveindex/refractiveindexkappa`, and requires an explicit `DisplacementFieldModel = "RefractiveIndex"` on the Wave Equation Electric feature.** Without both, Au domain solves as vacuum (n=1, no losses → σ_abs = 0). Working pattern:
    ```java
    mat.propertyGroup().create("RefractiveIndex", "Refractive index");
    mat.propertyGroup("RefractiveIndex").set("n",  "n_Au(ewfd.lambda0)");
    mat.propertyGroup("RefractiveIndex").set("ki", "k_Au(ewfd.lambda0)");
    // + on physics:
    model.component("comp1").physics("ewfd").feature("wee1")
         .set("DisplacementFieldModel", "RefractiveIndex");
    ```
    The `def` group holds appearance/coloring properties (color, roughness, etc.), not the dispersion table EWFD reads at solve.
- **`Ball` selection for a domain-in-larger-domain (Au sphere at origin inside air sphere, `posx=0,posy=0,posz=0,r=r_np*0.5,entitydim=3`) can return 1 entity that is NOT the intended domain — often it returns the enclosing air domain if a boolean union collapsed the inner sphere.** Diagnostic: `intop(1)` on a Ball-selected Au should equal `(4/3)πR³`; if it returns the enclosing volume instead, the Ball missed. Use auto-named `geom1_<sph_tag>_dom` (needs `createselection="on"`) — it survives union and is exactly the Au domain.
- **A material with no explicit selection does not fill in "the rest" — every domain must be covered.** `mat_air` without `.selection()` triggers `Undefined material property 'n' required by Wave Equation, Electric 1` on the empty domain. Set `.selection().all()` on the background material and let a later material with narrower selection override on top. (Latest-created material wins on overlap, so `mat_Au` created after `mat_air` with `.selection().named("geom1_sph_np_dom")` overrides on Au.)
- **`nx, ny, nz` (bare) are boundary outward-normal components and are always defined on real boundaries; `ewfd.nX, ewfd.nY, ewfd.nZ` are physics-scoped and undefined on any boundary where the EWFD physics isn't active (interior slice surfaces, virtual observation spheres that never got Boolean-cut).** Use bare `nx, ny, nz` for post-processing flux integrals; anything requiring physics-side up/down splitting stays in `ewfd.*`.
- **An observation `Sphere` created inside `air` without a Boolean cut becomes virtual after `geom.run()` — its boundary either does not exist in the finalized geometry, or exists but the flux integral returns garbage (values of the wrong magnitude/sign).** Skip the observation sphere entirely and compute σ_sca as the flux of scattered Poynting through the Au particle boundary (`geom1_sph_np_bnd`), pointing outward from Au. Numerically identical to a proper observation-surface integral when PML absorbs cleanly.
- **User-defined coupling operators (`Integration`) created via `component().cpl().create(...)` AFTER a `study.run()` are not attached to the stored solution and evaluate as `Unknown function or operator` in `EvalGlobal`.** For post-solve integration of a pre-existing `.mph`, use result-side derived values instead: `result().numerical().create("iv1","IntVolume")` / `IntSurface`. These take a selection directly and work against any stored dataset without a re-solve. Alternatively, define all `cpl` operators (`auint`, `abint`) in the Java source BEFORE `study.run()` so they're baked into the solved dataset.
- **`System.out.println` and `System.err.println` from `comsolbatch` are largely lost — only the very last few prints from `main()` reliably reach the process stdout that the shell redirects; anything inside `run()` may disappear even without an exception.** Reliable debug channel: open a `PrintWriter` on `logs/<name>_debug.log` and flush after every message. Print to that file for anything you must be able to see.
- **`Result → Global Evaluation` (`EvalGlobal`) with N expressions in one shot returns a truncated `double[expr][sol][ri]` on the first failing expression** — shape ends up `2 × nSol × 1` instead of `4 × nSol × 1` when expression 3/4 could not evaluate. Wrap each expression in its own `EvalGlobal` in a `try/catch` loop when isolating an eval failure; the batch API silently omits failed rows.
- **Scattering BC without PML gives cross-sections a factor 70–1000 too large near a metal LSPR.** In an R=25 nm Au sphere with `d_air = lam_max/2 = 400 nm`, closing the domain with Scattering BC on the outer sphere produces standing waves in the air buffer that pump the field to unphysical enhancement (|E_total|² ~50–200× background). Cross-sections come out ~1e5 nm² vs Mie ~2000 nm², and the σ_abs "peak" shifts to 400 nm from the true 500 nm LSPR because the cavity mode dominates. Not a diagnostic-acceptable approximation for validation — a PML is required.

## Data-Hygiene For Material Tables

- **Tabulated optical constants are downloaded once and treated as source of truth.** Fetch scripts must be idempotent: refuse to overwrite the local CSV unless `--force` is passed, and every downstream script (Mie reference, COMSOL interpolation, plotting) must read the local file with no network call. Re-fetching on every run breaks reproducibility and hides silent format changes from refractiveindex.info / other upstream sources. Include a spot-check of a known value (e.g. Au Johnson-Christy: `n≈0.43, k≈2.455 at 548.6 nm`) at the top of the fetch script and in the README so a corrupted file is caught immediately (learned 2026-07-31).
- **refractiveindex.info raw endpoint has changed URL scheme.** As of 2026-07: the working URL for tabulated Au(Johnson-Christy 1972) is `https://refractiveindex.info/tmp/database/data-nk/main/Au/Johnson.txt` and the file contains two consecutive blocks headed `wl\tn` and `wl\tk` (identical wavelength grids). The older `.../database/data-nk/main/Au/Johnson.yml` and `.../database/data/main/Au/Johnson.yml` return HTTP 404. Parse the two blocks by tracking the current mode after each `wl\t...` header row.
