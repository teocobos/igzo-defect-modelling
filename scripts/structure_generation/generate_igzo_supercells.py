############################################################################################
#  Generate supercell structures for InGaZnO4 unrelaxed structures for the 4 inequivalent  #
#  sites                                                                                   #
#                                                                                          #
#  Teo Cobos                                                                               #
#  24/08/2026                                                                              #
#  python3                                                                                 #
############################################################################################


from pathlib import Path

from pymatgen.core import Structure
from pymatgen.io.cif import CifWriter
from pymatgen.io.vasp import Poscar
from pymatgen.io.xyz import XYZ


ROOT = Path(__file__).resolve().parents[2]

# Change this if you want to use ordered_002, 003 or 004 instead.
PARENT_MODEL = "igzo_crystal_ordered_001"

INPUT_CIF = (
    ROOT
    / "structures"
    / "crystalline"
    / "ordered_models"
    / PARENT_MODEL
    / f"{PARENT_MODEL}.cif"
)

OUTPUT_ROOT = (
    ROOT
    / "structures"
    / "crystalline"
    / "supercells"
    / "unrelaxed"
)

SUPERCELLS = {
    "2x2x1": [2, 2, 1],
    "3x3x1": [3, 3, 1],
}


def validate_supercell(structure, expected_atoms):
    if len(structure) != expected_atoms:
        raise ValueError(
            f"Expected {expected_atoms} atoms, found {len(structure)}"
        )

    if not structure.is_ordered:
        raise ValueError("Supercell contains partial occupancies.")


def main():
    parent = Structure.from_file(INPUT_CIF)

    print(f"Parent model: {PARENT_MODEL}")
    print(f"Parent atoms: {len(parent)}")
    print(f"Parent formula: {parent.composition}")
    print()

    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)

    for label, scaling in SUPERCELLS.items():

        supercell = parent.copy()
        supercell.make_supercell(scaling)

        expected_atoms = len(parent)

        for factor in scaling:
            expected_atoms *= factor

        validate_supercell(
            supercell,
            expected_atoms,
        )

        model_id = (
            f"{PARENT_MODEL}_supercell_{label}_unrelaxed"
        )

        output_dir = OUTPUT_ROOT / model_id
        output_dir.mkdir(parents=True, exist_ok=True)

        cif_file = output_dir / f"{model_id}.cif"
        xyz_file = output_dir / f"{model_id}.xyz"
        vasp_file = output_dir / f"{model_id}.vasp"

        CifWriter(supercell).write_file(cif_file)
        XYZ(supercell).write_file(xyz_file)
        Poscar(supercell).write_file(vasp_file)

        print(f"{label}")
        print(f"  atoms: {len(supercell)}")
        print(f"  formula: {supercell.composition}")
        print(f"  lattice:")
        for vector in supercell.lattice.matrix:
            print(
                f"    {vector[0]:12.6f} "
                f"{vector[1]:12.6f} "
                f"{vector[2]:12.6f}"
            )

        print(f"  written to: {output_dir}")
        print()


if __name__ == "__main__":
    main()