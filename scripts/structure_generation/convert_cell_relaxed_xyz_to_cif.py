########################################################################
#  Convert cell optimised .xyz structures to .cif                      #
#                                                                      #
#                                                                      #
#  Teo Cobos                                                           #
#  27/08/2026                                                          #
#  python3                                                             #
#  pymatgen                                                            #
########################################################################


"""
Convert the final CP2K CELL_OPT XYZ structure into a CIF using the exact
cell-relaxed lattice vectors from the ordered_003 CP2K restart file.
"""

from pathlib import Path

from pymatgen.core import Lattice, Structure
from pymatgen.io.xyz import XYZ


ROOT = Path(__file__).resolve().parents[2]

MODEL_ID = "igzo_crystal_ordered_003_cell_relaxed"

STRUCTURE_DIR = (
    ROOT
    / "structures"
    / "crystalline"
    / "cell_relaxed"
    / MODEL_ID
)

XYZ_PATH = STRUCTURE_DIR / f"{MODEL_ID}.xyz"
CIF_PATH = STRUCTURE_DIR / f"{MODEL_ID}.cif"


LATTICE = Lattice([
    [
        3.3714317445963671,
        0.0000000000000000,
        0.0000000000000000,
    ],
    [
        1.6857158722981835,
        2.9197455379457429,
        0.0000000000000000,
    ],
    [
        0.0000000000000000,
        0.0000000000000000,
        26.171439712622281,
    ],
])


def main():

    if not XYZ_PATH.exists():
        raise FileNotFoundError(
            f"Final CELL_OPT XYZ not found: {XYZ_PATH}"
        )

    xyz = XYZ.from_file(XYZ_PATH)
    molecule = xyz.molecule

    structure = Structure(
        LATTICE,
        molecule.species,
        molecule.cart_coords,
        coords_are_cartesian=True,
        to_unit_cell=True,
    )

    structure.to(filename=CIF_PATH)

    print("=" * 72)
    print("CELL-RELAXED IGZO STRUCTURE")
    print("=" * 72)

    print(f"Structure ID: {MODEL_ID}")
    print(f"Atoms:        {len(structure)}")
    print(f"Formula:      {structure.composition.formula}")

    print()
    print("Lattice parameters:")
    print(f"  a     = {structure.lattice.a:.10f} Å")
    print(f"  b     = {structure.lattice.b:.10f} Å")
    print(f"  c     = {structure.lattice.c:.10f} Å")
    print(f"  alpha = {structure.lattice.alpha:.8f}°")
    print(f"  beta  = {structure.lattice.beta:.8f}°")
    print(f"  gamma = {structure.lattice.gamma:.8f}°")
    print(f"  V     = {structure.volume:.10f} Å³")

    print()
    print(f"Written: {CIF_PATH}")


if __name__ == "__main__":
    main()