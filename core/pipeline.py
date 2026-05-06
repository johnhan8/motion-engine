"""Single entry point for IMU simulation -> EMA filtering -> logging."""

from __future__ import annotations

import csv
import math
import time
from pathlib import Path
from typing import Protocol

from filtering.ema_filter import EmaFilter, FilteredImuSample
from sensors.imu_simulator import ImuSample, ImuSimulator


class OutputLogger(Protocol):
    """Protocol for pipeline output consumers."""

    def log(self, index: int, elapsed_s: float, raw: ImuSample, filtered: FilteredImuSample) -> None:
        """Consume one pipeline sample."""


class ConsoleLogger:
    """Human-readable console output logger."""

    def log(self, index: int, elapsed_s: float, raw: ImuSample, filtered: FilteredImuSample) -> None:
        print(
            f"[{index:03d}] t={elapsed_s:.3f}s "
            f"raw_accel={raw.accel} raw_gyro={raw.gyro} | "
            f"ema_accel={filtered.accel} ema_gyro={filtered.gyro}"
        )


class CsvLogger:
    """CSV logger for raw and EMA acceleration channels."""

    def __init__(self, output_path: str) -> None:
        self._path = Path(output_path)
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._fh = self._path.open("w", newline="")
        self._writer = csv.writer(self._fh)
        self._writer.writerow(
            [
                "time_s",
                "raw_accel_x",
                "raw_accel_y",
                "raw_accel_z",
                "ema_accel_x",
                "ema_accel_y",
                "ema_accel_z",
            ]
        )

    def log(self, index: int, elapsed_s: float, raw: ImuSample, filtered: FilteredImuSample) -> None:
        self._writer.writerow(
            [
                elapsed_s,
                raw.accel[0],
                raw.accel[1],
                raw.accel[2],
                filtered.accel[0],
                filtered.accel[1],
                filtered.accel[2],
            ]
        )

    def close(self) -> None:
        self._fh.close()

    @property
    def path(self) -> Path:
        return self._path


class ImuPipeline:
    """Connect IMU sensor simulation to EMA filtering."""

    def __init__(
        self,
        alpha: float = 0.2,
        motion_pattern: str = "sinusoidal",
        sample_rate_hz: float = 50.0,
    ) -> None:
        self.sensor = ImuSimulator(motion_pattern=motion_pattern)
        self.filter = EmaFilter(alpha=alpha)
        self.sample_rate_hz = sample_rate_hz

    def set_alpha(self, alpha: float) -> None:
        """Tune EMA alpha at runtime."""
        self.filter.set_alpha(alpha)

    def step(self) -> tuple[ImuSample, FilteredImuSample]:
        """Process one sensor sample through the filter."""
        raw = self.sensor.read()
        filtered = self.filter.update(raw)
        self._assert_sample_shapes(raw, filtered)
        self._assert_filtered_finite(filtered)
        return raw, filtered

    @staticmethod
    def _assert_vector3(name: str, value: tuple[float, ...]) -> None:
        assert isinstance(value, tuple), f"{name} must be a tuple, got {type(value).__name__}"
        assert len(value) == 3, f"{name} must have exactly 3 axes, got {len(value)}"

    def _assert_sample_shapes(self, raw: ImuSample, filtered: FilteredImuSample) -> None:
        self._assert_vector3("raw.accel", raw.accel)
        self._assert_vector3("raw.gyro", raw.gyro)
        self._assert_vector3("ema.accel", filtered.accel)
        self._assert_vector3("ema.gyro", filtered.gyro)

    @staticmethod
    def _assert_filtered_finite(filtered: FilteredImuSample) -> None:
        assert filtered.accel is not None, "EMA accel output must not be None"
        assert filtered.gyro is not None, "EMA gyro output must not be None"
        for idx, v in enumerate(filtered.accel):
            assert math.isfinite(v), f"EMA accel contains invalid value at axis {idx}: {v}"
        for idx, v in enumerate(filtered.gyro):
            assert math.isfinite(v), f"EMA gyro contains invalid value at axis {idx}: {v}"

    def run(
        self,
        *,
        duration_seconds: float | None = None,
        samples: int | None = None,
        logger: OutputLogger | None = None,
        interactive_tuning: bool = False,
    ) -> None:
        """Run the pipeline loop and emit samples through a logger."""
        if duration_seconds is None and samples is None:
            raise ValueError("Provide either duration_seconds or samples.")

        out = logger or ConsoleLogger()
        interval = 1.0 / self.sample_rate_hz
        start = time.perf_counter()
        deadline = start + duration_seconds if duration_seconds is not None else None
        idx = 0
        prev_ts: float | None = None

        while True:
            now = time.perf_counter()
            if samples is not None and idx >= samples:
                break
            if deadline is not None and now >= deadline:
                break
            if prev_ts is not None:
                assert now > prev_ts, (
                    f"Timestamps must be strictly increasing: prev={prev_ts:.9f}, now={now:.9f}"
                )

            raw, filtered = self.step()
            out.log(idx, now - start, raw, filtered)

            if interactive_tuning:
                user_input = input("New alpha (Enter to keep current): ").strip()
                if user_input:
                    try:
                        self.set_alpha(float(user_input))
                    except ValueError as exc:
                        print(f"Invalid alpha: {exc}")

            idx += 1
            prev_ts = now
            sleep_for = interval - (time.perf_counter() - now)
            if sleep_for > 0:
                time.sleep(sleep_for)


def run(
    *,
    duration_seconds: float | None = None,
    samples: int | None = 10,
    alpha: float = 0.2,
    motion_pattern: str = "sinusoidal",
    sample_rate_hz: float = 50.0,
    interactive_tuning: bool = False,
    csv_output: str | None = None,
) -> None:
    """Top-level pipeline entry point used by main and scripts."""
    pipeline = ImuPipeline(
        alpha=alpha,
        motion_pattern=motion_pattern,
        sample_rate_hz=sample_rate_hz,
    )
    csv_logger = CsvLogger(csv_output) if csv_output else None
    logger: OutputLogger = csv_logger if csv_logger else ConsoleLogger()
    try:
        pipeline.run(
            duration_seconds=duration_seconds,
            samples=samples,
            logger=logger,
            interactive_tuning=interactive_tuning,
        )
    finally:
        if csv_logger:
            csv_logger.close()
            print(f"Wrote IMU log to {csv_logger.path}")
