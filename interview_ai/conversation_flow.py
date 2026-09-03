from conversation_state_schema import ConversationState
from conversation_decision_tree import determine_next_action
from silence_handler import handle_silence
from response_issue_handler import (
    handle_confusion,
    handle_repeated_answer
)
from follow_up_handler import trigger_follow_up
from failure_retry_handler import handle_failure


def process_conversation(state: ConversationState):
    """
    Process the current conversation state and
    determine the next AI conversation action.
    """

    action = determine_next_action(state)

    if action == "handle_silence":
        return handle_silence(state)

    elif action == "handle_confusion":
        return handle_confusion(state)

    elif action == "handle_repeated_answer":
        return handle_repeated_answer(state)

    elif action == "ask_follow_up":
        return {
            "action": "ask_follow_up",
            "question": state.fallback_question,
            "follow_up_triggered": state.follow_up_triggered
        }

    elif action == "retry_or_end":
        return handle_failure(state)

    elif action == "end_conversation":
        return {
            "action": "end_conversation",
            "message": "Thank you for your time.",
            "conversation_status": state.conversation_status
        }

    return {
        "action": "continue_conversation",
        "message": "Let's continue with the next question.",
        "conversation_status": state.conversation_status
    }