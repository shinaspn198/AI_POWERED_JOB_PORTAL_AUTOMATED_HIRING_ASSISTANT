"""
Day 45 - HR Interview Demo & Finalization

Uses the existing HR interview system and scoring system.

Day 45 tasks covered:
- Candidate interview simulation
- Scoring breakdown
- Final hiring recommendation
- Manager evaluation
"""

from hr_interview import run_interview
from screening_scorer import calculate_question_score
from candidate_screening_score import calculate_candidate_screening_score


def evaluate_interview(responses, evaluations):
    """
    Combine live interview responses with manager/evaluator scores.

    responses:
        List of responses captured during the HR interview.

    evaluations:
        List containing evaluator scores for each response.
    """

    if len(responses) != len(evaluations):
        raise ValueError(
            "Number of responses and evaluations must be the same."
        )

    question_scores = []

    for response, evaluation in zip(responses, evaluations):

        score = calculate_question_score(
            clarity=evaluation["clarity"],
            relevance=evaluation["relevance"],
            completeness=evaluation["completeness"],
            consistency=evaluation["consistency"]
        )

        question_scores.append({
            "question_id": response["question_id"],
            "question": response["question"],
            "response": response["response"],
            "clarity": score["clarity"],
            "relevance": score["relevance"],
            "completeness": score["completeness"],
            "consistency": score["consistency"],
            "total_score": score["total_score"],
            "max_score": score["max_score"]
        })

    total_score = sum(
        item["total_score"]
        for item in question_scores
    )

    maximum_score = sum(
        item["max_score"]
        for item in question_scores
    )

    overall_score = round(
        (total_score / maximum_score) * 100,
        2
    ) if maximum_score else 0

    session_result = {
        "average_score": overall_score,
        "total_responses": len(question_scores)
    }

    recommendation = calculate_candidate_screening_score(
        session_result
    )

    return {
        "question_scores": question_scores,
        "total_score": total_score,
        "maximum_score": maximum_score,
        "overall_score": overall_score,
        "total_responses": len(question_scores),
        "recommendation": recommendation
    }


def print_evaluation_report(result):
    """Display the Day 45 scoring breakdown."""

    print("\n")
    print("=" * 70)
    print("              DAY 45 - HR INTERVIEW EVALUATION")
    print("=" * 70)

    print("\n--- SCORING BREAKDOWN ---")

    for item in result["question_scores"]:

        print(f"\nQuestion {item['question_id']}:")
        print(f"Q: {item['question']}")
        print(f"Answer: {item['response']}")

        print("\nScores:")

        print(f"  Clarity       : {item['clarity']}/25")
        print(f"  Relevance     : {item['relevance']}/25")
        print(f"  Completeness  : {item['completeness']}/25")
        print(f"  Consistency   : {item['consistency']}/25")

        print(
            f"  Total         : "
            f"{item['total_score']}/{item['max_score']}"
        )

    print("\n" + "-" * 70)

    print("\n--- FINAL INTERVIEW SCORE ---")

    print(
        f"Total Score    : "
        f"{result['total_score']}/{result['maximum_score']}"
    )

    print(
        f"Overall Score  : "
        f"{result['overall_score']}/100"
    )

    recommendation = result["recommendation"]

    print("\n--- FINAL HIRING RECOMMENDATION ---")

    print(
        f"Decision       : "
        f"{recommendation['decision']}"
    )

    print(
        f"Reason         : "
        f"{recommendation['reason']}"
    )

    print("\n" + "=" * 70)
    print("                END OF EVALUATION")
    print("=" * 70)


def run_demo():

    print("\n===== DAY 45 HR INTERVIEW DEMO =====")

    print(
        "\nStarting live candidate interview..."
    )

    # ---------------------------------------------------------
    # STEP 1: Conduct the live HR interview
    # ---------------------------------------------------------

    responses = run_interview(
        "fresher",
        "technical"
    )

    # ---------------------------------------------------------
    # STEP 2: Manager evaluation
    # ---------------------------------------------------------

    evaluations = []

    print("\n\n===== MANAGER EVALUATION =====")

    print(
        "\nEvaluate each candidate response."
    )

    print(
        "Enter a score from 0 to 25 for each parameter."
    )

    for response in responses:

        print("\n" + "-" * 60)

        print(
            f"Question {response['question_id']}: "
            f"{response['question']}"
        )

        print(
            f"Candidate: {response['response']}"
        )

        print("\nEnter scores from 0 to 25:")

        clarity = float(
            input("Clarity: ")
        )

        relevance = float(
            input("Relevance: ")
        )

        completeness = float(
            input("Completeness: ")
        )

        consistency = float(
            input("Consistency: ")
        )

        evaluations.append({
            "clarity": clarity,
            "relevance": relevance,
            "completeness": completeness,
            "consistency": consistency
        })

    # ---------------------------------------------------------
    # STEP 3: Calculate final evaluation
    # ---------------------------------------------------------

    result = evaluate_interview(
        responses,
        evaluations
    )

    # ---------------------------------------------------------
    # STEP 4: Display scoring breakdown and recommendation
    # ---------------------------------------------------------

    print_evaluation_report(result)


if __name__ == "__main__":
    run_demo()