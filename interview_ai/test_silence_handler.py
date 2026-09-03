from conversation_state_schema import ConversationState
from silence_handler import handle_silence


print("=" * 60)
print("DAY 29 - STEP 3 SILENCE HANDLING TEST")
print("=" * 60)


# Test 1 - First silence
state = ConversationState(
    candidate_id="CAND-001",
    current_question_id="Q001",
    current_question="Tell me about your Python experience."
)

result = handle_silence(state)

print("\nTest 1 - First Silence")
print(result)

assert result["action"] == "wait_for_response"
assert result["silence_count"] == 1


# Test 2 - Second silence
result = handle_silence(state)

print("\nTest 2 - Second Silence")
print(result)

assert result["action"] == "offer_question_repeat"
assert result["silence_count"] == 2


# Test 3 - Third silence
result = handle_silence(state)

print("\nTest 3 - Third Silence")
print(result)

assert result["action"] == "move_to_next_question"
assert result["silence_count"] == 3


print("\n" + "=" * 60)
print("DAY 29 - STEP 3 TEST PASSED")
print("=" * 60)