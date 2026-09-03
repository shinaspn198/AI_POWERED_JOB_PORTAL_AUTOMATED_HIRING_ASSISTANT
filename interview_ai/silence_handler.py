from conversation_state_schema import ConversationState


def handle_silence(state: ConversationState):
    """
    Handle silence during an AI screening conversation.
    """

    state.silence_count += 1

    if state.silence_count == 1:
        message = (
            "I didn't hear a response. Please take your time and answer "
            "when you're ready."
        )

        action = "wait_for_response"

    elif state.silence_count == 2:
        message = (
            "It seems you may need a little more time. "
            "Would you like me to repeat the question?"
        )

        action = "offer_question_repeat"

    else:
        message = (
            "I understand. We can move on to the next question."
        )

        action = "move_to_next_question"

    return {
        "action": action,
        "message": message,
        "silence_count": state.silence_count
    }