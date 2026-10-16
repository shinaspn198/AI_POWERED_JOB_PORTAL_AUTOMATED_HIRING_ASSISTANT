# Day 62 — Developer Onboarding Guide

## 1. Welcome to the Zecpath AI Engineering Team
This guide accelerates onboarding for new engineers working on the Zecpath AI Recruitment platform. It covers directory organization, coding standards, architecture mental models, testing procedures, and contribution workflows.

---

## 2. Repository Structure & Key Directories

```
Zecpath-AI-System/
├── api/                   # FastAPI REST API layer
│   ├── routes/            # Route controllers (resume, scoring, assessment, integration, monitoring)
│   ├── models/            # SQLAlchemy DB models & Pydantic schemas
│   └── main.py            # ASGI entrypoint & middleware configuration
├── parsers/               # Multi-format document parsers (PDF, DOCX)
├── semantic_matching/     # TF-IDF, Vector embeddings, cosine similarity
├── ats_engine/            # ATS scoring, keyword matching & eligibility verification
├── screening_ai/          # Conversational screening dialogue manager & NLP intent parsing
├── interview_ai/          # Multimodal interview engines (HR, Technical, Integrity detection)
├── unified_scoring/       # Cross-round aggregation & final hiring recommendations
├── performance/           # Observability, caching, benchmarking & monitoring
├── simulation/            # End-to-end recruitment pipeline simulators
├── tests/                 # Pytest automated test suites (Days 53–70)
├── frontend/              # React/Vite web application UI
└── docs/                  # Architectural documentation, handbooks & day-wise deliverables
```

---

## 3. Core Development Principles

1. **Deterministic Fallbacks:** AI/ML inference components must gracefully fall back to heuristic rules if models, GPUs, or third-party APIs fail.
2. **Explainability First:** Every score (ATS, Technical, HR, Integrity) must include clear natural-language rationale and score breakdowns.
3. **Immutability of Decisions:** Final hiring decisions must be cryptographically hashed via `performance/ai_monitoring.py` to prevent post-hoc bias or tampering.
4. **Targeted Diffs:** Never rewrite working modules wholesale. Maintain backwards compatibility with existing endpoints and tests.

---

## 4. How to Add a New Evaluation Dimension

To introduce a new scoring dimension (e.g., "Culture Alignment"):
1. **Define Scorer:** Implement `evaluate()` returning a float `[0.0, 100.0]` and explanatory strengths/risks in `interview_ai/`.
2. **Update Aggregation:** Add dimension weight into `unified_scoring/hiring_fit.py` or `cross_round_aggregator.py`.
3. **Register Route:** Update `api/routes/assessment.py` and `api/schemas.py`.
4. **Add Unit Test:** Create `tests/test_<new_dimension>.py` verifying boundary values `[0.0, 50.0, 100.0]`.

---

## 5. Local Development Commands

```bash
# Activate virtual environment
.\venv\Scripts\activate

# Run all test suites
pytest tests/

# Run focused single-round tests
pytest tests/test_day61_observability.py

# Run development server with live reload
uvicorn api.main:app --reload --port 8000
```
