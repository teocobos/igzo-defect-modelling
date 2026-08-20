# Reproducibility

## Principles

The project should be reproducible from version-controlled inputs, scripts and documented computational settings.

## Commit

- Input files.
- Small structures.
- Analysis scripts.
- Lightweight tables.
- Figures.
- Documentation.
- Environment specifications.

## Do Not Normally Commit

- VASP WAVECAR/CHGCAR.
- Large OUTCAR files.
- Large AIMD trajectories.
- Large LAMMPS trajectories.
- Large MACE checkpoints.
- Temporary HPC files.

## Provenance

Each production result should follow:

structure
    ↓
calculation input
    ↓
workflow
    ↓
raw output
    ↓
analysis
    ↓
figure/table

## Data Archival

Large datasets should be stored in appropriate research-data storage or an institutional archive, with the repository containing metadata and retrieval instructions.