# Computational Parameters

This document records validated computational parameters used throughout
the IGZO defect-modelling project.

Values marked `TBD` have not yet been established through convergence
testing or methodological validation.

Parameters should only be updated from `TBD` once the corresponding
validation has been completed.

---

# CP2K

## General

| Parameter | Value |
|---|---|
| CP2K version | TBD |
| Method | Quickstep / DFT |
| Representation | GPW/GAPW: TBD |
| XC functional | TBD |
| Dispersion correction | TBD |

## Basis Sets

| Element | Basis set |
|---|---|
| In | TBD |
| Ga | TBD |
| Zn | TBD |
| O | TBD |

Basis-set convergence/validation status:

    Pending

## Pseudopotentials

| Element | Pseudopotential |
|---|---|
| In | TBD |
| Ga | TBD |
| Zn | TBD |
| O | TBD |

Pseudopotential validation status:

    Pending

## Grid

| Parameter | Value |
|---|---|
| CUTOFF | TBD |
| REL_CUTOFF | TBD |
| NGRIDS | TBD |

Status:

    Pending convergence study

## SCF

| Parameter | Value |
|---|---|
| EPS_SCF | TBD |
| MAX_SCF | TBD |
| SCF method | TBD |
| Smearing | TBD |
| OT/diagonalisation | TBD |

## Brillouin-Zone Sampling

| System | k-point sampling |
|---|---|
| Crystalline IGZO | TBD |
| Amorphous IGZO | TBD |

## Geometry Optimisation

| Parameter | Value |
|---|---|
| Optimiser | TBD |
| MAX_FORCE | TBD |
| RMS_FORCE | TBD |
| MAX_DR | TBD |
| RMS_DR | TBD |
| Cell optimisation | TBD |

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

These parameters must be validated before production amorphisation.

---

# VASP

## General

| Parameter | Value |
|---|---|
| VASP version | TBD |
| XC functional | TBD |
| PAW datasets | TBD |
| ENCUT | TBD |
| PREC | TBD |

## Electronic Convergence

| Parameter | Value |
|---|---|
| EDIFF | TBD |
| ISMEAR | TBD |
| SIGMA | TBD |
| Spin treatment | TBD |

## Ionic Relaxation

| Parameter | Value |
|---|---|
| EDIFFG | TBD |
| IBRION | TBD |
| ISIF | TBD |
| NSW | TBD |

## k-points

    TBD

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

Production parameters should be traceable to the convergence or
validation calculation used to justify them.