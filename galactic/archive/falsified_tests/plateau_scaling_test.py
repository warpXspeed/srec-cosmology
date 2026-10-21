#!/usr/bin/env python3
"""
plateau_scaling_test.py -- Instrumented version.
What does the medium's yield stress track?
"""

import csv
import numpy as np
from collections import defaultdict

KPC_TO_M = 3.085677581e19

def main(db="clean_db/clean_seed_database.csv"):
    print(f"Reading database from: {db}")
    galaxies = defaultdict(list)
    
    try:
        with open(db, "r") as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                try:
                    r  = float(row["r_kpc"])
                    v  = float(row["v_obs_kms"])
                    vg = float(row["v_gas_kms"])
                    vd = float(row["v_disk_kms"])
                    vb = float(row["v_bulge_kms"])
                except (ValueError, TypeError):
                    continue
                if r > 0 and v > 0:
                    galaxies[row["galaxy"]].append((r, v, vg, vd, vb))
    except FileNotFoundError:
        print(f"ERROR: Could not find {db}. Did you run build_clean_seed_db.py?")
        return

    print(f"Loaded {len(galaxies)} galaxy entries from clean DB.")

    p_val, a_bar_out, r_max, v_max = [], [], [], []
    skipped = []
    
    for name, pts in galaxies.items():
        arr = np.array(sorted(pts))
        r, v, vg, vd, vb = arr.T
        if len(r) < 8:
            skipped.append(name)
            continue
            
        r_m   = r * KPC_TO_M
        a_tot = (v*1e3)**2 / r_m
        a_bar = ((vg**2 + vd**2 + vb**2) * 1e6) / r_m
        a_med = a_tot - a_bar

        n_out = max(3, len(r)//3)
        a_med_o, a_bar_o = a_med[-n_out:], a_bar[-n_out:]
        
        if np.any(a_med_o <= 0) or np.mean(a_bar_o) <= 0:
            skipped.append(name)
            continue

        p_val.append(float(np.median(a_med_o)))
        a_bar_out.append(float(np.median(a_bar_o)))
        r_max.append(float(r[-1]))
        v_max.append(float(np.max(v)))

    print(f"Successfully calculated plateaus for {len(p_val)} galaxies (Skipped: {len(skipped)}).")

    if len(p_val) < 5:
        print("ERROR: Too few valid galaxies to run regression.")
        return

    p, ab, rm, vm = map(np.array, (p_val, a_bar_out, r_max, v_max))

    def logfit(x, y):
        lx, ly = np.log10(x), np.log10(y)
        s, c = np.polyfit(lx, ly, 1)
        r2 = 1 - np.sum((ly-(s*lx+c))**2)/np.sum((ly-ly.mean())**2)
        return s, r2

    s_bar, r2_bar   = logfit(ab, p)
    s_size, r2_size = logfit(rm, p)
    s_vel, r2_vel   = logfit(vm, p)

    print("=" * 72)
    print("PLATEAU SCALING TEST -- what does the medium's yield stress track?")
    print("=" * 72)
    print(f"Galaxies in test                : {len(p)}")
    print(f"Plateau vs baryonic demand  : slope {s_bar:+.3f}   R^2 {r2_bar:.3f}")
    print(f"Plateau vs size (Rmax)      : slope {s_size:+.3f}   R^2 {r2_size:.3f}")
    print(f"Plateau vs speed (Vmax)      : slope {s_vel:+.3f}   R^2 {r2_vel:.3f}")
    print("=" * 72)

    if r2_bar > r2_size and r2_bar > r2_vel:
        print(f"DOMINANT DRIVER: baryonic demand (slope {s_bar:+.2f}).")
        if 0.3 < s_bar < 0.7:
            print("  -> Sqrt(strain) coupling. Elastic-saturation signature.")
        elif s_bar < 0.15:
            print("  -> Effectively flat: universal stress constant.")
        else:
            print("  -> Near-linear strain coupling.")
    elif r2_size > r2_bar and r2_size > r2_vel:
        print(f"DOMINANT DRIVER: vortex scale (slope {s_size:+.2f}).")
    else:
        print(f"DOMINANT DRIVER: velocity scale (slope {s_vel:+.2f}).")
    print("=" * 72)

if __name__ == "__main__":
    main()

