from dataclasses import dataclass, field
from typing import List


@dataclass
class ConversationState:
    """
    Represents the current state of an AI screening conversation.
    """

    candidate_id: str
    current_question_id: str = ""
    current_question: str = ""

    conversation_status: str = "active"

    last_answer: str = ""
    previous_answers: List[str] = field(default_factory=list)

    silence_count: int = 0
    confusion_count: int = 0
    repeated_answer_count: int = 0
    retry_count: int = 0

    fallback_question: str = ""
    follow_up_triggered: bool = False

    last_error: str = ""