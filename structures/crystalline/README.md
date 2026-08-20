# Experimental Reference Structures

This directory contains external crystallographic structures used as reference data for the IGZO defect-modelling project.

These structures provide the experimental provenance from which computational models are generated.

## Current Reference

The primary reference structure is:

```text
igzo_crystal_ingazno4_cod1521670.cif
```

### Source

**Crystallography Open Database**

* COD ID: `1521670`
* Material: InGaZnO₄
* Source: Nespolo *et al.*, *Crystal Research and Technology* **35** (2000), 151–165.

## Important

Files in this directory should represent the original externally sourced crystallographic data.

They should **not be manually modified** for computational calculations.

If changes are required, generate a new derived structure elsewhere in the repository.

The provenance relationship should remain:

```text
External crystallographic source
             ↓
        reference/
             ↓
   computational model
```

## Partial Occupancies

The current experimental CIF contains a mixed Ga/Zn crystallographic site with approximately:

```text
Ga = 0.5
Zn = 0.5
```

This represents an experimental average structure.

It is therefore retained as a crystallographic reference rather than used directly as an explicit atomistic DFT structure.

Ordered computational representations are generated separately under:

```text
../ordered_models/
```

## Provenance Requirements

For every reference structure, record where possible:

* database/source
* database identifier
* publication
* authors
* composition
* lattice parameters
* reported space group
* date accessed
* licence or redistribution conditions

Associated project metadata should be stored under:

```text
../metadata/
```

## Naming Convention

Reference structures should include their source identifier where practical.

Example:

```text
igzo_crystal_ingazno4_cod1521670.cif
```

This helps distinguish externally sourced structures from structures generated within the project.

## Rule

**Reference structures are immutable inputs.**

Derived, ordered, transformed or DFT-relaxed structures should never overwrite files in this directory.
