from perception.temporal.derivatives import KeyedDerivativeTracker

_DEFAULT_KEYS = {
    "hip_y": "hip_vel",
    "knee_angle": "knee_vel",
    "elbow_angle": "elbow_vel",
}


class MotionDynamics:
    def __init__(self):
        self._tracker = KeyedDerivativeTracker(_DEFAULT_KEYS)

    def update(self, features):
        return self._tracker.update(features)
