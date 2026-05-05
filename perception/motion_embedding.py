import numpy as np

class MotionEmbedding:
    def __init__(self):
        self.window = []

    def update(self, features):
        if features is None:
            return None

        vec = np.array([
            features["elbow_angle"],
            features["knee_angle"],
            features["shoulder_y"],
            features["hip_y"],
        ])

        self.window.append(vec)

        if len(self.window) > 30:
            self.window.pop(0)

        return self.get_embedding()

    def get_embedding(self):
        if len(self.window) < 10:
            return None

        seq = np.array(self.window)

        return {
            "mean": np.mean(seq, axis=0),
            "std": np.std(seq, axis=0),
            "trajectory": seq[-1] - seq[0],   # motion direction
        }
