#!/usr/bin/env python3
"""
torrent_confinement_test.py -- Does external confinement rescue the Keplerian fall?
================================================================================
Baseline: the honest mass engine from sim4_honest_engine.py (100% dropping).
Added: three EXTERNAL confinement terms, each with a named physical source,
declared magnitudes, and real-unit scaling. One parameter set for all seeds.

Falsification conditions (same as Sim 4, declared BEFORE the run):
  F1 both flat and rising regimes emerge (flat>15%, rising>10%)
  F2 scale separation (flat bigger/faster than rising)
  F3 dropping rare (<15%)
  F4 velocity range >= 2.5x

EXPECTED (stated up front from prior force-balance math):
  C1 magnetic: ~1e-4 of required -> FAILS on magnitude
  C2 ram: declining profile, magnitude = inflow speed -> fails unless inflow ~ 200 km/s
  C3 entrainment: can flatten ONLY by assuming ambient rotation is already flat
     (question relocated, not answered) -- reported as [RELOCATES QUESTION]

Whatever prints, that is the verdict. No post-hoc knob turning.
"""

import numpy as np

# ---- mass engine constants (identical to sim4_honest_engine.py) ----
K_DRAG, R_DEP, R_FILL = 0.004, 5.0, 3.0
A_PRESS, C_SWEEP, M0   = 5000.0, 2.0, 1.5
V_BASE, V_RICH         = 30.0, 35.0
N_SEEDS                = 175

# ---- confinement constants (REAL UNITS where declared) ----
MU0      = 4*np.pi*1e-7        # H/m
B0_MUG   = 5.0                 # measured Faraday-RM ceiling of coherent outer fields [microgauss]
B0_T     = B0_MUG * 1e-10      # tesla
RHO_ISM  = 1e-20               # kg/m^3 midplane gas density [flagged assumption]
R_REF    = 3.0                 # kpc, reference radius for B and inflow speed
U0_KMS   = 30.0                # km/s substrate inflow speed at R_REF [open parameter]

KMS2 = 1e6                     # (km/s)^2 = 1e6 m^2/s^2

def shell_reach(v0, t, k=K_DRAG):
    arg = 1.0 + 2.0*k*v0*v0*t
    return (np.sqrt(arg)-1.0)/(k*v0) if arg > 1.0 else 0.0

def mass_profile(r, shells, rich):
    L = R_DEP
    M = (0.1*len(shells)*M0)*(1.0-np.exp(-r/1.5))
    for v0, rj in shells:
        a  = K_DRAG*v0
        rr = np.minimum(r, rj)
        shed  = M0*((1-np.exp(-rr/L)) + a*L*(1-np.exp(-rr/L)*(1+rr/L)))
        sweep = C_SWEEP*rich*(rr + R_FILL*(np.exp(-rr/R_FILL)-1.0))
        M = M + shed + sweep
    return M

def classify(r, v):
    i0 = int(0.6*(len(r)-1))
    slope = (v[-1]-v[i0])/max(v[i0],1e-9)
    return "rising" if slope > 0.05 else ("dropping" if slope < -0.05 else "flat")

def census_curves(curves):
    cl = np.array([c[0] for c in curves])
    rm = np.array([c[1] for c in curves]); vm = np.array([c[2] for c in curves])
    n_disk = len(cl)
    fm, im, dm = cl=="flat", cl=="rising", cl=="dropping"
    out = []
    for nm, m in (("flat",fm),("rising",im),("dropping",dm)):
        if m.sum():
            out.append(f"{nm:8s}: {m.sum():3d} ({100*m.sum()/n_disk:4.1f}%) | "
                       f"R~{rm[m].mean():5.1f} | V~{vm[m].mean():6.1f}")
        else:
            out.append(f"{nm:8s}:   0 ( 0.0%)")
    pf, pr, pd = 100*fm.sum()/n_disk, 100*im.sum()/n_disk, 100*dm.sum()/n_disk
    f1 = pf > 15 and pr > 10
    f2 = (fm.sum() and im.sum() and rm[fm].mean() > rm[im].mean() and vm[fm].mean() > vm[im].mean())
    f3 = pd < 15
    f4 = vm.max()/max(vm.min(),1e-9) >= 2.5 if vm.size else False
    return out, (f1,f2,f3,f4), (pf,pr,pd), vm

def run():
    rng = np.random.default_rng(2026)
    seeds = []
    for _ in range(N_SEEDS):
        rich = rng.lognormal(0.0, 0.7)
        age  = rng.uniform(0.2, 6.0)
        n    = max(1, int(2+5*rich))
        v0s  = (V_BASE+V_RICH*rich)*rng.lognormal(0.0,0.15,n)
        tj   = age*(np.arange(n)+1)/(n+1)
        shells = [(v0s[j], shell_reach(v0s[j], age-tj[j])) for j in range(n)]
        rmax = max(rj for _,rj in shells)
        if rmax >= 2.0:
            seeds.append((rich, shells, rmax))

    # --- magnitude check done ONCE, in real units, before any curves ---
    v_c1_ref2 = B0_T**2/(MU0*RHO_ISM)            # m^2/s^2 at r = R_REF
    print("=" * 70)
    print("TORRENT CONFINEMENT TEST -- magnitudes first, curves second")
    print("=" * 70)
    print(f"C1 magnetic (B={B0_MUG} uG, rho={RHO_ISM:.0e} kg/m^3):")
    print(f"   v_conf at r={R_REF} kpc = {np.sqrt(v_c1_ref2)/1e3:.2f} km/s  (needed: ~150-300)")
    print(f"C2 ram (u={U0_KMS} km/s at r={R_REF}):")
    print(f"   v_conf = {np.sqrt(2)*U0_KMS:.1f} km/s, profile DECLINING as 1/r")
    print("-" * 70)

    for label, kind in (("C1 MAGNETIC confinement (B~1/r)", "c1"),
                        ("C2 RAM confinement (u~1/r inflow)", "c2"),
                        ("C3 ENTRAINMENT (ambient rotation)", "c3")):
        curves = []
        for rich, shells, rmax in seeds:
            r = np.linspace(0.5, 1.05*rmax, 80)
            v2_mass = A_PRESS*mass_profile(r, shells, rich)/r      # (mass-units km/s)^2
            if kind == "c1":
                # v_conf^2 = B(r)^2/(mu0 rho); B ~ B0*R_REF/r -> v_conf^2 ~ 1/r^2
                v2_conf = v_c1_ref2/KMS2 * (R_REF/r)**2
                v = np.sqrt(np.maximum(v2_mass + v2_conf, 0.0))
            elif kind == "c2":
                # v_conf^2 = 2 u(r)^2 ; u ~ U0*R_REF/r -> declining
                v2_conf = 2.0*(U0_KMS*R_REF/r)**2
                v = np.sqrt(np.maximum(v2_mass + v2_conf, 0.0))
            else:
                # C3: drag toward corotation with ambient vortex whose
                # rotation is assumed FLAT (the assumption is the whole point)
                v_amb = 150.0*np.sqrt(rich)      # [RELOCATES QUESTION]
                v = 0.5*np.sqrt(np.maximum(v2_mass,0.0)) + 0.5*v_amb
            curves.append((classify(r, v), rmax, v.max()))
        lines, (f1,f2,f3,f4), (pf,pr,pd), vm = census_curves(curves)
        print(f"[{label}]")
        for ln in lines: print("   " + ln)
        print(f"   F1 both regimes {'PASS' if f1 else 'FAIL'} (flat {pf:.0f}%/rising {pr:.0f}%) | "
              f"F2 separation {'PASS' if f2 else 'FAIL'} | "
              f"F3 drop rare {'PASS' if f3 else 'FAIL'} (drop {pd:.0f}%) | "
              f"F4 range {'PASS' if f4 else 'FAIL'} ({vm.max()/max(vm.min(),1e-9):.1f}x)")
        if kind == "c3":
            print("   [FLAG] C3 flattens ONLY by assuming ambient rotation is flat.")
            print("          The flat-curve question is relocated to the substrate,")
            print("          not answered. Next step would be: WHY is the substrate flat?")
        print("-" * 70)

    print("VERDICT RULES (locked before run): any candidate failing magnitude")
    print("or F1-F3 is logged [Contradicted] in the ledger. No re-tuning after.")
    print("=" * 70)

if __name__ == "__main__":
    run()

