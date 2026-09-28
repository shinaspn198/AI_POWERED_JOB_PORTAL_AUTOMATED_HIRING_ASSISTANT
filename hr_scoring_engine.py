from hr_weight_config import get_weights


def calculate_hr_score(
    answer_relevance,
    communication_score,
    confidence_score,
    consistency
):
    weights = get_weights()

    final_score = (
        answer_relevance * weights["answer_relevance"] +
        communication_score * weights["communication"] +
        confidence_score * weights["confidence"] +
        consistency * weights["consistency"]
    )

    return round(final_score, 2)


if __name__ == "__main__":

    score = calculate_hr_score(
        answer_relevance=80,
        communication_score=75,
        confidence_score=85,
        consistency=90
    )

    print("===== HR INTERVIEW SCORING ENGINE =====")
    print("Answer Relevance: 80")
    print("Communication Score: 75")
    print("Confidence Score: 85")
    print("Consistency: 90")

    print("\nFinal HR Interview Score:", score, "/ 100")