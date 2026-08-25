########################################################################
#  Convert .xyz structures to .cif                                     #
#                                                                      #
#                                                                      #
#  Teo Cobos                                                           #
#  25/08/2026                                                          #
#  python3                                                             #
#  pymatgen                                                            #
########################################################################


from pathlib import Path

from pymatgen.core import Structure, Lattice
from pymatgen.io.xyz import XYZ


ROOT = Path(__file__).resolve().parents[2]

RELAXED_ROOT = (
    ROOT
    / "structures"
    / "crystalline"
    / "relaxed"
)

MODELS = [
    "001",
    "003",
]

LATTICE = Lattice([
    [3.2990000000, 0.0000000000, 0.0000000000],
    [-1.6495000000, 2.8570178071, 0.0000000000],
    [0.0000000000, 0.0000000000, 26.1010000000],
])


def convert_model(model):
    model_id = f"igzo_crystal_ordered_{model}_relaxed"

    model_dir = RELAXED_ROOT / model_id

    xyz_path = model_dir / f"{model_id}.xyz"
    cif_path = model_dir / f"{model_id}.cif"

    if not xyz_path.exists():
        raise FileNotFoundError(
            f"Relaxed XYZ not found: {xyz_path}"
        )

    xyz = XYZ.from_file(xyz_path)
    molecule = xyz.molecule

    structure = Structure(
        LATTICE,
        molecule.species,
        molecule.cart_coords,
        coords_are_cartesian=True,
        to_unit_cell=True,
    )

    structure.to(filename=cif_path)

    print(f"{model_id}")
    print(f"  atoms:   {len(structure)}")
    print(f"  formula: {structure.composition.formula}")
    print(f"  output:  {cif_path}")
    print()


def main():
    for model in MODELS:
        convert_model(model)


if __name__ == "__main__":
    main()