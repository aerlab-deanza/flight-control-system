"""
Waypoint / mission scheduler.
 
Manages sequential navigation through a list of 3-D waypoints, each with an
optional heading (yaw) target.  Advances to the next waypoint when the vehicle
comes within `acceptance_radius` metres of the current target.
 
Waypoint format:  (x [m], y [m], z [m], yaw [rad])
    Yaw defaults to 0.0 if omitted.
 
Public API:
    Scheduler(waypoints: list, acceptance_radius: float = 0.4)
    .update(pos: ndarray) -> (target_pos, target_yaw, advanced: bool)
        — call every timestep; returns current target and whether WP changed.
    .done -> bool          — True once the final waypoint is reached.
    .progress -> (idx, total)  — for logging / display.
    .reset()               — restart from first waypoint.
 
Extension points:
    - Add loiter time per waypoint (hold for N seconds before advancing).
    - Add velocity feed-forward (pass desired approach speed to controller).
    - Support 'land' and 'takeoff' special waypoint types.
"""
 
