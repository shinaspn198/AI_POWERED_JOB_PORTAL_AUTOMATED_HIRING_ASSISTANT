def analyze_response(response):
    """
    Analyze the candidate response once and classify it.
    """

    if not isinstance(response, str):
        raise ValueError("Response must be a string.")

    response = response.strip()

    if not response:
        return "incomplete"

    word_count = len(response.split())

    if word_count <= 2:
        return "vague"

    if word_count <= 8:
        return "simple"

    return "confident"


def generate_follow_up(response, category, response_type=None):
    """
    Generate a follow-up question based on the response type.

    response_type can be passed from the decision tree so that
    the same response does not need to be analyzed again.
    """

    if response_type is None:
        response_type = analyze_response(response)

    if response_type == "incomplete":
        return {
            "type": "clarification",
            "question": (
                f"Could you please provide more details "
                f"about your {category}?"
            )
        }

    if response_type == "vague":
        return {
            "type": "clarification",
            "question": "Could you explain that a little more?"
        }

    if response_type == "simple":
        return {
            "type": "deepening",
            "question": (
                f"Can you give an example related "
                f"to your {category}?"
            )
        }

    return {
        "type": "example",
        "question": (
            "Can you describe a real situation "
            "where you demonstrated this?"
        )
    }