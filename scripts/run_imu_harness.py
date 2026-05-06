"""Run IMU pipeline for a fixed duration and log accel to CSV.

Uses the stable entrypoint ``core.pipeline.run`` (same contract as ``main.py``).
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.pipeline import run


def parse_args() -> argparse.Namespace:
    """Parse harness runtime arguments."""
    parser = argparse.ArgumentParser(description="IMU pipeline CSV logger.")
    parser.add_argument("--duration-seconds", type=float, default=10.0)
    parser.add_argument("--sample-rate-hz", type=float, default=50.0)
    parser.add_argument("--alpha", type=float, default=0.2)
    parser.add_argument(
        "--motion-pattern",
        choices=("none", "sinusoidal", "random_walk"),
        default="sinusoidal",
    )
    parser.add_argument("--output", default="data/imu_pipeline_log.csv")
    return parser.parse_args()


def run_harness(
    duration_seconds: float,
    sample_rate_hz: float,
    alpha: float,
    motion_pattern: str,
    output_path: str,
) -> None:
    """Execute pipeline loop and store acceleration channels to CSV."""
    run(
        duration_seconds=duration_seconds,
        samples=None,
        sample_rate_hz=sample_rate_hz,
        alpha=alpha,
        motion_pattern=motion_pattern,
        csv_output=output_path,
    )


if __name__ == "__main__":
    args = parse_args()
    run_harness(
        duration_seconds=args.duration_seconds,
        sample_rate_hz=args.sample_rate_hz,
        alpha=args.alpha,
        motion_pattern=args.motion_pattern,
        output_path=args.output,
    )
