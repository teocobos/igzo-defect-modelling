#!/usr/bin/env python3

"""
Generate pristine 3x3x1 crystalline IGZO CP2K reference calculations
for k-point convergence testing.

Outputs
-------
1. XYZ coordinates for the pristine 189-atom supercell.
2. PBE Gamma-point ENERGY input.
3. PBE 2x2x1 k-point ENERGY input.

Common settings
---------------
- PBE
- TZV2P-MOLOPT-PBE-GTH
- GTH-PBE pseudopotentials
- CUTOFF 700 Ry
- REL_CUTOFF 60 Ry
- Broyden mixing
- Fermi-Dirac smearing at 300 K
- ADDED_MOS 40
- EPS_SCF 1e-7

The Gamma and 2x2x1 calculations differ ONLY in the KPOINTS block.
"""

from pathlib import Path

from pymatgen.core import Structure
from pymatgen.io.xyz import XYZ


ROOT = Path(__file__).resolve().parents[2]

INPUT_CIF = (
    ROOT
    / "structures"
    / "crystalline"
    / "defects"
    / "oxygen_vacancies"
    / "3x3x1"
    / "pristine"
    / "igzo_r3m_3x3x1.cif"
)

OUTPUT_DIR = (
    ROOT
    / "calculations"
    / "crystalline"
    / "defects"
    / "oxygen_vacancies"
    / "3x3x1"
    / "pristine"
)

XYZ_FILE = OUTPUT_DIR / "igzo_r3m_3x3x1.xyz"

GAMMA_INPUT = (
    OUTPUT_DIR
    / "igzo_r3m_3x3x1_pbe_gamma.inp"
)

KPOINT_INPUT = (
    OUTPUT_DIR
    / "igzo_r3m_3x3x1_pbe_2x2x1.inp"
)


def build_cp2k_input(
    structure,
    project_name,
    kpoints_block,
):
    """
    Return a complete CP2K ENERGY input string.
    """

    a = structure.lattice.matrix[0]
    b = structure.lattice.matrix[1]
    c = structure.lattice.matrix[2]

    return f"""&GLOBAL
  PROJECT {project_name}
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

{kpoints_block}

  &END DFT

  &SUBSYS

    &CELL
      A {a[0]:.12f} {a[1]:.12f} {a[2]:.12f}
      B {b[0]:.12f} {b[1]:.12f} {b[2]:.12f}
      C {c[0]:.12f} {c[1]:.12f} {c[2]:.12f}
      PERIODIC XYZ
    &END CELL

    &TOPOLOGY
      COORD_FILE_NAME igzo_r3m_3x3x1.xyz
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


def main():

    if not INPUT_CIF.exists():
        raise FileNotFoundError(
            f"Pristine CIF not found:\n{INPUT_CIF}"
        )

    structure = Structure.from_file(INPUT_CIF)

    if len(structure) != 189:
        raise RuntimeError(
            f"Expected 189 atoms but found {len(structure)}."
        )

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    # ---------------------------------------------------------------
    # Coordinate file
    # ---------------------------------------------------------------

    XYZ(structure).write_file(XYZ_FILE)

    # ---------------------------------------------------------------
    # Gamma input
    # ---------------------------------------------------------------

    gamma_block = """    &KPOINTS
      SCHEME GAMMA
    &END KPOINTS"""

    gamma_input = build_cp2k_input(
        structure=structure,
        project_name="igzo_r3m_3x3x1_pbe_gamma",
        kpoints_block=gamma_block,
    )

    GAMMA_INPUT.write_text(gamma_input)

    # ---------------------------------------------------------------
    # 2x2x1 input
    # ---------------------------------------------------------------

    kpoint_block = """    &KPOINTS
      SCHEME MONKHORST-PACK 2 2 1
      FULL_GRID TRUE
    &END KPOINTS"""

    kpoint_input = build_cp2k_input(
        structure=structure,
        project_name="igzo_r3m_3x3x1_pbe_2x2x1",
        kpoints_block=kpoint_block,
    )

    KPOINT_INPUT.write_text(kpoint_input)

    # ---------------------------------------------------------------
    # Report
    # ---------------------------------------------------------------

    a = structure.lattice.matrix[0]
    b = structure.lattice.matrix[1]
    c = structure.lattice.matrix[2]

    print("=" * 80)
    print("PRISTINE 3x3x1 PBE K-POINT TEST GENERATED")
    print("=" * 80)

    print()
    print(f"Atoms:   {len(structure)}")
    print(f"Formula: {structure.composition.formula}")

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
    print("Generated calculations:")
    print("  1. Gamma-only")
    print("  2. 2x2x1 Monkhorst-Pack")

    print()
    print("Written:")
    print(f"  {XYZ_FILE}")
    print(f"  {GAMMA_INPUT}")
    print(f"  {KPOINT_INPUT}")


if __name__ == "__main__":
    main()