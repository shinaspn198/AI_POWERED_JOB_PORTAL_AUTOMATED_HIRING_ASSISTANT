from interview_summary import generate_summary
from recruiter_report import generate_recruiter_report


def simulate_interview(candidate_type):
    print("\n========================================")
    print("HR INTERVIEW SIMULATION")
    print("========================================")
    print("Candidate Type:", candidate_type)

    if candidate_type == "Confident":
        strengths = [
            "Clear communication",
            "Strong confidence",
            "Good problem-solving"
        ]
        weaknesses = [
            "Needs deeper technical examples"
        ]

    elif candidate_type == "Hesitant":
        strengths = [
            "Good technical knowledge",
            "Willing to learn"
        ]
        weaknesses = [
            "Hesitant communication",
            "Needs improvement in confidence"
        ]

    elif candidate_type == "Inexperienced":
        strengths = [
            "Good learning attitude",
            "Basic problem-solving ability"
        ]
        weaknesses = [
            "Limited professional experience"
        ]

    elif candidate_type == "Overqualified":
        strengths = [
            "Strong experience",
            "Excellent problem-solving",
            "Strong communication"
        ]
        weaknesses = [
            "May have expectations beyond the role"
        ]

    else:
        strengths = []
        weaknesses = []

    report = generate_summary(
        candidate_name="Test Candidate",
        strengths=strengths,
        weaknesses=weaknesses,
        cultural_fit=["Team-oriented"],
        risk_flags=["No major risk identified"],
        inconsistencies=["No major inconsistencies identified"],
        overall_performance="Interview completed successfully"
    )

    recruiter_report = generate_recruiter_report(report)

    print("\n" + recruiter_report)


if __name__ == "__main__":

    candidate_types = [
        "Confident",
        "Hesitant",
        "Inexperienced",
        "Overqualified"
    ]

    for candidate in candidate_types:
        simulate_interview(candidate)