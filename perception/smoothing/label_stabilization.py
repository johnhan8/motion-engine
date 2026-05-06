from collections import Counter, deque


class LabelStabilizer:
    """Majority-vote stabilization for discrete exercise labels over time."""

    def __init__(self, maxlen: int = 20, min_votes: int = 10, majority: float = 0.65):
        self.buffer = deque(maxlen=maxlen)
        self._min_votes = min_votes
        self._majority = majority

    def update(self, label):
        if label:
            self.buffer.append(label)

    def stable(self):
        if len(self.buffer) < self._min_votes:
            return None

        counts = Counter(self.buffer)
        label, freq = counts.most_common(1)[0]

        if freq / len(self.buffer) > self._majority:
            return label

        return None

__all__ = ["LabelStabilizer"]
