########################################################################
#  Bond Distribution Statistics                                        #
#                                                                      #
#                                                                      #
#  Teo Cobos                                                           #
#  25/08/2026                                                          #
#  python3                                                             #
########################################################################


from pathlib import Path
import numpy as np

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


def get_cation_sites(structure, element):
    return [
        (i, site)
        for i, site in enumerate(structure)
        if site.specie.symbol == element
    ]


def analyse_site(structure, index, site, cutoff):
    oxygen_neighbors = [
        n
        for n in structure.get_neighbors(site, cutoff)
        if n.specie.symbol == "O"
    ]

    distances = sorted(
        n.nn_distance
        for n in oxygen_neighbors
    )

    return {
        "site_index": index,
        "coordination": len(distances),
        "distances": distances,
        "mean": np.mean(distances) if distances else np.nan,
        "std": np.std(distances) if distances else np.nan,
        "min": np.min(distances) if distances else np.nan,
        "max": np.max(distances) if distances else np.nan,
    }


def analyse_element(structure, element, cutoff):
    site_results = []

    for index, site in get_cation_sites(structure, element):
        site_results.append(
            analyse_site(
                structure,
                index,
                site,
                cutoff,
            )
        )

    all_distances = [
        d
        for result in site_results
        for d in result["distances"]
    ]

    return {
        "sites": site_results,
        "all_distances": all_distances,
        "mean": np.mean(all_distances),
        "std": np.std(all_distances),
        "min": np.min(all_distances),
        "max": np.max(all_distances),
    }


def print_element_summary(model, element, result):
    print()
    print(f"{model} — {element}-O")
    print("-" * 72)

    print(
        f"Overall mean: {result['mean']:.6f} Å"
    )
    print(
        f"Overall std:  {result['std']:.6f} Å"
    )
    print(
        f"Overall min:  {result['min']:.6f} Å"
    )
    print(
        f"Overall max:  {result['max']:.6f} Å"
    )

    print()
    print(
        f"{'Site':>8}"
        f"{'CN':>6}"
        f"{'Mean / Å':>14}"
        f"{'Std / Å':>14}"
        f"{'Min / Å':>14}"
        f"{'Max / Å':>14}"
    )

    for site in result["sites"]:
        print(
            f"{site['site_index']:>8}"
            f"{site['coordination']:>6}"
            f"{site['mean']:>14.6f}"
            f"{site['std']:>14.6f}"
            f"{site['min']:>14.6f}"
            f"{site['max']:>14.6f}"
        )

        print(
            "        distances:",
            " ".join(
                f"{d:.6f}"
                for d in site["distances"]
            ),
        )


def main():
    structures = {
        name: Structure.from_file(path)
        for name, path in STRUCTURES.items()
    }

    print("=" * 80)
    print("RELAXED IGZO BOND-DISTRIBUTION ANALYSIS")
    print("=" * 80)

    results = {}

    for model, structure in structures.items():
        results[model] = {}

        for element, cutoff in CUTOFFS.items():
            result = analyse_element(
                structure,
                element,
                cutoff,
            )

            results[model][element] = result

            print_element_summary(
                model,
                element,
                result,
            )

    print()
    print("=" * 80)
    print("ORDERED_001 vs ORDERED_003")
    print("=" * 80)

    print(
        f"{'Bond':<10}"
        f"{'Mean 001 / Å':>16}"
        f"{'Mean 003 / Å':>16}"
        f"{'Δ mean / Å':>14}"
        f"{'σ 001 / Å':>14}"
        f"{'σ 003 / Å':>14}"
    )

    for element in CUTOFFS:
        r1 = results["ordered_001"][element]
        r3 = results["ordered_003"][element]

        delta_mean = r1["mean"] - r3["mean"]

        print(
            f"{element + '-O':<10}"
            f"{r1['mean']:>16.6f}"
            f"{r3['mean']:>16.6f}"
            f"{delta_mean:>14.6f}"
            f"{r1['std']:>14.6f}"
            f"{r3['std']:>14.6f}"
        )


if __name__ == "__main__":
    main()