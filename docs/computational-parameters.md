# Computational Parameters

This document records validated computational parameters used throughout
the IGZO defect-modelling project.

Values marked `TBD` have not yet been established through convergence
testing or methodological validation.

Parameters should only be promoted to production use once the relevant
validation has been completed.

---

# CP2K

## General

| Parameter | Current value |
|---|---|
| Local CP2K version | 2026.2 |
| ARCHER2 production version | 2025.2 |
| Method | Quickstep / DFT |
| Representation | GPW |
| XC functional | PBE |
| Dispersion correction | None for the current crystalline reference workflow |
| Primary production platform | ARCHER2 |

The local CP2K 2026.2 environment was used for initial smoke tests and
numerical convergence studies. Production ordered-structure geometry
optimisations and final tight single-point calculations were completed on
ARCHER2 using CP2K 2025.2.

---

## Basis Sets

Current crystalline production basis:

| Element | Basis set |
|---|---|
| In | `TZV2P-MOLOPT-PBE-GTH-q13` |
| Ga | `TZV2P-MOLOPT-PBE-GTH-q13` |
| Zn | `TZV2P-MOLOPT-PBE-GTH-q12` |
| O | `TZV2P-MOLOPT-PBE-GTH-q6` |

Data-file families used:

- local CP2K 2026.2: `BASIS_MOLOPT_UZH_2026.2`
- ARCHER2 CP2K 2025.2: `BASIS_MOLOPT_UZH`

Basis-set sensitivity was tested using DZVP, TZVP and TZV2P.

Preliminary energy differences relative to TZV2P at the test grid were:

| Basis | ΔE vs TZV2P (meV/f.u.) |
|---|---:|
| DZVP | 253.314 |
| TZVP | 70.201 |
| TZV2P | 0.000 |

**Status:** TZV2P selected as the crystalline reference basis.

---

## Pseudopotentials

Current crystalline production pseudopotentials:

| Element | Pseudopotential |
|---|---|
| In | `GTH-PBE-q13` |
| Ga | `GTH-PBE-q13` |
| Zn | `GTH-PBE-q12` |
| O | `GTH-PBE-q6` |

Data-file families used:

- local CP2K 2026.2: `POTENTIAL_UZH_2026.2`
- ARCHER2 CP2K 2025.2: `POTENTIAL_UZH`

The basis and pseudopotential valence definitions are matched element by
element.

**Status:** validated for the current PBE crystalline workflow.

---

## Grid

| Parameter | Production value |
|---|---:|
| CUTOFF | 700 Ry |
| REL_CUTOFF | 60 Ry |
| NGRIDS | 4 |

Validation summary:

- 600 → 700 Ry changed the energy by approximately 0.65 meV/f.u.
  in the cutoff series.
- REL_CUTOFF = 60 Ry was numerically stable, with the 50 → 60 Ry
  change approximately 0.024 meV/f.u.

**Status:** validated for the current crystalline ordering study.

---

## SCF

### Geometry optimisation

| Parameter | Production value |
|---|---|
| EPS_SCF | `1.0E-6` |
| MAX_SCF | 200 |
| SCF method | diagonalisation with `BROYDEN_MIXING` |
| ALPHA | 0.10 |
| BETA | 1.5 |
| NBUFFER | 4 |
| Smearing | Fermi–Dirac |
| Electronic temperature | 300 K |
| ADDED_MOS | 40 |
| Diagonalisation | `ALGORITHM STANDARD` |
| Preferred diagonalisation library | ScaLAPACK |

### Final single-point energies

| Parameter | Production value |
|---|---|
| EPS_SCF | `1.0E-7` |
| MAX_SCF | 200 |
| k-point sampling | same as production crystalline mesh |

A local benchmark showed that standard Pulay mixing could converge a
fixed-geometry 6×6×1 calculation faster than the original Broyden
baseline. However, Pulay-related runtime/conditioning failures were
encountered during local geometry-optimisation development under WSL.
The completed ARCHER2 production geometry optimisations therefore used
the robust Broyden setup above.

`IGNORE_CONVERGENCE_FAILURE` is not used for production geometry
optimisation.

---

## Brillouin-Zone Sampling

| System | k-point sampling |
|---|---|
| 21-atom crystalline ordered IGZO | 6×6×1 Monkhorst–Pack |
| Crystalline defect supercells | TBD; must be reconverged for supercell size |
| Amorphous IGZO | expected to approach Γ-only for sufficiently large cells, but validation is TBD |

The 5×5×1 → 6×6×1 energy change was approximately 4.5 meV/f.u.

**Status:** 6×6×1 selected for the current 21-atom crystalline reference cell.

---

## Geometry Optimisation

Current ordered-structure production workflow:

| Parameter | Value |
|---|---|
| RUN_TYPE | `GEO_OPT` |
| Optimiser | BFGS |
| Cell treatment | fixed experimental cell |
| MAX_FORCE | CP2K default |
| RMS_FORCE | CP2K default |
| MAX_DR | CP2K default |
| RMS_DR | CP2K default |
| EPS_SCF | `1.0E-6` |

All four ordered crystalline candidates converged successfully on
ARCHER2.

A final `RUN_TYPE ENERGY` calculation with `EPS_SCF = 1.0E-7` was
performed on each relaxed structure before energetic ranking.

---

## Final crystalline reference optimisation

The primary crystalline IGZO reference is the ordered `ordered_003`
configuration derived from COD 1521670.

The final crystalline structure was obtained using CP2K with:

- Method: Quickstep / GPW
- Exchange-correlation functional: PBE
- Basis set:
  - In: `TZV2P-MOLOPT-PBE-GTH-q13`
  - Ga: `TZV2P-MOLOPT-PBE-GTH-q13`
  - Zn: `TZV2P-MOLOPT-PBE-GTH-q12`
  - O: `TZV2P-MOLOPT-PBE-GTH-q6`
- Pseudopotentials: matching GTH-PBE potentials
- Plane-wave cutoff: 700 Ry
- Relative cutoff: 60 Ry
- k-point mesh: 6 × 6 × 1
- SCF mixing: Broyden
- Electronic temperature: 300 K Fermi-Dirac smearing
- Added molecular orbitals: 40
- Geometry/cell optimiser: BFGS
- Final tight single-point SCF threshold: `EPS_SCF = 1.0E-7`

### Symmetry-constrained cell optimisation

A final CELL_OPT calculation was performed for `ordered_003` while
preserving the R3m space group using `KEEP_SPACE_GROUP TRUE`.

The converged lattice parameters were:

- a = b = 3.3715680721 Å
- c = 26.1742696350 Å
- alpha = beta = 90°
- gamma = 60°
- volume = 257.673091903 Å³

The 60° gamma convention is the CP2K hexagonal representation of the
rhombohedral/hexagonal lattice.

The final internal pressure was:

- -69.7746 bar

which satisfied the specified pressure tolerance of 100 bar.

### Final reference energy

The final tight single-point energy of the R3m-constrained structure was:

- `E(R3m) = -767.259392342909337 Ha`

The corresponding unconstrained cell-relaxed structure had:

- `E(P1) = -767.259393316824116 Ha`

The difference is approximately:

- 0.0265 meV per 21-atom cell
- 0.0088 meV per formula unit

The two structures are therefore effectively energetically degenerate
at the precision relevant to the present workflow.

---

# CP2K AIMD

| Parameter | Value |
|---|---|
| Ensemble | TBD |
| Timestep | TBD |
| Thermostat | TBD |
| Barostat | TBD |
| Initial temperature | TBD |
| Melt temperature | TBD |
| Melt duration | TBD |
| Quench rate | TBD |
| Final temperature | TBD |
| Final equilibration | TBD |
| Initial amorphous-cell size/shape | TBD |
| Target density | TBD |

These parameters must be validated before production amorphisation.

---

# VASP

VASP remains a complementary crystalline/electronic-structure workflow.
No VASP production parameters have yet been validated for this project.

| Parameter | Value |
|---|---|
| VASP version | TBD |
| XC functional | TBD |
| PAW datasets | TBD |
| ENCUT | TBD |
| PREC | TBD |
| EDIFF | TBD |
| ISMEAR | TBD |
| SIGMA | TBD |
| Spin treatment | TBD |
| EDIFFG | TBD |
| IBRION | TBD |
| ISIF | TBD |
| NSW | TBD |
| k-points | TBD |

---

# MACE

| Parameter | Value |
|---|---|
| MACE version | TBD |
| Dataset version | TBD |
| Model architecture | TBD |
| Interaction cutoff | TBD |
| Number of layers | TBD |
| Energy weight | TBD |
| Force weight | TBD |
| Stress weight | TBD |
| Optimiser | TBD |
| Learning rate | TBD |
| Random seed | TBD |

---

# LAMMPS

| Parameter | Value |
|---|---|
| LAMMPS version | TBD |
| MACE model | TBD |
| Timestep | TBD |
| Ensemble | TBD |
| Thermostat | TBD |
| Barostat | TBD |
| Production duration | TBD |
| Sampling interval | TBD |

---

# Parameter Approval

Parameters should progress through:

    proposed
       ↓
    convergence testing
       ↓
    validation
       ↓
    production

Current validated crystalline CP2K production parameters are traceable
to the convergence and ordered-structure calculations recorded in
`docs/results-log.md`.
