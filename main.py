"""IMU pipeline CLI entry (stable).

Delegates to ``core.pipeline.run`` only. Do not reintroduce alternate IMU
execution paths here without updating the stability contract in
``core/pipeline.py``.
"""

from __future__ import annotations

import argparse

from core.pipeline import run

def _parse_args() -> argparse.Namespace:
    """Parse runtime options for IMU pipeline execution."""
    parser = argparse.ArgumentParser(description="IMU simulator + EMA filter demo.")
    parser.add_argument(
        "--samples",
        type=int,
        default=10,
        help="Number of samples to generate.",
    )
    parser.add_argument(
        "--alpha",
        type=float,
        default=0.2,
        help="Initial EMA alpha in (0.0, 1.0].",
    )
    parser.add_argument(
        "--interactive-tuning",
        action="store_true",
        help="Prompt to tune alpha after each sample.",
    )
    parser.add_argument(
        "--motion-pattern",
        choices=("none", "sinusoidal", "random_walk"),
        default="sinusoidal",
        help="IMU motion pattern mode.",
    )
    return parser.parse_args()


def main(
    samples: int = 10,
    alpha: float = 0.2,
    interactive_tuning: bool = False,
    motion_pattern: str = "sinusoidal",
) -> None:
    """Run the IMU pipeline via the single core entry point."""
    run(
        samples=samples,
        alpha=alpha,
        motion_pattern=motion_pattern,
        interactive_tuning=interactive_tuning,
    )


if __name__ == "__main__":
    args = _parse_args()
    main(
        samples=args.samples,
        alpha=args.alpha,
        interactive_tuning=args.interactive_tuning,
        motion_pattern=args.motion_pattern,
    )
