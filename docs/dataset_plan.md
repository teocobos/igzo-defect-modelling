# IGZO Dataset Plan

This document defines the initial dataset strategy for the IGZO defect
modelling project.

Dataset sizes are planning targets and should be revised according to
configuration-space coverage, convergence and scientific requirements.

---

## 1. Crystalline Structures

### Initial target

1–3 candidate crystalline IGZO structures.

### Purpose

- Structural benchmarking
- Selection of the reference crystalline model
- Comparison with literature

### Required information

- Composition
- Structure type
- Lattice parameters
- Atomic coordinates
- Density
- Source/provenance
- Relaxation status

---

## 2. Crystalline Oxygen Vacancies

### Initial strategy

Investigate all relevant inequivalent oxygen sites in the selected
crystalline model.

### Required information

- Parent structure
- Oxygen site
- Vacancy charge state
- Supercell
- Relaxed geometry
- Formation energy
- Electronic structure

---

## 3. Amorphous IGZO

### Initial target

Approximately 10–20 independent amorphous structures.

### Generation

CP2K DFT/AIMD melt-quench simulations.

### Diversity requirements

The ensemble should represent variation in:

- Local coordination
- Bond lengths
- Bond angles
- Density
- Structural motifs

Multiple independent trajectories should be preferred over repeatedly
sampling a single trajectory.

---

## 4. AIMD / MACE Dataset

### Initial target

Approximately 1,000–5,000 configurations.

### Sources

- Melt configurations
- Quench configurations
- Room-temperature configurations
- Thermally distorted configurations
- Structurally diverse amorphous configurations
- Defect configurations where required

### Properties

Where possible, configurations should contain:

- Total energy
- Atomic forces
- Stress tensor

---

## 5. Dataset Splitting

Initial target:

- Training: ~70%
- Validation: ~15%
- Test: ~15%

Splitting should avoid placing highly correlated trajectory frames in
different subsets where this would cause data leakage.

The test set should represent configurations that are genuinely
independent from the training data.

---

## 6. MACE Validation Dataset

### Initial target

Approximately 200–500 independent configurations.

The validation set should include:

- Different amorphous structures
- Different local environments
- Different temperatures
- Distorted configurations
- Defect environments where relevant

Validation should assess both numerical errors and physical behaviour.

---

## 7. Large-Scale LAMMPS Dataset

### Initial target

Hundreds to thousands of sampled configurations, depending on system
size and computational cost.

### Purpose

- Structural statistics
- Local environment statistics
- Amorphous ensemble generation
- Identification of representative structures
- Oxygen-vacancy sampling

---

## 8. Oxygen Vacancy Dataset

The final defect dataset should contain a statistically meaningful
sample of vacancy environments.

For each selected vacancy:

- Parent structure
- Vacancy site
- Local coordination
- Local structural descriptors
- Relaxed structure
- Formation energy
- Electronic properties where calculated

The objective is to determine distributions and correlations rather
than relying on a single representative vacancy.

---

## 9. Data Storage

Large datasets should not normally be stored directly in the GitHub
repository.

### GitHub

Store:

- Dataset-generation scripts
- Dataset schemas
- Metadata
- Small example datasets
- Data-processing scripts
- Documentation

### HPC / Research Storage

Store:

- Raw AIMD trajectories
- Large DFT datasets
- Large MACE datasets
- LAMMPS trajectories
- Intermediate calculation outputs

### Public Data Repository

Potentially release:

- Curated datasets
- Final structures
- Selected reference calculations
- Trained models

A DOI-based archive should be considered when the dataset reaches a
stable release.

---

## 10. Dataset Versioning

Datasets should use explicit versions:

    igzo_mace_training_v01
    igzo_mace_training_v02

A new version should be created when the dataset composition changes
substantially.

The metadata should record the relationship between dataset versions.