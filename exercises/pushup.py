from perception.landmarks import get_point
from perception.geometry import calculate_angle


def update_pushup(landmarks, state):
    if landmarks is None or len(landmarks) == 0:
        return state

    shoulder = get_point(landmarks, "left_shoulder")
    elbow = get_point(landmarks, "left_elbow")
    wrist = get_point(landmarks, "left_wrist")

    angle = calculate_angle(shoulder, elbow, wrist)

    if angle > 160:
        state.pushup_stage = "up"
    if angle < 90 and state.pushup_stage == "up":
        state.pushup_stage = "down"
        state.pushup_reps += 1

    return state
