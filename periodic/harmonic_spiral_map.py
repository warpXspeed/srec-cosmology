"""
Harmonic Octave Map (Engineering Drafting Plate Edition)
Scalar Relaxation Cosmology - Atomic Harmonics Module

All 118 elements on fixed radial steps with labeled octave rings.
Wrapped in an authentic technical drafting frame.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import Rectangle
import numpy as np
import os

# ---------------------------------------------------------------
# THE 6 MECHANICAL ARCHETYPES (Color Key)
# ---------------------------------------------------------------
ARCHETYPES = {
    "BLUE":  "#1E88E5",   # Primary Boundary Shedder (+)
    "LBLUE": "#4FC3F7",   # Secondary Boundary Shedder (2+)
    "GREEN": "#2E7D32",   # Structural Hub (0)
    "RED":   "#E53935",   # High Aether Sink (-)
    "WHITE": "#CFD8DC",   # Harmonic Zero (0) - inert
    "GOLD":  "#FBC02D",   # Core Transition Tensor
}

SYMBOLS = [
    "H","He","Li","Be","B","C","N","O","F","Ne",
    "Na","Mg","Al","Si","P","S","Cl","Ar","K","Ca",
    "Sc","Ti","V","Cr","Mn","Fe","Co","Ni","Cu","Zn",
    "Ga","Ge","As","Se","Br","Kr","Rb","Sr","Y","Zr",
    "Nb","Mo","Tc","Ru","Rh","Pd","Ag","Cd","In","Sn",
    "Sb","Te","I","Xe","Cs","Ba","La","Ce","Pr","Nd",
    "Pm","Sm","Eu","Gd","Tb","Dy","Ho","Er","Tm","Yb",
    "Lu","Hf","Ta","W","Re","Os","Ir","Pt","Au","Hg",
    "Tl","Pb","Bi","Po","At","Rn","Fr","Ra","Ac","Th",
    "Pa","U","Np","Pu","Am","Cm","Bk","Cf","Es","Fm",
    "Md","No","Lr","Rf","Db","Sg","Bh","Hs","Mt","Ds",
    "Rg","Cn","Nh","Fl","Mc","Lv","Ts","Og",
]
assert len(SYMBOLS) == 118

NOBLE      = {2, 10, 18, 36, 54, 86, 118}
ALKALI     = {3, 11, 19, 37, 55, 87}
ALKEARTH   = {4, 12, 20, 38, 56, 88}
HALOGEN    = {9, 17, 35, 53, 85, 117}
NONMETAL   = {1, 6, 7, 8, 15, 16, 34, 52}
STRUCTURAL = {5, 14, 32, 33, 51}

def archetype(z):
    if z in NOBLE:      return "WHITE"
    if z in ALKALI:     return "BLUE"
    if z in ALKEARTH:   return "LBLUE"
    if z in HALOGEN:    return "RED"
    if z in NONMETAL:   return "RED" if z != 6 else "GREEN"
    if z in STRUCTURAL: return "GREEN"
    return "GOLD"

def polarity_mark(z):
    if z in NOBLE:          return ""
    if z in ALKALI:         return "\u207A"
    if z in ALKEARTH:       return "\u00B2\u207A"
    if z in HALOGEN:        return "\u207B"
    if z in (8, 16, 34, 52): return "\u00B2\u207B"
    if z in (7, 15):        return "\u00B3\u207B"
    if z == 1:              return "\u207B"
    if z in (5, 14, 32, 33, 51): return ""
    return "\u1D57"

# Fixed-step placement math
Z_MAX   = 118
R_START = 2.0
R_STEP  = 0.072
TURNS   = 7.0
DTHETA  = TURNS * 2 * np.pi / Z_MAX

def spiral_point(z):
    theta = (z - 1) * DTHETA
    r = R_START + (z - 1) * R_STEP
    return r * np.cos(theta), r * np.sin(theta), r, theta

# ---------------------------------------------------------------
# FIGURE & DRAFTING PLATE STYLING
# ---------------------------------------------------------------
BG_COLOR = "#0b0f17"  # Deep technical drafting slate
fig = plt.figure(figsize=(18, 14), facecolor=BG_COLOR)
gs = gridspec.GridSpec(1, 2, width_ratios=[3.2, 1.3], wspace=0.03, figure=fig)

ax = fig.add_subplot(gs[0])
ax.set_facecolor(BG_COLOR)
axl = fig.add_subplot(gs[1])
axl.set_facecolor(BG_COLOR)

# Add double-line engineering frame border to the map panel
frame = Rectangle((-12.2, -12.2), 24.4, 24.4, linewidth=2,
                  edgecolor="#37474F", facecolor="none", zorder=10)
frame_inner = Rectangle((-12.0, -12.0), 24.0, 24.0, linewidth=0.8,
                        edgecolor="#263238", facecolor="none", zorder=10)
ax.add_patch(frame)
ax.add_patch(frame_inner)

# --- Octave rings + labels ---
octave_labels = ["O1:He", "O2:Ne", "O3:Ar", "O4:Kr",
                 "O5:Xe", "O6:Rn", "O7:Og"]
label_angle = np.radians(118)
for i, z_noble in enumerate(sorted(NOBLE)):
    _, _, r_ring, _ = spiral_point(z_noble)
    circle = plt.Circle((0, 0), r_ring, color="#455A64",
                        fill=False, linewidth=1.2, linestyle="--", zorder=2)
    ax.add_patch(circle)
    lx = (r_ring + 0.28) * np.cos(label_angle)
    ly = (r_ring + 0.28) * np.sin(label_angle)
    ax.text(lx, ly, octave_labels[i], ha="center", va="center",
            fontsize=8.5, color="#B0BEC5", fontweight="bold", zorder=7)

# --- Place 118 elements ---
for z, sym in enumerate(SYMBOLS, start=1):
    x, y, r, theta = spiral_point(z)
    color = ARCHETYPES[archetype(z)]
    mark = polarity_mark(z)

    ax.scatter(x, y, s=180, c=color, edgecolors="white",
               linewidths=0.7, zorder=5)
    ax.text(x, y, f"{sym}{mark}", ha="center", va="center",
            fontsize=6.5, fontweight="bold", color="black", zorder=6)

# Core marker
ax.scatter([0], [0], s=180, c="white", marker="*", zorder=4)
ax.text(0, -0.6, "AETHER CORE", ha="center", va="top",
        fontsize=8, color="white", fontweight="bold")

# Title block (Engineering stamp style)
ax.text(0, 11.4, "SCALAR RELAXATION COSMOLOGY", ha="center",
        fontsize=10, color="#90A4AE", tracking=1.5)
ax.text(0, 10.7, "HARMONIC OCTAVE MAP (Z: 1 — 118)", ha="center",
        fontsize=16, fontweight="bold", color="white")

ax.set_xlim(-12.5, 12.5)
ax.set_ylim(-12.5, 12.5)
ax.set_aspect("equal")
ax.axis("off")

# ---------------------------------------------------------------
# LEGEND & TECHNICAL GUIDE PANEL
# ---------------------------------------------------------------
axl.set_xlim(0, 10)
axl.set_ylim(0, 13)
axl.axis("off")

# Side panel frame
side_frame = Rectangle((0.2, 0.5), 9.6, 12.1, linewidth=1.5,
                       edgecolor="#37474F", facecolor="none")
axl.add_patch(side_frame)

axl.text(5, 11.9, "MECHANICAL KEY", ha="center", fontsize=13,
         fontweight="bold", color="white")

legend_entries = [
    ("Primary Shedder",       "BLUE",  "+",   "Loose outer ring; sheds freely"),
    ("Secondary Shedder",     "LBLUE", "2+",  "Two outer rings; higher tension"),
    ("Structural Hub",        "GREEN", "0",   "Balanced symmetric lattice geometry"),
    ("High Aether Sink",      "RED",   "-",   "Aggressive inward boundary pull"),
    ("Harmonic Zero",         "WHITE", "0",   "Octave closure; inert / zero shear"),
    ("Core Transition Tensor","GOLD",  "t",   "Multi-octave internal torsional fold"),
]

y = 10.7
for label, key, pol, desc in legend_entries:
    axl.scatter([1.0], [y], s=240, c=ARCHETYPES[key],
                edgecolors="white", linewidths=1.2, zorder=5)
    axl.text(1.7, y, f"{label} [{pol}]", fontsize=10,
             color="white", fontweight="bold", va="center")
    axl.text(1.7, y - 0.38, desc, fontsize=7.5,
             color="#90A4AE", va="center")
    y -= 1.25

# Plain-English Guide Box
axl.text(5, 2.7, "HOW TO READ THE RINGS", ha="center", fontsize=10,
         fontweight="bold", color="#FBC02D")

guide_text = (
    "• Dashed rings = Acoustic octaves\n"
    "• Expanding outward (O1 -> O7) scales\n"
    "  the atom, packing in boundary rings.\n"
    "• At the ring (White): Octave is full.\n"
    "  Pressure balances to zero (inert).\n"
    "• Just past a ring (Blue): New octave\n"
    "  starts with a loose shedding ring.\n"
    "• Just before a ring (Red): Octave is\n"
    "  nearly full; pulls hard to lock."
)
axl.text(0.6, 2.1, guide_text, fontsize=8, color="#ECEFF1",
         family="monospace", va="top", linespacing=1.3)

# ---------------------------------------------------------------
# SAVE PLATE
# ---------------------------------------------------------------
plt.savefig("harmonic_spiral_map.png", dpi=120, facecolor=BG_COLOR, bbox_inches="tight")
plt.savefig("harmonic_spiral_map.pdf", facecolor=BG_COLOR, bbox_inches="tight")
print("Saved technical drafting plate: harmonic_spiral_map.png / .pdf")

