HR_QUESTIONS = {
    "self_introduction": [
        "Tell me about yourself.",
        "Can you briefly describe your professional background?"
    ],

    "career_journey": [
        "Can you describe your career journey?",
        "What motivated you to choose this career?"
    ],

    "strengths_weaknesses": [
        "What are your greatest strengths?",
        "What is one weakness you are working to improve?"
    ],

    "teamwork_culture": [
        "How do you work in a team?",
        "How do you handle disagreements with team members?"
    ],

    "career_goals": [
        "What are your career goals?",
        "Where do you see yourself in the next few years?"
    ],

    "availability_commitment": [
        "When can you start?",
        "Are you comfortable committing to this role?"
    ]
}


def generate_questions(candidate_type, role_type):
    questions = []

    for category, category_questions in HR_QUESTIONS.items():
        for question in category_questions:
            questions.append({
                "question_id": len(questions) + 1,
                "category": category,
                "question": question,
                "candidate_type": candidate_type,
                "role_type": role_type,
                "follow_up_allowed": True
            })

    return questions


if __name__ == "__main__":
    questions = generate_questions("fresher", "technical")

    print("===== HR INTERVIEW QUESTION ENGINE =====")
    print("Candidate Type: Fresher")
    print("Role Type: Technical")
    print("Total Questions:", len(questions))

    for question in questions:
        print(
            f"{question['question_id']}. "
            f"[{question['category']}] "
            f"{question['question']}"
        )