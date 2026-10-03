# Technical Specification (Revision 2.0): Resolving Substrate Dynamics & Field Closure
**Framework:** Scalar Relaxation Cosmology (SRC)  
**Document Purpose:** Correcting internal mathematical gaps identified in the initial specification, specifically regarding galactic rotation curves, photon masslessness, and parameter parsimony.

---

## 1. Correcting Galactic Rotation: From Constant Density to Dynamic Field Gradients

### The Failure of Constant $\rho_s$
As demonstrated by internal stress-testing, assuming a static, constant background density ($\rho_s = \text{const}$) in Poisson's equation ($\nabla^2 \Phi = 4\pi G (\rho_b + \rho_s)$) yields a solid-body rotation curve ($v \propto r$), which contradicts flat galactic rotation curves ($v = \text{const}$). To achieve flatness at the outskirts, the effective substrate density profile must explicitly scale as:
$$\rho_s(r) \propto r^{-2}$$

### The SRC Correction: The Relaxation Field ($\phi$)
SRC does not treat the aether as a passive, uniform gas at all scales. Instead, the background density is governed by the gradient of the scalar relaxation field $\phi$:
* **The Governing Gradient:** In low-acceleration regimes ($a < a_c \approx 1.2 \times 10^{-10} \text{ m/s}^2$), the scalar field $\phi$ relaxes such that its energy density distribution naturally forms an $r^{-2}$ profile.
* **The Field Equation:** We replace the static $\rho_0$ assumption with a dynamic coupling between baryonic mass injection and scalar field relaxation:
  $$\nabla^2 \phi - \frac{1}{c^2}\ddot{\phi} = \beta \rho_{\text{baryon}}$$
  Where the effective substrate density $\rho_s(\phi) \equiv |\nabla \phi|^2$ self-organizes into the required $r^{-2}$ geometry at galactic boundaries without invoking unobserved WIMPs or ad-hoc dark matter halos.

---

## 2. The Photon as a Goldstone Boson (Solving Mass and Polarization)

### The Failure of Arbitrary Potentials
Attempting to bind a neutrino and antineutrino via an ad-hoc potential $V(r) = -\frac{\alpha}{r}e^{-\mu r} + kr^2$ introduces arbitrary free parameters (ghosts) and fails to naturally eliminate the unwanted longitudinal (helicity-0) polarization mode or guarantee exact masslessness ($m_\gamma = 0$).

### The SRC Correction: Collective Excitations in the Condensate
The photon is not formed by "gluing" two discrete fermions together with an arbitrary spring; it is an **emergent collective excitation (Goldstone mode)** of the $\nu-\bar{\nu}$ Bose-Einstein Condensate (BEC):
* **Exact Masslessness ($m_\gamma = 0$):** Spontaneous U(1) phase symmetry breaking in the macroscopic condensate wave function ($\Psi = \sqrt{\rho}e^{i\theta}$) natively generates massless Goldstone bosons. 
* **Transverse Polarization:** By Goldstone's theorem, phase fluctuations in the superfluid lattice propagate exclusively as transverse shear waves. The longitudinal mode is suppressed by the high bulk modulus of the condensate. Thus, the photon naturally possesses only $\pm 1$ helicity modes without manual constraints.

---

## 3. Parameter Parsimony (Eliminating Free Constants)

To satisfy the framework's core anti-ghost rule—*a theory must not trade unobserved particles for unmeasured continuous constants*—all micro-mechanical parameters must be derived directly from the fundamental properties of the condensate:
1. **Condensate Density ($n_0$):** The baseline ground-state number density of paired $\nu-\bar{\nu}$ components.
2. **Sparsity/Scattering Length ($a_s$):** The interaction length scale of the condensate.
3. **Effective Mass ($M$):** The invariant mass of the paired state.

All coupling strengths, photon frequencies, and topological charge units ($e$) must be calculated as functions of $(n_0, a_s, M)$, eliminating curve-fitting constants from the foundational equations.

---

## 4. Summary for Repository Integration

The SRC Technical Manual is updated with the following axioms:
* **Axiom A (Gravity):** Galactic rotation curves are shaped by the dynamic $r^{-2}$ relaxation gradient of the $\phi$-field ($\rho_s = |\nabla \phi|^2$), eliminating Dark Matter entirely.
* **Axiom B (Light):** Photons are transverse Goldstone modes (acoustic shear waves) of the $\nu-\bar{\nu}$ superfluid condensate, guaranteeing strict masslessness and two helicity states by symmetry.
* **Axiom C (Parsimony):** All dynamic parameters must reduce to fundamental condensate variables ($n_0, a_s, M$).

