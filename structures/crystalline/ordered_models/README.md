# Ordered Crystalline IGZO Models

This directory contains explicit ordered computational representations derived from crystallographic reference structures.

These models are **computational structures**, not experimental crystallographic structures.

## Motivation

The experimental InGaZnO₄ structure from COD 1521670 contains a mixed Ga/Zn crystallographic site.

The conventional cell contains six positions associated with the mixed site.

Stoichiometric InGaZnO₄ requires these positions to contain:

```text
3 Ga
3 Zn
```

An explicit atomistic model is required for conventional DFT calculations using CP2K or VASP.

## Configuration Generation

For six mixed sites containing three Ga and three Zn atoms, the number of possible raw assignments is:

```text
C(6,3) = 20
```

Symmetry-equivalent configurations are removed before first-principles calculations.

The initial structure-generation workflow identifies four symmetry-distinct candidate orderings.

They are labelled:

```text
igzo_crystal_ordered_001
igzo_crystal_ordered_002
igzo_crystal_ordered_003
igzo_crystal_ordered_004
```

The numbering is arbitrary and does **not** represent energetic stability.

## Generation

Structures should be generated using:

```text
scripts/structure_generation/generate_igzo_orderings.py
```

rather than by manually modifying the experimental CIF.

The workflow is:

```text
COD 1521670
      ↓
Experimental average structure
      ↓
Identify mixed Ga/Zn positions
      ↓
Enumerate Ga/Zn assignments
      ↓
Remove symmetry-equivalent configurations
      ↓
Validate stoichiometry
      ↓
Ordered computational models
```

## Expected Composition

Each conventional-cell model should contain:

```text
In3Ga3Zn3O12
```

corresponding to three formula units of:

```text
InGaZnO4
```

## Model Directory

Each model should have its own directory:

```text
ordered_models/
├── igzo_crystal_ordered_001/
├── igzo_crystal_ordered_002/
├── igzo_crystal_ordered_003/
└── igzo_crystal_ordered_004/
```

A model directory may contain:

```text
igzo_crystal_ordered_001/
├── igzo_crystal_ordered_001.cif
├── igzo_crystal_ordered_001.vasp
├── igzo_crystal_ordered_001.xyz
└── metadata.yaml
```

## File Formats

### CIF

Used for crystallographic inspection and structural analysis.

### VASP

Prepared for future VASP calculations.

### XYZ

Used for interoperability with CP2K, ASE, MACE and other atomistic tools.

The original periodic structure and lattice information should remain traceable to the source CIF.

## Validation

Before DFT calculations, each generated model should be checked for:

* correct In:Ga:Zn:O stoichiometry
* absence of partial occupancies
* correct number of atoms
* lattice consistency
* sensible interatomic distances
* coordination environments
* duplicate atoms
* periodicity
* symmetry

## DFT Screening

The four models will initially be treated as candidate structures.

They will be geometry-optimised and compared using first-principles calculations.

The primary comparison should use energy per formula unit:

```text
Model        Energy/f.u.       Relative energy
001             ...                ...
002             ...                ...
003             ...                ...
004             ...                ...
```

The computational reference structure should only be selected after this comparison.

## Current Status

* [x] Experimental reference obtained
* [x] Mixed Ga/Zn occupancy identified
* [x] Ordering strategy established
* [ ] Generate ordered models
* [ ] Validate compositions
* [ ] Validate structures
* [ ] Perform CP2K geometry optimisation
* [ ] Compare relative energies
* [ ] Select crystalline reference structure
* [ ] Repeat/cross-check using VASP when available
