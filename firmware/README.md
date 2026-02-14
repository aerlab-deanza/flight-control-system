# Flight Controller Firmware

Teensy 4.0 firmware implementing cascaded PID control.

## Hardware Requirements

- Teensy 4.0
- MPU6050 IMU (I2C)
- 4x ESCs (PWM output)
- Power supply (5V → 3.3V regulated)

## Pinout


Teensy → MPU6050: 18 (SDA) → SDA 19 (SCL) → SCL 3.3V → VCC GND → GND
Teensy → ESCs: 2 → ESC1 (front-right) 3 → ESC2 (rear-right) 4 → ESC3 (rear-left) 5 → ESC4 (front-left)

## Building

**Arduino IDE:**
1. Install Teensyduino
2. Select Tools → Board → Teensy 4.0
3. Upload

**PlatformIO:**
```bash
pio run -t upload
