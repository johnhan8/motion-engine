import numpy as np

from perception.temporal.window import RollingWindow


class MotionScorer:
    def __init__(self, maxlen=20, min_history=10):
        self._window = RollingWindow(maxlen)
        self._min_history = min_history

    def safe(self, features, key, default=0.0):
        return features.get(key, default)

    def update(self, features):
        if features is None:
            return None

        vec = np.array(
            [
                self.safe(features, "elbow_norm"),
                self.safe(features, "knee_norm"),
                self.safe(features, "hip_to_knee"),
                self.safe(features, "shoulder_to_hip"),
            ]
        )

        self._window.append(vec)
        return self.score()

    def score(self):
        if len(self._window) < self._min_history:
            return None

        seq = np.array(self._window.as_list())
        delta = np.diff(seq, axis=0)
        energy = np.sum(delta**2, axis=0)

        return {
            "curl_score": float(energy[0]),
            "squat_score": float(energy[2]),
            "raise_score": float(energy[3]),
        }
