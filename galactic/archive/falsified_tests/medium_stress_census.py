#!/usr/bin/env python3
"""
medium_stress_census.py -- Extract the outer-disk a_medium plateau for all 78
clean anchors and test whether the medium's yield stress is universal.
Provenance: a_bary carries SPARC M/L=1 flag; the plateau SHAPE is robust,
the plateau VALUE shifts if M/L differs. We report both honestly.
"""

import csv
import numpy as np
from collections import defaultdict

KPC_TO_M = 3.085677581e19

def main(db="clean_db/clean_seed_database.csv"):
    galaxies = defaultdict(list)
    with open(db) as fh:
        for row in csv.DictReader(fh):
            try:
                r  = float(row["r_kpc"]);    v  = float(row["v_obs_kms"])
                vg = float(row["v_gas_kms"]); vd = float(row["v_disk_kms"])
                vb = float(row["v_bulge_kms"])
            except (ValueError, TypeError):
                continue
            if r > 0 and v > 0:
                galaxies[row["galaxy"]].append((r, v, vg, vd, vb))

    plateau_vals, names = [], []
    skipped = []
    for name, pts in galaxies.items():
        arr = np.array(sorted(pts))
        r, v, vg, vd, vb = arr.T
        if len(r) < 8:
            skipped.append(name); continue

        r_m  = r * KPC_TO_M
        a_tot = (v*1e3)**2 / r_m
        a_bar = ((vg**2 + vd**2 + vb**2) * 1e6) / r_m
        a_med = a_tot - a_bar

        # Outer third of the disk: measure the plateau (median) and its flatness
        n_out = max(3, len(r)//3)
        a_out = a_med[-n_out:]
        if np.any(a_out <= 0):
            skipped.append(name); continue   # baryon model exceeds demand out there: logged

        plateau  = float(np.median(a_out))
        flatness = float(np.std(a_out) / np.mean(a_out))  # <0.3 = true plateau

        if plateau > 0:
            plateau_vals.append(plateau); names.append((name, plateau, flatness))

    pv = np.array(plateau_vals)
    print("=" * 72)
    print("MEDIUM STRESS CENSUS -- outer-disk a_medium plateau, 78 clean anchors")
    print("=" * 72)
    if skipped:
        print(f"Excluded (sparse or baryon-model exceeds demand; logged): {len(skipped)}")
    print(f"Galaxies with measurable plateau : {len(pv)}")
    print(f"Plateau value  mean : {pv.mean():.3e} m/s^2")
    print(f"                  median : {np.median(pv):.3e}")
    print(f"                  min    : {pv.min():.3e}")
    print(f"                  max    : {pv.max():.3e}")
    print(f"                  scatter: {pv.std()/pv.mean()*100:.0f}%")
    print("=" * 72)
    flat = [f for _,_,f in names if f < 0.3]
    print(f"Galaxies whose outer demand is a true plateau (flatness<30%): {len(flat)}/{len(names)}")
    print("=" * 72)

    if pv.std()/pv.mean() < 0.3:
        print("VERDICT: UNIVERSAL STRESS CONSTANT. The medium yields one number")
        print("across all fixed-ruler galaxies. The lattice shows its scale.")
    elif 0.3 <= pv.std()/pv.mean() < 0.8:
        print("VERDICT: STRUCTURED VARIATION. Plateau correlates with galaxy")
        print("properties -> next step: plateau vs (size, Vmax).")
    else:
        print("VERDICT: SCATTERED. No single medium stress scale. Log honestly.")
    print("=" * 72)

if __name__ == "__main__":
    main()

