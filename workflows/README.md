# Computational Workflows

This directory contains the computational workflows used throughout the
**IGZO Defect Modelling** project.

The project combines first-principles calculations, ab initio molecular
dynamics, machine-learning interatomic potentials, large-scale molecular
dynamics and workflow automation to investigate structural disorder,
oxygen vacancies and electronic properties in In-Ga-Zn-O (IGZO).

---

## Workflow Overview

The overall computational strategy is:

```text
Experimental crystalline IGZO
            │
            ▼
   Ordered crystalline models
            │
            ▼
     ┌──────┴──────┐
     │             │
     ▼             ▼
   CP2K           VASP
     │             │
     │             ├── crystalline DFT
     │             ├── electronic structure
     │             └── oxygen vacancies
     │
     ├── crystalline DFT
     ├── geometry optimisation
     └── AIMD
            │
            ▼
       Melt / quench
            │
            ▼
       Amorphous IGZO
            │
            ▼
   DFT reference dataset
            │
            ▼
           MACE
            │
            ▼
     Model validation
            │
            ▼
          LAMMPS
            │
            ▼
   Large-scale sampling
            │
            ▼
 Oxygen-vacancy statistics
            │
            ▼
 Structural + electronic analysis
```

AiiDA will progressively provide workflow automation and provenance
across appropriate stages of this pipeline.

---

# Directory Structure

```text
workflows/
├── README.md
│
├── vasp/
│   ├── convergence/
│   ├── relaxation/
│   ├── electronic_structure/
│   └── defects/
│
├── cp2k/
│   ├── convergence/
│   ├── relaxation/
│   ├── electronic_structure/
│   └── amorphisation/
│
├── mace/
│
├── lammps/
│
└── aiida/
```

Each workflow directory should contain the files required to reproduce
the corresponding computational methodology without requiring large raw
simulation outputs to be stored in Git.

---

# VASP

VASP is intended primarily for high-accuracy crystalline and defect
calculations.

Planned applications include:

- crystalline IGZO structural relaxation
- convergence testing
- electronic structure
- density of states
- projected density of states
- oxygen-vacancy calculations
- defect formation energies
- defect charge states
- comparison between pristine and defective structures

The VASP workflow will be developed further once the required licence
and computational environment are available.

Where appropriate, VASP calculations will provide an independent
comparison with CP2K results.

---

# CP2K

CP2K provides the initial first-principles route while the VASP workflow
is being established.

Planned applications include:

- crystalline IGZO DFT
- convergence testing
- geometry optimisation
- energetic comparison of Ga/Zn ordered models
- ab initio molecular dynamics
- melt-quench amorphisation
- generation of DFT reference configurations for MACE

The immediate workflow is:

```text
Ordered crystalline models
            ↓
     CP2K convergence
            ↓
     Geometry optimisation
            ↓
   Relative-energy comparison
            ↓
Select crystalline reference
            ↓
          AIMD
            ↓
       Melt / quench
            ↓
       Amorphous IGZO
```

See:

```text
cp2k/README.md
```

for the detailed CP2K methodology.

---

# MACE

MACE will be used to develop machine-learning interatomic potentials
for IGZO.

Reference data will initially be generated using first-principles
calculations.

The intended workflow is:

```text
DFT configurations
       ↓
Dataset construction
       ↓
Train / validation / test split
       ↓
MACE training
       ↓
Energy validation
       ↓
Force validation
       ↓
Structural validation
       ↓
MD stability testing
       ↓
Validated potential
```

The potential must be validated within its intended configuration space
before production molecular dynamics is performed.

Potential training data may include:

- crystalline structures
- thermally distorted crystalline structures
- AIMD melt configurations
- liquid configurations
- quench configurations
- amorphous structures
- defect environments where required

---

# LAMMPS

LAMMPS will be used for large-scale molecular dynamics once a suitable
MACE potential has been validated.

Planned applications include:

- larger simulation cells
- longer molecular-dynamics trajectories
- multiple independent amorphisation trajectories
- structural ensemble generation
- finite-temperature sampling
- statistically meaningful defect-environment sampling

The intended workflow is:

```text
Validated MACE model
        ↓
LAMMPS integration tests
        ↓
Small-system validation
        ↓
Production MD
        ↓
Large amorphous ensemble
        ↓
Structural statistics
        ↓
Representative configurations
        ↓
DFT validation / defect calculations
```

Large trajectories should normally remain on HPC or research-data
storage rather than GitHub.

---

# AiiDA

AiiDA will be used progressively for workflow automation and
computational provenance.

Potential applications include:

- structure provenance
- automated DFT calculations
- convergence studies
- high-throughput oxygen-vacancy calculations
- calculation monitoring
- metadata management
- reproducibility
- linking parent and derived calculations

A typical provenance chain may eventually be represented as:

```text
Reference structure
       ↓
Ordered structure
       ↓
DFT relaxation
       ↓
AIMD trajectory
       ↓
Amorphous structure
       ↓
MACE dataset
       ↓
MACE model
       ↓
LAMMPS structure
       ↓
Defect structure
       ↓
DFT defect calculation
       ↓
Final analysis
```

---

# Relationship to Structures

Workflow inputs should reference structures stored under:

```text
structures/
├── crystalline/
├── amorphous/
└── defects/
```

Where practical, structures should be referenced or generated
programmatically rather than duplicated unnecessarily throughout the
repository.

The original experimental crystallographic structures should remain
separate from computationally generated structures.

---

# Computational Parameters

Validated computational parameters should be documented centrally in:

```text
docs/computational_parameters.md
```

This should eventually include parameters such as:

## CP2K

- CP2K version
- exchange-correlation functional
- basis sets
- pseudopotentials
- CUTOFF
- REL_CUTOFF
- k-point sampling
- SCF criteria
- geometry optimisation criteria
- AIMD timestep
- thermostat
- ensemble
- melt/quench schedule

## VASP

- VASP version
- PAW datasets
- exchange-correlation functional
- plane-wave cutoff
- k-point mesh
- electronic convergence
- ionic convergence
- smearing
- spin treatment
- defect methodology

## MACE

- MACE version
- dataset version
- architecture
- cutoff radius
- loss weights
- optimisation parameters
- random seed
- training/validation/test split

## LAMMPS

- LAMMPS version
- MACE model version
- timestep
- ensemble
- thermostat/barostat
- temperature
- pressure
- simulation length

---

# Data Management

The Git repository should contain the information required to reproduce
the workflows without becoming a storage location for large simulation
data.

## Commit to GitHub

Where appropriate:

- input templates
- workflow scripts
- job submission scripts
- configuration files
- convergence scripts
- analysis scripts
- metadata schemas
- documentation
- small example inputs/outputs
- selected structures
- selected final results

## Keep on HPC / Research Storage

Normally exclude:

- large AIMD trajectories
- complete production MD trajectories
- wavefunction files
- restart files
- temporary calculation files
- large raw output files
- large training datasets
- model checkpoints during training
- intermediate calculation directories

Curated datasets and trained models may later be deposited in an
appropriate research-data repository rather than committed directly to
GitHub.

---

# Intellectual Property

This repository forms part of the R&D activity of **Nanosystems
Advisory**.

Before committing computational results, datasets, trained models or
methods that may have commercial value, consider whether they contain:

- potentially patentable results
- proprietary workflow details
- commercially sensitive parameters
- unpublished research findings
- proprietary datasets
- confidential collaboration data

GitHub should primarily contain the reproducible research infrastructure
that has been approved for inclusion in the repository.

Potentially sensitive research outputs should remain on controlled
research storage until an appropriate publication or IP decision has
been made.

---

# Reproducibility

Each production workflow should ultimately record:

```text
input structure
      +
software version
      +
computational parameters
      +
input files
      +
workflow version
      +
HPC environment
      +
metadata
      +
analysis method
```

This should allow important scientific results to be traced back to
their computational origin.

---

# Current Project Status

## Crystalline structures

- [x] Identify experimental InGaZnO4 reference
- [x] Obtain COD reference structure
- [x] Identify Ga/Zn partial occupancy
- [x] Establish ordering methodology
- [ ] Generate ordered structures
- [ ] Validate ordered structures

## CP2K

- [x] Define workflow strategy
- [ ] Establish convergence workflow
- [ ] Converge numerical parameters
- [ ] Relax ordered structures
- [ ] Compare relative energies
- [ ] Select crystalline reference
- [ ] Develop AIMD workflow
- [ ] Establish melt-quench protocol

## VASP

- [ ] Establish computational environment
- [ ] Implement convergence workflow
- [ ] Relax crystalline reference
- [ ] Calculate pristine electronic structure
- [ ] Implement oxygen-vacancy workflow

## MACE

- [ ] Generate DFT reference dataset
- [ ] Construct training dataset
- [ ] Train initial model
- [ ] Validate model
- [ ] Establish domain of validity

## LAMMPS

- [ ] Integrate validated MACE model
- [ ] Validate small-system MD
- [ ] Perform large-scale sampling
- [ ] Generate amorphous structural ensemble

## AiiDA

- [ ] Define provenance strategy
- [ ] Implement initial workflows
- [ ] Automate high-throughput calculations

---

# Immediate Next Steps

The current priority is:

```text
Generate ordered IGZO structures
             ↓
Validate structures
             ↓
Establish CP2K convergence workflow
             ↓
Relax four ordered models
             ↓
Compare relative energies
             ↓
Select crystalline reference
```

Only after the crystalline reference and CP2K methodology have been
validated should production amorphisation calculations begin.