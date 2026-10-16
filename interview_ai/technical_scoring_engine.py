"""
Day 47 - Technical Skill Scoring Model

Purpose:
Evaluate technical answers using the four scoring parameters
defined in the Day 47 requirements.
"""

from vague_answer_detector import detect_vague_answer


# =========================================================
# TECHNICAL SCORING PARAMETERS
# =========================================================

TECHNICAL_SCORING_PARAMETERS = {
    "accuracy": "Accuracy of Answer",
    "depth": "Depth of Explanation",
    "logical_reasoning": "Logical Reasoning",
    "real_world_applicability": "Real-World Applicability",
}


def get_technical_scoring_parameters():
    """Return the technical scoring parameters."""
    return TECHNICAL_SCORING_PARAMETERS.copy()


def get_parameter_names():
    """Return the technical scoring parameter names."""
    return list(TECHNICAL_SCORING_PARAMETERS.keys())


# =========================================================
# QUESTION TYPE RUBRICS
# =========================================================

QUESTION_TYPE_RUBRICS = {

    "introduction": {
        "accuracy": "Correct technical background and skills.",
        "depth": "Clearly explains technical skills and knowledge.",
        "logical_reasoning": (
            "Presents technical background and experience logically."
        ),
        "real_world_applicability": (
            "Connects technical skills to actual projects or work."
        ),
    },

    "experience_based": {
        "accuracy": "Correctly describes technical experience.",
        "depth": "Explains technical work and contributions in detail.",
        "logical_reasoning": (
            "Explains technical decisions and problem-solving logically."
        ),
        "real_world_applicability": (
            "Shows how technology was applied in actual work or projects."
        ),
    },

    "conceptual": {
        "accuracy": "Provides a technically correct explanation.",
        "depth": "Explains the concept beyond a basic definition.",
        "logical_reasoning": (
            "Explains relationships, causes, or technical behavior logically."
        ),
        "real_world_applicability": (
            "Connects the concept to practical usage."
        ),
    },

    "scenario_based": {
        "accuracy": "Provides a technically appropriate solution.",
        "depth": "Explains the proposed solution sufficiently.",
        "logical_reasoning": (
            "Demonstrates a logical problem-solving approach."
        ),
        "real_world_applicability": (
            "Applies technical knowledge to the given real-world scenario."
        ),
    },
}


def get_question_type_rubric(question_type):
    """Return the rubric for a specific question type."""
    return QUESTION_TYPE_RUBRICS.get(question_type)


def get_question_types():
    """Return all supported question types."""
    return list(QUESTION_TYPE_RUBRICS.keys())


# =========================================================
# TECHNICAL ANSWER DEPTH DETECTION
# =========================================================

def detect_answer_depth(answer):
    """
    Detect whether a technical answer is vague, shallow, or deep.

    This is a qualitative classification.
    It does not assign a numerical score.
    """

    if not isinstance(answer, str):
        return {
            "depth_level": "vague",
            "reason": "Answer is not valid text.",
        }

    text = " ".join(answer.lower().strip().split())

    if not text:
        return {
            "depth_level": "vague",
            "reason": "No technical explanation was provided.",
        }

    # Use the existing vague-answer detector.
    if detect_vague_answer(answer):
        return {
            "depth_level": "vague",
            "reason": (
                "Answer does not provide a clear technical explanation."
            ),
        }

    words = text.split()

    # Very short answers provide limited explanation.
    if len(words) <= 5:
        return {
            "depth_level": "shallow",
            "reason": (
                "Answer provides a technical response but "
                "limited explanation."
            ),
        }

    depth_indicators = [
        "because",
        "therefore",
        "for example",
        "for instance",
        "in practice",
        "the reason",
        "when",
        "if",
        "however",
        "compared to",
        "such as",
        "works by",
        "used to",
        "implemented",
        "architecture",
        "trade-off",
        "tradeoff",
    ]

    indicator_count = sum(
        1 for indicator in depth_indicators
        if indicator in text
    )

    if indicator_count > 0:
        return {
            "depth_level": "deep",
            "reason": (
                "Answer contains additional technical explanation "
                "or reasoning."
            ),
        }

    return {
        "depth_level": "shallow",
        "reason": (
            "Answer provides a technical response but limited "
            "additional explanation or reasoning."
        ),
    }


# =========================================================
# EXPLAINABLE SCORING OUTPUT
# =========================================================

def build_explainable_scoring_output(
    question_type,
    scores,
    depth_level,
    difficulty_level=None,
):
    """
    Build an explainable technical scoring output.
    """

    return {
        "question_type": question_type,
        "difficulty_level": difficulty_level,
        "scores": {
            "accuracy": scores.get("accuracy"),
            "depth": scores.get("depth"),
            "logical_reasoning": scores.get("logical_reasoning"),
            "real_world_applicability": scores.get(
                "real_world_applicability"
            ),
        },
        "answer_depth": depth_level,
        "explanation": {
            "accuracy": (
                "Measures the correctness of the technical answer."
            ),
            "depth": (
                "Measures how deeply the candidate explains the concept."
            ),
            "logical_reasoning": (
                "Measures the logical approach used in the answer."
            ),
            "real_world_applicability": (
                "Measures how the candidate connects knowledge "
                "to practical situations."
            ),
        },
    }


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    print("=" * 60)
    print("DAY 47 - EXPLAINABLE TECHNICAL SCORING")
    print("=" * 60)

    sample_scores = {
        "accuracy": 20,
        "depth": 18,
        "logical_reasoning": 19,
        "real_world_applicability": 17,
    }

    test_answers = [
        "Python is a programming language.",
        (
            "Python is an interpreted language. "
            "It is commonly used for automation and machine learning "
            "because it has a large ecosystem of libraries."
        ),
        "I don't know.",
    ]

    for answer in test_answers:

        depth_result = detect_answer_depth(answer)

        print("\nAnswer:")
        print(answer)

        print(
            f"Depth Level : {depth_result['depth_level']}"
        )

        print(
            f"Reason      : {depth_result['reason']}"
        )

    result = build_explainable_scoring_output(
        question_type="conceptual",
        scores=sample_scores,
        depth_level="deep",
        difficulty_level="intermediate",
    )

    print("\nQuestion Type:", result["question_type"])
    print("Difficulty:", result["difficulty_level"])
    print("Answer Depth:", result["answer_depth"])

    print("\nScores:")

    for parameter, score in result["scores"].items():
        print(f"{parameter}: {score}")

    print("\nExplanations:")

    for parameter, explanation in result["explanation"].items():
        print(f"{parameter}: {explanation}")

    print("\n" + "=" * 60)
    print("STEP 5 COMPLETED")
    print("=" * 60)