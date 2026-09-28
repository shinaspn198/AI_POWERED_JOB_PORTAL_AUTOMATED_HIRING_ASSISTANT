class InterviewState:

    def __init__(self):
        self.current_question_id = 1
        self.responses = []
        self.follow_up_allowed = True

    def capture_response(self, question_id, question, response):
        self.responses.append({
            "question_id": question_id,
            "question": question,
            "response": response
        })

    def can_follow_up(self):
        return self.follow_up_allowed

    def get_responses(self):
        return self.responses


if __name__ == "__main__":

    interview = InterviewState()

    interview.capture_response(
        1,
        "Tell me about yourself.",
        "I am a BCA student specializing in AI."
    )

    print("===== INTERVIEW STATE =====")
    print("Current Question ID:", interview.current_question_id)
    print("Follow-up Allowed:", interview.can_follow_up())
    print("Responses:", interview.get_responses())