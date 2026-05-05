import numpy as np

class MotionEmbedder:
    def __init__(self):
        # Define fixed feature order (VERY IMPORTANT)
        self.keys = [
            "elbow_norm",
            "knee_norm",
            "hip_to_knee",
            "shoulder_to_hip"
        ]

    def vectorize(self, features):
        # Convert dict → numeric vector
        return [features.get(k, 0.0) for k in self.keys]

    def encode(self, sequence):
        if not sequence or len(sequence) < 10:
            return None

        # ----------------------------
        # Convert sequence of dicts → matrix
        # ----------------------------
        seq = np.array([self.vectorize(f) for f in sequence])

        # ----------------------------
        # Temporal features
        # ----------------------------
        delta = np.diff(seq, axis=0)

        return {
            "mean": np.mean(seq, axis=0),
            "std": np.std(seq, axis=0),
            "delta": np.mean(delta, axis=0),
            "energy": np.sum(delta ** 2, axis=0),
        }
