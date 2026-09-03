from conversation_state_schema import ConversationState
from follow_up_handler import (
    get_fallback_question,
    trigger_follow_up
)


print("=" * 60)
print("DAY 29 - STEP 5 FALLBACK & FOLLOW-UP TEST")
print("=" * 60)


# ============================================================
# Test 1 - Technical fallback question
# ============================================================

question = get_fallback_question("technical")

print("\nTest 1 - Technical Fallback Question")
print("Question:", question)

assert question == (
    "Could you explain your technical experience with a simple example?"
)


# ============================================================
# Test 2 - Experience fallback question
# ============================================================

question = get_fallback_question("experience")

print("\nTest 2 - Experience Fallback Question")
print("Question:", question)

assert question == (
    "Could you describe one project or experience related to this?"
)


# ============================================================
# Test 3 - Skills fallback question
# ============================================================

question = get_fallback_question("skills")

print("\nTest 3 - Skills Fallback Question")
print("Question:", question)

assert question == (
    "Could you give an example of how you used this skill?"
)


# ============================================================
# Test 4 - General fallback question
# ============================================================

question = get_fallback_question("general")

print("\nTest 4 - General Fallback Question")
print("Question:", question)

assert question == (
    "Could you provide a little more information about your answer?"
)


# ============================================================
# Test 5 - Follow-up trigger
# ============================================================

state = ConversationState(
    candidate_id="CAND-001",
    current_question_id="Q001",
    current_question="Tell me about your Machine Learning experience."
)

result = trigger_follow_up(
    state,
    category="technical"
)

print("\nTest 5 - Follow-up Trigger")
print(result)

assert result["action"] == "ask_follow_up"
assert result["follow_up_triggered"] is True
assert result["question"] == (
    "Could you explain your technical experience with a simple example?"
)

assert state.follow_up_triggered is True
assert state.fallback_question == (
    "Could you explain your technical experience with a simple example?"
)


# ============================================================
# Test 6 - Unknown category
# ============================================================

question = get_fallback_question("unknown")

print("\nTest 6 - Unknown Category")
print("Question:", question)

assert question == (
    "Could you provide a little more information about your answer?"
)


print("\n" + "=" * 60)
print("DAY 29 - STEP 5 TEST PASSED")
print("=" * 60)