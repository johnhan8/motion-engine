"""Tests for IMU pipeline timing and logging contracts."""

from __future__ import annotations

import unittest

from core.pipeline import ImuPipeline


class ImuPipelineSampleRateTests(unittest.TestCase):
    def test_simulator_dt_matches_pipeline_sample_rate(self) -> None:
        """Simulator internal time must advance at the same rate as pipeline pacing."""
        rate_hz = 100.0
        pipeline = ImuPipeline(sample_rate_hz=rate_hz, motion_pattern="sinusoidal")
        n = 50
        for _ in range(n):
            pipeline.step()
        expected_t = n / rate_hz
        self.assertAlmostEqual(pipeline.sensor._t, expected_t, places=9)


if __name__ == "__main__":
    unittest.main()
