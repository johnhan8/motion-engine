# core/engine.py

from core.registry import EXERCISE_MAP

def run_engine(landmarks, state, exercise):
    fn = EXERCISE_MAP.get(exercise)
    if fn:
        return fn(landmarks, state)
    return state
