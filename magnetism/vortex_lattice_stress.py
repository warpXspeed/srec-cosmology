"""
vortex_lattice_stress.py
========================
SRC Magnetism Engine -- VLS Module v1.5 (Anisotropy Target Pivot)

Framework: Scalar Relaxation Cosmology (SRC)
Pivot:
    Target shifted from messy bulk susceptibility (chi, demag-dependent)
    to clean Single-Crystal Magnetocrystalline Anisotropy Energy (K1, J/m^3).
    K1 measures the intrinsic energy barrier to rotate spins relative to
    the vacuum grid axes, matching the VLS stress tensor (K_sigma).
"""

import numpy as np
from dataclasses import dataclass
from typing import List, Tuple, Optional
from enum import Enum

class BandType(Enum):
    D = "d"
    PI = "pi"
    P = "p"

class SpinState(Enum):
    POLARIZED = "polarized"
    PAIRED = "paired"

DEFAULT_A0 = 2.51      # Angstrom

@dataclass
class CrystalLattice:
    name: str
    a: float                    # basal (Å)
    c: float                    # axial (Å)
    gamma: float                # angle (deg)
    band_type: BandType = BandType.D
    spin_state: SpinState = SpinState.POLARIZED
    unpaired_per_formula: float = 1.0
    K1_measured: Optional[float] = None   # Clean single-crystal K1 (J/m^3)

def _frac_fit(ratio: float, n_max: int = 64) -> float:
    if ratio <= 0:
        return 0.0
    n = np.clip(np.round(ratio), 1.0, n_max)
    return float(np.exp(-abs(np.log(ratio / n))))

def hex_alignment_score(lattice: CrystalLattice, a0: float = DEFAULT_A0) -> float:
    m = _frac_fit(lattice.a / a0)
    g = lattice.gamma % 60.0
    ang_score = 1.0 - min(g, 60.0 - g) / 30.0
    kelvin_unit = a0 * np.sqrt(3) / 2.0
    c_score = _frac_fit(lattice.c / kelvin_unit)
    return float(np.clip(0.45 * m + 0.30 * ang_score + 0.25 * c_score, 0.0, 1.0))

def lattice_stress_tensor(lattice: CrystalLattice, H: float, sigma0: float = 1.0) -> np.ndarray:
    axial = H * sigma0
    basal = (1.0 - H) * sigma0
    return np.array([[basal, 0.0, 0.0],
                     [0.0, basal, 0.0],
                     [0.0, 0.0, axial]])

def principal_stress(sigma: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    vals, vecs = np.linalg.eigh(sigma)
    order = np.argsort(vals)[::-1]
    return vals[order], vecs[:, order]

def anisotropy_field_factor(sigma: np.ndarray) -> float:
    vals, _ = principal_stress(sigma)
    max_abs = np.max(np.abs(vals))
    if max_abs == 0:
        return 0.0
    return float(np.max(np.abs(vals - np.mean(vals))) / max_abs)

def predict_K1_vls(lattice: CrystalLattice, H: float, K_sigma: float,
                   k_aniso: float = 1.0) -> float:
    """
    K1_pred = k_aniso * H^2 * K_sigma * unpaired_electrons (J/m^3)
    Relates vacuum grid registry (H) and tensor stress spread (K_sigma)
    to intrinsic single-crystal anisotropy energy density.
    """
    if lattice.spin_state == SpinState.PAIRED:
        return 0.0  # Diamagnets have no single-ion spin anisotropy K1
    
    return float(k_aniso * (H ** 2) * K_sigma * lattice.unpaired_per_formula * 1e5)

def fit_vls_K1(lattices: List[CrystalLattice]) -> dict:
    measured = [l for l in lattices if l.K1_measured is not None and l.spin_state == SpinState.POLARIZED]
    if not measured:
        return {"a0": DEFAULT_A0, "k_aniso": 1.0, "mae_log10": float("inf")}

    def log_err(a0_val, k_a):
        errs = []
        for lat in measured:
            H = hex_alignment_score(lat, a0_val)
            sigma = lattice_stress_tensor(lat, H)
            Ks = anisotropy_field_factor(sigma)
            k1 = predict_K1_vls(lat, H, Ks, k_aniso=k_a)
            errs.append(abs(np.log10(abs(k1) + 1e-30) - np.log10(abs(lat.K1_measured) + 1e-30)))
        return float(np.mean(errs))

    best = {"a0": DEFAULT_A0, "k_aniso": 1.0, "mae_log10": float("inf")}
    for a0_c in np.linspace(1.0, 10.0, 51):
        for k_a in np.logspace(-2.0, 3.0, 61):
            e = log_err(a0_c, k_a)
            if e < best["mae_log10"]:
                best = {"a0": float(a0_c), "k_aniso": float(k_a), "mae_log10": e}
    return best

if __name__ == "__main__":
    # Benchmark data: Clean single-crystal K1 values (J/m^3) at room temp / low temp standard
    candidates = [
        CrystalLattice("Co (hcp)", a=2.51, c=4.07, gamma=120.0,
                       unpaired_per_formula=1.72, K1_measured=4.5e5),    # Bozorth / standard
        CrystalLattice("BaFe12O19 (Hexaferrite)", a=5.88, c=23.2, gamma=120.0,
                       unpaired_per_formula=12.0, K1_measured=3.3e5),  # High uniaxial K1
        CrystalLattice("Fe (bcc)", a=2.87, c=2.87, gamma=90.0,
                       unpaired_per_formula=2.22, K1_measured=4.8e4),    # Cubic baseline
        CrystalLattice("Ni (fcc)", a=3.52, c=3.52, gamma=90.0,
                       unpaired_per_formula=0.60, K1_measured=-4.5e3),   # Low cubic K1
    ]

    print("=" * 78)
    print("SRC Magnetism Engine -- VLS Single-Crystal K1 Simulation v1.5")
    print("Target: Intrinsic Magnetocrystalline Anisotropy Energy (J/m^3)")
    print("=" * 78)
    print()

    fit = fit_vls_K1(candidates)
    print(f"Fit: a0 = {fit['a0']:.3f} A, k_aniso = {fit['k_aniso']:.3e}")
    print(f"  log10 MAE = {fit['mae_log10']:.3f}")
    print()

    print(f"{'Compound':<28} {'H':>6} {'K_sig':>6} {'K1_pred (J/m^3)':>16} {'K1_meas':>12}")
    print("-" * 74)
    for lat in candidates:
        H = hex_alignment_score(lat, fit["a0"])
        sigma = lattice_stress_tensor(lat, H)
        Ks = anisotropy_field_factor(sigma)
        k1_p = predict_K1_vls(lat, H, Ks, k_aniso=fit["k_aniso"])
        print(f"{lat.name:<28} {H:>6.3f} {Ks:>6.3f} {k1_p:>16.2e} {lat.K1_measured:>12.2e}")

