import numpy as np
import sys

# =====================================================================
# SREC-Cosmology: V2.2 (Full-Resolution SPARC Engine)
# =====================================================================
# Ingests any SPARC-extracted CSV and computes full radial profiles 
# for enclosed current, magnetic field stress, and audit metrics.
# =====================================================================

MU0 = 4 * np.pi * 1e-7      
KPC = 3.085677581e19        
MSUN = 1.989e30             

def run_solver(filename):
    print(f"Running inverse solver on: {filename}...")
    try:
        data = np.genfromtxt(filename, delimiter=",", names=True)
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return
    
    r = np.asarray(data["r_kpc"], dtype=float)
    v_obs = np.asarray(data["v_obs_kms"], dtype=float)
    v_gas = np.asarray(data["v_gas_kms"], dtype=float)
    v_disk = np.asarray(data["v_disk_kms"], dtype=float)
    v_bulge = np.asarray(data["v_bulge_kms"], dtype=float)
    
    # 1. Baryonic Correction: 1.33x helium factor on gas velocity squared
    v_bar_sq = v_disk**2 + (1.33 * v_gas**2) + v_bulge**2
    v_bar = np.sqrt(np.maximum(0.0, v_bar_sq))
    
    # 2. Residual deficit calculation (centripetal acceleration gap)
    r_meters = r * KPC
    v_obs_ms = v_obs * 1000.0
    v_bar_ms = v_bar * 1000.0
    a_needed = np.maximum(0.0, (v_obs_ms**2 - v_bar_ms**2) / (r_meters + 1e-9))
    
    # 3. Mass-equivalent of field stress integration
    rho_baseline = 1.0e-24 # kg/m^3 ISM baseline
    integrand = rho_baseline * a_needed * r_meters**2
    integral = np.zeros_like(r_meters)
    integral[1:] = np.cumsum(0.5 * (integrand[1:] + integrand[:-1]) * np.diff(r_meters))
    
    I_enclosed = np.sqrt(np.maximum(0.0, (8 * np.pi**2 / MU0) * integral))
    B_phi = MU0 * I_enclosed / (2 * np.pi * (r_meters + 1e-9))
    
    # 4. Clean Audit Output
    print(f"\n{'R (kpc)':<8} | {'V_obs':<8} | {'V_bar':<8} | {'I_enc (A)':<12} | {'B_phi (uG)'}")
    print("-" * 55)
    for i in range(len(r)):
        # Print every 5th point to keep terminal clean, or all if small
        if i % 5 == 0 or i == len(r) - 1:
            print(f"{r[i]:<8.2f} | {v_obs[i]:<8.1f} | {v_bar[i]:<8.1f} | {I_enclosed[i]:<12.2e} | {B_phi[i]*1e10:<8.2f}")

    # Save output
    out_name = filename.replace("_extracted.csv", "_solved.csv")
    header = "r_kpc,v_obs_kms,v_bar_kms,I_enclosed_A,B_phi_microgauss"
    output = np.column_stack([r, v_obs, v_bar, I_enclosed, B_phi*1e10])
    np.savetxt(out_name, output, delimiter=",", header=header, comments="")
    print(f"\n[Audit Log] Success: Full-resolution profile written to {out_name}")

if __name__ == "__main__":
    target_csv = sys.argv[1] if len(sys.argv) > 1 else "ngc2403_extracted.csv"
    run_solver(target_csv)

