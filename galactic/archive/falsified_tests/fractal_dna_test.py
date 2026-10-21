#!/usr/bin/env python3
"""
fractal_dna_test.py -- Searching for the scaling signature.
Tests if Kinetic Energy (V^2) scales consistently with Radius (R) 
across our 78 geometric anchor galaxies.
"""

import csv
import numpy as np
from collections import defaultdict

def test_fractal_dna(db="clean_db/clean_seed_database.csv"):
    galaxies = defaultdict(list)
    with open(db) as fh:
        for row in csv.DictReader(fh):
            try:
                r, v = float(row["r_kpc"]), float(row["v_obs_kms"])
            except ValueError:
                continue
            galaxies[row["galaxy"]].append((r, v))

    # We extract the 'Fingerprint': Max Velocity and Max Radius for each galaxy
    # This represents the 'total energy state' of the vortex.
    radii, velocities = [], []
    for name, pts in galaxies.items():
        arr = np.array(pts)
        radii.append(np.max(arr[:, 0]))
        velocities.append(np.max(arr[:, 1]))

    R = np.array(radii)
    V = np.array(velocities)
    
    # Energy is proportional to V^2
    # Fractal scaling: V^2 ~ R^beta
    log_r = np.log10(R)
    log_e = np.log10(V**2)
    
    slope, intercept = np.polyfit(log_r, log_e, 1)
    r2 = 1 - np.sum((log_e - (slope*log_r + intercept))**2) / np.sum((log_e - log_e.mean())**2)

    print("=" * 65)
    print("FRACTAL DNA TEST -- Scaling of Kinetic Energy vs. Scale")
    print("=" * 65)
    print(f"Number of galaxies tested    : {len(R)}")
    print(f"Energy-Scale Exponent (beta) : {slope:.3f}")
    print(f"Fractal Correlation (R^2)    : {r2:.3f}")
    print("=" * 65)
    
    if r2 > 0.7:
        print("RESULT: STRONG FRACTAL SIGNATURE.")
        print(f"The galaxies share a common energy-scaling law (beta={slope:.2f}).")
        print("Nature uses a consistent 'DNA' to build these vortices.")
    else:
        print("RESULT: SCATTERED.")
        print("The galaxies do not share a single energy-scaling law.")
        print("The 'vortex' behaves differently at different scales.")
    print("=" * 65)

if __name__ == "__main__":
    test_fractal_dna()

