from __future__ import annotations

from typing import Any, Dict, Mapping, Optional


class Kinematics:
    """Frame-to-frame velocity for every numeric feature key."""

    def __init__(self):
        self.prev: Dict[str, float] = {}

    def update(self, features: Optional[Mapping[str, Any]]):
        if not features:
            return None

        out: Dict[str, float] = {}

        for k, v in features.items():
            if not isinstance(v, (int, float)):
                continue
            fv = float(v)
            if k in self.prev:
                out[k + "_vel"] = fv - self.prev[k]
            else:
                out[k + "_vel"] = 0.0
            self.prev[k] = fv

        return out


class KeyedDerivativeTracker:
    """Derivatives for a fixed mapping of feature key -> output velocity name."""

    def __init__(self, key_to_output: Mapping[str, str]):
        self._key_to_output = dict(key_to_output)
        self.prev: Optional[Dict[str, float]] = None

    def update(self, features: Optional[Mapping[str, Any]]):
        if features is None:
            return None

        if self.prev is None:
            self.prev = {k: float(features[k]) for k in self._key_to_output}
            return {out: 0 for out in self._key_to_output.values()}

        out: Dict[str, float] = {}
        for feat_key, out_key in self._key_to_output.items():
            cur = float(features[feat_key])
            out[out_key] = cur - self.prev[feat_key]
            self.prev[feat_key] = cur
        return out
