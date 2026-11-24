# rwp/src Atomic Program — file index

A record of the atomic-structure program: what each artifact was, what it established,
and why it was superseded. Put this at `~/Projects/active/srec-cosmology/atoms/README.md`.

Layout:

```
atoms/
  README.md      this file
  current/       the artifacts worth using
  archive/       superseded benches, kept for the record
  notes/         external audit + earlier Python tooling
```

---

## Current — use these

| file | what it is | status |
|---|---|---|
| `current/rwp-src-atomic-console-release-1-2-1.html` | The release console. All eight sequence fits, derivation chain with substituted arithmetic, four competing-mechanism tests, five held-out spectral cycles, disclosed grading windows, live handler validation, banked constants with ESTABLISHED/DERIVED/PROVISIONAL/WITHDRAWN labels, worklist, caveats, and the built-in cross-test with a locked official score. | **final artifact** — validated: self-test green, handler validation 6/6 |
| `current/cross-test-v4.html` | Replication instrument. Computes its own reference from the shipped data pack at load; blind first grade; sealed reveal; official score locked on first non-empty submission. | built, **not yet run** |
| `current/atomic-shape-lab-drag-the-orbitals-match.html` | Student-facing shape lab. Start from a measured D-line, drag two effective charges, watch the orbital shapes and the predicted wavelength move together. Includes the family shape table carrying the lithium anomaly. | current; verify it is the fixed copy (see bottom) |

## Notes

| file | what it is |
|---|---|
| `notes/Debug App Logic and Code - Grok.html` | external audit of the cross-test bench. Found the false universality claim, the one-sided residual window, and the incomplete self-test. All three were real and were fixed. |
| `notes/composition_chain.py` | earlier Python tooling |
| `notes/src_probes.py` | earlier Python tooling |

---

## Archive — lineage, oldest to newest

### Generation 1: the ring/spectrum simulator

| file | what it did | outcome |
|---|---|---|
| `ring-state-spectrum-simulator-rwp-src.html` | first simulator: ring populations → predicted lines | **circular.** Fitting N ring rates to a series with N lines proves nothing. Retired for that reason. |
| `ring-state-spectrum-simulator-rwp-src (1).html` | duplicate browser download | redundant |
| `ring-state-spectrum-simulator-v2.html` | rebuild with visible error banner and self-test | established the H-alpha constant check (656.2883 nm air vs published 656.281) |
| `residual-pattern-analyzer-v3-rwp-src.html` | instrument-zero / worklist analyzer | caught the circular "Rydberg model vs Rydberg references" comparison and the inverted branch labels |

### Generation 2: isoelectronic sequences — the substance

| file | what it did | outcome |
|---|---|---|
| `ring-law-matrix-isoelectronic-sequences.html` | four sequences, structure fixed, Z moving | the two compact laws: A ≈ 0.257·(Z−1)/N and ΔZ² ≈ 0.44·(Z−1)/N, both with exponent exactly 1 |
| `two-layer-screening-test-be-like-sequenc.html` | Be-like sequence, pre-registered two-layer prediction | produced the flawed 0.718 prediction, then the 0.542 subshell result — before the C²⁺ data correction |
| `closure-test-two-screening-constants-clo.html` | first closure attempt | contained a wrong B-like self-test expectation (2.6571) and bad hand arithmetic; superseded |
| `closure-test-v2-corrected-b-like-and-two.html` | corrected | B-like σ = 3.4381; open-ring excess +0.387; the 1/(Z−1)² form (later retracted) |
| `global-ring-screening-bench-eight-sequen.html` | eight sequences, one form, two constants | X_inner 0.7914 vs X_2p 0.7829 (1.1% apart). **Mg-like table was corrupted** (duplicate Z=12, wrong rows) |
| `ring-layer-partner-screen-corrected-data.html` | corrected Mg-like; fixed-Z partner increments | the cleanest measurement in the set: at Z=10 a 2p partner costs 0.7218, an s partner 0.5778 — 25% penetrating-s effect, no free parameters |
| `ring-relationship-decomposition-correcte.html` | eight-sequence decomposition with held-out Ne-like | **the held-out residual +0.1636**; also the data revision log (seven corrections) |
| `al-like-bench-open-ring-excess-one-shell.html` | Al-like sequence, form contest | form B 1/(Z−a) won decisively (RMS 0.0035 vs 0.0302); one copy contains an `ev is not defined` scoping bug |
| `al-like-bench-open-ring-excess-one-shell (1).html` | duplicate download | redundant |

### Generation 3: spectral return

| file | what it did | outcome |
|---|---|---|
| `spectral-return-bench-from-ring-constant.html` | held-out alkali D-line cycles from the binding constants | median predictor: Na −2.8, K +7.8, Cs −4.8 nm (good); **Li +202 nm and Rb −34 nm fail** — the measured size and shape of the missing structure |

### Generation 4: cross-test

| file | what it did | outcome |
|---|---|---|
| `cross-test-bench-independent-replication.html` | v1 grader, typed windows | graded numbers but could not check the derivation chain |
| `cross-test-bench-v2-self-computing-repli.html` | reference computed from the data at load | fixed the typed-window weakness; still hard-coded the universality answer |
| `cross-test-bench-v3-self-computing-repli.html` | computed universality, two-sided residual window, expanded self-test | correct honest answer is "no" (Mg-like RMS 0.01830) |
| `cross-test-v4.html` | protocol hardening | blind first grade, sealed reveal, locked official score. **Now in `current/`** |

### Generation 5: console

| file | what it did | outcome |
|---|---|---|
| `rwp-src-atomic-console-release-1-0.html` | first release | correct constants, but not auditable |
| `rwp-src-atomic-console-release-1-1-audit.html` | added all fits, arithmetic, live tests, windows, validation | **contains two known bugs**: the circular additivity row (p4 compared to itself) and a load-order crash (`TOL` used before declaration) |
| `rwp-src-atomic-console-release-1-2-1.html` | final | fixes both; adds the coherence double-confirmation. **Now in `current/`** |

---

## Erratum trail

Every correction the process caught, including the ones the assistant introduced.

| # | error | caught by |
|---|---|---|
| 1 | Ar⁷⁺ carried as 143.66 in one table and 143.46 in another (0.2 eV) | automated same-ion hygiene check |
| 2 | C²⁺ ionization typed 46.2020 instead of 47.8878 — produced a −0.050 outlier and a false asymptote | refit after the outlier was traced |
| 3 | Mg-like table contained Na-like rows with an extra Mg — duplicate Z=12, seven of eight rows wrong (RMS 0.227 vs 0.003 elsewhere) | RMS anomaly + integrity check |
| 4 | Hand-computed B-like sequence "declined to zero" — was bad arithmetic; real values are smooth 3.438→3.186 | the app's own table contradicted the prose |
| 5 | "Additivity falsified" demonstrated by comparing p4 to an algebraic identity of itself | re-derivation of the chain |
| 6 | Direction label inverted: v2 grading demanded "s" when the p partner screens more | external audit |
| 7 | Parser positional fallback consumed label-matched lines, masking two missing fields (would have produced false PASSes) | live handler validation panel |
| 8 | `TOL` declared after the panel that used it — console 1.2 crashed at load | browser error report |
| 9 | Self-test `META` table omitted `3p` while the pair list included it — `undefined[0]` crash | browser error report |
| 10 | "Exponent-2 open-ring law" — was a form artifact; the shifted form fits every sequence | form contest on all eight |
| 11 | X(3s) = 0.337 — withdrawn, product of the contaminated Mg-like fit | corrected refit |

---

## What the program established

**Measured, from raw ionization energies:**

| quantity | value | label |
|---|---|---|
| inner partner screening (1s) | 0.7914 | ESTABLISHED — cross-checked to 0.12% |
| inner partner screening (2p) | 0.7924 | ESTABLISHED — cross-checked to 0.12% |
| penetrating 2s partner (inner) | 0.7483 | DERIVED |
| same-ring 2s partner | 0.5548 | DERIVED |
| same-ring 2p partner (open shell) | 0.6728 | DERIVED |
| same-ring 2p partner (filled shell) | 0.7055 | DERIVED |
| filled-ring coherence | +0.1636 | DERIVED — double-confirmed (5 × 0.0327) |
| half-filled exchange (into ⁴S) | +0.230 / +0.246 | PROVISIONAL — pending NIST |
| a(3s \| same ring) | ~0.331 | PROVISIONAL — Mg-like RMS 0.0183 |
| X(3s) = 0.337 | — | WITHDRAWN |

**Structural findings:**

- One form, σ = σ₀ + c/(Z−a), fits 7 of 8 sequences at the data floor. Universality verdict: **no** (Mg-like is the exception).
- The doublet split couples to **unscreened** Z: ζ spread 1135× if screened, 2.5× if not. The split is a core-layer effect.
- The same 2p partner costs more in a **filled** shell than an open one, by +0.0327 per partner — and that excess sums exactly to the held-out residual.
- Ring-level residuals appear only at special subshell occupancies and have no single-electron analogue. **Configuration-level, not single-particle.**
- Spectral transfer is partial: 3 of 5 alkali D-lines predicted within 8 nm; Li (+202) and Rb (−34) fail.

## Caveats that stay with the model

1. **Proxy insensitivity.** σ = Z − Z_eff is a linearized accounting. The 1s/2p agreement at 0.12% may reflect the proxy being unable to distinguish them, not a law.
2. **Residual ambiguity.** The +0.1636 is double-confirmed as a *quantity*; its *meaning* (collective coherence vs proxy failure at complete subshells) only the spectral channel can settle.
3. **Reproducibility is not correctness.** Any replication shares the published values and the inversion. NIST remains the authority.
4. **The ring label is interpretation, not result.** The data require a collective explanation; they do not derive ring energies or resonance conditions.

## Open items

- NIST-verify Mg-like heavy members (S⁴⁺, Cl⁵⁺, Ar⁶⁺) — would firm a(3s|same)
- NIST-verify the N, O, Ne, Ar cascades — would bank the half-filled exchange magnitude
- The ζ (doublet-split) law — data-starved; four reliable points, no working two-parameter form
- Strength channel — radial-overlap oscillator strengths not yet tested against measured values
- Blind cross-test against another system — instrument ready in `current/cross-test-v4.html`
- Derive the ring formalism, or drop the ring label

---

