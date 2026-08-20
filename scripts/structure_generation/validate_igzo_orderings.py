from pathlib import Path
from itertools import combinations

from pymatgen.core import Structure
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
from pymatgen.analysis.structure_matcher import StructureMatcher


ROOT = Path(__file__).resolve().parents[2]

MODELS_DIR = (
    ROOT
    / "structures"
    / "crystalline"
    / "ordered_models"
)


EXPECTED_COMPOSITION = {
    "In": 3,
    "Ga": 3,
    "Zn": 3,
    "O": 12,
}

EXPECTED_ATOMS = 21

DISTANCE_WARNING_THRESHOLD = 1.2  # Å


def load_models():
    models = []

    for model_dir in sorted(MODELS_DIR.glob("igzo_crystal_ordered_*")):
        if not model_dir.is_dir():
            continue

        cif_files = list(model_dir.glob("*.cif"))

        if not cif_files:
            print(f"WARNING: No CIF found in {model_dir.name}")
            continue

        cif_path = cif_files[0]

        structure = Structure.from_file(cif_path)

        models.append(
            {
                "id": model_dir.name,
                "path": cif_path,
                "structure": structure,
            }
        )

    return models


def check_composition(structure):
    composition = structure.composition.get_el_amt_dict()

    errors = []

    for element, expected in EXPECTED_COMPOSITION.items():
        actual = composition.get(element, 0)

        if abs(actual - expected) > 1e-8:
            errors.append(
                f"{element}: expected {expected}, found {actual}"
            )

    unexpected = set(composition) - set(EXPECTED_COMPOSITION)

    if unexpected:
        errors.append(
            f"Unexpected elements: {sorted(unexpected)}"
        )

    return errors


def minimum_distance(structure):
    min_distance = float("inf")
    min_pair = None

    for i, j in combinations(range(len(structure)), 2):

        distance = structure.get_distance(i, j)

        if distance < min_distance:
            min_distance = distance
            min_pair = (i, j)

    return min_distance, min_pair


def get_symmetry(structure):
    analyzer = SpacegroupAnalyzer(
        structure,
        symprec=1e-3,
        angle_tolerance=5,
    )

    return (
        analyzer.get_space_group_symbol(),
        analyzer.get_space_group_number(),
    )


def validate_model(model):
    structure = model["structure"]

    errors = []
    warnings = []

    if len(structure) != EXPECTED_ATOMS:
        errors.append(
            f"Expected {EXPECTED_ATOMS} atoms, found {len(structure)}"
        )

    if not structure.is_ordered:
        errors.append("Structure contains partial occupancies.")

    composition_errors = check_composition(structure)
    errors.extend(composition_errors)

    min_distance, min_pair = minimum_distance(structure)

    if min_distance < DISTANCE_WARNING_THRESHOLD:
        warnings.append(
            f"Very short distance: {min_distance:.3f} Å "
            f"between sites {min_pair}"
        )

    sg_symbol, sg_number = get_symmetry(structure)

    return {
        "id": model["id"],
        "atoms": len(structure),
        "formula": structure.composition.formula,
        "ordered": structure.is_ordered,
        "min_distance": min_distance,
        "space_group": f"{sg_symbol} ({sg_number})",
        "errors": errors,
        "warnings": warnings,
    }


def check_lattice_consistency(models):
    reference = models[0]["structure"].lattice

    problems = []

    for model in models[1:]:
        lattice = model["structure"].lattice

        lengths_match = all(
            abs(a - b) < 1e-6
            for a, b in zip(reference.abc, lattice.abc)
        )

        angles_match = all(
            abs(a - b) < 1e-6
            for a, b in zip(reference.angles, lattice.angles)
        )

        if not lengths_match or not angles_match:
            problems.append(model["id"])

    return problems


def check_model_uniqueness(models):
    matcher = StructureMatcher(
        primitive_cell=False,
        scale=False,
        attempt_supercell=False,
    )

    duplicates = []

    for i in range(len(models)):
        for j in range(i + 1, len(models)):

            structure_a = models[i]["structure"]
            structure_b = models[j]["structure"]

            if matcher.fit(structure_a, structure_b):
                duplicates.append(
                    (models[i]["id"], models[j]["id"])
                )

    return duplicates


def print_results(results):
    print()
    print("=" * 100)
    print("IGZO ORDERED STRUCTURE VALIDATION")
    print("=" * 100)

    header = (
        f"{'Model':32}"
        f"{'Atoms':>8}"
        f"{'Ordered':>10}"
        f"{'Min dist / Å':>15}"
        f"{'Space group':>20}"
    )

    print(header)
    print("-" * 100)

    for result in results:
        print(
            f"{result['id']:32}"
            f"{result['atoms']:>8}"
            f"{str(result['ordered']):>10}"
            f"{result['min_distance']:>15.3f}"
            f"{result['space_group']:>20}"
        )

    print("=" * 100)
    print()

    for result in results:
        print(result["id"])
        print(f"  Formula: {result['formula']}")

        if result["errors"]:
            print("  ERRORS:")
            for error in result["errors"]:
                print(f"    - {error}")
        else:
            print("  Errors: none")

        if result["warnings"]:
            print("  WARNINGS:")
            for warning in result["warnings"]:
                print(f"    - {warning}")
        else:
            print("  Warnings: none")

        print()


def main():
    models = load_models()

    if not models:
        raise RuntimeError(
            f"No ordered models found in {MODELS_DIR}"
        )

    print(f"Found {len(models)} ordered IGZO models.")

    results = [
        validate_model(model)
        for model in models
    ]

    print_results(results)

    lattice_problems = check_lattice_consistency(models)

    if lattice_problems:
        print("LATTICE CONSISTENCY: FAIL")
        print(
            "The following models do not have the same lattice as "
            "model 001:"
        )

        for model_id in lattice_problems:
            print(f"  - {model_id}")
    else:
        print("LATTICE CONSISTENCY: PASS")

    print()

    duplicates = check_model_uniqueness(models)

    if duplicates:
        print("STRUCTURE UNIQUENESS: WARNING")
        print(
            "StructureMatcher considers the following models equivalent:"
        )

        for model_a, model_b in duplicates:
            print(f"  - {model_a} <-> {model_b}")
    else:
        print("STRUCTURE UNIQUENESS: PASS")

    print()

    failures = sum(
        bool(result["errors"])
        for result in results
    )

    if failures == 0 and not lattice_problems:
        print("OVERALL VALIDATION: PASS")
    else:
        print("OVERALL VALIDATION: FAIL")

    print()


if __name__ == "__main__":
    main()