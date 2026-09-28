def calculate_communication_score(
    fluency,
    grammar,
    vocabulary,
    clarity,
    filler_words,
    structure
):
    score = (
        fluency * 0.20 +
        grammar * 0.20 +
        vocabulary * 0.15 +
        clarity * 0.20 +
        filler_words * 0.10 +
        structure * 0.15
    )

    return round(score, 2)


if __name__ == "__main__":

    score = calculate_communication_score(
        fluency=80,
        grammar=75,
        vocabulary=70,
        clarity=85,
        filler_words=90,
        structure=80
    )

    print("===== COMMUNICATION SKILL EVALUATION =====")
    print("Fluency: 80")
    print("Grammar: 75")
    print("Vocabulary: 70")
    print("Clarity: 85")
    print("Filler Words: 90")
    print("Answer Structure: 80")

    print("\nCommunication Score:", score, "/ 100")