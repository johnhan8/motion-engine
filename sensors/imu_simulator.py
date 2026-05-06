"""IMU simulator for synthetic accelerometer and gyroscope data.

**STABLE (IMU path):** ``ImuSimulator.read()`` -> ``ImuSample`` with 3-axis
accel and gyro is the supported sensor output contract for the IMU pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
import random


@dataclass(frozen=True)
class ImuSample:
    """Single IMU reading with accel and gyro vectors."""

    accel: tuple[float, float, float]
    gyro: tuple[float, float, float]


class ImuSimulator:
    """Generate noisy IMU samples with optional drift and motion patterns."""

    def __init__(
        self,
        accel_baseline: tuple[float, float, float] = (0.0, 0.0, 9.81),
        gyro_baseline: tuple[float, float, float] = (0.0, 0.0, 0.0),
        accel_noise_std: float = 0.25,
        gyro_noise_std: float = 0.02,
        accel_bias_drift_per_sec: float = 0.01,
        gyro_bias_drift_per_sec: float = 0.001,
        motion_pattern: str = "sinusoidal",
        sample_rate_hz: float = 50.0,
        sinusoid_hz: float = 0.6,
        sinusoid_amplitude: float = 0.8,
        random_walk_std: float = 0.03,
    ) -> None:
        """Initialize simulator parameters.

        Args:
            accel_baseline: Static acceleration baseline (m/s^2).
            gyro_baseline: Static angular velocity baseline (rad/s).
            accel_noise_std: Gaussian acceleration noise stddev.
            gyro_noise_std: Gaussian gyroscope noise stddev.
            accel_bias_drift_per_sec: Bias drift scale for accel channels.
            gyro_bias_drift_per_sec: Bias drift scale for gyro channels.
            motion_pattern: One of ``none``, ``sinusoidal``, or ``random_walk``.
            sample_rate_hz: Simulator sampling frequency.
            sinusoid_hz: Frequency for sinusoidal mode.
            sinusoid_amplitude: Amplitude for sinusoidal mode.
            random_walk_std: Random walk step stddev for random-walk mode.
        """
        self._accel_baseline = accel_baseline
        self._gyro_baseline = gyro_baseline
        self._accel_noise_std = accel_noise_std
        self._gyro_noise_std = gyro_noise_std
        self._accel_bias_drift_per_sec = accel_bias_drift_per_sec
        self._gyro_bias_drift_per_sec = gyro_bias_drift_per_sec
        self._motion_pattern = motion_pattern
        self._dt = 1.0 / sample_rate_hz
        self._sinusoid_hz = sinusoid_hz
        self._sinusoid_amplitude = sinusoid_amplitude
        self._random_walk_std = random_walk_std
        self._t = 0.0
        self._accel_bias = [0.0, 0.0, 0.0]
        self._gyro_bias = [0.0, 0.0, 0.0]
        self._walk_state = [0.0, 0.0, 0.0]

    def read(self) -> ImuSample:
        """Return one noisy IMU sample."""
        self._t += self._dt
        self._update_biases()
        motion = self._motion_component()

        accel = tuple(
            axis + self._accel_bias[i] + motion[i] + random.gauss(0.0, self._accel_noise_std)
            for i, axis in enumerate(self._accel_baseline)
        )
        gyro = tuple(
            axis + self._gyro_bias[i] + 0.1 * motion[i] + random.gauss(0.0, self._gyro_noise_std)
            for i, axis in enumerate(self._gyro_baseline)
        )
        return ImuSample(accel=accel, gyro=gyro)

    def _update_biases(self) -> None:
        accel_step = self._accel_bias_drift_per_sec * self._dt
        gyro_step = self._gyro_bias_drift_per_sec * self._dt
        for i in range(3):
            self._accel_bias[i] += random.gauss(0.0, accel_step)
            self._gyro_bias[i] += random.gauss(0.0, gyro_step)

    def _motion_component(self) -> tuple[float, float, float]:
        if self._motion_pattern == "none":
            return (0.0, 0.0, 0.0)
        if self._motion_pattern == "random_walk":
            for i in range(3):
                self._walk_state[i] += random.gauss(0.0, self._random_walk_std)
            return tuple(self._walk_state)

        phase = 2.0 * math.pi * self._sinusoid_hz * self._t
        return (
            self._sinusoid_amplitude * math.sin(phase),
            0.5 * self._sinusoid_amplitude * math.sin(phase + math.pi / 3.0),
            0.25 * self._sinusoid_amplitude * math.sin(phase + 2.0 * math.pi / 3.0),
        )
