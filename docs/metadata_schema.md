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
- `parent_structure`
- `generation_script`

Example:

```yaml
ordering:
  ordered: true
  ordering_id: ordered_001
  ordering_method: exhaustive_enumeration
  raw_configuration_count: 20
  symmetry_class: 1
  generation_script: generate_igzo_orderings.py