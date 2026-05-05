import numpy as np

PROTOTYPES = {
    "Bicep Curls": {
        "mean": np.array([60, 170, 0.5, 0.5]),
        "std":  np.array([20, 10, 0.05, 0.05]),
    },
    "Squats": {
        "mean": np.array([160, 90, 0.5, 0.3]),
        "std":  np.array([25, 25, 0.05, 0.1]),
    },
    "Arm Raises": {
        "mean": np.array([170, 170, 0.2, 0.5]),
        "std":  np.array([15, 15, 0.05, 0.05]),
    },
}
