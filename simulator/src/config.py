"""
Configuration loader and dataclass definitions.
 
Responsibilities:
  - Define dataclasses for each subsystem's parameters:
      VehicleConfig   — mass, arm length, inertia tensor, kT, kQ, motor limits.
      ControllerConfig — PID gains and saturation limits for all five loops.
      SensorConfig    — noise sigmas and bias vectors for IMU, baro, GPS.
      WindConfig      — mean speed, turbulence sigma, gust magnitude, time constant.
      SimConfig       — duration, dt, log rate, output paths.
  - load_config(path: str) -> SimConfig:
      Read a YAML file, validate required fields, return populated dataclasses.
  - Provide safe defaults so the sim runs without a config file.
 
Note:
    All angular values stored internally in radians.
    All physical units: SI (kg, m, s, N, N·m).
"""
