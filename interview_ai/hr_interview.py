from hr_question_engine import generate_questions
from interview_state import InterviewState


def run_interview(candidate_type, role_type):
    questions = generate_questions(candidate_type, role_type)
    interview = InterviewState()

    print("\n===== AI HR INTERVIEW =====")
    print("Candidate Type:", candidate_type)
    print("Role Type:", role_type)

    # Phase 1
    print("\n--- INTRODUCTION ---")

    for question in questions[:2]:
        print(
            f"\nQuestion {question['question_id']}: "
            f"{question['question']}"
        )

        answer = input("Candidate: ")

        interview.capture_response(
            question["question_id"],
            question["question"],
            answer
        )

    # Phase 2
    print("\n--- CORE HR QUESTIONS ---")

    for question in questions[2:10]:
        print(
            f"\nQuestion {question['question_id']}: "
            f"{question['question']}"
        )

        answer = input("Candidate: ")

        interview.capture_response(
            question["question_id"],
            question["question"],
            answer
        )

    # Phase 3
    print("\n--- ROLE-BASED EVALUATION ---")

    for question in questions[10:]:
        print(
            f"\nQuestion {question['question_id']}: "
            f"{question['question']}"
        )

        answer = input("Candidate: ")

        interview.capture_response(
            question["question_id"],
            question["question"],
            answer
        )

    # Phase 4
    print("\n--- CLOSING ---")
    print("Thank you for completing the HR interview.")

    responses = interview.get_responses()

    print("\n===== INTERVIEW COMPLETED =====")
    print("Total Responses:", len(responses))

    # Return the actual live interview responses
    return responses


if __name__ == "__main__":
    run_interview("fresher", "technical")