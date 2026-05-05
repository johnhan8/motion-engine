import numpy as np

class Kinematics:
    def __init__(self):
        self.prev = {}

    def update(self, features):
        if not features:
            return None

        out = {}

        # store velocities
        for k, v in features.items():
            if k in self.prev:
                out[k + "_vel"] = v - self.prev[k]
            else:
                out[k + "_vel"] = 0.0

            self.prev[k] = v

        return out
