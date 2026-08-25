# Validation Strategy

Each stage of the IGZO workflow requires validation before results are
used for subsequent production calculations.

---

## 1. Reference CIF

Validate:

- composition;
- lattice parameters;
- site occupancies;
- atomic coordinates;
- symmetry information;
- bibliographic provenance.

Current reference:

    COD 1521670

**Status:** PASSED.

The original CIF remains unmodified.

---

## 2. Ordered Crystalline Models

Each generated model should satisfy:

- In3Ga3Zn3O12 composition;
- 21 atoms in the current conventional cell;
- 3 Ga atoms;
- 3 Zn atoms;
- no partial occupancies;
- correct periodic lattice;
- no overlapping atoms;
- physically sensible distances.

Symmetry-equivalent configurations should not be retained unnecessarily.

**Status:** PASSED for the four retained ordered candidates.

---

## 3. CP2K Crystalline Convergence

Validated for the current 21-atom crystalline ordering study:

- [x] basis-set sensitivity assessed;
- [x] CUTOFF convergence assessed;
- [x] REL_CUTOFF convergence assessed;
- [x] k-point convergence assessed;
- [x] SCF strategy tested;
- [x] final tight single-point threshold established.

Current parameters:

- TZV2P-MOLOPT-PBE-GTH;
- matching GTH-PBE pseudopotentials;
- CUTOFF = 700 Ry;
- REL_CUTOFF = 60 Ry;
- 6×6×1 Monkhorst–Pack mesh;
- final single-point EPS_SCF = 1e-7.

**Status:** PASSED for the current crystalline reference workflow.

These parameters must not automatically be transferred to larger defect
or amorphous cells without appropriate validation.

---

## 4. Crystalline Reference Structure Validation

Four candidate ordered InGaZnO4 structures were independently geometry
optimised on ARCHER2 using a consistent CP2K workflow.

Validation criteria:

- [x] geometry optimisation completed for all four structures;
- [x] identical physical/numerical settings used across the comparison;
- [x] final energies recalculated using EPS_SCF = 1e-7;
- [x] energetic ordering stable with respect to tighter SCF convergence;
- [x] relaxed structures checked for crystallographic symmetry;
- [x] coordination numbers validated;
- [x] bond-length distributions analysed;
- [x] local polyhedral distortions analysed.

Final energetic ordering:

    ordered_003 < ordered_001 << ordered_002 < ordered_004

`ordered_003` and `ordered_001` differ by approximately 2.07 meV/f.u.
`ordered_002` and `ordered_004` lie more than 0.7 eV/f.u. above the
minimum.

Primary crystalline reference:

    igzo_crystal_ordered_003_relaxed

Secondary low-energy ordering:

    igzo_crystal_ordered_001_relaxed

**Status:** PASSED.

---

## 5. Crystalline Electronic Structure

Before treating electronic-structure results as validated:

- converge/confirm settings appropriate to DOS/PDOS/band calculations;
- identify band-edge orbital character;
- compare with available literature;
- cross-check selected results with VASP where appropriate.

**Status:** PENDING.

---

## 6. Crystalline Oxygen Vacancies

For generated vacancy structures, check:

- correct oxygen removal;
- atom count;
- site identity;
- symmetry class and multiplicity;
- charge state;
- supercell dimensions;
- defect–defect separation;
- k-point convergence for the chosen supercell;
- SCF/geometry convergence;
- structural relaxation;
- local coordination;
- electronic behaviour.

The defect formation-energy methodology and oxygen chemical potential
must be explicitly documented.

**Status:** PENDING.

---

## 7. Amorphous Structures

A completed melt-quench trajectory is not sufficient validation.

### Density

Compare with experiment/literature where possible.

### RDFs

Calculate total and partial RDFs, including:

- In–O;
- Ga–O;
- Zn–O;
- O–O.

### Coordination

Calculate distributions for:

- In;
- Ga;
- Zn;
- O.

### Additional descriptors

- bond lengths;
- bond angles;
- local polyhedra;
- ring statistics where useful.

### Ensemble validation

Compare multiple independent structures and assess system-size effects.

**Status:** PENDING.

---

## 8. MACE

Validate numerically using:

- energy MAE/RMSE;
- force MAE/RMSE;
- stress errors where relevant.

Validate physically using:

- structures;
- energetic ordering;
- RDFs;
- coordination;
- geometry optimisation;
- short MD;
- temperature stability;
- extrapolation tests.

**Status:** PENDING.

---

## 9. LAMMPS

Before production:

1. reproduce small-system behaviour;
2. verify MACE integration;
3. test temperature/pressure control;
4. check energy stability;
5. inspect structures for unphysical behaviour;
6. compare structural observables with reference calculations.

**Status:** PENDING.

---

## Scientific Validation Principle

Final conclusions should not depend solely on:

- one amorphous structure;
- one Ga/Zn ordering;
- one defect site;
- one ML model;
- one simulation trajectory.

Statistical and first-principles validation should be used wherever
scientifically appropriate.
