
---

# 6. `docs/naming_conventions.md`

```markdown
# Naming Conventions

This document defines naming conventions for structures, calculations,
datasets, models and figures.

---

## General Rules

- Use lowercase filenames.
- Use underscores `_` between fields.
- Avoid spaces.
- Avoid temporary HPC job IDs in permanent filenames.
- Use explicit version numbers.
- Preserve identifiers throughout derived workflows.
- Avoid names such as `final`, `final2` or `new_final`.

---

# Reference Structures

Format:

    igzo_crystal_<composition>_<source>

Current example:

    igzo_crystal_ingazno4_cod1521670.cif

The external database identifier should be retained in reference
structure filenames where practical.

---

# Ordered Crystalline Models

Format:

    igzo_crystal_ordered_<identifier>

Examples:

    igzo_crystal_ordered_001
    igzo_crystal_ordered_002
    igzo_crystal_ordered_003
    igzo_crystal_ordered_004

Model identifiers do not imply energetic ranking.

---

# Relaxed Structures

Format:

    <structure_id>_relaxed

Example:

    igzo_crystal_ordered_001_relaxed

---

# Amorphous Structures

Format:

    igzo_amorphous_<natoms>atoms_<trajectory>_<frame>

Example:

    igzo_amorphous_120atoms_traj03_frame0450.xyz

---

# Defects

Format:

    igzo_<host>_<defect>_<site>_<charge>

Examples:

    igzo_crystal_vacancy_o017_q0
    igzo_amorphous_vacancy_o043_q+2

---

# CP2K Calculations

Examples:

    cp2k_crystal_convergence_cutoff
    cp2k_crystal_relax_ordered_001
    cp2k_aimd_melt_traj01
    cp2k_aimd_quench_traj01

---

# VASP Calculations

Examples:

    vasp_crystal_relax
    vasp_crystal_band
    vasp_crystal_dos
    vasp_vacancy_o017_q0

---

# MACE

Datasets:

    igzo_mace_training_v01
    igzo_mace_validation_v01
    igzo_mace_test_v01

Models:

    mace_igzo_v01
    mace_igzo_v02

---

# LAMMPS

Examples:

    lammps_igzo_amorphous_traj001
    lammps_igzo_amorphous_traj002

---

# Figures

Format:

    fig_<number>_<description>

Examples:

    fig_01_crystal_structure
    fig_02_cp2k_convergence
    fig_03_ordering_energies
    fig_04_band_structure
    fig_05_vacancy_distribution

---

# Versioning

Use:

    v01
    v02
    v03

for deliberate dataset, model or workflow versions.

Version numbers should not be used as substitutes for Git history.