########################################################################
#  Local coordination polyhedral distortions                           #
#                                                                      #
#  Analyse and compare local coordination polyhedral distortions in    #
#  relaxed ordered IGZO structures using bond-length, bond-angle,      #
#  and polyhedral-volume metrics for InO6, GaO5, and ZnO4 environments.#
#                                                                      #
#  Teo Cobos                                                           #
#  25/08/2026                                                          #
#  python3                                                             #
########################################################################


from pathlib import Path
from itertools import combinations

import numpy as np
from scipy.spatial import ConvexHull

from pymatgen.core import Structure


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


# Ideal bond-angle sets for comparison.
#
# Tetrahedron:
# 6 O-centre-O angles, all 109.471°
#
# Octahedron:
# 12 angles of 90°
# 3 angles of 180°
#
# Trigonal bipyramid:
# 6 axial-equatorial 90°
# 3 equatorial-equatorial 120°
# 1 axial-axial 180°
#
# Square pyramid:
# 8 adjacent/apical-base 90°
# 2 opposite basal 180°
#
IDEAL_ANGLE_SETS = {
    "tetrahedral": sorted(
        [109.4712206] * 6
    ),
    "octahedral": sorted(
        [90.0] * 12
        + [180.0] * 3
    ),
    "trigonal_bipyramidal": sorted(
        [90.0] * 6
        + [120.0] * 3
        + [180.0]
    ),
    "square_pyramidal": sorted(
        [90.0] * 8
        + [180.0] * 2
    ),
}


def oxygen_neighbours(structure, site, cutoff):
    neighbours = structure.get_neighbors(site, cutoff)

    return [
        neighbour
        for neighbour in neighbours
        if neighbour.specie.symbol == "O"
    ]


def angle_between(v1, v2):
    cosine = np.dot(v1, v2) / (
        np.linalg.norm(v1) * np.linalg.norm(v2)
    )

    cosine = np.clip(cosine, -1.0, 1.0)

    return np.degrees(np.arccos(cosine))


def calculate_angles(site, neighbours):
    vectors = [
        neighbour.coords - site.coords
        for neighbour in neighbours
    ]

    angles = []

    for i, j in combinations(
        range(len(vectors)),
        2,
    ):
        angles.append(
            angle_between(
                vectors[i],
                vectors[j],
            )
        )

    return sorted(angles)


def bond_distortion_index(distances):
    """
    Baur-type bond-length distortion index:

        D = (1/n) Σ |l_i - l_mean| / l_mean

    Dimensionless.
    """
    distances = np.asarray(distances)

    mean = np.mean(distances)

    return np.mean(
        np.abs(distances - mean) / mean
    )


def coefficient_of_variation(distances):
    distances = np.asarray(distances)

    return (
        np.std(distances)
        / np.mean(distances)
    )


def polyhedron_volume(neighbours):
    """
    Volume of the convex hull formed by oxygen vertices.

    Returns NaN if the points cannot form a 3D hull.
    """
    coords = np.array([
        neighbour.coords
        for neighbour in neighbours
    ])

    try:
        hull = ConvexHull(coords)
        return hull.volume
    except Exception:
        return np.nan


def angle_rms_from_ideal(
    measured_angles,
    ideal_angles,
):
    """
    Compare sorted measured and ideal angle sets.

    Appropriate here because the coordination numbers
    and therefore number of pairwise angles are fixed.
    """

    measured = np.asarray(
        sorted(measured_angles)
    )

    ideal = np.asarray(
        sorted(ideal_angles)
    )

    if len(measured) != len(ideal):
        return np.nan

    return np.sqrt(
        np.mean(
            (measured - ideal) ** 2
        )
    )


def classify_geometry(
    element,
    coordination,
    angles,
):
    """
    Assign an ideal-polyhedron comparison appropriate
    to each coordination environment.
    """

    if element == "Zn" and coordination == 4:

        rms = angle_rms_from_ideal(
            angles,
            IDEAL_ANGLE_SETS["tetrahedral"],
        )

        return "tetrahedral", rms

    if element == "In" and coordination == 6:

        rms = angle_rms_from_ideal(
            angles,
            IDEAL_ANGLE_SETS["octahedral"],
        )

        return "octahedral", rms

    if element == "Ga" and coordination == 5:

        tbp_rms = angle_rms_from_ideal(
            angles,
            IDEAL_ANGLE_SETS[
                "trigonal_bipyramidal"
            ],
        )

        sqp_rms = angle_rms_from_ideal(
            angles,
            IDEAL_ANGLE_SETS[
                "square_pyramidal"
            ],
        )

        if tbp_rms <= sqp_rms:
            return (
                "trigonal_bipyramidal",
                tbp_rms,
            )

        return (
            "square_pyramidal",
            sqp_rms,
        )

    return "unclassified", np.nan


def analyse_site(
    structure,
    site_index,
    site,
    element,
    cutoff,
):
    neighbours = oxygen_neighbours(
        structure,
        site,
        cutoff,
    )

    distances = sorted([
        neighbour.nn_distance
        for neighbour in neighbours
    ])

    angles = calculate_angles(
        site,
        neighbours,
    )

    geometry, angle_rms = classify_geometry(
        element,
        len(neighbours),
        angles,
    )

    return {
        "index": site_index,
        "coordination": len(neighbours),
        "geometry": geometry,
        "distances": distances,
        "angles": angles,
        "mean_bond": np.mean(distances),
        "std_bond": np.std(distances),
        "distortion_index":
            bond_distortion_index(distances),
        "coefficient_variation":
            coefficient_of_variation(distances),
        "angle_rms": angle_rms,
        "volume":
            polyhedron_volume(neighbours),
    }


def analyse_element(
    structure,
    element,
    cutoff,
):
    results = []

    for index, site in enumerate(structure):

        if site.specie.symbol != element:
            continue

        results.append(
            analyse_site(
                structure,
                index,
                site,
                element,
                cutoff,
            )
        )

    return results


def print_site_table(
    model,
    element,
    results,
):
    print()
    print(
        f"{model} — {element} polyhedra"
    )
    print("-" * 100)

    print(
        f"{'Site':>6}"
        f"{'CN':>5}"
        f"{'Geometry':>24}"
        f"{'Mean bond / Å':>16}"
        f"{'σ / Å':>12}"
        f"{'Distortion':>14}"
        f"{'Angle RMS / °':>16}"
        f"{'Volume / Å³':>15}"
    )

    for result in results:

        print(
            f"{result['index']:>6}"
            f"{result['coordination']:>5}"
            f"{result['geometry']:>24}"
            f"{result['mean_bond']:>16.6f}"
            f"{result['std_bond']:>12.6f}"
            f"{result['distortion_index']:>14.6f}"
            f"{result['angle_rms']:>16.4f}"
            f"{result['volume']:>15.6f}"
        )


def average_metric(
    results,
    metric,
):
    values = np.asarray([
        result[metric]
        for result in results
    ])

    return np.nanmean(values)


def main():
    structures = {
        name: Structure.from_file(path)
        for name, path
        in STRUCTURES.items()
    }

    all_results = {}

    print("=" * 100)
    print(
        "RELAXED IGZO POLYHEDRAL "
        "DISTORTION ANALYSIS"
    )
    print("=" * 100)

    for model, structure in structures.items():

        all_results[model] = {}

        for element, cutoff in CUTOFFS.items():

            results = analyse_element(
                structure,
                element,
                cutoff,
            )

            all_results[model][element] = (
                results
            )

            print_site_table(
                model,
                element,
                results,
            )

    print()
    print("=" * 100)
    print(
        "AVERAGE POLYHEDRAL DISTORTION:"
        " ORDERED_001 vs ORDERED_003"
    )
    print("=" * 100)

    print(
        f"{'Polyhedron':<12}"
        f"{'D 001':>12}"
        f"{'D 003':>12}"
        f"{'ΔD':>12}"
        f"{'Angle RMS 001':>18}"
        f"{'Angle RMS 003':>18}"
        f"{'Volume 001':>16}"
        f"{'Volume 003':>16}"
    )

    for element in CUTOFFS:

        r1 = all_results[
            "ordered_001"
        ][element]

        r3 = all_results[
            "ordered_003"
        ][element]

        d1 = average_metric(
            r1,
            "distortion_index",
        )

        d3 = average_metric(
            r3,
            "distortion_index",
        )

        angle1 = average_metric(
            r1,
            "angle_rms",
        )

        angle3 = average_metric(
            r3,
            "angle_rms",
        )

        volume1 = average_metric(
            r1,
            "volume",
        )

        volume3 = average_metric(
            r3,
            "volume",
        )

        print(
            f"{element + 'O':<12}"
            f"{d1:>12.6f}"
            f"{d3:>12.6f}"
            f"{d3 - d1:>12.6f}"
            f"{angle1:>18.4f}"
            f"{angle3:>18.4f}"
            f"{volume1:>16.6f}"
            f"{volume3:>16.6f}"
        )


if __name__ == "__main__":
    main()