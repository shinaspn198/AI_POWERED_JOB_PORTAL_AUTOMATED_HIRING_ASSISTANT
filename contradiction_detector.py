def detect_contradiction(previous_answer, current_answer):
    previous = previous_answer.lower()
    current = current_answer.lower()

    contradictions = []

    contradiction_pairs = [
        ("experience", "no experience"),
        ("experienced", "no experience"),
        ("yes", "no"),
        ("always", "never"),
        ("can", "cannot"),
        ("comfortable", "uncomfortable"),
        ("available", "unavailable")
    ]

    for word1, word2 in contradiction_pairs:

        if word1 in previous and word2 in current:
            contradictions.append((word1, word2))

        elif word2 in previous and word1 in current:
            contradictions.append((word2, word1))

    return contradictions


if __name__ == "__main__":

    previous = input("Enter previous answer: ")
    current = input("Enter current answer: ")

    contradictions = detect_contradiction(
        previous,
        current
    )

    print("\n===== CONTRADICTION ANALYSIS =====")
    print("Contradictions:", contradictions)

    if contradictions:
        print("Status: Possible contradiction detected")
    else:
        print("Status: No contradiction detected")