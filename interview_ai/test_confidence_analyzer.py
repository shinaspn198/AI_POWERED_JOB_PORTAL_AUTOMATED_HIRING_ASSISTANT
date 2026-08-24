from confidence_analyzer import detect_hesitation, analyze_confidence


print("=" * 60)
print("DAY 27 - STEP 1 CONFIDENCE ANALYSIS TEST")
print("=" * 60)


test_cases = [
    "I have two years of experience in Python.",
    "Uhh, I think I have around two years of experience.",
    "Um, maybe I worked with Python for two years.",
    "I am not sure, perhaps around one year of experience.",
    "I have probably worked with Python for three years, hmm.",
]


for index, answer in enumerate(test_cases, start=1):

    print(f"\nTest {index}")
    print("Answer:", answer)

    result = analyze_confidence(answer)

    print("Result:", result)


print("\n" + "=" * 60)
print("STEP 1 TEST COMPLETED")
print("=" * 60)