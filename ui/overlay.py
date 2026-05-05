#ui/overlay.py 

import cv2

def draw_overlay(frame, state, controller):

    exercise = controller.get_current()

    y = 30

    cv2.putText(frame, "KineticAI", (20, y),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (40,40,40), 2)
    y += 40

    cv2.putText(frame, f"Current: {exercise}", (20, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (40,40,40), 2)
    y += 40

    cv2.putText(frame, f"Squats: {state.squat_reps}", (20, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,0), 2)
    y += 30

    cv2.putText(frame, f"Curls: {state.curl_reps}", (20, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,0), 2)
    y += 30

    cv2.putText(frame, f"Raises: {state.raise_reps}", (20, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,0), 2)
    y += 40

    cv2.putText(frame, "[S] Squat  [B] Curl  [A] Raise  [ESC] Quit",
                (20, 460), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (180,180,180), 1)

    return frame
