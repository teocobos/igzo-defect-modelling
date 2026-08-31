# Validation Strategy

Each stage of the IGZO workflow requires validation before results are used for subsequent production calculations.

---

## 1. Reference CIF

Validate:

* composition;
* lattice parameters;
* site occupancies;
* atomic coordinates;
* symmetry information;
* bibliographic provenance.

Current reference:

```text
COD 1521670
```

**Status:** PASSED.

The original CIF remains unmodified.

---

## 2. Ordered Crystalline Models

Each generated model should satisfy:

* In3Ga3Zn3O12 composition;
* 21 atoms in the conventional cell;
* 3 In atoms;
* 3 Ga atoms;
* 3 Zn atoms;
* 12 O atoms;
* no partial occupancies;
* correct periodic lattice;
* no overlapping atoms;
* physically sensible interatomic distances.

Symmetry-equivalent configurations should not be retained unnecessarily.

Four symmetry-distinct ordered configurations were retained.

**Status:** PASSED.

---

## 3. CP2K Crystalline Convergence

Validated for the 21-atom crystalline ordering/reference workflow:

* [x] basis-set sensitivity assessed;
* [x] CUTOFF convergence assessed;
* [x] REL_CUTOFF convergence assessed;
* [x] k-point convergence assessed;
* [x] SCF strategy tested;
* [x] final tight single-point threshold established.

Validated primitive-cell parameters:

* PBE;
* TZV2P-MOLOPT-PBE-GTH;
* matching GTH-PBE pseudopotentials;
* CUTOFF = 700 Ry;
* REL_CUTOFF = 60 Ry;
* 6×6×1 Monkhorst-Pack mesh;
* geometry-optimisation EPS_SCF = 1e-6;
* final single-point EPS_SCF = 1e-7.

**Status:** PASSED for the crystalline reference workflow.

These parameters are not transferred automatically to larger defect or amorphous cells without additional validation.

---

## 4. Crystalline Reference Structure Validation

Four candidate ordered InGaZnO4 structures were independently geometry optimised on ARCHER2 using a consistent CP2K workflow.

Validation criteria:

* [x] geometry optimisation completed for all four structures;
* [x] identical physical/numerical settings used across the comparison;
* [x] final energies recalculated using EPS_SCF = 1e-7;
* [x] energetic ordering stable with tighter SCF convergence;
* [x] relaxed structures checked for crystallographic symmetry;
* [x] coordination numbers validated;
* [x] bond-length distributions analysed;
* [x] local polyhedral distortions analysed;
* [x] low-energy candidates subjected to CELL_OPT;
* [x] R3m symmetry explicitly validated.

Final fixed-cell energetic ordering:

```text
ordered_003 < ordered_001 << ordered_002 < ordered_004
```

`ordered_003` and `ordered_001` differ by approximately 2.07 meV/f.u.

`ordered_002` and `ordered_004` lie more than approximately 0.7 eV/f.u. above the minimum.

Primary crystalline reference:

```text
igzo_crystal_ordered_003_r3m_cell_relaxed
```

Secondary low-energy ordering:

```text
igzo_crystal_ordered_001
```

**Status:** PASSED.

---

## 5. Crystalline Symmetry Validation

The final `ordered_003` structure was tested for sensitivity to the symmetry tolerance used by pymatgen/spglib.

The R3m-constrained final geometry was classified as:

| symprec / Å | Space group |
| ----------: | ----------- |
|      1.0E-5 | P1          |
|      5.0E-5 | P1          |
|      1.0E-4 | P1          |
|      5.0E-4 | P1          |
|      1.0E-3 | P1          |
|      2.0E-3 | R3m         |
|      5.0E-3 | R3m         |
|      1.0E-2 | R3m         |

The deviations from exact special positions are therefore of order 10^-3 Å.

Production symmetry analysis uses:

```text
symprec = 2.0E-3 Å
angle_tolerance = 5.0°
```

A direct energetic comparison was also made between:

1. an unconstrained P1 cell-relaxed structure; and
2. an explicitly R3m-constrained cell-relaxed structure.

Final tight energies:

```text
E(P1)  = -767.259393316824116 Ha
E(R3m) = -767.259392342909337 Ha
```

The difference is approximately:

```text
0.0265 meV per 21-atom cell
0.0088 meV per InGaZnO4 formula unit
```

The P1 distortion is therefore interpreted as shallow numerical symmetry breaking rather than evidence for a distinct lower-symmetry phase.

**Status:** PASSED.

---

## 6. Oxygen-Site Enumeration

The canonical R3m structure contains 12 oxygen atoms that reduce to four symmetry-inequivalent classes.

| Site | Wyckoff | Multiplicity | Local cation environment |
| ---- | ------- | -----------: | ------------------------ |
| O001 | 3a      |            3 | Ga3Zn1                   |
| O002 | 3a      |            3 | In3Zn1                   |
| O003 | 3a      |            3 | In3Ga1                   |
| O004 | 3a      |            3 | Ga1Zn3                   |

Production site enumeration uses the canonical R3m reference and:

```text
SYMPREC = 2.0E-3
ANGLE_TOLERANCE = 5.0
NEIGHBOR_CUTOFF = 2.7 Å
```

**Status:** PASSED.

---

## 7. Crystalline Defect Supercell Validation

Candidate supercells derived from the canonical R3m reference were considered:

| Supercell | Atoms pristine | Approx. in-plane repeat |
| --------- | -------------: | ----------------------: |
| 2×2×1     |             84 |                  6.74 Å |
| 3×3×1     |            189 |                 10.11 Å |
| 4×4×1     |            336 |                 13.49 Å |

The c lattice parameter is already approximately 26.17 Å, so the shortest periodic defect separation is in the ab plane.

### 7.1 Pristine 3×3×1 k-point sensitivity

Corrected calculations using the validated 700/60 Ry grid gave:

```text
3×3×1 Γ:
E = -6905.224666809091104 Ha

3×3×1 2×2×1:
E = -6905.334544051158446 Ha
```

The difference is approximately:

```text
0.109877 Ha
2.99 eV per 189-atom cell
15.8 meV/atom
```

Γ-only sampling is therefore not converged for the absolute pristine 3×3×1 total energy.

A 2×2×1 mesh on the 3×3×1 supercell corresponds approximately to the reciprocal-space density of the validated 6×6×1 primitive-cell calculation.

### 7.2 4×4×1 Γ solver validation

Pristine 4×4×1 calculations gave:

```text
Γ + diagonalisation:
-12276.115932509646882 Ha

Γ + OT:
-12276.115920089672727 Ha
```

Difference:

```text
~1.24E-5 Ha
~0.000338 eV per 336-atom cell
~0.0010 meV/atom
```

OT reduced the runtime substantially while reproducing the Γ-point diagonalisation energy to very high precision.

### 7.3 4×4×1 + 2×2×1

A 4×4×1 calculation with a 2×2×1 mesh was found to be substantially more memory intensive and did not enter production SCF under the allocated resources.

This mesh would correspond to a reciprocal-space density exceeding that required by the validated primitive-cell 6×6×1 reference.

It is therefore excluded from the current production screening workflow.

---

## 8. O001 Neutral Oxygen-Vacancy Validation

O001 was used to validate supercell size, Brillouin-zone sampling and SCF solver choice before production calculations for O002–O004.

### 8.1 Calculations

| Supercell | Sampling | SCF solver      | Purpose                   |
| --------- | -------- | --------------- | ------------------------- |
| 3×3×1     | 2×2×1    | diagonalisation | k-point benchmark         |
| 3×3×1     | Γ        | diagonalisation | solver/k-point isolation  |
| 3×3×1     | Γ        | OT              | Γ production-method test  |
| 4×4×1     | Γ        | OT              | production supercell test |

All geometry optimisations completed successfully.

### 8.2 Γ-point solver comparison

Final 3×3×1 O001 energies:

```text
Γ + diagonalisation GEO_OPT:
-6889.147763739658330 Ha

Γ + OT tight static:
-6889.147760105754969 Ha
```

The difference is approximately:

```text
3.63E-6 Ha
9.9E-5 eV per defect cell
```

This difference is negligible for the present screening workflow.

### 8.3 Local reconstruction

First-shell radial changes:

| Setup                         | Ga Δr / Å | Zn Δr / Å | O Δr / Å |
| ----------------------------- | --------: | --------: | -------: |
| 3×3×1, 2×2×1, diagonalisation |   -0.0940 |   +0.0808 |  -0.0525 |
| 3×3×1, Γ, OT                  |   +0.1172 |   +0.0860 |  -0.1269 |
| 3×3×1, Γ, diagonalisation     |   +0.1169 |   +0.0868 |  -0.1272 |
| 4×4×1, Γ, OT                  |   +0.2237 |   +0.0645 |  -0.1563 |

The two independent 3×3×1 Γ calculations reproduce essentially the same local minimum despite using different SCF solvers.

Therefore:

**the O001 reconstruction difference is associated with Brillouin-zone sampling rather than OT versus diagonalisation.**

### 8.4 Relaxation localisation

For the 3×3×1 Γ + diagonalisation calculation:

```text
maximum displacement outside 6 Å = 0.0209 Å
maximum displacement outside 7 Å = 0.0151 Å
```

The defect-induced structural relaxation is therefore strongly localised.

The 3×3×1 Γ+OT and 4×4×1 Γ+OT calculations show similarly localised behaviour.

### 8.5 Matched defect-pristine energy differences

For consistent Γ+OT calculations:

```text
ΔE(3×3×1) = 16.076899548553229 Ha
ΔE(4×4×1) = 16.081291151052937 Ha
```

Difference:

```text
0.0043916025 Ha
~0.1195 eV
```

This residual supercell-size sensitivity must be retained when interpreting absolute vacancy energetics.

### 8.6 Production decision

The production PBE neutral-vacancy screening workflow is:

```text
4×4×1
Γ-only
OT
PBE
TZV2P-MOLOPT-PBE-GTH
700 Ry / 60 Ry
fixed-cell BFGS GEO_OPT
```

The 3×3×1 2×2×1 calculation is retained as a k-point-sensitivity benchmark rather than the production defect workflow.

**O001 validation status:** PASSED.

---

## 9. Production Neutral Oxygen-Vacancy Dataset

The production neutral oxygen-vacancy dataset contains four symmetry-inequivalent configurations:

```text
O001
O002
O003
O004
```

Each defective production cell contains:

```text
335 atoms
```

and is derived from the 336-atom 4×4×1 R3m pristine supercell.

The exact production cell is:

```text
A  13.486272280000   0.000000000000   0.000000000000
B  -6.743136140000  11.679454396834   0.000000000000
C   0.000000000000   0.000000000000  26.174269630000
```

with periodicity in XYZ.

All four fixed-cell Γ+OT PBE geometry optimisations and tight final static calculations have completed successfully.

### 9.1 Tight final energies

| Site | Environment | Tight static energy / Ha | Relative energy / eV |
| ---- | ----------- | -----------------------: | -------------------: |
| O004 | Ga1Zn3      |      -12260.070245473984 |             0.000000 |
| O003 | In3Ga1      |      -12260.066175247555 |            +0.110757 |
| O002 | In3Zn1      |      -12260.051235718196 |            +0.517282 |
| O001 | Ga3Zn1      |      -12260.034628938620 |            +0.969175 |

Final ordering:

```text
O004 < O003 < O002 < O001
```

The energetic ranking is robust to the final tighter SCF calculation because the differences between final GEO_OPT and tight static energies are negligible compared with the energy separation among sites.

### 9.2 First-shell reconstruction

Representative radial reconstruction:

| Site | Local environment | Principal cation response                | Oxygen response   |
| ---- | ----------------- | ---------------------------------------- | ----------------- |
| O001 | Ga3Zn1            | Ga outward ~0.224 Å; Zn outward ~0.064 Å | O inward ~0.156 Å |
| O002 | In3Zn1            | In outward ~0.190 Å; Zn outward ~0.322 Å | O inward ~0.105 Å |
| O003 | In3Ga1            | In outward ~0.167 Å; Ga outward ~0.358 Å | O inward ~0.164 Å |
| O004 | Ga1Zn3            | Ga outward ~0.301 Å; Zn outward ~0.387 Å | O inward ~0.251 Å |

Maximum first-shell displacements:

```text
O001: 0.223948 Å
O002: 0.321838 Å
O003: 0.358132 Å
O004: 0.389473 Å
```

The lowest-energy O004 configuration therefore exhibits the largest maximum first-shell reconstruction in the current PBE dataset.

O003 also undergoes a pronounced reconstruction.

This correlation does not by itself demonstrate that structural relaxation is the cause of the energetic ordering.

A future decomposition using unrelaxed and relaxed vacancy energies would be required to quantify lattice-relaxation stabilisation directly.

### 9.3 Relaxation localisation

At a radius of 6 Å:

| Site | Maximum displacement outside 6 Å / Å | Mean displacement outside 6 Å / Å |
| ---- | -----------------------------------: | --------------------------------: |
| O001 |                             0.018212 |                          0.004549 |
| O002 |                             0.050448 |                          0.005712 |
| O003 |                             0.061460 |                          0.006654 |
| O004 |                             0.057760 |                          0.007111 |

Mean displacements beyond 6 Å remain below approximately 0.008 Å for all four configurations.

The large first-shell distortions therefore remain predominantly local rather than generating a substantial long-range displacement field across the supercell.

### 9.4 Dataset reproducibility

Processed results are consolidated under:

```text
results/crystalline/oxygen_vacancies/pbe/
```

including:

```text
vacancy_tight_energies.csv
vacancy_energy_summary.csv
vacancy_first_shell_summary.csv
vacancy_structural_summary.csv
vacancy_localisation_summary.csv
```

Curated relaxed structures are stored under:

```text
results/crystalline/oxygen_vacancies/pbe/relaxed_structures/
```

Comparison figures are stored under:

```text
results/crystalline/oxygen_vacancies/pbe/figures/
```

The consolidated dataset is generated using:

```text
scripts/analysis/build_pbe_vacancy_dataset.py
```

**Status:** PASSED — PBE NEUTRAL OXYGEN-VACANCY DATASET COMPLETE.

---

## 10. PBE0-TC-LRC Validation

PBE0-TC-LRC will not be applied directly to large defect supercells without prior pristine validation.

The initial validation target is the canonical 21-atom pristine R3m crystalline reference.

Planned sequence:

```text
PBE R3m reference
        ↓
pristine PBE0-TC-LRC single-point validation
        ↓
validate hybrid methodology
        ↓
PBE0-TC-LRC R3m CELL_OPT
        ↓
tight pristine hybrid reference
        ↓
hybrid defect calculations
```

The pristine single-point calculation precedes the hybrid CELL_OPT so that the electronic methodology can be validated before structural optimisation.

The PBE0-TC-LRC CELL_OPT will be performed on the 21-atom pristine R3m reference.

Defective hybrid supercells will subsequently use the lattice obtained from the pristine hybrid reference and will be relaxed at fixed cell.

Validation will include:

* SCF stability;
* exact-exchange settings;
* truncated-Coulomb/LRC parameters;
* auxiliary-basis/ADMM strategy where appropriate;
* basis-set compatibility;
* hybrid k-point strategy;
* band gap;
* band-edge character;
* structural parameters;
* comparison with available literature;
* defect-electron localisation behaviour.

No PBE0-TC-LRC production parameter set will be considered validated until these checks are complete.

**Status:** CURRENT ACTIVE VALIDATION STAGE.

---

## 11. Crystalline Electronic Structure

Before electronic-structure results are treated as validated:

* establish pristine PBE0-TC-LRC methodology;
* calculate DOS/PDOS;
* identify band-edge orbital character;
* calculate band structure where appropriate;
* compare with available literature;
* cross-check selected results with VASP where appropriate.

**Status:** PENDING HYBRID VALIDATION.

---

## 12. Hybrid Neutral Oxygen Vacancies

After pristine hybrid validation:

* generate supercells from the hybrid-optimised pristine reference;
* perform PBE0-TC-LRC single points on selected PBE-relaxed vacancies;
* assess electronic localisation;
* test relevant spin states;
* perform fixed-cell hybrid GEO_OPT;
* calculate PDOS;
* analyse defect levels;
* analyse charge and spin density;
* compare PBE and PBE0-TC-LRC geometries and energetic ordering.

The initial hybrid calculations may prioritise PBE-identified configurations while retaining sufficient coverage to determine whether the energetic ordering changes at hybrid level.

**Status:** PENDING.

---

## 13. Charged Oxygen Vacancies

After hybrid validation:

* determine physically relevant charge states;
* test spin/localisation states;
* establish finite-size electrostatic correction methodology;
* establish potential alignment;
* establish oxygen chemical-potential limits;
* calculate formation energies;
* calculate charge-transition levels.

The general defect formation-energy expression is:

```text
E_f(D^q) =
E_defect^q
- E_bulk
- Σ_i n_i μ_i
+ q(E_F + E_VBM)
+ E_corr
```

Chemical-potential limits must be constrained by relevant competing phases rather than by an arbitrary isolated oxygen reference.

**Status:** PENDING.

---

## 14. Amorphous Structures

A completed melt-quench trajectory is not sufficient validation.

Validation will include:

* density;
* total and partial RDFs;
* In–O, Ga–O, Zn–O and O–O correlations;
* coordination distributions;
* bond lengths;
* bond angles;
* local polyhedra;
* ring statistics where useful;
* multiple independent structures;
* system-size effects.

**Status:** PENDING.

---

## 15. MACE

Validate numerically using:

* energy MAE/RMSE;
* force MAE/RMSE;
* stress errors where relevant.

Validate physically using:

* structures;
* energetic ordering;
* RDFs;
* coordination;
* geometry optimisation;
* short MD;
* temperature stability;
* extrapolation tests.

**Status:** PENDING.

---

## 16. LAMMPS

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

* one amorphous structure;
* one Ga/Zn ordering;
* one defect site;
* one k-point sampling choice;
* one SCF solver;
* one supercell size;
* one ML model;
* one simulation trajectory.

Statistical and first-principles validation should be used wherever scientifically appropriate.