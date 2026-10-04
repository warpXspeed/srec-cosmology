# Scalar Relaxation Cosmology (SRC)

**A single-continuum physics engine: from neutrinos to galactic cores, no dark matter required.**

SRC replaces the standard model of cosmology (GR + ΛCDM + WIMPs + singularities) with one mechanical system: a high-density neutrino/antineutrino substrate ("dark aether") whose **coupling density is gravity**, whose **pinched vortices are matter**, and whose **spallation events are the observed energy releases** (photons, electrons, flares, CMEs, polar jets).

> ⚠️ **Status:** This is an active, evolving research project — a working framework, not a finalized textbook. Core derivations are closed; numerical integration is ongoing.

---

## Quick Start (under 90 seconds)

Requires: Python 3.8+ with `numpy` (`pip install numpy`).

```bash
git clone https://github.com/warpXspeed/srec-cosmology.git
cd srec-cosmology
python3 srec.py              # self-test: validates the Rev 3 field equation
```

That's it. The default mode runs a full self-test in ~2 seconds and tells you immediately whether the engine is alive.

---

## The Three Operational Modes

The framework runs as **one app, three blades** via `srec.py`:

| Mode | Command | What it does |
| :--- | :--- | :--- |
| **Solar** | `python3 srec.py --mode solar` | Solar Furnace audit: computes $P_\odot = I_\odot \cdot \Delta V_{helio}$ as an inductive plasma load in the Galactic Current Sheet and compares to observed $L_\odot$ (**holds within 2%**). |
| **Catastrophe** | `python3 srec.py --mode catastrophe` | The 12.85 ka safety-valve clock: Younger Dryas / Hallstatt-cycle periodic over-pressurization events (GCS crossings, super-CMEs, crustal resets). |
| **Full** | `python3 srec.py --mode full` | The entire lifecycle: substrate lock-in (gravity) → pinch/tension loop → spall (photons/electrons/CMEs) → tension drop → stable baseline. |
| **Test** | `python3 srec.py --mode test` *(default)* | Self-test of `core.py`: verifies the Newtonian limit at Earth's orbit ($\mu \approx 1$) and the flat-curve / BTFR limit at galactic radius. |

---

## Core Physics (Rev 3)

The master field equation — **no dark matter halos, no fitted parameters**:

$$\nabla \cdot \left[ \mu\left(\frac{|\nabla\Phi|}{a_c}\right) \nabla\Phi \right] = 4\pi G \rho_b, \qquad \mu(x) = \frac{x}{1+x}$$

* **High acceleration** ($g \gg a_c$): $\mu \to 1$ → pure Newtonian gravity. Solar System untouched.
* **Low acceleration** ($g \ll a_c$): $g = \sqrt{G M_b a_c}/r$ → **flat rotation curves** and the **Baryonic Tully-Fisher Relation** ($v^4 = G M_b a_c$) emerge identically.

Key couplings: $\beta_g = -4.8\times10^{-6}$ (gravity strengthening), $\beta_\gamma = 5.5\times10^{-7}$ (EM relaxation), $a_c = 1.2\times10^{-10}$ m/s² (substrate critical tension).

### Closed results
| Target | Status | Result |
| :--- | :--- | :--- |
| Galactic rotation / BTFR | Closed | $v^4 = G M_b a_c$, zero dark matter |
| Solar power output | Closed | $P_\odot \approx 3.9\times10^{26}$ W (within 2% of $L_\odot$) |
| Charge quantization ($e_0$) | Closed in form | Shear-pin yield of the substrate ("rev limiter"), $W=1$ Hopfion |
| Baryon asymmetry ($\eta$) | Closed | $\eta \approx 6.1\times10^{-10}$ as condensation saturation threshold |
| CMB (2.7 K) | Interpreted | Idle temperature of the resting substrate, not a Big Bang afterglow |

---

## Repository Structure

```text
srec-cosmology/
├── README.md              # You are here
├── core.py                # The ONLY file with raw physics: constants, φ field, Rev 3 gravity
├── srec.py                # Main launcher (solar / catastrophe / full / test)
│
├── docs/                  # Theory, derivations, and operational manuals
│   ├── EVALUATION_REV3.md            # Current mathematical specification (Rev 3 closure)
│   ├── EVALUATION_REV2.md            # Archived: superseded field equation (historical record)
│   ├── THEORY_SOLAR_FURNACE.md       # Full solar inductive-load derivation
│   └── CIRCUIT_DYNAMICS_AND_VALVES.md # Recursive pinch-tension loop & spallation valves
│
├── neutrinos/             # Substrate specifications & micro-mechanics
│   ├── the-neutrino-substrate.md     # Continuum axioms, density, elastic modulus
│   ├── The Neutrino Condensate.md    # Macroscopic quantum fluid properties
│   ├── The Closed-Loop Photon.md     # Bound νν̄ pair topology
│   └── Macro-Lattice Coupling.md     # Micro-vortex → macro-potential translation
│
├── analysis/              # Observational reconciliation & case studies
│   ├── juno-jupiter-analysis.md      # Juno gravity harmonics vs. electromagnetic core
│   └── Solar-Galactic-event.md       # The 12 ka reset: Younger Dryas, GCS crossing
│
├── modes/                 # Runtime execution modules (solar_system, catastrophe_clock)
├── planetary/             # Orbital mechanics & 12 ka paleoclimate solvers
└── periodic/              # Reaction engine v5 & harmonic spiral maps
```

---

## File Roles

* **`core.py`** — the physics library. Constants ($G$, $\beta_g$, $\beta_\gamma$, $a_c$), the scalar field $\phi(t)$, effective couplings `G_eff` / `alpha_eff`, the Rev 3 gravity solver (`mu_interpolation`, `g_effective`, `v_orbital`), and the catastrophe clock. It produces no output when run alone; it is imported by everything else.
* **`srec.py`** — the entry point. Parses `--mode` and drives the corresponding routines. Always run this, not `core.py`.

---

## Current Development Targets

1. **Numerical $e_0$:** convert the closed-form Hopfion yield derivation into a computed value from $\tau_s$ (substrate shear modulus) without fitting to $\alpha$.
2. **$\eta$ simulation:** model the condensation of a $\nu\bar{\nu}$ cloud under the Rev 3 field and verify $\eta \to 6\times10^{-10}$ as the stable attractor.
3. **Pipeline audit:** ensure `reaction_engine_v5.py` and the `full` lifecycle mode ingest the Rev 3 field equation directly (no legacy fallbacks).

See `docs/EVALUATION_REV3.md` for the full mathematical closure audit.

