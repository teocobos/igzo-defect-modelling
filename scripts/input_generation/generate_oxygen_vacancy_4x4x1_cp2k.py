#!/usr/bin/env python3

"""
Generate production CP2K PBE Gamma+OT GEO_OPT inputs for neutral
oxygen vacancies O002-O004 in the crystalline R3m IGZO 4x4x1 supercell.

The calculation methodology reproduces the validated O001 production setup:

    PBE
    TZV2P-MOLOPT-PBE-GTH
    GTH-PBE
    GPW
    CUTOFF 700 Ry
    REL_CUTOFF 60 Ry
    Gamma only
    OT / DIIS
    fixed-cell BFGS GEO_OPT
    EPS_SCF 1e-6

The exact validated 120-degree 4x4x1 production cell is used explicitly.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

from pymatgen.core import Lattice, Structure


# =============================================================================
# PATHS
# =============================================================================

ROOT = Path(__file__).resolve().parents[2]

STRUCTURE_ROOT = (
    ROOT
    / "structures"
    / "crystalline"
    / "defects"
    / "oxygen_vacancies"
    / "4x4x1"
)

CALC_ROOT = (
    ROOT
    / "calculations"
    / "crystalline"
    / "defects"
    / "oxygen_vacancies"
    / "4x4x1"
)


# =============================================================================
# PRODUCTION CELL
# =============================================================================

PRODUCTION_LATTICE = Lattice(
    [
        [
            13.486272280000,
            0.000000000000,
            0.000000000000,
        ],
        [
            -6.743136140000,
            11.679454396834,
            0.000000000000,
        ],
        [
            0.000000000000,
            0.000000000000,
            26.174269630000,
        ],
    ]
)


# =============================================================================
# DEFECTS
# =============================================================================

DEFECTS = [
    "O002",
    "O003",
    "O004",
]


# =============================================================================
# XYZ WRITER
# =============================================================================

def write_xyz(
    filename: Path,
    structure: Structure,
    comment: str,
):
    """
    Write an XYZ coordinate file.
    """

    with filename.open("w") as handle:

        handle.write(
            f"{len(structure)}\n"
        )

        handle.write(
            f"{comment}\n"
        )

        for site in structure:

            x, y, z = site.coords

            handle.write(
                f"{site.specie.symbol:2s} "
                f"{x:18.10f} "
                f"{y:18.10f} "
                f"{z:18.10f}\n"
            )


# =============================================================================
# CELL REMAPPING
# =============================================================================

def remap_to_production_cell(
    structure: Structure,
) -> Structure:
    """
    Preserve fractional coordinates but express the structure using the exact
    validated 120-degree CP2K production lattice.

    This avoids any ambiguity between equivalent 60-degree and 120-degree
    hexagonal cell representations.
    """

    fractional_coordinates = np.array(
        structure.frac_coords,
        dtype=float,
    )

    fractional_coordinates %= 1.0

    species = [
        site.specie
        for site in structure
    ]

    return Structure(
        PRODUCTION_LATTICE,
        species,
        fractional_coordinates,
        coords_are_cartesian=False,
        to_unit_cell=True,
    )


# =============================================================================
# CP2K INPUT
# =============================================================================

def build_cp2k_input(
    project_name: str,
    xyz_filename: str,
) -> str:

    return f"""&GLOBAL
  PROJECT {project_name}
  RUN_TYPE GEO_OPT
  PRINT_LEVEL MEDIUM
&END GLOBAL

&FORCE_EVAL
  METHOD Quickstep

  &DFT
    BASIS_SET_FILE_NAME BASIS_MOLOPT_UZH
    POTENTIAL_FILE_NAME POTENTIAL_UZH

    CHARGE 0
    MULTIPLICITY 1

    &MGRID
      CUTOFF 700
      REL_CUTOFF 60
    &END MGRID

    &QS
      METHOD GPW
      EPS_PGF_ORB 1.0E-18
      EPS_FILTER_MATRIX 0.0
    &END QS

    &POISSON
      PERIODIC XYZ
    &END POISSON

    &SCF
      EPS_SCF 1.0E-6
      MAX_SCF 150
      SCF_GUESS ATOMIC

      &OT
        MINIMIZER DIIS
        PRECONDITIONER FULL_SINGLE_INVERSE
      &END OT

      &OUTER_SCF
        MAX_SCF 20
        EPS_SCF 1.0E-6
      &END OUTER_SCF

    &END SCF

    &XC
      &XC_FUNCTIONAL PBE
      &END XC_FUNCTIONAL
    &END XC

  &END DFT

  &SUBSYS

    &CELL
      A 13.486272280000 0.000000000000 0.000000000000
      B -6.743136140000 11.679454396834 0.000000000000
      C 0.000000000000 0.000000000000 26.174269630000
      PERIODIC XYZ
    &END CELL

    &TOPOLOGY
      COORD_FILE_NAME {xyz_filename}
      COORD_FILE_FORMAT XYZ
    &END TOPOLOGY

    &KIND In
      ELEMENT In
      BASIS_SET TZV2P-MOLOPT-PBE-GTH-q13
      POTENTIAL GTH-PBE-q13
    &END KIND

    &KIND Ga
      ELEMENT Ga
      BASIS_SET TZV2P-MOLOPT-PBE-GTH-q13
      POTENTIAL GTH-PBE-q13
    &END KIND

    &KIND Zn
      ELEMENT Zn
      BASIS_SET TZV2P-MOLOPT-PBE-GTH-q12
      POTENTIAL GTH-PBE-q12
    &END KIND

    &KIND O
      ELEMENT O
      BASIS_SET TZV2P-MOLOPT-PBE-GTH-q6
      POTENTIAL GTH-PBE-q6
    &END KIND

  &END SUBSYS

&END FORCE_EVAL


&MOTION

  &GEO_OPT
    TYPE MINIMIZATION
    OPTIMIZER BFGS
  &END GEO_OPT

  &PRINT

    &TRAJECTORY
      FORMAT XYZ

      &EACH
        GEO_OPT 1
      &END EACH

    &END TRAJECTORY

    &RESTART
      BACKUP_COPIES 3

      &EACH
        GEO_OPT 1
      &END EACH

    &END RESTART

    &RESTART_HISTORY

      &EACH
        GEO_OPT 1
      &END EACH

    &END RESTART_HISTORY

  &END PRINT

&END MOTION
"""


# =============================================================================
# MAIN
# =============================================================================

def main():

    print("=" * 80)
    print("4x4x1 IGZO NEUTRAL OXYGEN-VACANCY CP2K INPUT GENERATION")
    print("=" * 80)

    print()
    print("Production methodology:")
    print("  Functional       : PBE")
    print("  Basis            : TZV2P-MOLOPT-PBE-GTH")
    print("  Cutoff           : 700 Ry")
    print("  Relative cutoff  : 60 Ry")
    print("  Sampling         : Gamma only")
    print("  SCF solver       : OT / DIIS")
    print("  Geometry         : fixed-cell BFGS GEO_OPT")
    print("  Charge           : 0")
    print("  Multiplicity     : 1")

    print()
    print("Production cell:")
    print(
        "  A = "
        "13.486272280000 "
        "0.000000000000 "
        "0.000000000000"
    )
    print(
        "  B = "
        "-6.743136140000 "
        "11.679454396834 "
        "0.000000000000"
    )
    print(
        "  C = "
        "0.000000000000 "
        "0.000000000000 "
        "26.174269630000"
    )

    for label in DEFECTS:

        label_lower = label.lower()

        source_cif = (
            STRUCTURE_ROOT
            / label
            / "q0"
            / (
                f"igzo_r3m_4x4x1_vo_"
                f"{label_lower}_q0.cif"
            )
        )

        if not source_cif.exists():
            raise FileNotFoundError(
                f"\nMissing defect structure:\n{source_cif}\n\n"
                "Run generate_oxygen_vacancies.py "
                "--supercell 4x4x1 first."
            )

        structure = Structure.from_file(
            source_cif
        )

        if len(structure) != 335:
            raise RuntimeError(
                f"{label}: expected 335 atoms but found "
                f"{len(structure)}."
            )

        structure = remap_to_production_cell(
            structure
        )

        output_dir = (
            CALC_ROOT
            / label
            / "q0"
            / "pbe_gamma_ot"
        )

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        xyz_filename = (
            f"igzo_r3m_4x4x1_vo_"
            f"{label_lower}_q0.xyz"
        )

        xyz_file = (
            output_dir
            / xyz_filename
        )

        project_name = (
            f"igzo_r3m_4x4x1_vo_"
            f"{label_lower}_q0_pbe_gamma_ot"
        )

        input_filename = (
            f"{project_name}.inp"
        )

        input_file = (
            output_dir
            / input_filename
        )

        write_xyz(
            xyz_file,
            structure,
            (
                f"Neutral {label} oxygen vacancy "
                f"in R3m IGZO 4x4x1"
            ),
        )

        input_text = build_cp2k_input(
            project_name,
            xyz_filename,
        )

        input_file.write_text(
            input_text
        )

        print()
        print("-" * 80)
        print(label)
        print("-" * 80)

        print(
            f"  Source CIF : {source_cif}"
        )

        print(
            f"  Atoms      : {len(structure)}"
        )

        print(
            f"  XYZ        : {xyz_file}"
        )

        print(
            f"  CP2K input : {input_file}"
        )

    print()
    print("=" * 80)
    print("COMPLETE")
    print("=" * 80)

    print()
    print(
        "Generated production PBE Gamma+OT GEO_OPT inputs "
        "for O002-O004."
    )


if __name__ == "__main__":
    main()