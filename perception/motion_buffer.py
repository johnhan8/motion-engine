from collections import deque

class MotionBuffer:
    def __init__(self, maxlen=30):
        self.buffer = deque(maxlen=maxlen)

    def add(self, features):
        if features:
            self.buffer.append(features)

    def get_sequence(self):
        if len(self.buffer) < 10:
            return None
        return list(self.buffer)
