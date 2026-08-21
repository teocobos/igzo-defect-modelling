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

## CP2K SCF Optimisation — Final Selection

The crystalline IGZO SCF strategy was tested using the converged
numerical setup:

- PBE
- TZV2P-MOLOPT-PBE-GTH
- CUTOFF = 700 Ry
- REL_CUTOFF = 60 Ry
- 6×6×1 k-point mesh

### Results

| Method | SCF iterations | Wall time (s) | Status |
|---|---:|---:|---|
| Broyden mixing | 32 | 1240.878 | Converged |
| Pulay mixing | 17 | 700.825 | Converged |
| Low-alpha Broyden | — | — | Runtime failure |
| New Pulay mixing | — | — | SIGABRT/SIGBUS runtime failure |

### Decision

Standard `PULAY_MIXING` with `ALPHA = 0.20` and `NBUFFER = 8` was
selected as the production SCF strategy.

It converged to the same total energy as the Broyden baseline while
approximately halving the number of SCF iterations and substantially
reducing wall time.

The unstable alternative mixing schemes were not pursued further because
their failures were runtime-level process faults rather than ordinary
SCF non-convergence.

---
## Current Computational Status

- [x] Experimental CIF obtained
- [x] Crystallographic provenance recorded
- [x] Mixed Ga/Zn site identified
- [x] Ordering problem defined
- [x] Four symmetry-distinct configuration classes identified
- [x] Ordered structure files generated
- [x] Structures independently validated
- [ ] CP2K convergence completed
- [ ] Ordered structures relaxed
- [ ] Relative energies calculated
- [ ] Crystalline reference selected

---

# Scientific Results

No production DFT, defect, AIMD, MACE or LAMMPS results have yet been
recorded.

Future validated results should be added chronologically below this
section.