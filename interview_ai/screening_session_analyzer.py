from final_screening_evaluator import evaluate_screening_response


def analyze_screening_session(responses):
    """
    Analyze a complete candidate screening session.

    responses should be a list of dictionaries containing:
    {
        "question": "...",
        "answer": "..."
    }
    """

    evaluations = []

    total_score = 0

    for response in responses:

        question = response.get("question", "")
        answer = response.get("answer", "")

        evaluation = evaluate_screening_response(
            question,
            answer
        )

        evaluations.append(evaluation)

        total_score += evaluation["score"]["total_score"]

    response_count = len(evaluations)

    if response_count > 0:
        average_score = total_score / response_count
    else:
        average_score = 0

    if average_score >= 80:
        overall_status = "strong"

    elif average_score >= 60:
        overall_status = "acceptable"

    elif average_score >= 40:
        overall_status = "needs_improvement"

    else:
        overall_status = "weak"

    return {
        "total_responses": response_count,
        "total_score": total_score,
        "average_score": round(average_score, 2),
        "overall_status": overall_status,
        "evaluations": evaluations
    }