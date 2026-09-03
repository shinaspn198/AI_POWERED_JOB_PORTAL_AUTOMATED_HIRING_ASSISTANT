from conversation_state_schema import ConversationState
from conversation_decision_tree import determine_next_action


print("=" * 60)
print("DAY 29 - STEP 2 AI CALL DECISION TREE TEST")
print("=" * 60)


# Test 1 - Normal conversation
state = ConversationState(
    candidate_id="CAND-001",
    current_question_id="Q001",
    current_question="Tell me about your Python experience."
)

action = determine_next_action(state)

print("\nTest 1 - Normal Conversation")
print("Expected: continue_conversation")
print("Actual:", action)

assert action == "continue_conversation"


# Test 2 - Silence
state = ConversationState(
    candidate_id="CAND-002",
    current_question_id="Q002",
    current_question="What is your experience with Machine Learning?",
    silence_count=1
)

action = determine_next_action(state)

print("\nTest 2 - Silence Detected")
print("Expected: handle_silence")
print("Actual:", action)

assert action == "handle_silence"


# Test 3 - Confusion
state = ConversationState(
    candidate_id="CAND-003",
    current_question_id="Q003",
    current_question="Explain your previous project.",
    confusion_count=1
)

action = determine_next_action(state)

print("\nTest 3 - Confusion Detected")
print("Expected: handle_confusion")
print("Actual:", action)

assert action == "handle_confusion"


# Test 4 - Repeated answer
state = ConversationState(
    candidate_id="CAND-004",
    current_question_id="Q004",
    current_question="Why should we hire you?",
    repeated_answer_count=1
)

action = determine_next_action(state)

print("\nTest 4 - Repeated Answer")
print("Expected: handle_repeated_answer")
print("Actual:", action)

assert action == "handle_repeated_answer"


# Test 5 - Follow-up
state = ConversationState(
    candidate_id="CAND-005",
    current_question_id="Q005",
    current_question="Tell me about your FastAPI experience.",
    follow_up_triggered=True
)

action = determine_next_action(state)

print("\nTest 5 - Follow-up Triggered")
print("Expected: ask_follow_up")
print("Actual:", action)

assert action == "ask_follow_up"


# Test 6 - Completed conversation
state = ConversationState(
    candidate_id="CAND-006",
    current_question_id="Q006",
    current_question="Do you have any questions?",
    conversation_status="completed"
)

action = determine_next_action(state)

print("\nTest 6 - Conversation Completed")
print("Expected: end_conversation")
print("Actual:", action)

assert action == "end_conversation"


# Test 7 - Failed conversation
state = ConversationState(
    candidate_id="CAND-007",
    current_question_id="Q007",
    current_question="Tell me about yourself.",
    conversation_status="failed"
)

action = determine_next_action(state)

print("\nTest 7 - Conversation Failed")
print("Expected: retry_or_end")
print("Actual:", action)

assert action == "retry_or_end"


print("\n" + "=" * 60)
print("DAY 29 - STEP 2 TEST PASSED")
print("=" * 60)