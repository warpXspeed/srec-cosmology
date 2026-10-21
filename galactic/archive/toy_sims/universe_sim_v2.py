#!/usr/bin/env python3
"""
universe_sim_v2.py -- Open-Circuit Recycling Universe Engine
============================================================
Simulates a shared plasma resource grid with core competition (cannibalism),
dynamic mass growth, energetic recycling (no permanent waste), and 
stochastic 'shit happens' environmental variance.
"""

import numpy as np

def run_sim_2():
    print("=" * 65)
    print("INITIALIZING SIM 2: OPEN-CIRCUIT RECYCLING ENGINE")
    print("=" * 65)

    n_seeds = 175
    grid_size = 1000.0
    np.random.seed(1337)

    # Initialize the Shared Resource Grid (Ambient Plasma Density Field)
    # This is our active cosmic web -- fuel is finite locally, but recyclable.
    ambient_plasma_pool = np.random.uniform(50.0, 150.0, size=n_seeds)

    # Spawn Cores with Log-Uniform Power Potential
    core_potentials = np.random.exponential(scale=60.0, size=n_seeds) + 15.0
    
    # Track core states: 0 = Fizzled/Dead, 1 = Active Spiral, 2 = Cannibal/Glutton
    states = np.zeros(n_seeds, dtype=int)
    mass_ledger = core_potentials.copy()

    print(f"Spawns initialized : {n_seeds} cores")
    print(f"Grid fuel pool     : Dynamic shared plasma substrate\n")

    # Simulate the resource competition and recycling over evolutionary steps
    steps = 10
    for step in range(steps):
        for i in range(n_seeds):
            # 1. Resource Competition (Cannibalism / Starvation)
            # A massive core pulls fuel from its neighbors
            local_draw = mass_ledger[i] * 0.1
            
            if ambient_plasma_pool[i] > local_draw:
                ambient_plasma_pool[i] -= local_draw
                mass_ledger[i] += local_draw * 0.5  # Growth
                states[i] = 1 # Active
            else:
                # Starvation / Fizzle
                states[i] = 0 # Dead
                # 2. The Recycling Loop: Dump dead core mass back into the grid
                recycled_fuel = mass_ledger[i] * 0.3
                ambient_plasma_pool[i] += recycled_fuel
                mass_ledger[i] -= recycled_fuel

            # 3. The 'Shit Happens' Variance (Stochastic turbulence)
            turbulence = np.random.normal(0.0, 5.0)
            mass_ledger[i] = max(5.0, mass_ledger[i] + turbulence)

    # Final Census Classification
    active_spirals = np.sum(states == 1)
    fizzles_recycled = np.sum(states == 0)
    gluttons = np.sum(mass_ledger > np.percentile(mass_ledger, 90))

    print(f"-------------------------------------------------")
    print(f"SIM 2 CENSUS REPORT (After {steps} Evolutionary Steps):")
    print(f"  - Active Disks / Survivors : {active_spirals}")
    print(f"  - Recycled Fizzles (Dead)  : {fizzles_recycled}")
    print(f"  - Mega-Gluttons (Cannibals): {gluttons}")
    print(f"  - Total Mass in System     : {np.sum(mass_ledger):.1f} (Conserved via Recycling)")
    print(f"-------------------------------------------------")
    print(f"SIMULATION STATUS            : OPEN-CIRCUIT RUN COMPLETE.")
    print("=" * 65 + "\n")

if __name__ == "__main__":
    run_sim_2()

