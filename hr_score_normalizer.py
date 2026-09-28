def normalize_interview_score(total_score, number_of_questions):
    if number_of_questions <= 0:
        return 0

    average_score = total_score / number_of_questions

    return round(average_score, 2)


if __name__ == "__main__":

    total_score = 820
    number_of_questions = 10

    normalized_score = normalize_interview_score(
        total_score,
        number_of_questions
    )

    print("===== HR SCORE NORMALIZATION =====")
    print("Total Score:", total_score)
    print("Number of Questions:", number_of_questions)
    print("Normalized Score:", normalized_score, "/ 100")