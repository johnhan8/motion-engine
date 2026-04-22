# core/registry.py

from exercises.squat import update_squat
from exercises.bicep_curl import update_bicep_curl
from exercises.arm_raise import update_arm_raise
from exercises.pushup import update_pushup
from exercises.strict_press import update_strict_press

EXERCISE_MAP = {
    "Squats": update_squat,
    "Bicep Curls": update_bicep_curl,
    "Arm Raises": update_arm_raise,
    "Pushups": update_pushup,
    "Strict Press": update_strict_press,
}
