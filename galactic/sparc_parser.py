import numpy as np
import sys

def parse_sparc_master(master_file="sparc_mass_models.txt", target_galaxy="NGC2403"):
    radii, v_obs, v_gas, v_disk, v_bul = [], [], [], [], []
    
    print(f"Parsing {master_file} for galaxy: {target_galaxy}...")
    
    with open(master_file, "r") as f:
        for line in f:
            # Skip comments and header lines
            if line.startswith("#") or "=" in line or "Title" in line or "Authors" in line or "Table" in line or "Byte" in line or "---" in line:
                continue
            if not line.strip():
                continue
                
            parts = line.split()
            if len(parts) < 8:
                continue
                
            galaxy_id = parts[0]
            if galaxy_id.upper() == target_galaxy.upper():
                try:
                    # Based on Table columns: ID, D, R, Vobs, e_Vobs, Vgas, Vdisk, Vbul
                    radii.append(float(parts[2]))
                    v_obs.append(float(parts[3]))
                    v_gas.append(float(parts[5]))
                    v_disk.append(float(parts[6]))
                    v_bul.append(float(parts[7]))
                except ValueError:
                    continue

    if not radii:
        print(f"Error: Galaxy '{target_galaxy}' not found in {master_file}.")
        return None

    data = np.column_stack([radii, v_obs, v_gas, v_disk, v_bul])
    out_name = f"{target_galaxy.lower()}_extracted.csv"
    header = "r_kpc,v_obs_kms,v_gas_kms,v_disk_kms,v_bulge_kms"
    np.savetxt(out_name, data, delimiter=",", header=header, comments="")
    print(f"Success! Extracted {len(radii)} radial points to {out_name}")
    return out_name

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "NGC2403"
    parse_sparc_master(target_galaxy=target)

