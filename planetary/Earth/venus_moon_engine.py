#!/usr/bin/env python3
"""
src/venus_moon_engine.py  (v3.1 - Pompeii Escalation Model, Calibrated)
Simulates the Sun-Venus-Moon 3-body orbital mechanics and tests
the two-stage Birkeland ejection trigger:

  STAGE 1 (Pompeii Precursor): Days 1-5 of surge -> gradual orbital
           energy pumping (drives eccentricity + crustal stress/Tesserae)
           Orbit remains BOUND during this phase (survivable but fatal
           fatigue). Cumulative Delta-v ~ 200 m/s.
  STAGE 2 (Terminal Bump):     Day 6 impulse kick (~690 m/s Delta-v)
           -> escape velocity exceeded -> Hill Sphere breach
           -> Heliocentric crossing orbit toward Earth.

Calibration basis:
    Lunar circular velocity @ 200,000 km:   ~1,275 m/s
    Lunar escape velocity   @ 200,000 km:   ~1,803 m/s
    Escape margin (circular):               ~528 m/s
    At Day-6 apogee (~245,000 km):
        local velocity ~950 m/s, local escape ~1,627 m/s
        -> requires ~677 m/s of Delta-v at that phase
    TERMINAL_A = 8.0e-2 m/s^2 x 8,640 s (0.1 day) = ~690 m/s -> UNBOUND

Usage:
    python3 venus_moon_engine.py            # runs both tests
    python3 venus_moon_engine.py --csv      # also dumps orbit_history.csv
"""

import numpy as np
import math
import csv
import argparse

# ==============================================================================
# PHYSICAL CONSTANTS (SI UNITS)
# ==============================================================================
G = 6.67430e-11          # Gravitational constant (m^3 / kg / s^2)
M_SUN = 1.9885e30        # Sun mass (kg)
M_VENUS = 4.8675e24      # Venus mass (kg)
M_MOON = 7.3477e22       # Moon mass (kg) ~ Earth's Moon / Former Venus Moon
AU = 1.495978707e11      # Astronomical Unit (m)
DAY = 86400.0            # Seconds in a day
YEAR = 365.25 * DAY      # Seconds in a year

# ==============================================================================
# SYSTEM CONFIGURATION
# ==============================================================================
A_VENUS = 0.723332 * AU  # Semi-major axis of Venus (m)
R_MOON_INIT = 200_000e3  # Initial lunar orbital radius from Venus (200,000 km)
V_A_PLASMA = 5.0e5       # Mean Alfven velocity in filament (m/s)

# ==============================================================================
# POMPEII ESCALATION PARAMETERS (CALIBRATED SI, m/s^2)
# These are the "KP12 Venusian Ejection Constants" for the repository.
# ==============================================================================
PRECURSOR_START_DAY = 1.0    # Stage 1 begins
PRECURSOR_END_DAY   = 5.0    # Stage 1 ends
TERMINAL_BUMP_DAY   = 6.0    # Stage 2 impulse
BUMP_DURATION_DAYS  = 0.1    # width of the terminal kick window

PRECURSOR_A_BASE = 2.0e-4    # Stage 1 base accel (m/s^2), ramps 1x -> 5x
                             # Integrate over 4 days: ~200 m/s Delta-v
                             # Orbit inflates ~200k -> ~245k km, remains BOUND

TERMINAL_A       = 8.0e-2    # Stage 2 impulsive accel (m/s^2)
                             # x 8,640 s (0.1 day) = ~690 m/s Delta-v
                             # Calibrated for apogee intercept:
                             # local v ~950 m/s, local escape ~1,627 m/s
                             # -> 690 m/s clears the ~677 m/s margin

class CelestialBody:
    def __init__(self, name, mass, pos, vel):
        self.name = name
        self.mass = mass
        self.pos = np.array(pos, dtype=np.float64)
        self.vel = np.array(vel, dtype=np.float64)
        self.acc = np.zeros(3, dtype=np.float64)

def compute_gravitational_accelerations(bodies):
    """Computes pure Newtonian N-body gravitational accelerations."""
    for b in bodies:
        b.acc = np.zeros(3, dtype=np.float64)

    n = len(bodies)
    for i in range(n):
        for j in range(i + 1, n):
            r_vec = bodies[j].pos - bodies[i].pos
            dist = np.linalg.norm(r_vec)
            if dist == 0:
                continue
            force_mag = G / (dist**3)
            bodies[i].acc += force_mag * bodies[j].mass * r_vec
            bodies[j].acc -= force_mag * bodies[i].mass * r_vec

def tangential_unit(rel_pos):
    """Prograde tangential unit vector for a planar orbit."""
    t = np.array([-rel_pos[1], rel_pos[0], 0.0])
    norm = np.linalg.norm(t)
    return t / norm if norm > 0 else t

def apply_pompeii_surge(venus, moon, current_day):
    """
    Two-stage electrodynamic escalation (calibrated):

    STAGE 1 - THE PRECURSOR (Days 1-5):
      Gradual Lorentz pumping aligned with the Moon's motion.
      Physically corresponds to sustained J x B torque: crustal torsion
      (Tesserae formation), induction heating, escalating seismic stress.
      The orbit inflates and eccentricity climbs, but the moon remains
      bound - the Pompeii phase: survivable, fatiguing, escalating.

    STAGE 2 - THE TERMINAL BUMP (Day 6, 0.1-day window):
      Impulsive Lorentz discharge from the solar core rupture.
      Delivers ~690 m/s: total exceeds escape margin -> the SNAP.
    """
    rel_pos = moon.pos - venus.pos
    t_hat = tangential_unit(rel_pos)

    # ---------------- STAGE 1: PRECURSOR PUMPING ----------------
    if PRECURSOR_START_DAY <= current_day <= PRECURSOR_END_DAY:
        # Escalating intensity (linear ramp): stress builds day over day
        ramp = (current_day - PRECURSOR_START_DAY) / \
               (PRECURSOR_END_DAY - PRECURSOR_START_DAY)          # 0 -> 1
        a_torque = PRECURSOR_A_BASE * (1.0 + 4.0 * ramp)          # 2e-4 -> 1e-3
        moon.acc += a_torque * t_hat

    # ---------------- STAGE 2: TERMINAL BUMP --------------------
    elif abs(current_day - TERMINAL_BUMP_DAY) <= (BUMP_DURATION_DAYS / 2.0):
        # Massive impulsive discharge - the "snap"
        moon.acc += TERMINAL_A * t_hat

def orbital_elements(venus, moon):
    """Returns (distance_km, specific_orbital_energy, eccentricity)."""
    mu = G * (M_VENUS + M_MOON)
    rel_pos = moon.pos - venus.pos
    rel_vel = moon.vel - venus.vel
    r = np.linalg.norm(rel_pos)
    v2 = np.dot(rel_vel, rel_vel)

    energy = 0.5 * v2 - mu / r                                # <0 bound, >0 escape
    h_vec = np.cross(rel_pos, rel_vel)
    e_vec = (np.cross(rel_vel, h_vec) / mu) - (rel_pos / r)
    ecc = np.linalg.norm(e_vec)
    return r / 1e3, energy, ecc

def run_simulation(duration_days=100.0, dt_sec=60.0, trigger_surge_day=None,
                   csv_out=None, label="RUN"):
    """Symplectic Leapfrog Integrator with Pompeii escalation module."""
    sun = CelestialBody("Sun", M_SUN, [0.0, 0.0, 0.0], [0.0, 0.0, 0.0])
    v_venus_mag = math.sqrt(G * M_SUN / A_VENUS)
    venus = CelestialBody("Venus", M_VENUS,
                          [A_VENUS, 0.0, 0.0], [0.0, v_venus_mag, 0.0])
    v_moon_rel = math.sqrt(G * M_VENUS / R_MOON_INIT)
    moon = CelestialBody("Moon", M_MOON,
                         [A_VENUS + R_MOON_INIT, 0.0, 0.0],
                         [0.0, v_venus_mag + v_moon_rel, 0.0])

    bodies = [sun, venus, moon]
    hill_sphere_venus = A_VENUS * ((M_VENUS / (3.0 * M_SUN)) ** (1.0/3.0))
    total_steps = int((duration_days * DAY) / dt_sec)

    print(f"\n================ {label} ================")
    print(f"[*] Venus Orbit:      {A_VENUS/AU:.4f} AU")
    print(f"[*] Moon Orbit Rad:   {R_MOON_INIT/1e3:.1f} km")
    print(f"[*] Hill Sphere:      {hill_sphere_venus/1e3:.1f} km")
    print(f"[*] Surge Trigger:    Day {trigger_surge_day}")
    print(f"[*] Duration:         {duration_days} days (dt={dt_sec}s)")

    compute_gravitational_accelerations(bodies)

    ejected = False
    ejection_day = None
    bound_snapshots = []     # track the escalation during precursor phase
    history = []

    for step in range(total_steps):
        current_day = (step * dt_sec) / DAY

        # Leapfrog integration
        for b in bodies:
            b.vel += 0.5 * b.acc * dt_sec
        for b in bodies:
            b.pos += b.vel * dt_sec

        compute_gravitational_accelerations(bodies)

        # Pompeii escalation module
        if trigger_surge_day is not None and current_day >= trigger_surge_day:
            apply_pompeii_surge(venus, moon, current_day)

        for b in bodies:
            b.vel += 0.5 * b.acc * dt_sec

        # Telemetry every ~6 hours
        if step % 360 == 0:
            dist_km, energy, ecc = orbital_elements(venus, moon)
            history.append((round(current_day, 3), round(dist_km, 1),
                            round(ecc, 4), round(energy, 2)))
            # Log the escalating precursor phase (Pompeii curve)
            if (trigger_surge_day is not None
                    and PRECURSOR_START_DAY <= current_day <= TERMINAL_BUMP_DAY):
                bound_snapshots.append(
                    f"    Day {current_day:5.2f}:  dist={dist_km:>12,.1f} km  "
                    f"ecc={ecc:6.4f}  {'BOUND' if energy < 0 else 'UNBOUND'}")

        # Hill Sphere breach check
        dist_km, energy, ecc = orbital_elements(venus, moon)
        if not ejected and (
            dist_km * 1e3 > hill_sphere_venus or energy >= 0.0
        ):
            ejected = True
            ejection_day = current_day
            trigger_word = ("ESCAPE VELOCITY" if energy >= 0.0 else "HILL SPHERE")
            print(f"\n[!] BREACH at Day {ejection_day:.3f} "
                  f"({trigger_word} exceeded):")
            print(f"    - Distance: {dist_km:,.1f} km")
            print(f"    - Eccentricity: {ecc:.3f}")
            print(f"    - Moon entered HELIOCENTRIC CROSSING ORBIT.")

    # Print the Pompeii escalation log (the forensic record)
    if bound_snapshots:
        print("\n[*] PRECURSOR ESCALATION LOG (Tesserae/stress window):")
        for line in bound_snapshots:
            print(line)

    final_dist, final_energy, final_ecc = orbital_elements(venus, moon)
    print(f"\n[*] Simulation Complete ({label}):")
    print(f"    - Final Distance: {final_dist:,.1f} km")
    print(f"    - Final Eccentricity: {final_ecc:.4f}")
    print(f"    - Final Energy Sign: {'UNBOUND (escape)' if final_energy >= 0 else 'BOUND'}")
    print(f"    - System State: "
          f"{'EJECTED / HELIOCENTRIC DRIFT' if ejected else 'STABLE BOUND ORBIT'}")

    if csv_out:
        with open(csv_out, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["day", "distance_km", "eccentricity",
                        "specific_energy_J_per_kg"])
            w.writerows(history)
        print(f"    - History saved: {csv_out}")

    return ejected, ejection_day

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", action="store_true",
                        help="dump orbit_history.csv files")
    args = parser.parse_args()

    # TEST 1: Stable baseline (no surge) - must remain bound
    run_simulation(duration_days=100.0, dt_sec=60.0,
                   trigger_surge_day=None,
                   csv_out="orbit_history_test1.csv" if args.csv else None,
                   label="TEST 1: STABLE BASELINE")

    # TEST 2: Pompeii escalation - precursor ramp + terminal bump on Day 6
    run_simulation(duration_days=100.0, dt_sec=60.0,
                   trigger_surge_day=1.0,
                   csv_out="orbit_history_test2.csv" if args.csv else None,
                   label="TEST 2: POMPEII SURGE (CALIBRATED)")

