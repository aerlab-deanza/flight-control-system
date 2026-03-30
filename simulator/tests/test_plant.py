"""
tests/test_plant.py
===================
Unit and integration tests for the QuadDynamics plant model (src/sim/plant.py).
 
What is tested
--------------
1. Hover equilibrium
       Set all four motors to hover RPM:
           hover_rpm = sqrt(mass * g / (4 * kT))
       Step for 1 second.  Assert:
           |Δz|   < 0.01 m   (altitude barely moves)
           |roll| < 0.1 deg
           |pitch|< 0.1 deg
 
2. Quaternion normalisation invariant
       After any number of step() calls, |q| == 1.0 ± 1e-6.
 
3. Ground plane clamp
       Start at z=0, command all motors to min_rpm (falling).
       After several steps: z >= 0 and vz >= 0.
       (Plant must not tunnel through the floor.)
 
4. Thrust direction  (body frame → world frame rotation)
       Tilt the drone 45° in roll (set quaternion directly).
       Apply symmetric motor thrust.
       Net horizontal force must be non-zero in the expected direction.
       Net vertical force must be less than hover thrust.
 
5. Motor RPM lag
       Command a step from min_rpm to max_rpm.
       After one step of dt=0.005: new_rpm must be between old and max
       (first-order lag — cannot jump instantly).
       After many steps: rpm converges to max_rpm.
 
6. Motor RPM clamping
       set_rpms() with values above max_rpm or below min_rpm.
       Assert actual motor.rpm stays within [min_rpm, max_rpm] always.
 
7. Differential thrust → torque
       Command M0 (front) higher than M2 (back) by ΔRPM.
       After one step: pitch angular acceleration must be positive
       (nose pitches up when front motor is stronger).
 
8. Yaw torque from CW/CCW asymmetry
       Increase M0+M2 (CW) relative to M1+M3 (CCW) by ΔRPM.
       After one step: yaw angular acceleration must be in expected direction.
 
9. Wind disturbance effect
       Inject a constant wind = [5, 0, 0] m/s.
       At hover, net X-force must be non-zero (wind pushes drone).
       Body must start drifting in wind direction.
 
10. RK4 energy conservation proxy
        At hover, total kinetic energy (0.5*m*v²) must stay near zero
        (not growing) over 10 seconds.  A first-order Euler scheme diverges
        here; RK4 should not.
 
11. reset() restores initial state
        Step for 5 seconds, then reset(pos=[1,2,3], yaw=1.57).
        Assert pos == [1,2,3], euler[2] ≈ 1.57, vel == [0,0,0].
 
12. body_accel() at hover
        At hover (stationary, level): body_accel() ≈ [0, 0, 9.81].
        This is the specific force the IMU would measure.
 
13. NaN/Inf guard
        After 1000 random RPM commands (within limits), state must contain
        no NaN or Inf values.
 
Fixtures
--------
VehicleConfig with default parameters is instantiated fresh per test.
No shared mutable state between tests.
 
Usage
-----
    pytest tests/test_plant.py -v
    pytest tests/test_plant.py -v -k "hover"      # run hover tests only
    pytest tests/test_plant.py -v -k "motor"      # run motor tests only
"""