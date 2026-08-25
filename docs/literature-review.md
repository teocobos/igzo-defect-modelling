# Literature Review

This document records literature relevant to the IGZO defect-modelling
project.

It should be expanded continuously as the project develops.

---

## 1. Crystalline InGaZnO4

### Nespolo et al. (2000)

M. Nespolo, A. Sato, T. Osawa and H. Ohashi.

*Synthesis, crystal structure and charge distribution of InGaZnO4.
X-ray diffraction of 20 kb single crystal and 50 kb twin by reticular
merohedry.*

Crystal Research and Technology 35 (2000), 151–165.

Associated structure:

    COD 1521670

Reported cell approximately:

    a = 3.299 Å
    b = 3.299 Å
    c = 26.101 Å

    alpha = 90°
    beta  = 90°
    gamma = 120°

### Importance to this project

The associated crystallographic model contains mixed Ga/Zn occupancy.

This represents an experimental average structure and requires explicit
ordering before conventional atomistic DFT calculations.

---

## 2. Crystalline Structure Topics

Further literature review should cover:

- InGaZnO4 structural descriptions
- reported space groups
- Ga/Zn disorder
- cation ordering
- stability of ordered configurations
- lattice parameters
- cation coordination
- pressure dependence
- structural polymorphism

---

## 3. Electronic Structure

Review:

- experimental band gaps
- calculated band gaps
- conduction-band character
- valence-band character
- In contributions
- Ga contributions
- Zn contributions
- O contributions
- PBE/GGA calculations
- hybrid-functional calculations
- comparison with spectroscopy

---

## 4. Oxygen Vacancies

Review:

- neutral vacancies
- charged vacancies
- formation energies
- defect transition levels
- structural relaxation
- carrier generation
- localisation
- defect states
- crystalline versus amorphous behaviour

---

## 5. Amorphous IGZO

Review:

- AIMD methods
- system sizes
- starting configurations
- melt temperatures
- melt times
- quench rates
- density
- RDFs
- coordination distributions
- bond-angle distributions
- medium-range order
- electronic structure
- oxygen defects

---

## 6. Machine-Learning Interatomic Potentials

Review:

- ML potentials for metal oxides
- MACE for multicomponent systems
- MACE for amorphous materials
- active learning
- dataset construction
- uncertainty
- extrapolation
- defect-containing datasets

---

## 7. Application Context

Place the project within literature on:

- transparent conducting oxides
- transparent oxide semiconductors
- amorphous oxide semiconductors
- IGZO thin-film transistors
- low-power electronics
- defect-controlled conductivity
- disorder and localisation

---

## Literature Review Status

- [x] Primary crystallographic reference identified
- [ ] Complete crystalline structure review
- [ ] Review Ga/Zn ordering
- [ ] Review crystalline electronic structure
- [ ] Review oxygen vacancies
- [ ] Review amorphous IGZO modelling
- [ ] Review experimental amorphous structure
- [ ] Review MACE/ML potentials for oxides
- [ ] Build structured literature database

---

## Project-Derived Context for Future Literature Comparison

The current project calculations have selected a relaxed R3m
`ordered_003` model as the primary crystalline computational reference,
with P3m1 `ordered_001` retained as a near-degenerate alternative.

This is a project-derived result, not a literature claim. Future
literature review should specifically assess whether published
first-principles or diffraction studies report:

- competing R3m/P3m1 cation-ordering descriptions;
- relative stability of explicit Ga/Zn orderings;
- InO6, GaO5 and ZnO4 coordination environments;
- five-coordinate Ga trigonal-bipyramidal environments; and
- sensitivity of oxygen-vacancy energetics to local cation ordering.

These comparisons should be added only when supported by cited sources.
