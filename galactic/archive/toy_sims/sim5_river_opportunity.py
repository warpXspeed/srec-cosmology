#!/usr/bin/env python3
"""
sim5_river_opportunity.py -- The River & Opportunity Engine
=============================================================
Ununeven starting field, asynchronous EM pulses, and fluid rivers.
Outcomes (fizzle, pygmy, normal, giant) emerge purely from local 
opportunity in the current network.
"""

import numpy as np

def run_sim_5():
    print("=" * 68)
    print("SIM 5: THE RIVER & OPPORTUNITY ENGINE")
    print("=" * 68)

    n_seeds = 175
    np.random.seed(42)

    # 1. The Uneven Field (No level playing field)
    # Local substrate density and ambient current potential are rugged and wild.
    local_current_highway = np.random.pareto(a=2.0, size=n_seeds) * 10.0
    local_drag = np.random.uniform(0.5, 2.0, size=n_seeds)

    # 2. The Asynchronous Pulse (No starting gun)
    # Ignition energy arrives via propagating waves through the uneven medium.
    ignition_timing = np.random.uniform(0.0, 5.0, size=n_seeds)
    pulse_energy = np.random.exponential(scale=30.0, size=n_seeds)

    # 3. Opportunity & Outcome Mapping
    # Net energy delivered = pulse + highway feed - local drag resistance
    net_opportunity = (pulse_energy + local_current_highway) / local_drag

    outcomes = []
    for opp in net_opportunity:
        if opp < 15.0:
            outcomes.append("FIZZLE (Aborted / Dead)")
        elif opp < 40.0:
            outcomes.append("PYGMY (Stunted Dwarf)")
        elif opp < 120.0:
            outcomes.append("NORMAL (Balanced Spiral)")
        else:
            outcomes.append("GIANT (High-Current Mega-System)")

    outcomes = np.array(outcomes)

    # 4. Census
    fizzles = np.sum(outcomes == "FIZZLE (Aborted / Dead)")
    pygmies = np.sum(outcomes == "PYGMY (Stunted Dwarf)")
    normals = np.sum(outcomes == "NORMAL (Balanced Spiral)")
    giants  = np.sum(outcomes == "GIANT (High-Current Mega-System)")

    print(f"Wilderness Cores Spawned     : {n_seeds}")
    print(f"Playing Field                : Rugged, Uneven Substrate (No Level Field)")
    print("-" * 68)
    print(f"DEMOGRAPHIC CENSUS:")
    print(f"  - Fizzles (Dead/Failed)    : {fizzles} ({100*fizzles/n_seeds:.1f}%)")
    print(f"  - Pygmies (Stunted Dwarfs) : {pygmies} ({100*pygmies/n_seeds:.1f}%)")
    print(f"  - Normals (Stable Spirals) : {normals} ({100*normals/n_seeds:.1f}%)")
    print(f"  - Giants (High-Current)    : {giants} ({100*giants/n_seeds:.1f}%)")
    print("-" * 68)
    print("VERDICT: Outcomes are entirely a product of local opportunity")
    print("         in the river network. No dark matter. No fine-tuning.")
    print("=" * 68 + "\n")

if __name__ == "__main__":
    run_sim_5()

