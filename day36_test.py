from confidence_analyzer import analyze_confidence
from sentiment_engine import analyze_sentiment
from contradiction_detector import detect_contradiction
from stress_indicator import detect_stress
from behavioral_confidence import calculate_behavioral_confidence


previous_answer = "I have experience working with Python."

current_answer = (
    "I am confident and comfortable working with Python. "
    "I think I can handle difficult projects."
)


confidence = analyze_confidence(current_answer)
sentiment = analyze_sentiment(current_answer)
stress = detect_stress(current_answer)

contradictions = detect_contradiction(
    previous_answer,
    current_answer
)

final_score = calculate_behavioral_confidence(
    confidence_score=confidence["confidence_score"],
    sentiment_score=sentiment["sentiment_score"],
    stress_score=stress["stress_score"],
    contradiction_detected=bool(contradictions)
)


print("===== DAY 36 FINAL EVALUATION =====")

print("\nConfidence Analysis")
print("Confidence Score:", confidence["confidence_score"])

print("\nSentiment Analysis")
print("Sentiment:", sentiment["sentiment"])
print("Sentiment Score:", sentiment["sentiment_score"])

print("\nStress Analysis")
print("Stress Count:", stress["stress_count"])
print("Stress Score:", stress["stress_score"])

print("\nContradiction Analysis")
print("Contradictions:", contradictions)

print("\nFinal Behavioral Confidence")
print("Behavioral Confidence Score:", final_score, "/ 100")