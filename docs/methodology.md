
---

# 4. `docs/methodology.md`

This is particularly important for your project because it records **why** you're using VASP, CP2K, MACE and LAMMPS rather than simply listing them.

```markdown
# Computational Methodology

## 1. General Principle

Each computational method should have a defined scientific purpose.

### VASP

Primary role:

- Crystalline IGZO reference calculations.
- High-quality electronic-structure calculations.
- Selected defect calculations.

### CP2K

Primary role:

- DFT molecular dynamics.
- Melt-quench simulations.
- Amorphous IGZO reference configurations.
- DFT validation of ML-generated structures.

### MACE

Primary role:

- Learning the IGZO potential-energy surface from DFT data.
- Accelerating atomistic sampling after validation.

### LAMMPS

Primary role:

- Large-scale molecular dynamics using a validated interatomic potential.
- Longer and larger simulations than practical with direct DFT.

### AiiDA

Primary role:

- Workflow automation.
- Provenance.
- Reproducibility.
- High-throughput defect calculations.

---

## 2. DFT Methodology

The following parameters must be established through convergence testing rather than assumed.

| Parameter | Planned Value | Status |
|---|---|---|
| Exchange-correlation functional | TBD | Not established |
| Hubbard U | TBD | To assess |
| VASP PAW datasets | TBD | To establish |
| Plane-wave cutoff | TBD | Convergence required |
| k-point mesh | TBD | Convergence required |
| Electronic convergence | TBD | Convergence required |
| Ionic convergence | TBD | Convergence required |
| Spin treatment | TBD | To assess |
| Supercell size | TBD | Convergence required |

---

## 3. Cross-Code Validation

VASP and CP2K use different electronic-structure implementations.

Direct comparison of absolute energies should therefore be avoided unless methodological consistency has been established.

A small benchmark set should be calculated using both codes.

Compare:

- Optimised geometry.
- Relative structural energies.
- Forces where appropriate.
- DOS/PDOS where meaningful.
- Band-gap trends.

Document differences in:

- Basis sets.
- Pseudopotentials.
- Cutoffs.
- Numerical settings.

---

## 4. Oxygen-Vacancy Methodology

For an oxygen vacancy:

V_O

the formation energy should be calculated using an explicitly documented thermodynamic convention.

For charge state q:

E_f(D^q) = E_defect^q - E_bulk - Σ_i n_i μ_i + q(E_F + E_VBM) + E_corr

The exact convention, chemical potentials and correction methodology must be documented before production calculations.

---

## 5. Amorphous Modelling

Amorphous structures should be generated using multiple independent configurations to avoid conclusions based on a single structural realisation.

The melt-quench protocol must document:

- Initial structure.
- Number of atoms.
- Density.
- Initial temperature.
- Maximum temperature.
- Liquid equilibration time.
- Quench rate.
- Final temperature.
- Ensemble.
- Time step.
- Thermostat/barostat.
- Number of independent seeds.

---

## 6. ML Potential Validation

MACE models should not be used for scientific conclusions until validated against an independent DFT test set.

At minimum, report:

- Energy MAE/RMSE.
- Force MAE/RMSE.
- Stress errors if relevant.
- Structural stability.
- Representative extrapolation behaviour.

Training and validation sets must remain separate.

---

## 7. Data Management

Large raw files should not be committed to GitHub.

Examples:

- VASP WAVECAR.
- Large CHGCAR files.
- OUTCAR files from production calculations.
- Long AIMD trajectories.
- Large LAMMPS trajectories.
- Large MACE datasets/checkpoints.

Large datasets should instead be archived using appropriate research-data storage.

---

## 8. Reproducibility

Every production result should be traceable to:

- Structure.
- Code and version.
- Input parameters.
- Pseudopotential/basis information.
- Workflow.
- Analysis script.
- Data provenance.

Methodological changes should be recorded in Git history and documented here where significant.