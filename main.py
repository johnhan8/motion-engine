import cv2

from core.state import SessionState
from core.controller import ExerciseController
from core.engine import run_engine

from perception.detector import PoseDetector
from perception.features import extract_features

from perception.motion_buffer import MotionBuffer
from perception.motion_embedder import MotionEmbedder
from perception.motion_model import MotionModel
from perception.motion_smoother import MotionSmoother

from ui.overlay import draw_overlay
from session.logger import SessionLogger


controller = ExerciseController()


def main():
    state = SessionState()
    logger = SessionLogger()

    cap = cv2.VideoCapture(0)
    pose_detector = PoseDetector()

    buffer = MotionBuffer()
    embedder = MotionEmbedder()
    model = MotionModel()
    smoother = MotionSmoother()

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # ----------------------
        # Pose detection
        # ----------------------
        landmarks = pose_detector.get_landmarks(frame)

        # ----------------------
        # Feature extraction
        # ----------------------
        features = extract_features(landmarks)
        buffer.add(features)

        sequence = buffer.get_sequence()

        # ----------------------
        # Motion intelligence pipeline
        # ----------------------
        if sequence:
            embedding = embedder.encode(sequence)
            if embedding is None: 
                continue
            label, scores = model.predict(embedding)

            smoother.update(label)
            stable_exercise = smoother.stable()

            if stable_exercise:
                controller.set(stable_exercise)

        exercise = controller.get_current()

        # ----------------------
        # Rep engine
        # ----------------------
        state = run_engine(landmarks, state, exercise)

        logger.log(state, exercise)

        # ----------------------
        # UI
        # ----------------------
        frame = pose_detector.draw_landmarks(frame)
        frame = draw_overlay(frame, state, controller)

        cv2.imshow("KineticAI", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

    logger.save()
    print(state.__dict__)


if __name__ == "__main__":
    main()
