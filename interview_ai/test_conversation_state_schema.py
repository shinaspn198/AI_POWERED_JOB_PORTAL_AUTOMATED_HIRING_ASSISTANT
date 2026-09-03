from conversation_state_schema import ConversationState


print("=" * 60)
print("DAY 29 - STEP 1 CONVERSATION STATE SCHEMA TEST")
print("=" * 60)


state = ConversationState(
    candidate_id="CAND-001",
    current_question_id="Q001",
    current_question="Tell me about your Python experience."
)

print("\nConversation State:")
print(state)


print("\nCandidate ID:", state.candidate_id)
print("Current Question:", state.current_question)
print("Conversation Status:", state.conversation_status)
print("Silence Count:", state.silence_count)
print("Confusion Count:", state.confusion_count)
print("Repeated Answer Count:", state.repeated_answer_count)
print("Retry Count:", state.retry_count)


print("\n" + "=" * 60)
print("DAY 29 - STEP 1 TEST PASSED")
print("=" * 60)