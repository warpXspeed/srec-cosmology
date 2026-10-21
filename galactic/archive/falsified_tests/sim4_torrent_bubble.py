#!/usr/bin/env python3
"""
sim4_honest_engine.py -- SRC Sim 4 REDUX: The Uncheated Engine
================================================================
Rotation curves are COMPUTED from condensed mass, not written by hand.

M(r) = bulge + shed(deposition from pulse shells) + sweep(snowplow of
       replenished ambient substrate)
v(r) = sqrt( A_PRESS * M(r) / r )     (substrate pressure balance)

GLOBAL PARAMETERS (one set, physical names, NO per-galaxy tuning):
  K_DRAG  = 0.004   substrate ram-drag [1/(km/s kpc)]   -- shell deceleration
  R_DEP   = 5.0     pulse-shell mass-shedding length [kpc]
  R_FILL  = 3.0     ambient replenishment fill radius [kpc] (inner medium
                    is depleted by the core; refilled outward by the torrent)
  A_PRESS = 5000.0  substrate pressure coupling [open calibration parameter]
  C_SWEEP = 2.0     sweep-up efficiency [open calibration parameter]
  M0      = 1.5     pulse-shell mass [mass units]
  V_BASE  = 30.0, V_RICH = 35.0    shell launch speed law (km/s)

SEED VARIATION (environment, not tuning):
  torrent richness ~ lognormal(sigma=0.7); ignition age ~ U(0.2, 6) Gyr
  (asynchronous births -- no starting gun); per-shell jitter.

FALSIFICATION CONDITIONS (declared BEFORE the run):
  F1: both regimes must appear (flat > 15% AND rising > 10%)
  F2: scale separation -- flat mean R_max and V_max must EXCEED rising mean
  F3: dropping (Keplerian) must be rare (< 15%)
  F4: population V_max must span a factor >= 2.5

ANCHOR TARGETS (78 clean galaxies): flat 56.6% (R=20.8 kpc, V=156 km/s),
rising 42.1% (R=5.8 kpc, V=72 km/s), dropping 1.3%.

Whatever the numbers come out to be, that is the verdict.
"""

import numpy as np

K_DRAG, R_DEP, R_FILL = 0.004, 5.0, 3.0
A_PRESS, C_SWEEP, M0   = 5000.0, 2.0, 1.5
V_BASE, V_RICH         = 30.0, 35.0
N_SEEDS                = 175

def shell_reach(v0, t, k=K_DRAG):
    """Closed form of dr/dt = v0/(1 + k v0 r): r(t) = (sqrt(1+2 k v0^2 t)-1)/(k v0)."""
    arg = 1.0 + 2.0 * k * v0 * v0 * t
    return (np.sqrt(arg) - 1.0) / (k * v0) if arg > 1.0 else 0.0

def mass_profile(r, shells, rich):
    """Cumulative condensed mass. Each shell (v0, r_j) deposits:
       shed:  m0 * [(1-e^{-r/L}) + aL(1 - e^{-r/L}(1+r/L))]   (concentrated)
       sweep: C*rich * [r + R_FILL(e^{-r/R_FILL}-1)]         (flat when filled)
       Both evaluated at min(r, r_j): dissolved shells keep their deposit."""
    L = R_DEP
    M = (0.1 * len(shells) * M0) * (1.0 - np.exp(-r / 1.5))   # central bulge
    for v0, rj in shells:
        a  = K_DRAG * v0
        rr = np.minimum(r, rj)
        shed = M0 * ((1 - np.exp(-rr / L)) + a * L * (1 - np.exp(-rr / L) * (1 + rr / L)))
        sweep = C_SWEEP * rich * (rr + R_FILL * (np.exp(-rr / R_FILL) - 1.0))
        M = M + shed + sweep
    return M

def classify(r, v):
    """Same convention as analyze_velocity_profile.py: outer 40% slope."""
    i0 = int(0.6 * (len(r) - 1))
    slope = (v[-1] - v[i0]) / max(v[i0], 1e-9)
    if slope > 0.05:  return "rising"
    if slope < -0.05: return "dropping"
    return "flat"

def run():
    rng = np.random.default_rng(2026)
    classes, rmaxs, vmaxs = [], [], []

    for _ in range(N_SEEDS):
        rich = rng.lognormal(0.0, 0.7)          # torrent richness at birthplace
        age  = rng.uniform(0.2, 6.0)            # Gyr since ignition (no starting gun)
        n    = max(1, int(2 + 5 * rich))        # pulses delivered so far
        v0s  = (V_BASE + V_RICH * rich) * rng.lognormal(0.0, 0.15, n)
        tj   = age * (np.arange(n) + 1) / (n + 1)          # launch times
        shells = [(v0s[j], shell_reach(v0s[j], age - tj[j])) for j in range(n)]

        rmax = max(rj for _, rj in shells)
        if rmax < 2.0:
            classes.append("dark"); continue     # never condensed a disk

        r = np.linspace(0.5, 1.05 * rmax, 80)
        v = np.sqrt(A_PRESS * mass_profile(r, shells, rich) / r)
        classes.append(classify(r, v))
        rmaxs.append(rmax); vmaxs.append(v.max())

    rmaxs = np.array(rmaxs); vmaxs = np.array(vmaxs)
    cl = np.array(classes)
    flat_m = cl == "flat"; rise_m = cl == "rising"; drop_m = cl == "dropping"
    n_disk = flat_m.sum() + rise_m.sum() + drop_m.sum()

    print("=" * 70)
    print("SIM 4 REDUX: UNCHEATED ENGINE -- POPULATION VERDICT")
    print("=" * 70)
    print(f"Seeds                        : {N_SEEDS}")
    print(f"  never ignited (dark clouds) : {(cl=='dark').sum()}")
    print(f"  disks formed                : {n_disk}")
    print("-" * 70)
    if n_disk:
        for nm, m in (("FLAT", flat_m), ("RISING", rise_m), ("DROPPING", drop_m)):
            if m.sum():
                print(f"  {nm:8s}: {m.sum():3d} ({100*m.sum()/n_disk:4.1f}%)"
                      f" | R_max ~ {rmaxs[m].mean():5.1f} kpc | V_max ~ {vmaxs[m].mean():6.1f} km/s")
            else:
                print(f"  {nm:8s}:   0 ( 0.0%)")
    print("-" * 70)
    print("FALSIFICATION CHECKS (vs 78 clean anchors):")
    pf = 100*flat_m.sum()/max(n_disk,1); pr = 100*rise_m.sum()/max(n_disk,1)
    pd = 100*drop_m.sum()/max(n_disk,1)
    f1 = (pf > 15 and pr > 10)
    f2 = (flat_m.sum() and rise_m.sum() and
          rmaxs[flat_m].mean() > rmaxs[rise_m].mean() and
          vmaxs[flat_m].mean() > vmaxs[rise_m].mean())
    f3 = pd < 15
    f4 = vmaxs.size >= 2 and vmaxs.max() / max(vmaxs.min(), 1e-9) >= 2.5
    print(f"  F1 both regimes emerge          : {'PASS' if f1 else 'FAIL'}"
          f"  (flat {pf:.0f}% / rising {pr:.0f}%)")
    print(f"  F2 scale separation (flat>rising): {'PASS' if f2 else 'FAIL'}")
    print(f"  F3 Keplerian drop rare           : {'PASS' if f3 else 'FAIL'}"
          f"  (drop {pd:.0f}%)")
    print(f"  F4 velocity dynamic range         : {'PASS' if f4 else 'FAIL'}"
          f"  ({vmaxs.max()/max(vmaxs.min(),1e-9):.1f}x)" if vmaxs.size else "")
    print("-" * 70)
    print("ANCHOR TARGETS: flat 56.6% (R=20.8, V=156) | rising 42.1% (R=5.8, V=72)")
    print("Open parameters flagged: A_PRESS, C_SWEEP (calibration pending).")
    print("Process simulation -- units declared, outcomes NOT pre-written.")
    print("=" * 70)

if __name__ == "__main__":
    run()

