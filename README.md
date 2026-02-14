# flight-control-system

End-to-end quadcopter UAC development repository (mechanical + electrical + software + validation).

## What this is
A mini-Betaflight implementation: cascaded PID contorl for quadcopter attitude stabilization, built from first principles.

**Key Features:**
- Python simulator for control algorithm design and tuning
- Custom flight controller firmware (Teensy 4.0 + MPU6050)
- Hardware design files (breadboard -> protoboard -> custom PCB potentially)
- Full validation: sim-to-real comparison and flight test data

  **Team:**
  **Timeline:**
  **Status:** Planning

  ## Quick Start
  ### Simulator
  ```bash
  cd simulator
  pip install -r requirements.txt
  python -m src.main --config config/default.yaml
  ```

  ### Firmware (Teensy 4.0)
  ```bash
  cd firmware
  # Open in Arduino IDE or PlatformIO
  # Flash to Teensy 4.0
  ```

## Repository structure
- `hardware/` - CAD, BOM, electronics/power docs
- `firmware/` - embedded flight software
- `simulator/` - dynamics + sensor simulation
- `analysis/` - scripts/notebooks for logs + metrics
- `docs/` - architecutre notes, procedures, test plans
- `logs/` - sample logs + log format docs

## Current Milestones
Week 2: Simulator validated
Week 4: Hardware assmelbed, bench tested
Week 6: Firmware ported, sensor integration complete
Week 8: First flight attempt
Week 10: Stable flight + sim/reality comparision

## Getting Started
1. Skim `docs/` for the current architecture notes and conventions
2. Choose an area to contribute (hardware / firmware / simulation / analysis).
3. Create a brancy and add your work with a short folder-level README.


## License
MIT
