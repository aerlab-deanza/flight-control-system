
"""
Simulated sensor models.
 
Each class takes the true plant state and returns a noisy measurement,
mimicking real hardware behaviour so the controller must work with imperfect data.
 
Classes
-------
IMU
    6-axis inertial measurement unit (accelerometer + rate gyroscope).
    .measure(accel_body, omega_body) -> (accel_meas, omega_meas)
    Adds fixed bias vector + zero-mean Gaussian noise to each axis.
    Noise params: accel_noise [m/s²], gyro_noise [rad/s] from SensorConfig.
 
Barometer
    Altitude sensor (pressure → height).
    .measure(alt_true) -> float
    Adds Gaussian noise (σ ≈ 0.06 m).  No bias (resets on power cycle in reality).
 
GPS
    Position + velocity fix at fixed update rate (default 5 Hz).
    .measure(pos, vel, t) -> Optional[(pos_meas, vel_meas)]
    Returns None on steps where no new fix is available.
    Horizontal noise σ ≈ 0.25 m, velocity noise σ ≈ 0.04 m/s.
 
WindModel
    Three-axis Dryden-inspired turbulence.
    .step(dt) -> wind_vector [m/s]
    State: first-order Gauss-Markov process driven by white noise:
        τ · dw/dt = w_target − w,   w_target ~ N(mean, σ)
    Occasional gusts injected stochastically at ~5% probability per second.
"""
 