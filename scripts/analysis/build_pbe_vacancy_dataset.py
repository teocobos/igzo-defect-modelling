#!/usr/bin/env python3
from pathlib import Path
import shutil
import pandas as pd
import matplotlib.pyplot as plt

HA_TO_EV = 27.211386245988

ROOT = Path(__file__).resolve().parents[2]
VALIDATION = ROOT / "results/crystalline/oxygen_vacancies/validation"
OUT = ROOT / "results/crystalline/oxygen_vacancies/pbe"
ENERGY_FILE = OUT / "vacancy_tight_energies.csv"

SITES = {
    "O001": "Ga3Zn1",
    "O002": "In3Zn1",
    "O003": "In3Ga1",
    "O004": "Ga1Zn3",
}

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "figures").mkdir(exist_ok=True)
    (OUT / "relaxed_structures").mkdir(exist_ok=True)

    energies = pd.read_csv(ENERGY_FILE)
    if set(energies["site"]) != set(SITES):
        raise ValueError("vacancy_tight_energies.csv must contain O001-O004 exactly once.")

    e0 = energies.loc[energies["site"] == "O004", "tight_static_energy_Ha"].iloc[0]
    energies["environment"] = energies["site"].map(SITES)
    energies["relative_energy_eV"] = (energies["tight_static_energy_Ha"] - e0) * HA_TO_EV
    energies = energies[["site", "environment", "tight_static_energy_Ha", "relative_energy_eV"]]
    energies.to_csv(OUT / "vacancy_energy_summary.csv", index=False)

    first_shell_all = []
    localisation_all = []

    for site in SITES:
        src = VALIDATION / f"{site}_4x4_gamma_ot"
        fs = pd.read_csv(src / f"{site}_4x4_gamma_ot_first_shell_summary.csv")
        fs.insert(0, "site", site)
        first_shell_all.append(fs)

        loc = pd.read_csv(src / f"{site}_4x4_gamma_ot_localisation_by_radius.csv")
        loc.insert(0, "site", site)
        localisation_all.append(loc)

        relaxed_dir = OUT / "relaxed_structures" / site
        relaxed_dir.mkdir(parents=True, exist_ok=True)
        for ext in ("cif", "xyz"):
            source = src / f"{site}_4x4_gamma_ot_relaxed.{ext}"
            if source.exists():
                shutil.copy2(source, relaxed_dir / source.name)

    first_shell = pd.concat(first_shell_all, ignore_index=True)
    first_shell.to_csv(OUT / "vacancy_first_shell_summary.csv", index=False)

    localisation = pd.concat(localisation_all, ignore_index=True)
    localisation.to_csv(OUT / "vacancy_localisation_summary.csv", index=False)

    structural_rows = []
    for site in SITES:
        fs = first_shell[first_shell["site"] == site]
        loc6 = localisation[
            (localisation["site"] == site) &
            (localisation["radius_A"].round(6) == 6.0)
        ]

        row = {
            "site": site,
            "environment": SITES[site],
            "max_first_shell_displacement_A": fs["max_displacement_A"].max(),
        }
        if not loc6.empty:
            row["max_displacement_outside_6A_A"] = loc6["max_displacement_outside_A"].iloc[0]
            row["mean_displacement_outside_6A_A"] = loc6["mean_displacement_outside_A"].iloc[0]
        structural_rows.append(row)

    pd.DataFrame(structural_rows).to_csv(
        OUT / "vacancy_structural_summary.csv", index=False
    )

    # Relative energies
    plt.figure(figsize=(6.5, 4.2))
    plt.bar(energies["site"], energies["relative_energy_eV"])
    plt.xlabel("Oxygen vacancy site")
    plt.ylabel("Relative energy (eV)")
    plt.tight_layout()
    plt.savefig(OUT / "figures/vacancy_relative_energies.png", dpi=200)
    plt.close()

    # First-shell radial changes
    plt.figure(figsize=(7.0, 4.5))
    for element in ("Ga", "In", "Zn", "O"):
        subset = first_shell[first_shell["element"] == element]
        if not subset.empty:
            plt.plot(
                subset["site"],
                subset["mean_radial_change_A"],
                marker="o",
                label=element,
            )
    plt.axhline(0.0, linewidth=0.8)
    plt.xlabel("Oxygen vacancy site")
    plt.ylabel("Mean radial change (Å)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUT / "figures/vacancy_first_shell_relaxation.png", dpi=200)
    plt.close()

    # Maximum first-shell displacement
    structural = pd.read_csv(OUT / "vacancy_structural_summary.csv")
    plt.figure(figsize=(6.5, 4.2))
    plt.bar(structural["site"], structural["max_first_shell_displacement_A"])
    plt.xlabel("Oxygen vacancy site")
    plt.ylabel("Maximum first-shell displacement (Å)")
    plt.tight_layout()
    plt.savefig(OUT / "figures/vacancy_displacement_comparison.png", dpi=200)
    plt.close()

    print("\nFinal PBE neutral-vacancy ranking")
    print("---------------------------------")
    print(energies.to_string(index=False, float_format=lambda x: f"{x:.6f}"))
    print(f"\nDataset written to: {OUT}")

if __name__ == "__main__":
    main()
