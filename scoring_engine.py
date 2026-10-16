def final_score(ats_score, interview_score):

    scores = {
        "ATS score": ats_score,
        "Interview score": interview_score
    }

    for name, score in scores.items():

        if not isinstance(score, (int, float)):
            raise TypeError(
                f"{name} must be a number."
            )

        if score < 0 or score > 100:
            raise ValueError(
                f"{name} must be between 0 and 100."
            )

    return round(
        (ats_score + interview_score) / 2,
        2
    )