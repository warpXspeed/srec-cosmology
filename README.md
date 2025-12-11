# SREC — Scalar Relaxation Eddy Cosmology

**One tiny scalar field. Two tiny numbers. The entire universe.**

A single rolling scalar field φ changes only two things:
- Gravity slowly gets stronger (β_g ≈ -4.8 × 10⁻⁶)
- Electromagnetism slowly gets weaker (β_γ ≈ +5.5 × 10⁻⁷)

These two changes explain:
- galaxies without dark matter
- planets and moons forming from plasma eddies (not random rocks)
- the real 12.85 ka Younger Dryas catastrophe
- the Hallstatt cycle that collapsed Bronze-Age civilisations
- the final Oort-cloud collapse that will feed a dying Sun
- the risk of a nova explosion when the feeding gets too strong

### Three completely separate modes — you choose how deep you want to go

| Mode | What it shows | Command |
|------|----------------|---------|
| **solar** | Pure solar-system formation only (planets, moons, Oort cloud) | `./srec.py --mode solar` |
| **catastrophe** | Only the 12.85 ka + Hallstatt reset cycles | `./srec.py --mode catastrophe` |
| **full** | Full lifecycle from Big Bang to stellar death | `./srec.py --mode full` |

### Quick start (on any Linux / macOS / Windows)

```bash
git clone https://github.com/ghenton/srec.git
cd srec
./srec.py --mode solar          # planets forming from eddies
./srec.py --mode catastrophe   # Younger Dryas + Hallstatt events
./srec.py --mode full           # the entire cosmic clock
