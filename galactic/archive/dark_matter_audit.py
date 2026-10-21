#!/usr/bin/env python3
"""
dark_matter_audit.py -- The Shadow Observatory
================================================
Level-5 audit engine for the SRC/DFM electrodynamic rotation hypothesis.

Pipeline:
  1. Parse REAL SPARC master mass model (sparc_mass_models.txt). No synthetic data.
  2. Compute model-free rotation deficit:
         dV2(r) = Vobs^2 - Vbar^2
         Vbar^2 = (1.33 * Vgas)^2 + Vdisk^2 + Vbul^2
  3. Integrate enclosed current I_enc(r) and azimuthal magnetic field B_phi(r)
     directly from the acceleration gap using the real physical equations
     (mirroring inverse_current_solver_v2-2.py).
  4. Faraday audit check across real galaxy sample against 0.5 uG (strict)
     and 1.0 uG (nominal) outer-disk ceilings.
"""

import argparse
import csv
import os
import re
import sys
from dataclasses import dataclass, field
from typing import List, Optional

import numpy as np

# Physical and conversion constants
MU0 = 4 * np.pi * 1e-7
KPC_TO_M = 3.0856775814913673e19
KM_S2_TO_M_S2 = 1.0e6
RHO_BASELINE = 1.0e-24  # kg/m^3 ISM baseline mass-equivalent of field stress

B_CEILING_STRICT_U_G = 0.5
B_CEILING_NOMINAL_U_G = 1.0
OUTER_RADIUS_FRACTION = 0.70
MIN_POINTS = 4

@dataclass
class GalaxyProfile:
    name: str
    d_mpc: Optional[float] = None
    # rows: (r_kpc, v_obs, e_vobs, v_gas, v_disk, v_bul)
    rows: List[tuple] = field(default_factory=list)

    def arrays(self):
        r = np.array([row[0] for row in self.rows], dtype=float)
        vobs = np.array([np.nan if row[1] is None else row[1] for row in self.rows])
        err = np.array([np.nan if row[2] is None else row[2] for row in self.rows])
        vgas = np.array([0.0 if row[3] is None else row[3] for row in self.rows])
        vdisk = np.array([0.0 if row[4] is None else row[4] for row in self.rows])
        vbul = np.array([0.0 if row[5] is None else row[5] for row in self.rows])
        return r, vobs, err, vgas, vdisk, vbul

def parse_sparc_master(path: str) -> List[GalaxyProfile]:
    galaxies: List[GalaxyProfile] = []
    cur: Optional[GalaxyProfile] = None

    with open(path, "r") as fh:
        for lineno, raw in enumerate(fh, 1):
            line = raw.strip()
            if not line:
                continue
            # Skip header / comment block lines unless they name a galaxy or separator
            if line.startswith("Title:") or line.startswith("Authors:") or line.startswith("Table:") or line.startswith("Byte-by-byte") or line.startswith("---") or "Explanations" in line:
                continue

            # Data rows in sparc_mass_models.txt start with Galaxy ID (e.g. CamB, D512-2)
            toks = line.split()
            if len(toks) >= 8:
                # Check if second token is a float (Distance D)
                try:
                    name = toks[0]
                    d_val = float(toks[1])
                    r_val = float(toks[2])
                    vobs_val = float(toks[3])
                    evobs_val = float(toks[4])
                    vgas_val = float(toks[5])
                    vdisk_val = float(toks[6])
                    vbul_val = float(toks[7])
                except ValueError:
                    continue

                if cur is None or cur.name != name:
                    if cur is not None and len(cur.rows) >= MIN_POINTS:
                        galaxies.append(cur)
                    cur = GalaxyProfile(name=name, d_mpc=d_val)

                cur.rows.append((r_val, vobs_val, evobs_val, vgas_val, vdisk_val, vbul_val))

    if cur is not None and len(cur.rows) >= MIN_POINTS:
        galaxies.append(cur)

    if not galaxies:
        raise SystemExit(f"FATAL: zero valid galaxy blocks parsed from {path}. Hard stop.")
    return galaxies

def solve_electrodynamics(r_kpc, v_obs, v_gas, v_disk, v_bul):
    """Computes I_enc and B_phi using the physical first-principles solver engine."""
    # SPARC Vgas includes the 1.33 helium factor on velocity contribution
    v_bar_sq = v_disk**2 + v_gas**2 + v_bul**2
    v_bar = np.sqrt(np.maximum(0.0, v_bar_sq))

    r_meters = r_kpc * KPC_TO_M
    v_obs_ms = v_obs * 1000.0
    v_bar_ms = v_bar * 1000.0

    a_needed = np.maximum(0.0, (v_obs_ms**2 - v_bar_ms**2) / (r_meters + 1e-9))

    integrand = RHO_BASELINE * a_needed * r_meters**2
    integral = np.zeros_like(r_meters)
    if len(r_meters) > 1:
        integral[1:] = np.cumsum(0.5 * (integrand[1:] + integrand[:-1]) * np.diff(r_meters))

    i_enc = np.sqrt(np.maximum(0.0, (8 * np.pi**2 / MU0) * integral))
    b_phi = MU0 * i_enc / (2 * np.pi * (r_meters + 1e-9))
    b_phi_ug = b_phi * 1e10  # Tesla to microGauss

    return v_bar, a_needed, i_enc, b_phi_ug

def audit_galaxy(prof: GalaxyProfile) -> dict:
    r, vobs, err, vg, vd, vb = prof.arrays()
    n_meas = len(r)

    if n_meas < MIN_POINTS:
        return {"name": prof.name, "verdict": "EXCLUDED", "reason": f"Only {n_meas} points"}

    v_bar, a_anom, i_enc, b_phi = solve_electrodynamics(r, vobs, vg, vd, vb)

    vbar2 = v_bar**2
    dv2 = vobs**2 - vbar2
    sigma = 2.0 * vobs * err
    with np.errstate(invalid="ignore", divide="ignore"):
        sn = np.where(sigma > 0, dv2 / sigma, np.nan)

    outer = r >= OUTER_RADIUS_FRACTION * r.max()
    if not outer.any():
        return {"name": prof.name, "verdict": "NO_OUTER_POINTS", "reason": "No outer radii"}

    b_outer_max = float(np.nanmax(b_phi[outer]))
    if b_outer_max > B_CEILING_NOMINAL_U_G:
        verdict = "FAIL_NOMINAL"
    elif b_outer_max > B_CEILING_STRICT_U_G:
        verdict = "MARGINAL"
    else:
        verdict = "PASS"

    return {
        "name": prof.name,
        "verdict": verdict,
        "n_points": n_meas,
        "r_max_kpc": float(r.max()),
        "max_deficit_sn": float(np.nanmax(sn[outer])) if np.isfinite(sn[outer]).any() else np.nan,
        "a_anom_outer_max": float(np.nanmax(a_anom[outer])),
        "B_outer_max_uG": b_outer_max,
        "B_global_max_uG": float(np.nanmax(b_phi)),
        "_radii": {
            "r_kpc": r, "v_obs": vobs, "err": err,
            "v_bar": v_bar, "dv2": dv2, "sn": sn,
            "a_anom": a_anom, "i_enc": i_enc, "b_phi": b_phi,
            "outer": outer,
        }
    }

def print_honest_summary(results):
    n = len(results)
    tally = {"PASS": 0, "MARGINAL": 0, "FAIL_NOMINAL": 0, "NO_OUTER_POINTS": 0, "EXCLUDED": 0}
    for res in results:
        v = res["verdict"]
        if v in tally:
            tally[v] += 1

    print("=" * 72)
    print("THE SHADOW OBSERVATORY -- SPARC Master Mass Model Faraday Audit")
    print("=" * 72)
    print(f"Galaxies audited         : {n}")
    for k, val in tally.items():
        print(f"  {k:<18}: {val}")

    fails = [r for r in results if r["verdict"].startswith("FAIL")]
    print(f"\n-- Faraday Audit Failures (> {B_CEILING_NOMINAL_U_G} uG nominal ceiling) --")
    if not fails:
        print("  None")
    for r in fails[:10]:
        print(f"  {r['name']:<12} B_outer_max = {r['B_outer_max_uG']:.2f} uG")
    if len(fails) > 10:
        print(f"  ... and {len(fails) - 10} more.")
    print("=" * 72)

def main():
    ap = argparse.ArgumentParser(description="Shadow Observatory: SPARC Master Audit")
    ap.add_argument("--sparc-file", required=True, help="sparc_mass_models.txt master file")
    ap.add_argument("--outdir", default="audit_output")
    args = ap.parse_args()

    galaxies = parse_sparc_master(args.sparc_file)
    print(f"Successfully parsed {len(galaxies)} galaxy profiles from {args.sparc_file}")

    results = [audit_galaxy(g) for g in galaxies]

    os.makedirs(args.outdir, exist_ok=True)
    summary_path = os.path.join(args.outdir, "audit_summary.csv")
    with open(summary_path, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["galaxy", "verdict", "n_points", "r_max_kpc",
                    "max_deficit_sn_outer", "a_anom_outer_max_m_s2",
                    "B_outer_max_uG", "B_global_max_uG", "reason"])
        for res in results:
            w.writerow([
                res["name"], res["verdict"], res.get("n_points", ""),
                res["r_max_kpc"], res.get("max_deficit_sn", ""),
                res.get("a_anom_outer_max", ""), res.get("B_outer_max_uG", ""),
                res.get("B_global_max_uG", ""), res.get("reason", "")
            ])

    print_honest_summary(results)
    print(f"\nWrote master summary to {summary_path}")

if __name__ == "__main__":
    main()

