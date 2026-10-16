# Day 59 – API Mapping Diagram & Dataflow Specifications

**Project:** Zecpath Autonomous AI Hiring System  
**Stage:** Day 59  
**Focus:** Sequence Flows, Data Models & Endpoint Contracts

---

## 1. End-to-End API Interaction Sequence

```mermaid
sequenceDiagram
    autonumber
    actor Candidate
    participant FE as Frontend Portal
    participant API as FastAPI Backend
    participant Worker as Background Task Worker
    participant AI as Unified AI Engines
    participant DB as PostgreSQL Database

    Note over Candidate, DB: Phase 1: Ingestion & Resume Parsing (Async)
    Candidate->>FE: Uploads Resume (PDF / DOCX)
    FE->>API: POST /api/integration/resume/parse (is_async=True)
    API->>Worker: Enqueue parsing task
    API-->>FE: Return 202 Accepted {job_id, status: "PROCESSING"}
    Worker->>AI: Text Extraction & NER Skill Parser
    AI-->>Worker: Parsed structured entity dictionary
    Worker->>DB: Store parsed profile
    FE->>API: GET /api/integration/jobs/{job_id}/status (Polling)
    API-->>FE: Return {status: "COMPLETED", parsed_data: {...}}

    Note over Candidate, DB: Phase 2: Conversational Screening (Sync)
    Candidate->>FE: Answers voice screening question
    FE->>API: POST /api/integration/screening/evaluate
    API->>AI: Intent Refinement, Negation Detection & Score
    AI-->>API: {screening_score: 85, intent: "CONFIRM_EXPERIENCE"}
    API-->>FE: Return evaluation & next dialogue cue

    Note over Candidate, DB: Phase 3: Interview & Coding Sandbox (Sync)
    Candidate->>FE: Submits HR response & code solution
    FE->>API: POST /api/integration/interview/hr-technical
    API->>AI: Machine Test Evaluation & Proctoring Telemetry
    AI-->>API: {hr_score: 82, machine_score: 95, risk: "LOW_RISK"}
    API-->>FE: Return stage rubric scores

    Note over Candidate, DB: Phase 4: Final Unified Decision (Sync)
    FE->>API: POST /api/integration/decision/recommend
    API->>AI: False-Positive Mitigation & Rule+Score Aggregation
    AI-->>API: {decision: "Selected", fit_score: 89.2, confidence: 92%}
    API->>DB: Commit CandidateAssessment record & Audit Log
    API-->>FE: Return complete candidate dossier & report
```

---

## 2. API Endpoint Catalog

| Endpoint | Method | Input Schema | Output Schema | Latency Target |
| :--- | :---: | :--- | :--- | :---: |
| `/api/integration/resume/parse` | `POST` | `ResumeParseRequest` | `ResumeParseResponse` | < 1.5s (Async) |
| `/api/integration/jobs/{id}/status` | `GET` | `job_id: str` | `ResumeParseResponse` | < 10ms |
| `/api/integration/ats/score` | `POST` | `AtsScoringRequest` | `AtsScoringResponse` | < 30ms |
| `/api/integration/screening/evaluate` | `POST` | `ScreeningEvaluateRequest` | `ScreeningEvaluateResponse` | < 50ms |
| `/api/integration/interview/hr-technical` | `POST` | `InterviewEvaluateRequest` | `InterviewEvaluateResponse` | < 60ms |
| `/api/integration/decision/recommend` | `POST` | `DecisionRecommendRequest` | `DecisionRecommendResponse` | < 40ms |
