# Hardware Design

## Frame

- Type: 450mm X-configuration
- Material: [Carbon fiber / Fiberglass]
- Mass: TBD < 250g

## Electronics

**Flight Controller:**
- MCU: Teensy 4.0 (600 MHz ARM Cortex-M7)
- IMU: MPU6050 (gyro + accel)
- Mount: Protoboard with vibration dampers

**Power:**
- Battery: 3S LiPo, 2200mAh, 25C
- Voltage regulation: 5V BEC from ESCs
- Current monitoring: [TBD]

**Motors & ESCs:**
- Motors: [Brand/model], [KV rating]
- ESCs: [Brand/model], [Current rating]
- Props: [Size], [Pitch]

## Bill of Materials

See `electrical/bom.csv` for complete parts list with suppliers and costs.

## Assembly

See `integration/assembly_guide.md` for step-by-step instructions.

## Mass Properties

See `mechanical/mass_properties.md` for measured values (needed for sim).
