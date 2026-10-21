#!/usr/bin/env python3
"""
analyze_flat_vs_rising.py -- Compares physical traits of flat vs rising galaxies.
"""

import csv
import numpy as np
from collections import defaultdict

def classify_and_compare(db_path="clean_db/clean_seed_database.csv"):
    galaxies = defaultdict(list)
    with open(db_path, "r") as fh:
        for row in csv.DictReader(fh):
            try:
                r, v = float(row["r_kpc"]), float(row["v_obs_kms"])
            except (ValueError, TypeError):
                continue
            if r > 0 and v > 0:
                galaxies[row["galaxy"]].append((r, v))

    flat_metrics = []
    rising_metrics = []

    for name, pts in galaxies.items():
        if len(pts) < 6:
            continue
        arr = np.array(sorted(pts))
        r, v = arr[:, 0], arr[:, 1]
        
        half = len(r) // 2
        r_outer, v_outer = r[half:], v[half:]
        if len(r_outer) < 3:
            continue
            
        m, _ = np.polyfit(r_outer, v_outer, 1)
        rel_slope = m / np.mean(v_outer)
        
        max_r = r[-1]
        max_v = np.max(v)
        
        profile_data = {"name": name, "max_r": max_r, "max_v": max_v}
        
        if abs(rel_slope) < 0.02:
            flat_metrics.append(profile_data)
        elif rel_slope >= 0.02:
            rising_metrics.append(profile_data)

    print("=" * 65)
    print("FLAT VS. RISING PROFILE PHYSICAL COMPARISON (Fixed-Ruler Anchors)")
    print("=" * 65)
    print(f"Flat profiles count   : {len(flat_metrics)}")
    print(f"Rising profiles count : {len(rising_metrics)}")
    
    if flat_metrics and rising_metrics:
        flat_r = np.mean([x["max_r"] for x in flat_metrics])
        rising_r = np.mean([x["max_r"] for x in rising_metrics])
        flat_v = np.mean([x["max_v"] for x in flat_metrics])
        rising_v = np.mean([x["max_v"] for x in rising_metrics])
        
        print(f"\nAverage Outer Extent (R_max):")
        print(f"  Flat   : {flat_r:.2f} kpc")
        print(f"  Rising : {rising_r:.2f} kpc")
        
        print(f"\nAverage Maximum Velocity (V_max):")
        print(f"  Flat   : {flat_v:.2f} km/s")
        print(f"  Rising : {rising_v:.2f} km/s")
    print("=" * 65)

if __name__ == "__main__":
    classify_and_compare()

