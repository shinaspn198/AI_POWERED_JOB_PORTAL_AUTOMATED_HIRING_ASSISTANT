def generate_final_screening_report(session_analysis, screening_result):
    """
    Generate recruiter-friendly final screening report.
    """

    candidate_id = session_analysis.get("candidate_id", "UNKNOWN")

    total_responses = session_analysis.get("total_responses", 0)

    average_score = session_analysis.get("average_score", 0)

    screening_score = screening_result.get("screening_score", 0)

    decision = screening_result.get("decision", "rejected")

    reason = screening_result.get(
        "reason",
        "Candidate screening evaluation completed."
    )

    strengths = []
    weaknesses = []
    risk_indicators = []

    # Strong candidate
    if screening_score >= 80:
        strengths = [
            "High confidence",
            "Good answer quality",
            "Highly relevant responses"
        ]

    # Review candidate
    elif screening_score >= 60:
        strengths = [
            "Acceptable screening performance",
            "Generally relevant responses"
        ]

        weaknesses = [
            "Some areas require recruiter review"
        ]

    # Needs improvement
    elif screening_score >= 40:
        weaknesses = [
            "Low overall screening performance",
            "Answers require improvement"
        ]

        risk_indicators = [
            "Candidate may require additional evaluation"
        ]

    # Rejected
    else:
        weaknesses = [
            "Poor overall screening performance"
        ]

        risk_indicators = [
            "Low screening score",
            "Candidate does not currently meet screening expectations"
        ]

    return {
        "candidate_id": candidate_id,
        "total_responses": total_responses,
        "average_score": average_score,
        "screening_score": screening_score,
        "decision": decision,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "risk_indicators": risk_indicators,
        "recommendation": reason
    }