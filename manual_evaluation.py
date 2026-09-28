MANUAL_EVALUATION = {
    "Confident": {
        "communication": 90,
        "confidence": 95,
        "problem_solving": 85,
        "overall": 90
    },

    "Hesitant": {
        "communication": 65,
        "confidence": 55,
        "problem_solving": 75,
        "overall": 65
    },

    "Inexperienced": {
        "communication": 70,
        "confidence": 65,
        "problem_solving": 60,
        "overall": 65
    },

    "Overqualified": {
        "communication": 90,
        "confidence": 90,
        "problem_solving": 95,
        "overall": 92
    }
}


if __name__ == "__main__":

    print("===== MANUAL HR EVALUATION =====")

    for candidate_type, scores in MANUAL_EVALUATION.items():

        print("\nCandidate Type:", candidate_type)

        print("Communication:", scores["communication"])
        print("Confidence:", scores["confidence"])
        print("Problem Solving:", scores["problem_solving"])
        print("Overall Score:", scores["overall"])