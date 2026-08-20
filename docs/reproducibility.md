# Reproducibility

Reproducibility and computational provenance are core requirements of
the IGZO defect-modelling project.

---

## Provenance Chain

    COD 1521670
          ↓
    experimental CIF
          ↓
    ordering script
          ↓
    ordered crystalline model
          ↓
    DFT relaxation
          ↓
    crystalline reference
       ┌──┴───────────────┐
       ↓                  ↓
    defects             AIMD
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
                  defect calculations
                          ↓
                     analysis

---

## Reference Structures

External structures should:

- remain unmodified
- retain database identifiers
- retain publication provenance
- remain separate from derived structures

Current reference:

    COD 1521670

---

## Generated Structures

Derived structures should record:

- structure ID
- parent structure
- generation method
- generation script
- software/version
- ordering identifier where appropriate
- composition

Programmatic generation is preferred to manual editing.

---

## Calculations

Production calculations should record:

- calculation ID
- structure ID
- software
- software version
- computational parameters
- basis sets / pseudopotentials
- parent calculation
- HPC environment
- status

---

## Random Processes

Record random seeds where applicable for:

- AIMD initial velocities
- stochastic thermostats
- MACE dataset splitting
- MACE training
- structural sampling

---

## Software Environments

Version important dependencies including:

- CP2K
- VASP
- ASE
- pymatgen
- NumPy
- pandas
- SciPy
- matplotlib
- MACE
- LAMMPS
- AiiDA

---

## HPC Metadata

Record where appropriate:

- machine
- partition/queue
- nodes
- CPU cores
- GPUs
- memory
- walltime
- modules/environment
- scheduler
- job ID

Job IDs should not be embedded in permanent structure names.

---

## Git

Git should track:

- source code
- workflow definitions
- templates
- documentation
- metadata
- reference structures
- selected results
- analysis scripts

Git should not serve as bulk simulation storage.

---

## Large Data

Keep large files on appropriate HPC or research storage.

Examples:

- AIMD trajectories
- wavefunction files
- restart files
- large DFT outputs
- MACE datasets
- intermediate checkpoints
- LAMMPS trajectories

Curated datasets may later be archived separately with persistent
identifiers.

---

## AiiDA

AiiDA should progressively provide:

- calculation provenance
- parent-child relationships
- workflow automation
- metadata persistence
- high-throughput defect calculations

AiiDA should complement Git rather than replace it.

---

## Reproducing a Result

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