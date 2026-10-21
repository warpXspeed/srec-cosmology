#!/usr/bin/env python3
"""
analyze_clean_acceleration.py -- Raw acceleration scaling on geometric anchors.
"""

import csv
import numpy as np
from collections import defaultdict

def analyze_clean_db(db_path="clean_db/clean_seed_database.csv"):
    galaxies = defaultdict(list)
    
    with open(db_path, "r") as fh:
        for row in csv.DictReader(fh):
            name = row["galaxy"]
            try:
                r = float(row["r_kpc"])
                v = float(row["v_obs_kms"])
            except ValueError:
                continue
            if r > 0 and v > 0:
                galaxies[name].append((r, v))

    print(f"Loaded {len(galaxies)} clean galaxies for raw acceleration analysis.")
    
    # Calculate effective power-law slope (v^2/r ~ r^alpha) for each clean galaxy
    slopes = []
    for name, pts in galaxies.items():
        if len(pts) < 5:
            continue
        arr = np.array(pts)
        r, v = arr[:, 0], arr[:, 1]
        
        # Centripetal acceleration proxy: v^2 / r
        accel = (v**2) / r
        
        # Fit log(accel) vs log(r) to find local decay exponent alpha
        log_r = np.log10(r)
        log_a = np.log10(accel)
        
        slope, _ = np.polyfit(log_r, log_a, 1)
        slopes.append(slope)

    slopes = np.array(slopes)
    print("=" * 65)
    print("RAW ACCELERATION DECAY ANALYSIS (Fixed-Ruler Anchors)")
    print("=" * 65)
    print(f"Galaxies analyzed with >= 5 points : {len(slopes)}")
    print(f"Mean acceleration decay exponent  : {slopes.mean():.3f} (Newtonian point-mass = -2.0)")
    print(f"Median acceleration decay exponent: {np.median(slopes):.3f}")
    print("=" * 65)
    print("If this exponent clusters significantly shallower than -2.0 (e.g., -1.0),")
    print("nature is enforcing a 1/R vortex geometry across clean local space.")

if __name__ == "__main__":
    analyze_clean_db()

