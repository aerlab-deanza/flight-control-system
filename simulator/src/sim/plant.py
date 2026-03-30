"""
Quadrotor rigid-body physics model  (the 'plant' in control theory).
 
State vector  s ∈ ℝ¹³:
    s[0:3]   position      (x, y, z)  world ENU frame  [m]
    s[3:6]   velocity      (vx,vy,vz) world ENU frame  [m/s]
    s[6:10]  quaternion    (w, x, y, z) body → world   [–]
    s[10:13] angular vel   (p, q, r)  body frame        [rad/s]
 
Public API:
    Plant(cfg: VehicleConfig)
    .reset(pos, yaw)            — reinitialise state vector and motors.
    .set_rpms(rpms: ndarray)    — send RPM command to all four motors.
    .step(dt: float) -> state   — advance physics one timestep via RK4.
    .body_accel() -> ndarray    — specific force in body frame (for IMU).
    .pos / .vel / .quat / .euler / .omega / .R  — state accessors.
 
Internals:
    _derivatives(s, thrusts, torques) — Newton-Euler equations of motion.
        Forces:  gravity + thrust (body→world via R) + linear drag + wind drag.
        Torques: differential thrust (roll/pitch) + reactive torques (yaw)
                 + angular drag + gyroscopic term  ω × Iω.
    Motor   — nested class: first-order RPM lag, thrust = kT·ω², torque = kQ·ω².
    Ground plane enforced: z clamped to ≥ 0, downward velocity zeroed on contact.
 
Motor layout (+ configuration, viewed from above):
    M0 front (+X) CW    M1 right (+Y) CCW
    M2 back  (−X) CW    M3 left  (−Y) CCW
"""
 
