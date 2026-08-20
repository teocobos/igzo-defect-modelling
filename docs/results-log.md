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

## Current Computational Status

- [x] Experimental CIF obtained
- [x] Crystallographic provenance recorded
- [x] Mixed Ga/Zn site identified
- [x] Ordering problem defined
- [x] Four symmetry-distinct configuration classes identified
- [ ] Ordered structure files generated
- [ ] Structures independently validated
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