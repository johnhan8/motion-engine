# ============================================================
# MotionLoop - MediaPipe Version  (Clean)
# Real-time pose tracking + skeleton + rep counting
# 2026.04.21    main.py
# Pipeline: Camera → Pose Detection → Landmark Extraction → Engine → State → UI
# ============================================================
  

import cv2

from core.state import SessionState
from core.controller import ExerciseController
from core.engine import run_engine

from perception.detector import PoseDetector  # ✅ NEW

from ui.overlay import draw_overlay
from session.logger import SessionLogger

controller = ExerciseController()


def main():
    state = SessionState()
    logger = SessionLogger()

    cap = cv2.VideoCapture(0)
    pose_detector = PoseDetector()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # ----------------------
        # Pose detection
        # ----------------------
        landmarks = pose_detector.get_landmarks(frame)

        # ----------------------
        # Keyboard input
        # ----------------------
        key = cv2.waitKey(1) & 0xFF

        if key == ord('s'):
            controller.set("Squats")
        elif key == ord('b'):
            controller.set("Bicep Curls")
        elif key == ord('a'):
            controller.set("Arm Raises")
        elif key == ord('p'):
            controller.set("Pushups")
        elif key == ord('t'):
            controller.set("Strict Press")
        elif key == 27:
            break

        # ----------------------
        # Engine
        # ----------------------
        exercise = controller.get_current()
        state = run_engine(landmarks, state, exercise)

        logger.log(state, exercise)

        # ----------------------
        # UI Overlay
        # ----------------------
        frame = pose_detector.draw_landmarks(frame)
        frame = draw_overlay(frame, state, controller)

        cv2.imshow("KineticAI", frame)

    cap.release()
    cv2.destroyAllWindows()

    logger.save()
    print(state.__dict__)


if __name__ == "__main__":
    main()
