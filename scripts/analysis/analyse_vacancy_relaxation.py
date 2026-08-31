#!/usr/bin/env python3

"""
===============================================================================
IGZO OXYGEN-VACANCY RELAXATION ANALYSIS
===============================================================================

Purpose
-------
Analyse structural relaxation around an oxygen vacancy in crystalline IGZO by
comparing:

    1. A pristine supercell
    2. The corresponding unrelaxed oxygen-vacancy structure
    3. The final relaxed CP2K GEO_OPT trajectory frame

The script supports:

    - 3x3x1 supercell
    - 4x4x1 supercell

Important
---------
The 3x3x1 production calculations were performed using the 120-degree
hexagonal cell representation:

    A = (10.114704210000,  0.000000000000, 0.000000000000)
    B = (-5.057352105000,  8.759590797625, 0.000000000000)
    C = (0.000000000000,  0.000000000000, 26.174269630000)

The 4x4x1 calculations use the corresponding 120-degree representation:

    A = (13.486272288253,  0.000000000000, 0.000000000000)
    B = (-6.743136144126, 11.679454403981, 0.000000000000)
    C = (0.000000000000,  0.000000000000, 26.174269634965)

These lattice vectors are explicitly reconstructed because ordinary XYZ files
do not contain lattice information.

Analysis performed
------------------
For every atom:

    - Initial distance from the vacancy
    - Final distance from the vacancy
    - Total atomic displacement
    - dx, dy, dz displacement components
    - Radial movement toward or away from the vacancy

Additional analysis includes:

    - Automatic identification of the removed oxygen
    - Vacancy-neighbour reconstruction
    - First-shell reconstruction grouped by element
    - Relaxation localisation versus distance
    - Largest atomic displacements
    - Relaxed CIF and XYZ generation

Outputs
-------
    <label>_atomic_displacements.csv
    <label>_vacancy_neighbours.csv
    <label>_first_shell_summary.csv
    <label>_localisation_by_radius.csv
    <label>_displacement_vs_distance.png
    <label>_relaxed.cif
    <label>_relaxed.xyz
    <label>_relaxation_summary.txt

Example
-------
python scripts/analysis/analyse_vacancy_relaxation.py \\
    --supercell 3x3x1 \\
    --pristine pristine.xyz \\
    --defect defect.xyz \\
    --trajectory defect-pos-1.xyz \\
    --label O001_3x3x1_gamma_ot \\
    --output analysis/crystalline/oxygen_vacancies/O001/3x3x1_gamma_ot

===============================================================================
"""

from __future__ import annotations

import argparse
from itertools import product
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from pymatgen.core import Lattice, Structure
from pymatgen.io.cif import CifWriter


# =============================================================================
# COMMAND-LINE ARGUMENTS
# =============================================================================

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Analyse structural relaxation around an IGZO oxygen vacancy."
    )

    parser.add_argument(
        "--supercell",
        required=True,
        choices=["3x3x1", "4x4x1"],
        help="IGZO supercell used in the calculation.",
    )

    parser.add_argument(
        "--pristine",
        required=True,
        help="Pristine supercell structure.",
    )

    parser.add_argument(
        "--defect",
        required=True,
        help="Initial unrelaxed oxygen-vacancy structure.",
    )

    parser.add_argument(
        "--trajectory",
        required=True,
        help="CP2K GEO_OPT XYZ trajectory.",
    )

    parser.add_argument(
        "--label",
        default="oxygen_vacancy",
        help="Label used in output filenames.",
    )

    parser.add_argument(
        "--output",
        required=True,
        help="Output directory.",
    )

    parser.add_argument(
        "--neighbour-cutoff",
        type=float,
        default=3.0,
        help="Radius in Å used to define vacancy neighbours.",
    )

    parser.add_argument(
        "--matching-tolerance",
        type=float,
        default=0.20,
        help="Tolerance in Å for matching pristine and defect oxygen sites.",
    )

    return parser.parse_args()


# =============================================================================
# SUPERCELL LATTICES
# =============================================================================

def get_supercell_lattice(supercell: str) -> Lattice:
    """
    Return the exact lattice used for the corresponding production calculation.

    The 120-degree hexagonal representation is retained explicitly so that
    periodic-distance analysis is performed in the same cell representation as
    the CP2K calculation.
    """

    if supercell == "3x3x1":
        return Lattice(
            [
                [10.114704210000, 0.000000000000, 0.000000000000],
                [-5.057352105000, 8.759590797625, 0.000000000000],
                [0.000000000000, 0.000000000000, 26.174269630000],
            ]
        )

    if supercell == "4x4x1":
        return Lattice(
            [
                [13.486272288253, 0.000000000000, 0.000000000000],
                [-6.743136144126, 11.679454403981, 0.000000000000],
                [0.000000000000, 0.000000000000, 26.174269634965],
            ]
        )

    raise ValueError(
        f"Unsupported supercell: {supercell}"
    )


# =============================================================================
# XYZ READING
# =============================================================================

def read_xyz_structure(
    filename: Path,
    lattice: Lattice,
) -> Structure:
    """
    Read a single-frame XYZ file and attach a periodic lattice.
    """

    lines = filename.read_text().splitlines()

    if not lines:
        raise RuntimeError(
            f"Empty XYZ file: {filename}"
        )

    natoms = int(
        lines[0].strip()
    )

    species = []
    coords = []

    for row in lines[2:2 + natoms]:
        parts = row.split()

        if len(parts) < 4:
            raise RuntimeError(
                f"Malformed XYZ coordinate line:\n{row}"
            )

        species.append(
            parts[0]
        )

        coords.append(
            [
                float(parts[1]),
                float(parts[2]),
                float(parts[3]),
            ]
        )

    if len(species) != natoms:
        raise RuntimeError(
            f"Expected {natoms} atoms in {filename}, "
            f"but read {len(species)}."
        )

    return Structure(
        lattice,
        species,
        coords,
        coords_are_cartesian=True,
    )


def read_last_xyz_frame(
    filename: Path,
):
    """
    Read the final complete frame from a multi-frame CP2K XYZ trajectory.
    """

    lines = filename.read_text().splitlines()

    frames = []

    i = 0

    while i < len(lines):
        line = lines[i].strip()

        if not line:
            i += 1
            continue

        try:
            natoms = int(line)

        except ValueError:
            i += 1
            continue

        frame_end = (
            i
            + natoms
            + 2
        )

        if frame_end > len(lines):
            raise RuntimeError(
                f"Incomplete XYZ frame near line {i + 1}"
            )

        comment = lines[
            i + 1
        ].strip()

        species = []
        coords = []

        for row in lines[
            i + 2:
            frame_end
        ]:
            parts = row.split()

            if len(parts) < 4:
                raise RuntimeError(
                    f"Malformed XYZ coordinate line:\n{row}"
                )

            species.append(
                parts[0]
            )

            coords.append(
                [
                    float(parts[1]),
                    float(parts[2]),
                    float(parts[3]),
                ]
            )

        frames.append(
            (
                species,
                np.asarray(
                    coords,
                    dtype=float,
                ),
                comment,
            )
        )

        i = frame_end

    if not frames:
        raise RuntimeError(
            f"No valid XYZ frames found in {filename}"
        )

    return frames[-1]


# =============================================================================
# PERIODIC GEOMETRY
# =============================================================================

def minimum_image_vector(
    lattice: Lattice,
    frac_from,
    frac_to,
):
    """
    Return the shortest periodic Cartesian vector from frac_from to frac_to.

    An explicit search over neighbouring lattice translations is used rather
    than component-wise fractional-coordinate wrapping. This is more robust for
    the non-orthogonal 120-degree hexagonal cell.
    """

    frac_from = np.asarray(
        frac_from,
        dtype=float,
    )

    frac_to = np.asarray(
        frac_to,
        dtype=float,
    )

    base_difference = (
        frac_to
        - frac_from
    )

    shortest_vector = None
    shortest_distance = np.inf

    for translation in product(
        (-1, 0, 1),
        repeat=3,
    ):
        translated_difference = (
            base_difference
            + np.asarray(
                translation,
                dtype=float,
            )
        )

        cart_vector = (
            lattice.get_cartesian_coords(
                translated_difference
            )
        )

        distance = float(
            np.linalg.norm(
                cart_vector
            )
        )

        if distance < shortest_distance:
            shortest_distance = distance
            shortest_vector = cart_vector

    return shortest_vector


def minimum_image_distance(
    lattice: Lattice,
    frac_a,
    frac_b,
):
    """
    Return minimum-image distance under periodic boundary conditions.
    """

    vector = minimum_image_vector(
        lattice,
        frac_a,
        frac_b,
    )

    return float(
        np.linalg.norm(
            vector
        )
    )


# =============================================================================
# VACANCY IDENTIFICATION
# =============================================================================

def find_missing_oxygen(
    pristine: Structure,
    defect: Structure,
    tolerance: float,
):
    """
    Find the oxygen present in the pristine structure but absent from the
    unrelaxed oxygen-vacancy structure.
    """

    if len(pristine) != len(defect) + 1:
        raise RuntimeError(
            "\nExpected pristine structure to contain exactly one more atom "
            "than the defect structure.\n"
            f"Pristine atoms: {len(pristine)}\n"
            f"Defect atoms:   {len(defect)}"
        )

    defect_oxygen_indices = [
        i
        for i, site in enumerate(defect)
        if site.species_string == "O"
    ]

    missing_candidates = []

    for pristine_index, pristine_site in enumerate(
        pristine
    ):
        if pristine_site.species_string != "O":
            continue

        nearest_distance = np.inf

        for defect_index in defect_oxygen_indices:
            defect_site = defect[
                defect_index
            ]

            distance = minimum_image_distance(
                pristine.lattice,
                pristine_site.frac_coords,
                defect_site.frac_coords,
            )

            nearest_distance = min(
                nearest_distance,
                distance,
            )

        if nearest_distance > tolerance:
            missing_candidates.append(
                (
                    pristine_index,
                    pristine_site,
                    nearest_distance,
                )
            )

    if len(missing_candidates) != 1:
        print(
            "\nPossible missing oxygen sites:"
        )

        for (
            index,
            site,
            nearest_distance,
        ) in missing_candidates:
            frac = site.frac_coords

            print(
                f"  pristine index={index:4d} "
                f"frac=("
                f"{frac[0]:.8f}, "
                f"{frac[1]:.8f}, "
                f"{frac[2]:.8f}) "
                f"nearest remaining O="
                f"{nearest_distance:.6f} Å"
            )

        raise RuntimeError(
            "\nCould not uniquely identify the missing oxygen.\n"
            f"Number of candidates: {len(missing_candidates)}"
        )

    return missing_candidates[0]


# =============================================================================
# STRUCTURE WRITING
# =============================================================================

def write_xyz(
    filename: Path,
    structure: Structure,
    comment: str,
):
    """
    Write structure as XYZ.
    """

    with filename.open(
        "w"
    ) as handle:
        handle.write(
            f"{len(structure)}\n"
        )

        handle.write(
            f"{comment}\n"
        )

        for site in structure:
            x, y, z = (
                site.coords
            )

            handle.write(
                f"{site.species_string:2s} "
                f"{x:18.10f} "
                f"{y:18.10f} "
                f"{z:18.10f}\n"
            )


# =============================================================================
# MAIN
# =============================================================================

def main():
    args = parse_arguments()

    pristine_file = Path(
        args.pristine
    )

    defect_file = Path(
        args.defect
    )

    trajectory_file = Path(
        args.trajectory
    )

    output_dir = Path(
        args.output
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    lattice = get_supercell_lattice(
        args.supercell
    )

    print(
        "=" * 78
    )

    print(
        "IGZO OXYGEN-VACANCY RELAXATION ANALYSIS"
    )

    print(
        "=" * 78
    )

    print(
        "\nInput files"
    )

    print(
        "-----------"
    )

    print(
        f"Supercell  : {args.supercell}"
    )

    print(
        f"Pristine   : {pristine_file}"
    )

    print(
        f"Defect     : {defect_file}"
    )

    print(
        f"Trajectory : {trajectory_file}"
    )

    print(
        f"Output     : {output_dir}"
    )

    print(
        "\nSimulation cell"
    )

    print(
        "---------------"
    )

    print(
        f"a = {lattice.a:.8f} Å"
    )

    print(
        f"b = {lattice.b:.8f} Å"
    )

    print(
        f"c = {lattice.c:.8f} Å"
    )

    print(
        f"alpha = {lattice.alpha:.6f} deg"
    )

    print(
        f"beta  = {lattice.beta:.6f} deg"
    )

    print(
        f"gamma = {lattice.gamma:.6f} deg"
    )

    # =========================================================================
    # READ STRUCTURES
    # =========================================================================

    if pristine_file.suffix.lower() == ".xyz":
        pristine = read_xyz_structure(
            pristine_file,
            lattice,
        )

    else:
        pristine = Structure.from_file(
            pristine_file
        )

        lattice = pristine.lattice

    if defect_file.suffix.lower() == ".xyz":
        defect_initial = read_xyz_structure(
            defect_file,
            lattice,
        )

    else:
        defect_initial = Structure.from_file(
            defect_file
        )

    print(
        "\nSystem"
    )

    print(
        "------"
    )

    print(
        f"Pristine atoms : {len(pristine)}"
    )

    print(
        f"Defect atoms   : {len(defect_initial)}"
    )

    # =========================================================================
    # VACANCY IDENTIFICATION
    # =========================================================================

    (
        missing_index,
        missing_site,
        nearest_remaining_oxygen,
    ) = find_missing_oxygen(
        pristine,
        defect_initial,
        args.matching_tolerance,
    )

    vacancy_frac = (
        np.asarray(
            missing_site.frac_coords
        )
        % 1.0
    )

    vacancy_cart = (
        lattice.get_cartesian_coords(
            vacancy_frac
        )
    )

    print(
        "\nIdentified oxygen vacancy"
    )

    print(
        "-------------------------"
    )

    print(
        f"Pristine oxygen index (0-based) : "
        f"{missing_index}"
    )

    print(
        "Fractional coordinates          : "
        f"{vacancy_frac[0]:.10f} "
        f"{vacancy_frac[1]:.10f} "
        f"{vacancy_frac[2]:.10f}"
    )

    print(
        "Cartesian coordinates / Å       : "
        f"{vacancy_cart[0]:.10f} "
        f"{vacancy_cart[1]:.10f} "
        f"{vacancy_cart[2]:.10f}"
    )

    print(
        "Nearest remaining O / Å         : "
        f"{nearest_remaining_oxygen:.6f}"
    )

    # =========================================================================
    # FINAL CP2K FRAME
    # =========================================================================

    (
        final_species,
        final_coords,
        final_comment,
    ) = read_last_xyz_frame(
        trajectory_file
    )

    print(
        "\nFinal CP2K trajectory frame"
    )

    print(
        "---------------------------"
    )

    print(
        final_comment
    )

    if len(final_species) != len(defect_initial):
        raise RuntimeError(
            "Final trajectory atom count does not match initial defect."
        )

    initial_species = [
        site.species_string
        for site in defect_initial
    ]

    if initial_species != final_species:
        raise RuntimeError(
            "Species ordering changed between initial and final structures."
        )

    defect_final = Structure(
        lattice,
        final_species,
        final_coords,
        coords_are_cartesian=True,
    )

    # =========================================================================
    # DISPLACEMENT ANALYSIS
    # =========================================================================

    rows = []

    for atom_index, (
        initial_site,
        final_site,
    ) in enumerate(
        zip(
            defect_initial,
            defect_final,
        )
    ):
        initial_frac = (
            np.asarray(
                initial_site.frac_coords
            )
            % 1.0
        )

        final_frac = (
            np.asarray(
                final_site.frac_coords
            )
            % 1.0
        )

        displacement_vector = minimum_image_vector(
            lattice,
            initial_frac,
            final_frac,
        )

        displacement = float(
            np.linalg.norm(
                displacement_vector
            )
        )

        initial_vacancy_vector = minimum_image_vector(
            lattice,
            vacancy_frac,
            initial_frac,
        )

        initial_distance = float(
            np.linalg.norm(
                initial_vacancy_vector
            )
        )

        final_vacancy_vector = minimum_image_vector(
            lattice,
            vacancy_frac,
            final_frac,
        )

        final_distance = float(
            np.linalg.norm(
                final_vacancy_vector
            )
        )

        radial_change = (
            final_distance
            - initial_distance
        )

        rows.append(
            {
                "atom_index_0based":
                    atom_index,

                "atom_index_1based":
                    atom_index + 1,

                "element":
                    initial_site.species_string,

                "initial_distance_from_vacancy_A":
                    initial_distance,

                "final_distance_from_vacancy_A":
                    final_distance,

                "radial_change_A":
                    radial_change,

                "displacement_A":
                    displacement,

                "dx_A":
                    displacement_vector[0],

                "dy_A":
                    displacement_vector[1],

                "dz_A":
                    displacement_vector[2],
            }
        )

    df = pd.DataFrame(
        rows
    )

    df = df.sort_values(
        "displacement_A",
        ascending=False,
    ).reset_index(
        drop=True
    )

    displacement_file = (
        output_dir
        / f"{args.label}_atomic_displacements.csv"
    )

    df.to_csv(
        displacement_file,
        index=False,
    )

    # =========================================================================
    # VACANCY NEIGHBOURS
    # =========================================================================

    neighbours = df[
        df[
            "initial_distance_from_vacancy_A"
        ]
        <= args.neighbour_cutoff
    ].copy()

    neighbours = neighbours.sort_values(
        "initial_distance_from_vacancy_A"
    )

    neighbour_file = (
        output_dir
        / f"{args.label}_vacancy_neighbours.csv"
    )

    neighbours.to_csv(
        neighbour_file,
        index=False,
    )

    # =========================================================================
    # FIRST-SHELL SUMMARY
    # =========================================================================

    first_shell_summary = (
        neighbours
        .groupby(
            "element"
        )
        .agg(
            atom_count=(
                "atom_index_0based",
                "count",
            ),
            mean_initial_distance_A=(
                "initial_distance_from_vacancy_A",
                "mean",
            ),
            mean_final_distance_A=(
                "final_distance_from_vacancy_A",
                "mean",
            ),
            mean_radial_change_A=(
                "radial_change_A",
                "mean",
            ),
            mean_displacement_A=(
                "displacement_A",
                "mean",
            ),
            max_displacement_A=(
                "displacement_A",
                "max",
            ),
        )
        .reset_index()
    )

    first_shell_file = (
        output_dir
        / f"{args.label}_first_shell_summary.csv"
    )

    first_shell_summary.to_csv(
        first_shell_file,
        index=False,
    )

    # =========================================================================
    # LOCALISATION
    # =========================================================================

    radius_rows = []

    for radius in (
        3.0,
        4.0,
        5.0,
        6.0,
        7.0,
    ):
        inside = df[
            df[
                "initial_distance_from_vacancy_A"
            ]
            <= radius
        ]

        outside = df[
            df[
                "initial_distance_from_vacancy_A"
            ]
            > radius
        ]

        radius_rows.append(
            {
                "radius_A":
                    radius,

                "atoms_inside":
                    len(inside),

                "max_displacement_inside_A":
                    (
                        inside[
                            "displacement_A"
                        ].max()
                        if len(inside)
                        else np.nan
                    ),

                "mean_displacement_inside_A":
                    (
                        inside[
                            "displacement_A"
                        ].mean()
                        if len(inside)
                        else np.nan
                    ),

                "max_displacement_outside_A":
                    (
                        outside[
                            "displacement_A"
                        ].max()
                        if len(outside)
                        else np.nan
                    ),

                "mean_displacement_outside_A":
                    (
                        outside[
                            "displacement_A"
                        ].mean()
                        if len(outside)
                        else np.nan
                    ),
            }
        )

    radius_df = pd.DataFrame(
        radius_rows
    )

    radius_file = (
        output_dir
        / f"{args.label}_localisation_by_radius.csv"
    )

    radius_df.to_csv(
        radius_file,
        index=False,
    )

    # =========================================================================
    # PLOT
    # =========================================================================

    fig, ax = plt.subplots(
        figsize=(7.5, 5.5)
    )

    for element in sorted(
        df[
            "element"
        ].unique()
    ):
        subset = df[
            df[
                "element"
            ]
            == element
        ]

        ax.scatter(
            subset[
                "initial_distance_from_vacancy_A"
            ],
            subset[
                "displacement_A"
            ],
            label=element,
        )

    ax.set_xlabel(
        r"Initial distance from $V_{\mathrm{O}}$ (Å)"
    )

    ax.set_ylabel(
        "Atomic displacement (Å)"
    )

    ax.set_title(
        f"{args.label}: vacancy-induced structural relaxation"
    )

    ax.legend()

    fig.tight_layout()

    plot_file = (
        output_dir
        / f"{args.label}_displacement_vs_distance.png"
    )

    fig.savefig(
        plot_file,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close(
        fig
    )

    # =========================================================================
    # FINAL RELAXED STRUCTURES
    # =========================================================================

    final_cif = (
        output_dir
        / f"{args.label}_relaxed.cif"
    )

    CifWriter(
        defect_final,
        symprec=None,
    ).write_file(
        final_cif
    )

    final_xyz = (
        output_dir
        / f"{args.label}_relaxed.xyz"
    )

    write_xyz(
        final_xyz,
        defect_final,
        final_comment,
    )

    # =========================================================================
    # TEXT SUMMARY
    # =========================================================================

    summary_file = (
        output_dir
        / f"{args.label}_relaxation_summary.txt"
    )

    with summary_file.open(
        "w"
    ) as handle:
        handle.write(
            "IGZO oxygen-vacancy relaxation analysis\n"
        )

        handle.write(
            "=" * 60
            + "\n\n"
        )

        handle.write(
            f"Label: {args.label}\n"
        )

        handle.write(
            f"Supercell: {args.supercell}\n"
        )

        handle.write(
            f"Pristine atoms: {len(pristine)}\n"
        )

        handle.write(
            f"Defect atoms: {len(defect_initial)}\n\n"
        )

        handle.write(
            f"Missing oxygen pristine index: "
            f"{missing_index}\n"
        )

        handle.write(
            "Vacancy fractional coordinates: "
            f"{vacancy_frac[0]:.10f} "
            f"{vacancy_frac[1]:.10f} "
            f"{vacancy_frac[2]:.10f}\n"
        )

        handle.write(
            "\nFirst-shell reconstruction by element:\n"
        )

        for _, row in first_shell_summary.iterrows():
            change = row[
                "mean_radial_change_A"
            ]

            direction = (
                "toward vacancy"
                if change < 0
                else "away from vacancy"
            )

            handle.write(
                f"  {row['element']:2s}: "
                f"N={int(row['atom_count'])}, "
                f"<r_initial>="
                f"{row['mean_initial_distance_A']:.6f} Å, "
                f"<r_final>="
                f"{row['mean_final_distance_A']:.6f} Å, "
                f"<delta_r>="
                f"{change:+.6f} Å "
                f"({direction}), "
                f"<disp>="
                f"{row['mean_displacement_A']:.6f} Å, "
                f"max_disp="
                f"{row['max_displacement_A']:.6f} Å\n"
            )

        handle.write(
            "\nRelaxation localisation:\n"
        )

        for _, row in radius_df.iterrows():
            handle.write(
                f"  outside {row['radius_A']:.1f} Å: "
                f"max="
                f"{row['max_displacement_outside_A']:.6f} Å, "
                f"mean="
                f"{row['mean_displacement_outside_A']:.6f} Å\n"
            )

    # =========================================================================
    # TERMINAL OUTPUT
    # =========================================================================

    print(
        "\n" + "=" * 78
    )

    print(
        "15 LARGEST ATOMIC DISPLACEMENTS"
    )

    print(
        "=" * 78
    )

    print(
        df[
            [
                "atom_index_0based",
                "element",
                "initial_distance_from_vacancy_A",
                "displacement_A",
                "radial_change_A",
            ]
        ]
        .head(15)
        .to_string(
            index=False,
            float_format=lambda x: f"{x:.6f}",
        )
    )

    print(
        "\n" + "=" * 78
    )

    print(
        "FIRST-SHELL RECONSTRUCTION BY ELEMENT"
    )

    print(
        "=" * 78
    )

    print(
        first_shell_summary.to_string(
            index=False,
            float_format=lambda x: f"{x:.6f}",
        )
    )

    print(
        "\n" + "=" * 78
    )

    print(
        "RELAXATION LOCALISATION"
    )

    print(
        "=" * 78
    )

    print(
        radius_df.to_string(
            index=False,
            float_format=lambda x: f"{x:.6f}",
        )
    )

    print(
        "\nFiles written"
    )

    print(
        "-------------"
    )

    print(
        f"Atomic displacements : {displacement_file}"
    )

    print(
        f"Vacancy neighbours   : {neighbour_file}"
    )

    print(
        f"First-shell summary  : {first_shell_file}"
    )

    print(
        f"Localisation table   : {radius_file}"
    )

    print(
        f"Displacement plot    : {plot_file}"
    )

    print(
        f"Relaxed CIF          : {final_cif}"
    )

    print(
        f"Relaxed XYZ          : {final_xyz}"
    )

    print(
        f"Summary              : {summary_file}"
    )

    print(
        "\nAnalysis complete."
    )


if __name__ == "__main__":
    main()