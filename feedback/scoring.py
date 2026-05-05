# feedback/scoring.py
#

def squat_score(landmarks):
    return 0.0  # placeholder

def score_session(state):
    total = state.squat_reps + state.curl_reps + state.raise_reps

    consistency = min(1.0, total / 30)

    return {
        "volume_score": round(consistency, 2),
        "total_reps": total
    }

