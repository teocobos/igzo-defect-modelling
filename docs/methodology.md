# Methodology

This document describes the planned computational methodology for the
IGZO defect-modelling project.

The methodology will evolve as convergence tests and validation studies
are completed.

---

## 1. Experimental Crystalline Reference

The initial crystalline reference is stoichiometric InGaZnO4.

The primary crystallographic structure is obtained from:

**Crystallography Open Database — COD 1521670**

The original CIF is retained unchanged under:

    structures/crystalline/reference/

The experimental structure contains mixed Ga/Zn occupancy and therefore
cannot be used directly as a conventional ordered atomistic DFT model.

---

## 2. Ga/Zn Ordering

The mixed Ga/Zn crystallographic sites are converted into explicit
ordered configurations.

For the current conventional cell, six mixed positions must be occupied
by:

    3 Ga
    3 Zn

giving:

    C(6,3) = 20

raw assignments.

Symmetry-equivalent configurations are removed before first-principles
screening.

The initial workflow produces four symmetry-distinct ordered candidate
structures.

Structure generation is performed programmatically using:

    scripts/structure_generation/generate_igzo_orderings.py

Manual editing of the experimental CIF should be avoided.

---

## 3. Crystalline Model Selection

The ordered structures will be geometry-optimised using a consistent
first-principles methodology.

For each configuration, quantities including the following will be
recorded:

- total energy
- energy per formula unit
- relative energy
- relaxed lattice parameters
- atomic forces
- structural symmetry
- coordination environments

The preferred crystalline reference will be selected only after this
comparison.

---

## 4. CP2K

CP2K provides the initial first-principles workflow.

### Initial applications

- convergence testing
- crystalline geometry optimisation
- comparison of Ga/Zn ordered structures
- ab initio molecular dynamics
- amorphisation
- generation of reference configurations for machine learning

### Convergence

Parameters requiring systematic evaluation include:

- basis-set quality
- pseudopotential selection
- CUTOFF
- REL_CUTOFF
- SCF convergence
- k-point sampling
- geometry-optimisation tolerances

Production parameters should not be selected solely because they are
commonly used values.

---

## 5. VASP

VASP will provide a complementary first-principles workflow once the
required computational environment is available.

Planned applications include:

- crystalline relaxation
- convergence testing
- band structure
- density of states
- projected density of states
- oxygen-vacancy calculations
- defect formation energies
- charged defects where appropriate

Cross-code comparisons between CP2K and VASP should use equivalent
physical approximations wherever practical.

---

## 6. Oxygen Vacancies

Oxygen vacancies will initially be investigated in the selected
crystalline reference structure.

The workflow will include:

    pristine structure
            ↓
    identify oxygen sites
            ↓
    generate vacancy structures
            ↓
    geometry optimisation
            ↓
    defect energetics
            ↓
    electronic structure
            ↓
    local structural analysis

Symmetry should be used to avoid unnecessary calculations for equivalent
oxygen sites.

For amorphous structures, oxygen sites will generally be locally
inequivalent and statistical sampling will therefore be required.

---

## 7. CP2K Amor­phisation

Amorphous IGZO will initially be generated using first-principles
molecular dynamics.

The intended workflow is:

    initial structure
          ↓
    equilibration
          ↓
       heating
          ↓
        melt
          ↓
       quench
          ↓
    low-temperature equilibration
          ↓
    geometry optimisation
          ↓
    amorphous IGZO

The following parameters will be established and documented:

- initial cell
- density
- timestep
- ensemble
- thermostat
- melt temperature
- melt duration
- quench rate
- final temperature
- equilibration duration

Multiple independent trajectories should be generated.

---

## 8. Amorphous Structure Validation

Generated structures will be evaluated using structural descriptors
including:

- density
- radial distribution functions
- partial radial distribution functions
- coordination numbers
- bond lengths
- bond angles
- local polyhedra
- ring statistics where appropriate

Results should be compared with available experimental and computational
literature.

---

## 9. MACE Dataset Generation

First-principles configurations will be selected to represent the
configuration space required by the potential.

Potential configurations include:

- crystalline structures
- strained structures
- thermally distorted structures
- melt configurations
- liquid configurations
- quench configurations
- amorphous structures
- defect environments where required

Configurations should contain reference:

- energies
- forces
- stresses where appropriate

Highly correlated consecutive AIMD frames should not dominate the
dataset.

---

## 10. MACE Training and Validation

Datasets will be divided into training, validation and independent test
sets.

Validation should consider:

- energy MAE/RMSE
- force MAE/RMSE
- stress errors where applicable
- structural properties
- energetic ordering
- molecular-dynamics stability
- behaviour on unseen configurations

Numerical test-set accuracy alone is insufficient to establish that the
potential is suitable for production simulation.

---

## 11. LAMMPS Sampling

Following validation, MACE will be used with LAMMPS for larger-scale
molecular dynamics.

This will enable:

- larger simulation cells
- longer trajectories
- independent melt-quench simulations
- structural ensemble generation
- statistical sampling of local environments

Representative configurations may subsequently be returned to
first-principles calculations for validation.

---

## 12. Statistical Defect Sampling

The large amorphous ensemble will provide oxygen environments spanning
different:

- coordination numbers
- cation neighbours
- bond lengths
- bond angles
- local densities
- structural motifs

Representative oxygen sites will be selected for vacancy calculations.

The objective is to obtain distributions of defect properties rather
than relying on a single amorphous vacancy configuration.

---

## 13. Analysis

Analysis will primarily use Python together with:

- NumPy
- pandas
- SciPy
- ASE
- pymatgen
- matplotlib

All important analysis should be reproducible from scripts wherever
practical.

---

## Overall Methodology

    COD 1521670
          ↓
    experimental average structure
          ↓
    Ga/Zn ordering
          ↓
    ordered crystalline candidates
          ↓
    first-principles comparison
          ↓
    crystalline reference
       ┌──┴──────────────┐
       ↓                 ↓
    defects          CP2K AIMD
                         ↓
                    amorphous IGZO
                         ↓
                    DFT dataset
                         ↓
                       MACE
                         ↓
                     LAMMPS
                         ↓
               large-scale ensemble
                         ↓
                 vacancy statistics
                         ↓
              structural/electronic
                    conclusions