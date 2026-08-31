# Reproducibility

Reproducibility and computational provenance are core requirements of the IGZO defect-modelling project.

---

## Provenance Chain

```text
COD 1521670
      ↓
experimental CIF
      ↓
generate_igzo_orderings.py
      ↓
four ordered crystalline models
      ↓
PBE convergence + relaxation
      ↓
ordered_003
      ↓
R3m-preserving CELL_OPT
      ↓
igzo_crystal_ordered_003_r3m_cell_relaxed
      ↓
O001–O004 site enumeration
      ↓
supercell generation
      ↓
4×4×1 PBE neutral-vacancy screening
      ↓
PBE0-TC-LRC validation
      ↓
hybrid defects / charged defects / CTLs
```

Parallel amorphous branch:

```text
crystalline/stoichiometric starting structures
      ↓
CP2K AIMD
      ↓
amorphous IGZO
      ↓
DFT dataset
      ↓
MACE
      ↓
LAMMPS
      ↓
large-scale ensemble
      ↓
amorphous defect statistics
```

---

## Reference Structures

External structures should:

* remain unmodified;
* retain database identifiers;
* retain publication provenance;
* remain separate from derived structures.

Experimental reference:

```text
COD 1521670
```

Canonical derived PBE crystalline reference:

```text
igzo_crystal_ordered_003_r3m_cell_relaxed
```

Secondary low-energy ordering:

```text
igzo_crystal_ordered_001
```

---

## Canonical Crystalline Structure Provenance

The final crystalline reference is generated from the high-precision CP2K R3m CELL_OPT result using:

```text
scripts/structure_generation/extract_cp2k_r3m_reference.py
```

Canonical files:

```text
structures/crystalline/cell_relaxed/
└── igzo_crystal_ordered_003_r3m_cell_relaxed/
    ├── igzo_crystal_ordered_003_r3m_cell_relaxed.xyz
    └── igzo_crystal_ordered_003_r3m_cell_relaxed.cif
```

The large CP2K restart/wavefunction files are not intended for Git.

Production symmetry tolerance:

```text
SYMPREC = 2.0E-3
ANGLE_TOLERANCE = 5.0
```

---

## Oxygen-Site Provenance

Symmetry-inequivalent oxygen sites are generated using:

```text
scripts/structure_generation/enumerate_oxygen_sites.py
```

Stable labels:

```text
O001
O002
O003
O004
```

These labels must remain unchanged across:

* primitive structures;
* supercells;
* vacancy structures;
* CP2K calculations;
* analysis;
* figures;
* datasets.

---

## Vacancy-Structure Provenance

Neutral oxygen vacancies are generated programmatically using:

```text
scripts/structure_generation/generate_oxygen_vacancies.py
```

The generator records:

* site ID;
* local environment;
* removed atom index;
* fractional coordinates;
* Cartesian coordinates;
* supercell;
* pristine atom count;
* defect atom count;
* charge;
* generated filename.

Manual atom deletion should not replace the scripted production workflow.

---

## Production PBE Defect Supercell

Production supercell:

```text
4×4×1
```

Exact CP2K cell:

```text
A  13.486272280000   0.000000000000   0.000000000000
B  -6.743136140000  11.679454396834   0.000000000000
C   0.000000000000   0.000000000000  26.174269630000
```

This is the validated 120° representation.

Pristine atom count:

```text
336
```

Neutral vacancy atom count:

```text
335
```

---

## Production PBE Vacancy Method

The validated screening workflow is:

```text
PBE
TZV2P-MOLOPT-PBE-GTH
GTH-PBE
CUTOFF = 700 Ry
REL_CUTOFF = 60 Ry
Γ-only
OT / DIIS
fixed-cell BFGS GEO_OPT
```

Γ-only OT calculations omit an explicit `&KPOINTS` block.

Production inputs explicitly include:

```text
&MGRID
&QS
&POISSON
```

with the validated numerical parameters.

---

## Validation Calculations

O001 validation calculations must remain identifiable separately from production results.

Current validation set:

```text
3x3x1/O001/q0/pbe_2x2x1
3x3x1/O001/q0/pbe_gamma
3x3x1/O001/q0/pbe_gamma_ot
4x4x1/O001/q0/pbe_gamma_ot
```

The 3×3×1 Γ diagonalisation and Γ OT calculations reproduce essentially identical local reconstructions.

The 3×3×1 2×2×1 diagonalisation calculation finds a different local reconstruction.

These calculations are validation evidence and should not be mixed into the production O001–O004 ranking without explicit methodological labelling.

---

## Relaxation Analysis

Vacancy relaxation analysis is performed using:

```text
scripts/analysis/analyse_vacancy_relaxation.py
```

The analysis records:

* missing oxygen;
* vacancy coordinate;
* atomic displacements;
* radial displacement relative to vacancy;
* first-shell reconstruction;
* element-resolved first-shell behaviour;
* relaxation localisation;
* relaxed CIF;
* relaxed XYZ;
* displacement figure;
* text summary.

The exact supercell representation used by the corresponding CP2K calculation must be respected during periodic analysis.

---

## Current CP2K Environments

Local development:

```text
CP2K 2026.2
WSL2
```

ARCHER2 production:

```text
CP2K 2025.2
```

Basis/potential data-file names differ between environments and should be recorded.

---

## Calculation Metadata

Production calculations should record:

* calculation ID;
* structure ID;
* site ID where applicable;
* charge;
* multiplicity;
* functional;
* basis sets;
* pseudopotentials;
* CUTOFF;
* REL_CUTOFF;
* k-point sampling;
* SCF solver;
* geometry optimiser;
* software version;
* HPC environment;
* scheduler job ID;
* parent calculation;
* restart parent if applicable;
* convergence status;
* final energy.

---

## PBE0-TC-LRC Provenance

Hybrid calculations must be clearly distinguished from PBE screening.

The hybrid provenance chain will be:

```text
PBE R3m reference
      ↓
PBE0-TC-LRC validation single point
      ↓
PBE0-TC-LRC R3m CELL_OPT
      ↓
canonical hybrid pristine reference
      ↓
hybrid supercell generation
      ↓
hybrid defects
```

Hybrid defect supercells must be generated from the hybrid-optimised pristine lattice rather than silently reusing the PBE lattice.

All hybrid-specific parameters must be recorded explicitly.

---

## Random Processes

Record random seeds for:

* AIMD initial velocities;
* stochastic thermostats;
* MACE dataset splitting;
* MACE training;
* structural sampling.

---

## Software Environments

Version important dependencies:

* CP2K;
* VASP;
* ASE;
* pymatgen;
* NumPy;
* pandas;
* SciPy;
* matplotlib;
* MACE;
* LAMMPS;
* AiiDA.

---

## HPC Metadata

Record:

* machine;
* partition;
* nodes;
* CPU cores;
* GPUs where relevant;
* memory where relevant;
* walltime;
* modules/environment;
* scheduler;
* job ID.

Job IDs must not be embedded in permanent structure names.

---

## Git

Git should track:

* source code;
* workflow definitions;
* input-generation scripts;
* analysis scripts;
* documentation;
* metadata;
* reference structures;
* generated starting structures;
* curated relaxed structures;
* selected small numerical results;
* figures where appropriate.

Git should not serve as bulk simulation storage.

---

## Large Data

Keep large files on HPC or appropriate research storage.

Examples:

* CP2K `*.kp` files;
* wavefunction restart files;
* restart histories;
* large raw trajectories;
* large DFT outputs;
* AIMD trajectories;
* MACE datasets;
* checkpoints;
* LAMMPS trajectories.

Curated structures, summary tables and selected figures may be retained in Git.

---

## Directory Roles

Use the following conceptual separation:

```text
structures/
```

Canonical starting structures and curated final structures.

```text
calculations/
```

Calculation inputs and selected calculation-level files.

```text
results/
```

Processed tables, summaries and figures.

```text
scripts/
```

Generation, input-generation and analysis code.

```text
docs/
```

Scientific methodology, provenance and project decisions.

Raw HPC storage remains separate from the Git repository where files are too large for version control.

---

## Reproducing the PBE Crystalline Reference

A complete reproduction requires:

```text
COD 1521670
+
generate_igzo_orderings.py
+
ordered structure files
+
CP2K convergence parameters
+
ARCHER2 GEO_OPT inputs
+
CELL_OPT inputs
+
tight EPS_SCF = 1E-7 calculations
+
symmetry analysis
+
extract_cp2k_r3m_reference.py
+
results-log.md
```

---

## Reproducing the PBE Vacancy Screening

A complete reproduction requires:

```text
canonical R3m reference
+
enumerate_oxygen_sites.py
+
generate_oxygen_vacancies.py
+
4×4×1 production cell
+
validated Γ+OT CP2K parameters
+
O001–O004 starting structures
+
CP2K GEO_OPT inputs
+
final trajectories/structures
+
analyse_vacancy_relaxation.py
+
energy-analysis workflow
+
results-log.md
```

---

## AiiDA

AiiDA should progressively provide:

* calculation provenance;
* parent-child relationships;
* workflow automation;
* metadata persistence;
* high-throughput defect calculations.

AiiDA should complement Git rather than replace it.

---

## Reproducing a Future Result

A significant result should ideally be reproducible from:

```text
structure ID
+
provenance
+
workflow version
+
computational parameters
+
software version
+
analysis code
+
dataset/model version
``