# Dataset Plan

This document defines the initial data-generation strategy for the
IGZO defect-modelling project.

Dataset sizes are planning targets rather than fixed requirements.

---

## Crystalline Reference Data

### Experimental reference

Current reference:

    COD 1521670

The original CIF is retained unchanged.

### Ordered crystalline models

The experimental mixed Ga/Zn structure generates:

    20 raw Ga/Zn assignments

which are reduced to:

    4 symmetry-distinct candidate structures

These structures form the initial crystalline configuration set.

---

## Crystalline DFT Dataset

Initial data should include:

- four ordered structures before relaxation
- four relaxed structures
- total energies
- forces
- stresses where appropriate
- lattice parameters
- relative energies

Additional distorted crystalline structures may later be included for
machine-learning training.

---

## Amorphous Structures

Initial target:

    approximately 10–20 independent structures

Generation method:

    CP2K AIMD melt-quench

The final number should depend on structural convergence and diversity.

---

## Initial MACE Dataset

Planning target:

    approximately 1,000–5,000 configurations

Potential configuration classes:

- relaxed crystalline
- strained crystalline
- thermally distorted crystalline
- melt
- liquid
- quench
- amorphous
- defect-containing structures where required

Dataset diversity is more important than raw snapshot count.

---

## Dataset Splitting

Initial target:

- training: ~70%
- validation: ~15%
- test: ~15%

Highly correlated frames from the same trajectory should not be randomly
distributed across all three subsets where this would cause leakage.

Independent trajectories should be used where practical.

---

## MACE Validation Dataset

Initial planning target:

    approximately 200–500 independent configurations

Validation configurations should sample environments distinct from the
training configurations.

---

## Large-Scale Sampling

MACE/LAMMPS production simulations may eventually generate:

    hundreds to thousands of representative configurations

Large trajectory files should remain on HPC or research-data storage.

---

## Oxygen-Vacancy Dataset

The amorphous vacancy dataset should contain a statistically meaningful
range of local oxygen environments.

For each vacancy, record where possible:

- parent structure
- oxygen identifier
- neighbouring cations
- coordination
- local bond lengths
- defect charge
- relaxation result
- formation energy
- electronic properties

---

## Data Storage

### GitHub

Store:

- generation scripts
- metadata
- small reference structures
- input templates
- analysis code
- small curated examples

### HPC / Research Storage

Store:

- raw DFT calculations
- AIMD trajectories
- large ML datasets
- production LAMMPS trajectories
- restart files
- intermediate data

### Data Repository

Potential future public releases:

- curated datasets
- selected structures
- trained models
- supporting publication data

---

## Dataset Versioning

Use explicit versions such as:

    igzo_mace_training_v01
    igzo_mace_training_v02

A new version should be created when the composition or scope of a
dataset changes substantially.