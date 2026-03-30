
"""
Entry point for the quadcopter simulator.
 
Responsibilities:
  - Parse CLI arguments (duration, dt, config path, output directory).
  - Load config from YAML via config.py.
  - Instantiate all subsystems: plant, controller, sensors, filters, logger.
  - Run the main simulation loop:
      for each timestep:
          1. Step wind / environment.
          2. Read sensors from plant (noisy IMU, baro, GPS).
          3. Update Mahony filter → estimated attitude.
          4. Advance waypoint manager.
          5. Run cascade PID → RPM commands.
          6. Step plant physics (RK4).
          7. Log telemetry at downsampled rate.
  - After loop: call analysis/metrics.py and analysis/plotter.py.
 
Usage:
    python main.py --config config/default.yaml --duration 80
"""
 