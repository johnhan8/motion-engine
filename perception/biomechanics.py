from perception.landmarks import get_point
from perception.geometry import calculate_angle


def knee_angle(landmarks):
    hip_l = get_point(landmarks, "left_hip")
    knee_l = get_point(landmarks, "left_knee")
    ankle_l = get_point(landmarks, "left_ankle")

    hip_r = get_point(landmarks, "right_hip")
    knee_r = get_point(landmarks, "right_knee")
    ankle_r = get_point(landmarks, "right_ankle")

    return (
        calculate_angle(hip_l, knee_l, ankle_l) +
        calculate_angle(hip_r, knee_r, ankle_r)
    ) / 2


def elbow_angle(landmarks):
    shoulder = get_point(landmarks, "right_shoulder")
    elbow = get_point(landmarks, "right_elbow")
    wrist = get_point(landmarks, "right_wrist")

    return calculate_angle(shoulder, elbow, wrist)
