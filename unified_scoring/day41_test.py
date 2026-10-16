from unified_scoring.scoring_engine import create_candidate_score


def test_candidate(
    candidate_id,
    role,
    ats_score,
    screening_score,
    interview_score
):
    candidate = create_candidate_score(
        candidate_id=candidate_id,
        role=role,
        ats_score=ats_score,
        screening_score=screening_score,
        interview_score=interview_score
    )

    print("\n==============================")
    print("UNIFIED CANDIDATE SCORE")
    print("==============================")

    print("Candidate ID:", candidate.candidate_id)
    print("Role:", candidate.role)
    print("ATS Score:", candidate.ats_score)
    print("Screening Score:", candidate.screening_score)
    print("Interview Score:", candidate.interview_score)
    print("Unified Score:", candidate.unified_score)
    print("Hiring Fit:", candidate.hiring_fit_percentage, "%")


# Test 1 - AI Engineer
test_candidate(
    candidate_id="CAND001",
    role="ai_engineer",
    ats_score=85,
    screening_score=78,
    interview_score=90
)


# Test 2 - Software Engineer
test_candidate(
    candidate_id="CAND002",
    role="software_engineer",
    ats_score=80,
    screening_score=75,
    interview_score=85
)


# Test 3 - HR
test_candidate(
    candidate_id="CAND003",
    role="hr",
    ats_score=70,
    screening_score=85,
    interview_score=90
)