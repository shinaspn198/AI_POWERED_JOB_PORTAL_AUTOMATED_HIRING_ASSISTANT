from manual_evaluation import MANUAL_EVALUATION
from ai_vs_manual import AI_EVALUATION


def generate_report():

    print("========================================")
    print("       DAY 40 HR INTERVIEW TEST REPORT")
    print("========================================")

    consistent = 0
    inconsistent = 0

    for candidate_type in MANUAL_EVALUATION:

        manual_score = MANUAL_EVALUATION[candidate_type]["overall"]
        ai_score = AI_EVALUATION[candidate_type]["overall"]

        difference = abs(ai_score - manual_score)

        if difference <= 5:
            status = "Consistent"
            consistent += 1
        else:
            status = "Inconsistent"
            inconsistent += 1

        print("\nCandidate Type:", candidate_type)
        print("AI Score:", ai_score)
        print("Manual Score:", manual_score)
        print("Difference:", difference)
        print("Status:", status)

    total = consistent + inconsistent

    accuracy = (consistent / total) * 100

    print("\n========================================")
    print("EVALUATION SUMMARY")
    print("========================================")

    print("Total Candidates:", total)
    print("Consistent Results:", consistent)
    print("Inconsistent Results:", inconsistent)
    print("Accuracy Evaluation:", round(accuracy, 2), "%")

    print("\nImprovement Recommendations:")

    if inconsistent == 0:
        print("- Continue monitoring AI scoring consistency.")
        print("- Test with more candidate interview sessions.")
        print("- Expand testing with additional candidate profiles.")
    else:
        print("- Review scoring weights.")
        print("- Improve AI evaluation rules.")
        print("- Add more test cases.")


if __name__ == "__main__":
    generate_report()