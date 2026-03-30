"""
Cascade PID flight controller.
 
Five nested control loops (outer → inner):
    1. Altitude   PID : z error         → vertical velocity setpoint.
    2. Velocity Z PID : vz error        → throttle correction (ΔRPM).
    3. Position XY PID: xy error        → desired velocity in world frame.
    4. Velocity XY PID: vxy error       → desired tilt angles (roll_sp, pitch_sp).
    5. Attitude   PID : roll/pitch/yaw  → per-axis RPM deltas.
 
Motor mixing  (+ config):
    M0 = T + pitch_out − yaw_out
    M1 = T − roll_out  + yaw_out
    M2 = T − pitch_out − yaw_out
    M3 = T + roll_out  + yaw_out
    where T = hover_rpm + throttle_correction.
 
Public API:
    FlightController(vcfg, ccfg)
    .set_target(pos: ndarray, yaw: float)  — update position + heading setpoint.
    .compute(pos, vel, euler, dt) -> ndarray[4]  — return RPM commands.
    .reset()                               — zero all integrators.
 
Design notes:
    - Outer loop bandwidth < inner loop bandwidth (position gains << attitude gains).
    - Anti-windup: integral clamped so ki·I never exceeds output saturation limit.
    - Yaw controlled independently; does not couple into position loop.
    - max_tilt (rad) clips roll_sp / pitch_sp to prevent aggressive flips.
    - hover_rpm = sqrt(mass·g / (4·kT))  used as throttle baseline.
"""