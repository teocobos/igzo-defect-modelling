# Metadata Schema

This document defines the metadata associated with structures,
calculations, datasets and models in the IGZO defect modelling project.

The purpose of the metadata schema is to maintain reproducibility,
traceability and computational provenance throughout the project.

---

## Structure Metadata

Where applicable, each structure should record:

- `structure_id`
- `composition`
- `structure_type`
- `number_of_atoms`
- `source`
- `source_reference`
- `generation_method`
- `parent_structure`
- `cell_parameters`
- `density`
- `temperature`
- `pressure`
- `defects`
- `defect_site`
- `defect_charge`
- `creation_date`
- `software`
- `software_version`
- `calculation_status`

---

## Calculation Metadata

Each significant calculation should record:

- `calculation_id`
- `structure_id`
- `software`
- `software_version`
- `functional`
- `pseudopotential`
- `basis_set`
- `cutoff`
- `kpoints`
- `spin_polarisation`
- `electronic_convergence`
- `ionic_convergence`
- `hpc_system`
- `job_id`
- `parent_calculation`
- `status`

Additional software-specific parameters should be recorded where
scientifically relevant.

---

## Defect Metadata

Where a defect is present, record:

- `defect_type`
- `defect_site`
- `defect_charge`
- `defect_concentration`
- `parent_structure`
- `relaxation_status`
- `formation_energy`

Additional defect-specific properties may be added where required.

---

## Dataset Metadata

For machine-learning datasets, record:

- `dataset_id`
- `source`
- `generation_method`
- `number_of_configurations`
- `number_of_atoms`
- `composition`
- `temperature_range`
- `configuration_types`
- `energy_available`
- `forces_available`
- `stress_available`
- `train_validation_test_split`
- `version`

---

## MACE Model Metadata

Each trained MACE model should record:

- `model_id`
- `dataset_id`
- `mace_version`
- `training_configuration`
- `random_seed`
- `training_set`
- `validation_set`
- `test_set`
- `energy_mae`
- `energy_rmse`
- `force_mae`
- `force_rmse`
- `domain_of_validity`
- `version`

---

## LAMMPS Sampling Metadata

For production MD sampling, record:

- `simulation_id`
- `model_id`
- `structure_id`
- `system_size`
- `temperature`
- `pressure`
- `ensemble`
- `timestep`
- `simulation_time`
- `sampling_interval`
- `trajectory_id`
- `random_seed`
- `software_version`

---

## Provenance

Every derived structure or dataset should retain a reference to its
parent structure, calculation or dataset wherever possible.

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
            ↓
    final analysis

The objective is to maintain traceability from every scientific result
back to its original structure, dataset and computational method.

---

## Metadata Storage

Metadata may be stored using machine-readable formats such as:

- YAML
- JSON
- CSV

For structure-specific metadata, YAML or JSON is preferred.

Human-readable documentation should remain in Markdown.

---

## Future Integration

The metadata schema should be compatible with:

- AiiDA provenance
- ASE
- pymatgen
- MACE datasets
- LAMMPS workflows
- Python analysis pipelines

The schema may be extended as the project develops.