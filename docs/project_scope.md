# Project Scope

## IGZO Defect Modelling

This project investigates the structural, defect and electronic
properties of indium gallium zinc oxide (IGZO) using first-principles
calculations, atomistic simulation and machine-learning interatomic
potentials.

The initial material of interest is stoichiometric:

**InGaZnO4**

with particular emphasis on its role as a transparent conducting oxide
(TCO) and amorphous oxide semiconductor (AOS).

---

## Scientific Objectives

The project objectives are to:

1. establish a validated crystalline InGaZnO4 reference model;
2. investigate the influence of Ga/Zn ordering in crystalline IGZO;
3. characterise the pristine crystalline electronic structure;
4. investigate oxygen vacancies and their local environments;
5. generate and validate amorphous IGZO structures;
6. determine how structural disorder influences oxygen-vacancy behaviour;
7. develop machine-learning interatomic potentials for IGZO; and
8. use large-scale molecular dynamics to obtain statistically meaningful
   structural and defect distributions.

---

## Crystalline Reference

The primary experimental crystallographic reference is:

**COD 1521670**

derived from:

M. Nespolo, A. Sato, T. Osawa and H. Ohashi,

*Synthesis, crystal structure and charge distribution of InGaZnO4.
X-ray diffraction of 20 kb single crystal and 50 kb twin by reticular
merohedry.*

Crystal Research and Technology 35 (2000), 151–165.

The experimental CIF contains mixed Ga/Zn occupancy and represents an
average crystallographic structure.

Twenty raw Ga/Zn assignments were generated programmatically and reduced
to four symmetry-distinct ordered candidates.

Following converged CP2K geometry optimisation and tight final
single-point calculations, the primary crystalline computational
reference is:

    igzo_crystal_ordered_003_relaxed

This structure retains R3m symmetry.

The near-degenerate P3m1 structure:

    igzo_crystal_ordered_001_relaxed

is retained as a secondary low-energy cation ordering.

---

## Computational Methods

The project uses/plans:

- CP2K — DFT, geometry optimisation and ab initio molecular dynamics;
- VASP — complementary crystalline DFT, electronic structure and defect
  calculations;
- MACE — machine-learning interatomic potentials;
- LAMMPS — large-scale molecular dynamics;
- AiiDA — workflow automation and provenance;
- ASE — structure manipulation and analysis;
- pymatgen — crystallographic analysis and structure generation;
- Python — data processing, statistical analysis and visualisation.

CP2K currently provides the validated first-principles crystalline
workflow. VASP remains a complementary future cross-check.

---

## Initial Defect Scope

The initial defect investigation focuses on:

**oxygen vacancies**

including:

- crystallographically distinct vacancy environments;
- structural relaxation around vacancies;
- vacancy formation energies;
- charge states where appropriate;
- electronic defect states;
- local coordination;
- structural descriptors;
- distributions of defect properties in amorphous IGZO.

The crystalline defect workflow begins from relaxed
`ordered_003` and will use symmetry reduction plus explicit supercell
convergence.

---

## Amorphous IGZO

Amorphous structures will initially be generated using CP2K AIMD
melt-quench simulations.

The starting cell will be selected to be approximately isotropic where
practical rather than directly inheriting the elongated shape of the
crystalline conventional cell.

Multiple independent structures will be generated to avoid conclusions
being dependent on a single amorphous configuration.

Structural validation will include:

- density;
- radial distribution functions;
- coordination statistics;
- bond-length distributions;
- bond-angle distributions;
- local polyhedra;
- ring statistics where appropriate.

---

## Machine-Learning Scope

DFT configurations will be used to construct datasets for MACE.

The resulting potential will only be used for production molecular
dynamics after validation against independent first-principles data.

MACE/LAMMPS will then enable substantially larger system sizes and
longer trajectories than direct AIMD.

---

## Initial Project Boundary

The first major scientific objective is:

> Establish how structural disorder modifies oxygen-vacancy environments,
> energetics and electronic properties in IGZO.

The initial project does not require investigation of every possible
defect species.

Potential future extensions include:

- oxygen interstitials;
- cation vacancies;
- cation antisites;
- hydrogen-related defects;
- different IGZO compositions;
- surfaces;
- interfaces;
- extended defects.

These should only be introduced once the initial oxygen-vacancy workflow
has been validated.
