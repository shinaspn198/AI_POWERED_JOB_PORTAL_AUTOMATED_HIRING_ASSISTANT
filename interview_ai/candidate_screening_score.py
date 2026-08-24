def calculate_candidate_screening_score(session_result):
    """
    Convert screening session results into
    a final candidate screening score and decision.
    """

    average_score = session_result.get(
        "average_score",
        0
    )

    total_responses = session_result.get(
        "total_responses",
        0
    )

    if total_responses == 0:
        return {
            "screening_score": 0,
            "decision": "rejected",
            "reason": "No screening responses provided"
        }

    if average_score >= 80:
        decision = "strong_candidate"
        reason = "Candidate demonstrated strong screening performance."

    elif average_score >= 60:
        decision = "review"
        reason = "Candidate requires recruiter review."

    elif average_score >= 40:
        decision = "needs_improvement"
        reason = "Candidate responses require improvement."

    else:
        decision = "rejected"
        reason = "Candidate screening performance is below the minimum threshold."

    return {
        "screening_score": round(average_score, 2),
        "decision": decision,
        "reason": reason
    }