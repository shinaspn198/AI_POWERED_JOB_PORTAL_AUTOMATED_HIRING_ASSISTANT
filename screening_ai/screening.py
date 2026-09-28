from question_engine import build_conversation_objects
def run_screening():
    """Run the AI screening question flow."""

    questions = build_conversation_objects()

    print("\n===== AI SCREENING SYSTEM =====")
    print(f"Total questions: {len(questions)}")

    answers = []

    for question in questions:
        print(f"\nCategory: {question['category']}")
        print(f"Question: {question['prompt']}")

        answer = input("Candidate Answer: ")

        answers.append({
            "question_id": question["question_id"],
            "category": question["category"],
            "question": question["prompt"],
            "answer": answer,
            "mandatory": question["mandatory"],
            "scoring_importance": question["scoring_importance"]
        })

    print("\n===== SCREENING COMPLETED =====")

    for item in answers:
        print(f"\nQuestion: {item['question']}")
        print(f"Answer: {item['answer']}")

    return answers


if __name__ == "__main__":
    run_screening()