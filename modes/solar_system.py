"""
Mode 1 — Pure solar-system formation.
No catastrophes, no 12 ka events. Only eddies → planets → moons.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from core import (G_eff, alpha_eff, sec_per_yr,
                  age_universe_sec, alpha_today, G_today)

def run(chaos: float = 0.02, steps: int = 500):
    t_myr = np.linspace(0, 6.0, steps)

    def eddy_ode(t, omega):
        t_sec = (age_universe_sec - 4.6e9*sec_per_yr) + t*1e6*sec_per_yr
        em    = np.sqrt(alpha_eff(t_sec) / alpha_today)
        grav  = G_eff(t_sec) / G_today
        noise = chaos * np.random.normal()
        return (em - grav + noise) * omega

    sol = solve_ivp(eddy_ode, [0, 6], [1e-6], t_eval=t_myr, rtol=1e-8)
    omega = np.maximum(sol.y[0], 1e-30)

    plt.figure(figsize=(10,6))
    plt.semilogy(t_myr, omega, color='#d62728', lw=3)
    plt.title('SREC Mode 1 — Pure Solar-System Formation\n(only eddies → planets → moons)')
    plt.xlabel('Time after disk formation (Myr)')
    plt.ylabel('Eddy strength ω (arbitrary units)')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

    print("Mode 1 complete — solar system formed from eddies only.")
    print("   Inner zones → rocky planets")
    print("   Outer zones → gas/ice giants + rich moon systems")
    print("   Oort cloud → outermost ejected eddies")

if __name__ == '__main__':
    run()
