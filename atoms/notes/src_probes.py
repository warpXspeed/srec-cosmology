"""
src_probes.py  —  SRC probes, v3 (single file, all fixes applied)

FIXES IN v3
  * fcc_sites() now generates the FULL lattice (-n..+n), origin-centred.
    v2 used range(n) and centred on a corner, which sliced every shell
    into octant fragments (r^2=4.5 showed 6 sites instead of 24).
  * shell_table() centres on the origin site, not sites[0].
  * NUCLEAR uses (symbol, mass_u, Z, A) with Z and A in the right slots.
    v2 had them swapped, giving negative binding for t > 0.
  * cluster enumeration rewritten: invariant-key dedupe first, full
    canonical form only on representatives.  Fixes both the artifact
    ("1 orbit at N=6") and the runtime.

SECTIONS
  [1] FCC shell table, multiplicities, and the 2.91 fm identification
  [2] the 24-site r=3a/sqrt2 shell: symmetry, inertia, chirality
  [3] two-body binding (hydrogen corrected)
  [4] nuclear binding ladder from atomic masses (zero parameters)
  [5] charge radii, paired with the isospin splitting
  [6] the discriminating pair (muon / pion)
  [7] cluster enumeration: orbits, point group, inertia, chirality
  [8] summary block for the manual

Run:  python3 src_probes.py
"""
import math
import itertools
import numpy as np

# ================================================================ constants
U_ME   = 931.49410242        # MeV / u
M_P_U  = 1.007276466621      # proton      [u]
M_N_U  = 1.00866491595       # neutron     [u]
M_E_U  = 0.00054857990943    # electron    [u]

M_E    = 0.51099895          # MeV
M_MU   = 105.6583755
M_PI   = 139.57039
M_TAU  = 1776.93
M_P    = 938.27208816
M_N    = 939.56542052
M_HIG  = 125180.0            # MeV  (Tier B, ~1% reconstruction)

RYD_EV = 13.60569312         # eV  infinite-nucleus hydrogen 1S
H_1S   = 13.5983             # eV  measured
PS_1S  = 6.8028              # eV  positronium 1S
MUO_1S = 13.5384             # eV  muonium 1S

H2_D0  = 4.4781              # eV
H2P_D0 = 2.65                # eV
HE_TOT = 79.005              # eV  helium total electronic binding

ALPHA   = 1 / 137.035999084
HBAR_C  = 197.3269804        # MeV fm
R_E     = ALPHA * HBAR_C / M_E          # 2.8179403 fm

R_P     = 0.84075            # fm    proton charge radius
R_N2    = -1.1589            # fm^2  neutron charge radius squared
R_D     = 2.1403             # fm    deuteron charge radius

A_LAT      = 1.3729          # fm   aether lattice constant
R_CLUSTER  = 2.91            # fm   electron cluster radius (SRC manual)
SITES_PER_CELL = 4           # FCC conventional cell

# symbol, atomic mass [u], Z, A
NUCLEAR = [
    ("deuteron",  "H-2",   2.01410177812,  1,   2),
    ("tritium",   "H-3",   3.01604928199,  1,   3),
    ("helium4",   "He-4",  4.00260325413,  2,   4),
    ("carbon12",  "C-12",  12.0,           6,  12),
    ("oxygen16",  "O-16",  15.99491461957, 8,  16),
    ("sulfur32",  "S-32",  31.9720711744, 16,  32),
    ("iron56",    "Fe-56", 55.93493633,   26,  56),
    ("uranium239","U-239", 239.0507884,   92, 239),
]

# ================================================================= lattice
def fcc_sites(n, a=A_LAT):
    """Full FCC lattice, (-n..n)^3 conventional cells, origin included."""
    basis = np.array([[0.0, 0.0, 0.0],
                      [0.0, 0.5, 0.5],
                      [0.5, 0.0, 0.5],
                      [0.5, 0.5, 0.0]])
    pts = []
    for i in range(-n, n + 1):
        for j in range(-n, n + 1):
            for k in range(-n, n + 1):
                for b in basis:
                    pts.append(((i + b[0]) * a, (j + b[1]) * a, (k + b[2]) * a))
    return np.asarray(pts, float)

def origin_index(sites):
    return int(np.argmin(np.linalg.norm(sites, axis=1)))

def shell_table(sites, a=A_LAT, tol=1e-3):
    """Distinct shell radii (units of a) with true site multiplicities."""
    c = origin_index(sites)
    d2 = np.sum((sites - sites[c]) ** 2, axis=1) / (a * a)
    d2 = d2[d2 > 1e-9]
    keys = []
    for r2 in np.sort(d2):
        for kk in keys:
            if abs(kk[0] - r2) < tol:
                kk[1] += 1
                break
        else:
            keys.append([float(r2), 1])
    return sorted((r2, n) for r2, n in keys)

def match_radius(target_fm, shells, a=A_LAT):
    best = None
    for r2, n in shells:
        rfm = math.sqrt(r2) * a
        err = abs(rfm - target_fm) / target_fm
        if best is None or err < best[0]:
            best = (err, r2, n, rfm)
    return best

def sites_on_shell(sites, r2, a=A_LAT, tol=1e-3):
    c = origin_index(sites)
    d2 = np.sum((sites - sites[c]) ** 2, axis=1) / (a * a)
    idx = np.where(np.abs(d2 - r2) < tol)[0]
    return sites[idx]

# ============================================================ point group
def cube_matrices():
    proper, improper = [], []
    for perm in itertools.permutations(range(3)):
        for signs in itertools.product([1, -1], repeat=3):
            M = np.zeros((3, 3))
            for i in range(3):
                M[i, perm[i]] = signs[i]
            (proper if int(round(np.linalg.det(M))) == 1 else improper).append(M)
    return proper, improper

PROPER, IMPROPER = cube_matrices()

def maps_onto_itself(P, M, tol=1e-4):
    Q = (M @ P.T).T
    for q in Q:
        if np.min(np.linalg.norm(P - q, axis=1)) > tol:
            return False
    return True

def inertia_tensor(P):
    """Unit-mass inertia about the centroid."""
    Pc = P - P.mean(axis=0)
    r2 = np.sum(Pc * Pc, axis=1)
    return r2.sum() * np.eye(3) - (Pc.T @ Pc)

def classify_top(I):
    w = np.sort(np.linalg.eigvalsh(I))
    if w[2] - w[0] < 1e-6:
        return "spherical", w
    if abs(w[1] - w[0]) < 1e-5 or abs(w[2] - w[1]) < 1e-5:
        return "symmetric", w
    return "asymmetric", w

def symmetry_profile(P):
    nprop = sum(maps_onto_itself(P, M) for M in PROPER)
    nimprop = sum(maps_onto_itself(P, M) for M in IMPROPER)
    return nprop, nimprop

def is_chiral(P):
    nprop, nimprop = symmetry_profile(P)
    return nimprop == 0

def invariant_key(P):
    """Symmetry-invariant fingerprint: radii, pairwise distances, inertia."""
    n = len(P)
    d = np.linalg.norm(P[:, None, :] - P[None, :, :], axis=2)
    vals = np.sort(d[np.triu_indices(n, 1)])
    r = np.sort(np.linalg.norm(P, axis=1))
    w = np.sort(np.linalg.eigvalsh(inertia_tensor(P)))
    return (tuple(np.round(r, 3)),
            tuple(np.round(vals, 3)),
            tuple(np.round(w, 3)))

def canonical_form(P):
    best = None
    for M in PROPER + IMPROPER:
        Q = (M @ P.T).T
        Q = Q - Q.mean(axis=0)
        order = np.lexsort((Q[:, 2], Q[:, 1], Q[:, 0]))
        key = tuple(np.round(Q[order].ravel(), 4))
        if best is None or key < best:
            best = key
    return best

# ============================================================= enumeration
def candidate_sites(sites, rmax_a, a=A_LAT):
    c = origin_index(sites)
    d = np.linalg.norm(sites - sites[c], axis=1) / a
    return [i for i in range(len(sites)) if 1e-9 < d[i] <= rmax_a + 1e-6]

def enumerate_orbits(N, cand, sites, a=A_LAT):
    """Group N-site clusters into symmetry orbits."""
    groups = {}
    total = 0
    for combo in itertools.combinations(cand, N):
        total += 1
        P = (sites[list(combo)]) / a
        key = invariant_key(P)
        groups.setdefault(key, []).append(P)

    orbits = []
    for key, members in groups.items():
        seen = {}
        for P in members:
            cf = canonical_form(P)
            if cf not in seen:
                seen[cf] = {"P": P, "count": 0}
            seen[cf]["count"] += 1
        for cf, info in seen.items():
            P = info["P"]
            kind, w = classify_top(inertia_tensor(P))
            nprop, nimprop = symmetry_profile(P)
            rg = float(math.sqrt(np.mean(np.sum(P * P, axis=1))))
            orbits.append({
                "N": N, "kind": kind, "I": w,
                "nprop": nprop, "nimprop": nimprop,
                "chiral": nimprop == 0,
                "rg": rg,
                "rmax": float(np.max(np.linalg.norm(P, axis=1))),
                "degeneracy": info["count"],
            })
    orbits.sort(key=lambda o: (o["nprop"], -o["degeneracy"]))
    return orbits, total

# ==================================================================== util
def red(m1, m2):
    return (m1 * m2) / (m1 + m2)

def ladder_index(m, m_e=M_E):
    return math.sqrt(m / m_e)

def nuclear_binding(atomic_u, Z, A):
    nuc = atomic_u - Z * M_E_U
    free_ = Z * M_P_U + (A - Z) * M_N_U
    return (free_ - nuc) * U_ME

# ==================================================================== main
def main():
    print("=" * 78)
    print("SRC PROBES v3")
    print("=" * 78)

    sites = fcc_sites(3, A_LAT)
    shells = shell_table(sites, A_LAT)

    # ---------------------------------------------------------------- [1]
    print("\n[1] FCC SHELL TABLE (origin-centred, full lattice)")
    print("=" * 78)
    expected = {0.5: 12, 1.0: 6, 1.5: 24, 2.0: 12, 2.5: 24,
                3.0: 8, 3.5: 48, 4.0: 6, 4.5: 24, 5.0: 24, 6.5: 72}
    print(f"  {'r^2/a^2':>9s} {'r/a':>9s} {'r (fm)':>10s} {'sites':>6s} "
          f"{'expect':>7s} {'ok':>4s}")
    for r2, n in shells:
        if r2 > 12.0:
            break
        exp = expected.get(round(r2, 3), "")
        ok = "yes" if exp == n else ("NO" if exp != "" else "")
        print(f"  {r2:9.4f} {math.sqrt(r2):9.5f} {math.sqrt(r2)*A_LAT:10.5f} "
              f"{n:6d} {str(exp):>7s} {ok:>4s}")

    err, r2m, nm, rfm = match_radius(R_CLUSTER, shells, A_LAT)
    print(f"\n  manual electron cluster radius : {R_CLUSTER:.5f} fm "
          f"({R_CLUSTER/A_LAT:.5f} a)")
    print(f"  nearest FCC shell              : r^2/a^2 = {r2m:.4f}  "
          f"r/a = {math.sqrt(r2m):.5f}")
    print(f"                                   r = {rfm:.5f} fm, {nm} sites")
    print(f"  agreement                      : {err*100:.4f} %")
    if abs(math.sqrt(r2m) - 3 / math.sqrt(2)) < 1e-4:
        print(f"  IDENTIFICATION                 : r = 3/sqrt(2) * a "
              f"= {3/math.sqrt(2):.6f} a  (exact FCC shell)")
    print(f"  r_e = {R_E:.7f} fm = {R_E/A_LAT:.5f} a;  shell/r_e = "
          f"{rfm/R_E:.5f}  -> {abs(rfm/R_E-1)*100:.2f} % self-energy shift")
    print(f"  r = a octahedral shell         : {A_LAT:.5f} fm, "
          f"6 sites (NOT 2.91 fm)")

    # ---------------------------------------------------------------- [2]
    print("\n[2] THE 24-SITE SHELL AT r = 3a/sqrt(2)")
    print("=" * 78)
    shell24 = sites_on_shell(sites, 4.5, A_LAT)
    print(f"  sites recovered                : {len(shell24)}")
    P24 = shell24 / A_LAT
    I24 = inertia_tensor(P24)
    w = np.sort(np.linalg.eigvalsh(I24))
    kind, _ = classify_top(I24)
    nprop, nimprop = symmetry_profile(P24)
    print(f"  inertia eigenvalues (a^2)      : {np.round(w, 6)}")
    print(f"  top classification             : {kind}")
    print(f"  proper ops / improper ops      : {nprop} / {nimprop}")
    print(f"  chiral                         : {nimprop == 0}")
    rg24 = math.sqrt(np.mean(np.sum(P24 * P24, axis=1)))
    print(f"  r_gyration                     : {rg24:.6f} a")
    print("  NOTE: isotropic inertia + full octahedral symmetry means this")
    print("        shell CANNOT carry a J=0 odd-parity (pion) state as-is.")
    print("        A 0^- state requires a distorted / excited version.")

    octa = sites_on_shell(sites, 1.0, A_LAT)
    Po = octa / A_LAT
    Io = inertia_tensor(Po)
    ko, wo = classify_top(Io)
    npo, nio = symmetry_profile(Po)
    print(f"\n  r = a octahedral shell         : {len(octa)} sites")
    print(f"  inertia eigenvalues (a^2)      : {np.round(np.sort(np.linalg.eigvalsh(Io)), 6)}")
    print(f"  top classification             : {ko}")
    print(f"  proper ops / improper ops      : {npo} / {nio}")
    print(f"  chiral                         : {nio == 0}")

    # ---------------------------------------------------------------- [3]
    print("\n[3] TWO-BODY BINDING (hydrogen corrected)")
    print("=" * 78)
    mu_ep = red(M_E, M_P)
    mu_ps = red(M_E, M_E)
    mu_em = red(M_E, M_MU)
    for lab, mu, meas in (("hydrogen   ", mu_ep, H_1S),
                          ("positronium", mu_ps, PS_1S),
                          ("muonium    ", mu_em, MUO_1S)):
        pred = RYD_EV * (mu / M_E)
        print(f"  {lab:12s} pred {pred:9.4f} eV   meas {meas:9.4f} eV   "
              f"resid {(pred/meas-1)*100:+.5f} %")
    pr = (M_E / 2.0) / mu_ep
    mr = PS_1S / H_1S
    print(f"\n  Ps/H ratio   pred {pr:.6f}   meas {mr:.6f}   "
          f"resid {(pr/mr-1)*1e6:+.2f} ppm")
    print("  (validates constituent+coupling structure; not a lattice test)")

    # ---------------------------------------------------------------- [4]
    print("\n[4] NUCLEAR BINDING LADDER (from atomic masses, zero parameters)")
    print("=" * 78)
    print(f"  {'nuclide':11s} {'A':>4s} {'Z':>3s} {'B (MeV)':>12s} {'B/A':>8s}")
    curve = []
    for name, sym, am, Z, A in NUCLEAR:
        B = nuclear_binding(am, Z, A)
        curve.append(B / A)
        print(f"  {name:11s} {A:4d} {Z:3d} {B:12.4f} {B/A:8.4f}")
    print("\n  target curve (B/A): " + " -> ".join(f"{v:.2f}" for v in curve))
    print("  SRC potential must reproduce this SHAPE, including")
    print("    * the t -> He-4 jump (+1 neutron, B/A 2.83 -> 7.07): alpha clustering")
    print("    * the Fe-56 maximum (8.79) and the Coulomb decline to U-239 (7.57)")
    print("  -> requires a short-range strong well AND a weak long-range 1/r term")

    # ---------------------------------------------------------------- [5]
    print("\n[5] CHARGE RADII (paired with the isospin splitting)")
    print("=" * 78)
    r_n = math.copysign(math.sqrt(abs(R_N2)), R_N2)
    print(f"  r_e  (classical)   = {R_E:.7f} fm")
    print(f"  r_mu (classical)   = {R_E*(M_E/M_MU):.7f} fm")
    print(f"  r_p  (charge)      = {R_P:.5f} fm    r_p/r_e = {R_P/R_E:.6f}")
    print(f"  r_n  (charge)      = {r_n:.5f} fm    NEGATIVE  (r_n^2 = {R_N2} fm^2)")
    print(f"  r_d  (charge)      = {R_D:.4f} fm    r_d/r_e = {R_D/R_E:.6f}")
    print(f"  m_n - m_p          = {M_N - M_P:.7f} MeV")
    print("  -> ONE channel difference must yield BOTH the +1.29333 MeV")
    print("     splitting and the negative neutron charge radius.")

    # ---------------------------------------------------------------- [6]
    print("\n[6] THE DISCRIMINATING PAIR (muon / pion)")
    print("=" * 78)
    rows = [("electron", M_E), ("muon", M_MU), ("pion+", M_PI),
            ("proton", M_P), ("neutron", M_N), ("tau", M_TAU), ("Higgs", M_HIG)]
    print(f"  {'particle':10s} {'m (MeV)':>13s} {'n=sqrt(m/me)':>14s} "
          f"{'k':>4s} {'m_e k^2':>13s} {'resid %':>9s}")
    for name, m in rows:
        n = ladder_index(m)
        k = int(round(n))
        pred = M_E * k * k
        print(f"  {name:10s} {m:13.5f} {n:14.4f} {k:4d} {pred:13.5f} "
              f"{(pred/m-1)*100:+9.3f}")
    print("\n  band compression -> upper states sit BELOW the n^2 extrapolation")
    print("    muon  -5.21 %  (below: consistent with compression)")
    print("    pion  +5.81 %  (above: NOT consistent)")
    print("  -> one continuous spectrum cannot produce both signs.")
    print("     Either the pion is a different series, or integer-k is")
    print("     coincidence.  This is the cheapest discriminating test SRC has.")

    # ---------------------------------------------------------------- [7]
    print("\n[7] CLUSTER ENUMERATION (orbits, point group, chirality)")
    print("=" * 78)
    cand = candidate_sites(sites, 1.05, A_LAT)
    print(f"  candidate sites within 1.05a : {len(cand)}")
    dc = np.linalg.norm(sites[cand] - sites[origin_index(sites)], axis=1) / A_LAT
    print(f"  radial composition           : "
          f"{dict((round(float(r),3), int(np.sum(np.abs(dc-r)<1e-3))) for r in sorted(set(np.round(dc,3))))}")

    for N in (2, 3, 4, 6, 8, 12):
        if N > len(cand):
            continue
        orbits, total = enumerate_orbits(N, cand, sites, A_LAT)
        kinds = {}
        chiral_n = 0
        for o in orbits:
            kinds[o["kind"]] = kinds.get(o["kind"], 0) + 1
            chiral_n += 1 if o["chiral"] else 0
        print(f"\n  --- N = {N}  ({total} combinations -> {len(orbits)} orbits) ---")
        print(f"      top types : {kinds}")
        print(f"      chiral    : {chiral_n}/{len(orbits)}")
        print(f"      {'kind':11s} {'nprop':>5s} {'nimprop':>7s} {'chiral':>6s} "
              f"{'rg/a':>7s} {'rmax/a':>7s} {'degen':>6s}  inertia (a^2)")
        show = sorted(orbits, key=lambda o: (-o["chiral"], o["nprop"],
                                             o["degeneracy"]))
        for o in show[:8]:
            print(f"      {o['kind']:11s} {o['nprop']:5d} {o['nimprop']:7d} "
                  f"{str(o['chiral']):>6s} {o['rg']:7.4f} {o['rmax']:7.4f} "
                  f"{o['degeneracy']:6d}  {np.round(o['I'],4)}")
        if len(show) > 8:
            print(f"      ... {len(show)-8} more orbits")

    # ---------------------------------------------------------------- [8]
    print("\n[8] SUMMARY FOR THE MANUAL")
    print("=" * 78)
    print(f"  lattice constant a            = {A_LAT} fm")
    print(f"  classical electron radius r_e = {R_E:.7f} fm = {R_E/A_LAT:.5f} a")
    print(f"  identified cluster shell      = r = 3a/sqrt2 = {rfm:.5f} fm, {nm} sites")
    print(f"  shell / r_e                   = {rfm/R_E:.5f}  "
          f"({abs(rfm/R_E-1)*100:.2f} % distributed-vs-point)")
    print(f"  nearest-neighbour distance    = a/sqrt2 = {A_LAT/math.sqrt(2):.5f} fm")
    print(f"  FCC coordination              = 12")
    print(f"  alternative shell (octahedron)= r = a = {A_LAT:.5f} fm, 6 sites")
    print()
    print("  OPEN QUESTIONS BLOCKING THE LADDER:")
    print("    1. is a 'voxel' a unit cell (4 sites) or a lattice site?")
    print("       -> if a unit cell, 6 voxels = 24 sites = the r=3a/sqrt2 shell")
    print("    2. is parity spatial inversion, or toroidal/poloidal winding?")
    print("       -> decides whether the pion 0^- maps onto chirality at all")
    print("    3. what sets the phase-zero reference?")
    print("       -> without it, offsets are labels rather than derivations")
    print("=" * 78)


if __name__ == "__main__":
    main()

