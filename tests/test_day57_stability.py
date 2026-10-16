"""
Unit & Integration Tests for Day 57 - System Debugging & Stabilization
"""

import pytest
import math
from unified_scoring.stability_patch import (
    ScoreSanitizer,
    ConversationGuardrail,
    ResilientPipelineRunner,
    ZecpathException,
    ScoringValidationError
)
from parsers.resume_parser import extract_text, parse_resume


def test_score_sanitizer_edge_cases():
    # String percentages
    assert ScoreSanitizer.sanitize("85.5%") == 85.5
    assert ScoreSanitizer.sanitize(" 92 ") == 92.0
    
    # Negative and overflow clamping
    assert ScoreSanitizer.sanitize(-25.0) == 0.0
    assert ScoreSanitizer.sanitize(140.0) == 100.0
    
    # NaN and Inf handling
    assert ScoreSanitizer.sanitize(float("nan"), default=50.0) == 50.0
    assert ScoreSanitizer.sanitize(float("inf"), default=50.0) == 50.0
    
    # None and invalid types
    assert ScoreSanitizer.sanitize(None, default=60.0) == 60.0
    assert ScoreSanitizer.sanitize("not-a-number", default=40.0) == 40.0


def test_conversation_guardrails():
    # Dangerous control characters and excessive length
    malicious_text = "Hello\x00\x08World! " + ("A" * 5000)
    cleaned, is_empty = ConversationGuardrail.sanitize_input(malicious_text)
    
    assert "\x00" not in cleaned
    assert "\x08" not in cleaned
    assert len(cleaned) == ConversationGuardrail.MAX_INPUT_LENGTH
    assert is_empty is False
    
    # Empty or whitespace only
    empty_res, is_empty_flag = ConversationGuardrail.sanitize_input("   \n\t  ")
    assert empty_res == ""
    assert is_empty_flag is True
    
    # Progressive recovery prompts
    p1 = ConversationGuardrail.get_fallback_recovery_prompt(1)
    p2 = ConversationGuardrail.get_fallback_recovery_prompt(2)
    p3 = ConversationGuardrail.get_fallback_recovery_prompt(3)
    
    assert "didn't quite catch that" in p1.lower()
    assert "repeat or rephrase" in p2.lower()
    assert "move on to the next" in p3.lower()


def test_resilient_stage_execution():
    def failing_stage():
        raise RuntimeError("External microservice timed out")
        
    def successful_stage():
        return 88.4
        
    # Failing stage should not crash the caller
    res_fail = ResilientPipelineRunner.safe_run_stage(failing_stage, fallback_value=65.0)
    assert res_fail == 65.0
    
    # Successful stage
    res_success = ResilientPipelineRunner.safe_run_stage(successful_stage)
    assert res_success == 88.4


def test_resume_parser_raw_text_stabilization():
    raw_resume = """
    Jane Doe
    jane@example.com
    
    SKILLS
    Python, FastAPI, SQL, Machine Learning
    
    EXPERIENCE
    Software Engineer at TechCorp
    """
    
    result = parse_resume(raw_resume)
    assert result["name"] == "Jane Doe"
    assert any("Python" in s for s in result["skills"]) or any("FastAPI" in s for s in result["skills"])
