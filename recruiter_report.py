from interview_summary import generate_summary


def generate_recruiter_report(report):
    candidate = report["candidate_name"]

    strengths = ", ".join(report["strengths"])
    weaknesses = ", ".join(report["weaknesses"])
    cultural_fit = ", ".join(report["cultural_fit"])
    risk_flags = ", ".join(report["risk_flags"])
    inconsistencies = ", ".join(report["inconsistencies"])
    performance = report["overall_performance"]

    summary = f"""
===== RECRUITER INTERVIEW REPORT =====

Candidate: {candidate}

Overall HR Performance:
{performance}.

Strengths:
{strengths}.

Areas for Improvement:
{weaknesses}.

Cultural Fit Indicators:
{cultural_fit}.

Risk Flags:
{risk_flags}.

Inconsistencies:
{inconsistencies}.

Recruiter Summary:
{candidate} demonstrated {performance.lower()}.
The candidate showed strengths in {strengths.lower()}.
The main area for improvement is {weaknesses.lower()}.
"""

    return summary


if __name__ == "__main__":

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

    print(recruiter_report)