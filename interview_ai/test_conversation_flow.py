from conversation_state_schema import ConversationState
from conversation_flow import process_conversation


print("=" * 60)
print("DAY 29 - STEP 7 COMPLETE CONVERSATION FLOW TEST")
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
# Test 2 - Silence
# ============================================================

state = ConversationState(
    candidate_id="CAND-001",
    current_question_id="Q002",
    current_question="Tell me about your projects.",
    silence_count=0
)

# First mark silence so the decision tree detects it.
state.silence_count = 1

result = process_conversation(state)

print("\nTest 2 - Silence Handling")
print(result)

assert result["action"] == "offer_question_repeat"
assert state.silence_count == 2


# ============================================================
# Test 3 - Confusion
# ============================================================

state = ConversationState(
    candidate_id="CAND-001",
    current_question_id="Q003",
    current_question="Explain your machine learning experience.",
    confusion_count=0
)

state.confusion_count = 1

result = process_conversation(state)

print("\nTest 3 - Confusion Handling")
print(result)

assert result["action"] == "rephrase_question"
assert state.confusion_count == 2


# ============================================================
# Test 4 - Repeated answer
# ============================================================

state = ConversationState(
    candidate_id="CAND-001",
    current_question_id="Q004",
    current_question="Describe another project.",
    repeated_answer_count=0
)

state.repeated_answer_count = 1

result = process_conversation(state)

print("\nTest 4 - Repeated Answer Handling")
print(result)

assert result["action"] == "request_different_example"
assert state.repeated_answer_count == 2


# ============================================================
# Test 5 - Follow-up
# ============================================================

state = ConversationState(
    candidate_id="CAND-001",
    current_question_id="Q005",
    current_question="Tell me about your skills.",
    follow_up_triggered=True,
    fallback_question="Could you give an example of how you used this skill?"
)

result = process_conversation(state)

print("\nTest 5 - Follow-up Handling")
print(result)

assert result["action"] == "ask_follow_up"


# ============================================================
# Test 6 - Completed conversation
# ============================================================

state = ConversationState(
    candidate_id="CAND-001",
    conversation_status="completed"
)

result = process_conversation(state)

print("\nTest 6 - Completed Conversation")
print(result)

assert result["action"] == "end_conversation"


# ============================================================
# Test 7 - Failed conversation
# ============================================================

state = ConversationState(
    candidate_id="CAND-001",
    conversation_status="failed"
)

result = process_conversation(state)

print("\nTest 7 - Failed Conversation")
print(result)

assert result["action"] == "retry"


print("\n" + "=" * 60)
print("DAY 29 - STEP 7 TEST PASSED")
print("=" * 60)