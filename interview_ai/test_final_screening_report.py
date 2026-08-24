from final_screening_report import generate_final_screening_report


print("=" * 60)
print("DAY 27 - STEP 9 FINAL SCREENING REPORT TEST")
print("=" * 60)


# ------------------------------------------------------------
# Test 1 - Strong Candidate
# ------------------------------------------------------------

session_analysis = {
    "candidate_id": "CAND-001",
    "total_responses": 3,
    "average_score": 91.67
}

screening_result = {
    "screening_score": 91.67,
    "decision": "strong_candidate",
    "reason": "Candidate demonstrated strong screening performance."
}

report = generate_final_screening_report(
    session_analysis,
    screening_result
)

print("\nTest 1 - Strong Candidate")
print(report)


# ------------------------------------------------------------
# Test 2 - Review Candidate
# ------------------------------------------------------------

session_analysis = {
    "candidate_id": "CAND-002",
    "total_responses": 3,
    "average_score": 65.0
}

screening_result = {
    "screening_score": 65.0,
    "decision": "review",
    "reason": "Candidate requires recruiter review."
}

report = generate_final_screening_report(
    session_analysis,
    screening_result
)

print("\nTest 2 - Review Candidate")
print(report)


# ------------------------------------------------------------
# Test 3 - Needs Improvement
# ------------------------------------------------------------

session_analysis = {
    "candidate_id": "CAND-003",
    "total_responses": 3,
    "average_score": 45.0
}

screening_result = {
    "screening_score": 45.0,
    "decision": "needs_improvement",
    "reason": "Candidate needs improvement in screening performance."
}

report = generate_final_screening_report(
    session_analysis,
    screening_result
)

print("\nTest 3 - Needs Improvement")
print(report)


# ------------------------------------------------------------
# Test 4 - Rejected Candidate
# ------------------------------------------------------------

session_analysis = {
    "candidate_id": "CAND-004",
    "total_responses": 3,
    "average_score": 30.0
}

screening_result = {
    "screening_score": 30.0,
    "decision": "rejected",
    "reason": "Candidate did not meet screening requirements."
}

report = generate_final_screening_report(
    session_analysis,
    screening_result
)

print("\nTest 4 - Rejected Candidate")
print(report)


# ------------------------------------------------------------
# Test 5 - Empty Session
# ------------------------------------------------------------

session_analysis = {
    "candidate_id": "CAND-005",
    "total_responses": 0,
    "average_score": 0
}

screening_result = {
    "screening_score": 0,
    "decision": "rejected",
    "reason": "Empty screening session."
}

report = generate_final_screening_report(
    session_analysis,
    screening_result
)

print("\nTest 5 - Empty Session")
print(report)


print("\n" + "=" * 60)
print("DAY 27 - STEP 9 TEST COMPLETED")
print("=" * 60)