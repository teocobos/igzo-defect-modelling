# Project Roadmap

## Milestone 1 — Crystalline Reference

- [x] Obtain experimental InGaZnO4 parent structure
- [x] Generate ordered crystalline models
- [x] Validate ordered structures
- [x] Establish CP2K convergence parameters
- [x] Optimise all four ordered structures
- [x] Perform tight final single-point calculations
- [x] Rank ordered structures by relative energy
- [x] Analyse relaxed symmetry
- [x] Analyse cation–oxygen coordination
- [x] Analyse bond-length distributions
- [x] Analyse coordination-polyhedron distortions
- [x] Select primary crystalline reference structure

Selected reference:

    igzo_crystal_ordered_003_relaxed

Secondary low-energy ordering:

    igzo_crystal_ordered_001_relaxed

Primary output:

**Validated crystalline InGaZnO4 computational reference**

---

### Crystalline reference validation — COMPLETE

- [x] Enumerate ordered crystalline IGZO models
- [x] Perform basis-set convergence
- [x] Perform plane-wave cutoff convergence
- [x] Perform relative-cutoff convergence
- [x] Perform k-point convergence
- [x] Relax all ordered structures
- [x] Compare ordered-structure energies
- [x] Perform CELL_OPT on low-energy candidates
- [x] Validate `ordered_003` R3m symmetry
- [x] Compare unconstrained P1 and constrained R3m minima
- [x] Select canonical crystalline reference
- [x] Enumerate symmetry-inequivalent oxygen sites

Canonical reference:

`igzo_crystal_ordered_003_r3m_cell_relaxed`

### Next: crystalline oxygen vacancies

- [ ] Define candidate crystalline defect supercells
- [ ] Perform supercell convergence assessment
- [ ] Map O001-O004 onto the selected supercell
- [ ] Generate neutral oxygen-vacancy structures
- [ ] Relax neutral vacancies
- [ ] Compare vacancy formation energies
- [ ] Extend selected vacancies to charged states
- [ ] Determine finite-size correction strategy
- [ ] Calculate defect electronic structure and charge-transition levels

---

## Milestone 2 — Crystalline Electronic Structure

- [x] Relax selected reference
- [ ] Calculate DOS
- [ ] Calculate PDOS
- [ ] Calculate band structure where appropriate
- [ ] Identify band-edge orbital character
- [ ] Compare with literature
- [ ] Cross-check selected results using VASP when available

Primary output:

**Validated pristine crystalline electronic structure**

---

## Milestone 3 — Crystalline Oxygen Vacancies

- [ ] Identify symmetry-inequivalent oxygen sites in relaxed ordered_003
- [ ] Determine oxygen-site multiplicities
- [ ] Characterise local cation coordination of each oxygen site
- [ ] Generate one vacancy structure per inequivalent oxygen site
- [ ] Validate generated vacancy structures
- [ ] Construct defect supercells
- [ ] Converge supercell size / defect–defect separation
- [ ] Converge/reassess k-point sampling for defect supercells
- [ ] Relax neutral oxygen vacancies
- [ ] Calculate vacancy formation energies
- [ ] Extend calculations to relevant charge states
- [ ] Analyse defect-induced structural relaxation
- [ ] Analyse defect electronic states
- [ ] Test selected defects in ordered_001 if ordering sensitivity is important

Primary output:

**First-principles crystalline oxygen-vacancy dataset**

---

## Milestone 4 — Amorphous IGZO

- [ ] Select near-isotropic stoichiometric starting cell
- [ ] Establish target density
- [ ] Establish CP2K AIMD parameters
- [ ] Establish melt protocol
- [ ] Establish quench protocol
- [ ] Generate independent trajectories
- [ ] Generate approximately 10–20 candidate amorphous structures
- [ ] Relax selected structures
- [ ] Validate density
- [ ] Validate RDFs
- [ ] Validate coordination
- [ ] Validate bond-angle distributions
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
