from follow_up_engine import analyze_response, generate_follow_up


def adapt_question(response, category, asked_questions):

    response_type = analyze_response(response)

    follow_up = generate_follow_up(response, category)

    question = follow_up["question"]

    # Prevent repetitive questions
    if question in asked_questions:
        return {
            "action": "continue",
            "message": "Move to the next question."
        }

    return {
        "action": "follow_up",
        "response_type": response_type,
        "follow_up_type": follow_up["type"],
        "question": question
    }


if __name__ == "__main__":

    asked_questions = []

    response = "I worked on an AI project"

    result = adapt_question(
        response,
        "technical skills",
        asked_questions
    )

    print("===== ADAPTIVE QUESTIONING =====")
    print("Response Type:", result["response_type"])
    print("Follow-up Type:", result["follow_up_type"])
    print("Next Question:", result["question"])