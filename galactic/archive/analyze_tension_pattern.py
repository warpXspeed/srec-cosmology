#!/usr/bin/env python3
"""
analyze_tension_pattern.py -- Diagnostic Correlation Engine
============================================================
Examines all audited points from the SPARC master run to determine 
whether the Faraday audit tension is a systematic scaling trend (math/medium 
dependency) or random data acquisition noise (sketchy telemetry/geometry).
"""

import csv
import sys
import numpy as np

def analyze_tension(summary_csv="audit_output/audit_summary.csv"):
    galaxies = []
    verdicts = []
    b_outer = []
    r_max = []
    a_anom = []

    try:
        with open(summary_csv, "r") as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                galaxies.append(row["galaxy"])
                verdicts.append(row["verdict"])
                b_outer.append(float(row["B_outer_max_uG"]) if row["B_outer_max_uG"] else 0.0)
                r_max.append(float(row["r_max_kpc"]) if row["r_max_kpc"] else 0.0)
                a_anom.append(float(row["a_anom_outer_max_m_s2"]) if row["a_anom_outer_max_m_s2"] else 0.0)
    except Exception as e:
        print(f"Error reading {summary_csv}: {e}")
        print("Run dark_matter_audit.py first to generate audit_summary.csv.")
        return

    b_outer = np.array(b_outer)
    r_max = np.array(r_max)
    a_anom = np.array(a_anom)
    verdicts = np.array(verdicts)

    # Filter to non-passing (MARGINAL and FAIL_NOMINAL) to examine the "tension" population
    mask_tension = (verdicts == "MARGINAL") | (verdicts == "FAIL_NOMINAL")
    
    print("=" * 65)
    print("DIAGNOSTIC CORRELATION ANALYSIS (The 1-Issue Hypothesis)")
    print("=" * 65)
    print(f"Total galaxies in audit : {len(b_outer)}")
    print(f"Galaxies in tension     : {mask_tension.sum()}")

    if mask_tension.sum() < 2:
        print("Insufficient tension data for correlation.")
        return

    # Correlations for the tension group
    corr_r = np.corrcoef(b_outer[mask_tension], r_max[mask_tension])[0, 1]
    corr_a = np.corrcoef(b_outer[mask_tension], np.log10(a_anom[mask_tension] + 1e-15))[0, 1]

    print(f"\n[Metric 1] B_phi Tension vs. Physical Size (R_max)")
    print(f"  Correlation coefficient : {corr_r:.3f}")

    print(f"\n[Metric 2] B_phi Tension vs. Log(Max Anomalous Acceleration)")
    print(f"  Correlation coefficient : {corr_a:.3f}")

    print("-" * 65)
    if abs(corr_a) > 0.5 or abs(corr_r) > 0.5:
        print("DIAGNOSTIC RESULT: Systematic Trend Detected.")
        print("Interpretation: The tension is NOT random noise. It scales predictably")
        print("with physical scale or acceleration. This confirms the 'constant' (rho_0)")
        print("must be treated as a dynamic variable dependent on local system properties.")
    else:
        print("DIAGNOSTIC RESULT: Weak/Scattered Correlation.")
        print("Interpretation: The tension does not cleanly track global size or max acceleration.")
        print("The issue is likely driven by local data acquisition artifacts (e.g., individual")
        print("inclination errors, warps, or streaming noise in specific galaxies).")
    print("=" * 65)

if __name__ == "__main__":
    analyze_tension()

