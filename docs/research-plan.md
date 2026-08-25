# Research Plan

## Project

**Defect Chemistry and Structural Disorder in IGZO**

## Core Research Question

How does local structural disorder influence oxygen-vacancy formation
and electronic structure in crystalline and amorphous indium gallium
zinc oxide (IGZO)?

## Motivation

IGZO is a technologically relevant oxide semiconductor used in
transparent electronics and display technologies.

Its amorphous form is particularly interesting because useful electronic
properties can persist despite substantial structural disorder.

Defects, especially oxygen vacancies, can influence the electronic
properties of oxide semiconductors.

The central aim of this project is to connect the local atomic
environment of IGZO with defect energetics and electronic structure.

The project also extends previous experience with high-throughput
oxygen-vacancy modelling in amorphous oxides.

---

## Phase 1 — Literature and Structural Reference

Current status:

- [x] Identify a primary experimental crystalline reference.
- [x] Generate explicit ordered Ga/Zn models.
- [x] Validate four symmetry-distinct ordered structures.
- [x] Select a primary crystalline computational reference.
- [ ] Complete the broader crystalline/Ga–Zn-ordering literature review.
- [ ] Review experimental amorphous IGZO density and coordination.
- [ ] Complete the oxygen-vacancy literature review.

Selected computational reference:

    igzo_crystal_ordered_003_relaxed

Secondary low-energy ordering:

    igzo_crystal_ordered_001_relaxed

---

## Phase 2 — Crystalline IGZO

CP2K currently provides the validated crystalline first-principles
workflow.

Completed:

- [x] CP2K convergence testing.
- [x] Geometry optimisation of all four ordered candidates.
- [x] Tight final energy comparison.
- [x] Symmetry/coordination analysis of the two lowest-energy orderings.
- [x] Bond-distribution analysis.
- [x] Polyhedral-distortion analysis.

Next:

- [ ] Density of states.
- [ ] Projected density of states.
- [ ] Band structure where appropriate.
- [ ] Band-edge orbital character.
- [ ] Charge-density analysis where useful.
- [ ] Effective-mass analysis where justified.

VASP is retained as a complementary future cross-check rather than the
sole crystalline reference route.

---

## Phase 3 — Crystalline Oxygen Vacancies

Systematically investigate symmetry-inequivalent oxygen sites in relaxed
`ordered_003`.

For each selected site:

- generate the oxygen-vacancy structure;
- record site symmetry and multiplicity;
- construct an appropriate defect supercell;
- validate supercell size and k-point sampling;
- relax the defective structure;
- calculate vacancy formation energy;
- investigate relevant charge states;
- analyse local structural relaxation;
- analyse DOS/PDOS and defect states;
- record the local chemical environment.

A key objective is to determine whether vacancy energetics correlate
with local In/Ga/Zn coordination.

Selected defects may later be repeated in `ordered_001` to test
sensitivity to cation ordering.

---

## Phase 4 — Amorphous IGZO

Generate independent amorphous configurations using a validated
melt-quench protocol.

Initial approach:

1. construct a representative stoichiometric, approximately isotropic
   cell;
2. establish/validate target density;
3. equilibrate at low temperature where appropriate;
4. heat to a liquid state;
5. equilibrate in the liquid regime;
6. quench to the target temperature;
7. relax the resulting structure;
8. repeat for multiple independent configurations.

Structural analysis:

- density;
- radial distribution functions;
- coordination-number distributions;
- bond-angle distributions;
- In–O environments;
- Ga–O environments;
- Zn–O environments;
- oxygen coordination;
- local polyhedra;
- ring statistics where meaningful;
- local structural descriptors.

---

## Phase 5 — Defects in Amorphous IGZO

Select representative oxygen sites across multiple amorphous structures.

Calculate:

- vacancy formation energies;
- local structural relaxation;
- relevant charge states;
- electronic structure of representative defects.

The objective is to obtain a **distribution of defect properties**,
rather than a single value.

---

## Phase 6 — Machine-Learning Potential

Generate a DFT dataset containing diverse crystalline, liquid,
amorphous and defect configurations.

Train a MACE potential and assess:

- energy errors;
- force errors;
- stress errors where relevant;
- structural-property reproduction;
- stability during MD;
- transferability across structural environments.

---

## Phase 7 — Large-Scale Sampling

If validated, use MACE through LAMMPS or an appropriate supported
workflow to sample larger systems and longer timescales.

Potential analyses include:

- local environment distributions;
- oxygen coordination;
- structural motifs;
- vacancy precursor environments;
- temperature dependence;
- composition dependence.

---

## Phase 8 — Scientific Interpretation

Connect:

```text
Local chemical environment
        ↓
Structural disorder
        ↓
Defect formation energetics
        ↓
Defect electronic structure
        ↓
Potential influence on semiconductor behaviour
```
