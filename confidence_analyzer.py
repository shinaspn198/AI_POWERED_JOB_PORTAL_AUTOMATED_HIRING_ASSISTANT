UNCERTAINTY_PHRASES = [
    "maybe",
    "i think",
    "i guess",
    "not sure",
    "probably",
    "perhaps"
]


def detect_repeated_words(text):
    words = text.lower().split()

    repeated = []

    for i in range(len(words) - 1):
        if words[i] == words[i + 1]:
            repeated.append(words[i])

    return repeated


def detect_uncertainty(text):
    text = text.lower()

    detected = []

    for phrase in UNCERTAINTY_PHRASES:
        if phrase in text:
            detected.append(phrase)

    return detected


def detect_long_pause(text):
    pause_markers = [
        "...",
        "....",
        "[pause]",
        "[long pause]"
    ]

    for marker in pause_markers:
        if marker in text.lower():
            return True

    return False


def analyze_confidence(text):
    repeated_words = detect_repeated_words(text)
    uncertainty = detect_uncertainty(text)
    long_pause = detect_long_pause(text)

    hesitation_count = (
        len(repeated_words)
        + len(uncertainty)
        + int(long_pause)
    )

    if hesitation_count == 0:
        confidence_score = 100
    elif hesitation_count <= 2:
        confidence_score = 80
    elif hesitation_count <= 4:
        confidence_score = 60
    else:
        confidence_score = 40

    return {
        "repeated_words": repeated_words,
        "uncertainty_phrases": uncertainty,
        "long_pause": long_pause,
        "hesitation_count": hesitation_count,
        "confidence_score": confidence_score
    }


if __name__ == "__main__":

    answer = input("Enter candidate response: ")

    result = analyze_confidence(answer)

    print("\n===== CONFIDENCE ANALYSIS =====")
    print("Repeated Words:", result["repeated_words"])
    print("Uncertainty Phrases:", result["uncertainty_phrases"])
    print("Long Pause:", result["long_pause"])
    print("Hesitation Count:", result["hesitation_count"])
    print("Confidence Score:", result["confidence_score"], "/ 100")