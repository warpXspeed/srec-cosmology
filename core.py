# ======================================================================
# Scalar Relaxation Cosmology - Core Physics Engine (Rev 3)
# ======================================================================

import numpy as np

# Universal substrate parameters
G_today          = 6.67430e-11        # m³ kg⁻¹ s⁻²
c                = 2.99792458e8       # m s⁻¹
a_c              = 1.20e-10           # m s⁻² (Substrate critical tension)
alpha_today      = 7.2973525693e-3    # Fine-structure constant
beta_g           = -4.8e-6            # Gravity coupling factor
beta_gamma       =  5.5e-7            # EM relaxation factor

def mu_interpolation(g_mag: float) -> float:
    """
    Corrected Rev 3 Constitutive Interpolation Function.
    Replaces the divergent Rev 2 (1 + a_c/g) relation.
    """
    if g_mag <= 0.0:
        return 0.0
    return g_mag / (g_mag + a_c)

def g_effective(M_baryon: float, r: float) -> float:
    """
    Computes real acceleration from baryonic mass under the corrected phi field.
    Solves: g * mu(g / a_c) = G * M_b / r²
    """
    g_N = (G_today * M_baryon) / (r**2)
    # Exact algebraic inversion of g² / (g + a_c) = g_N:
    # g² - g_N * g - g_N * a_c = 0
    g_real = 0.5 * (g_N + np.sqrt(g_N**2 + 4.0 * g_N * a_c))
    return g_real

def v_rotational(M_baryon: float, r: float) -> float:
    """
    Computes orbital velocity showing flat rotation curve and BTFR.
    """
    g = g_effective(M_baryon, r)
    return np.sqrt(r * g)
