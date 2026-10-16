# Day 50 – Machine Test AI Design

## 1. Machine Test AI Framework

The Machine Test AI Framework automates technical skill assessments by embedding candidate activity within a secure execution sandbox, collecting fine-grained input/output telemetry, and evaluating real-world engineering proficiency across four distinct test paradigms.

```
+--------------------+      +--------------------+      +-------------------------+
| Candidate IDE      | ---> | Sandboxed Runtime  | ---> | Multi-Metric Scorer     |
| (Snapshots/Diffs)  |      | (Execution/Stdout) |      | (Correctness, Efficacy) |
+--------------------+      +--------------------+      +-------------------------+
                                                                     |
                                                                     v
                                                        [ Time-Weighted Grade ]
                                                        (STRONG_HIRE, HIRE, etc.)
```

### Types of Machine Tests

| Test Type | Description | Key Focus Areas | Default Time Limit |
|---|---|---|---|
| **Coding Problems** | Algorithmic and data structure challenges implemented against public and private unit test suites. | Algorithm design, boundary & edge cases, time/space complexity | 30 minutes |
| **Debugging Tasks** | Inspecting pre-existing broken codebases to isolate defects, apply minimal patches, and pass regression suites. | Root cause analysis, code navigation, regression avoidance | 25 minutes |
| **File-Based Tasks** | Real-world practical engineering involving file parsing (JSON, CSV), data serialization, schema validations, and file I/O. | Schema safety, file handling, exception handling, data pipelines | 45 minutes |
| **Mini System Design** | Modular component development (e.g., custom LRU Cache, Rate Limiter, Event Pub-Sub, In-Memory DB). | Modularity, interface segregation, clean architecture, concurrency | 45 minutes |

---

## 2. Input / Output Capture Architecture

### A. Code Snapshots Telemetry
Captured periodically (keystroke batching) and on every run trigger:
* **Time-series diffs:** Line and character changes per snapshot to measure implementation velocity.
* **Run triggers:** Timestamp and frequency of candidate-initiated test runs.
* **Copy-paste indicators:** Detects sudden mass insertions (>150 characters with zero typing trajectory) to identify unauthorized external code pasting.

### B. Execution Results Telemetry
Captured inside isolated containerized sandboxes (gVisor/Docker):
* **Test Case Outcomes:** Ratio of passed, failed, and timeout test cases (public vs. hidden).
* **Process Exit Code:** Normal termination (`0`), syntax/runtime exceptions (`1`), or signal interruptions (`SIGKILL`, `SIGSEGV`).
* **Resource Consumption:** Execution wall-clock time (ms) and peak resident memory usage (MB).
* **Standard Streams:** Captured `stdout` and `stderr` for stack trace analysis and debugging hygiene.

---

## 3. Task Evaluation Metrics

The evaluation weights balance functional correctness with production engineering standards:

$$\text{Base Score} = (0.40 \times \text{Correctness}) + (0.20 \times \text{Efficiency}) + (0.20 \times \text{Code Quality}) + (0.20 \times \text{Problem Solving Approach})$$

| Evaluation Metric | Weight | Measurement Criteria |
|---|---|---|
| **Correctness** | 40% | Test suite pass rate (public & hidden edge cases), zero unhandled runtime crashes or exit failures. |
| **Efficiency** | 20% | Execution runtime (ms) and memory footprint (MB) benchmarked against $O(N)$ reference baselines. |
| **Code Quality** | 20% | Modularity (functions/classes), naming conventions, docstrings, absence of monolithic scripts, lint standards. |
| **Problem-Solving Approach** | 20% | Iterative development cadence, healthy test execution frequency, lack of anomalous bulk copy-pastes. |

---

## 4. Time-Based Scoring Logic

Time-to-solution is used as an efficiency multiplier rather than a binary cutoff:

$$\text{Time Multiplier} = f(T_{\text{taken}}, T_{\text{expected}}, T_{\text{max}})$$

* **Early Completion Bonus ($T_{\text{taken}} \le 0.75 \times T_{\text{expected}}$):** Multiplier of **$1.10\times$** (applicable only if correctness $\ge 70\%$).
* **Standard Completion ($T_{\text{taken}} \le T_{\text{expected}}$):** Multiplier of **$1.00\times$**.
* **Delayed Completion ($T_{\text{expected}} < T_{\text{taken}} \le T_{\text{max}}$):** Linear decay from $1.00\times$ down to $0.75\times$:
  $$\text{Multiplier} = 1.00 - 0.25 \times \left(\frac{T_{\text{taken}} - T_{\text{expected}}}{T_{\text{max}} - T_{\text{expected}}}\right)$$
* **Overtime / Hard Timeout ($T_{\text{taken}} > T_{\text{max}}$):** Multiplier capped at **$0.50\times$**.

---

## 5. Performance Grading & Hiring Fit

$$\text{Final Score} = \min(100, \max(0, \text{Base Score} \times \text{Time Multiplier}))$$

* **STRONG_HIRE ($\ge 85$ pts):** Solution passes all test suites, optimal efficiency, clean modular code, completed within expected time.
* **HIRE ($70\text{--}84$ pts):** Passes core tests with minor edge-case or efficiency lapses; solid code quality.
* **NEEDS_IMPROVEMENT ($50\text{--}69$ pts):** Partial functionality, sub-optimal approach, or significant time overrun.
* **REJECT ($< 50$ pts):** Failure on core test cases, unhandled crashes, or severe timeout.
