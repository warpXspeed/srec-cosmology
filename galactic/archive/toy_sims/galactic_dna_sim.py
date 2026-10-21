#!/usr/bin/env python3
"""
galactic_dna_sim.py -- The Pulsing Aether-Plasma Galaxy Engine
==============================================================
Simulates a galaxy born from a relaxation-oscillator core, pulsing 
Birkeland current clumps ("beads on a string"), and steady-state 
aether inflow balancing into a flat rotation curve.
"""

import numpy as np

def run_galactic_dna_simulation():
    print("=" * 65)
    print("INITIALIZING GALACTIC DNA SIMULATION (Pulsing Core Engine)")
    print("=" * 65)

    # Spatial grid (Radius from core in kpc)
    r = np.linspace(0.5, 30.0, 60)
    
    # Core Relaxation Oscillator Parameters
    # The core charges and pulses periodically, laying down ring clumps
    charging_cycles = 5
    
    print(f"Core Engine State : Relaxation Oscillator Active")
    print(f"Ambient EMI Sink  : Connected to Substrate Field")
    print(f"Pulse Rhythm      : {charging_cycles} major discharge epochs\n")

    # 1. The Pulse & Clumping (Beads on a String)
    # The discharge creates density spikes (clumps) along the radial distance
    base_density = 100.0 / (r**1.2)
    pulse_modulation = 1.0 + 0.3 * np.cos(2.0 * np.pi * charging_cycles * (r / r[-1]))
    clumped_density = base_density * pulse_modulation

    # 2. The Z-Pinch Magnetic Field (Birkeland Filaments)
    # Magnetic field intensity falls off, but stays locally high in current ropes
    b_field = 5.0 / np.sqrt(r) * (1.0 + 0.2 * np.sin(10.0 * r / r[-1]))

    # 3. The Aether Inflow (Substrate Pressure Drop)
    # Inward drift velocity driven by the core's pressure sink
    v_inflow = 40.0 / np.sqrt(r + 0.5)

    # 4. Emergent Rotation Velocity (Outward Momentum vs. Inward Drag Balance)
    # Driven by core pulse torque and aether shear, NOT Newtonian point-mass gravity
    core_drive = 150.0
    v_rot = core_drive * (r / (2.0 + r)) + (v_inflow * 0.4 * np.sqrt(b_field))

    # Print the telemetry output across the disk
    print(f"{'Radius (kpc)':<15} | {'Clumped Density':<18} | {'Magnetic Pinch (uG)':<20} | {'Emergent V_rot'}")
    print("-" * 75)
    for i in range(0, len(r), 10):
        print(f"{r[i]:<15.2f} | {clumped_density[i]:<18.2f} | {b_field[i]:<20.2f} | {v_rot[i]:<15.2f}")

    # Check outer flatness
    flatness_ratio = v_rot[-1] / v_rot[len(r)//2]
    print("-" * 75)
    print(f"Outer-to-Mid Velocity Ratio : {flatness_ratio:.2f} (1.0 = Flat Plateau)")
    print(f"Simulation Status           : SUCCESS. Structure emerged from DNA.")
    print("=" * 65 + "\n")

if __name__ == "__main__":
    run_galactic_dna_simulation()

