"""
Day 54 - Intent Refinement & Conversational Disambiguation Engine

Provides robust intent detection for conversational screening:
- Negation handling ("haven't worked with", "not experienced in")
- Multi-intent classification (affirmation, qualification, deflection, clarifying question)
- Confidence scoring and boundary validation
"""

import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass


@dataclass
class IntentClassificationResult:
    primary_intent: str
    confidence: float
    is_negated: bool
    detected_entities: List[str]
    qualifiers: List[str]
    explanation: str


class ConversationalIntentRefiner:
    """Refined intent classifier for screening & interview conversations."""

    NEGATION_PATTERNS = [
        r"\b(?:not|never|haven't|havent|have not|don't|dont|do not|didn't|didnt|did not|rarely|hardly)\b",
        r"\b(?:no experience|zero experience|lack(?:ing)? experience|no exposure)\b",
        r"\b(?:cannot|can't|cant|unable to)\b",
    ]

    INTENT_KEYWORDS = {
        "CONFIRM_EXPERIENCE": [
            r"\b(?:worked on|built|designed|implemented|architected|maintained|deployed|scaled|developed)\b",
            r"\b(?:production experience|in production|hands-on|day-to-day|daily)\b",
        ],
        "QUALIFIED_EXPERIENCE": [
            r"\b(?:academic|coursework|tutorial|side project|hobby|personal project|bootcamp)\b",
            r"\b(?:basic|fundamental|familiar with|know the basics|conceptual)\b",
        ],
        "THEORETICAL_KNOWLEDGE": [
            r"\b(?:understand the concept|theoretically|read about|studied|know how it works)\b",
            r"\b(?:architecture principles|in theory)\b",
        ],
        "CLARIFICATION_REQUEST": [
            r"\b(?:could|can|would)\s+(?:you\s+)?(?:please\s+)?(?:clarify|repeat|rephrase|explain)\b",
            r"\b(?:what\s+do\s+you\s+mean|are\s+you\s+asking\s+about|do\s+you\s+mean)\b",
            r"\b(?:clarify|rephrase|repeat\s+the\s+question)\b",
        ],
        "DEFLECTION_OR_UNCERTAIN": [
            r"\b(?:not sure|no idea|don't recall|cannot remember|skip this|pass)\b",
            r"\b(?:haven't done this|haven't dealt with)\b",
        ],
    }

    TECH_ENTITIES = [
        "python", "fastapi", "django", "flask", "docker", "kubernetes", "k8s",
        "postgresql", "postgres", "sql", "redis", "celery", "react", "vue",
        "aws", "gcp", "azure", "git", "ci/cd", "microservices", "graphql", "rest"
    ]

    def classify_intent(self, text: str, expected_topic: Optional[str] = None) -> IntentClassificationResult:
        """Classifies conversational input with negation and entity extraction."""
        if not text or not text.strip():
            return IntentClassificationResult(
                primary_intent="EMPTY_RESPONSE",
                confidence=1.0,
                is_negated=False,
                detected_entities=[],
                qualifiers=[],
                explanation="Candidate provided empty or whitespace-only response."
            )

        clean_text = text.lower().strip()

        # Check for negation
        is_negated = any(re.search(pat, clean_text) for pat in self.NEGATION_PATTERNS)

        # Detect technical entities
        detected_entities = [
            entity for entity in self.TECH_ENTITIES
            if re.search(r"\b" + re.escape(entity) + r"\b", clean_text)
        ]

        # Score intents
        intent_scores: Dict[str, float] = {k: 0.0 for k in self.INTENT_KEYWORDS.keys()}
        for intent, patterns in self.INTENT_KEYWORDS.items():
            for pat in patterns:
                matches = re.findall(pat, clean_text)
                intent_scores[intent] += len(matches) * 1.5

        # Check clarification first
        if intent_scores["CLARIFICATION_REQUEST"] > 0:
            return IntentClassificationResult(
                primary_intent="CLARIFICATION_REQUEST",
                confidence=0.92,
                is_negated=is_negated,
                detected_entities=detected_entities,
                qualifiers=["clarification"],
                explanation="Candidate requested clarification on the question."
            )

        # Handle negation logic
        if is_negated:
            if "CONFIRM_EXPERIENCE" in intent_scores and intent_scores["CONFIRM_EXPERIENCE"] > 0:
                # E.g. "I haven't worked on Kubernetes in production, but..."
                if intent_scores["QUALIFIED_EXPERIENCE"] > 0 or intent_scores["THEORETICAL_KNOWLEDGE"] > 0:
                    return IntentClassificationResult(
                        primary_intent="QUALIFIED_EXPERIENCE",
                        confidence=0.88,
                        is_negated=True,
                        detected_entities=detected_entities,
                        qualifiers=["negation_on_production", "theoretical_backup"],
                        explanation="Candidate acknowledged lack of production experience but indicated foundational knowledge."
                    )
                else:
                    return IntentClassificationResult(
                        primary_intent="DEFLECTION_OR_UNCERTAIN",
                        confidence=0.90,
                        is_negated=True,
                        detected_entities=detected_entities,
                        qualifiers=["no_experience"],
                        explanation="Candidate explicitly confirmed lack of experience on the subject."
                    )

        # Determine primary intent
        max_intent = max(intent_scores, key=intent_scores.get)
        max_score = intent_scores[max_intent]

        if max_score == 0:
            # Fallback based on length and relevance
            if len(clean_text.split()) > 15:
                primary_intent = "CONFIRM_EXPERIENCE"
                confidence = 0.65
            else:
                primary_intent = "GENERAL_STATEMENT"
                confidence = 0.50
        else:
            primary_intent = max_intent
            confidence = min(0.95, 0.60 + max_score * 0.15)

        qualifiers = []
        if is_negated:
            qualifiers.append("negated")
        if detected_entities:
            qualifiers.append("tech_entities_present")

        return IntentClassificationResult(
            primary_intent=primary_intent,
            confidence=round(confidence, 2),
            is_negated=is_negated,
            detected_entities=detected_entities,
            qualifiers=qualifiers,
            explanation=f"Classified as '{primary_intent}' with {confidence*100:.0f}% confidence."
        )
