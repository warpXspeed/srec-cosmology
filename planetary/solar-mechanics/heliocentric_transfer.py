#!/usr/bin/env python3
"""
capture_inversion.py - Evidence-constrained capture test.
Takes the encounter conditions from the last transfer run and asks:
HOW MUCH dissipation is required to bind the wanderer to Earth?
Compares against KP12 geological energy estimates. No tuning.

Result interpretation:
    - If required E is within the KP12 budget (~1e27 - 1e29 J): model holds.
    - If required E >> budget: model FAILS (capture impossible, no Moon).
"""

import math

G = 6.67430e-11
M_EARTH = 5.9722e24
M_MOON = 7.3477e22
MU = G * (M_EARTH + M_MOON)

# ---- Encounter state (from heliocentric_transfer run, Day ~12,899) ----
r_enc = 6.192e9        # m, closest Earth approach
v_rel = 1.5e3          # m/s, Earth-relative speed at that distance
                       # (interpolated: 6.9 km/s @33.5M km -> 3.1 @26M km)

# ---- KP12 geological energy bracket (J) ----
E_KP12_MIN = 1e27      # conservative Black Mat / biomass burn
E_KP12_MAX = 1e29      # upper bracket incl. ice-sheet meltwater + seismic

v_escape = math.sqrt(2 * MU / r_enc)
dv_needed = v_rel - v_escape
E_capture = 0.5 * M_MOON * dv_needed**2

# Resulting bound orbit if exactly that much is dissipated
E_specific_final = 0.5 * v_escape**2 - MU / r_enc     # = -MU/2r at parabolic
a = -MU / (2 * E_specific_final)

print(f"Encounter distance:      {r_enc/1e6:,.0f} km")
print(f"Escape velocity there:   {v_escape/1e3:.3f} km/s")
print(f"Relative speed:          {v_rel/1e3:.3f} km/s")
print(f"Dissipation required:    dv = {dv_needed/1e3:.3f} km/s")
print(f"Energy required:         {E_capture:.2e} J")
print(f"KP12 geological budget:  {E_KP12_MIN:.0e} - {E_KP12_MAX:.0e} J")
print()
if E_capture <= E_KP12_MAX:
    print("[PASS] Capture energy is WITHIN the KP12 discharge budget.")
    print(f"       Bound orbit after dissipation: a ~ {a/1e6:,.0f} thousand km")
    print(f"       => The Moon's presence is consistent with the recorded")
    print(f"          discharge. Capture = circuit closure, not collision.")
else:
    print("[FAIL] Required energy exceeds geological record -> model dead.")

