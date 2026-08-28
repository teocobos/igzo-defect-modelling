"""
Enumerate symmetry-inequivalent oxygen sites in the fully cell-relaxed
ordered_003 IGZO crystalline reference and characterise their local
cation environments.
"""

from collections import Counter
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
    / "igzo_crystal_ordered_003_r3m_cell_relaxed"
    / "igzo_crystal_ordered_003_r3m_cell_relaxed.cif"
)

SYMPREC = 2.0e-3
ANGLE_TOLERANCE = 5.0

NEIGHBOR_CUTOFF = 2.7


def local_cation_environment(structure, site_index):

    site = structure[site_index]

    neighbors = structure.get_neighbors(
        site,
        NEIGHBOR_CUTOFF,
    )

    cation_neighbors = [
        neighbor
        for neighbor in neighbors
        if neighbor.specie.symbol in {"In", "Ga", "Zn"}
    ]

    cation_neighbors.sort(
        key=lambda neighbor: neighbor.nn_distance
    )

    counts = Counter(
        neighbor.specie.symbol
        for neighbor in cation_neighbors
    )

    return cation_neighbors, counts


def main():

    structure = Structure.from_file(CIF_PATH)

    analyzer = SpacegroupAnalyzer(
        structure,
        symprec=SYMPREC,
        angle_tolerance=ANGLE_TOLERANCE,
    )

    symmetrized = analyzer.get_symmetrized_structure()

    print("=" * 88)
    print("SYMMETRY-INEQUIVALENT OXYGEN SITES")
    print("=" * 88)

    print(f"Structure:   {STRUCTURE_ID}")
    print(f"Atoms:       {len(structure)}")
    print(f"Formula:     {structure.composition.formula}")

    print(
        f"Space group: "
        f"{analyzer.get_space_group_symbol()} "
        f"({analyzer.get_space_group_number()})"
    )

    print()

    oxygen_group_number = 0

    for group, wyckoff in zip(
        symmetrized.equivalent_indices,
        symmetrized.wyckoff_symbols,
    ):

        representative = group[0]

        if structure[representative].specie.symbol != "O":
            continue

        oxygen_group_number += 1

        neighbors, counts = local_cation_environment(
            structure,
            representative,
        )

        site = structure[representative]

        label = f"O{oxygen_group_number:03d}"

        print("-" * 88)

        print(f"Site label:       {label}")
        print(f"Representative:   atom index {representative}")
        print(f"Equivalent atoms: {group}")
        print(f"Multiplicity:     {len(group)}")
        print(f"Wyckoff:          {wyckoff}")

        print(
            "Fractional coord: "
            f"{site.frac_coords[0]:.8f} "
            f"{site.frac_coords[1]:.8f} "
            f"{site.frac_coords[2]:.8f}"
        )

        print(
            "Cation environment: "
            f"In={counts.get('In', 0)}, "
            f"Ga={counts.get('Ga', 0)}, "
            f"Zn={counts.get('Zn', 0)}"
        )

        print("Neighbour distances:")

        for neighbor in neighbors:
            print(
                f"  {neighbor.specie.symbol:2s} "
                f"{neighbor.nn_distance:10.6f} Å"
            )

        print()

    print("=" * 88)
    print(
        f"Total symmetry-inequivalent oxygen sites: "
        f"{oxygen_group_number}"
    )
    print("=" * 88)


if __name__ == "__main__":
    main()