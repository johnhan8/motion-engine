from collections import deque, Counter

class ExerciseRouter:
    def __init__(self):
        self.buffer = deque(maxlen=30)

        self.current_exercise = None
        self.last_switch_frame = 0
        self.frame_count = 0

        # stability tuning
        self.min_confidence = 0.60
        self.switch_cooldown = 90  # ~3 sec at 30fps
        self.lock_frames = 60      # must persist before switch allowed

    def update(self, prediction):
        self.frame_count += 1

        if prediction:
            self.buffer.append(prediction)

    def get_stable(self):

        if len(self.buffer) < 15:
            return self.current_exercise

        counts = Counter(self.buffer)
        candidate, freq = counts.most_common(1)[0]

        confidence = freq / len(self.buffer)

        # ----------------------------
        # INIT STATE
        # ----------------------------
        if self.current_exercise is None:
            if confidence > self.min_confidence:
                self.current_exercise = candidate
                self.last_switch_frame = self.frame_count
            return self.current_exercise

        # ----------------------------
        # STABILITY CHECK (HYSTERESIS)
        # ----------------------------
        if candidate == self.current_exercise:
            return self.current_exercise

        # require strong evidence before switching
        if confidence > 0.75:
            if self.frame_count - self.last_switch_frame > self.switch_cooldown:
                self.current_exercise = candidate
                self.last_switch_frame = self.frame_count

        return self.current_exercise
