import re


STOP_WORDS = {
    "i", "am", "is", "are", "the", "a", "an",
    "and", "or", "to", "of", "in", "for",
    "my", "have", "has", "with", "do", "did",
    "what", "how", "why", "you", "your",
    "which", "can", "could", "would"
}


CONCEPT_GROUPS = {
    "skills": {
        "skill", "skills", "programming", "technology",
        "technologies", "python", "fastapi", "machine",
        "learning", "java", "javascript", "sql", "react"
    },

    "experience": {
        "experience", "experienced", "worked",
        "working", "years", "project", "projects"
    },

    "education": {
        "education", "degree", "college", "university",
        "bca", "btech", "mca", "qualification"
    },

    "availability": {
        "available", "availability", "join", "joining",
        "immediate", "notice", "days", "week", "weeks"
    },

    "salary": {
        "salary", "expected", "expectation", "lpa",
        "pay", "compensation", "lakhs"
    },

    "location": {
        "location", "located", "city", "place",
        "bangalore", "kochi", "remote"
    }
}


def clean_text(text):
    """
    Convert text into normalized keywords.
    """

    text = text.lower()

    words = re.findall(r"\b[a-zA-Z0-9]+\b", text)

    keywords = [
        word
        for word in words
        if word not in STOP_WORDS
    ]

    return set(keywords)


def detect_concepts(keywords):
    """
    Detect HR screening concepts present in a set of keywords.
    """

    concepts = set()

    for concept, concept_words in CONCEPT_GROUPS.items():

        if keywords.intersection(concept_words):
            concepts.add(concept)

    return concepts


def analyze_relevance(question, answer):
    """
    Analyze how relevant a candidate's answer is
    to the interview question.
    """

    if not isinstance(question, str):
        raise ValueError("Question must be a string.")

    if not isinstance(answer, str):
        raise ValueError("Answer must be a string.")

    question = question.strip()
    answer = answer.strip()

    if not question:
        raise ValueError("Question cannot be empty.")

    question_keywords = clean_text(question)
    answer_keywords = clean_text(answer)

    if not answer:
        return {
            "question_keywords": sorted(question_keywords),
            "answer_keywords": [],
            "matched_keywords": [],
            "question_concepts": [],
            "answer_concepts": [],
            "matched_concepts": [],
            "match_count": 0,
            "concept_match_count": 0,
            "relevance_score": 0,
            "relevance_level": "irrelevant"
        }

    matched_keywords = question_keywords.intersection(
        answer_keywords
    )

    question_concepts = detect_concepts(
        question_keywords
    )

    answer_concepts = detect_concepts(
        answer_keywords
    )

    matched_concepts = question_concepts.intersection(
        answer_concepts
    )

    match_count = len(matched_keywords)
    concept_match_count = len(matched_concepts)

    answer_word_count = len(answer_keywords)

    # Prevent extremely short answers from
    # receiving a full relevance score.
    if answer_word_count == 1 and match_count > 0:
        return {
            "question_keywords": sorted(question_keywords),
            "answer_keywords": sorted(answer_keywords),
            "matched_keywords": sorted(matched_keywords),
            "question_concepts": sorted(question_concepts),
            "answer_concepts": sorted(answer_concepts),
            "matched_concepts": sorted(matched_concepts),
            "match_count": match_count,
            "concept_match_count": concept_match_count,
            "relevance_score": 20,
            "relevance_level": "partially_relevant"
        }

    keyword_score = 0

    if question_keywords:
        keyword_score = (
            match_count / len(question_keywords)
        ) * 100

    concept_score = 0

    if question_concepts:
        concept_score = (
            concept_match_count / len(question_concepts)
        ) * 100

    # Use the stronger signal between exact keyword
    # matching and domain concept matching.
    relevance_score = round(
        max(keyword_score, concept_score),
        2
    )

    if relevance_score >= 50:
        relevance_level = "relevant"

    elif relevance_score >= 20:
        relevance_level = "partially_relevant"

    else:
        relevance_level = "irrelevant"

    return {
        "question_keywords": sorted(question_keywords),
        "answer_keywords": sorted(answer_keywords),
        "matched_keywords": sorted(matched_keywords),
        "question_concepts": sorted(question_concepts),
        "answer_concepts": sorted(answer_concepts),
        "matched_concepts": sorted(matched_concepts),
        "match_count": match_count,
        "concept_match_count": concept_match_count,
        "relevance_score": relevance_score,
        "relevance_level": relevance_level
    }