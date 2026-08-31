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

raw assignments reduce to four symmetry-distinct ordered configurations.

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

This choice balances:

* defect localisation;
* supercell separation;
* numerical validation;
* solver accuracy;
* computational feasibility.

---

# 21. O002–O004 Production Calculations

Neutral 4×4×1 Γ+OT PBE GEO_OPT calculations have completed for:

```text
O002
O003
O004
```

Together with O001, all four symmetry-distinct neutral oxygen-vacancy production calculations are now complete.

Their final energies and structural reconstructions will be consolidated in the next analysis stage.

No relative energetic ranking is recorded here until the completed outputs have been processed consistently.

---

# 22. Next Methodological Stage

The next high-level electronic-structure methodology is PBE0-TC-LRC.

The planned sequence is:

```text
PBE R3m reference
      ↓
PBE0-TC-LRC pristine single-point validation
      ↓
PBE0-TC-LRC R3m CELL_OPT
      ↓
tight hybrid pristine reference
      ↓
hybrid neutral-vacancy calculations
      ↓
charged vacancies
      ↓
formation energies and CTLs
```

PBE0-TC-LRC parameters remain subject to explicit validation before production use.