# IGZO Defect Modelling — Project Roadmap

## Project Objective

Develop a reproducible computational framework for investigating
structural disorder, oxygen vacancies and electronic properties in
indium gallium zinc oxide (IGZO).

The project progresses from first-principles calculations to
machine-learning-assisted large-scale sampling.

---

# Milestone 1 — Computational Foundation

- [ ] Repository established
- [ ] Project scope defined
- [ ] Naming conventions established
- [ ] Metadata schema established
- [ ] Crystalline IGZO structure selected
- [ ] VASP computational parameters converged
- [ ] Pristine crystalline IGZO relaxed
- [ ] Pristine electronic structure calculated
- [ ] Electronic structure validated against literature

**Primary output:**

Validated crystalline IGZO computational model.

---

# Milestone 2 — Oxygen Vacancy Physics

- [ ] Oxygen-vacancy generation workflow established
- [ ] Inequivalent oxygen sites identified
- [ ] Vacancy structures generated
- [ ] Vacancy structures relaxed
- [ ] Vacancy formation energies calculated
- [ ] Defect electronic states analysed
- [ ] Relevant charge states investigated

**Primary output:**

Initial first-principles description of oxygen vacancies in crystalline
IGZO.

---

# Milestone 3 — Amorphous IGZO

- [ ] CP2K amorphisation workflow established
- [ ] Melt/quench protocol validated
- [ ] Multiple independent amorphous structures generated
- [ ] Density analysed
- [ ] RDFs calculated
- [ ] Coordination statistics calculated
- [ ] Bond-angle distributions calculated
- [ ] Ring statistics calculated
- [ ] Structures compared with available experimental/literature data

**Primary output:**

Validated ensemble of amorphous IGZO structures.

---

# Milestone 4 — Machine-Learning Potential

- [ ] AIMD configurations selected
- [ ] DFT reference dataset generated
- [ ] Dataset cleaned
- [ ] Training/validation/test sets created
- [ ] Initial MACE model trained
- [ ] Energy errors evaluated
- [ ] Force errors evaluated
- [ ] Unseen configurations tested
- [ ] Structural stability tested
- [ ] MD stability tested
- [ ] Domain of validity established

**Primary output:**

Validated MACE potential for the intended IGZO configuration space.

---

# Milestone 5 — Large-Scale Sampling

- [ ] MACE-LAMMPS interface validated
- [ ] Small-system tests completed
- [ ] Production MD parameters established
- [ ] Independent trajectories generated
- [ ] Large amorphous ensemble generated
- [ ] Structural statistics calculated
- [ ] System-size effects assessed where necessary

**Primary output:**

Statistically meaningful ensemble of amorphous IGZO structures.

---

# Milestone 6 — Oxygen Vacancy Statistics

- [ ] Vacancy generation applied to amorphous structures
- [ ] Local vacancy environments classified
- [ ] Representative structures selected
- [ ] DFT vacancy calculations performed
- [ ] Vacancy formation-energy distribution obtained
- [ ] Local structural descriptors calculated
- [ ] Structural/energetic correlations analysed
- [ ] Crystalline and amorphous vacancy behaviour compared

**Primary output:**

Statistical description of oxygen-vacancy energetics in amorphous IGZO.

---

# Milestone 7 — Electronic Properties

- [ ] Representative amorphous structures selected
- [ ] Pristine amorphous electronic properties calculated
- [ ] Representative vacancy structures calculated
- [ ] Defect states identified
- [ ] DOS/PDOS analysed
- [ ] Charge localisation analysed
- [ ] Crystalline/amorphous electronic properties compared

**Primary output:**

Relationship between structural disorder, oxygen vacancies and
electronic properties.

---

# Milestone 8 — Scientific Dissemination

- [ ] Central scientific narrative established
- [ ] Final analysis completed
- [ ] Publication-quality figures generated
- [ ] Computational methods documented
- [ ] Reproducibility audit completed
- [ ] Internal Nanosystems Advisory review completed
- [ ] Manuscript prepared
- [ ] Appropriate publication venue selected
- [ ] Code/data release strategy established

**Primary output:**

Publication-ready research package.

---

# Initial Dataset Targets

These are planning targets rather than fixed requirements.

| Dataset | Initial target |
|---|---:|
| Crystalline models | 1–3 |
| CP2K amorphous structures | 10–20 |
| Initial AIMD configurations | 1,000–5,000 |
| MACE training set | ~70% |
| MACE validation set | ~15% |
| MACE test set | ~15% |
| Independent MACE test structures | 200–500 |
| Large-scale amorphous structures | Hundreds–1,000s |
| DFT validation subset | ~50–200 |

Dataset sizes should be revised according to configuration-space
coverage, convergence and model validation.

---

# Scientific Narrative

The intended progression is:

    crystalline IGZO
            ↓
    structural disorder
            ↓
    amorphous IGZO
            ↓
    validated MACE potential
            ↓
    large-scale structural sampling
            ↓
    oxygen vacancies
            ↓
    defect energetics
            ↓
    electronic consequences

The objective is to progress from computational methodology to
statistically meaningful scientific conclusions.