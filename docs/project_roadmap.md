# Project Roadmap

## Milestone 1 — Crystalline Reference

- [x] Identify experimental InGaZnO4 structure
- [x] Obtain COD reference CIF
- [x] Record provenance
- [x] Identify Ga/Zn mixed occupancy
- [x] Establish ordering strategy
- [x] Generate four symmetry-distinct ordered models
- [x] Validate generated structures
- [ ] Establish CP2K convergence parameters
- [ ] Relax ordered structures
- [ ] Compare relative energies
- [ ] Select crystalline reference model

Primary output:

**Validated crystalline InGaZnO4 computational reference**

---

## Milestone 2 — Crystalline Electronic Structure

- [ ] Relax selected reference
- [ ] Calculate DOS
- [ ] Calculate PDOS
- [ ] Calculate band structure where appropriate
- [ ] Identify band-edge orbital character
- [ ] Compare with literature
- [ ] Cross-check using VASP when available

Primary output:

**Validated pristine crystalline electronic structure**

---

## Milestone 3 — Crystalline Oxygen Vacancies

- [ ] Identify inequivalent oxygen sites
- [ ] Generate vacancy structures
- [ ] Relax defects
- [ ] Calculate vacancy energetics
- [ ] Analyse local relaxation
- [ ] Analyse electronic states
- [ ] Investigate relevant charge states

Primary output:

**First-principles crystalline oxygen-vacancy dataset**

---

## Milestone 4 — Amorphous IGZO

- [ ] Establish CP2K AIMD parameters
- [ ] Establish melt protocol
- [ ] Establish quench protocol
- [ ] Generate independent trajectories
- [ ] Generate 10–20 candidate amorphous structures
- [ ] Relax selected structures
- [ ] Validate density
- [ ] Validate RDFs
- [ ] Validate coordination
- [ ] Validate medium-range structure

Primary output:

**Validated amorphous IGZO ensemble**

---

## Milestone 5 — MACE Dataset

- [ ] Define configuration classes
- [ ] Sample DFT/AIMD configurations
- [ ] Remove excessive correlation
- [ ] Generate reference energies
- [ ] Generate reference forces
- [ ] Generate stresses where required
- [ ] Create train/validation/test split
- [ ] Version dataset

Primary output:

**Validated IGZO reference dataset**

---

## Milestone 6 — MACE Potential

- [ ] Train initial model
- [ ] Evaluate energies
- [ ] Evaluate forces
- [ ] Evaluate unseen structures
- [ ] Test geometry optimisation
- [ ] Test MD stability
- [ ] Identify extrapolation
- [ ] Iteratively improve dataset
- [ ] Establish domain of validity

Primary output:

**Validated MACE potential**

---

## Milestone 7 — LAMMPS Sampling

- [ ] Integrate MACE with LAMMPS
- [ ] Validate small system
- [ ] Generate larger systems
- [ ] Run independent trajectories
- [ ] Produce amorphous ensemble
- [ ] Analyse system-size effects

Primary output:

**Large-scale amorphous IGZO ensemble**

---

## Milestone 8 — Amorphous Oxygen Vacancies

- [ ] Characterise local oxygen environments
- [ ] Select representative sites
- [ ] Generate defects
- [ ] Perform DFT calculations
- [ ] Calculate formation-energy distributions
- [ ] Identify structural correlations
- [ ] Compare crystalline and amorphous behaviour

Primary output:

**Statistical oxygen-vacancy model**

---

## Milestone 9 — Publication

- [ ] Finalise analysis
- [ ] Generate publication-quality figures
- [ ] Complete reproducibility audit
- [ ] Complete internal IP review
- [ ] Prepare technical report
- [ ] Prepare manuscript
- [ ] Determine code/data release
- [ ] Create repository release

Primary output:

**Publication-ready research package**