import re


HESITATION_PATTERNS = [
    "uh",
    "uhh",
    "um",
    "umm",
    "er",
    "err",
    "hmm",
    "maybe",
    "perhaps",
    "i think",
    "i guess",
    "not sure",
    "i'm not sure",
    "im not sure",
    "probably",
    "possibly",
    "kind of",
    "sort of",
]


def normalize_text(text):
    """
    Normalize candidate response text.
    """

    if not isinstance(text, str):
        return ""

    text = text.lower().strip()

    return text


def detect_hesitation(text):
    """
    Detect hesitation patterns in a candidate response.

    Returns:
        dict containing hesitation count,
        detected patterns, and hesitation indicator.
    """

    text = normalize_text(text)

    if not text:
        return {
            "has_hesitation": False,
            "hesitation_count": 0,
            "patterns": [],
        }

    detected_patterns = []
    hesitation_count = 0

    for pattern in HESITATION_PATTERNS:

        if " " in pattern:
            matches = re.findall(
                rf"\b{re.escape(pattern)}\b",
                text
            )
        else:
            matches = re.findall(
                rf"\b{re.escape(pattern)}\b",
                text
            )

        if matches:
            detected_patterns.append(pattern)
            hesitation_count += len(matches)

    return {
        "has_hesitation": hesitation_count > 0,
        "hesitation_count": hesitation_count,
        "patterns": detected_patterns,
    }


def analyze_confidence(text):
    """
    Analyze confidence-related hesitation signals.
    """

    result = detect_hesitation(text)

    if result["hesitation_count"] == 0:
        confidence_level = "high"

    elif result["hesitation_count"] <= 2:
        confidence_level = "moderate"

    else:
        confidence_level = "low"

    result["confidence_level"] = confidence_level

    return result