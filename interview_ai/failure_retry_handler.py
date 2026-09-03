from conversation_state_schema import ConversationState


MAX_RETRIES = 2


def handle_failure(state: ConversationState):
    """
    Handle a conversation failure and determine
    whether the AI should retry or end the conversation.
    """

    state.last_error = "Conversation could not be processed."

    if state.retry_count < MAX_RETRIES:
        state.retry_count += 1

        message = (
            "I'm sorry, I wasn't able to process that response. "
            "Let's try that again."
        )

        action = "retry"

    else:
        state.conversation_status = "failed"

        message = (
            "I'm sorry, but we're having difficulty continuing "
            "the conversation. We'll end the interview here. "
            "Thank you for your time."
        )

        action = "end_conversation"

    return {
        "action": action,
        "message": message,
        "retry_count": state.retry_count,
        "conversation_status": state.conversation_status
    }