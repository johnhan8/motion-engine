# ============================================================
# Session State (Single Source of Truth)
# ============================================================

class SessionState:
    def __init__(self):

        # ----------------------
        # GLOBAL METRICS
        # ----------------------
        self.session_start_time = None

        # ----------------------
        # SQUAT STATE
        # ----------------------
        self.squat_reps = 0
        self.squat_stage = "up"
        self.squat_prev_hip_y = None
        self.squat_hold_frames = 0
        self.squat_cooldown = 0

        # ----------------------
        # CURL STATE
        # ----------------------
        self.curl_reps = 0
        self.curl_stage = "down"
        self.curl_prev_angle = None

        # ----------------------
        # ARM RAISE STATE
        # ----------------------
        self.raise_reps = 0
        self.raise_stage = "down"
        self.raise_prev_angle = None

        # ----------------------
        # DEBUG
        # ----------------------
        self.debug = {}

        # Optional runtime log buffer (not required, but useful)
        self.debug_log = []
