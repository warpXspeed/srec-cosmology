#!/usr/bin/env python3
"""
derive_scaling_law.py -- Extract the required medium density per galaxy
and test whether it follows a tight scaling law with galactic size.
"""

import csv
import numpy as np

def derive_scaling(summary_csv="audit_output/audit_summary.csv"):
    names, b_outer, r_max = [], [], []
    with open(summary_csv, "r") as fh:
        for row in csv.DictReader(fh):
            try:
                b = float(row["B_outer_max_uG"])
                r = float(row["r_max_kpc"])
            except (ValueError, TypeError):
                continue
            names.append(row["galaxy"]); b_outer.append(b); r_max.append(r)

    b_outer, r_max = np.array(b_outer), np.array(r_max)

    # Required rho to bring each galaxy exactly to the 1.0 uG ceiling
    mask = b_outer > 0.01
    rho_req = 1.0e-24 * (1.0 / b_outer[mask])**2
    r_sel = r_max[mask]

    # Test scaling: log(rho_req) vs log(r_max)  ->  rho_req ~ r_max^alpha
    log_r = np.log10(r_sel)
    log_rho = np.log10(rho_req)
    alpha, logC = np.polyfit(log_r, log_rho, 1)
    pred = alpha * log_r + logC
    ss_res = np.sum((log_rho - pred)**2)
    ss_tot = np.sum((log_rho - np.mean(log_rho))**2)
    r2 = 1.0 - ss_res / ss_tot

    print("=" * 65)
    print("MEDIUM DENSITY SCALING LAW EXTRACTION")
    print("=" * 65)
    print(f"Galaxies used                : {mask.sum()}")
    print(f"Power-law index alpha        : {alpha:.3f}")
    print(f"Fit quality R^2              : {r2:.3f}")
    print(f"Implied scaling              : rho_req ~ r_max^{alpha:.2f}")
    print(f"Density range                : {rho_req.min():.2e} to {rho_req.max():.2e} kg/m^3")
    print("=" * 65)
    if r2 > 0.7:
        print("VERDICT: TIGHT LAW. The medium density is a smooth function of")
        print("galactic scale. The 'constant' is dead; the scaling law is measured.")
    elif r2 > 0.4:
        print("VERDICT: MODERATE TREND. Scaling exists but a second variable")
        print("(gas fraction, surface brightness) is likely involved.")
    else:
        print("VERDICT: SCATTERED. Required density is not a single-parameter law.")
    print("=" * 65)

if __name__ == "__main__":
    derive_scaling()

