# Harmonic Octave Map

An interactive, single-file map of the 118 chemical elements arranged in atomic-number
order along one continuous logarithmic coil, with octave rings drawn at the noble-gas
closure radii.

Hydrogen sits at the exact centre. The coil unwinds outward, placing Z = 1 → 118 in
strict sequence. Dashed rings appear only where a noble gas falls, so ring spacing is an
**output** of the closure positions rather than a hand-set grid.

No build step, no dependencies, no network calls. Open the HTML file in a browser.

---

## Quick start

1. Download `harmonic_octave_map.html`
2. Open it in any modern browser (Chrome, Firefox, Safari, Edge)
3. Drag to pan, use the Zoom slider to read the core
4. **Click any element** for its full dossier
5. `←` / `→` step through the sequence, `Esc` closes the dossier

To export a poster: set **Zoom** back to ×1, then browser print → **Save as PDF**.
Enable **Background graphics** in the print dialog, or the dark field drops out and the
label halos go with it. Output is real vector, so it stays sharp at any size.

---

## The geometry

### Radius law

Each element `z` is placed at r(z) = R_out · (q^(z−1) − 1) / (q^117 − 1)

with `R_out = 430` and `q` adjustable between 1.000 and 1.030 (default 1.010).

The `−1` terms are what put hydrogen at `r(1) = 0` exactly. Without them the first element
sits at a small radius rather than at the origin. The law stays geometric and strictly
monotonic in `z` at every slider setting; the status line reports the monotonic check on
every render, so a second spiral or an out-of-order node is structurally impossible.

### Angular law

θ(z) = −π/2 + (z − 1) · Δθ, Δθ = (turns · 2π) / 118

Constant angular step, so the coil has uniform turn density and the radius does all the
expansion work.

### Octave rings

A dashed circle is drawn at `r(C_k)` for each closure element `C_k ∈ {2, 10, 18, 36, 54,
86, 118}` and nowhere else. The ring radii therefore widen outward automatically, because
the outer octaves contain more element shells (2, 8, 8, 18, 18, 32, 32). The table under
the map prints the seven radii and the gaps between them.

### Node classification

Every element's class is derived from its **sequence distance to the nearest closure**,
not assigned:

| Position relative to a closure | Class                  | Colour      |
| ------------------------------ | ---------------------- | ----------- |
| Is a closure                   | Harmonic zero          | gold        |
| 1 step past                    | Primary shedder [+1]   | blue        |
| 2 steps past                   | Secondary shedder [+2] | light blue  |
| 1 step before                  | High aether sink [−1]  | red         |
| 2 steps before                 | Sink [−2]              | salmon      |
| 3 steps before                 | Sink [−3]              | pale salmon |
| otherwise (mid-octave)         | Structural hub [0]     | grey        |
| Z = 1                          | Seed / core            | gold        |

This reproduces the standard group behaviour without a lookup table: alkalis are one step
past a closure, alkaline earths two, halogens one step before, chalcogens two, pnictogens
three, noble gases are the closures themselves.

---

## Features

- **Click any node** for a dossier: mass, category, group, period, block, electron
  configuration, shell occupancy, node class, octave, ring radius, and sequence distance
  to the bracketing closures
- **Zoom to** button frames any selected element at a readable scale
- **Label level-of-detail**: a node is labelled only when its angular arc exceeds a
  screen-constant threshold, so zooming reveals more labels instead of enlarging them.
  The status line reports `n shown / n held for zoom`, so nothing disappears silently
- **Full index** toggle: a 118-element grid, also clickable, for symbols too crowded to
  label on the coil
- **Pan and zoom** with pointer drag; all marks sized as fractions of the viewBox so they
  stay constant on screen at any magnification

---

## Data provenance

**Conventional atomic data** (mass, category, group, period, block, configuration,
shells) is standard reference data.

- Masses below Z = 84 are standard atomic weights (IUPAC). Above Z = 84 they are mass
  numbers of the most stable known isotope, and the dossier says so.
- Electron configurations are aufbau with the standard exceptions applied (Cr, Cu, Nb, Mo,
  Ru, Rh, Pd, Ag, La, Ce, Gd, Pt, Au, Ac, Th, Pa, U, Np, Cm).
- Configurations **beyond about Z = 103 are predictive**, not measured. Elements from
  Z = 104 are marked "(predicted)" in the dossier category line.
- Categories for the superheavy elements follow conventional prediction and are the least
  certain field in the dataset.

**The map geometry and node classification** are an interpretive framework, not standard
physics. See `METHOD.md`. Nothing in this repo is fetched at runtime; the file is
self-contained and works offline.

---

## Known limitations

- **Core crowding.** Z = 1–18 occupies a small fraction of the outer radius. At ×1 zoom
  the innermost labels are suppressed. Use the zoom slider or **Centre on H** (×18).
- **Label density.** Roughly 118 labels cannot coexist at ×1. The LOD rule handles this
  by design; the status line tells you how many are held back.
- **Predictive data past Z = 103**, as noted above.
- **The expansion factor `q` is a display parameter.** The slider changes how the coil
  looks, not what the classification says. Changing `q` does not move any element's class.

---

## Files

harmonic_octave_map.html interactive map, single file, no dependencies

METHOD.md the geometric method and its scope

README.md this file
