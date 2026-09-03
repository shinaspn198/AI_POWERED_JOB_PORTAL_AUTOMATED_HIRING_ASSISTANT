from conversation_state_schema import ConversationState


FALLBACK_QUESTIONS = {
    "technical": "Could you explain your technical experience with a simple example?",
    "experience": "Could you describe one project or experience related to this?",
    "skills": "Could you give an example of how you used this skill?",
    "general": "Could you provide a little more information about your answer?"
}


def get_fallback_question(category="general"):
    """
    Return a fallback question based on the conversation category.
    """

    return FALLBACK_QUESTIONS.get(
        category,
        FALLBACK_QUESTIONS["general"]
    )


def trigger_follow_up(
    state: ConversationState,
    category="general"
):
    """
    Trigger a follow-up question when additional information is required.
    """

    state.follow_up_triggered = True

    state.fallback_question = get_fallback_question(category)

    return {
        "action": "ask_follow_up",
        "question": state.fallback_question,
        "follow_up_triggered": state.follow_up_triggered
    }