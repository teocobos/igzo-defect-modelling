# Methodology

This document describes the computational methodology for the IGZO
defect-modelling project.

Validated methods are recorded as completed workflow decisions; future
methods remain explicitly identified as planned.

---

## 1. Experimental Crystalline Reference

The crystalline reference composition is stoichiometric InGaZnO4.

The primary experimental crystallographic structure is:

**Crystallography Open Database — COD 1521670**

The original CIF is retained unchanged under:

    structures/crystalline/reference/

The experimental structure contains mixed Ga/Zn occupancy and therefore
represents an average crystallographic model rather than an explicit
ordered atomistic DFT structure.

---

## 2. Ga/Zn Ordering

The mixed Ga/Zn crystallographic sites were converted into explicit
ordered configurations.

For the current 21-atom conventional cell, six mixed positions must be
occupied by:

    3 Ga
    3 Zn

giving:

    C(6,3) = 20

raw assignments.

Symmetry-equivalent configurations were removed before first-principles
screening, producing four symmetry-distinct ordered candidate
structures.

Structure generation was performed programmatically using:

    scripts/structure_generation/generate_igzo_orderings.py

Manual editing of the experimental CIF is avoided.

---

## 3. Crystalline Model Selection

All four ordered 21-atom models were geometry optimised consistently
using CP2K.

Validated crystalline setup:

- PBE;
- TZV2P-MOLOPT-PBE-GTH;
- matching GTH-PBE pseudopotentials;
- CUTOFF = 700 Ry;
- REL_CUTOFF = 60 Ry;
- 6×6×1 Monkhorst–Pack k-point mesh;
- fixed experimental cell;
- BFGS geometry optimisation on ARCHER2;
- geometry-optimisation EPS_SCF = 1e-6;
- final single-point EPS_SCF = 1e-7.

Relative energies are reported per InGaZnO4 formula unit.

The final tight-energy ordering is:

    ordered_003 < ordered_001 << ordered_002 < ordered_004

`ordered_003` is the primary crystalline reference. `ordered_001` is
retained as a near-degenerate alternative ordering.

---

## 4. CP2K Numerical Validation

Initial convergence work was performed locally with CP2K 2026.2.
Production ordered-structure calculations were completed on ARCHER2
with CP2K 2025.2.

The following quantities were systematically assessed:

- basis-set quality;
- CUTOFF;
- REL_CUTOFF;
- SCF strategy;
- k-point sampling.

The current crystalline production parameters are documented in
`docs/computational-parameters.md`.

Local fixed-geometry SCF benchmarking found Pulay mixing to be fast, but
geometry-optimisation development under WSL encountered Pulay/runtime
instabilities. Production ARCHER2 geometry optimisation therefore used
Broyden mixing with:

    ALPHA = 0.10
    BETA = 1.5
    NBUFFER = 4

No unconverged SCF cycles are accepted for production geometry
optimisation.

---

## 5. Relaxed-Structure Analysis

The two lowest-energy structures, `ordered_001` and `ordered_003`, were
compared using:

- crystallographic symmetry analysis;
- pymatgen StructureMatcher;
- cation–oxygen coordination analysis;
- site-resolved bond-length distributions;
- bond-length distortion indices;
- coordination-polyhedron angular deviations; and
- oxygen-vertex convex-hull polyhedral volumes.

Both structures retain:

- InO6 coordination;
- GaO5 coordination;
- ZnO4 coordination.

The GaO5 environments are classified as trigonal bipyramidal by the
current angular comparison.

`ordered_003` retains R3m symmetry and exhibits highly uniform
symmetry-related cation environments. It also has a substantially
narrower Zn–O bond-length distribution than `ordered_001`, although it
is not less distorted in every metric.

---

## 6. VASP

VASP remains a complementary first-principles workflow once the required
computational environment is available.

Planned applications include:

- crystalline electronic-structure cross-checks;
- band structure;
- density of states;
- projected density of states;
- oxygen-vacancy calculations;
- defect formation energies; and
- charged defects where appropriate.

Cross-code comparisons should use equivalent physical approximations
where practical.

---

## 7. Crystalline Oxygen Vacancies

Oxygen vacancies will initially be investigated in relaxed
`ordered_003`.

The workflow is:

    relaxed ordered_003
            ↓
    identify symmetry-inequivalent oxygen sites
            ↓
    record multiplicities/local coordination
            ↓
    generate vacancy structures
            ↓
    construct and validate defect supercells
            ↓
    reconverge k-point sampling as required
            ↓
    geometry optimisation
            ↓
    defect energetics
            ↓
    relevant charge states
            ↓
    electronic/local structural analysis

Symmetry will be used to avoid unnecessary duplicate calculations.

The 21-atom cell will not automatically be treated as a converged defect
cell. Supercell size and defect–defect interaction must be assessed
before production vacancy energetics are interpreted.

A subset of defects may later be repeated in `ordered_001` to test
sensitivity to cation ordering.

---

## 8. CP2K Amorphisation

Amorphous IGZO will initially be generated using first-principles
molecular dynamics.

The amorphous starting cell will be designed to be approximately
isotropic where practical rather than obtained by blindly replicating
the highly elongated crystalline conventional cell.

Intended workflow:

    stoichiometric near-isotropic cell
          ↓
    equilibration
          ↓
    heating
          ↓
    liquid equilibration
          ↓
    quench
          ↓
    low-temperature equilibration
          ↓
    geometry optimisation
          ↓
    amorphous IGZO

Parameters still requiring validation include:

- initial cell size and atom count;
- target density;
- timestep;
- ensemble;
- thermostat;
- melt temperature;
- melt duration;
- quench rate;
- final temperature;
- equilibration duration.

Multiple independent trajectories should be generated.

---

## 9. Amorphous Structure Validation

Generated structures will be evaluated using:

- density;
- total/partial radial distribution functions;
- coordination distributions;
- bond lengths;
- bond angles;
- local polyhedra;
- ring statistics where appropriate.

Results should be compared with available experimental and computational
literature.

---

## 10. MACE Dataset Generation

First-principles configurations will be selected to represent the
configuration space required by the potential.

Potential classes include:

- relaxed crystalline structures;
- strained/thermally distorted crystalline structures;
- crystalline defect structures;
- melt/liquid/quench configurations;
- amorphous structures;
- amorphous defect environments where required.

Reference energies, forces and stresses should be retained where
appropriate.

Highly correlated consecutive AIMD frames should not dominate the
dataset.

---

## 11. MACE Training and Validation

Datasets will be divided into training, validation and independent test
sets.

Validation should consider:

- energy MAE/RMSE;
- force MAE/RMSE;
- stress errors where applicable;
- structural properties;
- energetic ordering;
- molecular-dynamics stability;
- unseen configurations and extrapolation.

Numerical test-set accuracy alone is insufficient to establish
production suitability.

---

## 12. LAMMPS Sampling

Following validation, MACE will be used with LAMMPS for larger-scale
molecular dynamics.

This will enable:

- larger simulation cells;
- longer trajectories;
- independent melt-quench simulations;
- structural ensemble generation;
- statistical sampling of local environments.

Representative configurations may subsequently be returned to
first-principles calculations for validation.

---

## 13. Statistical Defect Sampling

The large amorphous ensemble will provide oxygen environments spanning
different:

- coordination numbers;
- cation neighbours;
- bond lengths;
- bond angles;
- local densities;
- structural motifs.

Representative oxygen sites will be selected for vacancy calculations.

The objective is to obtain distributions of defect properties rather
than rely on a single amorphous vacancy configuration.

---

## 14. Analysis

Analysis primarily uses Python together with:

- NumPy;
- pandas;
- SciPy;
- ASE;
- pymatgen;
- matplotlib.

Important analysis should be reproducible from scripts wherever
practical.

---

## Overall Methodology

    COD 1521670
          ↓
    experimental average structure
          ↓
    explicit Ga/Zn ordering
          ↓
    four ordered candidates
          ↓
    converged CP2K relaxation + tight energies
          ↓
    ordered_003 crystalline reference
       ┌───────────────┴───────────────┐
       ↓                               ↓
    crystalline defects            CP2K AIMD
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
                                vacancy statistics
                                       ↓
                           structural/electronic conclusions
