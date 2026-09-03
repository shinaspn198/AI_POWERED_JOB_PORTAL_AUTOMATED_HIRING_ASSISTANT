from conversation_state_schema import ConversationState


def determine_next_action(state: ConversationState):
    """
    Determine the next AI conversation action
    based on the current conversation state.
    """

    # Conversation already completed
    if state.conversation_status == "completed":
        return "end_conversation"

    # Conversation failed
    if state.conversation_status == "failed":
        return "retry_or_end"

    # Silence detected
    if state.silence_count > 0:
        return "handle_silence"

    # Confusion detected
    if state.confusion_count > 0:
        return "handle_confusion"

    # Repeated answer detected
    if state.repeated_answer_count > 0:
        return "handle_repeated_answer"

    # Follow-up required
    if state.follow_up_triggered:
        return "ask_follow_up"

    # Default action
    return "continue_conversation"