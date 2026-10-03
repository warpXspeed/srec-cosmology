===========================================================================
 SRC RECURSIVE REACTION ENGINE v0.5
===========================================================================

### The CO vs CO2 question

--- C + O ---
    assembly centers on C (4 open boundary positions)
  C + O -> CO   [COVALENT LOCK]  dTau=-2.078  E~249  open slots=2
  CO + O -> CO₂   [COVALENT LOCK]  dTau=-2.104  E~252  open slots=0
  SATURATION: CO₂ — boundary fully engaged, geometric rest.
  Product: CO₂   Total released: ~502 scale units

### Recursive saturation: methane

--- C + H ---
    assembly centers on C (4 open boundary positions)
  C + H -> CH   [COVALENT LOCK]  dTau=-1.350  E~162  open slots=3
  CH + H -> CH₂   [COVALENT LOCK]  dTau=-1.277  E~153  open slots=2
  CH₂ + H -> CH₃   [COVALENT LOCK]  dTau=-1.466  E~176  open slots=1
  CH₃ + H -> CH₄   [COVALENT LOCK]  dTau=-1.280  E~154  open slots=0
  SATURATION: CH₄ — boundary fully engaged, geometric rest.
  Product: CH₄   Total released: ~645 scale units

### Water

--- O + H ---
    assembly centers on O (2 open boundary positions)
  O + H -> OH   [COVALENT LOCK]  dTau=-1.847  E~222  open slots=1
  OH + H -> OH₂   [COVALENT LOCK]  dTau=-1.905  E~229  open slots=0
  SATURATION: OH₂ — boundary fully engaged, geometric rest.
  Product: OH₂   Total released: ~450 scale units

### Ammonia

--- N + H ---
    assembly centers on N (3 open boundary positions)
  N + H -> NH   [COVALENT LOCK]  dTau=-1.509  E~181  open slots=2
  NH + H -> NH₂   [COVALENT LOCK]  dTau=-1.547  E~186  open slots=1
  NH₂ + H -> NH₃   [COVALENT LOCK]  dTau=-1.694  E~203  open slots=0
  SATURATION: NH₃ — boundary fully engaged, geometric rest.
  Product: NH₃   Total released: ~570 scale units

### Salts and oxides

--- Na + Cl ---
    assembly centers on Na (1 open boundary positions)
  Na + Cl -> NaCl   [IONIC SNAP]  dTau=-6.290  E~755  open slots=0
  SATURATION: NaCl — boundary fully engaged, geometric rest.
  Product: NaCl   Total released: ~755 scale units

--- Mg + O ---
    assembly centers on Mg (2 open boundary positions)
  Mg + O -> MgO   [IONIC SNAP]  dTau=-4.745  E~569  open slots=0
  SATURATION: MgO — boundary fully engaged, geometric rest.
  Product: MgO   Total released: ~569 scale units

--- Mg + Cl ---
    assembly centers on Mg (2 open boundary positions)
  Mg + Cl -> MgCl   [IONIC SNAP]  dTau=-5.950  E~714  open slots=1
  MgCl + Cl -> MgCl₂   [COVALENT LOCK]  dTau=-2.447  E~294  open slots=0
  SATURATION: MgCl₂ — boundary fully engaged, geometric rest.
  Product: MgCl₂   Total released: ~1008 scale units

--- Al + Cl ---
    assembly centers on Al (3 open boundary positions)
  Al + Cl -> AlCl   [IONIC SNAP]  dTau=-3.723  E~447  open slots=2
  AlCl + Cl -> AlCl₂   [COVALENT LOCK]  dTau=-2.384  E~286  open slots=1
  AlCl₂ + Cl -> AlCl₃   [COVALENT LOCK]  dTau=-2.620  E~314  open slots=0
  SATURATION: AlCl₃ — boundary fully engaged, geometric rest.
  Product: AlCl₃   Total released: ~1047 scale units

### Lattice formers

--- Si + O ---
    assembly centers on Si (4 open boundary positions)
  Si + O -> SiO   [COVALENT LOCK]  dTau=-2.400  E~288  open slots=2
  SiO + O -> SiO₂   [COVALENT LOCK]  dTau=-1.787  E~214  open slots=0
  SATURATION: SiO₂ — boundary fully engaged, geometric rest.
  Product: SiO₂   Total released: ~502 scale units

--- C + Cl ---
    assembly centers on C (4 open boundary positions)
  C + Cl -> CCl   [IONIC SNAP]  dTau=-3.231  E~388  open slots=3
  CCl + Cl -> CCl₂   [COVALENT LOCK]  dTau=-2.621  E~315  open slots=2
  CCl₂ + Cl -> CCl₃   [COVALENT LOCK]  dTau=-2.377  E~285  open slots=1
  CCl₃ + Cl -> CCl₄   [COVALENT LOCK]  dTau=-2.430  E~292  open slots=0
  SATURATION: CCl₄ — boundary fully engaged, geometric rest.
  Product: CCl₄   Total released: ~1279 scale units

### Noble rejection

--- H + He ---
    assembly centers on H (1 open boundary positions)
  STOP: BOUNCE (harmonic zero)
  Product: H   Total released: ~0 scale units

--- Na + Ar ---
    assembly centers on Na (1 open boundary positions)
  STOP: BOUNCE (harmonic zero)
  Product: Na   Total released: ~0 scale units
(base) merlin@localhost:~/periodic> 
