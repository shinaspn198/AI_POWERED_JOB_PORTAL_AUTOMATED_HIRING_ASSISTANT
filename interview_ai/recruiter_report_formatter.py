from screening_report_schema import ScreeningReport


def format_recruiter_report(report: ScreeningReport):
    """
    Convert a ScreeningReport into a recruiter-friendly text report.
    """

    lines = []

    lines.append("=" * 60)
    lines.append("AI SCREENING REPORT")
    lines.append("=" * 60)

    lines.append(f"Candidate ID: {report.candidate_id}")
    lines.append(f"Screening Score: {report.screening_score}")
    lines.append(f"Decision: {report.decision}")

    lines.append("\nKEY ANSWERS")
    lines.append("-" * 30)

    if report.key_answers:
        for answer in report.key_answers:
            lines.append(f"- {answer}")
    else:
        lines.append("- No key answers available")

    lines.append("\nSTRENGTHS")
    lines.append("-" * 30)

    if report.strengths:
        for strength in report.strengths:
            lines.append(f"- {strength}")
    else:
        lines.append("- No strengths identified")

    lines.append("\nRISKS")
    lines.append("-" * 30)

    if report.risks:
        for risk in report.risks:
            lines.append(f"- {risk}")
    else:
        lines.append("- No risks identified")

    lines.append("\nMISSING INFORMATION")
    lines.append("-" * 30)

    if report.missing_information:
        for item in report.missing_information:
            lines.append(f"- {item}")
    else:
        lines.append("- No missing information")

    lines.append("\nCANDIDATE DETAILS")
    lines.append("-" * 30)
    lines.append(f"Salary Expectation: {report.salary_expectation}")
    lines.append(f"Availability: {report.availability}")

    lines.append("\nCONFIRMED SKILLS")
    lines.append("-" * 30)

    if report.confirmed_skills:
        for skill in report.confirmed_skills:
            lines.append(f"- {skill}")
    else:
        lines.append("- No confirmed skills")

    lines.append("\nRECRUITER RECOMMENDATION")
    lines.append("-" * 30)
    lines.append(report.recommendation)

    lines.append("\n" + "=" * 60)

    return "\n".join(lines)