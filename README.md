# Defect Chemistry and Structural Disorder in IGZO

Computational investigation of indium gallium zinc oxide (IGZO), with a focus on oxygen vacancies, structural disorder, and their influence on electronic properties.

## Research Question

**How does local structural disorder influence oxygen-vacancy formation and electronic structure in crystalline and amorphous IGZO?**

## Objectives

1. Establish a reproducible computational reference for crystalline IGZO.
2. Investigate oxygen-vacancy formation energies and charge states.
3. Determine how local In/Ga/Zn coordination affects vacancy energetics and electronic structure.
4. Generate and characterise amorphous IGZO structures.
5. Compare defect chemistry between crystalline and amorphous IGZO.
6. Develop and validate a MACE interatomic potential for larger-scale atomistic sampling.
7. Build reproducible workflows using AiiDA, Python, ASE and pymatgen.

## Computational Methods

- **VASP** — crystalline reference calculations and electronic structure.
- **CP2K** — DFT molecular dynamics, amorphisation and amorphous-structure calculations.
- **LAMMPS** — large-scale molecular dynamics using validated potentials.
- **MACE** — machine-learning interatomic potential development.
- **AiiDA** — workflow automation, provenance and reproducibility.
- **ASE / pymatgen** — structure generation and analysis.
- **Python** — data processing, statistics and visualisation.

## Project Status

🟡 **Research project initiated**

### Completed

- [x] Define initial research direction
- [x] Establish repository structure

### In Progress

- [ ] Literature review
- [ ] Identify and validate crystalline IGZO structure
- [ ] DFT convergence testing
- [ ] Pristine crystalline IGZO calculations

### Planned

- [ ] Oxygen-vacancy calculations
- [ ] Amorphous IGZO generation
- [ ] Amorphous structural analysis
- [ ] MACE dataset generation
- [ ] MACE training and validation
- [ ] Large-scale atomistic sampling
- [ ] Defect statistics

## Repository Structure

```text
igzo-defect-modelling/
├── docs/
├── structures/
├── calculations/
├── mace/
├── notebooks/
├── src/
├── reports/
├── workflows/
├── README.md
├── LICENSE
└── requirements.txt