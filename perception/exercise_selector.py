class ExerciseSelector:
    def __init__(self):
        self.current = "Arm Raises"
        self.last_switch = 0

    def update(self, scores, frame_count):

        if scores is None:
            return self.current

        ranked = {
            "Squats": scores["squat_score"],
            "Bicep Curls": scores["curl_score"],
            "Arm Raises": scores["raise_score"],
        }

        best = max(ranked, key=ranked.get)

        best_score = ranked[best]
        second_best = sorted(ranked.values())[-2]

        # -----------------------------
        # confidence margin (IMPORTANT)
        # -----------------------------
        margin = best_score - second_best

        # require separation between classes
        if margin < 0.5:
            return self.current

        # stability gate
        if frame_count - self.last_switch > 30:
            self.current = best
            self.last_switch = frame_count

        return self.current
