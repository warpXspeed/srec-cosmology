# Name: magnetism_engine_v1_2.py
# Type: code
"""
SRC Magnetic Tensor Module v1.2
Scalar Relaxation Cosmology - Magnetism as its own field of interest

v1.2 changes relative to v1.1:
 1. EXCHANGE SIGN (Bethe-Slater analog): boundary-tier nodes with
    insufficient stored tension (tau < 1.3) cannot hold a parallel
    tensor lock against boundary crowding. They order into a
    checkerboard (antiferromagnetic). Cr and Mn fall below the
    threshold; Fe, Co, Ni above it.
 2. HEAVY DEEP-TIER ANTIPARALLEL: deep-tier nodes carrying more
    unclosed asymmetry (u >= 6) than the boundary tier can resonate
    with fall OUT OF PHASE with the frame (Gd, Dy). Light rare
    earths (Nd u=4, Sm u=5) stay parallel. This reproduces the
    light/heavy rare-earth split without a lookup table: heavy
    substitution RAISES retention but LOWERS moment.
 3. Cu TUPLE FIX: Cu's 3d boundary closes in the lattice. u = 0.
    Diamagnetic, as observed.
 4. HARD/SOFT THRESHOLD recalibrated to K > 1.2, between elemental
    Co (1.32, genuinely hard) and dilute Co-Ti (1.15, artifact).

Honest notes:
 - Sublattice site occupancy is NOT derivable from stoichiometry
   (same class of gap as the V vector in reaction_engine v0.5).
   Passed in as geometry, never looked up.
 - Hexaferrite (SrFe12O19) anisotropy is UNDER-predicted: its K
   lives in the hexagonal lattice frame, not modeled here.
 - Alnico retention is shape anisotropy of precipitates - a
   microstructure problem, out of scope until v1.3.
 - Direct exchange sign is a per-species pair simplification:
   frustration (alpha-Mn's complex structure) needs geometry.
"""

import numpy as np

# E = (tau, f, dP, s, u, Kf, tier)
#   u  = unclosed harmonic slots carried into the lattice (spin analog)
#   Kf = crystal-symmetry anisotropy factor (cubic ~0, uniaxial/deep ~1)
#   tau < 1.3 at boundary tier -> checkerboard order (AF) by itself
#   deep tier with u >= 6 -> falls out of phase with the frame
MAG_ELEMENTS = {
    "Fe": {"tau": 1.5, "freq": 8.2,  "dP":  0.5, "s": 3, "u": 4, "Kf": 0.15, "tier": "boundary"},
    "Co": {"tau": 1.5, "freq": 8.35, "dP":  0.2, "s": 3, "u": 3, "Kf": 0.80, "tier": "boundary"},
    "Ni": {"tau": 1.6, "freq": 8.5,  "dP": -0.2, "s": 2, "u": 2, "Kf": 0.10, "tier": "boundary"},
    "Mn": {"tau": 1.2, "freq": 8.1,  "dP": -0.3, "s": 4, "u": 5, "Kf": 0.05, "tier": "boundary"},
    "Cr": {"tau": 1.1, "freq": 8.05, "dP": -0.4, "s": 3, "u": 6, "Kf": 0.05, "tier": "boundary"},
    "Cu": {"tau": 1.6, "freq": 8.5,  "dP": -0.4, "s": 2, "u": 0, "Kf": 0.05, "tier": "boundary"},  # v1.2: closed
    "Zn": {"tau": 1.8, "freq": 8.8,  "dP":  0.8, "s": 2, "u": 0, "Kf": 0.00, "tier": "boundary"},
    "Gd": {"tau": 2.0, "freq": 12.0, "dP":  0.0, "s": 3, "u": 7, "Kf": 1.00, "tier": "deep"},   # heavy: antiparallel
    "Nd": {"tau": 2.2, "freq": 12.3, "dP":  0.3, "s": 3, "u": 4, "Kf": 1.00, "tier": "deep"},   # light: parallel
    "Sm": {"tau": 2.1, "freq": 12.4, "dP":  0.2, "s": 3, "u": 5, "Kf": 1.00, "tier": "deep"},   # light: parallel
    "Dy": {"tau": 2.3, "freq": 12.6, "dP":  0.4, "s": 3, "u": 6, "Kf": 1.00, "tier": "deep"},   # heavy: antiparallel
    "O":  {"tau": 3.0, "freq": 4.5,  "dP": -3.0, "s": 2, "u": 0, "Kf": 0.00, "tier": "sink"},
    "B":  {"tau": 1.2, "freq": 3.8,  "dP": -0.5, "s": 3, "u": 0, "Kf": 0.00, "tier": "anchor"},
    "Al": {"tau": 1.5, "freq": 5.6,  "dP":  0.3, "s": 3, "u": 0, "Kf": 0.00, "tier": "boundary"},
    "Sr": {"tau": 3.2, "freq": 10.5, "dP":  2.0, "s": 2, "u": 0, "Kf": 0.00, "tier": "anchor"},
    "Ti": {"tau": 1.3, "freq": 8.0,  "dP":  0.4, "s": 4, "u": 2, "Kf": 0.10, "tier": "boundary"},
    "Y":  {"tau": 2.0, "freq": 12.1, "dP":  0.1, "s": 3, "u": 0, "Kf": 0.00, "tier": "deep"},
}

ANCHOR_K     = 4.6     # anisotropy calibration (Nd2Fe14B anchor)
ANCHOR_J     = 1.0     # exchange calibration
SE_FACTOR    = 0.75    # superexchange weakens |J| through a sink bridge
PARALLEL_TAU = 1.3     # tension threshold for parallel lock (boundary tier)
HEAVY_U      = 6       # deep-tier asymmetry above this falls out of phase
DELTA_CRIT   = 2.0     # polarization-separation scale for exchange

# ---------------------------------------------------------------
# FIELD FUNCTIONS
# ---------------------------------------------------------------
def octave_coupling(f1, f2):
    """Octave-reduced harmonic coupling, 0..1 (same kernel as v0.5)."""
    ratio = max(f1, f2) / min(f1, f2)
    while ratio >= 2.0:
        ratio /= 2.0
    simple = [1.0, 1.25, 1.333, 1.5, 1.666, 1.75, 2.0]
    d = min(abs(ratio - r) for r in simple)
    return float(np.exp(-(d ** 2) / 0.05))

def local_moment(sym):
    """Unresolved tensor asymmetry of a lattice node. Scale units."""
    e = MAG_ELEMENTS[sym]
    return e["u"] * e["tau"] / e["freq"]

def has_sink(comp):
    return any(MAG_ELEMENTS[s]["tier"] == "sink" for s in comp)

def direct_exchange_sign(sym):
    """Bethe-Slater analog. Boundary nodes with too little stored
    tension to hold a parallel lock order into a checkerboard.
    Deep-tier nodes always lock parallel to the frame (their sign
    is handled separately in net_moment)."""
    e = MAG_ELEMENTS[sym]
    if e["tier"] != "boundary":
        return +1
    return +1 if e["tau"] >= PARALLEL_TAU else -1

def exchange_coupling(sym_a, sym_b):
    """|J_ij| between lattice neighbors. Sign structure is handled
    in net_moment (checkerboard / out-of-phase), not here."""
    a, b = MAG_ELEMENTS[sym_a], MAG_ELEMENTS[sym_b]
    coup = octave_coupling(a["freq"], b["freq"])
    drive = abs(a["dP"] - b["dP"]) / DELTA_CRIT
    tier_bonus = 1.4 if ("deep" in (a["tier"], b["tier"])) else 1.0
    slot_overlap = min(a["u"], b["u"]) / max(a["u"], b["u"], 1)
    J = ANCHOR_J * coup * slot_overlap * tier_bonus * np.exp(-drive)
    if a["tier"] == "sink" or b["tier"] == "sink":
        J = -0.6 * abs(J)   # sink contact flips sign (superexchange)
    return float(J)

def anisotropy_K(comp):
    """Lattice resistance to relaxation of the tensor direction.
    Deep-tier asymmetry is buried below the boundary tier: thermal
    agitation cannot reach it. Boundary-tier asymmetry is thinned by
    crystal symmetry (Kf)."""
    K = 0.0
    for sym, n in comp.items():
        e = MAG_ELEMENTS[sym]
        if e["u"] <= 0:
            continue
        if e["tier"] == "deep":
            K += n * e["u"] * e["tau"] * 0.5              # buried asymmetry
        else:
            K += n * e["u"] * e["tau"] * 0.08 * e["Kf"]   # symmetry-thinned
    return ANCHOR_K * K / max(sum(comp.values()), 1)

def net_moment(comp, sublattice=None):
    """Net lattice moment.

    sublattice = {sym: (n_up, n_down)} for sink-bridged lattices.
    None + sink-bridged -> exact cancellation (antiferro default).

    Non-sink lattices:
      - all-checkerboard species (Cr, Mn elemental) -> exact cancel
      - heavy deep-tier species (u >= 6) count NEGATIVE
        (out of phase with the frame: Gd, Dy)
    """
    if has_sink(comp):
        if sublattice is None:
            return 0.0     # honest default: stoichiometry can't fix occupancy
        total = 0.0
        for sym, (up, down) in sublattice.items():
            total += local_moment(sym) * (up - down)
        return float(abs(total))

    mag = [(s, n) for s, n in comp.items() if MAG_ELEMENTS[s]["u"] > 0]
    if not mag:
        return 0.0
    # checkerboard frame: low-tension boundary species cancel themselves
    if all(direct_exchange_sign(s) < 0 for s, _ in mag):
        return 0.0
    total = 0.0
    for s, n in mag:
        e = MAG_ELEMENTS[s]
        m = local_moment(s) * n
        # heavy deep-tier asymmetry falls out of phase with the frame
        if e["tier"] == "deep" and e["u"] >= HEAVY_U:
            m = -abs(m)
        total += m
    return float(abs(total))

def curie_index(comp):
    """Thermal robustness of ORDER (any sign of J).
    Includes same-species self-coupling, weighted by count."""
    mag = [s for s in comp if MAG_ELEMENTS[s]["u"] > 0]
    if not mag:
        return 0.0
    se = SE_FACTOR if has_sink(comp) else 1.0
    j_sum, w_sum = 0.0, 0.0
    for s in mag:                       # self-coupling J_ii
        j_sum += abs(exchange_coupling(s, s)) * se * comp[s]
        w_sum += comp[s]
    for i, s1 in enumerate(mag):        # cross-coupling J_ij
        for s2 in mag[i + 1:]:
            w = (comp[s1] * comp[s2]) ** 0.5
            j_sum += abs(exchange_coupling(s1, s2)) * se * w
            w_sum += w
    j_avg = j_sum / max(w_sum, 1.0)
    return float(np.clip(j_avg * (0.4 + 0.12 * anisotropy_K(comp)), 0.0, 2.0))

# ---------------------------------------------------------------
# COMPOUND ASSESSMENT
# ---------------------------------------------------------------
def classify(comp, sublattice=None):
    m  = net_moment(comp, sublattice)
    K  = anisotropy_K(comp)
    tc = curie_index(comp)

    if m < 0.01:
        ctype = "ANTIFERRO / DIAMAGNETIC (cancels or closed)"
    elif tc < 0.15:
        ctype = "PARAMAGNETIC (order collapses thermally)"
    elif has_sink(comp):
        ctype = "FERRIMAGNETIC (incomplete sublattice cancellation)"
    elif K > 3.0 and tc > 0.8:
        ctype = "HARD FERROMAGNET (extreme retention)"
    elif K > 1.2:
        ctype = "HARD FERROMAGNET (permanent)"
    else:
        ctype = "SOFT FERROMAGNET (high permeability, low retention)"

    return {"moment": round(m, 3), "anisotropy": round(K, 2),
            "curie_index": round(tc, 2), "type": ctype,
            "energy_product": round(m * K * tc, 2)}

def report(name, comp, sublattice=None):
    r = classify(comp, sublattice)
    formula = "".join(f"{s}{(str(n) if n > 1 else '')}" for s, n in comp.items())
    print(f"\n--- {name}: {formula} ---")
    if sublattice:
        print(f"    sublattice (up/down): {sublattice}")
    print(f"    net moment     : {r['moment']:.3f} scale units")
    print(f"    anisotropy K   : {r['anisotropy']:.2f}")
    print(f"    Curie index    : {r['curie_index']:.2f}  (>0.8 robust)")
    print(f"    classification : {r['type']}")
    print(f"    energy product ~ {r['energy_product']:.2f}")
    return r

def screen(candidates):
    print("\n" + "=" * 70)
    print(" SRC MAGNETIC SCREEN - ranked by energy product")
    print("=" * 70)
    results = sorted(
        ((classify(c)["energy_product"], n, classify(c)["type"])
         for n, c in candidates.items()), reverse=True)
    for ep, name, ctype in results:
        print(f"  {name:<32} EP~{ep:6.2f}   {ctype}")
    return results

# ---------------------------------------------------------------
# DEMONSTRATIONS
# ---------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 70)
    print(" SRC MAGNETIC TENSOR ENGINE v1.2")
    print("=" * 70)

    print("\n### Calibration anchors")
    report("Iron (elemental)",   {"Fe": 1})
    report("Cobalt (elemental)", {"Co": 1})
    report("Nickel (elemental)", {"Ni": 1})
    report("Zinc (elemental)",   {"Zn": 1})
    report("Copper (elemental)", {"Cu": 1})     # v1.2: should be dead

    print("\n### v1.2 validation: exchange-sign regime")
    report("Manganese (elemental)", {"Mn": 1})  # should be ANTIFERRO now
    report("Chromium (elemental)",  {"Cr": 1})   # should be ANTIFERRO now

    print("\n### Extreme magnets")
    report("Nd2Fe14B (neodymium magnet)", {"Nd": 2, "Fe": 14, "B": 1})
    report("SmCo5 (samarium cobalt)",     {"Sm": 1, "Co": 5})
    report("GdCo5 (heavy RE analog)",     {"Gd": 1, "Co": 5})   # v1.2: moment must DROP vs SmCo5
    report("Dy-doped NdFeB (grade tuning)", {"Nd": 2, "Dy": 0.5, "Fe": 14, "B": 1})

    print("\n### Oxides: sublattice cancellation regimes")
    report("Fe3O4 (magnetite)",      {"Fe": 3, "O": 4},   sublattice={"Fe": (2, 1)})
    report("MnO (antiferro)",        {"Mn": 1, "O": 1})
    report("NiO (antiferro)",        {"Ni": 1, "O": 1})
    report("SrFe12O19 (hexaferrite)",{"Sr": 1, "Fe": 12, "O": 19}, sublattice={"Fe": (8, 4)})
    report("Y3Fe5O12 (YIG)",         {"Y": 3, "Fe": 5, "O": 12}, sublattice={"Fe": (3, 2)})

    print("\n### Screening: rare-earth-free candidates")
    screen({
        "Co-Ti (buried asymmetry)":     {"Co": 6, "Ti": 1},
        "Fe + Al + Co (Alnico analog)": {"Fe": 5, "Al": 1, "Co": 2},
        "Fe-Co lattice (permendur)":    {"Fe": 1, "Co": 1},
        "Fe + B anchor (Fe2B analog)":  {"Fe": 2, "B": 1},
        "Mn-rich (moment, low K)":       {"Mn": 4, "B": 1},
    })

