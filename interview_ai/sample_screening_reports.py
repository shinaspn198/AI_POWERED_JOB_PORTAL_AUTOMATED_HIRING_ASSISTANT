from screening_report_builder import build_screening_report
from recruiter_report_formatter import format_recruiter_report


def generate_sample_reports():
    reports = []

    # Strong Candidate
    strong_candidate = build_screening_report(
        candidate_id="CAND-001",
        screening_score=91.67,
        decision="strong_candidate",
        key_answers=[
            "Experienced with Python and Machine Learning"
        ],
        strengths=[
            "Strong technical knowledge",
            "High confidence"
        ],
        risks=[
            "Limited experience"
        ],
        missing_information=[
            "Notice period"
        ],
        salary_expectation="6 LPA",
        availability="Immediate",
        confirmed_skills=[
            "Python",
            "Machine Learning",
            "FastAPI"
        ]
    )

    reports.append(strong_candidate)

    # Review Candidate
    review_candidate = build_screening_report(
        candidate_id="CAND-002",
        screening_score=65.0,
        decision="review",
        key_answers=[
            "Has basic Python and data analysis experience"
        ],
        strengths=[
            "Good communication"
        ],
        risks=[
            "Limited Machine Learning experience"
        ],
        missing_information=[
            "Salary expectation"
        ],
        salary_expectation="",
        availability="15 days",
        confirmed_skills=[
            "Python",
            "Pandas"
        ]
    )

    reports.append(review_candidate)

    return reports


if __name__ == "__main__":
    reports = generate_sample_reports()

    for report in reports:
        print(format_recruiter_report(report))
        print()