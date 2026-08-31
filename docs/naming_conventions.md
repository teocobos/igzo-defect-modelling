# Naming Conventions

This document defines naming conventions for structures, calculations, datasets, models, figures and validation workflows.

---

## General Rules

* use lowercase filenames where practical;
* use underscores between fields;
* avoid spaces;
* avoid temporary HPC job IDs in permanent filenames;
* retain stable structure and defect identifiers;
* use explicit versions only for deliberate releases;
* avoid names such as `final`, `final2` and `new_final`;
* distinguish validation calculations from production calculations.

---

## Reference Structures

Format:

```text
igzo_crystal_<composition>_<source>
```

Example:

```text
igzo_crystal_ingazno4_cod1521670.cif
```

---

## Ordered Crystalline Models

Format:

```text
igzo_crystal_ordered_<identifier>
```

Examples:

```text
igzo_crystal_ordered_001
igzo_crystal_ordered_002
igzo_crystal_ordered_003
igzo_crystal_ordered_004
```

Identifiers do not imply energetic ranking.

---

## Canonical R3m Reference

The canonical PBE crystalline reference is:

```text
igzo_crystal_ordered_003_r3m_cell_relaxed
```

Associated files:

```text
igzo_crystal_ordered_003_r3m_cell_relaxed.cif
igzo_crystal_ordered_003_r3m_cell_relaxed.xyz
```

Do not rename this structure to `final`.

---

## Supercells

Preferred compact defect-workflow form:

```text
igzo_r3m_<na>x<nb>x<nc>
```

Examples:

```text
igzo_r3m_2x2x1
igzo_r3m_3x3x1
igzo_r3m_4x4x1
```

Pristine structure example:

```text
igzo_r3m_4x4x1.cif
```

---

## Oxygen Sites

Stable labels:

```text
O001
O002
O003
O004
```

Lowercase filenames use:

```text
o001
o002
o003
o004
```

These labels must not be reassigned after site enumeration.

---

## Defects

Preferred crystalline vacancy format:

```text
igzo_r3m_<supercell>_vo_<site>_<charge>
```

Examples:

```text
igzo_r3m_3x3x1_vo_o001_q0
igzo_r3m_4x4x1_vo_o002_q0
igzo_r3m_4x4x1_vo_o003_q0
igzo_r3m_4x4x1_vo_o004_q0
```

Future charged examples:

```text
igzo_r3m_4x4x1_vo_o001_q+1
igzo_r3m_4x4x1_vo_o001_q+2
```

The charge label describes the defect-cell charge state.

---

## PBE Calculation Method Labels

Use concise method directories.

### Γ + OT

```text
pbe_gamma_ot
```

Production 4×4×1 neutral-vacancy workflow.

### Γ + diagonalisation

```text
pbe_gamma
```

Used for validation unless a more explicit future distinction is required.

### 2×2×1 + diagonalisation

```text
pbe_2x2x1
```

Used for the O001 3×3×1 k-point benchmark.

Where ambiguity may arise in future datasets, use explicit forms:

```text
pbe_gamma_diag
pbe_2x2x1_diag
```

but do not rename completed calculation directories solely for cosmetic consistency.

---

## CP2K Project Names

Preferred format:

```text
igzo_r3m_<supercell>_vo_<site>_<charge>_<method>
```

Examples:

```text
igzo_r3m_4x4x1_vo_o001_q0_pbe_gamma_ot
igzo_r3m_4x4x1_vo_o002_q0_pbe_gamma_ot
igzo_r3m_3x3x1_vo_o001_q0_pbe_gamma
```

---

## Validation Results

Validation output directories should make the tested variable explicit.

Example:

```text
results/crystalline/oxygen_vacancies/validation/
```

Individual labels:

```text
O001_3x3_2x2x1_diag
O001_3x3_gamma_diag
O001_3x3_gamma_ot
O001_4x4_gamma_ot
```

Validation calculations should remain distinguishable from production datasets.

---

## Production Results

Production neutral-vacancy results should use:

```text
results/crystalline/oxygen_vacancies/pbe/
```

Suggested structure:

```text
results/crystalline/oxygen_vacancies/pbe/
├── vacancy_energy_summary.csv
├── vacancy_structural_summary.csv
├── vacancy_first_shell_summary.csv
├── vacancy_localisation_summary.csv
├── relaxed_structures/
└── figures/
```

---

## PBE0-TC-LRC

Use:

```text
pbe0_tc_lrc
```

Examples:

```text
igzo_r3m_pbe0_tc_lrc
igzo_r3m_4x4x1_vo_o001_q0_pbe0_tc_lrc
```

Additional method qualifiers may be added only where they distinguish genuinely different calculations.

Examples:

```text
pbe0_tc_lrc_sp
pbe0_tc_lrc_geo_opt
pbe0_tc_lrc_cell_opt
```

---

## Relaxed Structures

General format:

```text
<structure_id>_relaxed
```

Examples:

```text
igzo_r3m_4x4x1_vo_o001_q0_pbe_relaxed
igzo_r3m_4x4x1_vo_o002_q0_pbe_relaxed
```

For the canonical pristine reference, retain:

```text
igzo_crystal_ordered_003_r3m_cell_relaxed
```

---

## Amorphous Structures

Format:

```text
igzo_amorphous_<natoms>atoms_<trajectory>_<frame>
```

Example:

```text
igzo_amorphous_189atoms_traj03_frame0450.xyz
```

---

## VASP Calculations

Examples:

```text
vasp_crystal_relax
vasp_crystal_band
vasp_crystal_dos
vasp_vacancy_o001_q0
```

---

## MACE

Datasets:

```text
igzo_mace_training_v01
igzo_mace_validation_v01
igzo_mace_test_v01
```

Models:

```text
mace_igzo_v01
mace_igzo_v02
```

---

## LAMMPS

Examples:

```text
lammps_igzo_amorphous_traj001
lammps_igzo_amorphous_traj002
```

---

## Figures

Format:

```text
fig_<number>_<description>
```

Examples:

```text
fig_01_crystal_structure
fig_02_cp2k_convergence
fig_03_ordering_energies
fig_04_relaxed_polyhedra
fig_05_vacancy_validation
fig_06_vacancy_energies
fig_07_vacancy_relaxation
fig_08_hybrid_band_structure
```

---

## Versioning

Use:

```text
v01
v02
v03
```

for deliberate dataset, model or workflow releases.

Version numbers must not substitute for Git history.

---

## Naming Principle

A permanent name should answer, where relevant:

```text
What material?
What structure?
What supercell?
What defect?
What site?
What charge?
What method?
```

while remaining short enough to use reliably in scripts and HPC workflows.