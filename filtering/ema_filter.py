"""Backward-compatible import path for IMU EMA types.

Implementation lives in ``filtering.filters``. Import from there for new code.
"""

from filtering.filters import EmaFilter, FilteredImuSample, ScalarEma

__all__ = ["EmaFilter", "FilteredImuSample", "ScalarEma"]
