from final_screening_evaluator import evaluate_screening_response


print("=" * 60)
print("DAY 27 - STEP 6 FINAL SCREENING EVALUATION TEST")
print("=" * 60)


# Test 1 - Strong Candidate Response
question = "What is your experience with Python?"

answer = (
    "I have two years of professional experience "
    "working with Python and FastAPI."
)

result = evaluate_screening_response(
    question,
    answer
)

print("\nTest 1 - Strong Candidate")
print(result)


# Test 2 - Moderate Candidate Response
question = "What programming skills do you have?"

answer = (
    "I know Python and some other technologies."
)

result = evaluate_screening_response(
    question,
    answer
)

print("\nTest 2 - Moderate Candidate")
print(result)


# Test 3 - Weak Candidate Response
question = "What is your experience with Python?"

answer = "I am not sure, maybe."

result = evaluate_screening_response(
    question,
    answer
)

print("\nTest 3 - Weak Candidate")
print(result)


# Test 4 - Irrelevant Response
question = "What is your experience with Python?"

answer = (
    "I enjoy playing football and watching movies."
)

result = evaluate_screening_response(
    question,
    answer
)

print("\nTest 4 - Irrelevant Response")
print(result)


# Test 5 - Empty Response
question = "What is your experience with Python?"

answer = ""

result = evaluate_screening_response(
    question,
    answer
)

print("\nTest 5 - Empty Response")
print(result)


print("\n" + "=" * 60)
print("STEP 6 TEST COMPLETED")
print("=" * 60)