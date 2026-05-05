from perception.landmarks import get_point
from perception.geometry import calculate_angle

def extract_features(landmarks):
    if not landmarks:
        return None

    try:
        shoulder = get_point(landmarks, "left_shoulder")
        elbow = get_point(landmarks, "left_elbow")
        wrist = get_point(landmarks, "left_wrist")

        hip = get_point(landmarks, "left_hip")
        knee = get_point(landmarks, "left_knee")
        ankle = get_point(landmarks, "left_ankle")

        # angles
        elbow_angle = calculate_angle(shoulder, elbow, wrist)
        knee_angle = calculate_angle(hip, knee, ankle)

        # ----------------------------
        # NORMALIZED FEATURES (0–1 SCALE)
        # ----------------------------

        elbow_norm = elbow_angle / 180.0
        knee_norm = knee_angle / 180.0

        hip_to_knee = abs(hip[1] - knee[1])
        shoulder_to_hip = abs(shoulder[1] - hip[1])

        return {
            "elbow_angle": elbow_angle,
            "knee_angle": knee_angle,

            "elbow_norm": elbow_norm,
            "knee_norm": knee_norm,
            "hip_to_knee": hip_to_knee,
            "shoulder_to_hip": shoulder_to_hip,

            # keep raw signals for debugging
            "hip_y": hip[1],
            "shoulder_y": shoulder[1],
        }

    except:
        return None
