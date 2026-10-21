#!/usr/bin/env python3
"""
substrate_response_test.py -- Is the missing acceleration a MEDIUM PROPERTY?
==============================================================================
Two routes, magnitudes first, then the decisive universality test.

P1 PRESSURE ROUTE (expected to fail):
   substrate pushes via dP/dr = rho_s * a_miss. Compute required |dP/dr|
   and implied pressure over disk scale. Compare against any measured
   interstellar pressure ceiling (magnetic + thermal ~ 1e-13 Pa at best).

P2 RESPONSE ROUTE (the decisive test):
   a_obs = f(a_bar) for ALL 78 anchors with ONE function.
   - Fit the two-regime response: a_obs = a_bar / (1 - exp(-sqrt(a_bar/a0)))
     with a single universal coupling scale a0.
   - Universality criterion: if per-galaxy residuals are tight (<15% scatter)
     with NO per-galaxy parameters, the missing acceleration is a FIELD
     PROPERTY of the medium (a response), not unseen mass.
   - Falsification: if a single f() cannot describe the population, the
     response route is dead and SRC is out of mechanisms. Log it.

Data: sparc_mass_models.txt (r, vobs, vbar), filtered to the 78 clean
fixed-ruler anchors from clean_db/clean_seed_database.csv when available.
"""

import os, math
import numpy as np
from collections import defaultdict

MASTER = "sparc_mass_models.txt"
CLEAN  = os.path.join("clean_db", "clean_seed_database.csv")
KPC    = 3.085677581e19   # m

def load_clean_names():
    """Names of the 78 fixed-ruler anchors, if the clean DB exists."""
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

def load_profiles(clean_names):
    rows = defaultdict(list)
    with open(MASTER) as fh:
        for line in fh:
            p = line.split()
            if len(p) < 8:
                continue
            try:
                r    = float(p[2]); vobs = float(p[3])
                vgas = float(p[5]); vdisk = float(p[6]); vbul = float(p[7])
            except ValueError:
                continue
            name = p[0].upper()
            if clean_names and name not in clean_names:
                continue
            vbar2 = vgas**2 + vdisk**2 + vbul**2
            if vobs > 0 and r > 0:
                rows[name].append((r, vobs, vbar2))
    return {k: np.array(v) for k, v in rows.items() if len(v) >= 4}

# ---------------------------------------------------------------- P1
def pressure_route(gals):
    """Required pressure gradient if the medium pushes. Real units."""
    print("=" * 70)
    print("P1 PRESSURE ROUTE -- can the medium PUSH hard enough?")
    print("=" * 70)
    r_m, a_miss = [], []
    for pts in gals.values():
        r, vobs, vbar2 = pts.T
        rm = r * KPC
        am = np.maximum(0.0, (vobs*1e3)**2 - vbar2*1e6) / rm
        r_m.append(rm); a_miss.append(am)
    rm  = np.concatenate(r_m); am = np.concatenate(a_miss)
    mid = (rm > 1*KPC) & (rm < 15*KPC)          # disk region only
    am_mid = am[mid]
    rho_s  = 1e-20                              # kg/m^3 generous substrate density
    dPdr   = rho_s * am_mid
    L      = 3.0 * KPC                          # disk scale height of the effect
    dP     = dPdr * L                           # total pressure drop across disk
    P_mag  = (5e-10)**2 / (2*4*np.pi*1e-7)       # 5 uG magnetic pressure [Pa]
    P_thm  = 1e-13                              # generous thermal/turbulent ceiling
    print(f"Substrate density assumed   : {rho_s:.0e} kg/m^3 (generous)")
    print(f"Typical a_miss in disk       : {np.median(am_mid):.2e} m/s^2")
    print(f"Required |dP/dr|            : {np.median(dPdr):.2e} Pa/m")
    print(f"Required pressure drop      : {np.median(dP):.2e} Pa")
    print(f"Best measured pressure      : ~{max(P_mag, P_thm):.2e} Pa (magnetic+thermal ceiling)")
    verdict_p1 = "PASS" if np.median(dP) < max(P_mag, P_thm) else "FAIL"
    print(f"P1 VERDICT                  : {verdict_p1} "
          f"(shortfall ~ {np.median(dP)/max(P_mag, P_thm):.0f}x)")
    print("-" * 70)

# ---------------------------------------------------------------- P2
def response_model(a_bar, a0):
    """Universal two-regime response: full baryonic response at high accel,
    sqrt-response (field polarization) at low accel."""
    return a_bar / (1.0 - np.exp(-np.sqrt(np.maximum(a_bar, 1e-30) / a0)))

def response_route(gals):
    print("P2 RESPONSE ROUTE -- is a_miss a universal property of the medium?")
    print("=" * 70)
    a_bar_all, a_obs_all = [], []
    for pts in gals.values():
        r, vobs, vbar2 = pts.T
        rm = r * KPC
        a_bar_all.append(vbar2*1e6 / rm)
        a_obs_all.append((vobs*1e3)**2 / rm)
    a_bar = np.concatenate(a_bar_all); a_obs = np.concatenate(a_obs_all)

    # ---- fit ONE universal a0 by minimizing residuals in log-space ----
    best, best_rms = None, np.inf
    for a0 in np.logspace(-12.5, -9.5, 200):     # m/s^2 scan, wide, no peeking
        pred = response_model(a_bar, a0)
        good = np.isfinite(pred) & (pred > 0)
        rms  = np.sqrt(np.mean((np.log10(pred[good]) - np.log10(a_obs[good]))**2))
        if rms < best_rms:
            best_rms, best = rms, a0

    pred = response_model(a_bar, best)
    good = np.isfinite(pred) & (pred > 0)
    # universality: per-galaxy scatter of log residuals
    print(f"Galaxies in test             : {len(gals)}")
    print(f"Radius points                : {good.sum()}")
    print(f"Universal coupling scale a0  : {best:.3e} m/s^2")
    print(f"Global RMS (dex)             : {best_rms:.3f}  "
          f"(~{10**best_rms:.2f}x typical scatter)")
    scat = []
    for name, pts in gals.items():
        r, vobs, vbar2 = pts.T
        rm = r * KPC
        ab = vbar2*1e6 / rm; ao = (vobs*1e3)**2 / rm
        pr = response_model(ab, best)
        ok = np.isfinite(pr) & (pr > 0)
        if ok.sum() >= 3:
            scat.append(np.std(np.log10(pr[ok]) - np.log10(ao[ok])))
    scat = np.array(scat)
    print(f"Per-galaxy residual scatter  : median {10**np.median(scat):.2f}x "
          f"| worst {10**scat.max():.2f}x")
    # two-regime signature check: slope of log(a_obs) vs log(a_bar) at low a_bar
    low  = a_bar < best
    if low.sum() > 100:
        slope_low = np.polyfit(np.log10(a_bar[low]), np.log10(a_obs[low]), 1)[0]
        print(f"Low-accel regime slope       : {slope_low:.2f} "
              f"(mass-like=1.0, response-like=0.5)")
    uni = (10**np.median(scat) < 1.15)   # <15% typical per-galaxy deviation
    print("-" * 70)
    print("FALSIFICATION (locked before run):")
    print(f"  F1 pressure route viable          : {'PASS' if verdict_p1=='PASS' else 'FAIL'}")
    print(f"  F2 ONE function fits all galaxies : {'PASS' if uni else 'FAIL'}")
    print("=" * 70)
    print("INTERPRETATION (printed only as logic, not as proof):")
    print("  If F2 passes: the missing acceleration behaves as a UNIVERSAL")
    print("  response of the medium to baryonic presence (coupling scale a0),")
    print("  NOT as per-galaxy unseen mass. That is a field property with a")
    print("  measured constant -- the first SRC-owned number. Next burden:")
    print("  derive a0 from medium physics, and test its external-field")
    print("  predictions (dwarf spheroidals, wide binaries).")
    print("  If F2 fails: response route joins the ledger. No mechanisms left.")
    print("=" * 70)
    return verdict_p1

if __name__ == "__main__":
    names = load_clean_names()
    gals  = load_profiles(names)
    if not gals:
        raise SystemExit("No clean anchor profiles found. Check files.")
    verdict_p1 = pressure_route(gals)
    response_route(gals)

