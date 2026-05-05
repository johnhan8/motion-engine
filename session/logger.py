# session/logger.py

import csv
import time

class SessionLogger:
    def __init__(self):
        self.rows = []
        self.start_time = time.time()

    def log(self, state, exercise):
        self.rows.append([
            time.time() - self.start_time,
            exercise,
            state.squat_reps,
            state.curl_reps,
            state.raise_reps
        ])

    def save(self, path="data/session.csv"):
        with open(path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["time", "exercise", "squats", "curls", "raises"])
            writer.writerows(self.rows)
