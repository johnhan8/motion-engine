from perception.temporal.window import RollingWindow


class MotionBuffer:
    def __init__(self, maxlen=30, min_sequence=10):
        self._window = RollingWindow(maxlen)
        self._min_sequence = min_sequence

    def add(self, features):
        if features:
            self._window.append(features)

    def get_sequence(self):
        if len(self._window) < self._min_sequence:
            return None
        return self._window.as_list()
