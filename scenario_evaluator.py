SCENARIOS = [
    {
        "id": 1,
        "scenario": "Your team has a deadline tomorrow, but one team member has not completed their task. What would you do?",
        "ideal_points": [
            "understand the problem",
            "communicate with team member",
            "prioritize the task",
            "help solve the issue",
            "complete the deadline"
        ]
    },
    {
        "id": 2,
        "scenario": "You find a serious bug just before a project demo. What would you do?",
        "ideal_points": [
            "identify the bug",
            "assess the impact",
            "communicate with the team",
            "fix or prioritize the issue",
            "test the solution"
        ]
    }
]


def evaluate_scenario(answer, scenario):
    answer = answer.lower()

    matched_points = 0

    for point in scenario["ideal_points"]:
        keywords = point.split()

        if any(keyword in answer for keyword in keywords):
            matched_points += 1

    score = (matched_points / len(scenario["ideal_points"])) * 100

    return round(score, 2)


if __name__ == "__main__":

    scenario = SCENARIOS[0]

    print("===== SITUATIONAL JUDGMENT EVALUATION =====")
    print("\nScenario:")
    print(scenario["scenario"])

    answer = input("\nCandidate Answer: ")

    score = evaluate_scenario(answer, scenario)

    print("\nScenario Evaluation Score:", score, "/ 100")