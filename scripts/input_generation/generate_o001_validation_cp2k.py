#!/usr/bin/env python3

"""
Generate O001 neutral oxygen-vacancy validation calculations for crystalline IGZO.

Calculations generated
----------------------
1. 3x3x1 supercell
   - 188 atoms
   - neutral O001 vacancy
   - PBE
   - 2x2x1 Monkhorst-Pack
   - diagonalisation
   - fixed-cell GEO_OPT

2. 4x4x1 supercell
   - 335 atoms
   - neutral O001 vacancy
   - PBE
   - Gamma only
   - OT
   - fixed-cell GEO_OPT

The same symmetry-defined O001 oxygen class is used in both cells.

Production numerical settings:
- TZV2P-MOLOPT-PBE-GTH UZH
- GTH-PBE
- CUTOFF 700 Ry
- REL_CUTOFF 60 Ry
- GPW
- EPS_PGF_ORB 1e-18
- EPS_FILTER_MATRIX 0
- periodic XYZ electrostatics
"""

from pathlib import Path

import numpy as np

from pymatgen.core import Structure
from pymatgen.io.xyz import XYZ
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer


ROOT = Path(__file__).resolve().parents[2]

REFERENCE = (
    ROOT
    / "structures"
    / "crystalline"
    / "cell_relaxed"
    / "igzo_crystal_ordered_003_r3m_cell_relaxed"
    / "igzo_crystal_ordered_003_r3m_cell_relaxed.cif"
)

OUTPUT_ROOT = (
    ROOT
    / "calculations"
    / "crystalline"
    / "defects"
    / "oxygen_vacancies"
)

SYMPREC = 2.0e-3
ANGLE_TOLERANCE = 5.0


def identify_oxygen_classes(structure):
    """
    Identify the four symmetry-inequivalent oxygen classes in the
    canonical 21-atom R3m structure.

    Classes are ordered by representative fractional z coordinate,
    corresponding to O001--O004.
    """

    sga = SpacegroupAnalyzer(
        structure,
        symprec=SYMPREC,
        angle_tolerance=ANGLE_TOLERANCE,
    )

    symm = sga.get_symmetrized_structure()

    oxygen_groups = []

    for group in symm.equivalent_indices:

        first = group[0]

        if structure[first].specie.symbol != "O":
            continue

        z = float(structure[first].frac_coords[2] % 1.0)

        oxygen_groups.append(
            {
                "indices": list(group),
                "z": z,
            }
        )

    oxygen_groups.sort(
        key=lambda x: x["z"]
    )

    if len(oxygen_groups) != 4:
        raise RuntimeError(
            f"Expected 4 inequivalent oxygen classes, "
            f"found {len(oxygen_groups)}."
        )

    classes = {}

    for i, group in enumerate(
        oxygen_groups,
        start=1,
    ):
        label = f"O{i:03d}"

        classes[label] = group["indices"]

    return classes


def label_reference_sites(structure, oxygen_classes):
    """
    Add an oxygen_site_id property to the primitive structure.
    """

    labels = []

    lookup = {}

    for label, indices in oxygen_classes.items():

        for index in indices:
            lookup[index] = label

    for index, site in enumerate(structure):

        if site.specie.symbol == "O":
            labels.append(
                lookup[index]
            )
        else:
            labels.append(
                site.specie.symbol
            )

    structure.add_site_property(
        "oxygen_site_id",
        labels,
    )


def choose_central_o001(supercell):
    """
    Select the O001 site nearest to the fractional centre
    (0.5, 0.5, 0.5) using the minimum-image convention.
    """

    centre = np.array(
        [0.5, 0.5, 0.5]
    )

    candidates = []

    for index, site in enumerate(supercell):

        label = site.properties.get(
            "oxygen_site_id"
        )

        if label != "O001":
            continue

        delta = (
            site.frac_coords - centre
        )

        delta -= np.round(delta)

        cart_delta = (
            supercell.lattice
            .get_cartesian_coords(delta)
        )

        distance = np.linalg.norm(
            cart_delta
        )

        candidates.append(
            (
                distance,
                index,
                site.frac_coords.copy(),
                site.coords.copy(),
            )
        )

    if not candidates:
        raise RuntimeError(
            "No O001 sites found in supercell."
        )

    candidates.sort(
        key=lambda x: x[0]
    )

    return candidates[0]


def cell_block(structure):

    matrix = structure.lattice.matrix

    a = matrix[0]
    b = matrix[1]
    c = matrix[2]

    return f"""    &CELL
      A {a[0]:.12f} {a[1]:.12f} {a[2]:.12f}
      B {b[0]:.12f} {b[1]:.12f} {b[2]:.12f}
      C {c[0]:.12f} {c[1]:.12f} {c[2]:.12f}
      PERIODIC XYZ
    &END CELL"""


def common_dft_prefix():

    return """    BASIS_SET_FILE_NAME BASIS_MOLOPT_UZH
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
    &END POISSON"""


def xc_block():

    return """    &XC
      &XC_FUNCTIONAL PBE
      &END XC_FUNCTIONAL
    &END XC"""


def kinds_block():

    return """    &KIND In
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
    &END KIND"""


def geo_opt_block():

    return """&MOTION
  &GEO_OPT
    TYPE MINIMIZATION
    OPTIMIZER BFGS

    MAX_ITER 100

    MAX_DR 3.0E-3
    RMS_DR 1.5E-3

    MAX_FORCE 4.5E-4
    RMS_FORCE 3.0E-4
  &END GEO_OPT
&END MOTION"""


def make_3x3x1_input(structure, xyz_name):

    return f"""&GLOBAL
  PROJECT igzo_r3m_3x3x1_vo_o001_q0_pbe
  RUN_TYPE GEO_OPT
  PRINT_LEVEL MEDIUM
&END GLOBAL

&FORCE_EVAL
  METHOD Quickstep

  &DFT
{common_dft_prefix()}

    &SCF
      EPS_SCF 1.0E-6
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

{xc_block()}

    &KPOINTS
      SCHEME MONKHORST-PACK 2 2 1
      FULL_GRID TRUE
    &END KPOINTS

  &END DFT

  &SUBSYS

{cell_block(structure)}

    &TOPOLOGY
      COORD_FILE_NAME {xyz_name}
      COORD_FILE_FORMAT XYZ
    &END TOPOLOGY

{kinds_block()}

  &END SUBSYS

&END FORCE_EVAL

{geo_opt_block()}
"""


def make_4x4x1_ot_input(structure, xyz_name):

    return f"""&GLOBAL
  PROJECT igzo_r3m_4x4x1_vo_o001_q0_pbe_ot
  RUN_TYPE GEO_OPT
  PRINT_LEVEL MEDIUM
&END GLOBAL

&FORCE_EVAL
  METHOD Quickstep

  &DFT
{common_dft_prefix()}

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

{xc_block()}

  &END DFT

  &SUBSYS

{cell_block(structure)}

    &TOPOLOGY
      COORD_FILE_NAME {xyz_name}
      COORD_FILE_FORMAT XYZ
    &END TOPOLOGY

{kinds_block()}

  &END SUBSYS

&END FORCE_EVAL

{geo_opt_block()}
"""


def generate_case(
    reference,
    scaling,
    directory,
    xyz_name,
    inp_name,
    input_function,
):

    supercell = reference.copy()

    supercell.make_supercell(
        scaling
    )

    (
        distance,
        removed_index,
        frac,
        cart,
    ) = choose_central_o001(
        supercell
    )

    pristine_atoms = len(
        supercell
    )

    defect = supercell.copy()

    defect.remove_sites(
        [removed_index]
    )

    directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    xyz_path = (
        directory
        / xyz_name
    )

    inp_path = (
        directory
        / inp_name
    )

    XYZ(defect).write_file(
        xyz_path
    )

    inp_path.write_text(
        input_function(
            defect,
            xyz_name,
        )
    )

    print("-" * 72)
    print(
        f"Supercell: {scaling}"
    )
    print(
        f"Pristine atoms: {pristine_atoms}"
    )
    print(
        f"Defect atoms:   {len(defect)}"
    )
    print(
        f"Removed index:  {removed_index}"
    )
    print(
        "Removed O001 fractional coordinate:"
    )
    print(
        f"  {frac[0]:.8f} "
        f"{frac[1]:.8f} "
        f"{frac[2]:.8f}"
    )
    print(
        "Removed O001 Cartesian coordinate [A]:"
    )
    print(
        f"  {cart[0]:.8f} "
        f"{cart[1]:.8f} "
        f"{cart[2]:.8f}"
    )
    print(
        f"Distance from supercell centre: "
        f"{distance:.6f} A"
    )
    print()
    print(
        f"XYZ: {xyz_path}"
    )
    print(
        f"INP: {inp_path}"
    )


def main():

    if not REFERENCE.exists():
        raise FileNotFoundError(
            f"Canonical R3m reference not found:\n"
            f"{REFERENCE}"
        )

    reference = Structure.from_file(
        REFERENCE
    )

    if len(reference) != 21:
        raise RuntimeError(
            f"Expected 21 atoms in reference, "
            f"found {len(reference)}."
        )

    sga = SpacegroupAnalyzer(
        reference,
        symprec=SYMPREC,
        angle_tolerance=ANGLE_TOLERANCE,
    )

    print("=" * 72)
    print("O001 VACANCY VALIDATION GENERATOR")
    print("=" * 72)
    print()
    print(
        f"Reference space group: "
        f"{sga.get_space_group_symbol()} "
        f"({sga.get_space_group_number()})"
    )
    print(
        f"Reference atoms: {len(reference)}"
    )

    oxygen_classes = (
        identify_oxygen_classes(
            reference
        )
    )

    print()
    print("Symmetry-defined oxygen classes:")

    for label, indices in oxygen_classes.items():
        print(
            f"  {label}: {indices}"
        )

    label_reference_sites(
        reference,
        oxygen_classes,
    )

    # ---------------------------------------------------------------
    # 3x3x1 + 2x2x1
    # ---------------------------------------------------------------

    dir_3 = (
        OUTPUT_ROOT
        / "3x3x1"
        / "O001"
        / "q0"
        / "pbe_2x2x1"
    )

    generate_case(
        reference=reference,
        scaling=[3, 3, 1],
        directory=dir_3,
        xyz_name=(
            "igzo_r3m_3x3x1_vo_o001_q0.xyz"
        ),
        inp_name=(
            "igzo_r3m_3x3x1_vo_o001_q0_pbe_2x2x1.inp"
        ),
        input_function=make_3x3x1_input,
    )

    print()

    # ---------------------------------------------------------------
    # 4x4x1 + Gamma + OT
    # ---------------------------------------------------------------

    dir_4 = (
        OUTPUT_ROOT
        / "4x4x1"
        / "O001"
        / "q0"
        / "pbe_gamma_ot"
    )

    generate_case(
        reference=reference,
        scaling=[4, 4, 1],
        directory=dir_4,
        xyz_name=(
            "igzo_r3m_4x4x1_vo_o001_q0.xyz"
        ),
        inp_name=(
            "igzo_r3m_4x4x1_vo_o001_q0_pbe_gamma_ot.inp"
        ),
        input_function=make_4x4x1_ot_input,
    )

    print()
    print("=" * 72)
    print("GENERATION COMPLETE")
    print("=" * 72)
    print()
    print(
        "3x3x1: 2x2x1 k-points + diagonalisation"
    )
    print(
        "4x4x1: Gamma only + OT"
    )
    print(
        "Both: fixed-cell PBE GEO_OPT"
    )


if __name__ == "__main__":
    main()