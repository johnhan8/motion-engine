# ----------------------
# exercises/squat.py
# ----------------------


from perception.landmarks import get_point
from perception.geometry import calculate_angle


# ----------------------
# Tuned thresholds (more forgiving)
# ----------------------
DOWN_ANGLE = 125   # easier to enter squat
UP_ANGLE = 150     # standing threshold

MIN_HOLD_FRAMES = 5
MIN_REP_GAP_FRAMES = 8


def update_squat(landmarks, state):

    if not landmarks:
        return state

    hip_l = get_point(landmarks, "left_hip")
    hip_r = get_point(landmarks, "right_hip")

    knee_l = get_point(landmarks, "left_knee")
    knee_r = get_point(landmarks, "right_knee")

    ankle_l = get_point(landmarks, "left_ankle")
    ankle_r = get_point(landmarks, "right_ankle")

    # Visibility check
    if min(hip_l[2], hip_r[2], knee_l[2], knee_r[2], ankle_l[2], ankle_r[2]) < 0.6:
        return state

    # ----------------------
    # Compute features
    # ----------------------
    hip_y = (hip_l[1] + hip_r[1]) / 2

    angle_l = calculate_angle(hip_l, knee_l, ankle_l)
    angle_r = calculate_angle(hip_r, knee_r, ankle_r)
    knee_angle = (angle_l + angle_r) / 2

    # ----------------------
    # Init
    # ----------------------
    if state.squat_prev_hip_y is None:
        state.squat_prev_hip_y = hip_y
        return state

    # ----------------------
    # Motion direction
    # ----------------------
    velocity = hip_y - state.squat_prev_hip_y

    going_down = velocity > 0.002
    going_up = velocity < -0.002

    # ----------------------
    # STATE MACHINE (IMPROVED)
    # ----------------------

    # Enter bottom
    if state.squat_stage == "up":
        if knee_angle < DOWN_ANGLE and going_down:
            state.squat_stage = "down"

    # Count rep on upward drive
    elif state.squat_stage == "down":
        if knee_angle > UP_ANGLE and going_up:
            state.squat_reps += 1
            state.squat_stage = "up"

    # ----------------------
    # Update memory
    # ----------------------
    state.squat_prev_hip_y = hip_y

    return state
