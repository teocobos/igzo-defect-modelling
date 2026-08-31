#!/usr/bin/env python3

"""
Generate a pristine 4x4x1 crystalline IGZO Gamma-point CP2K ENERGY
calculation.

Purpose
-------
Compare:

    3x3x1 + 2x2x1 k-points

against:

    4x4x1 + Gamma

to determine whether increasing the real-space supercell permits
Gamma-only sampling for subsequent defect and hybrid-DFT calculations.

Common electronic-structure settings are retained from the converged
crystalline workflow.
"""

from pathlib import Path

from pymatgen.core import Structure
from pymatgen.io.xyz import XYZ


ROOT = Path(__file__).resolve().parents[2]

INPUT_CIF = (
    ROOT
    / "structures"
    / "crystalline"
    / "supercells"
    / "igzo_r3m_4x4x1"
    / "igzo_r3m_4x4x1.cif"
)

OUTPUT_DIR = (
    ROOT
    / "calculations"
    / "crystalline"
    / "defects"
    / "oxygen_vacancies"
    / "4x4x1"
    / "pristine"
    / "gamma"
)

XYZ_FILE = (
    OUTPUT_DIR
    / "igzo_r3m_4x4x1.xyz"
)

INPUT_FILE = (
    OUTPUT_DIR
    / "igzo_r3m_4x4x1_pbe_gamma.inp"
)


def main():

    if not INPUT_CIF.exists():
        raise FileNotFoundError(
            f"4x4x1 pristine CIF not found:\n{INPUT_CIF}"
        )

    structure = Structure.from_file(INPUT_CIF)

    if len(structure) != 336:
        raise RuntimeError(
            f"Expected 336 atoms but found {len(structure)}."
        )

    expected = {
        "In": 48,
        "Ga": 48,
        "Zn": 48,
        "O": 192,
    }

    for element, count in expected.items():

        actual = int(
            structure.composition[element]
        )

        if actual != count:
            raise RuntimeError(
                f"Expected {count} {element} atoms "
                f"but found {actual}."
            )

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    # ---------------------------------------------------------------
    # Coordinates
    # ---------------------------------------------------------------

    XYZ(structure).write_file(
        XYZ_FILE
    )

    # ---------------------------------------------------------------
    # Cell
    # ---------------------------------------------------------------

    a = structure.lattice.matrix[0]
    b = structure.lattice.matrix[1]
    c = structure.lattice.matrix[2]

    # ---------------------------------------------------------------
    # CP2K input
    # ---------------------------------------------------------------

    cp2k_input = f"""&GLOBAL
  PROJECT igzo_r3m_4x4x1_pbe_gamma
  RUN_TYPE ENERGY
  PRINT_LEVEL MEDIUM
&END GLOBAL

&FORCE_EVAL
  METHOD Quickstep

  &DFT
    BASIS_SET_FILE_NAME BASIS_MOLOPT_UZH
    POTENTIAL_FILE_NAME POTENTIAL_UZH

    CHARGE 0
    MULTIPLICITY 1

    &SCF
      EPS_SCF 1.0E-7
      MAX_SCF 200
      SCF_GUESS ATOMIC

      ADDED_MOS 40

      &DIAGONALIZATION
        ALGORITHM STANDARD
      &END DIAGONALIZATION

      &MIXING
        METHOD BROYDEN_MIXING
        ALPHA 0.10
        BETA 1.5
        NBUFFER 4
      &END MIXING

      &SMEAR
        METHOD FERMI_DIRAC
        ELECTRONIC_TEMPERATURE 300
      &END SMEAR

    &END SCF

    &XC
      &XC_FUNCTIONAL PBE
      &END XC_FUNCTIONAL
    &END XC

    &KPOINTS
      SCHEME GAMMA
    &END KPOINTS

  &END DFT

  &SUBSYS

    &CELL
      A {a[0]:.12f} {a[1]:.12f} {a[2]:.12f}
      B {b[0]:.12f} {b[1]:.12f} {b[2]:.12f}
      C {c[0]:.12f} {c[1]:.12f} {c[2]:.12f}
      PERIODIC XYZ
    &END CELL

    &TOPOLOGY
      COORD_FILE_NAME igzo_r3m_4x4x1.xyz
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
"""

    INPUT_FILE.write_text(
        cp2k_input
    )

    print("=" * 80)
    print("4x4x1 PRISTINE GAMMA-POINT INPUT GENERATED")
    print("=" * 80)

    print()
    print(f"Atoms:   {len(structure)}")
    print(f"Formula: {structure.composition.formula}")
    print("Formula units: 48")

    print()
    print("Lattice:")
    print(
        f"a = {structure.lattice.a:.6f} Å"
    )
    print(
        f"b = {structure.lattice.b:.6f} Å"
    )
    print(
        f"c = {structure.lattice.c:.6f} Å"
    )
    print(
        f"gamma = {structure.lattice.gamma:.6f} deg"
    )

    print()
    print("Cell vectors:")
    print(
        f"A = {a[0]:.8f} {a[1]:.8f} {a[2]:.8f}"
    )
    print(
        f"B = {b[0]:.8f} {b[1]:.8f} {b[2]:.8f}"
    )
    print(
        f"C = {c[0]:.8f} {c[1]:.8f} {c[2]:.8f}"
    )

    print()
    print("K-point sampling:")
    print("  Gamma only")

    print()
    print("Written:")
    print(f"  {XYZ_FILE}")
    print(f"  {INPUT_FILE}")


if __name__ == "__main__":
    main()