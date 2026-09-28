def calculate_aptitude_score(correct_answers, total_questions):
    if total_questions <= 0:
        return 0

    score = (correct_answers / total_questions) * 100

    return round(score, 2)


if __name__ == "__main__":

    correct_answers = 8
    total_questions = 10

    score = calculate_aptitude_score(
        correct_answers,
        total_questions
    )

    print("===== APTITUDE LOGIC SCORING =====")
    print("Correct Answers:", correct_answers)
    print("Total Questions:", total_questions)
    print("Logical Reasoning Score:", score, "/ 100")