# ============================================================
# scripts/plot_session_v5_enhanced.py
# ENHANCED SESSION ANALYSIS & PLOTTING
# For AI PT Assistant v5 (MoveNet)
# Features:
# - Moving average smoothing for angles
# - Visual markers for rep thresholds
# - Per-exercise rep and joint angle plots
# ============================================================

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ----------------------
# Load CSV
# ----------------------
file_path = "session_v5_data.csv"
df = pd.read_csv(file_path)
time_sec = df['Time']

# ----------------------
# Smooth joint angles using moving average
# ----------------------
def moving_average(x, w=5):
    return np.convolve(x, np.ones(w)/w, mode='same')

knee_smooth = moving_average(df['Knee'])
shoulder_smooth = moving_average(df['Shoulder'])
elbow_smooth = moving_average(df['Elbow'])

# ----------------------
# Plot Rep Counts with Thresholds
# ----------------------
plt.figure(figsize=(14,6))
exercises = ['Squats','ArmRaises','BicepCurls','StrictPress']
thresholds = {'Squats':100, 'ArmRaises':150, 'BicepCurls':40, 'StrictPress':170}  # example thresholds
colors = {'Squats':'green','ArmRaises':'blue','BicepCurls':'orange','StrictPress':'red'}

for ex in exercises:
    reps = df[ex]
    plt.plot(time_sec, reps, label=ex, color=colors[ex])
    
    # show rep threshold marker line
    plt.hlines(thresholds[ex], xmin=time_sec.min(), xmax=time_sec.max(),
               colors=colors[ex], linestyles='dashed', alpha=0.3)

plt.xlabel("Time (s)")
plt.ylabel("Reps")
plt.title("Exercise Reps Over Time with Thresholds")
plt.legend()
plt.grid(True)
plt.show()

# ----------------------
# Plot Smoothed Joint Angles with Thresholds
# ----------------------
plt.figure(figsize=(14,6))
plt.plot(time_sec, knee_smooth, label='Knee Angle (smoothed)', color='green')
plt.plot(time_sec, shoulder_smooth, label='Shoulder Angle (smoothed)', color='blue')
plt.plot(time_sec, elbow_smooth, label='Elbow Angle (smoothed)', color='red')

# Example threshold lines for rep detection
plt.hlines([100,150,40,170], xmin=time_sec.min(), xmax=time_sec.max(),
           colors=['green','blue','red','red'], linestyles='dotted', alpha=0.3,
           label='Rep Thresholds')

plt.xlabel("Time (s)")
plt.ylabel("Angle (degrees)")
plt.title("Smoothed Joint Angles with Rep Thresholds")
plt.legend()
plt.grid(True)
plt.show()

# ----------------------
# Print Warnings
# ----------------------
warnings = df['Warnings']
all_warnings = [w for w in warnings if w != '']
if all_warnings:
    print("Warnings during session:")
    for w in all_warnings:
        print(w)
else:
    print("No warnings detected in session.")

