"""
Day 50 - Machine Test AI Design & Evaluation Engine

Purpose:
Evaluate real-world technical skills via interactive coding problems,
debugging tasks, file-based challenges, and mini system designs using
automated execution sandbox telemetry, code snapshot tracking, and
time-weighted multi-metric scoring.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum


# =========================================================
# 1. MACHINE TEST TYPES DEFINITION
# =========================================================

class MachineTestType(str, Enum):
    CODING_PROBLEM = "coding_problems"
    DEBUGGING_TASK = "debugging_tasks"
    FILE_BASED_TASK = "file_based_tasks"
    MINI_SYSTEM_DESIGN = "mini_system_design"


MACHINE_TEST_TYPES: Dict[str, Dict[str, Any]] = {
    MachineTestType.CODING_PROBLEM.value: {
        "name": "Coding Problems",
        "description": "Algorithmic and data structure challenges requiring logic implementation against test suites.",
        "primary_focus": ["algorithms", "edge_case_handling", "runtime_complexity"],
        "default_time_minutes": 30,
    },
    MachineTestType.DEBUGGING_TASK.value: {
        "name": "Debugging Tasks",
        "description": "Troubleshoot pre-existing buggy codebases to diagnose, patch, and regression-test fixes.",
        "primary_focus": ["root_cause_analysis", "minimal_diff_fix", "regression_prevention"],
        "default_time_minutes": 25,
    },
    MachineTestType.FILE_BASED_TASK.value: {
        "name": "File-Based Tasks",
        "description": "Real-world project tasks involving file I/O, parsing (JSON/CSV), schema transformations, and API data flows.",
        "primary_focus": ["file_io", "data_transformation", "error_handling"],
        "default_time_minutes": 45,
    },
    MachineTestType.MINI_SYSTEM_DESIGN.value: {
        "name": "Mini System Design",
        "description": "Implementation of micro-architectural components (e.g., rate limiter, LRU cache, pub-sub queue).",
        "primary_focus": ["modularity", "interface_design", "concurrency_or_state"],
        "default_time_minutes": 45,
    },
}


def get_test_types() -> Dict[str, Dict[str, Any]]:
    """Return all defined machine test types."""
    return MACHINE_TEST_TYPES.copy()


# =========================================================
# 2. INPUT / OUTPUT CAPTURE SCHEMAS
# =========================================================

@dataclass
class CodeSnapshot:
    """Captures time-series telemetry of code evolution and keystroke diffs."""
    timestamp_sec: float
    snapshot_index: int
    char_count: int
    line_count: int
    diff_size: int
    is_run_trigger: bool = False
    paste_detected: bool = False


@dataclass
class ExecutionResult:
    """Captures sandbox execution runtime output and test pass rates."""
    total_test_cases: int
    passed_test_cases: int
    failed_test_cases: int
    execution_time_ms: float
    memory_used_mb: float
    exit_code: int = 0
    stdout: str = ""
    stderr: str = ""
    timeout_occurred: bool = False


@dataclass
class TaskSubmission:
    """Full candidate task submission payload."""
    test_type: MachineTestType
    source_code: str
    time_taken_seconds: float
    expected_time_seconds: float
    max_allowed_seconds: float
    execution_result: ExecutionResult
    snapshots: List[CodeSnapshot] = field(default_factory=list)


# =========================================================
# 3. TASK EVALUATION METRICS & SCORING LOGIC
# =========================================================

METRIC_WEIGHTS = {
    "correctness": 0.40,
    "efficiency": 0.20,
    "code_quality": 0.20,
    "problem_solving_approach": 0.20,
}


class MachineTestEvaluator:
    """Evaluates submissions across correctness, efficiency, code quality, approach, and timing."""

    def __init__(self, weights: Optional[Dict[str, float]] = None):
        self.weights = weights or METRIC_WEIGHTS

    def evaluate_correctness(self, exec_result: ExecutionResult) -> float:
        """Score (0-100) based on test cases passed and execution stability."""
        if exec_result.total_test_cases <= 0:
            return 0.0
        if exec_result.timeout_occurred:
            return max(0.0, round((exec_result.passed_test_cases / exec_result.total_test_cases) * 50.0, 2))

        pass_ratio = exec_result.passed_test_cases / exec_result.total_test_cases
        score = pass_ratio * 100.0
        if exec_result.exit_code != 0:
            score = max(0.0, score - 20.0)
        return round(score, 2)

    def evaluate_efficiency(
        self,
        exec_result: ExecutionResult,
        benchmark_ms: float = 100.0,
        benchmark_mb: float = 64.0
    ) -> float:
        """Score (0-100) based on runtime and memory consumption relative to benchmarks."""
        if exec_result.timeout_occurred or exec_result.passed_test_cases == 0:
            return 0.0

        # Runtime efficiency
        if exec_result.execution_time_ms <= benchmark_ms:
            runtime_score = 100.0
        elif exec_result.execution_time_ms <= benchmark_ms * 3:
            runtime_score = 80.0
        elif exec_result.execution_time_ms <= benchmark_ms * 10:
            runtime_score = 50.0
        else:
            runtime_score = 25.0

        # Memory efficiency
        if exec_result.memory_used_mb <= benchmark_mb:
            mem_score = 100.0
        elif exec_result.memory_used_mb <= benchmark_mb * 2:
            mem_score = 75.0
        else:
            mem_score = 50.0

        return round(runtime_score * 0.70 + mem_score * 0.30, 2)

    def evaluate_code_quality(self, source_code: str) -> float:
        """Score (0-100) based on modularity, naming, line length, and structure."""
        if not source_code.strip():
            return 0.0

        score = 100.0
        lines = source_code.splitlines()

        # Penalize excessive line lengths (> 100 chars)
        long_lines = [l for l in lines if len(l) > 100]
        if len(long_lines) > 5:
            score -= 10.0

        # Reward functions / modular breakdown
        has_functions = any("def " in l or "function " in l or "class " in l for l in lines)
        if not has_functions:
            score -= 25.0

        # Check for meaningful comments or docstrings
        has_comments = any("#" in l or "//" in l or '"""' in l for l in lines)
        if not has_comments:
            score -= 10.0

        # Penalize single-letter variable names proliferation
        single_char_vars = sum(1 for l in lines if " = " in l and len(l.split("=")[0].strip()) == 1)
        if single_char_vars > 4:
            score -= 10.0

        return max(0.0, round(score, 2))

    def evaluate_problem_solving_approach(self, snapshots: List[CodeSnapshot]) -> float:
        """Score (0-100) based on incremental iteration, test-run cadence, and copy-paste signals."""
        if not snapshots:
            return 70.0  # Baseline when no granular snapshot telemetry is available

        score = 80.0
        run_triggers = sum(1 for s in snapshots if s.is_run_trigger)
        paste_events = sum(1 for s in snapshots if s.paste_detected)

        # Iterative testing bonus (candidate ran tests 3-10 times during development)
        if 3 <= run_triggers <= 15:
            score += 15.0
        elif run_triggers == 0:
            score -= 20.0  # Never tested before final submission

        # Deduct for abrupt large pastes without incremental typing
        if paste_events >= 2:
            score -= 25.0
        elif paste_events == 1:
            score -= 10.0

        # Smooth evolution bonus
        if len(snapshots) >= 5:
            score += 5.0

        return min(100.0, max(0.0, round(score, 2)))

    def calculate_time_factor(
        self,
        time_taken_seconds: float,
        expected_time_seconds: float,
        max_allowed_seconds: float
    ) -> float:
        """
        Time multiplier:
        - 1.05 to 1.10 (fast completion with correct solution)
        - 1.00 (within expected time)
        - 0.80 to 0.95 (between expected and max time)
        - 0.50 (exceeded max allowed time)
        """
        if time_taken_seconds > max_allowed_seconds:
            return 0.50
        if time_taken_seconds <= expected_time_seconds * 0.75:
            return 1.10
        if time_taken_seconds <= expected_time_seconds:
            return 1.00

        # Linear decay between expected and max
        ratio = (time_taken_seconds - expected_time_seconds) / (max_allowed_seconds - expected_time_seconds)
        decay = 1.00 - (0.25 * ratio)
        return round(decay, 2)

    def evaluate_submission(self, submission: TaskSubmission) -> Dict[str, Any]:
        """Produce the comprehensive machine test evaluation."""
        correctness = self.evaluate_correctness(submission.execution_result)
        efficiency = self.evaluate_efficiency(submission.execution_result)
        code_quality = self.evaluate_code_quality(submission.source_code)
        approach = self.evaluate_problem_solving_approach(submission.snapshots)

        base_score = (
            correctness * self.weights["correctness"]
            + efficiency * self.weights["efficiency"]
            + code_quality * self.weights["code_quality"]
            + approach * self.weights["problem_solving_approach"]
        )

        time_factor = self.calculate_time_factor(
            submission.time_taken_seconds,
            submission.expected_time_seconds,
            submission.max_allowed_seconds
        )

        # Apply time factor (bonus only if correctness is at least 70)
        if time_factor > 1.0 and correctness < 70.0:
            final_score = base_score
        else:
            final_score = base_score * time_factor

        final_score = min(100.0, max(0.0, round(final_score, 2)))

        # Performance Tier & Hiring Fit
        if final_score >= 85.0:
            grade = "STRONG_HIRE"
        elif final_score >= 70.0:
            grade = "HIRE"
        elif final_score >= 50.0:
            grade = "NEEDS_IMPROVEMENT"
        else:
            grade = "REJECT"

        return {
            "test_type": submission.test_type.value,
            "final_score": final_score,
            "performance_grade": grade,
            "metrics": {
                "correctness": correctness,
                "efficiency": efficiency,
                "code_quality": code_quality,
                "problem_solving_approach": approach,
            },
            "timing": {
                "time_taken_seconds": submission.time_taken_seconds,
                "expected_time_seconds": submission.expected_time_seconds,
                "max_allowed_seconds": submission.max_allowed_seconds,
                "time_factor": time_factor,
            },
            "sandbox": {
                "tests_passed": f"{submission.execution_result.passed_test_cases}/{submission.execution_result.total_test_cases}",
                "runtime_ms": submission.execution_result.execution_time_ms,
                "memory_mb": submission.execution_result.memory_used_mb,
            }
        }


# =========================================================
# TEST RUN
# =========================================================

if __name__ == "__main__":
    print("=" * 65)
    print("DAY 50 - MACHINE TEST AI EVALUATION DEMO")
    print("=" * 65)

    evaluator = MachineTestEvaluator()

    # Scenario: Candidate completing a Coding Problem (Binary Search / Cache)
    submission = TaskSubmission(
        test_type=MachineTestType.CODING_PROBLEM,
        source_code=(
            "class LRUCache:\n"
            "    def __init__(self, capacity: int):\n"
            "        self.capacity = capacity\n"
            "        self.cache = {}\n\n"
            "    def get(self, key: int) -> int:\n"
            "        # Retrieve and mark as recently used\n"
            "        if key not in self.cache:\n"
            "            return -1\n"
            "        val = self.cache.pop(key)\n"
            "        self.cache[key] = val\n"
            "        return val\n\n"
            "    def put(self, key: int, value: int) -> None:\n"
            "        if key in self.cache:\n"
            "            self.cache.pop(key)\n"
            "        elif len(self.cache) >= self.capacity:\n"
            "            del self.cache[next(iter(self.cache))]\n"
            "        self.cache[key] = value\n"
        ),
        time_taken_seconds=1200.0,       # 20 mins
        expected_time_seconds=1800.0,   # 30 mins
        max_allowed_seconds=2700.0,     # 45 mins
        execution_result=ExecutionResult(
            total_test_cases=10,
            passed_test_cases=10,
            failed_test_cases=0,
            execution_time_ms=45.2,
            memory_used_mb=28.5,
            exit_code=0
        ),
        snapshots=[
            CodeSnapshot(timestamp_sec=100.0, snapshot_index=1, char_count=80, line_count=4, diff_size=80),
            CodeSnapshot(timestamp_sec=350.0, snapshot_index=2, char_count=210, line_count=10, diff_size=130, is_run_trigger=True),
            CodeSnapshot(timestamp_sec=700.0, snapshot_index=3, char_count=350, line_count=18, diff_size=140, is_run_trigger=True),
            CodeSnapshot(timestamp_sec=1150.0, snapshot_index=4, char_count=420, line_count=22, diff_size=70, is_run_trigger=True),
        ]
    )

    result = evaluator.evaluate_submission(submission)

    print(f"Test Type         : {result['test_type']}")
    print(f"Final Score       : {result['final_score']} / 100")
    print(f"Grade             : {result['performance_grade']}")
    print("\nMetric Breakdown:")
    for k, v in result['metrics'].items():
        print(f" - {k.replace('_', ' ').title():<25}: {v}/100")
    print("\nTiming & Sandbox:")
    print(f" - Tests Passed    : {result['sandbox']['tests_passed']}")
    print(f" - Runtime         : {result['sandbox']['runtime_ms']} ms")
    print(f" - Memory          : {result['sandbox']['memory_mb']} MB")
    print(f" - Time Factor     : {result['timing']['time_factor']}x")
    print("\n" + "=" * 65)
    print("STEP COMPLETED")
    print("=" * 65)
