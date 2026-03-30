"""
Post-flight performance metrics computed from logged telemetry.
 
Functions
---------
position_rmse(data) -> float
    Root-mean-square position error  ‖p_actual − p_target‖  over the flight.
 
tracking_error_per_segment(data) -> list[float]
    Mean position error for each waypoint-to-waypoint leg.
    Useful for identifying which segments the controller handles poorly.
 
attitude_rmse(data) -> dict
    Separate RMSE for roll, pitch, yaw tracking.
 
estimation_error(data) -> dict
    Mahony filter accuracy: RMSE of (true − estimated) roll and pitch.
 
max_tilt_angle(data) -> float
    Peak roll or pitch reached during flight  [deg].
 
motor_utilisation(data) -> ndarray[4]
    Mean RPM per motor normalised to max_rpm.  Values near 1.0 indicate
    a motor that was saturated; asymmetry indicates trim offsets.
 
flight_time(data) -> float
    Total simulated duration  [s].
 
All functions accept the dict returned by Logger.arrays().
"""
 
