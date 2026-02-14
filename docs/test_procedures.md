# Test Procedures

## Bench Tests

### BT-001: Sensor Verification
**Purpose:** Verify IMU reads correctly  
**Setup:** Teensy + MPU6050 on bench, USB power  
**Procedure:**
1. Flash firmware with sensor test code
2. Open serial monitor (115200 baud)
3. Rotate IMU by hand
4. Verify gyro readings change appropriately
5. Check sign conventions (right-hand rule)

**Pass criteria:** Gyro reads ±2000°/s range, noise < 0.1°/s

### BT-002: Motor Spin Test
**Purpose:** Verify ESCs respond to commands  
**Setup:** Teensy + 4x ESCs + motors (NO PROPS), bench power  
**Procedure:**
1. Calibrate ESCs (google "ESC calibration procedure")
2. Send throttle = 10% command to ESC1
3. Verify motor 1 spins
4. Repeat for ESC 2, 3, 4
5. Check rotation directions (CW vs CCW)

**Pass criteria:** All motors spin, correct directions

### BT-003: Control Loop Timing
**Purpose:** Verify 1kHz loop runs consistently  
**Setup:** Teensy running control loop, oscilloscope or serial  
**Procedure:**
1. Toggle GPIO pin at start of each loop iteration
2. Measure on oscilloscope OR print micros() timestamps
3. Calculate jitter

**Pass criteria:** 1000 ± 5 μs per iteration

## Flight Tests

### FT-001: Tethered Hover
**Purpose:** Verify basic stabilization  
**Setup:** Drone on test stand or tethered to ceiling  
**Procedure:**
1. Pre-flight checklist (see below)
2. Arm via serial command
3. Slowly increase throttle
4. Observe: Does drone attempt to level itself?
5. Record data

**Pass criteria:** Drone resists manual tilting, no divergence

### FT-002: Free Hover
**Purpose:** Achieve stable flight  
**Setup:** Open area, observer with kill switch  
**Procedure:**
1. Pre-flight checklist
2. Arm
3. Slowly increase throttle to liftoff
4. Hover at 1 foot altitude for 10 seconds
5. Land smoothly

**Pass criteria:** 10+ second hover, < 10° tilt

### FT-003: Angle Tracking
**Purpose:** Validate control performance  
**Setup:** Same as FT-002  
**Procedure:**
1. Hover stably
2. Command 10° roll angle
3. Observe response
4. Record logs

**Pass criteria:** Reaches setpoint in < 1s, < 20% overshoot

## Pre-Flight Checklist

- [ ] Battery voltage > 11.1V (3S)
- [ ] All props secure and undamaged
- [ ] Flight controller mounted securely
- [ ] No loose wires
- [ ] Kill switch functional
- [ ] Clear flight area (no people/obstacles)
- [ ] Camera recording
- [ ] Data logging enabled
- [ ] Weather acceptable (< 10 mph wind)
```

---

### `analysis/` - Post-Processing
```
analysis/
├── README.md
├── compare_sim_vs_flight.py
├── plot_pid_response.py
├── compute_metrics.py
└── notebooks/
    └── flight_analysis.ipynb
