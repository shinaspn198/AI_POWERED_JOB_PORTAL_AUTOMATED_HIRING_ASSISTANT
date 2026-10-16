import re


FILLER_WORDS = [
    "uh",
    "uhh",
    "um",
    "umm",
    "er",
    "err",
    "you know",
]


def clean_transcript(text):

    if not isinstance(text, str):
        raise ValueError("Transcript must be a string.")

    text = text.strip()

    if not text:
        return ""

    # Remove filler words
    for filler in FILLER_WORDS:
        text = re.sub(
            rf"\b{re.escape(filler)}\b",
            "",
            text,
            flags=re.IGNORECASE
        )

    # Remove repeated dots
    text = re.sub(r"\.{2,}", ".", text)

    # Remove spaces before punctuation
    text = re.sub(r"\s+([,.!?])", r"\1", text)

    # Remove unnecessary punctuation at the beginning
    text = re.sub(r"^[.,!?]+\s*", "", text)

    # Normalize spaces
    text = re.sub(r"\s+", " ", text).strip()

    # Remove punctuation that became isolated after filler removal
    text = re.sub(r"\s+\.", ".", text)

    # Capitalize the first character
    if text:
        text = text[0].upper() + text[1:]

    # Add final punctuation
    if text and text[-1] not in ".!?":
        text += "."

    return text


if __name__ == "__main__":

    raw = "Uhh... I have   two years um of experience in Python and Fast API"

    print("Raw:", raw)
    print("Cleaned:", clean_transcript(raw))