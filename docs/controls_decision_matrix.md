# Control Decision Matrix (Draft)

This document tracks control-related design decision for the quadcopter flight stack.


## Decision Matrix

| ID | Decision Area | Options Considered | Current Choice | Why (short) | Evidence Needed | Status |
|---:|---|---|---|---|---|---|
| C-001 | Control architecture | (A) Attitude outer + rate inner (B) Rate-only (C) Quaternion control | (A) Outer+inner | Common baseline; easy tuning + debugging | Rig step response plots | PROVISIONAL |
| C-002 | Primary control variables | (A) Euler angles (B) Quaternion error (C) DCM | TBD | Must align with estimator outputs + avoid singularities | Architecture doc + interface agreement | OPEN |
| C-003 | Inner loop type | (A) PID (B) PI (C) LQR | PID (v0) | Standard baseline; straightforward tuning | Stable rig response + no sustained oscillation | PROVISIONAL |
| C-004 | Outer loop type | (A) P/PI on angle (B) PID on angle (C) quaternion error controller | P/PI (v0) | Outer loop typically slower; keep simple early | Step tests showing adequate tracking | PROVISIONAL |
| C-005 | Anti-windup | (A) Clamp integrator (B) Back-calculation (C) Conditional integration | Clamp (v0) | Minimal complexity; prevents runaway | Saturation-recovery test evidence | PROVISIONAL |
| C-006 | Derivative term source | (A) error derivative (B) gyro rate (recommended) | Gyro rate | Less noise amplification; standard approach | Noise/response comparison | PROVISIONAL |
| C-007 | Filtering for D-term | (A) none (B) low-pass filter (C) notch (vibration) | TBD | Depends on vibration/noise baseline | IMU noise + vibration observations | OPEN |
| C-008 | Mixer model | (A) Standard X-mix (B) custom mix | Standard X-mix | Baseline and easy to validate | Mixer sanity test | PROVISIONAL |
| C-009 | Saturation handling | (A) clip outputs only (B) clip + scale (C) prioritize axes | TBD | Must prevent instability when motors saturate | Saturation tests + flight observations | OPEN |
| C-010 | Yaw control strategy | (A) yaw rate hold only (B) yaw angle hold | TBD | Angle hold needs stable heading reference | Estimator yaw stability baseline | OPEN |
| C-011 | Setpoint shaping | (A) raw step commands (B) rate limiting (C) smoothing/trajectory | TBD | Helps reduce oscillations + improves feel | Rig response comparison | OPEN |
| C-012 | Controller update rate | 250 Hz / 500 Hz / 1 kHz | Target 500 Hz | Common; matches sensor/compute constraints | Timing baseline (R-001/R-002) | PROVISIONAL |
| C-013 | Gains management | (A) fixed gains (B) mode-based (C) scheduled by throttle | Fixed (v0) | Keep initial tuning simple | Successful hover/rig performance | PROVISIONAL |
| C-014 | Units + conventions | deg vs rad; body axes; sign conventions | TBD | Must be consistent across sim/firmware/logs | Documented conventions + cross-check | OPEN |
| C-015 | Control output type | (A) thrust + torques (B) per-motor directly | TBD | Depends on mixer design + model | Architecture consistency + tests | OPEN |

---

(TBD)