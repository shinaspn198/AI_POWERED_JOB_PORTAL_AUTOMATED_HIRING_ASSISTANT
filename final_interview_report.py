from interview_summary import generate_summary
from recruiter_report import generate_recruiter_report


def create_final_report():
    report = generate_summary(
        candidate_name="Shinas PN",
        strengths=[
            "Good logical reasoning",
            "Clear communication",
            "Strong problem-solving ability"
        ],
        weaknesses=[
            "Needs improvement in advanced reasoning"
        ],
        cultural_fit=[
            "Team-oriented",
            "Willing to communicate"
        ],
        risk_flags=[
            "No major risk identified"
        ],
        inconsistencies=[
            "No major inconsistencies identified"
        ],
        overall_performance="Good HR interview performance"
    )

    recruiter_report = generate_recruiter_report(report)

    return recruiter_report


if __name__ == "__main__":

    print(create_final_report())