"""Exponential moving average filtering for IMU vectors."""

from __future__ import annotations

from dataclasses import dataclass

from sensors.imu_simulator import ImuSample


@dataclass(frozen=True)
class FilteredImuSample:
    """Filtered IMU output for accel and gyro vectors."""

    accel: tuple[float, float, float]
    gyro: tuple[float, float, float]


class ScalarEma:
    """EMA smoother for a single scalar signal."""

    def __init__(self, alpha: float = 0.2) -> None:
        self._alpha = EmaFilter._validate_alpha(alpha)
        self._state: float | None = None

    @property
    def alpha(self) -> float:
        return self._alpha

    def set_alpha(self, alpha: float) -> None:
        self._alpha = EmaFilter._validate_alpha(alpha)

    def update(self, value: float) -> float:
        if self._state is None:
            self._state = value
            return value
        self._state = (self._alpha * value) + ((1.0 - self._alpha) * self._state)
        return self._state


class EmaFilter:
    """Apply EMA smoothing independently to accel and gyro channels."""

    def __init__(self, alpha: float = 0.2) -> None:
        self._alpha = self._validate_alpha(alpha)
        self._accel_state: tuple[float, float, float] | None = None
        self._gyro_state: tuple[float, float, float] | None = None

    @property
    def alpha(self) -> float:
        """Return the current EMA alpha value."""
        return self._alpha

    def set_alpha(self, alpha: float) -> None:
        """Update EMA alpha at runtime."""
        self._alpha = self._validate_alpha(alpha)

    def update(self, sample: ImuSample) -> FilteredImuSample:
        """Update EMA state with a new IMU sample and return filtered output."""
        self._accel_state = self._ema_vector(self._accel_state, sample.accel)
        self._gyro_state = self._ema_vector(self._gyro_state, sample.gyro)
        return FilteredImuSample(accel=self._accel_state, gyro=self._gyro_state)

    @staticmethod
    def _validate_alpha(alpha: float) -> float:
        if not 0.0 < alpha <= 1.0:
            raise ValueError("alpha must be in (0.0, 1.0].")
        return alpha

    def _ema_vector(
        self,
        previous: tuple[float, float, float] | None,
        current: tuple[float, float, float],
    ) -> tuple[float, float, float]:
        if previous is None:
            return current
        a = self._alpha
        return tuple(
            (a * cur) + ((1.0 - a) * prev) for cur, prev in zip(current, previous)
        )
