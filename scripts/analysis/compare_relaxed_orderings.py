########################################################################
#  Structure comparison between relaxed 001 and 003                    #
#                                                                      #
#  - Space group after relaxation                                      #
#  - Lattice-preserving symmetry                                       #       
#  - Coordination environments                                         #
#  - RMS structural difference                                         #
#  - key In-O/Ga-O/Zn-O bond distribution                              #
#                                                                      #
#  Teo Cobos                                                           #
#  25/08/2026                                                          #
#  python3                                                             #
########################################################################


from pathlib import Path
import numpy as np

from pymatgen.core import Structure
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
from pymatgen.analysis.structure_matcher import StructureMatcher


ROOT = Path(__file__).resolve().parents[2]

STRUCTURES = {
    "ordered_001": (
        ROOT
        / "structures"
        / "crystalline"
        / "relaxed"
        / "igzo_crystal_ordered_001_relaxed"
        / "igzo_crystal_ordered_001_relaxed.cif"
    ),
    "ordered_003": (
        ROOT
        / "structures"
        / "crystalline"
        / "relaxed"
        / "igzo_crystal_ordered_003_relaxed"
        / "igzo_crystal_ordered_003_relaxed.cif"
    ),
}

CUTOFFS = {
    "In": 2.6,
    "Ga": 2.4,
    "Zn": 2.4,
}


def symmetry_info(structure):
    sga = SpacegroupAnalyzer(
        structure,
        symprec=1e-3,
        angle_tolerance=5,
    )

    return {
        "symbol": sga.get_space_group_symbol(),
        "number": sga.get_space_group_number(),
    }


def cation_oxygen_distances(structure, element, cutoff):
    distances = []
    coordinations = []

    for i, site in enumerate(structure):
        if site.specie.symbol != element:
            continue

        neighbours = structure.get_neighbors(site, cutoff)

        oxygen_neighbours = [
            n for n in neighbours
            if n.specie.symbol == "O"
        ]

        coordinations.append(len(oxygen_neighbours))

        for n in oxygen_neighbours:
            distances.append(n.nn_distance)

    return distances, coordinations


def print_bond_stats(name, structure):
    print(f"\n{name}")
    print("-" * 60)

    for element, cutoff in CUTOFFS.items():

        distances, coordinations = cation_oxygen_distances(
            structure,
            element,
            cutoff,
        )

        if distances:
            print(
                f"{element}-O:"
                f" mean={np.mean(distances):.4f} Å,"
                f" min={np.min(distances):.4f} Å,"
                f" max={np.max(distances):.4f} Å"
            )

        if coordinations:
            print(
                f"{element} coordination:"
                f" mean={np.mean(coordinations):.2f},"
                f" values={coordinations}"
            )


def main():
    structures = {
        name: Structure.from_file(path)
        for name, path in STRUCTURES.items()
    }

    print("=" * 72)
    print("RELAXED IGZO ORDERING COMPARISON")
    print("=" * 72)

    for name, structure in structures.items():

        sym = symmetry_info(structure)

        print(f"\n{name}")
        print(f"  atoms:       {len(structure)}")
        print(f"  formula:     {structure.composition.formula}")
        print(
            f"  space group: {sym['symbol']} ({sym['number']})"
        )

        print(
            "  lattice:"
            f" a={structure.lattice.a:.6f} Å,"
            f" b={structure.lattice.b:.6f} Å,"
            f" c={structure.lattice.c:.6f} Å"
        )

        print(
            "  angles:"
            f" α={structure.lattice.alpha:.4f}°, "
            f"β={structure.lattice.beta:.4f}°, "
            f"γ={structure.lattice.gamma:.4f}°"
        )

        print(
            f"  volume: {structure.volume:.6f} Å³"
        )

    s1 = structures["ordered_001"]
    s3 = structures["ordered_003"]

    matcher = StructureMatcher(
        primitive_cell=False,
        scale=False,
        attempt_supercell=False,
    )

    print()
    print("=" * 72)
    print("STRUCTURE MATCHING")
    print("=" * 72)

    equivalent = matcher.fit(s1, s3)

    print(
        "StructureMatcher equivalent:",
        equivalent
    )

    rms = matcher.get_rms_dist(s1, s3)

    if rms is not None:
        print(
            f"RMS displacement: {rms[0]:.6f}"
        )
        print(
            f"Maximum displacement: {rms[1]:.6f}"
        )
    else:
        print(
            "No direct StructureMatcher RMS mapping found."
        )

    print()
    print("=" * 72)
    print("LOCAL COORDINATION")
    print("=" * 72)

    print_bond_stats("ordered_001", s1)
    print_bond_stats("ordered_003", s3)


if __name__ == "__main__":
    main()