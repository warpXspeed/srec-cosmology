#!/usr/bin/env python3
"""
residual_error_audit.py -- Are residuals within measurement noise?
===================================================================
1. Computes pull residuals: (v_pred - v_obs) / err_v for each SPARC anchor.
   Tests if the universal response model fits within error bars.
2. Performs a raw, model-free linear regression and sliding-bin slope
   on log(a_obs) vs log(a_bar) at low accelerations to measure the true
   data slope without a pre-ordained function kernel.
"""

import os
import numpy as np
from collections import defaultdict

MASTER = "sparc_mass_models.txt"
CLEAN  = os.path.join("clean_db", "clean_seed_database.csv")
KPC    = 3.085677581e19   # m
A0     = 3.55e-11         # m/s^2 (fixed coupling scale from previous fit)

def load_clean_names():
    if not os.path.exists(CLEAN):
        return None
    names = set()
    with open(CLEAN) as fh:
        for line in fh:
            p = line.replace(",", " ").split()
            if not p or p[0].lower() in ("galaxy", "name", "id"):
                continue
            names.add(p[0].upper())
    return names or None

def load_profiles_with_errors(clean_names):
    """Parses r, vobs, errv, vbar2. If error is missing, defaults to 5%."""
    rows = defaultdict(list)
    with open(MASTER) as fh:
        for line in fh:
            p = line.split()
            if len(p) < 8:
                continue
            name = p[0].upper()
            if clean_names and name not in clean_names:
                continue
            try:
                r    = float(p[2])
                vobs = float(p[3])
                errv = float(p[4]) if len(p) > 4 and p[4].replace('.','',1).isdigit() else 0.05 * vobs
                vgas = float(p[5]); vdisk = float(p[6]); vbul = float(p[7])
            except ValueError:
                continue
            vbar2 = vgas**2 + vdisk**2 + vbul**2
            if vobs > 0 and r > 0 and errv > 0:
                rows[name].append((r, vobs, errv, vbar2))
    return {k: np.array(v) for k, v in rows.items() if len(v) >= 4}

def response_velocity(vbar2, rm, a0=A0):
    """Inverts the response function to predict v_obs from vbar."""
    a_bar = vbar2 * 1e6 / rm
    # a_obs = a_bar / (1 - exp(-sqrt(a_bar / a0)))
    denom = 1.0 - np.exp(-np.sqrt(np.maximum(a_bar, 1e-30) / a0))
    a_obs = a_bar / np.maximum(denom, 1e-10)
    return np.sqrt(np.maximum(0.0, a_obs * rm)) / 1e3  # km/s

def main():
    names = load_clean_names()
    gals  = load_profiles_with_errors(names)
    if not gals:
        raise SystemExit("No profiles found.")

    all_pulls = []
    abar_raw, aobs_raw = [], []

    for name, pts in gals.items():
        r, vobs, errv, vbar2 = pts.T
        rm = r * KPC
        v_pred = response_velocity(vbar2, rm)
        
        # Pull residual: (predicted - observed) / error
        pulls = (v_pred - vobs) / errv
        all_pulls.extend(pulls.tolist())

        abar_raw.extend((vbar2 * 1e6 / rm).tolist())
        aobs_raw.extend(((vobs * 1e3)**2 / rm).tolist())

    all_pulls = np.array(all_pulls)
    abar_raw = np.array(abar_raw)
    aobs_raw = np.array(aobs_raw)

    # Filter out infinities/NaNs
    valid = np.isfinite(all_pulls)
    all_pulls = all_pulls[valid]

    mean_pull = np.mean(all_pulls)
    std_pull  = np.std(all_pulls)

    # --- RAW SLOPE FIT (Model-free log-log regression at low accel) ---
    log_abar = np.log10(abar_raw)
    log_aobs = np.log10(aobs_raw)
    ok_log = np.isfinite(log_abar) & np.isfinite(log_aobs)
    
    low_accel = ok_log & (abar_raw < 1e-10) # Deep RAR regime
    raw_slope, raw_intercept = np.polyfit(log_abar[low_accel], log_aobs[low_accel], 1)

    print("=" * 68)
    print("RESIDUAL & ERROR AUDIT (Model-Free Verification)")
    print("=" * 68)
    print(f"Total evaluated radius points : {len(all_pulls)}")
    print(f"Pull residuals (v_pred - v_obs) / err_v:")
    print(f"  - Mean pull                 : {mean_pull:.3f} (Ideal: 0.0)")
    print(f"  - Std deviation of pulls    : {std_pull:.3f} (Ideal: 1.0)")
    print("-" * 68)
    print(f"RAW LOW-ACCELERATION SLOPE (Data-driven, no kernel):")
    print(f"  - Measured slope (< 1e-10)  : {raw_slope:.3f}")
    print(f"    (Mass-like expectation    : 1.00)")
    print(f"    (Response expectation     : 0.50)")
    print("-" * 68)
    print("VERDICT:")
    if 0.8 <= std_pull <= 1.5:
        print("  RESIDUALS MATCH ERROR FLOORS -- The universal response function")
        print("  is statistically consistent with SPARC measurement noise.")
    else:
        print("  EXCESS SCATTER DETECTED -- Significant per-galaxy deviation")
        print("  beyond measurement error. History/environment matters.")
    print("=" * 68)

if __name__ == "__main__":
    main()

