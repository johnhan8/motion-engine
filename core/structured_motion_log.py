"""Buffered structured (JSON Lines) logging for IMU motion ticks.

Uses only the standard library. Batched writes limit per-tick I/O cost.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from filtering.filters import FilteredImuSample
from sensors.imu_simulator import ImuSample


def motion_tick_to_dict(
    index: int,
    elapsed_s: float,
    raw: ImuSample,
    filtered: FilteredImuSample,
) -> dict[str, Any]:
    """Structured record for one timestep (raw + filtered IMU)."""
    return {
        "index": index,
        "time_s": elapsed_s,
        "raw": {
            "accel": [raw.accel[0], raw.accel[1], raw.accel[2]],
            "gyro": [raw.gyro[0], raw.gyro[1], raw.gyro[2]],
        },
        "filtered": {
            "accel": [
                filtered.accel[0],
                filtered.accel[1],
                filtered.accel[2],
            ],
            "gyro": [filtered.gyro[0], filtered.gyro[1], filtered.gyro[2]],
        },
    }


class JsonlMotionLogger:
    """Append one JSON object per line; flush in batches to reduce write overhead.

    Tick path only builds a small dict; ``json.dumps`` runs on flush batches so the
    main loop avoids serialization work every sample when the buffer is not full.
    """

    def __init__(
        self,
        output_path: str,
        *,
        flush_every: int = 64,
    ) -> None:
        self._path = Path(output_path)
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._fh = self._path.open("w", encoding="utf-8", newline="\n")
        self._flush_every = max(1, int(flush_every))
        self._pending: list[dict[str, Any]] = []

    def log(self, index: int, elapsed_s: float, raw: ImuSample, filtered: FilteredImuSample) -> None:
        self._pending.append(motion_tick_to_dict(index, elapsed_s, raw, filtered))
        if len(self._pending) >= self._flush_every:
            self._flush_buffer()

    def _flush_buffer(self) -> None:
        if not self._pending:
            return
        lines = [
            json.dumps(rec, separators=(",", ":")) for rec in self._pending
        ]
        self._fh.write("\n".join(lines) + "\n")
        self._pending.clear()

    def close(self) -> None:
        self._flush_buffer()
        self._fh.close()

    @property
    def path(self) -> Path:
        return self._path


class FanOutOutputLogger:
    """Forward each tick to multiple sinks (e.g. CSV + JSONL)."""

    def __init__(self, *loggers: Any) -> None:
        self._loggers = list(loggers)

    def log(self, index: int, elapsed_s: float, raw: ImuSample, filtered: FilteredImuSample) -> None:
        for lg in self._loggers:
            lg.log(index, elapsed_s, raw, filtered)

    def close(self) -> None:
        for lg in self._loggers:
            closer = getattr(lg, "close", None)
            if closer is not None:
                closer()
