from screening_report_schema import ScreeningReport


def build_screening_report(
    candidate_id,
    screening_score,
    decision,
    key_answers=None,
    strengths=None,
    risks=None,
    missing_information=None,
    salary_expectation="",
    availability="",
    confirmed_skills=None,
):
    """
    Build a recruiter-ready AI screening report.
    """

    if key_answers is None:
        key_answers = []

    if strengths is None:
        strengths = []

    if risks is None:
        risks = []

    if missing_information is None:
        missing_information = []

    if confirmed_skills is None:
        confirmed_skills = []

    if decision == "strong_candidate":
        recommendation = "Candidate is recommended for the next recruitment stage."

    elif decision == "review":
        recommendation = "Candidate requires recruiter review before proceeding."

    elif decision == "needs_improvement":
        recommendation = "Candidate may require further evaluation."

    else:
        recommendation = "Candidate is not recommended for the next recruitment stage."

    return ScreeningReport(
        candidate_id=candidate_id,
        screening_score=screening_score,
        decision=decision,
        key_answers=key_answers,
        strengths=strengths,
        risks=risks,
        missing_information=missing_information,
        salary_expectation=salary_expectation,
        availability=availability,
        confirmed_skills=confirmed_skills,
        recommendation=recommendation,
    )