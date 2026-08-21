from pathlib import Path
import re

HARTREE_TO_EV = 27.211386245988
N_FORMULA_UNITS = 3

ROOT = Path(__file__).resolve().parents[2]

BASE_DIR = ROOT / "workflows" / "cp2k" / "convergence" / "01_basis"

CALCULATIONS = {
    "DZVP": BASE_DIR / "dzvp" / "igzo_basis_dzvp.out",
    "TZVP": BASE_DIR / "tzvp" / "igzo_basis_tzvp.out",
    "TZV2P": BASE_DIR / "tzv2p" / "igzo_basis_tzv2p.out",
}


def extract_energy(path):
    text = path.read_text(errors="ignore")

    matches = re.findall(
        r"ENERGY\|\s+Total FORCE_EVAL.*?([-+]?\d+\.\d+)",
        text,
    )

    if not matches:
        raise RuntimeError(f"No CP2K energy found in {path}")

    return float(matches[-1])


def main():
    results = []

    for basis, path in CALCULATIONS.items():
        energy_ha = extract_energy(path)
        energy_ev = energy_ha * HARTREE_TO_EV
        energy_fu = energy_ev / N_FORMULA_UNITS

        results.append(
            {
                "basis": basis,
                "energy_ha": energy_ha,
                "energy_fu_ev": energy_fu,
            }
        )

    reference = results[-1]["energy_fu_ev"]

    print()
    print("=" * 78)
    print("CP2K IGZO BASIS CONVERGENCE")
    print("=" * 78)
    print(
        f"{'Basis':<10}"
        f"{'Energy / Ha':>20}"
        f"{'E / f.u. / eV':>22}"
        f"{'ΔE vs TZV2P / meV/f.u.':>26}"
    )
    print("-" * 78)

    for result in results:
        delta_mev = (
            result["energy_fu_ev"] - reference
        ) * 1000.0

        print(
            f"{result['basis']:<10}"
            f"{result['energy_ha']:>20.10f}"
            f"{result['energy_fu_ev']:>22.8f}"
            f"{delta_mev:>26.3f}"
        )

    print("=" * 78)
    print()


if __name__ == "__main__":
    main()