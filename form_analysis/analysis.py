# form_analysis/analysis.py

import numpy as np

def form_warnings(knee_angle, elbow_angle, hip_y, shoulder_y):
    warnings=[]
    if knee_angle < 150: warnings.append("Knees collapsing inward")
    if hip_y < shoulder_y-0.05: warnings.append("Torso leaning forward")
    if elbow_angle < 40: warnings.append("Elbow too flexed")
    return warnings

# Rep quality feedback 
def evaluate_squat(knee_angle):
    if knee_angle > 120:
        return "Too shallow"
    elif knee_angle > 90:
        return "Decent"
    else:
        return "Good rep"

