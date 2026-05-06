from perception.landmarks import get_point
from perception.geometry import calculate_angle


def left_knee_angle_deg(landmarks):
    """Primary knee angle for the left kinematic chain (matches feature extraction defaults)."""

    hip = get_point(landmarks, "left_hip")
    knee = get_point(landmarks, "left_knee")
    ankle = get_point(landmarks, "left_ankle")

    return calculate_angle(hip, knee, ankle)


def left_elbow_angle_deg(landmarks):
    """Primary elbow angle for the left kinematic chain (matches feature extraction defaults)."""

    shoulder = get_point(landmarks, "left_shoulder")
    elbow = get_point(landmarks, "left_elbow")
    wrist = get_point(landmarks, "left_wrist")

    return calculate_angle(shoulder, elbow, wrist)


def right_knee_angle_deg(landmarks):
    """Right knee angle for the right kinematic chain."""

    hip = get_point(landmarks, "right_hip")
    knee = get_point(landmarks, "right_knee")
    ankle = get_point(landmarks, "right_ankle")

    return calculate_angle(hip, knee, ankle)


def right_elbow_angle_deg(landmarks):
    """Right elbow angle for the right kinematic chain."""

    shoulder = get_point(landmarks, "right_shoulder")
    elbow = get_point(landmarks, "right_elbow")
    wrist = get_point(landmarks, "right_wrist")

    return calculate_angle(shoulder, elbow, wrist)


def mean_knee_angle_deg(landmarks):
    """Average left/right knee angle."""

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
