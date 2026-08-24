def calculate_response_score(confidence, quality, relevance):
    """
    Calculate an overall response score based on
    confidence, quality, and relevance.
    """

    score = 0

    # Confidence score
    confidence_scores = {
        "high": 30,
        "moderate": 20,
        "low": 10
    }

    score += confidence_scores.get(
        confidence.get("confidence_level"),
        0
    )

    # Quality score
    quality_scores = {
        "good": 30,
        "moderate": 20,
        "poor": 10
    }

    score += quality_scores.get(
        quality.get("quality_level"),
        0
    )

    # Relevance score
    relevance_score = relevance.get("relevance_score", 0)

    if relevance_score >= 80:
        score += 40
    elif relevance_score >= 50:
        score += 25
    elif relevance_score > 0:
        score += 10

    # Final classification
    if score >= 80:
        assessment = "excellent"

    elif score >= 60:
        assessment = "good"

    elif score >= 40:
        assessment = "moderate"

    else:
        assessment = "poor"

    return {
        "confidence_score": confidence_scores.get(
            confidence.get("confidence_level"),
            0
        ),
        "quality_score": quality_scores.get(
            quality.get("quality_level"),
            0
        ),
        "relevance_score": relevance_score,
        "total_score": score,
        "assessment": assessment
    }