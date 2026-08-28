# Results Log

This document records significant project observations, computational
results and methodological decisions.

Planned work should be recorded in the roadmap rather than presented as
a result.

---

# Crystalline Reference Structure

## COD 1521670

**Status:** Reference structure identified and obtained.

**Material:** InGaZnO4

**Source:** Crystallography Open Database

**COD ID:** 1521670

**Reference:** Nespolo, M.; Sato, A.; Osawa, T.; Ohashi, H.
Crystal Research and Technology 35 (2000), 151–165.

---

## Reference Cell

The CIF contains approximately:

    a = 3.299 Å
    b = 3.299 Å
    c = 26.101 Å

    alpha = 90°
    beta  = 90°
    gamma = 120°

---

## Mixed Ga/Zn Site

Inspection of the crystallographic structure shows that Ga and Zn share
the same crystallographic site with approximately:

    Ga occupancy = 0.5
    Zn occupancy = 0.5

The CIF therefore represents an experimental average structure rather
than an explicit ordered atomistic model.

---

## Conventional Cell

Expansion of the crystallographic structure produces six mixed Ga/Zn
positions.

Stoichiometric InGaZnO4 requires:

    3 Ga
    3 Zn

across these positions.

The number of possible raw assignments is:

    C(6,3) = 20

Initial symmetry analysis reduces these to:

    4 symmetry-distinct ordered configurations

---

## Methodological Decision

The original COD CIF will be retained unchanged as the experimental
reference.

Ordered Ga/Zn configurations will be generated programmatically.

No ordered configuration has yet been selected as the final crystalline
reference.

Selection will be based on first-principles relaxation and relative
energetics.

---

## Ordered Crystalline Structure Validation

**Status:** Completed.

Four symmetry-distinct ordered InGaZnO4 structures were generated from
the mixed Ga/Zn crystallographic model derived from COD 1521670.

### Validation results

| Model | Atoms | Composition | Ordered | Minimum distance (Å) | Space group |
|---|---:|---|---|---:|---|
| `igzo_crystal_ordered_001` | 21 | In3Ga3Zn3O12 | Yes | 1.930 | P3m1 (156) |
| `igzo_crystal_ordered_002` | 21 | In3Ga3Zn3O12 | Yes | 1.930 | P3m1 (156) |
| `igzo_crystal_ordered_003` | 21 | In3Ga3Zn3O12 | Yes | 1.930 | R3m (160) |
| `igzo_crystal_ordered_004` | 21 | In3Ga3Zn3O12 | Yes | 1.930 | P3m1 (156) |

Validation confirmed:

- correct 21-atom conventional-cell composition
- 3 In, 3 Ga, 3 Zn and 12 O atoms
- complete site occupancies
- consistent lattice parameters
- no unphysical short contacts
- four structurally distinct ordered configurations

pymatgen reported that fractional coordinates were rounded to ideal
crystallographic values during CIF parsing to avoid finite-precision
issues. No structural validation failures resulted from this operation.

### Symmetry observation

Three ordered configurations have P3m1 symmetry, while
`igzo_crystal_ordered_003` retains R3m symmetry.

The higher symmetry of model 003 does not imply that it is energetically
preferred. All four models will be compared using first-principles
geometry optimisation and relative energies.

No final crystalline computational reference has yet been selected.

---

## CP2K Smoke Test — Ordered Model 003

**Status:** Completed successfully.

A single-point PBE calculation was performed on
`igzo_crystal_ordered_003` using CP2K 2026.2.

### Setup

- Method: Quickstep / GPW
- XC functional: PBE
- Basis family: UZH 2026.2
- Pseudopotential family: UZH 2026.2 GTH-PBE
- Basis quality: TZVP
- CUTOFF: 600 Ry
- REL_CUTOFF: 60 Ry
- k-point sampling: Gamma only
- OpenMP threads: 4
- Diagonalisation library: ScaLAPACK

### Result

- SCF convergence: achieved
- SCF iterations: 55
- Total energy: -765.397428081766179 Ha
- CP2K warnings: 0
- Runtime: approximately 1015 s (~16.9 min)

This calculation is a numerical smoke test and should not yet be
interpreted as a converged scientific result.

---

## CP2K Basis-Set Sensitivity

**Structure:** `igzo_crystal_ordered_003`

**Functional:** PBE

**Pseudopotentials:** UZH 2026.2 GTH-PBE

**Grid used for preliminary comparison:**

- CUTOFF = 600 Ry
- REL_CUTOFF = 60 Ry

### Results

| Basis | Total energy (Ha) | ΔE vs TZV2P (meV/f.u.) |
|---|---:|---:|
| DZVP | -765.3772402115 | 253.314 |
| TZVP | -765.3974280818 | 70.201 |
| TZV2P | -765.4051675944 | 0.000 |

### Interpretation

The change from DZVP to TZVP is substantial, and the remaining
TZVP-to-TZV2P difference is approximately 70 meV per InGaZnO4 formula
unit.

TZVP therefore cannot yet be considered converged for the intended
comparison of Ga/Zn ordering energies.

TZV2P will be used as the numerical reference for subsequent grid
convergence testing.

The final basis-set choice will be reassessed after CUTOFF and
REL_CUTOFF convergence.

---

## CP2K CUTOFF Convergence

**Structure:** `igzo_crystal_ordered_003`

**Functional:** PBE  
**Basis:** TZV2P-MOLOPT-PBE-GTH  
**REL_CUTOFF:** 80 Ry

### Results

| CUTOFF (Ry) | Total energy (Ha) | ΔE from previous (meV/f.u.) |
|---:|---:|---:|
| 400 | -765.4080331996 | — |
| 500 | -765.4055777921 | 22.272 |
| 600 | -765.4051670060 | 3.726 |
| 700 | -765.4050953121 | 0.650 |
| 800 | -765.4047988772 | 2.689 |

### Decision

A provisional CUTOFF of **700 Ry** was selected.

The 600 → 700 Ry change is approximately 0.65 meV per InGaZnO4
formula unit, indicating satisfactory numerical stability for the current
ordering-energy study.

The 800 Ry result shows a small non-monotonic shift and does not justify
the additional computational cost at this stage.

REL_CUTOFF convergence remains to be completed.

---

## CP2K REL_CUTOFF Convergence

**Structure:** `igzo_crystal_ordered_003`

**Functional:** PBE  
**Basis:** TZV2P-MOLOPT-PBE-GTH  
**CUTOFF:** 700 Ry

### Results

| REL_CUTOFF (Ry) | Total energy (Ha) | ΔE from previous (meV/f.u.) |
|---:|---:|---:|
| 40 | -765.4051507847 | — |
| 50 | -765.4050975818 | 0.483 |
| 60 | -765.4050948992 | 0.024 |
| 70 | -765.4050953205 | -0.004 |
| 80 | -765.4050953120 | 0.00008 |
| 100 | -765.4050953117 | 0.000003 |

### Decision

A production value of **REL_CUTOFF = 60 Ry** was selected.

The energy change between 50 and 60 Ry is approximately 0.024 meV per
InGaZnO4 formula unit, while further increases produce negligible changes.

The provisional CP2K grid parameters are therefore:

    CUTOFF = 700 Ry
    REL_CUTOFF = 60 Ry

---

## CP2K k-point Convergence — Initial Series

**Structure:** `igzo_crystal_ordered_003`

**Functional:** PBE  
**Basis:** TZV2P-MOLOPT-PBE-GTH  
**CUTOFF:** 700 Ry  
**REL_CUTOFF:** 60 Ry

### Results

| k-point mesh | Total energy (Ha) | ΔE from previous (meV/f.u.) |
|---|---:|---:|
| 1×1×1 | -765.4050954366 | — |
| 2×2×1 | -767.2228310662 | -16487.7 |
| 3×3×1 | -767.1767376187 | +418.1 |
| 4×4×1 | -767.1905528013 | -125.3 |

### Interpretation

The k-point series is not yet converged.

Gamma-point-only sampling is inadequate for the current crystalline
cell. Significant energy changes also remain between the 2×2×1,
3×3×1 and 4×4×1 meshes.

The k-point series will therefore be extended to denser in-plane meshes
before a production mesh is selected.

---

## CP2K k-point Convergence

**Structure:** `igzo_crystal_ordered_003`

**Functional:** PBE  
**Basis:** TZV2P-MOLOPT-PBE-GTH  
**CUTOFF:** 700 Ry  
**REL_CUTOFF:** 60 Ry

### Results

| k-point mesh | Total energy (Ha) | ΔE from previous (meV/f.u.) |
|---|---:|---:|
| 4×4×1 | -767.1905528013 | — |
| 5×5×1 | -767.1894488047 | +10.01 |
| 6×6×1 | -767.1899457172 | -4.51 |

### Decision

A provisional production mesh of **6×6×1** was selected.

The change from 5×5×1 to 6×6×1 is approximately 4.5 meV per
InGaZnO4 formula unit, which is within the target numerical tolerance
for the crystalline ordering study.

A 7×7×1 calculation may be used later as an additional confirmation if
required.

---

## CP2K SCF Optimisation — Pulay Mixing

**Structure:** `igzo_crystal_ordered_003`

The baseline Broyden mixing scheme was compared with Pulay mixing using
the converged crystalline numerical setup.

### Results

| SCF method | SCF iterations | Total energy (Ha) | Wall time (s) |
|---|---:|---:|---:|
| Broyden mixing | 32 | -767.1899457172 | 1240.878 |
| Pulay mixing | 17 | -767.1899457538 | 700.825 |

The two methods converge to effectively identical total energies.

Pulay mixing reduced the SCF iteration count from 32 to 17 and
substantially reduced the wall time.

The Pulay calculation was performed using fewer OpenMP threads than the
baseline calculation, so the timing comparison is not strictly
like-for-like.

### Current decision

`PULAY_MIXING` with `ALPHA = 0.20` and `NBUFFER = 8` is the current
preferred SCF strategy.

Further comparison with `NEW_PULAY_MIXING` will be performed before the
production SCF settings are finalised.

---


## CP2K SCF Optimisation — Local Benchmark and Production Decision

The crystalline IGZO SCF strategy was benchmarked locally using the
converged numerical setup:

- PBE;
- TZV2P-MOLOPT-PBE-GTH;
- CUTOFF = 700 Ry;
- REL_CUTOFF = 60 Ry;
- 6×6×1 k-point mesh.

### Local fixed-geometry benchmark

| Method | SCF iterations | Wall time (s) | Status |
|---|---:|---:|---|
| Broyden baseline | 32 | 1240.878 | Converged |
| Pulay mixing | 17 | 700.825 | Converged |
| Low-alpha Broyden | — | — | Local runtime/WSL failure |
| New Pulay mixing | — | — | SIGABRT/SIGBUS local runtime failure |

Standard Pulay mixing was the fastest successful fixed-geometry local
test and converged to essentially the same energy as the Broyden
baseline.

During subsequent local geometry-optimisation development, however,
Pulay-related conditioning/runtime failures and WSL instability were
encountered. These failures were treated as environment/workflow
development issues rather than physical results.

### ARCHER2 production decision

The completed ordered-structure geometry optimisations used CP2K 2025.2
on ARCHER2 with:

- diagonalisation-based SCF;
- `BROYDEN_MIXING`;
- `ALPHA = 0.10`;
- `BETA = 1.5`;
- `NBUFFER = 4`;
- `EPS_SCF = 1e-6`;
- `MAX_SCF = 200`;
- 300 K Fermi–Dirac smearing;
- BFGS geometry optimisation.

This robust ARCHER2 setup is the current production geometry-optimisation
workflow. Final relaxed-structure energies were subsequently recalculated
using `EPS_SCF = 1e-7`.

---

## Crystalline IGZO Ordered-Structure Optimisation and Selection

### Status

**Completed.**

### Objective

Identify a low-energy ordered crystalline InGaZnO4 reference structure
for subsequent defect calculations and comparison with amorphous IGZO.

Four 21-atom ordered models (In3Ga3Zn3O12; three InGaZnO4 formula units)
were geometry optimised using CP2K 2025.2 on ARCHER2.

### Computational setup

- XC functional: PBE
- Basis: TZV2P-MOLOPT-PBE-GTH
- Matching GTH-PBE pseudopotentials
- CUTOFF: 700 Ry
- REL_CUTOFF: 60 Ry
- k-point mesh: 6×6×1
- Geometry optimiser: BFGS
- Geometry-optimisation SCF mixing: Broyden
- Geometry-optimisation EPS_SCF: 1e-6
- Final single-point EPS_SCF: 1e-7
- Electronic temperature: 300 K
- Fixed experimental cell
- HPC platform: ARCHER2

All four geometry optimisations converged successfully.

### Geometry-optimisation results

| Model | Final GEO_OPT energy (Ha) | Optimisation steps |
|---|---:|---:|
| ordered_001 | -767.247980382261 | 24 |
| ordered_002 | -767.169895002002 | 27 |
| ordered_003 | -767.248215342702 | 18 |
| ordered_004 | -767.166206810877 | 24 |

### Tight single-point energy comparison

Final energies were recalculated on the relaxed structures using
`EPS_SCF = 1e-7`.

| Model | Single-point energy (Ha) | ΔE (meV/f.u.) | Rank |
|---|---:|---:|---:|
| ordered_003 | -767.248205609002 | 0.00 | 1 |
| ordered_001 | -767.247977684509 | 2.07 | 2 |
| ordered_002 | -767.169898091297 | 710.29 | 3 |
| ordered_004 | -767.166212503339 | 743.72 | 4 |

The final energy ordering is:

    ordered_003 < ordered_001 << ordered_002 < ordered_004

`ordered_001` and `ordered_003` are near-degenerate, separated by only
approximately 2.07 meV per InGaZnO4 formula unit. `ordered_002` and
`ordered_004` are approximately 0.71–0.74 eV/f.u. above the minimum.

### Relaxed structural comparison

The two low-energy structures remain crystallographically distinct:

| Property | ordered_001 | ordered_003 |
|---|---|---|
| Space group | P3m1 (156) | R3m (160) |
| In coordination | 6 | 6 |
| Ga coordination | 5 | 5 |
| Zn coordination | 4 | 4 |
| Mean In–O distance (Å) | 2.194916 | 2.195080 |
| Mean Ga–O distance (Å) | 1.935413 | 1.935998 |
| Mean Zn–O distance (Å) | 1.986724 | 1.986415 |

pymatgen StructureMatcher does not identify `ordered_001` and
`ordered_003` as equivalent.

Despite their different long-range symmetry, their mean first-shell bond
lengths and coordination numbers are extremely similar.

### Bond-distribution analysis

| Bond | ordered_001 σ (Å) | ordered_003 σ (Å) |
|---|---:|---:|
| In–O | 0.002620 | 0.003106 |
| Ga–O | 0.037624 | 0.039067 |
| Zn–O | 0.016615 | 0.007362 |

The largest difference occurs in the ZnO4 environments.
`ordered_003` has a substantially narrower Zn–O bond-length
distribution.

### Polyhedral distortion analysis

Both structures retain:

- InO6 octahedral coordination;
- GaO5 trigonal-bipyramidal coordination under the current angular
  classifier;
- ZnO4 tetrahedral coordination.

Average bond-length distortion indices:

| Polyhedron | ordered_001 | ordered_003 |
|---|---:|---:|
| InO6 | 0.000707 | 0.001414 |
| GaO5 | 0.019031 | 0.019356 |
| ZnO4 | 0.007234 | 0.003208 |

Average angular RMS deviations:

| Polyhedron | ordered_001 (deg) | ordered_003 (deg) |
|---|---:|---:|
| InO6 | 6.6578 | 6.6509 |
| GaO5 | 0.2665 | 0.4342 |
| ZnO4 | 2.0054 | 2.5071 |

`ordered_003` cannot simply be described as less distorted overall.
Instead, the two orderings distribute local distortions differently.

The three symmetry-related In, Ga and Zn environments in `ordered_003`
are nearly identical, consistent with retained R3m symmetry.

### Crystalline reference selection

`ordered_003` is selected as the primary crystalline reference because:

1. it has the lowest tight single-point energy;
2. its energetic ordering relative to `ordered_001` is retained after
   tightening EPS_SCF from 1e-6 to 1e-7;
3. it retains R3m symmetry after relaxation; and
4. it exhibits highly uniform symmetry-related cation environments.

`ordered_001` is retained as a low-energy competing ordering.

---

## Fully Relaxed Crystalline Reference Selection

Cell optimisation was subsequently performed for the two low-energy
ordered structures, ordered_001 and ordered_003, using CP2K 2025.2 on
ARCHER2.

Both calculations used:

- PBE
- TZV2P-MOLOPT-PBE-GTH
- CUTOFF = 700 Ry
- REL_CUTOFF = 60 Ry
- 6 x 6 x 1 Monkhorst-Pack k-point sampling
- BFGS cell optimisation
- analytical stress tensor
- hexagonal cell symmetry
- zero external pressure
- pressure tolerance = 100 bar
- EPS_SCF = 1e-6 during CELL_OPT

Final cell parameters were:

| Model | a = b (A) | c (A) | Volume (A^3) | Final pressure (bar) |
|---|---:|---:|---:|---:|
| ordered_001 | 3.369483 | 26.210476 | 257.710482 | -1.50 |
| ordered_003 | 3.371432 | 26.171440 | 257.624398 | 96.31 |

Final tight single-point energies were recalculated using
EPS_SCF = 1e-7:

| Model | Energy (Ha) | Delta E (meV/f.u.) |
|---|---:|---:|
| ordered_003 | -767.259393316824 | 0.00 |
| ordered_001 | -767.259021707076 | 3.37 |

Full cell relaxation therefore preserves and slightly strengthens the
energetic preference for ordered_003.

The final primary crystalline computational reference is:

`igzo_crystal_ordered_003_cell_relaxed`

The P3m1 ordered_001 structure remains a near-degenerate secondary
ordering.

---

## 2026-08-28 — Crystalline R3m reference finalised

The crystalline reference selection and symmetry validation workflow
has been completed.

### Final structure

The canonical crystalline structure is:

`igzo_crystal_ordered_003_r3m_cell_relaxed`

Space group:

- R3m (160)

Final lattice:

- a = b = 3.3715680721 Å
- c = 26.1742696350 Å
- gamma = 60°
- volume = 257.673091903 Å³

Final R3m CELL_OPT pressure:

- -69.7746 bar

### Final tight energies

Unconstrained cell-relaxed structure:

- `E(P1) = -767.259393316824116 Ha`

R3m-constrained cell-relaxed structure:

- `E(R3m) = -767.259392342909337 Ha`

Energy difference:

- `E(R3m) - E(P1) ≈ 0.0265 meV/cell`
- `≈ 0.0088 meV/f.u.`

This difference is negligible. The apparent P1 distortion is therefore
not treated as evidence for a distinct lower-energy crystalline phase.

The R3m structure is adopted as the crystalline reference because it
retains the physically meaningful crystallographic symmetry while
remaining energetically indistinguishable from the unconstrained
minimum.

### Symmetry-equivalent oxygen sites

The 12 oxygen atoms reduce to four inequivalent sites:

| Site | Equivalent atoms | Multiplicity | Wyckoff | Environment |
| --- | --- | ---: | --- | --- |
| O001 | 9, 10, 11 | 3 | 3a | Ga3Zn1 |
| O002 | 12, 13, 14 | 3 | 3a | In3Zn1 |
| O003 | 15, 16, 17 | 3 | 3a | In3Ga1 |
| O004 | 18, 19, 20 | 3 | 3a | Ga1Zn3 |

This completes pristine crystalline reference validation.

Next stage:

1. select and converge the crystalline defect supercell;
2. map O001–O004 into the supercell;
3. generate representative oxygen-vacancy structures;
4. begin neutral vacancy relaxation calculations.

---

## Current Computational Status

- [x] Experimental CIF obtained
- [x] Crystallographic provenance recorded
- [x] Mixed Ga/Zn site identified
- [x] Ordering problem defined
- [x] Four symmetry-distinct configuration classes identified
- [x] Ordered structure files generated
- [x] Structures independently validated
- [x] CP2K basis/grid/k-point convergence completed for the current crystalline study
- [x] All ordered structures relaxed
- [x] Tight relative energies calculated
- [x] Low-energy structures structurally characterised
- [x] Primary crystalline reference selected
- [ ] Pristine crystalline DOS/PDOS/band analysis completed
- [X] Symmetry-inequivalent oxygen sites enumerated
- [ ] Defect supercell convergence completed
- [ ] Crystalline oxygen-vacancy calculations completed
- [ ] Amorphous IGZO generated
- [ ] MACE dataset/model completed
- [ ] LAMMPS large-scale sampling completed

---

## Next Scientific Step

Enumerate symmetry-inequivalent oxygen sites in
`igzo_crystal_ordered_003_relaxed`, record their multiplicities and local
cation environments, and generate the initial crystalline
oxygen-vacancy structures.

Defect supercell size and k-point sampling must then be validated before
production vacancy energetics are interpreted.
