# session/summary.py
#


def generate_summary(state):
    return {
        "Squats": state.squat_reps,
        "Curls": state.curl_reps,
        "Raises": state.raise_reps,
        "Total Reps": state.squat_reps + state.curl_reps + state.raise_reps
    }

def compute_score(state):
    return round(
        (state.squat_reps * 1.0 +
         state.curl_reps * 0.5 +
         state.raise_reps * 0.5),
        2
    )

