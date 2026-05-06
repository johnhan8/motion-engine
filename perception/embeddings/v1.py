from __future__ import annotations

from typing import Mapping, Optional

import numpy as np

from perception.temporal.window import RollingWindow

# Raw-ish feature order for rolling-window embeddings (v1).
RAW_EMBEDDING_COMPONENTS = ("elbow_angle", "knee_angle", "shoulder_y", "hip_y")

DEFAULT_MAXLEN = 30
DEFAULT_MINLEN = 10


class MotionEmbeddingV1:
    """Rolling-window embedding over raw angles and vertical positions."""

    def __init__(self, maxlen: int = DEFAULT_MAXLEN, minlen: int = DEFAULT_MINLEN):
        self._window = RollingWindow(maxlen)
        self._minlen = minlen

    def update(self, features: Optional[Mapping[str, float]]):
        if features is None:
            return None

        vec = np.array(
            [float(features[k]) for k in RAW_EMBEDDING_COMPONENTS],
            dtype=np.float64,
        )
        self._window.append(vec)
        return self.get_embedding()

    def get_embedding(self) -> Optional[dict]:
        if len(self._window) < self._minlen:
            return None

        seq = np.array(self._window.as_list())
        return {
            "version": 1,
            "mean": np.mean(seq, axis=0),
            "std": np.std(seq, axis=0),
            "trajectory": seq[-1] - seq[0],
        }
