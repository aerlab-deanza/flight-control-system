# Requirements (Draft/ TBD)

This document defines the engineering metrics we will eventually commit to.

Targets are intentionally TBD until we have:
- hardware selected and integrated,**
- baseline measurements
- a first working estimator + controller loop.

Baseline measurements are:
1. Loop timing baseline
    - How fast and consistently the main control loop runs(e.g., 500 Hz).
2. IMU noise baseline
    - How "jittery" the IMU readings are when the drone is perfectly still
3. Estimator drift baseline
    - How much the estimated attitude slowly "walks" over time while the drone is stationary.
4. Rig step response baseline
    - The control system's response to a sudden change in command 
5. Failsafe baseline

## How to use this doc

1. Add rows when we identify a metric that matters.
2. Fill **How to Measure** first (so it's not vague).
3. After we collect the baseline data, set **Target** and **Min Acceptable**/
4. Every requirement must eventually link to evidence (log/plot/test note).

## Requirements Table (targets initially TBD)

| ID | Category | Metric | Target | Min Acceptable | How to Measure | Evidence Link | Owner | Status |
|---:|---|---|---|---|---|---|---|---|
| R-001 | Timing | Control loop frequency | TBD | TBD | Timestamp successive loop iterations for ≥ 60s; compute mean/min/max/std | TBD | TBD | Draft |
| R-002 | Timing | Control-loop jitter | TBD | TBD | Histogram of loop period; report 99th percentile | TBD | TBD | Draft |
| R-003 | Estimation | Attitude drift (bench, no motion) | TBD | TBD | Log attitude for ≥ 10 min stationary; fit slope (deg/min) | TBD | TBD | Draft |
| R-004 | Control | Roll/pitch settle time (step input) | TBD | TBD | Apply a defined step; compute settling time within tolerance band | TBD | TBD | Draft |
| R-005 | Actuation | Controller output → ESC update latency | TBD | TBD | Instrument timestamps at controller output and PWM/DShot update | TBD | TBD | Draft |
| R-006 | Safety | Disarm time on signal loss | TBD | TBD | Induce signal loss; measure time to motor stop command | TBD | TBD | Draft |
| R-007 | Logging | Minimum log fields + rates | TBD | TBD | Verify schema includes required fields; confirm effective sample rate | TBD | TBD | Draft |

## Notes
- "Target" is the goal; "Min Acceptable" is the pass threshold.
- TBD is allowed until we have measurements.
