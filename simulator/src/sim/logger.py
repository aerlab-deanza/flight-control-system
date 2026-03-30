"""
Telemetry logger.
 
Captures simulation state at a fixed downsampled rate (default 50 Hz from
200 Hz physics) and exposes the data as numpy arrays for post-processing.
 
Logged channels (one value per sample):
    t                   — simulation time  [s]
    x, y, z             — true position    [m]
    vx, vy, vz          — true velocity    [m/s]
    roll, pitch, yaw    — true Euler angles [deg]
    est_roll/pitch/yaw  — Mahony estimate   [deg]
    p, q, r             — true angular rates [rad/s]
    wind_x/y/z          — wind vector       [m/s]
    target_x/y/z        — current waypoint  [m]
    rpms[4]             — motor RPM commands
 
Public API:
    Logger()
    .record(t, state, euler_true, euler_est, wind, target, rpms)
        — append one sample; call every log_every physics steps.
    .arrays() -> dict[str, ndarray]
        — return all channels as numpy arrays for analysis / plotting.
    .to_csv(path)          — write telemetry to CSV for external tools.
    .reset()               — clear all stored data.
"""