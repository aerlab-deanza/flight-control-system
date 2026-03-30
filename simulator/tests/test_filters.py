"""
tests/test_filters.py
=====================
Unit and integration tests for the Madgwick attitude estimation filter.
 
What is tested
--------------
1. Identity initialisation
       Filter starts at q = [1, 0, 0, 0].
       getRoll / getPitch / getYaw all return 0.0 on a fresh instance.
 
2. Static convergence  (flat, stationary)
       Feed the filter N steps of:
           accel = [0, 0, 9.81]   (pure gravity, level)
           gyro  = [0, 0, 0]      (no rotation)
       After convergence (~200 steps at dt=0.005, beta=0.033):
           |roll|  < 0.5 deg
           |pitch| < 0.5 deg
       Yaw is unobservable without a magnetometer — not asserted here.
 
3. Known tilt recovery
       Initialise quaternion to a known 20° roll offset.
       Feed level accel + zero gyro.
       Assert filter returns to < 1° roll error within 2 seconds.
 
4. Pure gyro integration (accel = 0 fallback)
       Pass accel = [0, 0, 0] (simulated free-fall / sensor dropout).
       Filter must NOT crash or produce NaN.
       Quaternion must remain unit norm: |q| == 1.0 ± 1e-6.
 
5. Quaternion normalisation invariant
       After any number of update() calls with random valid inputs,
       assert |q| == 1.0 ± 1e-6  (numerical drift check).
 
6. Beta sensitivity  (parametric)
       Run convergence test with beta in [0.01, 0.033, 0.05, 0.1].
       Higher beta must converge faster (fewer steps to reach < 1° error).
       All beta values must remain stable (no divergence).
 
7. Drop-in equivalence with MahonyFilter
       Both filters fed identical IMU sequences from fixtures/.
       Final roll/pitch must agree to within 2° after 10 seconds.
       (Yaw comparison skipped — Mahony Ki accumulates differently.)
 
8. 9-DOF path smoke test  (MadgwickFilter9DOF)
       Feed valid accel + gyro + mag = [1, 0, 0].
       No crash, quaternion stays unit norm, yaw not NaN.
 
Fixtures
--------
fixtures/imu_static.npy   — 1000-sample static accel/gyro log  (pre-recorded)
fixtures/imu_flight.npy   — 5000-sample flight log with manoeuvres
 
Usage
-----
    pytest tests/test_filters.py -v
    pytest tests/test_filters.py -v -k "convergence"   # run one group only
"""