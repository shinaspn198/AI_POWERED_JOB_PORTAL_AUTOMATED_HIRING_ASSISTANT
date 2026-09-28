REASONING_QUESTIONS = [
    {
        "id": 1,
        "question": "If 2, 4, 8, 16, what comes next?",
        "answer": "32",
        "type": "number_series"
    },
    {
        "id": 2,
        "question": "If all developers know Python and Rahul is a developer, does Rahul know Python?",
        "answer": "yes",
        "type": "logical_reasoning"
    },
    {
        "id": 3,
        "question": "A project has 10 tasks. 6 are completed. How many remain?",
        "answer": "4",
        "type": "basic_logic"
    }
]


def get_questions():
    return REASONING_QUESTIONS


if __name__ == "__main__":
    print("===== APTITUDE AI QUESTION ENGINE =====")

    questions = get_questions()

    for question in questions:
        print("\nQuestion", question["id"])
        print(question["question"])
        print("Type:", question["type"])