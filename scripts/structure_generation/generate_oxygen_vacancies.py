#!/usr/bin/env python3

"""
Generate symmetry-distinct neutral oxygen-vacancy structures for
crystalline R3m IGZO.

Examples
--------
Generate the established 3x3x1 dataset:

    python scripts/structure_generation/generate_oxygen_vacancies.py \
        --supercell 3x3x1

Generate the production 4x4x1 dataset:

    python scripts/structure_generation/generate_oxygen_vacancies.py \
        --supercell 4x4x1
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import numpy as np

from pymatgen.core import Structure
from pymatgen.io.cif import CifWriter
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer


# =============================================================================
# PATHS
# =============================================================================

ROOT = Path(__file__).resolve().parents[2]

REFERENCE_FILE = (
    ROOT
    / "structures"
    / "crystalline"
    / "cell_relaxed"
    / "igzo_crystal_ordered_003_r3m_cell_relaxed"
    / "igzo_crystal_ordered_003_r3m_cell_relaxed.cif"
)


# =============================================================================
# SETTINGS
# =============================================================================

SYMPREC = 2.0e-3
ANGLE_TOLERANCE = 5.0

EXPECTED_REFERENCE_ATOMS = 21
EXPECTED_O_CLASSES = 4

SUPERCELLS = {
    "3x3x1": {
        "matrix": [3, 3, 1],
        "pristine_atoms": 189,
        "defect_atoms": 188,
    },
    "4x4x1": {
        "matrix": [4, 4, 1],
        "pristine_atoms": 336,
        "defect_atoms": 335,
    },
}

ENVIRONMENTS = {
    "O001": "Ga3Zn1",
    "O002": "In3Zn1",
    "O003": "In3Ga1",
    "O004": "Ga1Zn3",
}


# =============================================================================
# ARGUMENTS
# =============================================================================

def parse_arguments():
    parser = argparse.ArgumentParser(
        description=(
            "Generate symmetry-distinct neutral oxygen vacancies "
            "for crystalline R3m IGZO."
        )
    )

    parser.add_argument(
        "--supercell",
        required=True,
        choices=sorted(SUPERCELLS),
        help="Supercell to generate.",
    )

    return parser.parse_args()


# =============================================================================
# SYMMETRY CLASSIFICATION
# =============================================================================

def classify_reference_oxygen_sites(structure):
    """
    Identify the four symmetry-inequivalent oxygen classes in the
    canonical 21-atom R3m reference.
    """

    sga = SpacegroupAnalyzer(
        structure,
        symprec=SYMPREC,
        angle_tolerance=ANGLE_TOLERANCE,
    )

    symbol = sga.get_space_group_symbol()
    number = sga.get_space_group_number()

    print()
    print("Reference symmetry:")
    print(f"  Space group: {symbol} ({number})")

    if number != 160:
        raise RuntimeError(
            "Canonical reference was not recognised as R3m (160). "
            f"Detected {symbol} ({number})."
        )

    symmetrized = sga.get_symmetrized_structure()

    oxygen_groups = []

    for indices in symmetrized.equivalent_indices:
        representative = structure[indices[0]]

        if representative.specie.symbol == "O":
            oxygen_groups.append(list(indices))

    if len(oxygen_groups) != EXPECTED_O_CLASSES:
        raise RuntimeError(
            f"Expected {EXPECTED_O_CLASSES} inequivalent oxygen groups "
            f"but found {len(oxygen_groups)}."
        )

    # Preserve established O001-O004 ordering.
    oxygen_groups.sort(key=lambda group: min(group))

    site_classes = {}

    for i, indices in enumerate(oxygen_groups, start=1):
        label = f"O{i:03d}"
        site_classes[label] = indices

    return site_classes


# =============================================================================
# SITE LABELLING
# =============================================================================

def assign_reference_labels(structure, site_classes):
    """
    Attach the stable O001-O004 label to each oxygen atom.
    """

    labels = [""] * len(structure)

    for label, indices in site_classes.items():
        for index in indices:
            labels[index] = label

    structure.add_site_property(
        "oxygen_site_id",
        labels,
    )

    return structure


# =============================================================================
# REPRESENTATIVE SITE SELECTION
# =============================================================================

def minimum_image_vector_to_centre(structure, frac_coords):
    """
    Return minimum-image Cartesian vector between a site and the
    fractional centre (0.5, 0.5, 0.5).

    Explicit lattice translations are used so this remains robust for
    non-orthogonal hexagonal cells.
    """

    centre = np.array(
        [0.5, 0.5, 0.5],
        dtype=float,
    )

    frac_coords = np.asarray(
        frac_coords,
        dtype=float,
    )

    base_delta = frac_coords - centre

    best_vector = None
    best_distance = np.inf

    for i in (-1, 0, 1):
        for j in (-1, 0, 1):
            for k in (-1, 0, 1):

                delta = (
                    base_delta
                    + np.array(
                        [i, j, k],
                        dtype=float,
                    )
                )

                cart = structure.lattice.get_cartesian_coords(
                    delta
                )

                distance = np.linalg.norm(
                    cart
                )

                if distance < best_distance:
                    best_distance = distance
                    best_vector = cart

    return best_vector


def select_central_site(structure, label):
    """
    Select the member of a given O001-O004 class closest to the
    supercell centre under periodic boundary conditions.
    """

    labels = structure.site_properties[
        "oxygen_site_id"
    ]

    candidates = []

    for index, site_label in enumerate(labels):

        if site_label != label:
            continue

        vector = minimum_image_vector_to_centre(
            structure,
            structure[index].frac_coords,
        )

        distance = np.linalg.norm(
            vector
        )

        candidates.append(
            (
                distance,
                index,
            )
        )

    if not candidates:
        raise RuntimeError(
            f"No atoms found for oxygen class {label}."
        )

    candidates.sort()

    return candidates[0][1]


# =============================================================================
# MAIN
# =============================================================================

def main():
    args = parse_arguments()

    config = SUPERCELLS[
        args.supercell
    ]

    supercell_matrix = config[
        "matrix"
    ]

    expected_pristine_atoms = config[
        "pristine_atoms"
    ]

    expected_defect_atoms = config[
        "defect_atoms"
    ]

    output_root = (
        ROOT
        / "structures"
        / "crystalline"
        / "defects"
        / "oxygen_vacancies"
        / args.supercell
    )

    pristine_dir = (
        output_root
        / "pristine"
    )

    metadata_file = (
        output_root
        / f"oxygen_vacancy_sites_{args.supercell}.csv"
    )

    print("=" * 80)
    print("CRYSTALLINE IGZO OXYGEN-VACANCY GENERATION")
    print("=" * 80)

    print()
    print(f"Requested supercell: {args.supercell}")
    print(f"Supercell matrix:    {supercell_matrix}")

    # -------------------------------------------------------------------------
    # Load canonical reference
    # -------------------------------------------------------------------------

    if not REFERENCE_FILE.exists():
        raise FileNotFoundError(
            f"Reference structure not found:\n{REFERENCE_FILE}"
        )

    reference = Structure.from_file(
        REFERENCE_FILE
    )

    if len(reference) != EXPECTED_REFERENCE_ATOMS:
        raise RuntimeError(
            f"Expected {EXPECTED_REFERENCE_ATOMS} atoms in reference "
            f"but found {len(reference)}."
        )

    print()
    print("Reference structure:")
    print(f"  {REFERENCE_FILE}")
    print(f"  Atoms:   {len(reference)}")
    print(f"  Formula: {reference.composition.formula}")

    # -------------------------------------------------------------------------
    # Oxygen classes
    # -------------------------------------------------------------------------

    site_classes = classify_reference_oxygen_sites(
        reference
    )

    print()
    print("Reference oxygen classes:")

    for label, indices in site_classes.items():
        print(
            f"  {label}: "
            f"indices={indices}, "
            f"multiplicity={len(indices)}, "
            f"environment={ENVIRONMENTS[label]}"
        )

    reference = assign_reference_labels(
        reference,
        site_classes,
    )

    # -------------------------------------------------------------------------
    # Generate supercell
    # -------------------------------------------------------------------------

    supercell = reference.copy()

    supercell.make_supercell(
        supercell_matrix
    )

    if len(supercell) != expected_pristine_atoms:
        raise RuntimeError(
            f"Expected {expected_pristine_atoms} atoms in "
            f"{args.supercell} supercell but found {len(supercell)}."
        )

    print()
    print(f"{args.supercell} pristine supercell:")
    print(f"  Atoms:   {len(supercell)}")
    print(f"  Formula: {supercell.composition.formula}")
    print(f"  a = {supercell.lattice.a:.8f} Å")
    print(f"  b = {supercell.lattice.b:.8f} Å")
    print(f"  c = {supercell.lattice.c:.8f} Å")
    print(f"  alpha = {supercell.lattice.alpha:.6f}°")
    print(f"  beta  = {supercell.lattice.beta:.6f}°")
    print(f"  gamma = {supercell.lattice.gamma:.6f}°")

    # -------------------------------------------------------------------------
    # Write pristine CIF
    # -------------------------------------------------------------------------

    pristine_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    pristine_file = (
        pristine_dir
        / f"igzo_r3m_{args.supercell}.cif"
    )

    pristine_for_output = supercell.copy()

    if "oxygen_site_id" in pristine_for_output.site_properties:
        pristine_for_output.remove_site_property(
            "oxygen_site_id"
        )

    CifWriter(
        pristine_for_output,
        symprec=None,
    ).write_file(
        pristine_file
    )

    print()
    print("Pristine parent written:")
    print(f"  {pristine_file}")

    # -------------------------------------------------------------------------
    # Generate vacancy structures
    # -------------------------------------------------------------------------

    metadata = []

    print()
    print("-" * 80)
    print("VACANCY STRUCTURES")
    print("-" * 80)

    for label in sorted(site_classes):

        representative_index = select_central_site(
            supercell,
            label,
        )

        removed_site = supercell[
            representative_index
        ]

        frac = np.array(
            removed_site.frac_coords
        )

        cart = np.array(
            removed_site.coords
        )

        defect = supercell.copy()

        defect.remove_sites(
            [representative_index]
        )

        if len(defect) != expected_defect_atoms:
            raise RuntimeError(
                f"{label}: expected {expected_defect_atoms} atoms "
                f"after vacancy creation but found {len(defect)}."
            )

        if "oxygen_site_id" in defect.site_properties:
            defect.remove_site_property(
                "oxygen_site_id"
            )

        defect_dir = (
            output_root
            / label
            / "q0"
        )

        defect_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        filename = (
            f"igzo_r3m_{args.supercell}_vo_"
            f"{label.lower()}_q0.cif"
        )

        output_file = (
            defect_dir
            / filename
        )

        CifWriter(
            defect,
            symprec=None,
        ).write_file(
            output_file
        )

        metadata.append(
            {
                "site_id": label,
                "wyckoff": "3a",
                "environment": ENVIRONMENTS[label],
                "removed_atom_index_0based": representative_index,
                "removed_atom_index_1based": representative_index + 1,
                "frac_x": frac[0],
                "frac_y": frac[1],
                "frac_z": frac[2],
                "cart_x_A": cart[0],
                "cart_y_A": cart[1],
                "cart_z_A": cart[2],
                "supercell": args.supercell,
                "pristine_atoms": expected_pristine_atoms,
                "defect_atoms": expected_defect_atoms,
                "charge": 0,
                "filename": str(
                    output_file.relative_to(ROOT)
                ),
            }
        )

        print()
        print(label)
        print(
            f"  Environment: {ENVIRONMENTS[label]}"
        )
        print(
            f"  Removed index: "
            f"{representative_index} "
            f"(0-based)"
        )
        print(
            "  Fractional coordinate: "
            f"{frac[0]:.10f} "
            f"{frac[1]:.10f} "
            f"{frac[2]:.10f}"
        )
        print(
            "  Cartesian coordinate:  "
            f"{cart[0]:.10f} "
            f"{cart[1]:.10f} "
            f"{cart[2]:.10f} Å"
        )
        print(
            f"  Defect atoms: {len(defect)}"
        )
        print(
            f"  Written: {output_file}"
        )

    # -------------------------------------------------------------------------
    # Metadata
    # -------------------------------------------------------------------------

    fieldnames = [
        "site_id",
        "wyckoff",
        "environment",
        "removed_atom_index_0based",
        "removed_atom_index_1based",
        "frac_x",
        "frac_y",
        "frac_z",
        "cart_x_A",
        "cart_y_A",
        "cart_z_A",
        "supercell",
        "pristine_atoms",
        "defect_atoms",
        "charge",
        "filename",
    ]

    with metadata_file.open(
        "w",
        newline="",
    ) as handle:

        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(
            metadata
        )

    print()
    print("=" * 80)
    print("COMPLETE")
    print("=" * 80)

    print()
    print(
        f"Generated {len(metadata)} "
        f"symmetry-distinct neutral oxygen vacancies "
        f"for {args.supercell}."
    )

    print()
    print("Metadata:")
    print(f"  {metadata_file}")


if __name__ == "__main__":
    main()