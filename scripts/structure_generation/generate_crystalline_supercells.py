#!/usr/bin/env python3

"""
Generate crystalline IGZO supercells from the canonical
R3m cell-relaxed reference structure.

The generated structures are intended for crystalline
defect-supercell convergence and oxygen-vacancy calculations.
"""

from pathlib import Path

from pymatgen.core import Structure
from pymatgen.io.cif import CifWriter


ROOT = Path(__file__).resolve().parents[2]

REFERENCE_FILE = (
    ROOT
    / "structures"
    / "crystalline"
    / "cell_relaxed"
    / "igzo_crystal_ordered_003_r3m_cell_relaxed"
    / "igzo_crystal_ordered_003_r3m_cell_relaxed.cif"
)

OUTPUT_ROOT = (
    ROOT
    / "structures"
    / "crystalline"
    / "supercells"
)

SUPERCELLS = {
    "2x2x1": [2, 2, 1],
    "3x3x1": [3, 3, 1],
    "4x4x1": [4, 4, 1],
}


def minimum_lattice_translation(structure):
    """
    Determine the shortest non-zero lattice translation
    using translations from -2 to +2.
    """

    lattice = structure.lattice

    minimum_distance = float("inf")
    minimum_vector = None

    for i in range(-2, 3):
        for j in range(-2, 3):
            for k in range(-2, 3):

                if i == 0 and j == 0 and k == 0:
                    continue

                cart = lattice.get_cartesian_coords(
                    [i, j, k]
                )

                distance = (
                    cart[0] ** 2
                    + cart[1] ** 2
                    + cart[2] ** 2
                ) ** 0.5

                if distance < minimum_distance:
                    minimum_distance = distance
                    minimum_vector = (i, j, k)

    return minimum_distance, minimum_vector


def main():

    if not REFERENCE_FILE.exists():
        raise FileNotFoundError(
            f"Reference structure not found:\n{REFERENCE_FILE}"
        )

    reference = Structure.from_file(REFERENCE_FILE)

    print("=" * 78)
    print("CRYSTALLINE IGZO SUPERCELL GENERATION")
    print("=" * 78)

    print()
    print("Reference:")
    print(REFERENCE_FILE)

    print()
    print(f"Atoms:   {len(reference)}")
    print(f"Formula: {reference.composition.formula}")

    print()
    print("Reference lattice:")
    print(f"a = {reference.lattice.a:.6f} Å")
    print(f"b = {reference.lattice.b:.6f} Å")
    print(f"c = {reference.lattice.c:.6f} Å")
    print(f"γ = {reference.lattice.gamma:.6f}°")

    OUTPUT_ROOT.mkdir(
        parents=True,
        exist_ok=True,
    )

    print()
    print("-" * 78)

    for label, scaling in SUPERCELLS.items():

        structure = reference.copy()
        structure.make_supercell(scaling)

        output_dir = OUTPUT_ROOT / f"igzo_r3m_{label}"
        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_file = (
            output_dir
            / f"igzo_r3m_{label}.cif"
        )

        # Do not symmetry-reduce or modify coordinates when writing
        # the defect-parent supercell.
        CifWriter(
            structure,
            symprec=None,
        ).write_file(output_file)

        minimum_distance, minimum_vector = (
            minimum_lattice_translation(structure)
        )

        print()
        print(f"Supercell: {label}")
        print(f"Scaling:   {scaling}")
        print(f"Atoms:     {len(structure)}")
        print(
            f"Formula:   "
            f"{structure.composition.formula}"
        )

        print()
        print("Lattice:")
        print(
            f"  a = {structure.lattice.a:.6f} Å"
        )
        print(
            f"  b = {structure.lattice.b:.6f} Å"
        )
        print(
            f"  c = {structure.lattice.c:.6f} Å"
        )
        print(
            f"  γ = {structure.lattice.gamma:.6f}°"
        )

        print()
        print(
            "Shortest periodic lattice translation:"
        )
        print(
            f"  {minimum_distance:.6f} Å "
            f"for translation {minimum_vector}"
        )

        print()
        print(f"Written:")
        print(output_file)

        print()
        print("-" * 78)


if __name__ == "__main__":
    main()