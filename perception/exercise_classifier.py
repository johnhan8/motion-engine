def classify_exercise(features):
    if not features:
        return None

    knee = features["knee_angle"]
    elbow = features["elbow_angle"]

    # Squat detection
    if knee < 140:
        return "Squats"

    # Bicep curl detection
    if elbow < 60:
        return "Bicep Curls"

    # Arm raise detection
    if elbow > 150 and features["shoulder_y"] < features["hip_y"]:
        return "Arm Raises"

    return None
