# Validation Strategy

Each stage of the IGZO workflow requires validation before results are
used for subsequent production calculations.

---

## 1. Reference CIF

Validate:

- composition
- lattice parameters
- site occupancies
- atomic coordinates
- symmetry information
- bibliographic provenance

Current reference:

    COD 1521670

The original CIF should remain unmodified.

---

## 2. Ordered Crystalline Models

Each generated model should satisfy:

- In3Ga3Zn3O12 composition
- 21 atoms in the current conventional cell
- 3 Ga atoms
- 3 Zn atoms
- no partial occupancies
- correct periodic lattice
- no overlapping atoms
- physically sensible distances

Symmetry-equivalent configurations should not be retained unnecessarily.

---

## 3. Ordered-Model DFT Screening

Compare:

- total energy
- energy per formula unit
- relative energy
- lattice constants
- volume
- forces
- coordination environments
- symmetry after relaxation

The final reference model must not be selected from its model number.

---

## 4. CP2K Convergence

Systematically assess:

- basis-set quality
- pseudopotentials
- CUTOFF
- REL_CUTOFF
- SCF settings
- k-point sampling

Possible convergence quantities:

- total energy per formula unit
- relative ordering energies
- forces
- lattice parameters

---

## 5. VASP Convergence

When available, assess:

- PAW datasets
- ENCUT
- k-points
- EDIFF
- ionic convergence
- smearing
- spin treatment where relevant

Selected results should be cross-checked with CP2K where appropriate.

---

## 6. Oxygen Vacancies

Check:

- correct oxygen removal
- atom count
- site identity
- charge state
- convergence
- structural relaxation
- local coordination
- electronic behaviour

The defect formation-energy methodology must be explicitly documented.

---

## 7. Amorphous Structures

A completed melt-quench trajectory is not sufficient validation.

Analyse:

### Density

Compare with experiment/literature where possible.

### RDFs

Calculate total and partial RDFs, including:

- In–O
- Ga–O
- Zn–O
- O–O

### Coordination

Calculate distributions for:

- In
- Ga
- Zn
- O

### Additional descriptors

- bond lengths
- bond angles
- local polyhedra
- ring statistics where useful

### Ensemble validation

Compare multiple independent structures.

---

## 8. MACE

Validate numerically using:

- energy MAE/RMSE
- force MAE/RMSE
- stress errors where relevant

Validate physically using:

- structures
- energetic ordering
- RDFs
- coordination
- geometry optimisation
- short MD
- temperature stability
- extrapolation tests

---

## 9. LAMMPS

Before production:

1. reproduce small-system behaviour;
2. verify MACE integration;
3. test temperature/pressure control;
4. check energy stability;
5. inspect structures for unphysical behaviour;
6. compare structural observables with reference calculations.

---

## Scientific Validation

Final conclusions should not depend solely on:

- one amorphous structure
- one Ga/Zn ordering
- one defect site
- one ML model
- one simulation trajectory

Statistical and first-principles validation should be used wherever
scientifically appropriate.