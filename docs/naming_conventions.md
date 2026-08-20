# Naming Conventions

This document defines the naming conventions used throughout the
IGZO defect modelling project.

## General Principles

- Use lowercase filenames.
- Use underscores `_` to separate fields.
- Use descriptive, machine-readable names.
- Avoid spaces and special characters.
- Use consistent identifiers for structures, calculations, datasets,
  models and figures.
- Use version identifiers where deliberate versions exist.
- Avoid temporary HPC job IDs in permanent filenames.
- Preserve identifiers when structures move between computational stages.

---

## Structures

### Crystalline Structures

Format:

    igzo_crystal_<composition>_<structure>_<version>

Example:

    igzo_crystal_111_primitive_v01.vasp

### Amorphous Structures

Format:

    igzo_amorphous_<cellsize>_<trajectory>_<frame>

Example:

    igzo_amorphous_120atoms_traj03_frame0450.xyz

### Defect Structures

Format:

    igzo_<defect_type>_<site>_<charge>_<version>

Example:

    igzo_vacancy_o17_q0_v01.vasp

---

## Calculations

Format:

    <software>_<system>_<calculation_type>

Examples:

    vasp_pristine_relax
    vasp_pristine_band
    vasp_pristine_dos
    vasp_vacancy_o17_q0

    cp2k_melt_traj01
    cp2k_quench_traj01

    mace_train_v01
    mace_test_v01

    lammps_amorphous_001

---

## Trajectories

Format:

    <software>_<system>_<trajectory_type>_<identifier>

Examples:

    cp2k_igzo_melt_traj01
    cp2k_igzo_quench_traj01
    lammps_igzo_amorphous_traj001

---

## Datasets

Format:

    igzo_<dataset_type>_<version>

Examples:

    igzo_mace_training_v01
    igzo_mace_validation_v01
    igzo_mace_test_v01

---

## MACE Models

Format:

    mace_igzo_<model_type>_<version>

Examples:

    mace_igzo_amorphous_v01
    mace_igzo_defect_v01

---

## Figures

Format:

    fig_<number>_<description>

Examples:

    fig_01_crystalline_structure
    fig_02_vasp_convergence
    fig_03_band_structure
    fig_04_pristine_dos
    fig_05_vacancy_formation_energy

---

## Scripts

Use descriptive names indicating the purpose of the script.

Examples:

    generate_vacancies.py
    calculate_rdf.py
    analyse_coordination.py
    calculate_ring_statistics.py
    plot_pdos.py
    calculate_vacancy_statistics.py

---

## Versions

Use:

    v01
    v02
    v03

for deliberate versions of structures, datasets, models or workflows.

Avoid ambiguous names such as:

    final
    final2
    final_new
    final_really_final

---

## Identifiers

Use consistent identifiers for:

- Structures
- Oxygen sites
- Defect charge states
- Trajectories
- AIMD frames
- Datasets
- MACE models
- LAMMPS simulations

The same identifier should be retained throughout the project wherever
possible.

---

## Provenance

Names should allow a structure or dataset to be traced through the
computational workflow.

Example:

    crystalline structure
            ↓
    relaxed structure
            ↓
    amorphous AIMD structure
            ↓
    MACE dataset configuration
            ↓
    LAMMPS sampled configuration
            ↓
    oxygen-vacancy structure
            ↓
    DFT defect calculation