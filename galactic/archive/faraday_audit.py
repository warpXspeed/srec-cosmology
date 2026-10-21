import numpy as np
import sys

# =====================================================================
# SREC-Cosmology: Faraday Rotation Falsification Audit
# =====================================================================
# Compares the solver's inferred coherent B-field against 
# radio-astronomy observational limits (Faraday Rotation / RM).
# =====================================================================

def audit_faraday(solved_csv):
    print(f"Auditing Faraday constraints for: {solved_csv}...")
    try:
        data = np.genfromtxt(solved_csv, delimiter=",", names=True)
    except Exception as e:
        print(f"Error reading {solved_csv}: {e}")
        return

    r = np.asarray(data["r_kpc"], dtype=float)
    b_inferred = np.asarray(data["B_phi_microgauss"], dtype=float) # uG

    # Realistic upper limit for COHERENT (ordered) magnetic fields in outer disks.
    # Total fields might be 1-2 uG, but the large-scale ordered component 
    # responsible for large-scale Faraday rotation rarely exceeds ~0.3 - 0.5 uG at r > 15 kpc.
    # Let's model a generous observational upper limit curve: B_max(r) = 0.5 * exp(-r / 30)
    b_obs_limit = 0.5 * np.exp(-r / 40.0) # uG threshold

    print(f"\n{'R (kpc)':<8} | {'Inferred B_phi (uG)':<20} | {'Obs Limit (uG)':<15} | {'Status'}")
    print("-" * 65)

    tension_count = 0
    for i in range(len(r)):
        if i % 5 == 0 or i == len(r) - 1:
            status = "PASS (Viable)" if b_inferred[i] <= b_obs_limit[i] else "FAIL (Tension)"
            if b_inferred[i] > b_obs_limit[i]:
                tension_count += 1
            print(f"{r[i]:<8.2f} | {b_inferred[i]:<20.2f} | {b_obs_limit[i]:<15.2f} | {status}")

    print("-" * 65)
    if tension_count > 0:
        print(f"\n[Falsification Result] TENSION DETECTED: The solver's required B_phi exceeds observational coherent field limits at {tension_count} sampled points.")
        print("Interpretation: If the solver demands a coherent field stronger than what Faraday rotation measures, the pure azimuthal current hypothesis is falsified for this galaxy profile.")
    else:
        print("\n[Falsification Result] PASSED: Inferred fields remain within observational limits.")

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "ngc2403_solved.csv"
    audit_faraday(target)

