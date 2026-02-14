# System Architecture

## Overview
```
[Setpoint] → [Outer Loop] → [Rate SP] → [Inner PID] → [Mixer] → [Motors]
                ↑                 ↑                                   ↓
                └─[Angle Est]─────┴───[Filtered Gyro]←──[Sensors + Noise]
                                                              ↑
                                                         [Plant Dynamics]
```

## Control Loops

### Outer Loop: Angle → Rate
- **Input:** Desired angle (φ_sp)
- **Feedback:** Estimated angle (φ_est)
- **Output:** Desired rate (p_sp)
- **Control Law:** p_sp = K_p * (φ_sp - φ_est)
- **Rate:** 200 Hz

### Inner Loop: Rate → Torque
- **Input:** Desired rate (p_sp)
- **Feedback:** Filtered gyro (p_filt)
- **Output:** Torque command (τ_cmd)
- **Control Law:** PID with anti-windup
- **Rate:** 1 kHz

## State Estimation

**Complementary Filter:**
- Integrate gyro for short-term accuracy
- Correct with accel-derived angle for long-term stability
- α = 0.98 (typical)

## Filtering

**Gyro PT1 Filter:**
- Cutoff: 90 Hz
- Purpose: Remove high-frequency noise
- Trade-off: Adds ~2ms phase lag

**Notch Filter (optional):**
- Center: ~180 Hz (motor vibration frequency)
- Purpose: Reject resonant vibration
- Enable only if needed after flight tests

## Safety Features

1. **Arming logic:** Requires level attitude + zero throttle
2. **Failsafe:** Auto-disarm after 1s no command
3. **Orientation check:** Kill motors if upside-down
4. **Watchdog timer:** Reset if loop hangs

## Module Interfaces

See `simulator/src/` for reference implementation.
