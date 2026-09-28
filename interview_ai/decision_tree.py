from follow_up_engine import analyze_response, generate_follow_up


class ConversationState:

    def __init__(self):
        self.asked_questions = []
        self.responses = []
        self.follow_up_count = 0

    def add_response(self, question, response):
        self.responses.append({
            "question": question,
            "response": response
        })

    def add_question(self, question):
        if question not in self.asked_questions:
            self.asked_questions.append(question)

    def can_follow_up(self):
        return self.follow_up_count < 2


def decide_next_action(response, category, state):

    response_type = analyze_response(response)

    # Incomplete or vague → clarification
    if response_type in ["incomplete", "vague"]:
        follow_up = generate_follow_up(response, category)

    # Simple → deeper probe
    elif response_type == "simple":
        follow_up = generate_follow_up(response, category)

    # Confident → example/scenario
    else:
        follow_up = generate_follow_up(response, category)

    question = follow_up["question"]

    # Prevent repetitive questioning
    if question in state.asked_questions:
        return "next_question", None

    # Limit excessive follow-ups
    if not state.can_follow_up():
        return "next_question", None

    state.follow_up_count += 1
    state.add_question(question)

    return "follow_up", {
        "type": follow_up["type"],
        "question": question
    }


if __name__ == "__main__":

    state = ConversationState()

    original_question = "Tell me about your technical skills."
    state.add_question(original_question)

    response = "I know Python and machine learning."

    state.add_response(original_question, response)

    action, result = decide_next_action(
        response,
        "technical skills",
        state
    )

    print("===== DECISION TREE =====")
    print("Action:", action)

    if result:
        print("Follow-up Type:", result["type"])
        print("Next Question:", result["question"])

    print("Follow-up Count:", state.follow_up_count)
    print("Responses Stored:", len(state.responses))