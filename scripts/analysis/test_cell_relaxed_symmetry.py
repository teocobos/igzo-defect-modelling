"""
Test the sensitivity of the fully cell-relaxed ordered_003 IGZO
space-group assignment to the symmetry tolerance.
"""

from pathlib import Path

from pymatgen.core import Structure
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer


ROOT = Path(__file__).resolve().parents[2]

STRUCTURE_ID = "igzo_crystal_ordered_003_cell_relaxed"

CIF_PATH = (
    ROOT
    / "structures"
    / "crystalline"
    / "cell_relaxed"
    / STRUCTURE_ID
    / f"{STRUCTURE_ID}.cif"
)

SYMPRECS = [
    1.0e-4,
    5.0e-4,
    1.0e-3,
    2.0e-3,
    5.0e-3,
    1.0e-2,
    2.0e-2,
    5.0e-2,
]


def main():

    structure = Structure.from_file(CIF_PATH)

    print("=" * 72)
    print("SYMMETRY TOLERANCE TEST")
    print("=" * 72)

    print(
        f"{'symprec / Å':>14} "
        f"{'space group':>16} "
        f"{'number':>8}"
    )

    for symprec in SYMPRECS:

        analyzer = SpacegroupAnalyzer(
            structure,
            symprec=symprec,
            angle_tolerance=5.0,
        )

        print(
            f"{symprec:14.6g} "
            f"{analyzer.get_space_group_symbol():>16} "
            f"{analyzer.get_space_group_number():>8}"
        )


if __name__ == "__main__":
    main()