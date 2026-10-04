# SREC — Scalar Relaxation Eddy Cosmology

SREC is a developing physics framework and simulation project. This repository collects its working code, model proposals, analyses, and open technical questions.

The repository began as a scratchpad. Its files are being organized into a clearer structure, so some documentation and links may change as that work continues.

## Project status

The ideas in this repository are **proposals and working hypotheses**, not established findings. A simulation or a numerical match is not, by itself, evidence that the underlying physical explanation is correct.

The project aims to make its assumptions, equations, code, and unresolved questions easier to inspect. In particular, documentation should distinguish between:
- assumptions or proposed mechanisms;
- results calculated by the current code;
- comparisons with observations; and
- questions that remain unresolved.

## Repository map

- [`core.py`](./core.py) — shared constants and scalar-field functions.
- [`srec.py`](./srec.py) — command-line launcher for the simulation modes in `modes/`.
- [`modes/`](./modes/) — mode-specific simulation code.
- [`neutrinos/`](./neutrinos/) — neutrino-substrate and solar-furnace model documents.
- [`periodic/`](./periodic/) — periodic and reaction-engine materials.
- [`planetary/`](./planetary/) — planetary and solar-system materials.
- [`magnetism/`](./magnetism/) — magnetism-related materials.
- [`docs/Why the Sun Has Not Burnt Out.md`](./docs/Why%20the%20Sun%20Has%20Not%20Burnt%20Out.md) — the SRC proposal for an externally powered solar model.
- [`analysis/Solar-Galactic-event.md`](./analysis/Solar-Galactic-event.md) — an SRC interpretation of a proposed solar–galactic event.

### Related theory documents

- [Solar Furnace Model](./neutrinos/THEORY_SOLAR_FURNACE.md) — the proposed gravity–current–plasma model and its stated power calculation.
- [Neutrino Substrate Framework](./neutrinos/neutrino-substrate-framework.md) — overview of the proposed substrate model.

## Running the simulator

The launcher accepts these modes:

```bash
python3 srec.py --mode solar
python3 srec.py --mode catastrophe
python3 srec.py --mode full
