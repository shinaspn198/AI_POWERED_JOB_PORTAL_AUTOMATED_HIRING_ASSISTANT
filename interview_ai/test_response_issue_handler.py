from conversation_state_schema import ConversationState
from response_issue_handler import (
    handle_confusion,
    handle_repeated_answer
)


print("=" * 60)
print("DAY 29 - STEP 4 CONFUSION & REPEATED ANSWER TEST")
print("=" * 60)


# ============================================================
# CONFUSION TESTS
# ============================================================

state = ConversationState(
    candidate_id="CAND-001",
    current_question_id="Q001",
    current_question="Explain your Machine Learning project."
)


# Test 1 - First confusion
result = handle_confusion(state)

print("\nTest 1 - First Confusion")
print(result)

assert result["action"] == "clarify_question"
assert result["confusion_count"] == 1


# Test 2 - Second confusion
result = handle_confusion(state)

print("\nTest 2 - Second Confusion")
print(result)

assert result["action"] == "rephrase_question"
assert result["confusion_count"] == 2


# Test 3 - Third confusion
result = handle_confusion(state)

print("\nTest 3 - Third Confusion")
print(result)

assert result["action"] == "move_to_next_question"
assert result["confusion_count"] == 3


# ============================================================
# REPEATED ANSWER TESTS
# ============================================================

state = ConversationState(
    candidate_id="CAND-002",
    current_question_id="Q002",
    current_question="Tell me about your previous experience."
)


# Test 4 - First repeated answer
result = handle_repeated_answer(state)

print("\nTest 4 - First Repeated Answer")
print(result)

assert result["action"] == "request_additional_details"
assert result["repeated_answer_count"] == 1


# Test 5 - Second repeated answer
result = handle_repeated_answer(state)

print("\nTest 5 - Second Repeated Answer")
print(result)

assert result["action"] == "request_different_example"
assert result["repeated_answer_count"] == 2


# Test 6 - Third repeated answer
result = handle_repeated_answer(state)

print("\nTest 6 - Third Repeated Answer")
print(result)

assert result["action"] == "move_to_next_question"
assert result["repeated_answer_count"] == 3


print("\n" + "=" * 60)
print("DAY 29 - STEP 4 TEST PASSED")
print("=" * 60)