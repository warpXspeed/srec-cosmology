#!/usr/bin/env python3
"""
build_clean_seed_db.py -- The Fixed-Ruler Extraction Engine
============================================================
Filters the SPARC master database to retain ONLY galaxies with 
independent, geometric, non-Hubble-flow distance measurements 
(TRGB, Cepheids, clusters; f_D in {2, 3, 4, 5}). 
Strips out expanding-metric assumptions entirely.
"""

import csv
import os

def build_clean_database(table1_path="SPARC - Mass Models.txt", 
                           master_path="sparc_mass_models.txt", 
                           out_csv="clean_seed_database.csv"):
    
    print("Scanning Table 1 for fixed-ruler geometric distance anchors...")
    clean_galaxies = {}

    # 1. Parse Table 1 to find galaxies with f_D >= 2
    with open(table1_path, "r") as fh:
        for line in fh:
            s = line.strip()
            if not s or s.startswith("#") or s.startswith("Title") or s.startswith("Authors") or s.startswith("Table") or s.startswith("Byte") or s.startswith("---"):
                continue
            parts = s.split()
            if len(parts) < 6:
                continue
            
            name = parts[0].strip()
            try:
                # Column layout: Galaxy (0), T (1), D (2), e_D (3), f_D (4), Inc (5)
                f_d = int(parts[4])
                distance = float(parts[2])
                inclination = float(parts[5])
            except (ValueError, IndexError):
                continue

            # Keep ONLY independent geometric rulers
            if f_d >= 2:
                clean_galaxies[name.upper()] = {
                    "distance_mpc": distance,
                    "distance_method": f_d,
                    "inclination_deg": inclination
                }

    print(f"Found {len(clean_galaxies)} galaxies with fixed geometric rulers (f_D >= 2).")

    # 2. Extract their raw radial profiles from the mass model master file
    print(f"Extracting raw telemetry for clean galaxies from {master_path}...")
    
    current_galaxy = None
    extracted_data = []
    matched_count = 0

    with open(master_path, "r") as fh:
        for line in fh:
            s = line.strip()
            if not s or s.startswith("#") or s.startswith("Title") or s.startswith("Authors") or s.startswith("Table") or s.startswith("Byte") or s.startswith("---"):
                continue
            
            parts = s.split()
            if len(parts) < 8:
                continue

            name = parts[0].strip().upper()
            if name in clean_galaxies:
                if name != current_galaxy:
                    current_galaxy = name
                    matched_count += 1
                
                try:
                    # Mass model columns: ID (0), D (1), R_kpc (2), Vobs (3), e_Vobs (4), Vgas (5), Vdisk (6), Vbul (7)
                    r_kpc = float(parts[2])
                    v_obs = float(parts[3])
                    v_gas = float(parts[5])
                    v_disk = float(parts[6])
                    v_bul  = float(parts[7])
                    
                    extracted_data.append({
                        "galaxy": name,
                        "distance_mpc": clean_galaxies[name]["distance_mpc"],
                        "distance_method": clean_galaxies[name]["distance_method"],
                        "r_kpc": r_kpc,
                        "v_obs_kms": v_obs,
                        "v_gas_kms": v_gas,
                        "v_disk_kms": v_disk,
                        "v_bulge_kms": v_bul
                    })
                except ValueError:
                    continue

    # 3. Write out the clean seed database
    os.makedirs("clean_db", exist_ok=True, mode=0o755)
    out_path = os.path.join("clean_db", out_csv)
    
    fields = ["galaxy", "distance_mpc", "distance_method", "r_kpc", "v_obs_kms", "v_gas_kms", "v_disk_kms", "v_bulge_kms"]
    with open(out_path, "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(extracted_data)

    print("=" * 65)
    print("CLEAN SEED DATABASE CREATED")
    print("=" * 65)
    print(f"Matched galaxies written : {matched_count}")
    print(f"Total radial data points : {len(extracted_data)}")
    print(f"Output saved to          : {out_path}")
    print("=" * 65)
    print("Hubble-flow (f_D=1) rubber-ruler galaxies completely purged.")

if __name__ == "__main__":
    build_clean_database()

