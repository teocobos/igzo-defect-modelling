# Dataset Plan

This document defines the data-generation strategy for the IGZO
defect-modelling project.

Dataset sizes are planning targets rather than fixed requirements.

---

## Crystalline Reference Data

### Experimental reference

Current experimental reference:

    COD 1521670

The original CIF is retained unchanged.

### Ordered crystalline models

The mixed Ga/Zn crystallographic structure generates:

    20 raw Ga/Zn assignments

which are reduced to:

    4 symmetry-distinct ordered candidate structures

The initial crystalline configuration set now contains:

- four unrelaxed ordered structures;
- four successfully relaxed ordered structures;
- final tight single-point total energies for all four structures; and
- detailed structural analysis for the two lowest-energy structures.

Primary crystalline reference:

    igzo_crystal_ordered_003_relaxed

Secondary low-energy ordering:

    igzo_crystal_ordered_001_relaxed

---

## Crystalline DFT Dataset

Completed/current reference data include:

- ordered structures before relaxation;
- relaxed structures;
- geometry-optimisation energies;
- tight final single-point energies;
- relative energies per formula unit;
- structural symmetry;
- coordination numbers;
- bond-length distributions; and
- local polyhedral distortion descriptors.

Additional data to add as the crystalline workflow develops:

- DOS and PDOS;
- band structure where appropriate;
- oxygen-vacancy structures and energetics;
- charged-defect data where appropriate;
- distorted/thermal crystalline configurations for machine-learning
  training.

---

## Crystalline Oxygen-Vacancy Dataset

The first defect dataset will be generated from relaxed
`ordered_003`.

Initial steps:

1. identify symmetry-inequivalent oxygen sites;
2. record site multiplicities;
3. record local In/Ga/Zn coordination;
4. generate one vacancy structure per inequivalent oxygen site;
5. validate defect supercell size and k-point sampling;
6. calculate neutral vacancy relaxations and formation energies;
7. extend to relevant charge states and electronic properties.

For each crystalline vacancy, record where possible:

- parent structure;
- supercell;
- oxygen identifier;
- symmetry class;
- multiplicity;
- neighbouring cations;
- local coordination;
- local bond lengths;
- defect charge;
- relaxation result;
- formation energy;
- electronic properties.

A subset of defects may later be repeated in
`igzo_crystal_ordered_001_relaxed` to test sensitivity to the
near-degenerate cation ordering.

---

## Amorphous Structures

Initial target:

    approximately 10–20 independent structures

Generation method:

    CP2K AIMD melt-quench

The amorphous cell should be designed independently from the elongated
crystalline conventional cell and should be approximately isotropic
where practical.

The final number of structures should depend on structural convergence
and ensemble diversity.

---

## Initial MACE Dataset

Planning target:

    approximately 1,000–5,000 configurations

Potential configuration classes:

- relaxed crystalline;
- strained crystalline;
- thermally distorted crystalline;
- crystalline defect structures;
- melt;
- liquid;
- quench;
- amorphous;
- amorphous defect-containing structures where required.

Dataset diversity is more important than raw snapshot count.

---

## Dataset Splitting

Initial target:

- training: ~70%;
- validation: ~15%;
- test: ~15%.

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

MACE/LAMMPS production simulations may eventually generate hundreds to
thousands of representative configurations.

Large trajectory files should remain on HPC or research-data storage.

---

## Amorphous Oxygen-Vacancy Dataset

The amorphous vacancy dataset should contain a statistically meaningful
range of local oxygen environments.

For each vacancy, record where possible:

- parent amorphous structure;
- oxygen identifier;
- neighbouring cations;
- coordination;
- local bond lengths and angles;
- local structural descriptors;
- defect charge;
- relaxation result;
- formation energy;
- electronic properties.

---

## Data Storage

### GitHub

Store:

- generation scripts;
- metadata;
- small reference/derived structures;
- input templates;
- analysis code;
- small curated results;
- documentation.

### HPC / Research Storage

Store:

- raw production calculations;
- AIMD trajectories;
- wavefunction/restart files;
- large ML datasets;
- production LAMMPS trajectories;
- intermediate data.

### Data Repository

Potential future public releases:

- curated datasets;
- selected structures;
- trained models;
- supporting publication data.

---

## Dataset Versioning

Use explicit versions such as:

    igzo_mace_training_v01
    igzo_mace_training_v02

A new version should be created when the composition or scope of a
dataset changes substantially.
