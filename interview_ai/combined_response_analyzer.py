from confidence_analyzer import analyze_confidence
from answer_quality_analyzer import analyze_answer
from answer_relevance_analyzer import analyze_relevance


def analyze_response(question, answer):
    """
    Combine confidence, quality, and relevance analysis
    into one candidate response evaluation.
    """

    if not isinstance(question, str):
        raise ValueError("Question must be a string.")

    if not isinstance(answer, str):
        raise ValueError("Answer must be a string.")

    question = question.strip()
    answer = answer.strip()

    if not question:
        raise ValueError("Question cannot be empty.")

    confidence = analyze_confidence(answer)

    quality = analyze_answer(answer)

    relevance = analyze_relevance(question, answer)

    confidence_level = confidence["confidence_level"]
    quality_level = quality["quality_level"]
    relevance_level = relevance["relevance_level"]

    # Overall assessment
    if (
        confidence_level == "high"
        and quality_level == "good"
        and relevance_level == "relevant"
    ):
        overall_assessment = "strong"

    elif (
        relevance_level == "irrelevant"
        or quality_level == "poor"
    ):
        overall_assessment = "weak"

    else:
        overall_assessment = "moderate"

    return {
        "question": question,
        "answer": answer,

        "confidence": confidence,
        "quality": quality,
        "relevance": relevance,

        "overall_assessment": overall_assessment
    }