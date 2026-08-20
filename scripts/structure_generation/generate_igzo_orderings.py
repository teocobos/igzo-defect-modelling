########################################################################
#  Generate structures for InGaZnO4 structures for the 4 inequivalent  #
#  sites                                                               #
#                                                                      #
#  Teo Cobos                                                           #
#  21/08/2026                                                          #
#  python3                                                             #
########################################################################


from pathlib import Path
from itertools import combinations

from pymatgen.core import Structure
from pymatgen.io.cif import CifParser, CifWriter
from pymatgen.io.vasp import Poscar
from pymatgen.io.xyz import XYZ
from pymatgen.analysis.structure_matcher import StructureMatcher


ROOT = Path(__file__).resolve().parents[2]

INPUT_CIF = (
    ROOT
    / "structures"
    / "crystalline"
    / "reference"
    / "igzo_crystal_ingazno4_cod1521670.cif"
)

OUTPUT_DIR = (
    ROOT
    / "structures"
    / "crystalline"
    / "ordered_models"
)


def load_structure():
    parser = CifParser(INPUT_CIF)
    structures = parser.parse_structures(primitive=False)

    if not structures:
        raise RuntimeError("No structure could be read from the CIF.")

    return structures[0]


def find_mixed_ga_zn_sites(structure):
    mixed_sites = []

    for i, site in enumerate(structure):
        species = site.species

        has_ga = "Ga" in species
        has_zn = "Zn" in species

        if has_ga and has_zn:
            mixed_sites.append(i)

    return mixed_sites


def generate_orderings(structure, mixed_indices):
    """
    Generate every possible 3 Ga / 3 Zn assignment for the six
    mixed Ga/Zn positions.
    """

    n_sites = len(mixed_indices)

    if n_sites != 6:
        raise RuntimeError(
            f"Expected 6 mixed Ga/Zn sites, found {n_sites}."
        )

    structures = []

    for ga_positions in combinations(range(n_sites), 3):

        ordered = structure.copy()

        ga_positions = set(ga_positions)

        for local_index, structure_index in enumerate(mixed_indices):

            if local_index in ga_positions:
                ordered.replace(structure_index, "Ga")
            else:
                ordered.replace(structure_index, "Zn")

        structures.append(ordered)

    return structures


def remove_symmetry_duplicates(structures):
    """
    Group chemically equivalent structures using pymatgen's
    StructureMatcher.
    """

    matcher = StructureMatcher(
        primitive_cell=False,
        scale=False,
        attempt_supercell=False,
    )

    groups = matcher.group_structures(structures)

    representatives = [group[0] for group in groups]

    return representatives, groups


def validate_model(structure):

    composition = structure.composition.get_el_amt_dict()

    expected = {
        "In": 3,
        "Ga": 3,
        "Zn": 3,
        "O": 12,
    }

    for element, number in expected.items():
        found = composition.get(element, 0)

        if abs(found - number) > 1e-8:
            raise ValueError(
                f"Invalid composition: expected {element}={number}, "
                f"found {found}"
            )

    if not structure.is_ordered:
        raise ValueError("Generated structure remains disordered.")


def write_model(structure, model_number):

    model_id = f"igzo_crystal_ordered_{model_number:03d}"

    model_dir = OUTPUT_DIR / model_id
    model_dir.mkdir(parents=True, exist_ok=True)

    cif_path = model_dir / f"{model_id}.cif"
    vasp_path = model_dir / f"{model_id}.vasp"
    xyz_path = model_dir / f"{model_id}.xyz"

    CifWriter(structure).write_file(cif_path)

    Poscar(structure).write_file(vasp_path)

    XYZ(structure).write_file(xyz_path)

    print(f"Wrote {model_id}")


def main():

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    structure = load_structure()

    print("Input structure")
    print("----------------")
    print(f"Formula: {structure.composition}")
    print(f"Number of sites: {len(structure)}")
    print(f"Ordered: {structure.is_ordered}")
    print()

    mixed_indices = find_mixed_ga_zn_sites(structure)

    print(f"Mixed Ga/Zn sites: {len(mixed_indices)}")

    for index in mixed_indices:
        site = structure[index]

        print(
            index,
            site.species,
            site.frac_coords,
        )

    print()

    all_orderings = generate_orderings(
        structure,
        mixed_indices,
    )

    print(f"Raw orderings: {len(all_orderings)}")

    representatives, groups = remove_symmetry_duplicates(
        all_orderings
    )

    print(
        f"Symmetry-distinct orderings: "
        f"{len(representatives)}"
    )

    for i, group in enumerate(groups, start=1):
        print(
            f"Model {i:03d}: "
            f"{len(group)} equivalent raw assignments"
        )

    print()

    for i, model in enumerate(representatives, start=1):

        validate_model(model)

        write_model(
            model,
            i,
        )

    print()
    print("Generation complete.")


if __name__ == "__main__":
    main()