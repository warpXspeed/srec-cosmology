"""
Scalar Relaxation Cosmology -- Core Physics Engine (Rev 3)
Library module: constants + physics functions. Run srec.py to use these.
"""
import numpy as np

# ------------------------- Universal constants -------------------------
G_today     = 6.67430e-11          # m^3 kg^-1 s^-2
c           = 2.99792458e8         # m/s
a_c         = 1.20e-10             # m/s^2  substrate critical tension
alpha_today = 7.2973525693e-3      # fine-structure constant today
beta_g      = -4.8e-6             # gravity strengthening rate
beta_gamma  = 5.5e-7              # EM relaxation rate
hbar        = 1.054571817e-34
eps0        = 8.8541878128e-12
yr_sec      = 365.25 * 24 * 3600
T_H         = 13.8e9 * yr_sec      # characteristic cosmic epoch

L_sun_obs   = 3.828e26             # W
M_sun       = 1.989e30             # kg

# ------------------------- Scalar field --------------------------------
# NOTE: if your existing repo has a more detailed phi()/G_eff() derivation,
# paste its body in here. The wiring in srec.py does not change.
def phi(t_sec):
    """Normalized scalar field amplitude (phi = 1.0 today)."""
    return 1.0 + beta_g * (t_sec - T_H) / T_H

def G_eff(t_sec):
    """Effective gravitational coupling: gravity locks in as phi evolves."""
    return G_today * phi(t_sec)

def alpha_eff(t_sec):
    """Effective EM coupling: charge torque weakens as the substrate relaxes."""
    return alpha_today * (1.0 + beta_gamma * (t_sec - T_H) / T_H)

# ------------------------- Rev 3 field equation ------------------------
def mu_interpolation(g_mag):
    """Rev 3 constitutive interpolation. mu -> 1 (Newtonian), mu -> g/a_c (flat)."""
    if g_mag <= 0.0:
        return 0.0
    return g_mag / (g_mag + a_c)

def g_effective(M_b, r):
    """
    Solve g * mu(g/a_c) = G M_b / r^2  exactly.
    Algebraic inversion of g^2/(g+a_c) = g_N  =>  g^2 - g_N g - g_N a_c = 0
    """
    g_N = G_today * M_b / r**2
    return 0.5 * (g_N + np.sqrt(g_N**2 + 4.0 * g_N * a_c))

def v_orbital(M_b, r):
    """Circular orbital velocity under the Rev 3 field (flat curves + BTFR)."""
    return np.sqrt(r * g_effective(M_b, r))

# ------------------------- Solar Furnace -------------------------------
def solar_power(r_helio_volt=1.0e9):
    """
    P_sun = I_sun * dV_helio. Birkeland current load model.
    dV_helio ~ 1 GV across the heliospheric load.
    """
    I_sun     = 3.9e17              # A  (inductive current into the solar load)
    dV        = r_helio_volt         # V
    return I_sun * dV, I_sun, dV

# ------------------------- Catastrophe clock ---------------------------
YD_PERIOD = 12850.0                  # yr, Younger Dryas / Hallstatt beat

def cme_kick(t_yr, period=YD_PERIOD, width=40.0):
    """
    Periodic over-pressurization pulse of the solar safety valve.
    Sharp gaussian pulse once per cycle.
    """
    phase = (t_yr % period)
    d = min(phase, period - phase)   # distance to nearest event
    return np.exp(-(d / width) ** 2)

