# ============================================================
# ADD GLOBAL NOISE FILTER  
# Problem: MediaPipe jitter causes false transitions
# Solution: ADD smoothing helper
# ============================================================

class ExponentialSmoother:
    def __init__(self, alpha=0.7):
        self.alpha = alpha
        self.prev = None

    def update(self, value):
        if self.prev is None:
            self.prev = value
            return value

        self.prev = self.alpha * self.prev + (1 - self.alpha) * value
        return self.prev
