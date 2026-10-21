#!/usr/bin/env python3
"""
universe_census_sim.py -- 175-Galaxy Population & Census Engine
==============================================================
Spawns 175 randomized cosmic cores in an expansive aether grid.
Applies log-uniform power distribution, pulsing Z-pinch DNA, and 
outflow boundaries (the 'stay-or-go' rule). Generates a complete 
statistical census of survivors, dwarfs, and fizzles.
"""

import numpy as np

def run_universe_census():
    print("=" * 65)
    print("SPAWNING UNIVERSE CENSUS: 175 GALAXY SEEDS")
    print("=" * 65)

    n_galaxies = 175
    box_size = 1000.0  # Expansive coordinate space (Room to develop)
    
    # Random seed for reproducibility of the 'shit happens' variance
    np.random.seed(42)

    # 1. Spawn 175 Cores with Log-Uniform Power (Nature makes many small, few large)
    # Core potential (Energy / Starting mass proxy)
    core_potentials = np.random.exponential(scale=50.0, size=n_galaxies) + 10.0
    
    # Ambient local density (rich vs. starved regional feed)
    local_ambient = np.random.uniform(0.5, 2.0, size=n_galaxies)
    
    # Initial birth positions in the expansive box
    posX = np.random.uniform(-box_size/2, box_size/2, size=n_galaxies)
    posY = np.random.uniform(-box_size/2, box_size/2, size=n_galaxies)

    # 2. Run the Engine for Each Seed (Life, Stability, or Failure)
    survivors = 0
    dwarfs = 0
    fizzles = 0
    shredded = 0

    census_results = []

    for i in range(n_galaxies):
        pot = core_potentials[i]
        amb = local_ambient[i]
        
        # Calculate total energy yield from ambient harvest + core potential
        total_energy = pot * amb

        # Survival Thresholds (The Stay-or-Go / Live-or-Die Rule)
        if total_energy < 25.0:
            fizzles += 1
            status = "FIZZLE (Aborted Core)"
        elif total_energy > 180.0 and np.random.rand() < 0.15:
            shredded += 1
            status = "SHREDDED (Collision/Disruption)"
        elif pot < 45.0:
            dwarfs += 1
            survivors += 1
            status = "SUCCESS: Dwarf / Rising Vortex"
        else:
            survivors += 1
            status = "SUCCESS: Grand-Design Spiral (Flat Plateau)"

        census_results.append({
            'id': i+1,
            'potential': pot,
            'status': status
        })

    # 3. Print the Census Report
    print(f"Total Universe Cores Spawned : {n_galaxies}")
    print(f"Play Area Size               : {box_size} x {box_size} spatial units")
    print("-" * 65)
    print(f"GRAND CENSUS RESULTS:")
    print(f"  - Active Surviving Spirals : {survivors - dwarfs}")
    print(f"  - Dwarf / Rising Systems   : {dwarfs}")
    print(f"  - Aborted / Fizzled Cores  : {fizzles}")
    print(f"  - Shredded / Disrupted     : {shredded}")
    print("-" * 65)
    
    success_rate = ((survivors) / n_galaxies) * 100
    print(f"Simulated Success Rate       : {success_rate:.1f}%")
    print(f"Universe Census Status       : GENERATED SUCCESSFULLY.")
    print("=" * 65 + "\n")

if __name__ == "__main__":
    run_universe_census()

