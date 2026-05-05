import numpy as np

class MotionScorer:
    def __init__(self):
        self.history = []

    def safe(self, features, key, default=0.0):
        return features.get(key, default)

    def update(self, features):
        if features is None:
            return None

        vec = np.array([
            self.safe(features, "elbow_norm"),
            self.safe(features, "knee_norm"),
            self.safe(features, "hip_to_knee"),
            self.safe(features, "shoulder_to_hip"),
        ])

        self.history.append(vec)

        if len(self.history) > 20:
            self.history.pop(0)

        return self.score()

    def score(self):
        if len(self.history) < 10:
            return None

        seq = np.array(self.history)
        delta = np.diff(seq, axis=0)

        energy = np.sum(delta ** 2, axis=0)

        return {
            "curl_score": float(energy[0]),
            "squat_score": float(energy[2]),
            "raise_score": float(energy[3]),
        }
