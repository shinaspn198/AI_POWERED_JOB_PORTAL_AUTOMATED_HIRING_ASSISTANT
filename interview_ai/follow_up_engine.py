def analyze_response(response):
    response = response.strip()

    if not response:
        return "incomplete"

    if len(response.split()) <= 2:
        return "vague"

    if len(response.split()) <= 8:
        return "simple"

    return "confident"


def generate_follow_up(response, category):
    response_type = analyze_response(response)

    if response_type == "incomplete":
        return {
            "type": "clarification",
            "question": f"Could you please provide more details about your {category}?"
        }

    if response_type == "vague":
        return {
            "type": "clarification",
            "question": "Could you explain that a little more?"
        }

    if response_type == "simple":
        return {
            "type": "deepening",
            "question": f"Can you give an example related to your {category}?"
        }

    return {
        "type": "example",
        "question": "Can you describe a real situation where you demonstrated this?"
    }


if __name__ == "__main__":

    test_responses = [
        "",
        "Python",
        "I worked on an AI project",
        "I developed an AI fraud detection system using Python and machine learning."
    ]

    for response in test_responses:
        result = generate_follow_up(response, "technical skills")

        print("\nResponse:", response)
        print("Follow-up Type:", result["type"])
        print("Follow-up:", result["question"])