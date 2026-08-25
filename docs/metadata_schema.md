# Metadata Schema

This document defines metadata used to maintain traceability and
computational provenance throughout the project.

---

## Structure Metadata

Recommended fields:

- `structure_id`
- `composition`
- `structure_type`
- `number_of_atoms`
- `source_database`
- `source_id`
- `source_reference`
- `parent_structure`
- `generation_method`
- `generation_script`
- `cell_parameters`
- `density`
- `temperature`
- `pressure`
- `creation_date`
- `software`
- `software_version`
- `status`

---

## Ordering Metadata

For structures derived from partially occupied crystallographic models:

- `ordered`
- `ordering_id`
- `ordering_method`
- `raw_configuration_count`
- `symmetry_class`
- `space_group_initial`
- `space_group_relaxed`
- `parent_structure`
- `generation_script`
- `relative_energy_mev_per_fu`
- `reference_status`

Example:

```yaml
ordering:
  ordered: true
  ordering_id: ordered_003
  ordering_method: exhaustive_enumeration
  raw_configuration_count: 20
  space_group_initial: "R3m (160)"
  space_group_relaxed: "R3m (160)"
  parent_structure: igzo_crystal_ingazno4_cod1521670
  generation_script: generate_igzo_orderings.py
  relative_energy_mev_per_fu: 0.0
  reference_status: primary
```

---

## Calculation Metadata

Recommended fields:

- `calculation_id`
- `structure_id`
- `calculation_type`
- `software`
- `software_version`
- `machine`
- `scheduler`
- `job_id`
- `input_file`
- `output_file`
- `xc_functional`
- `basis_set_family`
- `pseudopotential_family`
- `cutoff_ry`
- `rel_cutoff_ry`
- `kpoint_mesh`
- `eps_scf`
- `max_scf`
- `scf_method`
- `geometry_optimizer`
- `restart_parent`
- `status`
- `final_energy_hartree`
- `warnings`

---

## Relaxation Metadata

For relaxed structures:

- `parent_structure`
- `relaxation_calculation`
- `optimizer`
- `fixed_cell`
- `geometry_steps`
- `final_energy_hartree`
- `final_space_group`
- `final_force_status`
- `tight_single_point_calculation`
- `tight_single_point_energy_hartree`

---

## Defect Metadata

For oxygen-vacancy structures:

- `defect_id`
- `parent_structure`
- `supercell_id`
- `defect_type`
- `removed_species`
- `site_index`
- `site_label`
- `symmetry_class`
- `multiplicity`
- `charge_state`
- `neighbouring_cations`
- `local_coordination`
- `local_bond_lengths`
- `relaxation_status`
- `formation_energy_ev`
- `electronic_state_summary`

Example:

```yaml
defect:
  defect_type: oxygen_vacancy
  site_label: o001
  charge_state: 0
  parent_structure: igzo_crystal_ordered_003_relaxed
  supercell_id: TBD
  multiplicity: TBD
```

---

## Dataset Metadata

Recommended fields:

- `dataset_id`
- `dataset_version`
- `configuration_classes`
- `number_of_configurations`
- `source_calculations`
- `selection_method`
- `train_fraction`
- `validation_fraction`
- `test_fraction`
- `random_seed`
- `creation_date`
- `status`
