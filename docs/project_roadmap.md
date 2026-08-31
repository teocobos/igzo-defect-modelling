# Project Roadmap

## Milestone 1 — Crystalline Reference

* [x] Obtain experimental InGaZnO4 parent structure
* [x] Generate ordered crystalline models
* [x] Validate ordered structures
* [x] Establish CP2K convergence parameters
* [x] Optimise all four ordered structures
* [x] Perform tight final single-point calculations
* [x] Rank ordered structures
* [x] Analyse relaxed symmetry
* [x] Analyse cation–oxygen coordination
* [x] Analyse bond-length distributions
* [x] Analyse coordination-polyhedron distortions
* [x] Perform CELL_OPT
* [x] Validate R3m symmetry
* [x] Select canonical crystalline reference

Canonical reference:

```text
igzo_crystal_ordered_003_r3m_cell_relaxed
```

**Milestone status: COMPLETE**

---

## Milestone 2 — Crystalline Defect Infrastructure

* [x] Enumerate O001–O004
* [x] Determine multiplicities
* [x] Characterise local cation environments
* [x] Generate 2×2×1, 3×3×1 and 4×4×1 supercells
* [x] Generate neutral oxygen-vacancy structures
* [x] Validate atom counts
* [x] Validate site identities
* [x] Establish defect metadata
* [x] Establish vacancy-relaxation analysis workflow
* [x] Establish exact 4×4×1 production cell

**Milestone status: COMPLETE**

---

## Milestone 3 — PBE Neutral Vacancy Validation

* [x] Test pristine 3×3×1 Γ sampling
* [x] Test pristine 3×3×1 2×2×1 sampling
* [x] Test pristine 4×4×1 Γ diagonalisation
* [x] Test pristine 4×4×1 Γ OT
* [x] Attempt 4×4×1 2×2×1
* [x] Validate O001 in 3×3×1 2×2×1 DIAG
* [x] Validate O001 in 3×3×1 Γ OT
* [x] Validate O001 in 3×3×1 Γ DIAG
* [x] Validate O001 in 4×4×1 Γ OT
* [x] Analyse solver dependence
* [x] Analyse k-point dependence
* [x] Analyse supercell-size sensitivity
* [x] Analyse relaxation localisation
* [x] Select production workflow

Production workflow:

```text
4×4×1 + Γ + OT + PBE
```

**Milestone status: COMPLETE**

---

## Milestone 4 — PBE Neutral Vacancy Dataset

* [x] Relax O001
* [x] Relax O002
* [x] Relax O003
* [x] Relax O004
* [ ] Extract tight/consistent final energies for O001–O004
* [ ] Analyse O002 relaxation
* [ ] Analyse O003 relaxation
* [ ] Analyse O004 relaxation
* [ ] Compare first-shell reconstruction
* [ ] Compare relaxation localisation
* [ ] Rank neutral vacancy energies
* [ ] Curate relaxed structures
* [ ] Generate comparison figures
* [ ] Complete PBE neutral-vacancy dataset summary

**Current active milestone.**

Primary output:

**Validated PBE crystalline neutral oxygen-vacancy screening dataset**

---

## Milestone 5 — PBE0-TC-LRC Pristine Validation

* [ ] Generate pristine PBE0-TC-LRC input
* [ ] Validate exact-exchange settings
* [ ] Validate TC/LRC parameters
* [ ] Validate auxiliary-basis/ADMM strategy where appropriate
* [ ] Validate SCF convergence
* [ ] Establish hybrid k-point strategy
* [ ] Calculate pristine hybrid single-point energy
* [ ] Calculate band gap
* [ ] Analyse band-edge character
* [ ] Compare with PBE
* [ ] Compare with literature
* [ ] Perform R3m PBE0-TC-LRC CELL_OPT
* [ ] Perform tight final hybrid single point
* [ ] Establish canonical hybrid pristine reference

Primary output:

**Validated PBE0-TC-LRC crystalline IGZO reference**

---

## Milestone 6 — Hybrid Neutral Oxygen Vacancies

* [ ] Generate hybrid-reference supercells
* [ ] Select vacancy configurations from PBE screening
* [ ] Perform PBE0-TC-LRC single points on PBE structures
* [ ] Examine defect-electron localisation
* [ ] Examine spin states
* [ ] Relax selected vacancies with PBE0-TC-LRC
* [ ] Calculate PDOS
* [ ] Analyse defect levels
* [ ] Analyse charge/spin densities
* [ ] Compare PBE and PBE0-TC-LRC structures
* [ ] Assess ordering sensitivity if required

Primary output:

**Hybrid-functional neutral oxygen-vacancy dataset**

---

## Milestone 7 — Charged Defects and CTLs

* [ ] Determine relevant vacancy charge states
* [ ] Establish charged-supercell methodology
* [ ] Determine finite-size correction strategy
* [ ] Establish potential alignment
* [ ] Establish oxygen chemical-potential limits
* [ ] Determine competing phases
* [ ] Calculate charged-defect energies
* [ ] Calculate formation energies
* [ ] Calculate charge-transition levels
* [ ] Analyse localisation/spin
* [ ] Perform Koopmans/localisation checks where appropriate

Primary output:

**Crystalline IGZO defect thermodynamics and CTLs**

---

## Milestone 8 — Crystalline Electronic Structure

* [x] Relax PBE crystalline reference
* [ ] Calculate PBE DOS/PDOS where useful
* [ ] Calculate PBE0-TC-LRC DOS/PDOS
* [ ] Calculate band structure
* [ ] Identify band-edge orbital character
* [ ] Compare with literature
* [ ] Cross-check selected results with VASP when available

Primary output:

**Validated pristine crystalline electronic structure**

---

## Milestone 9 — Amorphous IGZO

* [ ] Select near-isotropic stoichiometric starting cell
* [ ] Establish target density
* [ ] Establish CP2K AIMD parameters
* [ ] Establish melt protocol
* [ ] Establish quench protocol
* [ ] Generate independent trajectories
* [ ] Generate approximately 10–20 candidate structures
* [ ] Relax selected structures
* [ ] Validate density
* [ ] Validate RDFs
* [ ] Validate coordination
* [ ] Validate bond angles
* [ ] Validate medium-range structure

Primary output:

**Validated amorphous IGZO ensemble**

---

## Milestone 10 — MACE Dataset

* [ ] Define configuration classes
* [ ] Sample DFT/AIMD configurations
* [ ] Remove excessive correlation
* [ ] Generate reference energies
* [ ] Generate reference forces
* [ ] Generate stresses where required
* [ ] Create train/validation/test split
* [ ] Version dataset

Primary output:

**Validated IGZO reference dataset**

---

## Milestone 11 — MACE Potential

* [ ] Train initial model
* [ ] Evaluate energies
* [ ] Evaluate forces
* [ ] Evaluate unseen structures
* [ ] Test geometry optimisation
* [ ] Test MD stability
* [ ] Identify extrapolation
* [ ] Iteratively improve dataset
* [ ] Establish domain of validity

Primary output:

**Validated MACE potential**

---

## Milestone 12 — LAMMPS Sampling

* [ ] Integrate MACE with LAMMPS
* [ ] Validate small system
* [ ] Generate larger systems
* [ ] Run independent trajectories
* [ ] Produce amorphous ensemble
* [ ] Analyse system-size effects

Primary output:

**Large-scale amorphous IGZO ensemble**

---

## Milestone 13 — Amorphous Oxygen Vacancies

* [ ] Characterise local oxygen environments
* [ ] Select representative sites
* [ ] Generate defects
* [ ] Perform DFT calculations
* [ ] Calculate formation-energy distributions
* [ ] Identify structural correlations
* [ ] Compare crystalline and amorphous behaviour

Primary output:

**Statistical oxygen-vacancy model**

---

## Milestone 14 — Publication

* [ ] Finalise analysis
* [ ] Generate publication-quality figures
* [ ] Complete reproducibility audit
* [ ] Complete internal IP review
* [ ] Prepare technical report
* [ ] Prepare manuscript
* [ ] Determine code/data release
* [ ] Create repository release

Primary output:

**Publication-ready research package**
