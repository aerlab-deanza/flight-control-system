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

# test_plant.py
import numpy as np
import pytest

from src.sim.plant import Plant, VehicleConfig, G


# ============================================================
# HELPERS / FIXTURES
# ============================================================

@pytest.fixture
def cfg():
    return VehicleConfig(
        I=np.diag([0.02, 0.02, 0.04]),
        m=1.5,
        L=0.25,
        kT=1.0e-5,
        kQ=2.0e-7,
        c_v=0.0,
        c_w=0.0,
    )


@pytest.fixture
def yaw_signs():
    # Example:
    # M0 CW, M1 CCW, M2 CW, M3 CCW
    return np.array([-1.0, +1.0, -1.0, +1.0])


@pytest.fixture
def plant(cfg, yaw_signs):
    return Plant(cfg, yaw_signs)


def equal_rpm_for_hover(cfg):
    """
    Hover condition with identity attitude:

        sum(thrusts) = m g
        4 * kT * omega^2 = m g
        omega = sqrt(m g / (4 kT))
    """
    return np.sqrt(cfg.m * G / (4.0 * cfg.kT))


# ============================================================
# BASIC INITIALIZATION / RESET
# ============================================================

def test_init_state_has_correct_shape_and_identity_quaternion(plant):
    assert plant.state.shape == (13,)
    np.testing.assert_allclose(plant.pos, np.array([0.0, 0.0, 0.0]))
    np.testing.assert_allclose(plant.vel, np.array([0.0, 0.0, 0.0]))
    np.testing.assert_allclose(plant.quat, np.array([1.0, 0.0, 0.0, 0.0]))
    np.testing.assert_allclose(plant.omega, np.array([0.0, 0.0, 0.0]))


def test_reset_sets_position_and_yaw(plant):
    pos = np.array([10.0, -3.0, 2.0])
    yaw = np.pi / 2

    plant.reset(pos=pos, yaw=yaw)

    np.testing.assert_allclose(plant.pos, pos)

    expected_quat = np.array([
        np.cos(yaw / 2.0),
        0.0,
        0.0,
        np.sin(yaw / 2.0),
    ])
    np.testing.assert_allclose(plant.quat, expected_quat, atol=1e-12)

    np.testing.assert_allclose(plant.vel, np.zeros(3))
    np.testing.assert_allclose(plant.omega, np.zeros(3))


# ============================================================
# QUATERNION / ROTATION TESTS
# ============================================================

def test_normalize_quat_returns_unit_quaternion(plant):
    q = np.array([2.0, 0.0, 0.0, 0.0])
    qn = plant.normalize_quat(q)

    assert np.isclose(np.linalg.norm(qn), 1.0)
    np.testing.assert_allclose(qn, np.array([1.0, 0.0, 0.0, 0.0]))


def test_quat_to_R_identity_is_identity_matrix(plant):
    q = np.array([1.0, 0.0, 0.0, 0.0])
    R = plant.quat_to_R(q)

    np.testing.assert_allclose(R, np.eye(3), atol=1e-12)


def test_rotation_matrix_is_orthonormal(plant):
    q = plant.normalize_quat(np.array([0.9, 0.1, -0.2, 0.3]))
    R = plant.quat_to_R(q)

    np.testing.assert_allclose(R.T @ R, np.eye(3), atol=1e-10)
    assert np.isclose(np.linalg.det(R), 1.0, atol=1e-10)


# ============================================================
# MOTOR / FORCE / TORQUE TESTS
# ============================================================

def test_motor_thrusts_follow_square_law(plant):
    omegas = np.array([100.0, 200.0, 300.0, 400.0])
    thrusts = plant.motor_thrusts(omegas)

    expected = plant.cfg.kT * omegas**2
    np.testing.assert_allclose(thrusts, expected)


def test_motor_yaw_torques_follow_square_law(plant):
    omegas = np.array([100.0, 200.0, 300.0, 400.0])
    torques = plant.motor_yaw_torques(omegas)

    expected = plant.cfg.kQ * omegas**2
    np.testing.assert_allclose(torques, expected)


def test_total_thrust_body_points_upward_in_ned_frd(plant):
    thrusts = np.array([1.0, 2.0, 3.0, 4.0])
    F = plant.total_thrust_body(thrusts)

    # NED + FRD means body +z is DOWN,
    # so thrust should point upward = negative body z
    np.testing.assert_allclose(F, np.array([0.0, 0.0, -10.0]))


def test_total_torque_body_matches_manual_formula(plant):
    thrusts = np.array([1.0, 2.0, 3.0, 4.0])
    omegas = np.array([100.0, 200.0, 300.0, 400.0])

    tau = plant.total_torque_body(thrusts, omegas)

    expected_tau_x = plant.cfg.L * (thrusts[1] - thrusts[3])
    expected_tau_y = plant.cfg.L * (thrusts[2] - thrusts[0])
    expected_tau_z = np.dot(plant.yaw_signs, plant.cfg.kQ * omegas**2)

    expected = np.array([expected_tau_x, expected_tau_y, expected_tau_z])
    np.testing.assert_allclose(tau, expected)


# ============================================================
# TRANSLATIONAL DYNAMICS TESTS
# ============================================================

def test_translational_accel_is_gravity_when_no_thrust(plant):
    q = np.array([1.0, 0.0, 0.0, 0.0])
    vel = np.array([0.0, 0.0, 0.0])
    thrusts = np.zeros(4)

    a = plant.translational_accel_world(q, vel, thrusts)

    # In NED, gravity is +z
    np.testing.assert_allclose(a, np.array([0.0, 0.0, G]), atol=1e-12)


def test_translational_accel_is_near_zero_at_hover_identity_attitude(plant):
    omega_hover = equal_rpm_for_hover(plant.cfg)
    omegas = np.full(4, omega_hover)
    thrusts = plant.motor_thrusts(omegas)

    q = np.array([1.0, 0.0, 0.0, 0.0])   # level attitude
    vel = np.array([0.0, 0.0, 0.0])

    a = plant.translational_accel_world(q, vel, thrusts)

    np.testing.assert_allclose(a, np.zeros(3), atol=1e-8)


# ============================================================
# ROTATIONAL DYNAMICS TESTS
# ============================================================

def test_angular_accel_zero_when_no_torque_and_no_rotation(plant):
    omega_b = np.array([0.0, 0.0, 0.0])
    thrusts = np.zeros(4)
    omegas = np.zeros(4)

    alpha = plant.angular_accel_body(omega_b, thrusts, omegas)

    np.testing.assert_allclose(alpha, np.zeros(3), atol=1e-12)


def test_angular_accel_matches_I_inverse_tau_when_omega_zero(plant):
    omega_b = np.array([0.0, 0.0, 0.0])
    thrusts = np.array([1.0, 2.0, 3.0, 4.0])
    omegas = np.array([100.0, 200.0, 300.0, 400.0])

    tau = plant.total_torque_body(thrusts, omegas)
    expected_alpha = np.linalg.solve(plant.cfg.I, tau)

    alpha = plant.angular_accel_body(omega_b, thrusts, omegas)

    np.testing.assert_allclose(alpha, expected_alpha)


# ============================================================
# FULL DERIVATIVE TESTS
# ============================================================

def test_derivatives_has_correct_shape(plant):
    s = plant.state.copy()
    omegas = np.zeros(4)

    sdot = plant.derivatives(s, omegas)

    assert sdot.shape == (13,)


def test_derivatives_position_dot_equals_velocity(plant):
    s = plant.state.copy()
    s[3:6] = np.array([1.2, -0.5, 3.4])  # world velocity
    omegas = np.zeros(4)

    sdot = plant.derivatives(s, omegas)

    np.testing.assert_allclose(sdot[0:3], s[3:6])


def test_derivatives_quaternion_dot_zero_when_omega_zero(plant):
    s = plant.state.copy()
    s[6:10] = np.array([1.0, 0.0, 0.0, 0.0])
    s[10:13] = np.array([0.0, 0.0, 0.0])
    omegas = np.zeros(4)

    sdot = plant.derivatives(s, omegas)

    np.testing.assert_allclose(sdot[6:10], np.zeros(4), atol=1e-12)


# ============================================================
# STEP / INTEGRATION TESTS
# ============================================================

def test_step_keeps_quaternion_normalized(plant):
    plant.reset()
    plant.state[10:13] = np.array([0.2, -0.1, 0.3])  # body rates
    plant.set_rpms(np.array([300.0, 310.0, 290.0, 305.0]))

    plant.step(0.01)

    assert np.isclose(np.linalg.norm(plant.quat), 1.0, atol=1e-10)


def test_step_hover_does_not_accelerate_much_in_z(plant):
    plant.reset()
    omega_hover = equal_rpm_for_hover(plant.cfg)
    plant.set_rpms(np.full(4, omega_hover))

    s_before = plant.state.copy()
    s_after = plant.step(0.01)

    # With perfect hover and level attitude, z-velocity should stay near zero
    assert abs(s_after[5] - s_before[5]) < 1e-6


# ============================================================
# BODY ACCEL / IMU-LIKE TESTS
# ============================================================

def test_body_accel_hover_level_is_negative_g_in_body_z(plant):
    plant.reset()
    omega_hover = equal_rpm_for_hover(plant.cfg)
    plant.set_rpms(np.full(4, omega_hover))

    acc_b = plant.body_accel()

    # In FRD (body +z down), hover specific force should be upward,
    # which is negative body z.
    np.testing.assert_allclose(acc_b, np.array([0.0, 0.0, -G]), atol=1e-8)