from combined_response_analyzer import analyze_response


print("=" * 60)
print("DAY 27 - STEP 4 COMBINED RESPONSE ANALYSIS TEST")
print("=" * 60)


# Test 1 - Strong response
question = "What is your experience with Python?"

answer = (
    "I have two years of professional experience working with "
    "Python and FastAPI."
)

print("\nTest 1 - Strong Response")
print("Question:", question)
print("Answer:", answer)
print("Result:", analyze_response(question, answer))


# Test 2 - Moderate response
question = "What programming skills do you have?"

answer = "I know Python and some other technologies."

print("\nTest 2 - Moderate Response")
print("Question:", question)
print("Answer:", answer)
print("Result:", analyze_response(question, answer))


# Test 3 - Weak response
question = "What is your experience with Python?"

answer = "I am not sure, maybe."

print("\nTest 3 - Weak Response")
print("Question:", question)
print("Answer:", answer)
print("Result:", analyze_response(question, answer))


# Test 4 - Irrelevant response
question = "What is your experience with Python?"

answer = "I enjoy playing football and watching movies."

print("\nTest 4 - Irrelevant Response")
print("Question:", question)
print("Answer:", answer)
print("Result:", analyze_response(question, answer))


# Test 5 - Empty response
question = "What is your experience with Python?"

answer = ""

print("\nTest 5 - Empty Response")
print("Question:", question)
print("Answer:", answer)
print("Result:", analyze_response(question, answer))


print("\n" + "=" * 60)
print("STEP 4 TEST COMPLETED")
print("=" * 60)