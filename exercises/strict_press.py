from perception.landmarks import get_point
from perception.geometry import calculate_angle


def update_strict_press(landmarks, state):
    if landmarks is None or len(landmarks) == 0:
        return state

    shoulder = get_point(landmarks, "left_shoulder")
    elbow = get_point(landmarks, "left_elbow")
    wrist = get_point(landmarks, "left_wrist")

    angle = calculate_angle(shoulder, elbow, wrist)

    if angle > 160:
        state.press_stage = "up"
    if angle < 70 and state.press_stage == "up":
        state.press_stage = "down"
        state.press_reps += 1

    return state
