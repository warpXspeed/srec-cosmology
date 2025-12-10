"""
core.py — the only file that contains the raw physics.
Never changes. Imported by every mode.
"""

import numpy as np

# ======================================================================
# Universal constants
# ======================================================================
G_today          = 6.67430e-11                    # m³ kg⁻¹ s⁻²
alpha_today      = 7.2973525693e-3                 # fine-structure constant today
sec_per_yr       = 365.25 * 24 * 3600
age_universe_sec = 13.787e9 * sec_per_yr           # seconds since Big Bang

# ======================================================================
# Scalar field φ and effective couplings (the two β parameters)
# ======================================================================
beta_g     = -4.8e-6      # gravity gets stronger
beta_gamma =  5.5e-7      # electromagnetism gets weaker

def phi(t_sec: float) -> float:
    """Scalar field — rolls from ≈0.82 (early universe) → 0 (today)."""
    t_yr = t_sec / sec_per_yr
    return 0.82 * (1.0 - t_yr / 13.8e9)

def G_eff(t_sec: float) -> float:
    return G_today * np.exp(-beta_g * phi(t_sec))

def alpha_eff(t_sec: float) -> float:
    return alpha_today * np.exp(beta_gamma * phi(t_sec))

# ======================================================================
# Periodic super-CME kicks (used by catastrophe modes)
# ======================================================================
def cme_kick(t_sec: float, period_yr: float, amplitude: float = 0.162) -> float:
    """Single sinusoidal kick. Amplitude 0.162 → 162× spike."""
    t_yr  = t_sec / sec_per_yr
    phase = 2 * np.pi * (t_yr % period_yr) / period_yr
    return 1.0 + amplitude * np.sin(phase)**2

