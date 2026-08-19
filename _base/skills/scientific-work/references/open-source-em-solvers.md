# Open-Source EM Solvers

Use this reference when COMSOL is unavailable, when a second independent solver
is needed to check a COMSOL or analytic result, or before spending time on an
open-source package that was already evaluated here.

Each entry states what was actually tried on the user's Windows machine and what
the outcome was. Do not re-litigate a rejected package without new evidence: the
rejection reasons below are reproducible failures, not opinions.

## femwell — validated, use this one

FEM mode solver for photonic and plasmonic waveguide cross-sections, built on
`scikit-fem` and `gmsh`. Install: `pip install femwell` (pulls `gmsh`, `shapely`,
`scikit-fem`, and numpy 2.x).

**Validation status: `validated` (2026-08-19).** Checked against the COMSOL 6.2
mode-analysis exports stored in `phd_lerer/edp/metal_strip_w800/`: a 20 nm silver
strip on an n=1.45 substrate, air above, 6 x 4 um domain, with the same silver
permittivities that were fed to COMSOL. Over the 450-800 nm sweep at 800 nm strip
width femwell reproduces the COMSOL eigenvalues to **0.476 % in `Re(n_eff)` and
1.53 % in `Im(n_eff)`**. Reproduce with
`python edp/metal_strip_w800/scripts/validate_femwell_vs_comsol.py`.

Working practices learned while doing that validation:

- **The computational domain must comfortably exceed the mode's decay length.**
  For weakly bound long-range plasmon modes this is the dominant error source,
  not the mesh. A 3 um wide LR-SPP strip whose field decays over ~200 um returned
  `Re(n_eff)` *below* the cladding index in a 26 um domain — that is a box mode,
  not a waveguide mode. Always compute `1/(k0*sqrt(n_eff^2 - n_clad^2))` from the
  result and compare it with the half-domain; if the mode is not bound, say so
  instead of reporting the number.
- **Mesh the thin metal, but keep the graded zone small.** For 14-20 nm films a
  resolution of 4-6 nm across the metal is enough. The `distance` parameter of the
  resolution dict controls how far that fine zone extends and is what makes the
  mesh explode: 0.5 um around two metal strips in a 44 um domain did not finish,
  while 0.12 um in a 30 um domain solved in minutes at 89k nodes.
- **`n_guess` selects a branch, it does not identify a mode.** A metal strip
  supports a ladder of plasmonic modes; request several and sort them yourself.
  Filter by "above the cladding index and visibly lossy" to drop the nearly
  lossless substrate-slab and box modes, then take the largest `Re(n_eff)` as the
  fundamental. Never trust the solver's ordering.
- femwell requires numpy 2.x. That is incompatible with `emepy` (see below), so
  the two cannot share one environment.

**A caution that came out of the same validation.** femwell exposed a defect in
our own COMSOL post-processing: for one and the same configuration the two
summaries in `edp/metal_strip_w800/results/` disagreed, because the width-sweep
selection had drifted onto modes 1, 2, 3 and 5 as the strip widened. The summary
that carried an explicit field-based `selection_rule` column was the correct one.
Treat a stored COMSOL summary without a documented selection rule as unverified.

## Rejected after evaluation

**emepy** (eigenmode expansion, `pip install emepy`) — *not usable*. Import fails
because `emepy` depends on `EMpy_gpu`, whose `__init__` does
`from numpy.testing import Tester`, removed in numpy >= 1.25. Pinning
`numpy < 1.25` does not help on Python 3.12: no wheels exist for that
combination, and the source build dies on the missing `distutils`. It would need
a separate Python <= 3.11 interpreter, and even then could not share an
environment with femwell.

**CAMFR** — *not usable*. The `camfr` package on PyPI is a 5.6 kB placeholder
whose `__init__.py` only prints "Camfr: coming soon!". The real project is a
2007-era C++/Python 2 codebase with no maintained Windows or Python 3 build.

**ngslab** (FEM modes of unbounded multilayer planar waveguides with PML/TBC) —
*not installable here*. It is otherwise a good fit, shipping demos for exactly our
problem class (IMI/DMD and MDM gold waveguides). But it builds against PETSc, and
PETSc's configure refuses native Windows Python outright: "Windows python
detected. Please rerun ./configure with cygwin-python." Reconsider only under WSL
or Cygwin.

**MLSWG** — *not usable as a tool, no loss*. MATLAB (GPL-3.0), and there is no
MATLAB on this machine. It solves 1D multilayer TE/TM modes with complex indices,
which is exactly what `phd_lerer/lrspp_coupling/slabmodes/tmm.py` already does,
and that module is validated against Maier's coupled-film equations, the
single-interface SPP limit and a COMSOL-checked three-layer formula. Useful only
as a published cross-check of method, not as software to run.

## Choosing a checking tool

- Planar multilayer stack, any number of layers, lossy metals: use the analytic
  transfer-matrix solver in `phd_lerer/lrspp_coupling/slabmodes/`. It is exact for
  this class and needs no mesh.
- Two-dimensional cross-section, finite strip width, lossy metals: femwell.
- Propagation along a slowly varying cross-section: no validated open package is
  available. If the transverse problem is single-mode, the adiabatic limit plus a
  Love-criterion check answers the question analytically; see
  `phd_lerer/lrspp_coupling/slabmodes/eme.py`.
- Whenever a reduced model and a full-vector solver disagree, first check whether
  the measured or reference quantity is even a modal quantity. A finite-width
  strip cannot absorb more than the infinite film of the same stack, so a measured
  loss above that ceiling proves a non-modal contribution is present.
