from candidate_screening_score import calculate_candidate_screening_score


print("=" * 60)
print("DAY 27 - STEP 8 CANDIDATE SCREENING SCORE TEST")
print("=" * 60)


# Test 1 - Strong Candidate
session_result = {
    "total_responses": 3,
    "total_score": 275,
    "average_score": 91.67,
    "overall_status": "strong"
}

result = calculate_candidate_screening_score(
    session_result
)

print("\nTest 1 - Strong Candidate")
print(result)


# Test 2 - Review Candidate
session_result = {
    "total_responses": 3,
    "total_score": 195,
    "average_score": 65.0,
    "overall_status": "acceptable"
}

result = calculate_candidate_screening_score(
    session_result
)

print("\nTest 2 - Review Candidate")
print(result)


# Test 3 - Needs Improvement
session_result = {
    "total_responses": 3,
    "total_score": 135,
    "average_score": 45.0,
    "overall_status": "needs_improvement"
}

result = calculate_candidate_screening_score(
    session_result
)

print("\nTest 3 - Needs Improvement")
print(result)


# Test 4 - Rejected Candidate
session_result = {
    "total_responses": 3,
    "total_score": 90,
    "average_score": 30.0,
    "overall_status": "weak"
}

result = calculate_candidate_screening_score(
    session_result
)

print("\nTest 4 - Rejected Candidate")
print(result)


# Test 5 - Empty Session
session_result = {
    "total_responses": 0,
    "total_score": 0,
    "average_score": 0,
    "overall_status": "weak"
}

result = calculate_candidate_screening_score(
    session_result
)

print("\nTest 5 - Empty Session")
print(result)


print("\n" + "=" * 60)
print("STEP 8 TEST COMPLETED")
print("=" * 60)