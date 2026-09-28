HR_WEIGHTS = {
    "answer_relevance": 0.30,
    "communication": 0.25,
    "confidence": 0.25,
    "consistency": 0.20
}


def get_weights():
    return HR_WEIGHTS


if __name__ == "__main__":
    print("===== HR WEIGHT CONFIGURATION =====")

    for parameter, weight in HR_WEIGHTS.items():
        print(parameter, ":", weight * 100, "%")

    print("\nTotal Weight:", sum(HR_WEIGHTS.values()) * 100, "%")