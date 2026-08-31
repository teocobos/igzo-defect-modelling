# Results Log

This document records significant project observations, computational results and methodological decisions.

Planned work is recorded in `docs/project_roadmap.md`.

---

# 1. Experimental Crystalline Reference

## COD 1521670

**Status:** Completed.

**Material:** InGaZnO4

**Reference:** Nespolo, M.; Sato, A.; Osawa, T.; Ohashi, H. Crystal Research and Technology 35 (2000), 151–165.

Approximate experimental cell:

```text
a = b = 3.299 Å
c = 26.101 Å
alpha = beta = 90°
gamma = 120°
```

The experimental CIF contains mixed Ga/Zn occupancy and represents an average crystallographic structure.

Six mixed positions require three Ga and three Zn atoms.

```text
C(6,3) = 20
```

These raw assignments reduce to four symmetry-distinct ordered configurations.

---

# 2. Ordered Crystalline Models

| Model       | Atoms | Composition  | Initial space group |
| ----------- | ----: | ------------ | ------------------- |
| ordered_001 |    21 | In3Ga3Zn3O12 | P3m1                |
| ordered_002 |    21 | In3Ga3Zn3O12 | P3m1                |
| ordered_003 |    21 | In3Ga3Zn3O12 | R3m                 |
| ordered_004 |    21 | In3Ga3Zn3O12 | P3m1                |

All models passed structural validation.

---

# 3. PBE Numerical Convergence

## Basis

Representative energies:

```text
DZVP   -767.130342129481 Ha
TZVP   -767.168221873639 Ha
TZV2P  -767.175973661526 Ha
```

**Decision:** TZV2P.

---

## CUTOFF

At REL_CUTOFF = 60 Ry:

| CUTOFF / Ry |       Energy / Ha |
| ----------: | ----------------: |
|         400 | -765.408033199634 |
|         500 | -765.405577792115 |
|         600 | -765.405167005996 |
|         700 | -765.405095312065 |
|         800 | -765.404798877185 |

**Decision:** 700 Ry.

---

## REL_CUTOFF

At CUTOFF = 700 Ry:

| REL_CUTOFF / Ry |       Energy / Ha |
| --------------: | ----------------: |
|              40 | -765.405150784704 |
|              50 | -765.405097581796 |
|              60 | -765.405094899160 |
|              70 | -765.405095320479 |
|              80 | -765.405095312017 |
|             100 | -765.405095311677 |

**Decision:** 60 Ry.

---

## k-points

| Mesh  |       Energy / Ha |
| ----- | ----------------: |
| 1×1×1 | -765.405095436558 |
| 2×2×1 | -767.222831066246 |
| 3×3×1 | -767.176737618702 |
| 4×4×1 | -767.190552801255 |
| 5×5×1 | -767.189448804695 |
| 6×6×1 | -767.189945717155 |

**Decision:** 6×6×1 for the 21-atom crystalline reference.

---

# 4. Ordered-Structure Relaxation

Fixed-cell GEO_OPT energies:

```text
ordered_001  -767.247980382261 Ha
ordered_002  -767.169895002002 Ha
ordered_003  -767.248215342702 Ha
ordered_004  -767.166206810877 Ha
```

Tight final energies:

```text
ordered_001  -767.247977684509 Ha
ordered_002  -767.169898091297 Ha
ordered_003  -767.248205609002 Ha
ordered_004  -767.166212503339 Ha
```

Relative ordering:

```text
ordered_003 < ordered_001 << ordered_002 < ordered_004
```

Relative to ordered_003:

```text
ordered_001 ≈ +2.07 meV/f.u.
ordered_002 ≈ +710 meV/f.u.
ordered_004 ≈ +744 meV/f.u.
```

---

# 5. Cell Optimisation

## ordered_003 unconstrained

```text
E_CELL_OPT = -767.259029985456664 Ha
E_tight    = -767.259393316824116 Ha

a = b = 3.371432 Å
c = 26.171440 Å
V = 257.624398 Å^3
pressure = +96.305 bar
```

The relaxed coordinates were identified as P1 at tight symmetry tolerances.

## ordered_001

```text
E_CELL_OPT = -767.258676561620291 Ha
E_tight    = -767.259021707075931 Ha

a = b = 3.369483 Å
c = 26.210476 Å
V = 257.710482 Å^3
pressure = -1.501 bar
```

ordered_003 remained the lower-energy candidate.

---

# 6. R3m-Constrained Reference

A final ordered_003 CELL_OPT was performed using:

```text
KEEP_SYMMETRY TRUE
KEEP_SPACE_GROUP TRUE
KEEP_ANGLES TRUE
```

Final result:

```text
E_CELL_OPT = -767.2593919388 Ha
E_tight    = -767.259392342909337 Ha

pressure = -69.7746387 bar
V = 257.673092 Å^3

a = b = 3.371568 Å
c = 26.174270 Å
```

Exact CP2K 60° cell:

```text
A 3.3715680720631815 0.0000000000000000 0.0000000000000000
B 1.6857840360315908 2.9198636009952379 0.0000000000000000
C 0.0000000000000000 0.0000000000000000 26.174269634964521
```

Comparison with unconstrained P1:

```text
E(P1)  = -767.259393316824116 Ha
E(R3m) = -767.259392342909337 Ha
```

Difference:

```text
~0.0265 meV per cell
~0.0088 meV/f.u.
```

**Decision:** canonical crystalline reference = R3m ordered_003.

---

# 7. R3m Symmetry Validation

| symprec / Å | Space group |
| ----------: | ----------- |
|        1E-5 | P1          |
|        5E-5 | P1          |
|        1E-4 | P1          |
|        5E-4 | P1          |
|        1E-3 | P1          |
|        2E-3 | R3m         |
|        5E-3 | R3m         |
|        1E-2 | R3m         |

Production tolerance:

```text
SYMPREC = 2.0E-3
ANGLE_TOLERANCE = 5.0
```

---

# 8. Oxygen-Site Enumeration

Four symmetry-inequivalent oxygen classes:

## O001

```text
Environment: Ga3Zn1
Wyckoff: 3a
Multiplicity: 3
```

Representative coordination:

```text
Ga 1.946710 Å ×3
Zn 2.547845 Å ×1
```

## O002

```text
Environment: In3Zn1
Wyckoff: 3a
Multiplicity: 3
```

Representative coordination:

```text
Zn 2.002239 Å
In 2.225113 Å ×3
```

## O003

```text
Environment: In3Ga1
Wyckoff: 3a
Multiplicity: 3
```

Representative coordination:

```text
Ga 1.982168 Å
In 2.231800 Å ×3
```

## O004

```text
Environment: Ga1Zn3
Wyckoff: 3a
Multiplicity: 3
```

Representative coordination:

```text
Ga 2.007485 Å
Zn 2.026423 Å ×3
```

---

# 9. Defect Supercells

Generated pristine supercells:

```text
2×2×1: 84 atoms
3×3×1: 189 atoms
4×4×1: 336 atoms
```

Production 4×4×1 lattice:

```text
A  13.486272280000   0.000000000000   0.000000000000
B  -6.743136140000  11.679454396834   0.000000000000
C   0.000000000000   0.000000000000  26.174269630000
```

Production neutral vacancy structures contain 335 atoms.

---

# 10. Corrected Pristine Supercell Validation

Earlier development inputs were found to omit explicit `&MGRID`, `&QS` and `&POISSON` blocks.

Because CP2K defaults differ from the validated 700/60 Ry grid, those energies were not retained for scientific comparison.

Corrected calculations were rerun from atomic guesses with explicit:

```text
CUTOFF = 700 Ry
REL_CUTOFF = 60 Ry
METHOD GPW
EPS_PGF_ORB = 1E-18
EPS_FILTER_MATRIX = 0
PERIODIC XYZ
```

---

# 11. 3×3×1 Pristine k-point Test

Corrected energies:

```text
Γ:
-6905.224666809091104 Ha

2×2×1:
-6905.334544051158446 Ha
```

Difference:

```text
0.109877242067342 Ha
~2.990 eV/cell
~15.82 meV/atom
~110.7 meV/f.u.
```

**Result:** Γ-only is not converged for the absolute 3×3×1 pristine total energy.

---

# 12. 4×4×1 Γ Solver Test

```text
Γ + diagonalisation:
-12276.115932509646882 Ha

Γ + OT:
-12276.115920089672727 Ha
```

Difference:

```text
~1.242E-5 Ha
~0.000338 eV/cell
~0.0010 meV/atom
```

Approximate runtimes:

```text
DIAG: 1990 s
OT:    757 s
```

OT was approximately 2.6× faster.

---

# 13. 4×4×1 + 2×2×1 Test

The 336-atom 4×4×1 calculation with 2×2×1 sampling did not enter SCF under the available memory/resources.

Increasing resources was not considered necessary because this sampling corresponds to a reciprocal-space density beyond the established primitive-cell requirement.

**Decision:** exclude from production.

---

# 14. O001 3×3×1 2×2×1 Diagonalisation

Final GEO_OPT energy:

```text
-6889.225469819143655 Ha
```

Matched pristine:

```text
-6905.334544051158446 Ha
```

Matched difference:

```text
16.109074232014791 Ha
```

First-shell relaxation:

```text
Ga: -0.094044 Å
Zn: +0.080849 Å
O:  -0.052455 Å
```

Ga moves inward toward the vacancy.

---

# 15. O001 3×3×1 Γ + OT

Final GEO_OPT:

```text
-6889.147759208457501 Ha
```

Tight defect energy:

```text
-6889.147760105754969 Ha
```

Tight pristine:

```text
-6905.224659654308198 Ha
```

Matched difference:

```text
16.076899548553229 Ha
```

First-shell relaxation:

```text
Ga: +0.117150 Å
Zn: +0.085985 Å
O:  -0.126901 Å
```

Ga and Zn move outward; neighbouring oxygen moves inward.

---

# 16. O001 4×4×1 Γ + OT

Final GEO_OPT:

```text
-12260.034627548473509 Ha
```

Tight defect:

```text
-12260.034628938619790 Ha
```

Tight pristine:

```text
-12276.115920089672727 Ha
```

Matched difference:

```text
16.081291151052937 Ha
```

Representative first-shell relaxation:

```text
Ga: +0.223704 Å
Zn: +0.064467 Å
O:  -0.156253 Å
```

The relaxation remains localised.

---

# 17. O001 3×3×1 Γ + Diagonalisation

**Status:** Completed.

Final GEO_OPT energy:

```text
-6889.147763739658330 Ha
```

Runtime:

```text
~1878.5 s
~31.3 min
```

Final frame:

```text
i = 12
```

First-shell reconstruction:

| Element | Count | Initial distance / Å | Final distance / Å | Mean radial change / Å |
| ------- | ----: | -------------------: | -----------------: | ---------------------: |
| Ga      |     3 |             1.946710 |           2.063575 |              +0.116865 |
| Zn      |     1 |             2.547845 |           2.634596 |              +0.086751 |
| O       |     6 |             2.787210 |           2.659979 |              -0.127231 |

Relaxation localisation:

| Radius / Å | Max displacement outside / Å | Mean displacement outside / Å |
| ---------: | ---------------------------: | ----------------------------: |
|          3 |                     0.086996 |                      0.008210 |
|          4 |                     0.034895 |                      0.006951 |
|          5 |                     0.034895 |                      0.006323 |
|          6 |                     0.020857 |                      0.004394 |
|          7 |                     0.015114 |                      0.003786 |

The Γ+DIAG structure is essentially identical to the Γ+OT reconstruction.

---

# 18. O001 Solver Conclusion

Comparison:

| Setup          | Ga Δr / Å | Zn Δr / Å | O Δr / Å |
| -------------- | --------: | --------: | -------: |
| 3×3 2×2×1 DIAG |   -0.0940 |   +0.0808 |  -0.0525 |
| 3×3 Γ DIAG     |   +0.1169 |   +0.0868 |  -0.1272 |
| 3×3 Γ OT       |   +0.1172 |   +0.0860 |  -0.1269 |
| 4×4 Γ OT       |   +0.2237 |   +0.0645 |  -0.1563 |

Energy difference between 3×3 Γ DIAG and tight Γ OT:

```text
~3.63E-6 Ha
~9.9E-5 eV
```

**Conclusion:** OT is not responsible for the O001 reconstruction change.

The different minimum is associated with Γ versus 2×2×1 Brillouin-zone sampling.

---

# 19. O001 Supercell-Size Sensitivity

Matched Γ+OT:

```text
3×3×1:
16.076899548553229 Ha

4×4×1:
16.081291151052937 Ha
```

Difference:

```text
0.004391602499708 Ha
~0.1195 eV
```

This residual is retained as finite-size sensitivity in the current screening methodology.

---

# 20. Production PBE Vacancy Decision

The production PBE neutral-vacancy screening workflow is:

```text
4×4×1
Γ-only
OT
PBE
TZV2P-MOLOPT-PBE-GTH
GTH-PBE
CUTOFF = 700 Ry
REL_CUTOFF = 60 Ry
fixed-cell BFGS GEO_OPT
```

Final defect energies are obtained from tight static calculations using:

```text
EPS_SCF = 1E-7
```

This choice balances:

* defect localisation;
* supercell separation;
* numerical validation;
* solver accuracy;
* computational feasibility.

---

# 21. PBE Neutral Oxygen-Vacancy Dataset

**Status:** Completed.

Neutral 4×4×1 Γ+OT PBE geometry optimisations and tight final static-energy calculations have been completed for all four symmetry-inequivalent oxygen-vacancy sites:

```text
O001
O002
O003
O004
```

The production calculations use the 336-atom pristine cell and corresponding 335-atom neutral oxygen-vacancy cells.

## 21.1 Tight final energies

| Site | Local environment | Tight static energy / Ha | Relative energy / eV |
| ---- | ----------------- | -----------------------: | -------------------: |
| O004 | Ga1Zn3            |      -12260.070245473984 |             0.000000 |
| O003 | In3Ga1            |      -12260.066175247555 |            +0.110757 |
| O002 | In3Zn1            |      -12260.051235718196 |            +0.517282 |
| O001 | Ga3Zn1            |      -12260.034628938620 |            +0.969175 |

The final PBE energetic ordering is:

```text
O004 < O003 < O002 < O001
```

O004 is therefore the lowest-energy neutral oxygen-vacancy configuration within the validated PBE screening dataset.

The tight static corrections relative to the converged final GEO_OPT energies are extremely small and do not alter the ordering.

---

## 21.2 O002 structural reconstruction

O002 has the local cation environment:

```text
In3Zn1
```

First-shell reconstruction:

| Element | Count | Initial distance / Å | Final distance / Å | Mean radial change / Å |
| ------- | ----: | -------------------: | -----------------: | ---------------------: |
| In      |     3 |             2.225113 |           2.415355 |              +0.190242 |
| Zn      |     1 |             2.002239 |           2.324077 |              +0.321838 |
| O       |     3 |             2.914868 |           2.809492 |              -0.105376 |

The Zn neighbour exhibits the largest first-shell displacement:

```text
0.321838 Å
```

The three In neighbours also move outward from the vacancy, while the nearby oxygen atoms relax inward.

Relaxation outside 6 Å:

```text
maximum displacement = 0.050448 Å
mean displacement    = 0.005712 Å
```

---

## 21.3 O003 structural reconstruction

O003 has the local cation environment:

```text
In3Ga1
```

First-shell reconstruction:

| Element | Count | Initial distance / Å | Final distance / Å | Mean radial change / Å |
| ------- | ----: | -------------------: | -----------------: | ---------------------: |
| Ga      |     1 |             1.982168 |           2.340300 |              +0.358132 |
| In      |     3 |             2.231800 |           2.398497 |              +0.166696 |
| O       |     6 |             2.854694 |           2.691005 |              -0.163690 |

The Ga neighbour moves strongly outward:

```text
+0.358132 Å
```

while neighbouring oxygen atoms move inward toward the vacancy region.

A structured second-shell response is also present, including an oxygen initially approximately 3.99 Å from the vacancy that moves by approximately 0.213 Å.

Relaxation outside 6 Å:

```text
maximum displacement = 0.061460 Å
mean displacement    = 0.006654 Å
```

---

## 21.4 O004 structural reconstruction

O004 has the local cation environment:

```text
Ga1Zn3
```

First-shell reconstruction:

| Element | Count | Initial distance / Å | Final distance / Å | Mean radial change / Å |
| ------- | ----: | -------------------: | -----------------: | ---------------------: |
| Ga      |     1 |             2.007485 |           2.308928 |              +0.301442 |
| Zn      |     3 |             2.026423 |           2.413767 |              +0.387344 |
| O       |     3 |             2.779900 |           2.528435 |              -0.251464 |

O004 exhibits the largest first-shell reconstruction among the four sites.

The three Zn neighbours move strongly outward:

```text
+0.387344 Å
```

while the nearby oxygen shell undergoes a substantial inward reconstruction:

```text
-0.251464 Å
```

The maximum first-shell atomic displacement is:

```text
0.389473 Å
```

Relaxation outside 6 Å:

```text
maximum displacement = 0.057760 Å
mean displacement    = 0.007111 Å
```

---

## 21.5 Four-site structural comparison

| Site | Environment | Relative energy / eV | Maximum first-shell displacement / Å | Maximum displacement outside 6 Å / Å | Mean displacement outside 6 Å / Å |
| ---- | ----------- | -------------------: | -----------------------------------: | -----------------------------------: | --------------------------------: |
| O001 | Ga3Zn1      |            +0.969175 |                             0.223948 |                             0.018212 |                          0.004549 |
| O002 | In3Zn1      |            +0.517282 |                             0.321838 |                             0.050448 |                          0.005712 |
| O003 | In3Ga1      |            +0.110757 |                             0.358132 |                             0.061460 |                          0.006654 |
| O004 | Ga1Zn3      |             0.000000 |                             0.389473 |                             0.057760 |                          0.007111 |

The lower-energy O003 and O004 configurations exhibit larger first-shell reconstructions than O001.

This suggests that the ability of the local environment to accommodate oxygen removal through cation and anion rearrangement may contribute to vacancy stabilisation.

However, this is currently treated as a structural correlation rather than a demonstrated causal relationship.

A quantitative separation of vacancy-creation energy and lattice-relaxation energy would require comparison with unrelaxed defect calculations.

---

## 21.6 Relaxation localisation

All four 4×4×1 vacancy calculations show predominantly local structural reconstruction.

Mean atomic displacements beyond 6 Å are:

```text
O001: 0.004549 Å
O002: 0.005712 Å
O003: 0.006654 Å
O004: 0.007111 Å
```

All remain below approximately 0.008 Å.

This supports the use of the 4×4×1 supercell for the present PBE neutral-vacancy screening workflow.

The previously identified approximately 0.12 eV O001 3×3×1-to-4×4×1 matched-energy difference remains the primary explicit finite-size sensitivity benchmark.

---

## 21.7 Dataset outputs

The consolidated dataset is stored under:

```text
results/crystalline/oxygen_vacancies/pbe/
```

Primary processed files:

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

for:

```text
O001
O002
O003
O004
```

Generated comparison figures include:

```text
figures/vacancy_relative_energies.png
figures/vacancy_first_shell_relaxation.png
figures/vacancy_displacement_comparison.png
```

The dataset-level analysis is generated using:

```text
scripts/analysis/build_pbe_vacancy_dataset.py
```

**Decision:** the PBE neutral oxygen-vacancy screening dataset is complete.

---

# 22. PBE0-TC-LRC Pristine Validation

The next major electronic-structure methodology is PBE0-TC-LRC.

PBE0-TC-LRC parameters will not be transferred blindly from previous materials or calculations.

The hybrid-functional workflow will first be validated on the 21-atom pristine canonical R3m crystalline reference.

The planned sequence is:

```text
PBE R3m reference
      ↓
PBE0-TC-LRC pristine single-point validation
      ↓
validate exact exchange / TC-LRC / ADMM / SCF behaviour
      ↓
analyse pristine hybrid electronic structure
      ↓
PBE0-TC-LRC R3m CELL_OPT
      ↓
tight hybrid pristine reference
      ↓
construct hybrid-reference supercells
      ↓
hybrid oxygen-vacancy calculations
```

Initial validation will examine:

* SCF stability;
* exact-exchange implementation;
* truncated-Coulomb/LRC parameters;
* auxiliary-density-matrix/ADMM strategy where appropriate;
* basis compatibility;
* k-point strategy;
* band gap;
* band-edge character;
* structural response.

The pristine hybrid single-point calculation will be performed before the PBE0-TC-LRC CELL_OPT.

The PBE0-TC-LRC CELL_OPT will be performed only on the pristine 21-atom R3m reference.

Large hybrid defect supercells will subsequently inherit the hybrid-optimised pristine lattice and undergo fixed-cell ionic relaxation.

**Status:** CURRENT ACTIVE METHODOLOGICAL STAGE.

---

# 23. Future Hybrid Defect Workflow

Once the pristine PBE0-TC-LRC methodology is validated, selected oxygen-vacancy structures will proceed through:

```text
PBE-relaxed vacancy
        ↓
PBE0-TC-LRC single point
        ↓
electronic localisation / spin analysis
        ↓
PBE0-TC-LRC fixed-cell GEO_OPT
        ↓
final electronic-structure analysis
```

The hybrid stage will assess:

* vacancy energetic ordering;
* structural changes relative to PBE;
* defect-electron localisation;
* spin state;
* PDOS;
* in-gap or resonant defect levels;
* charge density;
* spin density;
* possible localisation metastability.

Subsequent charged-defect calculations will establish:

* physically relevant charge states;
* finite-size electrostatic corrections;
* potential alignment;
* chemical-potential limits;
* formation energies;
* charge-transition levels.

PBE0-TC-LRC parameters remain subject to explicit validation before production use.