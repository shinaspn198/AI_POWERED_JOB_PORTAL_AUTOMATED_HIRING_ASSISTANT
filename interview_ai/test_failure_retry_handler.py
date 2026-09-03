from conversation_state_schema import ConversationState
from failure_retry_handler import handle_failure


print("=" * 60)
print("DAY 29 - STEP 6 FAILURE & RETRY LOGIC TEST")
print("=" * 60)


# ============================================================
# Test 1 - First failure
# ============================================================

state = ConversationState(
    candidate_id="CAND-001",
    current_question_id="Q001",
    current_question="Tell me about your Python experience."
)

result = handle_failure(state)

print("\nTest 1 - First Failure")
print(result)

assert result["action"] == "retry"
assert result["retry_count"] == 1
assert result["conversation_status"] == "active"


# ============================================================
# Test 2 - Second failure
# ============================================================

result = handle_failure(state)

print("\nTest 2 - Second Failure")
print(result)

assert result["action"] == "retry"
assert result["retry_count"] == 2
assert result["conversation_status"] == "active"


# ============================================================
# Test 3 - Maximum retries exceeded
# ============================================================

result = handle_failure(state)

print("\nTest 3 - Maximum Retries Exceeded")
print(result)

assert result["action"] == "end_conversation"
assert result["retry_count"] == 2
assert result["conversation_status"] == "failed"


# ============================================================
# Test 4 - Error information stored
# ============================================================

print("\nTest 4 - Error Information")
print("Last Error:", state.last_error)

assert state.last_error == "Conversation could not be processed."


print("\n" + "=" * 60)
print("DAY 29 - STEP 6 TEST PASSED")
print("=" * 60)