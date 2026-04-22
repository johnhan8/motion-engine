# ============================================================
# exercises/arm_raise.py (FIXED BOTH SIDES)
# ============================================================

from perception.landmarks import get_point
from perception.geometry import calculate_angle


UP_ANGLE = 60
DOWN_ANGLE = 120


def update_arm_raise(landmarks, state):
    if landmarks is None:
        return state

    # LEFT side
    shoulder_l = get_point(landmarks, "left_shoulder")
    elbow_l = get_point(landmarks, "left_elbow")
    hip_l = get_point(landmarks, "left_hip")

    # RIGHT side
    shoulder_r = get_point(landmarks, "right_shoulder")
    elbow_r = get_point(landmarks, "right_elbow")
    hip_r = get_point(landmarks, "right_hip")

    # visibility check
    if min(shoulder_l[2], elbow_l[2], hip_l[2],
           shoulder_r[2], elbow_r[2], hip_r[2]) < 0.5:
        return state

    # angles
    angle_l = calculate_angle(hip_l, shoulder_l, elbow_l)
    angle_r = calculate_angle(hip_r, shoulder_r, elbow_r)

    angle = min(angle_l, angle_r)  # KEY FIX: whichever arm is active

    # state machine
    if angle < UP_ANGLE:
        state.raise_stage = "up"

    elif angle > DOWN_ANGLE and state.raise_stage == "up":
        state.raise_reps += 1
        state.raise_stage = "down"

    return state
