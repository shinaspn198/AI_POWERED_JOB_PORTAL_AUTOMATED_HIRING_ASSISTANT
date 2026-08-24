import re


def analyze_answer(answer):
    """
    Analyze the quality of a candidate's interview answer.
    """

    if not isinstance(answer, str):
        raise ValueError("Answer must be a string.")

    answer = answer.strip()

    # Empty answer
    if not answer:
        return {
            "word_count": 0,
            "sentence_count": 0,
            "has_content": False,
            "is_too_short": True,
            "quality_level": "poor"
        }

    # Count words
    words = answer.split()
    word_count = len(words)

    # Count sentences
    sentences = re.split(r"[.!?]+", answer)
    sentences = [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]

    sentence_count = len(sentences)

    has_content = word_count > 0

    # Short-answer detection
    is_too_short = word_count < 4

    # Quality classification
    if word_count < 4:
        quality_level = "poor"

    elif word_count < 10:
        quality_level = "moderate"

    else:
        quality_level = "good"

    return {
        "word_count": word_count,
        "sentence_count": sentence_count,
        "has_content": has_content,
        "is_too_short": is_too_short,
        "quality_level": quality_level
    }