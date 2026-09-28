def calculate_final_aptitude_score(
    logical_reasoning,
    scenario_score,
    problem_solving
):
    final_score = (
        logical_reasoning * 0.40 +
        scenario_score * 0.30 +
        problem_solving * 0.30
    )

    return round(final_score, 2)


if __name__ == "__main__":

    logical_reasoning = 80
    scenario_score = 100
    problem_solving = 85.75

    final_score = calculate_final_aptitude_score(
        logical_reasoning,
        scenario_score,
        problem_solving
    )

    print("===== FINAL APTITUDE AI SCORE =====")
    print("Logical Reasoning:", logical_reasoning)
    print("Scenario Evaluation:", scenario_score)
    print("Problem-Solving Clarity:", problem_solving)

    print("\nFinal Aptitude Score:", final_score, "/ 100")