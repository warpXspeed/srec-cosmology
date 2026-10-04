"""
Mode 2 — Only the 12.85 ka + Hallstatt reset cycles.
No planet formation, no Oort feeding. Pure solar variability.
"""

import numpy as np
import matplotlib.pyplot as plt
from core import cme_kick, sec_per_yr, age_universe_sec

def run():
    main_period    = 12850
    hallstatt_per  = main_period / 5.35

    years_ago = np.linspace(0, 30000, 12000)
    t_sec_ago = age_universe_sec - years_ago * sec_per_yr

    kick = (cme_kick(t_sec_ago, main_period, amplitude=0.162) *
            cme_kick(t_sec_ago, hallstatt_per, amplitude=0.032))

    events = {
        12850: "Younger Dryas\n12.85 ka catastrophe",
         8200: "8.2 ka event",
         5900: "5.9 ka aridification",
         4200: "4.2 ka collapse",
         3200: "Bronze Age collapse"
    }

    plt.figure(figsize=(12,7))
    plt.plot(years_ago/1000, kick, color='#b22222', lw=2.5)
    plt.fill_between(years_ago/1000, 1.0, kick, where=kick>1, color='red', alpha=0.2)

    for yr, txt in events.items():
        idx = np.argmin(np.abs(years_ago - yr))
        plt.axvline(years_ago[idx]/1000, color='k', ls='--', alpha=0.7)
        plt.text(years_ago[idx]/1000, kick[idx]+0.015, txt,
                 ha='center', fontsize=11, weight='bold')

    plt.title('SREC Mode 2 — Pure Catastrophe Clock\n(12.85 ka + Hallstatt cycles only)')
    plt.xlabel('Thousands of years ago')
    plt.ylabel('Solar/coronal output (× today)')
    plt.ylim(0.95, 1.20)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.show()

    yd_idx = np.argmin(np.abs(years_ago - 12850))
    print(f"Younger Dryas peak = {kick[yd_idx]:.4f} × today → ~{int(kick[yd_idx]*1000)/10:.0f}× energy")

if __name__ == '__main__':
    run()
