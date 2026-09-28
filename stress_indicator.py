STRESS_WORDS = [
    "nervous",
    "worried",
    "stressed",
    "afraid",
    "anxious",
    "pressure",
    "difficult"
]

UNCERTAINTY_PHRASES = [
    "i think",
    "i guess",
    "not sure",
    "maybe",
    "probably"
]


def detect_stress(text):
    text_lower = text.lower()

    stress_words = []

    for word in STRESS_WORDS:
        if word in text_lower:
            stress_words.append(word)

    uncertainty = []

    for phrase in UNCERTAINTY_PHRASES:
        if phrase in text_lower:
            uncertainty.append(phrase)

    repeated_words = []

    words = text_lower.split()

    for i in range(len(words) - 1):
        if words[i] == words[i + 1]:
            repeated_words.append(words[i])

    excessive_punctuation = (
        "!!!" in text or "???" in text
    )

    stress_count = (
        len(stress_words)
        + len(uncertainty)
        + len(repeated_words)
        + int(excessive_punctuation)
    )

    if stress_count == 0:
        stress_score = 0
    elif stress_count <= 2:
        stress_score = 30
    elif stress_count <= 4:
        stress_score = 60
    else:
        stress_score = 80

    return {
        "stress_words": stress_words,
        "uncertainty_phrases": uncertainty,
        "repeated_words": repeated_words,
        "excessive_punctuation": excessive_punctuation,
        "stress_count": stress_count,
        "stress_score": stress_score
    }


if __name__ == "__main__":

    answer = input("Enter candidate response: ")

    result = detect_stress(answer)

    print("\n===== STRESS INDICATOR ANALYSIS =====")
    print("Stress Words:", result["stress_words"])
    print("Uncertainty Phrases:", result["uncertainty_phrases"])
    print("Repeated Words:", result["repeated_words"])
    print("Excessive Punctuation:", result["excessive_punctuation"])
    print("Stress Count:", result["stress_count"])
    print("Stress Score:", result["stress_score"], "/ 100")