from perception.landmarks import get_point
from perception.geometry import calculate_angle


def update_bicep_curl(landmarks, state):
    if landmarks is None or len(landmarks) == 0:
        return state

    shoulder_l = get_point(landmarks, "left_shoulder")
    elbow_l = get_point(landmarks, "left_elbow")
    wrist_l = get_point(landmarks, "left_wrist")

    shoulder_r = get_point(landmarks, "right_shoulder")
    elbow_r = get_point(landmarks, "right_elbow")
    wrist_r = get_point(landmarks, "right_wrist")


    angle_l = calculate_angle(shoulder_l, elbow_l, wrist_l)
    angle_r = calculate_angle(shoulder_r, elbow_r, wrist_r)

    elbow_angle = (angle_l + angle_r) / 2


    # Curl logic
    if elbow_angle > 160:
        state.curl_stage = "down"
    if elbow_angle < 50 and state.curl_stage == "down":
        state.curl_stage = "up"
        state.curl_reps += 1

    return state
