from conversation_state_schema import ConversationState


def handle_confusion(state: ConversationState):
    """
    Handle candidate confusion during the AI screening conversation.
    """

    state.confusion_count += 1

    if state.confusion_count == 1:
        message = (
            "No problem. Let me explain the question in a simpler way."
        )

        action = "clarify_question"

    elif state.confusion_count == 2:
        message = (
            "I'll rephrase the question to make it easier to understand."
        )

        action = "rephrase_question"

    else:
        message = (
            "That's okay. We can move to the next question."
        )

        action = "move_to_next_question"

    return {
        "action": action,
        "message": message,
        "confusion_count": state.confusion_count
    }


def handle_repeated_answer(state: ConversationState):
    """
    Handle repeated candidate answers during the conversation.
    """

    state.repeated_answer_count += 1

    if state.repeated_answer_count == 1:
        message = (
            "Thank you. I noticed that your answer is similar to "
            "your previous response. Could you provide any additional details?"
        )

        action = "request_additional_details"

    elif state.repeated_answer_count == 2:
        message = (
            "Let's approach the question from a different perspective. "
            "Could you share another example?"
        )

        action = "request_different_example"

    else:
        message = (
            "Thank you. We can move forward to the next question."
        )

        action = "move_to_next_question"

    return {
        "action": action,
        "message": message,
        "repeated_answer_count": state.repeated_answer_count
    }