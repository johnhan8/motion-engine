# Motion Engine

Real-time motion processing (IMU-first pipeline in `main.py`); legacy MediaPipe pose stack remains in-repo for optional vision work.

**Guiding vision and roadmap:** [MOTION_ENGINE_SPEC.md](MOTION_ENGINE_SPEC.md).

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
