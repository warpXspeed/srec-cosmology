"""
srec.py -- SRC master launcher.
  python3 srec.py                 -> status + self-test (default)
  python3 srec.py --mode solar    -> solar furnace power audit
  python3 srec.py --mode catastrophe -> 12.85 ka cycle clock
  python3 srec.py --mode full     -> all closures demonstrated
"""
import argparse
import time
import core as src

BANNER = "=" * 62

def self_test():
    print(BANNER); print("SRC CORE SELF-TEST (Rev 3)"); print(BANNER)
    t_now = src.T_H
    print(f"phi(now)            = {src.phi(t_now):.6f}")
    print(f"G_eff(now)          = {src.G_eff(t_now):.6e}  (G_today = {src.G_today:.6e})")
    print(f"alpha_eff(now)      = {src.alpha_eff(t_now):.8f}")

    # High-acceleration limit: Earth's orbit must be Newtonian
    r_e   = 1.496e11
    g     = src.g_effective(src.M_sun, r_e)
    g_N   = src.G_today * src.M_sun / r_e**2
    print(f"\ng_eff @ Earth orbit = {g:.6e} m/s^2   Newtonian: {g_N:.6e}")
    print(f"mu(g)              = {src.mu_interpolation(g):.8f}  (must be ~1.0)")

    # Low-acceleration limit: galactic flat curve + BTFR
    M_MW  = 6.0e10 * 1.989e30
    r_out = 8.0e20   # ~26 kpc
    v     = src.v_orbital(M_MW, r_out)
    print(f"\nv_flat (MW, M_b=6e10 Msun) = {v/1e3:.1f} km/s  (observed ~220 km/s)")
    print(f"BTFR check: v^4 = {v**4:.3e}  vs  G*M_b*a_c = {src.G_today*M_MW*src.a_c:.3e}")
    print(BANNER)

def solar_mode():
    print(BANNER); print("SOLAR FURNACE MODE"); print(BANNER)
    P, I, dV = src.solar_power()
    err = (P - src.L_sun_obs) / src.L_sun_obs * 100
    print(f"I_sun     = {I:.3e} A")
    print(f"dV_helio  = {dV:.3e} V")
    print(f"P_sun     = {P:.3e} W")
    print(f"L_sun obs = {src.L_sun_obs:.3e} W   -> deviation: {err:+.2f}%")
    print("Mechanism: Sun = inductive plasma load in the Galactic Current Sheet.")
    print(BANNER)

def catastrophe_mode():
    print(BANNER); print("CATASTROPHE MODE -- 12.85 ka SAFETY-VALVE CLOCK"); print(BANNER)
    t_now_yr = time.localtime().tm_year + 2000 - 0  # years since YD datum (approx)
    print(f"Cycle period        = {src.YD_PERIOD:.0f} yr")
    print(f"Years since datum   = ~{t_now_yr:.0f}")
    phase = t_now_yr % src.YD_PERIOD
    to_next = src.YD_PERIOD - phase
    print(f"Current phase       = {phase:.0f} yr into cycle")
    print(f"Years to next pulse = {to_next:.0f} yr")
    print(f"Kick amplitude now  = {src.cme_kick(float(t_now_yr)):.6f} (baseline hum)")
    print("Valve states: trickle -> solar cycles -> GCS major vent -> reset.")
    print(BANNER)

def full_mode():
    self_test(); solar_mode(); catastrophe_mode()
    print("FULL LIFECYCLE: storage (gravity locks in) -> pinch/tension loop")
    print("-> spall (photons/electrons/CMEs) -> tension drop -> stable loop.")
    print("Machine status: HUMMING.")

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Scalar Relaxation Cosmology engine")
    p.add_argument("--mode", choices=["solar", "catastrophe", "full", "test"],
                   default="test", help="execution mode (default: self-test)")
    args = p.parse_args()

    if args.mode == "solar":        solar_mode()
    elif args.mode == "catastrophe": catastrophe_mode()
    elif args.mode == "full":      full_mode()
    else:                          self_test()

