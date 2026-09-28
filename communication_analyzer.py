FILLER_WORDS = [
    "um",
    "uh",
    "like",
    "you know",
    "actually",
    "basically",
    "hmm"
]


def detect_filler_words(text):
    text = text.lower()

    detected = {}

    for filler in FILLER_WORDS:
        count = text.count(filler)

        if count > 0:
            detected[filler] = count

    return detected


def calculate_filler_score(text):
    detected = detect_filler_words(text)

    total_fillers = sum(detected.values())

    if total_fillers == 0:
        return 100

    if total_fillers <= 2:
        return 90

    if total_fillers <= 4:
        return 75

    if total_fillers <= 6:
        return 60

    return 40


if __name__ == "__main__":

    answer = input("Enter candidate answer: ")

    fillers = detect_filler_words(answer)
    score = calculate_filler_score(answer)

    print("\n===== FILLER WORD ANALYSIS =====")
    print("Detected Fillers:", fillers)
    print("Filler Word Score:", score, "/ 100")