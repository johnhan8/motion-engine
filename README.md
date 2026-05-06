# Motion Engine

Real-time human motion tracking system using MediaPipe Pose.

## Features
- Live webcam pose detection
- Squat, curl, and arm raise tracking
- Rep counting with state machines
- Multi-exercise switching

## Tech Stack
- Python
- OpenCV
- MediaPipe

## Status
Working prototype (v1). Improving reliability and smoothing.

## Stable: IMU pipeline
The path **sensors → filtering → `core/pipeline.py` → `main.py`** is treated as **stable**.  
Do not change layout or public behavior except for bugfixes or deliberate interface updates.
- Harness: `scripts/run_imu_harness.py` uses the same `core.pipeline.run` entrypoint.
- Plot: `scripts/plot_imu.py` reads the CSV written by that harness.

## Run locally
pip install -r requirements.txt
python main.py
