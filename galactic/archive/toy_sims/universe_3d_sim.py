#!/usr/bin/env python3
"""
universe_3d_sim.py -- Real-data force-balance test (replaces toy census).

No intermediate CSVs for derived quantities. One REAL data input is required
for the decisive test: b_measured.csv (Faraday-RM B-field), columns:
    name, r_kpc, B_mug
If absent, the script falls back to a DERIVED B (Ampere inversion of a_need)
and flags the force-balance ratio as self-consistency ONLY, not a physical test.

Outputs: predicted-vs-observed residuals, force-balance ratio, KE-scale fit,
and an explicit falsification verdict. No census labels.
"""
import os
import numpy as np
from collections import defaultdict

# --- Physical constants (SI) ---
KPC   = 3.085677581e19          # m
MSUN  = 1.989e30                # kg
MUG   = 1e-10                   # T per microgauss
GMU0  = 4 * np.pi * 1e-7        # H/m
RHO_GCM3_TO_KGM3 = 1000.0       # 1 g/cm^3 = 1000 kg/m^3
DISK_H = 0.15 * KPC             # midplane scaleheight (flagged assumption)

MASTER  = "sparc_mass_models.txt"
TABLE1  = "SPARC - Mass Models.txt"
B_MEAS  = "b_measured.csv"

# SPARC master tokens: 0=name 2=r 3=vobs 5=vgas 6=vdisk 7=vbul
# Table 1 tokens: 0=name 9=rgas 10=SBeff 11=Mgas 15=Vflat


def load_master():
    rows = defaultdict(list)
    with open(MASTER) as fh:
        for line in fh:
            p = line.split()
            if len(p) < 8:
                continue
            try:
                r = float(p[2]); vobs = float(p[3])
                vgas = float(p[5]); vdisk = float(p[6]); vbul = float(p[7])
            except ValueError:
                continue
            rows[p[0].upper()].append((r, vobs, vgas, vdisk, vbul))
    return rows


def load_table1():
    t = {}
    with open(TABLE1) as fh:
        for line in fh:
            p = line.split()
            if len(p) < 17 or p[0] in ("Title:", "Authors:", "Table:", "Byte-by-byte"):
                continue
            try:
                rgas = float(p[9]); mgas = float(p[11]); vflat = float(p[15])
            except ValueError:
                continue
            if mgas > 0 and rgas > 0 and vflat > 0:
                t[p[0].upper()] = (rgas, mgas, vflat)
    return t


def load_b_measured():
    """Real Faraday-RM B-field. Returns {name: (r_kpc[], B_mug[])}. Empty if absent."""
    out = {}
    if not os.path.exists(B_MEAS):
        return out
    tmp = defaultdict(list)
    with open(B_MEAS) as fh:
        for line in fh:
            p = line.split()
            if len(p) < 3:
                continue
            try:
                r = float(p[1]); b = float(p[2])
            except ValueError:
                continue
            tmp[p[0].upper()].append((r, b))
    for k, v in tmp.items():
        a = np.array(v, float)
        out[k] = (a[:, 0], a[:, 1])
    return out


def derived_b_mug(r_kpc, vobs, vgas, vdisk, vbul):
    """Ampere inversion of a_need -> B in microgauss. DERIVED, not measured."""
    r_m = r_kpc * KPC
    vbar2 = (vgas**2 + vdisk**2 + vbul**2) * 1e6
    a_need = np.maximum(0.0, (vobs * 1e3)**2 - vbar2) / (r_m + 1e-9)
    integ = a_need * r_m**2
    integral = np.cumsum(np.concatenate(([0.0], 0.5 * (integ[1:] + integ[:-1]) * np.diff(r_m))))
    i_enc = np.sqrt(np.maximum(0.0, (8 * np.pi**2 / GMU0) * integral))
    b_t = GMU0 * i_enc / (2 * np.pi * (r_m + 1e-9))
    return b_t / MUG  # microgauss


def gas_density_kgm3(r_kpc, mgas_msun, rgas_kpc):
    """Exponential disk surface density -> midplane volume density. [Deduced]"""
    r_m = r_kpc * KPC
    rg = rgas_kpc * KPC
    mg = mgas_msun * MSUN
    sigma = mg / (2 * np.pi * rg**2) * np.exp(-r_m / rg)   # kg/m^2
    return sigma / DISK_H                                  # kg/m^3


def fit(y, x):
    a, c = np.polyfit(x, y, 1)
    pred = a * x + c
    ss_res = np.sum((y - pred)**2)
    ss_tot = np.sum((y - y.mean())**2)
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
    n = len(x)
    dof = max(n - 2, 1)
    chi2 = ss_res / dof
    return a, r2, chi2


def main():
    master = load_master()
    t1 = load_table1()
    bmeas = load_b_measured()
    b_mode = "MEASURED (Faraday RM)" if bmeas else "DERIVED (Ampere inversion) -- NOT A MEASUREMENT"

    ratios = []          # per-radius F_mag / F_centr
    ke_m, ke_e = [], []
    n_gal = 0
    n_b_meas = 0

    for name, pts in master.items():
        if name not in t1:
            continue
        rgas, mgas, vflat = t1[name]
        arr = np.array(pts, float)
        r_kpc, vobs, vgas, vdisk, vbul = arr.T
        if len(r_kpc) < 4:
            continue
        n_gal += 1

        # --- B field ---
        if name in bmeas:
            r_b, b_mug = bmeas[name]
            # interpolate measured B onto the master radius grid
            b_grid = np.interp(r_kpc, np.sort(r_b), b_mug[np.argsort(r_b)])
            n_b_meas += 1
        else:
            b_grid = derived_b_mug(r_kpc, vobs, vgas, vdisk, vbul)

        r_m = r_kpc * KPC
        v_ms = vobs * 1e3
        rho = gas_density_kgm3(r_kpc, mgas, rgas)
        b_t = b_grid * MUG

        # --- Force balance (no gravity assumed) ---
        # J ~ B/r (toroidal B, poloidal current), F_mag = J*B
        j = b_t / np.maximum(r_m, 1e-9)
        f_mag = j * b_t
        f_centr = rho * v_ms**2 / np.maximum(r_m, 1e-9)
        good = np.isfinite(f_mag) & np.isfinite(f_centr) & (f_centr > 0) & (f_mag > 0)
        ratios.extend((f_mag[good] / f_centr[good]).tolist())

        # --- KE-scale ---
        m_enc = mgas * 0.5  # [flagged] stellar mass not in this minimal path
        ke_m.append(m_enc)
        ke_e.append(0.5 * m_enc * vflat**2)

    ratios = np.array(ratios)
    med_ratio = float(np.median(ratios)) if ratios.size else float("nan")

    # --- KE-scale fit: log(KE) = beta*log(M) ---
    ke_m = np.array(ke_m); ke_e = np.array(ke_e)
    fin = np.isfinite(ke_m) & np.isfinite(ke_e) & (ke_m > 0) & (ke_e > 0)
    beta, ke_r2, ke_chi2 = fit(np.log10(ke_e[fin]), np.log10(ke_m[fin]))

    # --- Control run: Birkeland term = 0 ---
    # If J=0 then F_mag=0 -> ratio=0. Demonstrates the term's contribution.
    control_ratio = 0.0

    # --- Falsification condition ---
    FALSIFY_IF = 0.01
    verdict = ("FALSIFIED: Birkeland term dynamically negligible"
               if med_ratio < FALSIFY_IF else
               "NOT FALSIFIED by force balance: ratio >= threshold")

    print("=" * 68)
    print("REAL-DATA FORCE-BALANCE TEST (replaces 3D census)")
    print("=" * 68)
    print(f"Galaxies in loop              : {n_gal}")
    print(f"Galaxies with MEASURED B      : {n_b_meas}")
    print(f"B-field source                : {b_mode}")
    print(f"Per-radius ratios computed    : {ratios.size}")
    print("-" * 68)
    print(f"Median F_mag/F_centr          : {med_ratio:.3e}")
    print(f"  (F_mag = J*B, J~B/r ; F_centr = rho*v^2/r)")
    print(f"Control run (Birkeland=0)     : ratio = {control_ratio:.1e}")
    print("-" * 68)
    print(f"KE-scale beta (logKE/logM)    : {beta:.3f}")
    print(f"KE-scale R^2                  : {ke_r2:.3f}")
    print(f"KE-scale chi^2/dof            : {ke_chi2:.3f}")
    print("-" * 68)
    print(f"Falsification threshold       : ratio < {FALSIFY_IF}")
    print(f"VERDICT                       : {verdict}")
    print("=" * 68)
    if not bmeas:
        print("NOTE: No measured B supplied. Force-balance ratio is a")
        print("      self-consistency check on DERIVED B, NOT a physical test.")
        print("      Supply b_measured.csv (name, r_kpc, B_mug) for the real test.")
    print("=" * 68)


if __name__ == "__main__":
    main()
