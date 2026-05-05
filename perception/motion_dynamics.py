import numpy as np

class MotionDynamics:
    def __init__(self):
        self.prev = None

    def update(self, features):
        if features is None:
            return None

        if self.prev is None:
            self.prev = features
            return {
                "hip_vel": 0,
                "knee_vel": 0,
                "elbow_vel": 0
            }

        dyn = {
            "hip_vel": features["hip_y"] - self.prev["hip_y"],
            "knee_vel": features["knee_angle"] - self.prev["knee_angle"],
            "elbow_vel": features["elbow_angle"] - self.prev["elbow_angle"],
        }

        self.prev = features
        return dyn
