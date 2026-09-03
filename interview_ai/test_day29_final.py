from conversation_state_schema import ConversationState
from conversation_flow import process_conversation


print("=" * 60)
print("DAY 29 - FINAL CONVERSATION FLOW VALIDATION")
print("=" * 60)


# ============================================================
# Test 1 - Normal conversation
# ============================================================

state = ConversationState(
    candidate_id="CAND-001",
    current_question_id="Q001",
    current_question="Tell me about your Python experience."
)

result = process_conversation(state)

print("\nTest 1 - Normal Conversation")
print(result)

assert result["action"] == "continue_conversation"


# ============================================================
# Test 2 - Silence handling
# ============================================================

state = ConversationState(
    candidate_id="CAND-001",
    current_question_id="Q002",
    silence_count=1
)

result = process_conversation(state)

print("\nTest 2 - Silence Handling")
print(result)

assert result["action"] == "offer_question_repeat"


# ============================================================
# Test 3 - Confusion handling
# ============================================================

state = ConversationState(
    candidate_id="CAND-001",
    current_question_id="Q003",
    confusion_count=1
)

result = process_conversation(state)

print("\nTest 3 - Confusion Handling")
print(result)

assert result["action"] == "rephrase_question"


# ============================================================
# Test 4 - Repeated answer handling
# ============================================================

state = ConversationState(
    candidate_id="CAND-001",
    current_question_id="Q004",
    repeated_answer_count=1
)

result = process_conversation(state)

print("\nTest 4 - Repeated Answer Handling")
print(result)

assert result["action"] == "request_different_example"


# ============================================================
# Test 5 - Follow-up question
# ============================================================

state = ConversationState(
    candidate_id="CAND-001",
    current_question_id="Q005",
    follow_up_triggered=True,
    fallback_question="Could you give an example of how you used this skill?"
)

result = process_conversation(state)

print("\nTest 5 - Follow-up Question")
print(result)

assert result["action"] == "ask_follow_up"


# ============================================================
# Test 6 - Failure and retry
# ============================================================

state = ConversationState(
    candidate_id="CAND-001",
    current_question_id="Q006"
)

state.conversation_status = "failed"

result = process_conversation(state)

print("\nTest 6 - Failure & Retry")
print(result)

assert result["action"] == "retry"
assert result["retry_count"] == 1


# ============================================================
# Test 7 - Completed conversation
# ============================================================

state = ConversationState(
    candidate_id="CAND-001",
    conversation_status="completed"
)

result = process_conversation(state)

print("\nTest 7 - Completed Conversation")
print(result)

assert result["action"] == "end_conversation"


# ============================================================
# Final validation
# ============================================================

print("\n" + "=" * 60)
print("ALL DAY 29 CONVERSATION FLOW TESTS PASSED")
print("=" * 60)
print("Day 29 AI Conversation Flow Validation: SUCCESS")
print("=" * 60)