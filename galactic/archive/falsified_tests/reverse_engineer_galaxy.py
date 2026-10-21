#!/usr/bin/env python3
"""
reverse_engineer_galaxy.py -- v2: reads from the CLEAN DATABASE.
Reverse-engineers NGC 2403's mechanical demand profile.
Provenance labels on every quantity. No legacy files, no ghosts.
"""

import csv
import numpy as np

KPC_TO_M = 3.085677581e19
TARGET = "NGC2403"
D_MPC_TRGB = 3.16   # fixed geometric ruler (f_D=2) -- trusted anchor

def load_clean_galaxy(target=TARGET, db="clean_db/clean_seed_database.csv"):
    rows = []
    with open(db) as fh:
        for row in csv.DictReader(fh):
            if row["galaxy"].strip().upper() != target:
                continue
            try:
                rows.append((float(row["r_kpc"]), float(row["v_obs_kms"]),
                             float(row["v_gas_kms"]), float(row["v_disk_kms"]),
                             float(row["v_bulge_kms"])))
            except (ValueError, TypeError):
                continue
    return np.array(sorted(rows))

def main():
    data = load_clean_galaxy()
    if len(data) < 5:
        raise SystemExit(f"FATAL: {TARGET} not found or too sparse in clean DB. Hard stop.")
    r_kpc, v_obs, v_gas, v_disk, v_bul = data.T

    r_m  = r_kpc * KPC_TO_M
    v_ms = v_obs * 1e3

    # [Direct Evidence] -- total mechanical demand of the orbit (pure geometry)
    a_total = v_ms**2 / r_m

    # [Deduced, flagged provenance] -- SPARC baryonic contribution:
    # v_gas is He-corrected (1.33); v_disk/v_bul are M/L=1 GRAVITATIONAL models.
    # Used only to locate the residual; the residual itself is the measured fact.
    v_bar2 = v_gas**2 + v_disk**2 + v_bul**2
    a_bary = (v_bar2 * 1e6) / r_m

    # [Direct Evidence] -- what the medium must supply, per unit mass, per radius
    a_med = a_total - a_bary

    print("=" * 72)
    print(f"REVERSE ENGINEERING {TARGET}  (D = {D_MPC_TRGB} Mpc, TRGB fixed ruler)")
    print("=" * 72)
    print(f"{'R (kpc)':>7} | {'V_obs':>6} | {'a_total':>10} | {'a_bary':>10} | {'a_medium':>10} | med/total")
    print("-" * 72)
    for i in range(0, len(r_kpc), max(1, len(r_kpc)//12)):
        frac = a_med[i] / a_total[i] if a_total[i] > 0 else 0
        print(f"{r_kpc[i]:>7.2f} | {v_obs[i]:>6.1f} | {a_total[i]:>10.2e} | "
              f"{a_bary[i]:>10.2e} | {a_med[i]:>10.2e} | {frac:>7.1%}")
    print("-" * 72)

    # Outer-disk demand shape: fit log(a_med) vs log(r) in the outer half
    half = len(r_kpc) // 2
    lr, la = np.log10(r_m[half:]), np.log10(np.maximum(a_med[half:], 1e-30))
    slope = np.polyfit(lr, la, 1)[0]
    print(f"Outer-disk medium-demand exponent: a_med ~ r^{slope:+.2f}")
    print(f"  (a_med ~ r^-1 = flat-V 1/R demand;  r^-2 = Keplerian)")
    print("=" * 72)
    print("PROVENANCE: r,v_obs = Doppler+TRGB [Direct]. a_bary carries SPARC's")
    print("M/L=1 gravitational model [flagged]; residual demand is the measured fact.")
    print("=" * 72)

if __name__ == "__main__":
    main()

