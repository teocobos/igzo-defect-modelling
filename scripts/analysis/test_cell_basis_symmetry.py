"""
Compare symmetry detection for equivalent 60-degree and 120-degree
representations of the cell-relaxed ordered_003 IGZO lattice.
"""

from pathlib import Path

from pymatgen.core import Lattice, Structure
from pymatgen.io.xyz import XYZ
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer


ROOT = Path(__file__).resolve().parents[2]

XYZ_PATH = (
    ROOT
    / "structures"
    / "crystalline"
    / "cell_relaxed"
    / "igzo_crystal_ordered_003_cell_relaxed"
    / "igzo_crystal_ordered_003_cell_relaxed.xyz"
)


CELL_60 = Lattice([
    [
        3.3714317445963671,
        0.0,
        0.0,
    ],
    [
        1.6857158722981835,
        2.9197455379457429,
        0.0,
    ],
    [
        0.0,
        0.0,
        26.171439712622281,
    ],
])


CELL_120 = Lattice([
    [
        3.3714317445963671,
        0.0,
        0.0,
    ],
    [
        -1.6857158722981836,
        2.9197455379457429,
        0.0,
    ],
    [
        0.0,
        0.0,
        26.171439712622281,
    ],
])


SYMPRECS = [
    1e-4,
    5e-4,
    1e-3,
    2e-3,
    5e-3,
    1e-2,
    2e-2,
    5e-2,
]


def make_structure(lattice):
    xyz = XYZ.from_file(XYZ_PATH)
    molecule = xyz.molecule

    return Structure(
        lattice,
        molecule.species,
        molecule.cart_coords,
        coords_are_cartesian=True,
        to_unit_cell=True,
    )


def analyse(label, structure):

    print()
    print("=" * 72)
    print(label)
    print("=" * 72)

    print(
        f"gamma = {structure.lattice.gamma:.8f} degrees"
    )

    print(
        f"{'symprec / A':>14}"
        f"{'space group':>18}"
        f"{'number':>10}"
    )

    for symprec in SYMPRECS:

        sga = SpacegroupAnalyzer(
            structure,
            symprec=symprec,
            angle_tolerance=5,
        )

        print(
            f"{symprec:>14.6g}"
            f"{sga.get_space_group_symbol():>18}"
            f"{sga.get_space_group_number():>10}"
        )


def main():

    structure_60 = make_structure(CELL_60)
    structure_120 = make_structure(CELL_120)

    analyse(
        "CP2K 60-degree cell",
        structure_60,
    )

    analyse(
        "Equivalent 120-degree cell",
        structure_120,
    )


if __name__ == "__main__":
    main()