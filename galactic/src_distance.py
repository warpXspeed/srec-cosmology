import numpy as np

# SRC DFM Tired Light / Fluid Damping Distance Calculator
# Replaces expanding-metric distance integrals with a linear aether-damping constant.

C_KMS = 299792.458  # Speed of light in km/s

def src_distance(z, h_src=70.0):
    """
    Computes Euclidean distance (Mpc) using SRC linear aether damping 
    instead of standard FLRW expanding metric.
    
    z: observed redshift
    h_src: SRC damping velocity parameter (km/s/Mpc)
    """
    # Recalculate recession speed from redshift directly via local damping
    v_rec = z * C_KMS
    
    # Distance in Mpc (Euclidean / non-expanding)
    distance_mpc = v_rec / h_src
    return distance_mpc

if __name__ == "__main__":
    test_z = 0.05  # Example low redshift galaxy
    d = src_distance(test_z)
    print(f"Observed Redshift z: {test_z}")
    print(f"SRC Euclidean Distance: {d:.2f} Mpc")

