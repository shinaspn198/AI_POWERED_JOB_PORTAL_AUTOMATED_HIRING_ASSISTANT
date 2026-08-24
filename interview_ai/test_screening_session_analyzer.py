from screening_session_analyzer import analyze_screening_session


print("=" * 60)
print("DAY 27 - STEP 7 SCREENING SESSION ANALYSIS TEST")
print("=" * 60)


responses = [

    {
        "question": "What is your experience with Python?",
        "answer": (
            "I have two years of professional experience "
            "working with Python and FastAPI."
        )
    },

    {
        "question": "What programming skills do you have?",
        "answer": (
            "I know Python, FastAPI, and Machine Learning."
        )
    },

    {
        "question": "Why are you interested in AI Engineering?",
        "answer": (
            "I am interested in building AI systems and "
            "solving real world problems using machine learning."
        )
    }

]


result = analyze_screening_session(responses)


print("\nTotal Responses:")
print(result["total_responses"])

print("\nTotal Score:")
print(result["total_score"])

print("\nAverage Score:")
print(result["average_score"])

print("\nOverall Status:")
print(result["overall_status"])


print("\nIndividual Evaluations:")

for index, evaluation in enumerate(
    result["evaluations"],
    start=1
):

    print("\nQuestion", index)
    print("Question:", evaluation["question"])
    print("Answer:", evaluation["answer"])
    print("Score:", evaluation["score"]["total_score"])
    print("Assessment:", evaluation["score"]["assessment"])
    print("Final Status:", evaluation["final_status"])


print("\n" + "=" * 60)
print("STEP 7 TEST COMPLETED")
print("=" * 60)