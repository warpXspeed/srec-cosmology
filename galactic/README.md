# SREC-Cosmology: Galactic Module

Scalar Relaxation Cosmology (SRC) — a first-principles framework for
galactic dynamics with **zero dark matter, zero dark energy, zero
expanding metric**. This module audits galactic rotation telemetry and
tests fluid-plasma substrate mechanisms against real data.

## Method: The Anti-Fudge Protocol

1. **No ghosts.** No invisible mass, no adjustable halos, no naming
   the unmeasured and calling the name a measurement.
2. **No rubber rulers.** The clean database uses only the 78 SPARC
   galaxies with fixed-ruler (geometric) distances — TRGB, Cepheids,
   masers — purged of Hubble-flow contamination.
3. **No self-grading.** Every mechanism is stated with its
   falsification condition BEFORE the test runs. Failed mechanisms go
   in the ledger, not in a footnote.
4. **Process over mirror.** Simulations here are generative process
   engines, not curve-fitting spreadsheets. We do not tune a model to
   hug a pre-filtered dataset; we run the physics and read the verdict.

## Core empirical findings

- 98.7% of clean-anchor galaxies never reach Keplerian decline.
  Outer disks: 56.6% flat, 42.1% rising.
- Flat vs. rising rotation separates cleanly by scale — a structural
  signal, not noise.
- The low-acceleration regime scales with a raw model-free slope of
  **0.575** — between Newtonian mass (1.0) and pure response (0.5),
  contradicting unseen-mass scaling.
- A single universal coupling scale (a0 ≈ 3.55e-11 m/s²) tracks all
  78 galaxies with zero per-galaxy parameters — the signature of a
  medium response, not custom halos.

## Repository layout

| Path                                   | Contents                                                   |
| -------------------------------------- | ---------------------------------------------------------- |
| `clean_db/` + `build_clean_seed_db.py` | The 78 fixed-ruler anchor database                         |
| `analyze_velocity_profile.py`          | Flat/rising/Keplerian census                               |
| `analyze_flat_vs_rising.py`            | Scale-separation audit                                     |
| `substrate_response_test.py`           | Universal response fit (the open door)                     |
| `residual_error_audit.py`              | Error-bar audit + raw model-free slope                     |
| `src_distance.py`                      | SRC aether-damping distance model                          |
| `archive/falsified_tests/`             | Mechanisms tested and killed — kept as the audit trail     |
| `archive/toy_sims/`                    | Process/demographic generators (labeled as such, honestly) |
| `LEDGER.md`                            | Every mechanism, every test, every verdict                 |

## Honest status

This framework does NOT claim a solved rotation curve. What it owns:

- A clean telemetry foundation (78 geometric anchors).
- Nine mechanisms honestly tested and falsified — including by our
  own uncheated engine, which re-derives the dark matter problem from
  first principles rather than hiding it.
- Two measurements that survive: the universal response scale and the
  0.575 raw slope.
- A defined frontier: close the coupled force budget
  (`−∂P/∂r + J×B + drag + viscosity = ρv²/r`) from measured medium
  parameters, or falsify the route.

## Data sources

SPARC mass models (Lelli, McGaugh, Schombert) — raw files included,
unmodified. Distance anchors filtered to geometric methods only.

## License & use

See repo root. Scripts are plain Python 3 + NumPy. Run any test:
read its printed falsification conditions first — that is the whole
point.
