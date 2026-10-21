#!/usr/bin/env python3
"""
fit_two_variable_law.py -- Self-contained. No intermediate CSVs.
Reads raw SPARC sources only:
  1. sparc_mass_models.txt  -> recompute B_phi per galaxy, median of outer disk
  2. SPARC - Mass Models.txt -> Vflat (token 15), SBeff (token 10)
Fits log(rho_req) = a*log(V) + b*log(SBeff) + c, plus velocity-only fit.
Everything unmeasured is logged and excluded. No substitutions.
"""

import numpy as np
from collections import defaultdict

MU0 = 4 * np.pi * 1e-7
KPC = 3.085677581e19
RHO0 = 1.0e-24
OUTER_FRAC = 0.70

VFLAT_IDX, SBEFF_IDX = 15, 10

def compute_median_outer_b(master_file="sparc_mass_models.txt"):
    """Parse master file, run the same solver equations, return median outer-disk B per galaxy."""
    rows = defaultdict(list)
    with open(master_file) as fh:
        for line in fh:
            parts = line.split()
            if len(parts) < 8:
                continue
            try:
                name = parts[0]
                r  = float(parts[2]);  vobs = float(parts[3])
                vgas = float(parts[5]); vdisk = float(parts[6]); vbul = float(parts[7])
            except ValueError:
                continue
            rows[name].append((r, vobs, vgas, vdisk, vbul))

    med_b = {}
    for name, pts in rows.items():
        if len(pts) < 4:
            continue
        arr = np.array(pts, dtype=float)
        r, vobs, vgas, vdisk, vbul = arr.T
        vbar2 = vdisk**2 + vgas**2 + vbul**2          # same as audit (no re-correction)
        r_m = r * KPC
        a_need = np.maximum(0.0, (vobs*1e3)**2 - vbar2*1e6) / (r_m + 1e-9)
        integ = RHO0 * a_need * r_m**2
        integral = np.cumsum(np.concatenate(([0.0],
                  0.5*(integ[1:]+integ[:-1])*np.diff(r_m))))
        i_enc = np.sqrt(np.maximum(0.0, (8*np.pi**2/MU0)*integral))
        b_ug = (MU0 * i_enc / (2*np.pi*(r_m+1e-9))) * 1e10
        outer = r >= OUTER_FRAC * r.max()
        sel = b_ug[outer]
        sel = sel[np.isfinite(sel) & (sel > 0)]
        if sel.size >= 3:
            med_b[name.upper()] = float(np.median(sel))
    return med_b

def load_table1(table1_file="SPARC - Mass Models.txt"):
    vflat, sbeff, skipped = {}, {}, []
    with open(table1_file) as fh:
        for line in fh:
            parts = line.split()
            if len(parts) < 17 or parts[0] in ("Title:", "Authors:", "Table:", "Byte-by-byte"):
                continue
            name = parts[0].upper()
            try:
                v = float(parts[VFLAT_IDX]); s = float(parts[SBEFF_IDX])
            except (ValueError, IndexError):
                continue
            if v > 0 and s > 0:
                vflat[name] = v; sbeff[name] = s
            else:
                skipped.append(parts[0])
    return vflat, sbeff, skipped

def main():
    med_b = compute_median_outer_b()
    vflat, sbeff, skipped = load_table1()
    print(f"Median outer-B computed for {len(med_b)} galaxies from raw master file.")
    print(f"Table 1 usable: {len(vflat)} | unmeasured logged & excluded: {len(skipped)}")

    v, s, lr = [], [], []
    unmatched = []
    for g, b in med_b.items():
        if g not in vflat or g not in sbeff:
            unmatched.append(g); continue
        v.append(vflat[g]); s.append(sbeff[g])
        lr.append(np.log10(RHO0 * (1.0/b)**2))

    v = np.array(v); s = np.array(s); lr = np.array(lr)
    lv, ls = np.log10(v), np.log10(s)
    print(f"Matched for fit: {len(v)} | unmatched (logged): {len(unmatched)}")

    finite = np.isfinite(lv) & np.isfinite(ls) & np.isfinite(lr)
    lv, ls, lr = lv[finite], ls[finite], lr[finite]

    a1, c1 = np.polyfit(lv, lr, 1)
    r2_1 = 1 - np.sum((lr-(a1*lv+c1))**2)/np.sum((lr-lr.mean())**2)

    X = np.column_stack([lv, ls, np.ones_like(lv)])
    coef, *_ = np.linalg.lstsq(X, lr, rcond=None)
    r2_2 = 1 - np.sum((lr - X@coef)**2)/np.sum((lr-lr.mean())**2)

    print("=" * 65)
    print("TWO-VARIABLE SCALING TEST (self-contained, median-B estimator)")
    print("=" * 65)
    print(f"Fit 1  rho ~ V^{a1:.3f}                R^2 = {r2_1:.3f}")
    print(f"Fit 2  rho ~ V^{coef[0]:.3f} * SBeff^{coef[1]:.3f}   R^2 = {r2_2:.3f}")
    print(f"        improvement from surface density: +{r2_2-r2_1:.3f}")
    print("=" * 65)

    if r2_1 > 0.8:
        print("VERDICT: Velocity law is tight once estimator noise is removed.")
    elif r2_2 - r2_1 > 0.2:
        print("VERDICT: Surface density is the real second variable.")
    else:
        print("VERDICT: Residual scatter is genuine per-galaxy physics or geometry.")
    print("=" * 65)

if __name__ == "__main__":
    main()

