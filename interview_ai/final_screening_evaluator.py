from confidence_analyzer import analyze_confidence
from answer_quality_analyzer import analyze_answer
from answer_relevance_analyzer import analyze_relevance
from response_score_analyzer import calculate_response_score


def evaluate_screening_response(question, answer):
    """
    Perform complete AI screening response evaluation.
    """

    confidence = analyze_confidence(answer)

    quality = analyze_answer(answer)

    relevance = analyze_relevance(
        question,
        answer
    )

    score = calculate_response_score(
        confidence,
        quality,
        relevance
    )

    total_score = score["total_score"]

    if total_score >= 80:
        final_status = "strong"

    elif total_score >= 60:
        final_status = "acceptable"

    elif total_score >= 40:
        final_status = "needs_improvement"

    else:
        final_status = "weak"

    return {
        "question": question,
        "answer": answer,
        "confidence": confidence,
        "quality": quality,
        "relevance": relevance,
        "score": score,
        "final_status": final_status
    }