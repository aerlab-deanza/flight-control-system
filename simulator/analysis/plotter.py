"""
Visualisation utilities for post-flight telemetry analysis.
 
Functions
---------
plot_telemetry(data, vcfg, save_path)
    Full dashboard: dark-themed 4×4 grid of subplots.
    Panels: 3-D trajectory, altitude, XY position, velocities, Euler angles
            (true vs estimated), angular rates, motor RPMs, wind disturbance,
            yaw RPM differential, Mahony estimation error, position error norm,
            airspeed profile.
 
animate_flight(data, vcfg, save_gif, gif_path)
    3-D animated replay via matplotlib FuncAnimation.
    Renders body-frame arms (red=CW, green=CCW), flight trail coloured by speed,
    live HUD showing time / altitude / speed / attitude.
 
plot_metrics(metrics_dict, save_path)
    Bar/line summary of the values returned by analysis/metrics.py.
 
Style conventions:
    Background  #0b0c10  (near-black)
    Actual data  #00e5ff (cyan)
    Setpoints    #ff5252 (red-orange)
    Estimates    #ffd740 (amber)
    Velocities   #69ff47 (green)
    Wind         #ff9100 (orange)
    Per-motor    [cyan, orange, green, purple]
"""
 