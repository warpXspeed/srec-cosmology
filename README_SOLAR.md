
### 2. `README_SOLAR.md` (detailed explanation of the solar-system plot)

```markdown
# SREC Mode 1 — Solar-System Builder
## What the red curve actually shows

| X-axis (Myr) | Real meaning |
|------------|----------------|
| 0 Myr      | Disk has just formed — almost no structure |
| 1–2 Myr   | Rocky planets (Mercury → Mars) condense |
| 2–4 Myr   | Jupiter & Saturn grow to final size |
| 4–6 Myr   | Moons finish forming, Oort cloud is ejected |

| Y-axis (log scale) | Physical meaning |
|------------------|------------------|
| 10⁻⁶ (start) → 10⁰ | Tiny turbulence → full-sized planets |
| >10¹ | Giant eddies → gas giants + rich moon systems |

The curve going up = the solar system being born in real time.

### Try these experiments
```bash
# Chaotic universe — many small planets, maybe no gas giants
# → edit modes/solar_system.py → change chaos=0.5 and run again

# No electromagnetism weakening (beta_gamma=0) → one super-Jupiter
# → set beta_gamma=0.0 in core.py and run again
