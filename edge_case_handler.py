def handle_edge_case(text, retry_count=0):

    MAX_RETRIES = 3

    # Missing answer
    if not text or not text.strip():
        if retry_count < MAX_RETRIES:
            return {
                "status": "retry",
                "message": "I didn't receive an answer. Please try again.",
                "retry_count": retry_count + 1
            }

        return {
            "status": "fallback",
            "message": "I'm unable to get your answer after multiple attempts."
        }

    text = text.strip()

    # Unclear answer
    unclear_words = ["uh", "hmm", "noise", "unclear"]

    if text.lower() in unclear_words:

        if retry_count < MAX_RETRIES:
            return {
                "status": "retry",
                "message": "I couldn't clearly understand your answer. Please repeat it.",
                "retry_count": retry_count + 1
            }

        return {
            "status": "fallback",
            "message": "I'm still unable to understand your answer."
        }

    # Valid answer
    return {
        "status": "success",
        "message": "Answer received",
        "answer": text
    }
def detect_language_mixing(text):

    if not text or not text.strip():
        return {
            "status": "missing",
            "message": "No answer provided."
        }

    words = text.split()

    # Very basic indicator of mixed-language input
    english_words = 0
    other_words = 0

    for word in words:
        if word.isascii():
            english_words += 1
        else:
            other_words += 1

    if english_words > 0 and other_words > 0:
        return {
            "status": "mixed_language",
            "message": "Mixed language detected. Continue processing the answer.",
            "text": text
        }

    return {
        "status": "normal",
        "message": "No language mixing detected.",
        "text": text
    }
def handle_audio_quality(text, confidence=1.0):

    if not text or not text.strip():
        return {
            "status": "retry",
            "message": "No clear audio was detected. Please speak again."
        }

    if confidence < 0.5:
        return {
            "status": "retry",
            "message": "The audio was unclear. Please speak clearly and try again."
        }

    if confidence < 0.7:
        return {
            "status": "warning",
            "message": "The audio quality is low. Please try to speak more clearly.",
            "text": text
        }

    return {
        "status": "success",
        "message": "Audio quality is acceptable.",
        "text": text
    }
def process_answer(text, confidence=1.0, retry_count=0):

    # 1. Check audio quality
    audio_result = handle_audio_quality(text, confidence)

    if audio_result["status"] == "retry":
        return audio_result

    # 2. Check missing / unclear answer
    answer_result = handle_edge_case(text, retry_count)

    if answer_result["status"] != "success":
        return answer_result

    # 3. Detect language mixing
    language_result = detect_language_mixing(text)

    # 4. Final result
    return {
        "status": "success",
        "answer": text,
        "language_status": language_result["status"],
        "audio_confidence": confidence
    }
def handle_background_noise(text, confidence=1.0):
    if not text or not text.strip():
        return {
            "status": "retry",
            "message": "Background noise or unclear audio detected. Please speak again."
        }

    if confidence < 0.4:
        return {
            "status": "retry",
            "message": "Too much background noise detected. Please move to a quieter place and try again."
        }

    if confidence < 0.7:
        return {
            "status": "warning",
            "message": "Some background noise was detected. Please speak clearly.",
            "text": text
        }

    return {
        "status": "success",
        "message": "Audio is clear enough to continue.",
        "text": text
    }