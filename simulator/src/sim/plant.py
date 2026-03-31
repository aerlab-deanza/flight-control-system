"""
Quadrotor rigid-body physics model.

State vector s ∈ R^13:
    s[0:3]   position      (x, y, z)   world NED frame   [m]
    s[3:6]   velocity      (vx,vy,vz)  world NED frame   [m/s]
    s[6:10]  quaternion    (w, x, y, z) body -> world    [-]
    s[10:13] angular vel   (p, q, r)   body frame        [rad/s]

Frame convention:
    World frame: NED
        +x = North
        +y = East
        +z = Down

    Body frame: FRD
        +x = Forward
        +y = Right
        +z = Down

Physics convention:
    Gravity in world frame:
        g_world = [0, 0, +g]

    Rotor thrust acts upward, so in body frame:
        F_thrust_body = [0, 0, -T]

Core equations:
    pos_dot   = vel
    vel_dot   = g_world + (R @ F_thrust_body)/m + F_drag/m
    quat_dot  = 1/2 * Omega(omega_body) * quat
    omega_dot = I^{-1} [tau - omega x (I omega)]
"""
 
import numpy as np
from dataclasses import dataclass

# Gravity
G = 9.8

@dataclass 
class VehicleConfig:
    # Inertia of the Vehicle
    
    I: np.ndarray

    #Mass of the vehicle
    m: float 

    # Length of each arm
    # Distance from center of mass to each motor
    L: float 

    # Thrust koefficient
    kT: float

    # Yaw torque coefficient
    kQ = float

    # Linear drag coefficient
    # F_drag = -c_v * v
    c_v: float = 0.0

    # Angular drag coefficient
    # tau_drag = -c_w * omega
    c_w: float = 0.0




"""
FRAME CONVENTION:

World frame: NED
  x = North
  y = East
  z = Down

Body frame: also choose +z DOWN
  x = Forward
  y = Right
  z = Down

This is the standard aerospace-style convention.

Important consequences:

1) Gravity is positive in world z:
      g_world = [0, 0, +g]

2) If the propellers generate lift upward, then thrust points
   along NEGATIVE body z:
      F_thrust_body = [0, 0, -T]

3) Position and velocity in world frame:
      pos = [x, y, z]
      vel = [vx, vy, vz]

4) Angular velocity is in body frame:
      omega = [p, q, r]

5) Rotation matrix R maps body -> world:
      v_world = R @ v_body
"""d

class Plant:
    def __init__(self, state_vectors):
        self.state_vectors = np.array(state_vectors)
        # (x, y, z) world NED (north, east, down) frame (m)
        self.position = state_vectors[0:3] 

        # (vx, vy, vz) world NED frame (m/s)
        self.velocity = state_vectors[3:6] 

        # (w, x, y, z) body frame -> world
        self.quaternion = state_vectors[6:10] 

        # (p, q, r) body frame (rad /s)
        self.angular_velocity = state_vectors[10:13]
    
    # QUATERNION / ROTATION MATH
    
    def normalize_quat(self, q):

    def quat_to_R(self, q):
        """
        Convert unit quaternion q = [qw, qx, qy, qz]
        into rotation matrix R that maps:
            v_world = R @ v_body
        
        """
    
    # MOTOR / FORCE/ TORQUE MATH


    # TRANSLATIONAL DYNAMICS   


    # ROTATIONAL DYNAMICS


    # FULL STATE DERIVATIVE

    
    # RK4 INTEGRATION
    

    