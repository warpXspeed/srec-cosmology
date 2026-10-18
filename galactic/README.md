
# Galaxtic: Plasma-Electrodynamic Diagnostic Engine

A first-principles solver for calculating the electromagnetic current density ($J$) and magnetic field stress ($B_\phi$) required to maintain observed galactic rotation curves, using only baryonic input data.

## The Objective
To move beyond "Dark Matter" as a gravitational fudge factor. This framework treats galaxies as electrodynamic circuits. It reverse-solves the required current density ($J$) to balance the rotation of stars after accounting for observed baryonic (gas + disk + bulge) matter.

## Key Features
- **He-Corrected Baryonics:** Accounts for Helium/molecular mass in gas contribution (1.33x factor).
- **Bennett Pinch Diagnostic:** Calculates the magnetic pinch ratio ($P_{mag}/P_{plasma}$). A ratio > 1.0 identifies the transition point where electromagnetic confinement must dominate to prevent the observed rotation deficit.
- **Transparent Derivation:** No invisible particles. No halo curve-fitting. Every output is a physical requirement derived from the observed rotation deficit.

## How to use
1. **Input:** Place a SPARC-formatted CSV in the directory (`r_kpc,v_obs_kms,v_gas_kms,v_disk_kms,v_bulge_kms`).
2. **Execute:** `python3 inverse_current_solver_v2-1.py`
3. **Audit:** The engine outputs a CSV log with the required current ($I$) and the physical pinch ratio.

## Philosophy
- **Physicality over Fitting:** We do not tune parameters to hide discrepancies.
- **Diagnostic Transparency:** The tool reports the required current as a mechanical necessity, not an ontological assumption.
- **Falsifiable:** If the engine requires a pinch ratio that violates plasma stability limits (or exceeds measurable field strengths), the current hypothesis for that galaxy is falsified.

## Roadmap
- [ ] Automated batch processing for the full SPARC galaxy sample.
- [ ] Integration of direct Faraday rotation observational constraints.
- [ ] Refinement of the plasma density profile $\rho(r)$ from standard ISM models.

## Scientific Ledger & Limitations (The "Audit Log")
This framework is currently a **local galactic diagnostic engine**. 
* **Strengths:** Reproduces flat rotation curves using measured magnetic field scales (~1 μG) without non-baryonic mass.
* **Open Challenges (The Priest's Stones):**
    - **Cosmological Consistency:** This model has not yet computed the CMB power spectrum.
    - **Collision Geometry:** The mechanism by which the electromagnetic field energy decouples from collisional gas during cluster collisions (like the Bullet Cluster) remains an active research problem.
    - **Current Origin:** The framework derives the current requirement from the rotation curve; it does not yet propose the EMF source for the large-scale galactic circuit.

We invite open-source contributions to compute the CMB and structure formation spectra using the Einstein-Maxwell-Vlasov system. We prioritize verifiable field-theory derivations over the introduction of new, non-baryonic particle species.


---
*Developed as part of the Scalar Relaxation Cosmology (SRC) framework.*

