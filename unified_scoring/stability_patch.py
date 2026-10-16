"""
Day 57 - System Stability, Exception Hierarchy & Input Sanitization Patch

Stabilizes AI evaluation pipeline against:
- Non-numeric, NaN, negative, or >100 score inputs
- Corrupt/unreadable file inputs and unicode errors
- Empty, malicious, or excessively long conversational inputs
- Pipeline crashes with graceful fallback defaults
"""

import math
import re
import unicodedata
from typing import Dict, List, Any, Optional, Tuple


# =========================================================
# 1. CENTRALIZED EXCEPTION HIERARCHY
# =========================================================

class ZecpathException(Exception):
    """Base exception for all Zecpath AI hiring system errors."""
    def __init__(self, message: str, error_code: str = "INTERNAL_ERROR"):
        super().__init__(message)
        self.message = message
        self.error_code = error_code


class ScoringValidationError(ZecpathException):
    """Raised when score inputs violate range [0, 100] or numeric contracts."""
    def __init__(self, message: str):
        super().__init__(message, error_code="INVALID_SCORE")


class DataIngestionError(ZecpathException):
    """Raised when resume or candidate document is unreadable or malformed."""
    def __init__(self, message: str):
        super().__init__(message, error_code="DATA_INGESTION_FAILED")


class ConversationalFlowError(ZecpathException):
    """Raised on conversational timeouts, dead-ends, or unparseable dialogue."""
    def __init__(self, message: str):
        super().__init__(message, error_code="CONVERSATION_ERROR")


# =========================================================
# 2. NUMERIC SCORE SANITIZER & BOUND ENFORCER
# =========================================================

class ScoreSanitizer:
    """Clamps and validates numeric scores strictly into safe [0.0, 100.0] bounds."""

    @staticmethod
    def sanitize(value: Any, default: float = 0.0, stage_name: str = "Stage") -> float:
        """Converts arbitrary input to safe 0.0 - 100.0 float without throwing."""
        if value is None:
            return float(default)

        # Handle string inputs like "85.5%" or " 92 "
        if isinstance(value, str):
            clean_str = value.replace("%", "").strip()
            try:
                numeric_val = float(clean_str)
            except ValueError:
                return float(default)
        elif isinstance(value, (int, float)):
            numeric_val = float(value)
        else:
            return float(default)

        # Handle NaN or Inf
        if math.isnan(numeric_val) or math.isinf(numeric_val):
            return float(default)

        # Clamping
        return round(max(0.0, min(100.0, numeric_val)), 2)

    @classmethod
    def sanitize_stage_dict(cls, stages: Dict[str, Any]) -> Dict[str, float]:
        """Sanitizes dictionary of stage scores."""
        return {k: cls.sanitize(v, default=0.0, stage_name=k) for k, v in stages.items()}


# =========================================================
# 3. CONVERSATIONAL INPUT SANITIZER & RECOVERY
# =========================================================

class ConversationGuardrail:
    """Sanitizes conversational inputs and handles recovery prompts."""

    MAX_INPUT_LENGTH = 4000

    @classmethod
    def sanitize_input(cls, user_text: Optional[str]) -> Tuple[str, bool]:
        """
        Normalizes unicode, strips dangerous control characters, and enforces length.
        Returns: (sanitized_text, is_empty_flag)
        """
        if user_text is None:
            return "", True

        # Normalize unicode
        text = unicodedata.normalize("NFKC", str(user_text))

        # Remove null bytes and non-printable control characters (except newline and tab)
        text = "".join(ch for ch in text if ch in ("\n", "\t") or not unicodedata.category(ch).startswith("C"))

        # Strip whitespace
        text = text.strip()

        if not text:
            return "", True

        # Truncate if exceeds maximum length
        if len(text) > cls.MAX_INPUT_LENGTH:
            text = text[:cls.MAX_INPUT_LENGTH]

        return text, False

    @staticmethod
    def get_fallback_recovery_prompt(silence_or_empty_count: int, stage: str = "screening") -> str:
        """Generates friendly conversational recovery prompts when candidate inputs fail."""
        if silence_or_empty_count == 1:
            return (
                "I didn't quite catch that. Could you please share your experience or answer "
                "when you're ready?"
            )
        elif silence_or_empty_count == 2:
            return (
                "No problem! Take your time. Would you like me to repeat or rephrase the question?"
            )
        else:
            return (
                "It looks like we might be experiencing an audio or network delay. "
                "Let's move on to the next question, and we can revisit this topic at the end."
            )


# =========================================================
# 4. RESILIENT EVALUATION PIPELINE RUNNER
# =========================================================

class ResilientPipelineRunner:
    """Wraps stage executions with comprehensive safety fallbacks."""

    @staticmethod
    def safe_run_stage(stage_func, fallback_value: float = 50.0, *args, **kwargs) -> float:
        """Executes an evaluation stage function safely, returning fallback on unexpected error."""
        try:
            raw_result = stage_func(*args, **kwargs)
            return ScoreSanitizer.sanitize(raw_result, default=fallback_value)
        except Exception:
            return float(fallback_value)
