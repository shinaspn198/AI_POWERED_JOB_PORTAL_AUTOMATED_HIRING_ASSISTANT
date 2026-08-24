from answer_relevance_analyzer import analyze_relevance


print("=" * 60)
print("DAY 27 - STEP 3 ANSWER RELEVANCE ANALYSIS TEST")
print("=" * 60)


# Test 1 - Strongly relevant
question = "What is your experience with Python?"
answer = "I have two years of experience working with Python."

print("\nTest 1")
print("Question:", question)
print("Answer:", answer)
print("Result:", analyze_relevance(question, answer))


# Test 2 - Partially relevant
question = "What is your experience with Python?"
answer = "I have worked with Python and other technologies."

print("\nTest 2")
print("Question:", question)
print("Answer:", answer)
print("Result:", analyze_relevance(question, answer))


# Test 3 - Irrelevant
question = "What is your experience with Python?"
answer = "I enjoy playing football and watching movies."

print("\nTest 3")
print("Question:", question)
print("Answer:", answer)
print("Result:", analyze_relevance(question, answer))


# Test 4 - Empty answer
question = "What is your experience with Python?"
answer = ""

print("\nTest 4")
print("Question:", question)
print("Answer:", answer)
print("Result:", analyze_relevance(question, answer))


# Test 5 - Skills question
question = "Which programming skills do you have?"
answer = "I know Python, FastAPI, and Machine Learning."

print("\nTest 5")
print("Question:", question)
print("Answer:", answer)
print("Result:", analyze_relevance(question, answer))


print("\n" + "=" * 60)
print("STEP 3 TEST COMPLETED")
print("=" * 60)