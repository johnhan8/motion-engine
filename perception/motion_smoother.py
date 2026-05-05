from collections import deque, Counter

class MotionSmoother:
    def __init__(self):
        self.buffer = deque(maxlen=20)

    def update(self, label):
        if label:
            self.buffer.append(label)

    def stable(self):
        if len(self.buffer) < 10:
            return None

        counts = Counter(self.buffer)
        label, freq = counts.most_common(1)[0]

        if freq / len(self.buffer) > 0.65:
            return label

        return None
