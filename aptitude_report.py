from aptitude_final_score import calculate_final_aptitude_score


def generate_aptitude_report(candidate_name):
    logical_reasoning = 80
    scenario_score = 100
    problem_solving = 85.75

    final_score = calculate_final_aptitude_score(
        logical_reasoning,
        scenario_score,
        problem_solving
    )

    print("========================================")
    print("       APTITUDE AI CANDIDATE REPORT")
    print("========================================")

    print("Candidate:", candidate_name)

    print("\nEvaluation Breakdown:")
    print("Logical Reasoning:", logical_reasoning)
    print("Scenario Evaluation:", scenario_score)
    print("Problem-Solving Clarity:", problem_solving)

    print("\n----------------------------------------")
    print("Final Aptitude Score:", final_score, "/ 100")
    print("----------------------------------------")


if __name__ == "__main__":
    generate_aptitude_report("Shinas PN")