Copy-pasting from chat windows constantly drops formatting. Let's bypass copy-pasting entirely.

Run this one-liner in your terminal inside your srec-cosmology directory. It will write the correct README.md file directly to your disk with all formatting intact:

python3 -c '
content = """# Scalar Relaxation Cosmology (SRC)

**A single-continuum physics engine: from neutrinos to galactic cores, no dark matter required.**

SRC replaces the standard model of cosmology (GR + ΛCDM + WIMPs + singularities) with one mechanical system: a high-density neutrino/antineutrino substrate ("dark aether") whose **coupling density is gravity**, whose **pinched vortices are matter**, and whose **spallation events are the observed energy releases** (photons, electrons, flares, CMEs, polar jets).

> ⚠️ **Status:** This is an active, evolving research project — a working framework, not a finalized textbook. Core derivations are closed; numerical integration is ongoing.

---

## Quick Start (under 90 seconds)

Requires: Python 3.8+ with `numpy` (`pip install numpy`).

\`\`\`bash
git clone https://github.com/warpXspeed/srec-cosmology.git
cd srec-cosmology
python3 srec.py   # self-test: validates the Rev 3 field equation
\`\`\`

That is it. The default mode runs a full self-test in ~2 seconds and tells you immediately whether the engine is alive.

---

## The Three Operational Modes

The framework runs as **one app, three blades** via `srec.py`:

| Mode | Command | What it does |
| :--- | :--- | :--- |
| **Solar** | `python3 srec.py --mode solar` | Solar Furnace audit: computes $P_\\odot = I_\\odot \\cdot \\Delta V_{helio}$ as an inductive plasma load in the Galactic Current Sheet and compares to observed $L_\\odot$ (**holds within 2%**). |
| **Catastrophe** | `python3 srec.py --mode catastrophe` | The 12.85 ka safety-valve clock: Younger Dryas / Hallstatt-cycle periodic over-pressurization events (GCS crossings, super-CMEs, crustal resets). |
| **Full** | `python3 srec.py --mode full` | The entire lifecycle: substrate lock-in (gravity) → pinch/tension loop → spall (photons/electrons/CMEs) → tension drop → stable baseline. |
| **Test** | `python3 srec.py --mode test` *(default)* | Self-test of `core.py`: verifies the Newtonian limit at Earth orbit ($\\mu \\approx 1$) and the flat-curve / BTFR limit at galactic radius. |

---

## Core Physics (Rev 3)

The master field equation — **no dark matter halos, no fitted parameters**:

$$\\nabla \\cdot \\left[ \\mu\\left(\\frac{|\\nabla\\Phi|}{a_c}\\right) \\nabla\\Phi \\right] = 4\\pi G \\rho_b, \\qquad \\mu(x) = \\frac{x}{1+x}$$

* **High acceleration** ($g \\gg a_c$): $\\mu \\to 1$ → pure Newtonian gravity. Solar System untouched.
* **Low acceleration** ($g \\ll a_c$): $g = \\sqrt{G M_b a_c}/r$ → **flat rotation curves** and the **Baryonic Tully-Fisher Relation** ($v^4 = G M_b a_c$) emerge identically.

Key couplings: $\\beta_g = -4.8\\times10^{-6}$ (gravity strengthening), $\\beta_\\gamma = 5.5\\times10^{-7}$ (EM relaxation), $a_c = 1.2\\times10^{-10}$ m/s² (substrate critical tension).

### Closed results

| Target | Status | Result |
| :--- | :--- | :--- |
| Galactic rotation / BTFR | Closed | $v^4 = G M_b a_c$, zero dark matter |
| Solar power output | Closed | $P_\\odot \\approx 3.9\\times10^{26}$ W (within 2% of $L_\\odot$) |
| Charge quantization ($e_0$) | Closed in form | Shear-pin yield of the substrate ("rev limiter"), $W=1$ Hopfion |
| Baryon asymmetry ($\\eta$) | Closed | $\\eta \\approx 6.1\\times10^{-10}$ as condensation saturation threshold |
| CMB (2.7 K) | Interpreted | Idle temperature of the resting substrate, not a Big Bang afterglow |

---

## Core Theoretical Principles

The mathematical engine above rests on a unified physical picture, documented in full under `docs/`:

1. **The Aether Substrate.** Space is not an empty vacuum; it is a physical, history-preserving fluid medium whose baseline excitation resolves to coupled neutrino–antineutrino wave dynamics.
2. **Plasma as the Baseline.** More than 99% of the visible universe is plasma in a cold, quiescent baseline state — the default, not the exception. Active plasmas (solar coronae, glowing nebulae) are high-stress transition zones driven by macro-scale Birkeland currents.
3. **Toroidal Charge Topology.** Charge is not a static property; it is a directional hydrodynamic vector. An electron is an inward-drawing sink; a positron is an outward-pushing source. "Antimatter" is simply inverted rotational chirality of the same toroidal node.
4. **Z-Pinch Nucleosynthesis.** Heavy elements are not forged in gentle stellar cores or rare neutron-star mergers; they are synthesized rapidly via electromagnetic Z-pinch compression within galactic current bottlenecks.
5. **Deterministic Radioactivity.** Radioactive decay is not a random statistical coin-flip. It is forced mechanical failure — dissonant, over-spun wave injection (neutrino/photon fluxes) breaking a node toroidal phase lock, shed as α / β / γ discharge.
6. **Scale-Invariant Harmonic Spacing.** The spacing of electron shells in atoms, planetary orbits in solar systems, and star streams in galaxies are driven by the same hydrodynamic wave equations, solved via Riemann theta functions on compact Riemann surfaces.

See `docs/SRC_CORE_MECHANICS_OVERVIEW.md` for the master architectural overview tying all six principles into one causal pipeline.

---

## Repository Structure

\`\`\`text
srec-cosmology/
├── README.md               # You are here
├── core.py                 # The ONLY file with raw physics: constants, φ field, Rev 3 gravity
├── srec.py                 # Main launcher (solar / catastrophe / full / test)
│
├── docs/                   # Theory, derivations, and operational manuals
│   ├── SRC_CORE_MECHANICS_OVERVIEW.md   # Master theoretical overview (all principles)
│   ├── EVALUATION_REV3.md                # Current mathematical specification (Rev 3 closure)
│   ├── EVALUATION_REV2.md                # Archived: superseded field equation (historical record)
│   ├── THEORY_SOLAR_FURNACE.md           # Full solar inductive-load derivation
│   ├── CIRCUIT_DYNAMICS_AND_VALVES.md    # Recursive pinch-tension loop & spallation valves
│   │
│   ├── 01_PLASMA_DYNAMICS/
│   │   └── plasma_dynamics.md            # Quiescent baseline, Z-pinches, current networks
│   ├── 02_TOROIDAL_TOPOLOGY/
│   │   ├── charge_as_vortex.md           # Hydrodynamic sinks/sources, chirality & antimatter
│   │   └── atomic_double_torus.md       # Equatorial planes, chemical bonding resonance
│   ├── 03_NUCLEOSYNTHESIS_AND_DECAY/
│   │   ├── dynamic_synthesis.md         # Z-pinch heavy element formation (Gold, Uranium)
│   │   ├── harmonic_resonance_table.md  # Replacing the static Periodic Table
│   │   └── induced_radioactivity.md     # Deterministic wave-stress failure (α, β, γ)
│   └── 04_DFM_ENGINE_MATHEMATICS/
│       ├── riemann_theta_derivation.md  # Multi-periodic wave interference math
│       ├── scale_invariance_proofs.md   # Micro-to-macro unified scaling (atoms to galaxies)
│       └── inverse_solver_spec.md       # Reverse-engineering core spin/density from orbits
│
├── neutrinos/              # Substrate specifications & micro-mechanics
│   ├── the-neutrino-substrate.md        # Continuum axioms, density, elastic modulus
│   ├── The Neutrino Condensate.md       # Macroscopic quantum fluid properties
│   ├── The Closed-Loop Photon.md        # Bound νν̄ pair topology
│   └── Macro-Lattice Coupling.md        # Micro-vortex → macro-potential translation
│
├── analysis/               # Observational reconciliation & case studies
│   ├── juno-jupiter-analysis.md         # Juno gravity harmonics vs. electromagnetic core
│   └── Solar-Galactic-event.md         # The 12 ka reset: Younger Dryas, GCS crossing
│
├── modes/                  # Runtime execution modules (solar_system, catastrophe_clock)
├── planetary/              # Orbital mechanics & 12 ka paleoclimate solvers
└── periodic/               # Reaction engine v5 & harmonic spiral maps
\`\`\`

---

## File Roles

* **`core.py`** — the physics library. Constants ($G$, $\\beta_g$, $\\beta_\\gamma$, $a_c$), the scalar field $\\phi(t)$, effective couplings `G_eff` / `alpha_eff`, the Rev 3 gravity solver (`mu_interpolation`, `g_effective`, `v_orbital`), and the catastrophe clock. It produces no output when run alone; it is imported by everything else.
* **`srec.py`** — the entry point. Parses `--mode` and drives the corresponding routines. Always run this, not `core.py`.

---

## Current Development Targets

1. **Numerical $e_0$:** convert the closed-form Hopfion yield derivation into a computed value from $\\tau_s$ (substrate shear modulus) without fitting to $\\alpha$.
2. **$\\eta$ simulation:** model the condensation of a $\\nu\\bar{\\nu}$ cloud under the Rev 3 field and verify $\\eta \\to 6\\times10^{-10}$ as the stable attractor.
3. **Pipeline audit:** ensure `reaction_engine_v5.py` and the `full` lifecycle mode ingest the Rev 3 field equation directly (no legacy fallbacks).
4. **Inverse solver implementation:** per `docs/04_DFM_ENGINE_MATHEMATICS/inverse_solver_spec.md`, build the bi-directional diagnostic — feed measured shell/orbital radii into the theta-function optimization and derive core spin ($\\omega$) and density ($\\rho$) directly. The Rev 3 solver in `core.py` is the forward machinery; this closes the loop in reverse.

See `docs/EVALUATION_REV3.md` for the full mathematical closure audit, or `docs/SRC_CORE_MECHANICS_OVERVIEW.md` for the theoretical architecture.
"""
with open("README.md", "w") as f:
    f.write(content)
print("README.md successfully written!")
'
