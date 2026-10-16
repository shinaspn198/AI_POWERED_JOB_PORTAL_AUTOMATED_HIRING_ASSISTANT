import math


def normalize_interview_score(total_score, number_of_questions):
    """
    Safely calculates normalized interview score per question.
    Guards against ZeroDivisionError, None inputs, strings, and non-numeric payloads.
    """
    if not number_of_questions or number_of_questions <= 0:
        return 0.0

    if total_score is None:
        return 0.0

    try:
        t_val = float(total_score)
        q_val = float(number_of_questions)
        if math.isnan(t_val) or math.isinf(t_val):
            return 0.0
        avg = t_val / q_val
        return max(0.0, min(100.0, round(avg, 2)))
    except (ValueError, TypeError):
        return 0.0


if __name__ == "__main__":
    total_score = 820
    number_of_questions = 10
    normalized_score = normalize_interview_score(total_score, number_of_questions)
    print("===== HR SCORE NORMALIZATION =====")
    print("Total Score:", total_score)
    print("Number of Questions:", number_of_questions)
    print("Normalized Score:", normalized_score, "/ 100")