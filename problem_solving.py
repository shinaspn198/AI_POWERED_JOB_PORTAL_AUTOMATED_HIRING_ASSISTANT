def calculate_problem_solving_score(
    problem_identification,
    communication,
    solution,
    action,
    verification
):
    score = (
        problem_identification * 0.20 +
        communication * 0.20 +
        solution * 0.25 +
        action * 0.20 +
        verification * 0.15
    )

    return round(score, 2)


if __name__ == "__main__":

    score = calculate_problem_solving_score(
        problem_identification=90,
        communication=85,
        solution=80,
        action=90,
        verification=85
    )

    print("===== PROBLEM-SOLVING CLARITY =====")
    print("Problem Identification: 90")
    print("Communication: 85")
    print("Solution: 80")
    print("Action: 90")
    print("Verification: 85")

    print("\nProblem-Solving Clarity Score:", score, "/ 100")