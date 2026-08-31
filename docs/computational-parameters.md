# Computational Parameters

This document records validated computational parameters used throughout the IGZO defect-modelling project.

Values marked `TBD` have not yet been established through convergence testing or methodological validation.

Parameters should only be promoted to production use once the relevant validation has been completed.

---

# CP2K

## General

| Parameter                   | Current value                         |
| --------------------------- | ------------------------------------- |
| Local CP2K version          | 2026.2                                |
| ARCHER2 production version  | 2025.2                                |
| Method                      | Quickstep / DFT                       |
| Representation              | GPW                                   |
| Current PBE functional      | PBE                                   |
| Hybrid functional           | PBE0-TC-LRC — validation pending      |
| Dispersion correction       | None for current crystalline workflow |
| Primary production platform | ARCHER2                               |

Local CP2K 2026.2 is used for workflow development and selected numerical testing.

Production crystalline calculations are performed on ARCHER2 using CP2K 2025.2.

---

## Basis Sets

Validated PBE crystalline basis:

| Element | Basis set                  |
| ------- | -------------------------- |
| In      | `TZV2P-MOLOPT-PBE-GTH-q13` |
| Ga      | `TZV2P-MOLOPT-PBE-GTH-q13` |
| Zn      | `TZV2P-MOLOPT-PBE-GTH-q12` |
| O       | `TZV2P-MOLOPT-PBE-GTH-q6`  |

Data-file families:

```text
Local CP2K 2026.2:
BASIS_MOLOPT_UZH_2026.2

ARCHER2 CP2K 2025.2:
BASIS_MOLOPT_UZH
```

Basis-set sensitivity was tested using DZVP, TZVP and TZV2P.

| Basis | ΔE vs TZV2P / meV/f.u. |
| ----- | ---------------------: |
| DZVP  |                253.314 |
| TZVP  |                 70.201 |
| TZV2P |                  0.000 |

**Status:** TZV2P selected for the PBE crystalline workflow.

Hybrid-specific basis suitability will be checked during PBE0-TC-LRC validation.

---

## Pseudopotentials

Validated PBE pseudopotentials:

| Element | Pseudopotential |
| ------- | --------------- |
| In      | `GTH-PBE-q13`   |
| Ga      | `GTH-PBE-q13`   |
| Zn      | `GTH-PBE-q12`   |
| O       | `GTH-PBE-q6`    |

Data-file families:

```text
Local CP2K 2026.2:
POTENTIAL_UZH_2026.2

ARCHER2 CP2K 2025.2:
POTENTIAL_UZH
```

**Status:** validated for PBE crystalline calculations.

---

## Grid

| Parameter  | Production value |
| ---------- | ---------------: |
| CUTOFF     |           700 Ry |
| REL_CUTOFF |            60 Ry |
| NGRIDS     |                4 |

Validation:

* 600 → 700 Ry changed the energy by approximately 0.65 meV/f.u.;
* 50 → 60 Ry REL_CUTOFF changed the energy by approximately 0.024 meV/f.u.

**Status:** validated.

Production inputs explicitly contain:

```text
&MGRID
  CUTOFF 700
  REL_CUTOFF 60
&END MGRID

&QS
  METHOD GPW
  EPS_PGF_ORB 1.0E-18
  EPS_FILTER_MATRIX 0.0
&END QS

&POISSON
  PERIODIC XYZ
&END POISSON
```

These blocks must not be omitted from production calculations.

---

## Primitive-Cell SCF

Geometry optimisation:

| Parameter              | Value                |
| ---------------------- | -------------------- |
| EPS_SCF                | `1.0E-6`             |
| MAX_SCF                | 200                  |
| Solver                 | diagonalisation      |
| Mixing                 | `BROYDEN_MIXING`     |
| ALPHA                  | 0.10                 |
| BETA                   | 1.5                  |
| NBUFFER                | 4                    |
| Smearing               | Fermi–Dirac          |
| Electronic temperature | 300 K                |
| ADDED_MOS              | 40                   |
| Diagonalisation        | `ALGORITHM STANDARD` |
| Preferred library      | ScaLAPACK            |

Final tight energies:

```text
EPS_SCF = 1.0E-7
```

`IGNORE_CONVERGENCE_FAILURE` is not used for production geometry optimisation.

---

## Primitive-Cell Brillouin-Zone Sampling

| System                       | Sampling             |
| ---------------------------- | -------------------- |
| 21-atom crystalline R3m IGZO | 6×6×1 Monkhorst-Pack |

The 5×5×1 → 6×6×1 change was approximately 4.5 meV/f.u.

**Status:** validated for the 21-atom PBE crystalline reference.

---

## Final PBE Crystalline Reference

Canonical reference:

```text
igzo_crystal_ordered_003_r3m_cell_relaxed
```

Validated methodology:

* PBE;
* TZV2P-MOLOPT-PBE-GTH;
* matching GTH-PBE potentials;
* 700 Ry CUTOFF;
* 60 Ry REL_CUTOFF;
* 6×6×1 k-points;
* Broyden mixing;
* 300 K Fermi–Dirac smearing;
* ADDED_MOS = 40;
* BFGS;
* R3m-preserving CELL_OPT;
* final EPS_SCF = 1e-7.

Final R3m lattice:

```text
a = b = 3.3715680721 Å
c = 26.1742696350 Å
alpha = beta = 90°
```

Equivalent CP2K hexagonal representation:

```text
gamma = 60°
```

Final volume:

```text
257.673091903 Å^3
```

Final pressure:

```text
-69.7746 bar
```

Final tight energy:

```text
E(R3m) = -767.259392342909337 Ha
```

---

# PBE Neutral Oxygen-Vacancy Workflow

## Production Supercell

Selected production supercell:

```text
4×4×1
```

Composition:

```text
Pristine: 336 atoms
V_O^0:    335 atoms
```

Exact CP2K production cell:

```text
&CELL
  A 13.486272280000 0.000000000000 0.000000000000
  B -6.743136140000 11.679454396834 0.000000000000
  C 0.000000000000 0.000000000000 26.174269630000
  PERIODIC XYZ
&END CELL
```

This is the 120° representation used by the validated O001 production calculation.

The pristine supercell is generated by exact replication of the optimised primitive reference.

No separate CELL_OPT is performed on the replicated pristine supercell.

---

## Production Vacancy Sampling

Production PBE neutral vacancies use:

```text
Γ-only
```

For the OT workflow, Γ-only is represented by omission of an explicit `&KPOINTS` section.

The production decision is based on explicit O001 validation against:

* 3×3×1 + 2×2×1 + diagonalisation;
* 3×3×1 + Γ + diagonalisation;
* 3×3×1 + Γ + OT;
* 4×4×1 + Γ + OT.

The Γ-point OT and diagonalisation calculations reproduce essentially identical O001 energies and local reconstructions.

---

## Production Vacancy SCF

```text
&SCF
  EPS_SCF 1.0E-6
  MAX_SCF 150
  SCF_GUESS ATOMIC

  &OT
    MINIMIZER DIIS
    PRECONDITIONER FULL_SINGLE_INVERSE
  &END OT

  &OUTER_SCF
    MAX_SCF 20
    EPS_SCF 1.0E-6
  &END OUTER_SCF
&END SCF
```

No diagonalisation mixing block, smearing or ADDED_MOS is used in the Γ+OT production workflow.

---

## Production Vacancy Geometry Optimisation

| Parameter            | Value                    |
| -------------------- | ------------------------ |
| RUN_TYPE             | `GEO_OPT`                |
| Optimiser            | BFGS                     |
| Cell treatment       | fixed pristine supercell |
| EPS_SCF              | `1.0E-6`                 |
| Charge               | 0                        |
| Initial multiplicity | 1                        |

The supercell lattice remains fixed during defect relaxation.

The defective supercell is not CELL_OPTed.

---

## O001 Solver Validation

3×3×1 Γ calculations:

```text
Γ + diagonalisation:
E = -6889.147763739658330 Ha

Γ + OT tight:
E = -6889.147760105754969 Ha
```

Difference:

```text
~9.9E-5 eV per defect cell
```

The first-shell reconstructions are also essentially identical.

This validates OT as an efficient Γ-point solver for the current large-cell PBE screening workflow.

---

## O001 Supercell-Size Sensitivity

Matched Γ+OT differences:

```text
ΔE(3×3×1) = 16.076899548553229 Ha
ΔE(4×4×1) = 16.081291151052937 Ha
```

Difference:

```text
~0.1195 eV
```

This residual finite-size sensitivity should be retained as part of the uncertainty/validation context for neutral-vacancy screening.

---

# PBE0-TC-LRC

## Status

```text
VALIDATION PENDING
```

PBE0-TC-LRC will be validated before production hybrid defect calculations.

The intended sequence is:

```text
PBE R3m geometry
      ↓
PBE0-TC-LRC pristine single point
      ↓
PBE0-TC-LRC R3m CELL_OPT
      ↓
tight hybrid pristine reference
      ↓
hybrid defect calculations
```

Hybrid parameters must not be copied blindly from previous oxide projects.

Parameters requiring explicit validation include:

| Parameter                     | Status       |
| ----------------------------- | ------------ |
| Exact-exchange fraction       | TBD/validate |
| TC/LRC treatment              | TBD/validate |
| Interaction/truncation radius | TBD/validate |
| Auxiliary basis/ADMM strategy | TBD/validate |
| SCF solver                    | TBD/validate |
| k-point treatment             | TBD/validate |
| EPS_SCF                       | TBD/validate |
| Hybrid CELL_OPT settings      | TBD/validate |
| Band gap                      | validate     |
| Band-edge character           | validate     |
| Structural parameters         | validate     |

The final hybrid pristine lattice will be replicated to construct hybrid defect supercells.

Hybrid defect supercells will be relaxed at fixed cell.

---

# CP2K AIMD

| Parameter                         | Value |
| --------------------------------- | ----- |
| Ensemble                          | TBD   |
| Timestep                          | TBD   |
| Thermostat                        | TBD   |
| Barostat                          | TBD   |
| Initial temperature               | TBD   |
| Melt temperature                  | TBD   |
| Melt duration                     | TBD   |
| Quench rate                       | TBD   |
| Final temperature                 | TBD   |
| Final equilibration               | TBD   |
| Initial amorphous-cell size/shape | TBD   |
| Target density                    | TBD   |

---

# VASP

VASP remains a complementary crystalline/electronic-structure workflow.

No VASP production parameters have yet been validated.

---

# MACE

Model and dataset parameters remain TBD pending first-principles dataset generation.

---

# LAMMPS

LAMMPS production parameters remain TBD pending MACE validation.

---

# Parameter Approval

Parameters progress through:

```text
proposed
   ↓
convergence testing
   ↓
validation
   ↓
production
```

The PBE crystalline reference and 4×4×1 Γ+OT neutral-vacancy screening workflow have reached production status.

PBE0-TC-LRC remains in the validation stage.