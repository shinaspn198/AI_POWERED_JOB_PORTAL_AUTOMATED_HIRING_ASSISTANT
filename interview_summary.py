def generate_summary(
    candidate_name,
    strengths,
    weaknesses,
    cultural_fit,
    risk_flags,
    inconsistencies,
    overall_performance
):
    report = {
        "candidate_name": candidate_name,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "cultural_fit": cultural_fit,
        "risk_flags": risk_flags,
        "inconsistencies": inconsistencies,
        "overall_performance": overall_performance
    }

    return report


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

    print("===== AI INTERVIEW SUMMARY =====")

    print("\nCandidate:", report["candidate_name"])

    print("\nStrengths:")
    for item in report["strengths"]:
        print("-", item)

    print("\nWeaknesses:")
    for item in report["weaknesses"]:
        print("-", item)

    print("\nCultural Fit:")
    for item in report["cultural_fit"]:
        print("-", item)

    print("\nRisk Flags:")
    for item in report["risk_flags"]:
        print("-", item)

    print("\nInconsistencies:")
    for item in report["inconsistencies"]:
        print("-", item)

    print("\nOverall HR Performance:")
    print(report["overall_performance"])