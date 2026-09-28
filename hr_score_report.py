from hr_scoring_engine import calculate_hr_score
from hr_score_breakdown import generate_score_breakdown


def generate_hr_report(candidate_name):
    answer_relevance = 80
    communication = 75
    confidence = 85
    consistency = 90

    final_score = calculate_hr_score(
        answer_relevance,
        communication,
        confidence,
        consistency
    )

    breakdown = generate_score_breakdown(
        answer_relevance,
        communication,
        confidence,
        consistency
    )

    print("========================================")
    print("       CANDIDATE HR SCORE REPORT")
    print("========================================")

    print("Candidate:", candidate_name)

    print("\nScore Breakdown:")

    for parameter, values in breakdown.items():
        print(
            f"{parameter}: "
            f"{values['score']} "
            f"(Weighted: {round(values['weighted_score'], 2)})"
        )

    print("\n----------------------------------------")
    print("Final HR Interview Score:", final_score, "/ 100")
    print("----------------------------------------")


if __name__ == "__main__":
    generate_hr_report("Shinas PN")