#!/usr/bin/env python3
"""
check_rubber_ruler.py -- Cross-references audit failures against SPARC distance methods.
"""

import csv
import sys

def analyze_failures(summary_csv="audit_output/audit_summary.csv", table1_file="SPARC - Mass Models.txt"):
    # Load failures from our audit summary
    failures = set()
    with open(summary_csv, "r") as fh:
        r = csv.DictReader(fh)
        for row in r:
            if row["verdict"].startswith("FAIL") or row["verdict"] == "MARGINAL":
                failures.add(row["galaxy"].strip().upper())

    print(f"Loaded {len(failures)} non-passing galaxies from audit summary.")

    # Parse Table1.mrt for distance method f_D
    # Format description from table header:
    # Galaxy: 1-11, D: 14-19, f_D: 25-26
    hub_flow_count = 0
    geo_count = 0
    total_checked = 0

    with open(table1_file, "r") as fh:
        for line in fh:
            if line.startswith("#") or len(line.strip()) < 30:
                continue
            # Try to parse fixed columns or whitespace-delimited tokens
            parts = line.split()
            if len(parts) < 6:
                continue
            
            gal_name = parts[0].strip().upper()
            if gal_name in failures:
                total_checked += 1
                # Find the distance method flag (f_D)
                # In SPARC Table 1, f_D is typically the integer after distance and error
                try:
                    # Let's inspect tokens or use character slices if format is strict
                    # Token-based heuristic: usually [Galaxy, T, D, e_D, f_D, Inc, ...]
                    f_d_val = int(parts[4])
                    if f_d_val == 1:
                        hub_flow_count += 1
                    else:
                        geo_count += 1
                except (ValueError, IndexError):
                    pass

    print("=" * 60)
    print("RUBBER RULER AUDIT RESULTS")
    print("=" * 60)
    print(f"Non-passing galaxies matched in Table 1 : {total_checked}")
    print(f"  Hubble-Flow Assumed (f_D = 1)         : {hub_flow_count} ({hub_flow_count/max(1,total_checked)*100:.1f}%)")
    print(f"  Independent Geometry (f_D > 1)        : {geo_count} ({geo_count/max(1,total_checked)*100:.1f}%)")
    print("=" * 60)

if __name__ == "__main__":
    analyze_failures()

