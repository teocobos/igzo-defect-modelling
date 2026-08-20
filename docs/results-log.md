# Results Log

This document records significant project observations, computational
results and methodological decisions.

Planned work should be recorded in the roadmap rather than presented as
a result.

---

# Crystalline Reference Structure

## COD 1521670

**Status:** Reference structure identified and obtained.

**Material:** InGaZnO4

**Source:** Crystallography Open Database

**COD ID:** 1521670

**Reference:** Nespolo, M.; Sato, A.; Osawa, T.; Ohashi, H.
Crystal Research and Technology 35 (2000), 151–165.

---

## Reference Cell

The CIF contains approximately:

    a = 3.299 Å
    b = 3.299 Å
    c = 26.101 Å

    alpha = 90°
    beta  = 90°
    gamma = 120°

---

## Mixed Ga/Zn Site

Inspection of the crystallographic structure shows that Ga and Zn share
the same crystallographic site with approximately:

    Ga occupancy = 0.5
    Zn occupancy = 0.5

The CIF therefore represents an experimental average structure rather
than an explicit ordered atomistic model.

---

## Conventional Cell

Expansion of the crystallographic structure produces six mixed Ga/Zn
positions.

Stoichiometric InGaZnO4 requires:

    3 Ga
    3 Zn

across these positions.

The number of possible raw assignments is:

    C(6,3) = 20

Initial symmetry analysis reduces these to:

    4 symmetry-distinct ordered configurations

---

## Methodological Decision

The original COD CIF will be retained unchanged as the experimental
reference.

Ordered Ga/Zn configurations will be generated programmatically.

No ordered configuration has yet been selected as the final crystalline
reference.

Selection will be based on first-principles relaxation and relative
energetics.

---

## Ordered Crystalline Structure Validation

**Status:** Completed.

Four symmetry-distinct ordered InGaZnO4 structures were generated from
the mixed Ga/Zn crystallographic model derived from COD 1521670.

### Validation results

| Model | Atoms | Composition | Ordered | Minimum distance (Å) | Space group |
|---|---:|---|---|---:|---|
| `igzo_crystal_ordered_001` | 21 | In3Ga3Zn3O12 | Yes | 1.930 | P3m1 (156) |
| `igzo_crystal_ordered_002` | 21 | In3Ga3Zn3O12 | Yes | 1.930 | P3m1 (156) |
| `igzo_crystal_ordered_003` | 21 | In3Ga3Zn3O12 | Yes | 1.930 | R3m (160) |
| `igzo_crystal_ordered_004` | 21 | In3Ga3Zn3O12 | Yes | 1.930 | P3m1 (156) |

Validation confirmed:

- correct 21-atom conventional-cell composition
- 3 In, 3 Ga, 3 Zn and 12 O atoms
- complete site occupancies
- consistent lattice parameters
- no unphysical short contacts
- four structurally distinct ordered configurations

pymatgen reported that fractional coordinates were rounded to ideal
crystallographic values during CIF parsing to avoid finite-precision
issues. No structural validation failures resulted from this operation.

### Symmetry observation

Three ordered configurations have P3m1 symmetry, while
`igzo_crystal_ordered_003` retains R3m symmetry.

The higher symmetry of model 003 does not imply that it is energetically
preferred. All four models will be compared using first-principles
geometry optimisation and relative energies.

No final crystalline computational reference has yet been selected.

## Current Computational Status

- [x] Experimental CIF obtained
- [x] Crystallographic provenance recorded
- [x] Mixed Ga/Zn site identified
- [x] Ordering problem defined
- [x] Four symmetry-distinct configuration classes identified
- [x] Ordered structure files generated
- [x] Structures independently validated
- [ ] CP2K convergence completed
- [ ] Ordered structures relaxed
- [ ] Relative energies calculated
- [ ] Crystalline reference selected

---

# Scientific Results

No production DFT, defect, AIMD, MACE or LAMMPS results have yet been
recorded.

Future validated results should be added chronologically below this
section.