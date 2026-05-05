class MotionModel:
    def predict(self, embedding):

        # Squats = dominant lower-body variance
        squat_score = embedding["energy"][1] + embedding["energy"][2]

        # Curls = elbow dominance
        curl_score = embedding["energy"][0]

        # Raises = shoulder + vertical motion
        raise_score = embedding["energy"][3]

        scores = {
            "Squats": squat_score,
            "Bicep Curls": curl_score,
            "Arm Raises": raise_score
        }

        label = max(scores, key=scores.get)

        return label, scores
