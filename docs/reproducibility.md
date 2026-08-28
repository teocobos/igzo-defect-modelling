# Reproducibility

Reproducibility and computational provenance are core requirements of
the IGZO defect-modelling project.

---

## Provenance Chain

    COD 1521670
          ↓
    experimental CIF
          ↓
    generate_igzo_orderings.py
          ↓
    four ordered crystalline models
          ↓
    converged CP2K relaxation + tight energies
          ↓
    igzo_crystal_ordered_003_relaxed
       ┌──────────────┴──────────────┐
       ↓                             ↓
    crystalline defects          CP2K AIMD
                                     ↓
                                amorphous IGZO
                                     ↓
                                  DFT dataset
                                     ↓
                                    MACE
                                     ↓
                                   LAMMPS
                                     ↓
                              sampled configurations
                                     ↓
                                defect statistics
                                     ↓
                                   analysis

---

## Reference Structures

External structures should:

- remain unmodified;
- retain database identifiers;
- retain publication provenance;
- remain separate from derived structures.

Current experimental reference:

    COD 1521670

Current primary derived crystalline reference:

    igzo_crystal_ordered_003_relaxed

Secondary low-energy ordering:

    igzo_crystal_ordered_001_relaxed

---

## Generated Structures

Derived structures should record:

- structure ID;
- parent structure;
- generation method;
- generation script;
- software/version;
- ordering identifier where appropriate;
- composition;
- relaxation parent where appropriate;
- reference/secondary status where appropriate.

Programmatic generation is preferred to manual editing.

---

## Calculations

Production calculations should record:

- calculation ID;
- structure ID;
- software;
- software version;
- computational parameters;
- basis sets/pseudopotentials;
- parent calculation;
- restart parent if used;
- HPC environment;
- scheduler job ID;
- status;
- final energy where appropriate.

---

## Canonical crystalline structure provenance

The final crystalline reference is generated directly from the
high-precision CP2K CELL_OPT restart coordinates using:

`scripts/structure_generation/extract_cp2k_r3m_reference.py`

The generated canonical files are:

- `structures/crystalline/cell_relaxed/igzo_crystal_ordered_003_r3m_cell_relaxed/igzo_crystal_ordered_003_r3m_cell_relaxed.xyz`
- `structures/crystalline/cell_relaxed/igzo_crystal_ordered_003_r3m_cell_relaxed/igzo_crystal_ordered_003_r3m_cell_relaxed.cif`

The CP2K restart file itself is not intended for version control because
restart and wavefunction files may be large and are machine/run-state
artifacts.

The canonical CIF is written using a symmetry tolerance of
`2.0E-3 Å`, which recovers R3m (160) for the final DFT-relaxed
structure.

Symmetry-inequivalent oxygen sites are generated using:

`scripts/structure_generation/enumerate_oxygen_sites.py`

with:

- `SYMPREC = 2.0E-3`
- `ANGLE_TOLERANCE = 5.0`
- `NEIGHBOR_CUTOFF = 2.7 Å`

---

## Current CP2K Environments

Initial local convergence work:

    CP2K 2026.2
    WSL2 / local Linux environment

Production ordered-structure calculations:

    CP2K 2025.2
    ARCHER2

The data-file family/version used by each calculation should be recorded
because local CP2K 2026.2 and ARCHER2 CP2K 2025.2 use differently named
UZH basis/potential data files.

---

## Random Processes

Record random seeds where applicable for:

- AIMD initial velocities;
- stochastic thermostats;
- MACE dataset splitting;
- MACE training;
- structural sampling.

---

## Software Environments

Version important dependencies including:

- CP2K;
- VASP;
- ASE;
- pymatgen;
- NumPy;
- pandas;
- SciPy;
- matplotlib;
- MACE;
- LAMMPS;
- AiiDA.

---

## HPC Metadata

Record where appropriate:

- machine;
- partition/queue;
- nodes;
- CPU cores;
- GPUs;
- memory;
- walltime;
- loaded modules/environment;
- scheduler;
- job ID.

Job IDs should not be embedded in permanent structure names.

---

## Git

Git should track:

- source code;
- workflow definitions;
- templates;
- documentation;
- metadata;
- reference structures;
- selected relaxed structures;
- selected small results;
- analysis scripts.

Git should not serve as bulk simulation storage.

---

## Large Data

Keep large files on appropriate HPC or research storage.

Examples:

- AIMD trajectories;
- CP2K `*.kp` wavefunction restart files;
- wavefunction files;
- restart histories;
- large DFT outputs;
- MACE datasets;
- intermediate checkpoints;
- LAMMPS trajectories.

Curated datasets may later be archived separately with persistent
identifiers.

---

## AiiDA

AiiDA should progressively provide:

- calculation provenance;
- parent-child relationships;
- workflow automation;
- metadata persistence;
- high-throughput defect calculations.

AiiDA should complement Git rather than replace it.

---

## Reproducing the Current Crystalline Reference

The crystalline reference selection should be reproducible from:

    COD 1521670
       +
    generate_igzo_orderings.py
       +
    four ordered structure files
       +
    CP2K convergence parameters
       +
    ARCHER2 geometry-optimisation inputs
       +
    tight EPS_SCF = 1e-7 single points
       +
    relaxed-structure analysis scripts
       +
    docs/results-log.md

---

## Reproducing a Future Result

A significant result should ideally be reproducible from:

    structure ID
       +
    provenance
       +
    workflow version
       +
    computational parameters
       +
    software version
       +
    analysis code
       +
    dataset/model version
