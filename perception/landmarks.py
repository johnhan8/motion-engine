# perception/landmarks.py
# 


LANDMARKS = {
    "nose": 0,
    "left_shoulder": 11,
    "right_shoulder": 12,
    "left_elbow": 13,
    "right_elbow": 14,
    "left_wrist": 15,
    "right_wrist": 16,
    "left_hip": 23,
    "right_hip": 24,
    "left_knee": 25,
    "right_knee": 26,
    "left_ankle": 27,
    "right_ankle": 28,
}

def get_point(landmarks, name):
    idx = LANDMARKS[name]
    lm = landmarks[idx]

    # FIX: support both MediaPipe object AND tuple formats
    if hasattr(lm, "x"):
        return [lm.x, lm.y, getattr(lm, "visibility", 1.0)]

    # fallback if tuple/list
    return [lm[0], lm[1], 1.0]
