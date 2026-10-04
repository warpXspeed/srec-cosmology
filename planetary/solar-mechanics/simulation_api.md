# Simulation API & Implementation

The `src/` directory uses a three-stage pipeline to validate the "No-Ghost" model:

1.  **`venus_moon_engine.py`**: Integrates gravitational N-body physics with a Pompeii escalation surge module.
    *   *Output:* Ejection trajectory (eccentricity, breach day).
2.  **`heliocentric_transfer.py`**: Evaluates binding conditions.
    *   *Calculation:* $\Delta E_{\text{capture}} \le E_{\text{KP12\_MAX}}$ ($10^{29} \text{ J}$).
3.  **`kp12_event_simulator.py`**: Executes the dielectric breakdown logic.
    *   *Condition:* If compressed_radius <= 1.0 (Earth Standoff):
        *   `dielectric_puncture = True`
        *   `megafauna_kill_rate_pct = 0.82`
        *   `geomorphology_mode = "PLASMA_EDM_TRENCHING"`

