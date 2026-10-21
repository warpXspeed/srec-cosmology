#!/usr/bin/env python3
"""
analyze_velocity_profile.py -- Inspects clean V(r) profiles for fluid/drag signatures.
"""

import csv
import numpy as np
from collections import defaultdict

def analyze_velocities(db_path="clean_db/clean_seed_database.csv"):
    galaxies = defaultdict(list)
    with open(db_path) as fh:
        for row in csv.DictReader(fh):
            try:
                r, v = float(row["r_kpc"]), float(row["v_obs_kms"])
            except (ValueError, TypeError):
                continue
            if r > 0 and v > 0:
                galaxies[row["galaxy"]].append((r, v))

    print(f"Analyzing velocity profiles for {len(galaxies)} clean galaxies...")

    # Classify the outer-disk behavior for each galaxy:
    # Does V rise, stay flat, or drop in the outer half of the measured disk?
    flat_count = 0
    rising_count = 0
    dropping_count = 0

    for name, pts in galaxies.items():
        if len(pts) < 6:
            continue
        arr = np.array(sorted(pts))
        r, v = arr[:, 0], arr[:, 1]
        
        # Look at the outer half of the points
# Look at the outer half of the points
        half = len(r) // 2
        r_outer, v_outer = r[half:], v[half:]
        
        if len(r_outer) < 3:
            continue
            
        # Fit a simple line to outer velocity vs radius: v = m*r + c
        m, _ = np.polyfit(r_outer, v_outer, 1)
        
        # Normalize slope relative to average velocity
        relative_slope = m / np.mean(v_outer)
        
        if abs(relative_slope) < 0.02:  # velocity is stable/flat
            flat_count += 1
        elif relative_slope > 0.02:    # velocity keeps rising
            rising_count += 1
        else:                          # velocity drops
            dropping_count += 1

    total = flat_count + rising_count + dropping_count
    print("=" * 65)
    print("OUTER-DISK VELOCITY BEHAVIOR (78 Fixed-Ruler Galaxies)")
    print("=" * 65)
    print(f"Total classified galaxies    : {total}")
    print(f"Flat velocity profiles       : {flat_count} ({flat_count/total*100:.1f}%)")
    print(f"Rising velocity profiles     : {rising_count} ({rising_count/total*100:.1f}%)")
    print(f"Dropping velocity profiles   : {dropping_count} ({dropping_count/total*100:.1f}%)")
    print("=" * 65)
    print("Physics Interpretation:")
    print("In a vacuum (Newtonian), velocities must drop (Keplerian decline).")
    print("In a fluid medium with core drive and outer momentum transfer,")
    print("velocities hold flat or sustain against drag.")
    print("=" * 65)

if __name__ == "__main__":
    analyze_velocities()

