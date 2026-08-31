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

## 9. Production Neutral Oxygen Vacancies

Production neutral vacancy structures contain:

```text
335 atoms
```

and are generated for:

```text
O001
O002
O003
O004
```

using the 4×4×1 R3m-derived supercell.

The exact production cell is:

```text
A  13.486272280000   0.000000000000   0.000000000000
B  -6.743136140000  11.679454396834   0.000000000000
C   0.000000000000   0.000000000000  26.174269630000
```

with periodicity in XYZ.

O001 has completed the production workflow.

O002–O004 have completed their production calculations and await consolidated energetic and structural analysis.

**Status:** PRODUCTION CALCULATIONS COMPLETE; DATASET ANALYSIS IN PROGRESS.

---

## 10. PBE0-TC-LRC Validation

PBE0-TC-LRC will not be applied directly to large defect supercells without prior pristine validation.

Planned sequence:

```text
PBE R3m reference
        ↓
pristine PBE0-TC-LRC single-point validation
        ↓
PBE0-TC-LRC R3m CELL_OPT
        ↓
tight pristine hybrid reference
        ↓
hybrid defect calculations
```

The PBE0-TC-LRC CELL_OPT will be performed on the 21-atom pristine R3m reference.

Defective hybrid supercells will subsequently use the lattice obtained from the pristine hybrid reference and will be relaxed at fixed cell.

Validation will include:

* SCF stability;
* exact-exchange settings;
* truncated-Coulomb/LRC parameters;
* band gap;
* band-edge character;
* structural parameters;
* comparison with available literature;
* defect-electron localisation behaviour.

**Status:** NEXT MAJOR VALIDATION STAGE.

---

## 11. Crystalline Electronic Structure

Before electronic-structure results are treated as validated:

* establish pristine PBE0-TC-LRC methodology;
* calculate DOS/PDOS;
* identify band-edge orbital character;
* calculate band structure where appropriate;
* compare with available literature;
* cross-check selected results with VASP where appropriate.

**Status:** PENDING.

---

## 12. Charged Oxygen Vacancies

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

## 13. Amorphous Structures

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

## 14. MACE

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

## 15. LAMMPS

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