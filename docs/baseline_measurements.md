# Baseline Measurements (Simple + Flexible)

Baseline measurements are our “starting points.” We record them early so we can:
- see what improves over time,
- spot problems quickly,
- make future requirements based on real data.

**Rule:** if you record a baseline, include (1) what you measured, (2) the setup, and (3) a log or note showing it happened.

---

## 1 Loop timing baseline
**What it means:** How steady the main program loop runs.  
**Examples of what you can record:**
- “It runs close to the intended speed most of the time.”
- “Sometimes it slows down when logging is enabled.”
- “Average loop speed” (if you have a number)

**What to include:**
- intended loop rate (if any), plus your observation or measurement
- a short log snippet or screenshot of timing output

---

## 2 IMU noise baseline
**What it means:** How “shaky” the sensor readings are when the drone is not moving.  
**Examples of what you can record:**
- “Readings look stable / noisy.”
- “Noise improved after remounting the IMU.”
- a simple “before vs after” comparison plot or summary

**What to include:**
- how you kept it still (desk, foam, mounted to frame)
- raw IMU log (even short) or a quick plot/screenshot

---

## 3 Estimator drift baseline
**What it means:** Whether the estimated angle slowly changes over time even when nothing moves.  
**Examples of what you can record:**
- “Roll/pitch stays almost constant for 10 minutes.”
- “Yaw slowly drifts (expected without magnetometer).”
- “Drift got worse when vibration increased.”

**What to include:**
- how long you tested (e.g., 5–10 minutes)
- a plot or simple note like “changed by ~X degrees over Y minutes”

---

## 4 Rig step response baseline
**What it means:** How the system reacts to a sudden change in command when the drone is safely constrained (rig/tether).  
**Examples of what you can record:**
- “It reaches the target smoothly.”
- “It overshoots and oscillates.”
- “It responds faster after tuning.”

**What to include:**
- what step you applied (e.g., small roll command)
- what you observed (smooth / oscillates / too slow)
- a short log or video note (optional) + any plot if you have it

---

## 5 Failsafe baseline
**What it means:** What happens when something goes wrong (signal loss, bad sensor, etc.).  
**Examples of what you can record:**
- “Motors stop quickly when signal is lost.”
- “It logs the reason for disarm.”
- “It sometimes fails to disarm (needs fixing).”

**What to include:**
- what failure you triggered (RC off, unplug receiver, etc.)
- what the system did (disarm, keep running, error message)
- a log line or screenshot showing the event

---

## Minimum “good baseline” checklist
A baseline is good if it has:
- a short description of the setup,
- an observation or simple number,
- a log / plot / screenshot / short note stored in the repo.
