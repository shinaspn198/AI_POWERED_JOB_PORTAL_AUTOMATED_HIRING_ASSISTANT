from manual_evaluation import MANUAL_EVALUATION


AI_EVALUATION = {
    "Confident": {
        "overall": 88
    },

    "Hesitant": {
        "overall": 62
    },

    "Inexperienced": {
        "overall": 68
    },

    "Overqualified": {
        "overall": 90
    }
}


def compare_scores():

    print("===== AI VS MANUAL EVALUATION =====")

    for candidate_type in MANUAL_EVALUATION:

        manual_score = MANUAL_EVALUATION[candidate_type]["overall"]
        ai_score = AI_EVALUATION[candidate_type]["overall"]

        difference = abs(ai_score - manual_score)

        print("\nCandidate Type:", candidate_type)
        print("AI Score:", ai_score)
        print("Manual Score:", manual_score)
        print("Difference:", difference)

        if difference <= 5:
            print("Status: Consistent")
        else:
            print("Status: Inconsistent")


if __name__ == "__main__":
    compare_scores()