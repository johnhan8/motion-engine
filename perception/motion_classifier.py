def classify_motion(sequence):

    if not sequence or len(sequence) < 10:
        return None

    last = sequence[-1]

    # -------------------------
    # PRIORITY RULES (IMPORTANT)
    # -------------------------

    # 1. Squat detection (highest priority)
    if last.get("knee_angle") and last["knee_angle"] < 120:
        return "Squats"

    # 2. Arm raise
    if last.get("shoulder_y") and last.get("elbow_angle"):
        if last["elbow_angle"] > 150:
            return "Arm Raises"

    # 3. Bicep curl (lowest priority)
    if last.get("elbow_angle") and last["elbow_angle"] < 70:
        return "Bicep Curls"

    return None
