
---

# 3. `docs/research-plan.md`

```markdown
# Research Plan

## Project

**Defect Chemistry and Structural Disorder in IGZO**

## Core Research Question

How does local structural disorder influence oxygen-vacancy formation and electronic structure in crystalline and amorphous indium gallium zinc oxide (IGZO)?

## Motivation

IGZO is a technologically relevant oxide semiconductor used in transparent electronics and display technologies.

Its amorphous form is particularly interesting because useful electronic properties can persist despite substantial structural disorder.

Defects, especially oxygen vacancies, can influence the electronic properties of oxide semiconductors.

The central aim of this project is to connect the local atomic environment of IGZO with defect energetics and electronic structure.

The project also provides a natural extension of previous work on high-throughput oxygen-vacancy modelling in amorphous oxides.

---

## Phase 1 — Literature and Structural Reference

- Identify experimentally reported IGZO compositions and structures.
- Determine an appropriate crystalline reference structure.
- Establish realistic stoichiometry and supercell sizes.
- Review experimental information on amorphous IGZO density, coordination and composition.
- Review reported defect chemistry and oxygen-vacancy interpretations.

---

## Phase 2 — Crystalline IGZO

Use VASP to establish a high-quality reference.

Planned calculations:

- Structural optimisation.
- Lattice parameters.
- Convergence tests.
- Density of states.
- Projected density of states.
- Band structure where appropriate.
- Charge-density analysis.
- Effective-mass analysis where justified.

---

## Phase 3 — Oxygen Vacancies

Systematically investigate inequivalent oxygen sites.

For each selected site:

- Generate the oxygen-vacancy structure.
- Relax the defective structure.
- Calculate vacancy formation energy.
- Investigate relevant charge states.
- Analyse local structural relaxation.
- Analyse DOS/PDOS and defect states.
- Record the local chemical environment.

A key objective is to determine whether vacancy energetics correlate with local In/Ga/Zn coordination.

---

## Phase 4 — Amorphous IGZO

Generate independent amorphous configurations using a validated melt-quench protocol.

Initial approach:

1. Construct a representative stoichiometric model.
2. Equilibrate at low temperature.
3. Heat to a liquid state.
4. Equilibrate in the liquid regime.
5. Quench to the target temperature.
6. Relax the resulting structure.
7. Repeat for multiple independent configurations.

Structural analysis:

- Density.
- Radial distribution functions.
- Coordination-number distributions.
- Bond-angle distributions.
- In–O environments.
- Ga–O environments.
- Zn–O environments.
- Oxygen coordination.
- Ring statistics where meaningful.
- Local structural descriptors.

---

## Phase 5 — Defects in Amorphous IGZO

Select representative oxygen sites across multiple amorphous structures.

Calculate:

- Vacancy formation energies.
- Local structural relaxation.
- Relevant charge states.
- Electronic structure of representative defects.

The objective is to obtain a **distribution of defect properties**, rather than a single value.

---

## Phase 6 — Machine-Learning Potential

Generate a DFT dataset containing diverse crystalline, liquid, amorphous and defect configurations.

Train a MACE potential and assess:

- Energy errors.
- Force errors.
- Stress errors where relevant.
- Structural-property reproduction.
- Stability during MD.
- Transferability across structural environments.

---

## Phase 7 — Large-Scale Sampling

If validated, use MACE through LAMMPS or an appropriate supported workflow to sample larger systems and longer timescales.

Potential analyses include:

- Local environment distributions.
- Oxygen coordination.
- Structural motifs.
- Vacancy precursor environments.
- Temperature dependence.
- Composition dependence.

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