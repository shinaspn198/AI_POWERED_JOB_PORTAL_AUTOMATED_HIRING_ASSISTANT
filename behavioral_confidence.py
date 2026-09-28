def calculate_behavioral_confidence(
    confidence_score,
    sentiment_score,
    stress_score,
    contradiction_detected
):
    contradiction_score = 0 if contradiction_detected else 100

    final_score = (
        confidence_score * 0.40
        + sentiment_score * 0.25
        + (100 - stress_score) * 0.20
        + contradiction_score * 0.15
    )

    return round(final_score, 2)


if __name__ == "__main__":

    score = calculate_behavioral_confidence(
        confidence_score=80,
        sentiment_score=70,
        stress_score=30,
        contradiction_detected=False
    )

    print("===== BEHAVIORAL CONFIDENCE =====")
    print("Confidence/Hesitation Score: 80")
    print("Sentiment Score: 70")
    print("Stress Score: 30")
    print("Contradiction Detected: False")
    print("Behavioral Confidence Score:", score, "/ 100")