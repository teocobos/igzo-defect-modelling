# CP2K Workflows

This directory contains CP2K workflows used in the IGZO defect-modelling project.

CP2K is initially used for:

* crystalline IGZO DFT calculations
* convergence testing
* geometry optimisation
* comparison of ordered Ga/Zn configurations
* ab initio molecular dynamics
* melt-quench amorphisation
* generation of reference configurations for MACE

## Directory Structure

The intended structure is:

```text
cp2k/
├── README.md
├── convergence/
├── relaxation/
├── electronic_structure/
└── amorphisation/
```

### `convergence/`

Contains calculations used to establish appropriate CP2K numerical parameters.

### `relaxation/`

Contains workflows for geometry optimisation of crystalline and selected amorphous structures.

### `electronic_structure/`

Contains CP2K electronic-structure calculations where appropriate.

### `amorphisation/`

Contains AIMD melt-quench workflows used to generate amorphous IGZO.

---

# Computational Strategy

The initial CP2K workflow is:

```text
Experimental CIF
       ↓
Ordered crystalline models
       ↓
CP2K convergence
       ↓
Geometry optimisation
       ↓
Relative-energy comparison
       ↓
Selected crystalline model
       ↓
AIMD
       ↓
Melt
       ↓
Quench
       ↓
Amorphous IGZO
```

---

# Stage 1 — Convergence

Before production calculations, numerical parameters should be tested systematically.

Initial convergence studies should consider:

* basis-set quality
* pseudopotentials
* plane-wave cutoff
* relative cutoff
* SCF convergence
* k-point sampling
* geometry-optimisation tolerances

Convergence should be assessed using scientifically relevant quantities rather than simply confirming that a calculation completes.

Potential quantities include:

* total energy per formula unit
* forces
* lattice parameters
* relative energies between ordered models

Final validated settings should be documented in:

```text
docs/computational_parameters.md
```

---

# Stage 2 — Ordered-Model Relaxation

The symmetry-distinct crystalline Ga/Zn configurations should be relaxed using a consistent computational setup.

For each model, record:

* initial structure
* final structure
* total energy
* energy per formula unit
* relative energy
* cell parameters
* atomic forces
* convergence status

The initial models are:

```text
igzo_crystal_ordered_001
igzo_crystal_ordered_002
igzo_crystal_ordered_003
igzo_crystal_ordered_004
```

No model should be considered the preferred crystalline reference before this comparison is completed.

---

# Stage 3 — Electronic Structure

After selecting the crystalline reference model, CP2K may be used to investigate quantities such as:

* electronic density of states
* projected density of states
* charge distribution
* defect-induced states

VASP calculations can subsequently provide an independent or complementary electronic-structure workflow.

---

# Stage 4 — Amor­phisation

CP2K AIMD will be used to generate first-principles amorphous IGZO configurations.

The intended procedure is:

```text
Crystalline / initial structure
            ↓
        Equilibration
            ↓
           Heating
            ↓
            Melt
            ↓
           Quench
            ↓
     Low-temperature AIMD
            ↓
        DFT relaxation
            ↓
       Amorphous IGZO
```

Parameters such as melt temperature, simulation duration and cooling rate must be validated rather than assumed.

Multiple independent trajectories should be generated to reduce dependence on a single melt-quench history.

---

# Data Management

Large CP2K output should normally remain on HPC or research-data storage.

## Commit to GitHub

Examples:

* input templates
* workflow scripts
* job submission templates
* parameter files
* analysis scripts
* small example calculations
* documentation
* selected final structures

## Keep on HPC / Research Storage

Examples:

* long AIMD trajectories
* wavefunction restart files
* large output files
* temporary files
* intermediate trajectories
* large batches of calculations

---

# Reproducibility

Every production calculation should be traceable to:

```text
structure
   +
CP2K input
   +
basis set
   +
pseudopotential
   +
software version
   +
HPC environment
   +
workflow configuration
```

Where practical, AiiDA should eventually be used to automate calculations and retain computational provenance.

---

# Current Status

* [x] CP2K selected for crystalline DFT and AIMD
* [x] CP2K workflow structure defined
* [ ] Generate ordered crystalline models
* [ ] Establish convergence workflow
* [ ] Select basis sets
* [ ] Select pseudopotentials
* [ ] Converge CUTOFF
* [ ] Converge REL_CUTOFF
* [ ] Test k-point sampling
* [ ] Establish SCF settings
* [ ] Relax four ordered IGZO models
* [ ] Compare relative energies
* [ ] Select crystalline reference model
* [ ] Begin AIMD protocol development
