"""
State estimation filters.
 
Classes
-------
MahonyFilter
    Explicit complementary filter on SO(3).
    Fuses gyroscope (high-rate, drifts) with accelerometer (noisy, drift-free).
    Algorithm:
        1. Normalise accelerometer reading → estimated gravity direction.
        2. Cross-product with predicted gravity from current quaternion → error.
        3. Feed error back via PI gains (Kp, Ki) to correct gyro integration.
        4. Integrate corrected angular velocity as quaternion derivative:
               dq/dt = 0.5 · q ⊗ [0, ω_corrected]
        5. Renormalise quaternion.
    Outputs: estimated quaternion, euler angles.
    Does NOT estimate yaw from accelerometer (no magnetometer); yaw drifts slowly.
 
AltitudeFusion  (optional)
    Complementary filter merging barometer altitude with IMU vertical acceleration.
    Barometer: low noise but low rate (GPS-level, ~5 Hz).
    IMU accel:  high rate but drifts when double-integrated.
    Blends at crossover frequency to get smooth, drift-free altitude estimate.
 
Public API:
    MahonyFilter(Kp, Ki)
    .update(accel, gyro, dt)   — fuse one IMU sample.
    .euler -> ndarray          — current [roll, pitch, yaw] estimate in radians.
    .q    -> ndarray           — current unit quaternion.
"""