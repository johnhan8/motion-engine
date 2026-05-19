"""Reusable IMU filtering primitives and EMA implementations.

Pure blend functions are stateless; ``EmaFilter`` / ``ScalarEma`` hold runtime state.
IMU pipeline uses this module for all EMA behavior (see ``core.pipeline``).
"""

from __future__ import annotations

from dataclasses import dataclass

from sensors.imu_simulator import ImuSample


@dataclass(frozen=True)
class FilteredImuSample:
    """Filtered IMU output for accel and gyro vectors."""

    accel: tuple[float, float, float]
    gyro: tuple[float, float, float]


def validate_alpha(alpha: float) -> float:
    """Return alpha if valid for EMA; raises ValueError otherwise."""
    if not 0.0 < alpha <= 1.0:
        raise ValueError("alpha must be in (0.0, 1.0].")
    return alpha


def ema_vector_blend(
    previous: tuple[float, float, float] | None,
    current: tuple[float, float, float],
    alpha: float,
) -> tuple[float, float, float]:
    """One EMA step for a 3-vector. Stateless; ``previous`` is None on first sample."""
    if previous is None:
        return current
    return tuple(
        (alpha * cur) + ((1.0 - alpha) * prev) for cur, prev in zip(current, previous)
    )


def ema_scalar_blend(previous: float | None, current: float, alpha: float) -> float:
    """One EMA step for a scalar. Stateless; ``previous`` is None on first sample."""
    if previous is None:
        return current
    return (alpha * current) + ((1.0 - alpha) * previous)


class ScalarEma:
    """EMA smoother for a single scalar signal."""

    def __init__(self, alpha: float = 0.2) -> None:
        self._alpha = validate_alpha(alpha)
        self._state: float | None = None

    @property
    def alpha(self) -> float:
        return self._alpha

    def set_alpha(self, alpha: float) -> None:
        self._alpha = validate_alpha(alpha)

    def update(self, value: float) -> float:
        self._state = ema_scalar_blend(self._state, value, self._alpha)
        return self._state


class EmaFilter:
    """Apply EMA smoothing independently to accel and gyro channels."""

    def __init__(self, alpha: float = 0.2) -> None:
        self._alpha = validate_alpha(alpha)
        self._accel_state: tuple[float, float, float] | None = None
        self._gyro_state: tuple[float, float, float] | None = None

    @property
    def alpha(self) -> float:
        """Return the current EMA alpha value."""
        return self._alpha

    def set_alpha(self, alpha: float) -> None:
        """Update EMA alpha at runtime."""
        self._alpha = validate_alpha(alpha)

    def update(self, sample: ImuSample) -> FilteredImuSample:
        """Update EMA state with a new IMU sample and return filtered output."""
        self._accel_state = ema_vector_blend(self._accel_state, sample.accel, self._alpha)
        self._gyro_state = ema_vector_blend(self._gyro_state, sample.gyro, self._alpha)
        return FilteredImuSample(accel=self._accel_state, gyro=self._gyro_state)
