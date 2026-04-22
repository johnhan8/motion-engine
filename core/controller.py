# ============================================================
# Exercise Controller
# Handles current exercise state + switching
# core/controller.py
# ============================================================

class ExerciseController:
    def __init__(self):
        self.current = "Squats"

    def get_current(self):
        return self.current

    def set(self, exercise_name):
        self.current = exercise_name
