from hr_weight_config import get_weights


def generate_score_breakdown(
    answer_relevance,
    communication_score,
    confidence_score,
    consistency
):
    weights = get_weights()

    breakdown = {
        "Answer Relevance": {
            "score": answer_relevance,
            "weight": weights["answer_relevance"],
            "weighted_score": answer_relevance * weights["answer_relevance"]
        },
        "Communication": {
            "score": communication_score,
            "weight": weights["communication"],
            "weighted_score": communication_score * weights["communication"]
        },
        "Confidence": {
            "score": confidence_score,
            "weight": weights["confidence"],
            "weighted_score": confidence_score * weights["confidence"]
        },
        "Consistency": {
            "score": consistency,
            "weight": weights["consistency"],
            "weighted_score": consistency * weights["consistency"]
        }
    }

    return breakdown


if __name__ == "__main__":

    breakdown = generate_score_breakdown(
        answer_relevance=80,
        communication_score=75,
        confidence_score=85,
        consistency=90
    )

    print("===== EXPLAINABLE HR SCORE BREAKDOWN =====")

    for parameter, values in breakdown.items():
        print(f"\n{parameter}")
        print("Score:", values["score"])
        print("Weight:", values["weight"] * 100, "%")
        print("Weighted Score:", round(values["weighted_score"], 2))