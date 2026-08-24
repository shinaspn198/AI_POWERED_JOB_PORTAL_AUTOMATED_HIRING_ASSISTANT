from answer_quality_analyzer import analyze_answer


print("=" * 60)
print("DAY 27 - STEP 2 ANSWER QUALITY ANALYSIS TEST")
print("=" * 60)


# Test 1
answer = "Python."
print("\nTest 1")
print("Answer:", answer)
print("Result:", analyze_answer(answer))


# Test 2
answer = "I know Python and FastAPI."
print("\nTest 2")
print("Answer:", answer)
print("Result:", analyze_answer(answer))


# Test 3
answer = (
    "I have two years of experience in Python. "
    "I have worked with FastAPI and Machine Learning."
)
print("\nTest 3")
print("Answer:", answer)
print("Result:", analyze_answer(answer))


# Test 4
answer = ""
print("\nTest 4")
print("Answer:", answer)
print("Result:", analyze_answer(answer))


# Test 5
answer = "Yes, I have experience."
print("\nTest 5")
print("Answer:", answer)
print("Result:", analyze_answer(answer))


print("\n" + "=" * 60)
print("STEP 2 TEST COMPLETED")
print("=" * 60)