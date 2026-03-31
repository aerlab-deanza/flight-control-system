"""
State estimation filters.
 
Classes
-------
MadgwickFilter
    Gradient-descent-based complementary filter on SO(3).
    Fuses gyroscope (high-rate, drifts) with accelerometer (noisy, drift-free).
    Algorithm (Madgwick 2010):
        1. Normalise accelerometer reading → estimated gravity direction.
        2. Define objective function f(q) measuring alignment error between
           predicted gravity (rotated via current quaternion) and measured gravity.
        3. Compute Jacobian J(q) of f with respect to quaternion components.
        4. Gradient step: ∇f = Jᵀ · f(q),  normalise → gradient direction.
        5. Fuse gyro rate with gradient correction via beta gain:
               ω_corrected = ω_gyro − beta · ∇̂f
        6. Integrate as quaternion derivative:
               dq/dt = 0.5 · q ⊗ [0, ω_corrected]
        7. Renormalise quaternion.
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