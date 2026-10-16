"""
Day 42 - Stable Vague Answer Detection

Purpose:
Reduce false positives while detecting genuinely vague answers.
"""

VAGUE_PHRASES = {
    "not sure",
    "i don't know",
    "don't know",
    "anything is fine",
    "it depends",
    "somewhere",
    "perhaps",
    "probably",
}


def detect_vague_answer(answer: str) -> bool:
    """
    Detect whether an answer is genuinely vague.
    """

    if not isinstance(answer, str):
        return False

    text = " ".join(answer.lower().strip().split())

    if not text:
        return False

    words = text.split()

    if len(words) <= 2:
        return True

    if any(phrase in text for phrase in VAGUE_PHRASES):
        return True

    return False