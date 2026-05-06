# Architecture Rules

## Active System (IMU Pipeline)
- sensors/
- filtering/
- core/pipeline.py
- main.py
- scripts/run_imu_harness.py

## Rules
- IMU pipeline is independent
- No dependencies from perception/ or exercises/
- core/ pipeline must NOT import legacy modules
- Keep IMU system self-contained

## Legacy System
- perception/, exercises/, session/ are deprecated for IMU work
- Do not modify unless explicitly working on vision stack
