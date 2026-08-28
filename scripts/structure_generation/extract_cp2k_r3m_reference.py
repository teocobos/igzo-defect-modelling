#!/usr/bin/env python3

"""
Extract the final high-precision structure from a CP2K restart file
and write canonical XYZ and CIF files for the IGZO crystalline reference.
"""

from pathlib import Path
import re

from pymatgen.core import Lattice, Structure
from pymatgen.io.cif import CifWriter
from pymatgen.io.xyz import XYZ
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer


ROOT = Path(__file__).resolve().parents[2]

REFERENCE_DIR = (
    ROOT
    / "structures"
    / "crystalline"
    / "cell_relaxed"
    / "igzo_crystal_ordered_003_r3m_cell_relaxed"
)

RESTART_FILE = REFERENCE_DIR / "igzo_ordered_003_cell_opt-1.restart"

XYZ_FILE = (
    REFERENCE_DIR
    / "igzo_crystal_ordered_003_r3m_cell_relaxed.xyz"
)

CIF_FILE = (
    REFERENCE_DIR
    / "igzo_crystal_ordered_003_r3m_cell_relaxed.cif"
)


def parse_cp2k_restart(path):
    text = path.read_text()

    # -------------------------------------------------------------
    # Extract first &CELL block.
    #
    # This deliberately ignores &CELL_REF later in the restart.
    # -------------------------------------------------------------

    cell_match = re.search(
        r"&CELL\s*\n(.*?)&END CELL",
        text,
        flags=re.S,
    )

    if cell_match is None:
        raise RuntimeError("Could not locate &CELL block.")

    cell_text = cell_match.group(1)

    vectors = {}

    for label in ("A", "B", "C"):

        match = re.search(
            rf"^\s*{label}\s+"
            r"([-+0-9.Ee]+)\s+"
            r"([-+0-9.Ee]+)\s+"
            r"([-+0-9.Ee]+)",
            cell_text,
            flags=re.M,
        )

        if match is None:
            raise RuntimeError(
                f"Could not extract lattice vector {label}."
            )

        vectors[label] = [
            float(match.group(1)),
            float(match.group(2)),
            float(match.group(3)),
        ]

    # -------------------------------------------------------------
    # Extract &COORD block.
    # -------------------------------------------------------------

    coord_match = re.search(
        r"&COORD\s*\n(.*?)&END COORD",
        text,
        flags=re.S,
    )

    if coord_match is None:
        raise RuntimeError("Could not locate &COORD block.")

    coord_text = coord_match.group(1)

    species = []
    coordinates = []

    for line in coord_text.splitlines():

        fields = line.split()

        if len(fields) != 4:
            continue

        element = fields[0]

        if element not in {"In", "Ga", "Zn", "O"}:
            continue

        species.append(element)

        coordinates.append(
            [
                float(fields[1]),
                float(fields[2]),
                float(fields[3]),
            ]
        )

    if len(species) != 21:
        raise RuntimeError(
            f"Expected 21 atoms but extracted {len(species)}."
        )

    lattice = Lattice(
        [
            vectors["A"],
            vectors["B"],
            vectors["C"],
        ]
    )

    structure = Structure(
        lattice=lattice,
        species=species,
        coords=coordinates,
        coords_are_cartesian=True,
        to_unit_cell=True,
    )

    return structure


def report_symmetry(structure):

    print("=" * 72)
    print("FINAL R3m REFERENCE STRUCTURE")
    print("=" * 72)

    print()
    print("Lattice")
    print(f"a     = {structure.lattice.a:.10f} Å")
    print(f"b     = {structure.lattice.b:.10f} Å")
    print(f"c     = {structure.lattice.c:.10f} Å")
    print(f"alpha = {structure.lattice.alpha:.10f} deg")
    print(f"beta  = {structure.lattice.beta:.10f} deg")
    print(f"gamma = {structure.lattice.gamma:.10f} deg")
    print(f"V     = {structure.volume:.10f} Å^3")

    print()
    print("Symmetry tolerance scan")
    print(
        f"{'symprec / Å':>14}"
        f"{'space group':>18}"
        f"{'number':>10}"
    )

    for symprec in [
        1e-5,
        5e-5,
        1e-4,
        5e-4,
        1e-3,
        2e-3,
        5e-3,
        1e-2,
    ]:

        sga = SpacegroupAnalyzer(
            structure,
            symprec=symprec,
            angle_tolerance=5,
        )

        print(
            f"{symprec:>14.6g}"
            f"{sga.get_space_group_symbol():>18}"
            f"{sga.get_space_group_number():>10}"
        )


def main():

    structure = parse_cp2k_restart(RESTART_FILE)

    report_symmetry(structure)

    # XYZ retains the exact relaxed Cartesian coordinates.
    XYZ(structure).write_file(XYZ_FILE)

    # Use the tolerance that already recovered R3m reliably.
    writer = CifWriter(
        structure,
        symprec=2e-3,
    )

    writer.write_file(CIF_FILE)

    print()
    print("Written:")
    print(XYZ_FILE)
    print(CIF_FILE)


if __name__ == "__main__":
    main()