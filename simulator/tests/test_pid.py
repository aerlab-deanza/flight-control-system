"""
tests/test_pid.py
=================
Unit tests for the PIDController class (src/sim/controller.py).
 
What is tested
--------------
1. Zero-error output
       When measurement == setpoint, output is 0 (no I accumulated, no D spike).
 
2. Proportional-only response
       With ki=0, kd=0: output == kp * (setpoint - measurement).
       Sign: positive error → positive output.
 
3. Integral accumulation
       After N steps of constant error e, integral term == ki * e * N * dt.
       Verify output includes the accumulated integral.
 
4. Derivative kick on step input
       On the FIRST step after a large error change:
           derivative = (error - prev_error) / dt
       Verify the D term contributes the expected amount.
 
5. First-step derivative warm-start
       On the very first call, prev_error is None → derivative term = 0.
       No spurious D spike on initialisation.
 
6. Anti-windup clamping
       Set output_limits = (-10, 10), ki > 0.
       Drive error to a large value for many steps.
       Assert: ki * integral is never larger than the output limit.
       Assert: output is clamped to [-10, 10] throughout.
 
7. Output limit saturation
       With large kp: output must be clamped to output_limits.
       Check both positive and negative saturation.
 
8. Reset clears state
       After reset(): integral == 0, prev_error is None, last_output is None.
       Next update() must behave as if newly constructed.
 
9. Setpoint change mid-flight
       Call set_setpoint() between update() calls.
       Verify the error on the next update reflects the new setpoint.
 
10. Negative setpoint / measurement
        All arithmetic must work correctly with negative values.
        (Common failure: sign errors in error = setpoint - measurement.)
 
11. Step response shape  (integration test)
        Run a P-only controller on a first-order plant (dx/dt = -x + u) for
        100 steps.  Assert the output converges to within 5% of setpoint.
        This catches gain-sign or frame errors that unit tests miss.
 
12. dt validation
        update() with dt <= 0 must raise ValueError.
 
Usage
-----
    pytest tests/test_pid.py -v
    pytest tests/test_pid.py -v --tb=short
"""