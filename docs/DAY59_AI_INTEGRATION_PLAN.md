# Day 59 – API & System Integration Plan

**Project:** Zecpath Autonomous AI Hiring System  
**Stage:** Day 59  
**Focus:** Enterprise API Architecture, Async vs. Sync Processing, Error Handling & Security

---

## 1. System Integration Overview
The Zecpath platform decouples compute-intensive AI operations from low-latency conversational user interactions.

### Identified AI Services:
1. **Resume Parsing API:** Extracts candidate contact details, skills, experience, and education from `.pdf`, `.docx`, `.txt`.
2. **ATS Scoring API:** Multi-metric keyword and semantic resume match against job description rubrics.
3. **Screening AI API:** Live conversational understanding, intent disambiguation, and entity detection.
4. **Interview AI API:** Multi-turn HR behavioral and technical coding rubric evaluation.
5. **Decision AI API:** Cross-round aggregation, false-positive mitigation, and explainable hiring recommendation.

---

## 2. Asynchronous vs. Synchronous Architectural Strategy

| Service | Processing Mode | Transport / Protocol | Target Latency | Failure Handling |
| :--- | :---: | :---: | :---: | :--- |
| **Resume Parsing** | **Asynchronous** | Background Worker / Celery Queue | 500ms – 2s | Retries with exponential backoff; dead-letter queue. |
| **ATS Scoring** | **Synchronous / Batch** | HTTP REST POST | < 50ms | In-memory calculation; fallback default scoring. |
| **Voice Screening** | **Synchronous** | HTTP REST / WebSocket | < 100ms | Conversational fallback prompts on timeout. |
| **HR / Tech Interview** | **Synchronous** | HTTP REST | < 80ms | Graceful degradation; partial score caching. |
| **Final Decision AI** | **Synchronous** | HTTP REST | < 20ms | Immutable audit logging with SHA-256 seal. |

---

## 3. Resilience, Retry & Security Mechanisms
- **Circuit Breaker:** Automatically trips to `OPEN` state after 5 consecutive failures, shielding upstream servers for a 30-second recovery cool-down before entering `HALF-OPEN` canary state.
- **Retry with Jitter:** `t_retry = min(max_backoff, base_backoff * (2 ** attempt)) + random_jitter`.
- **API Authentication:** Standardized Bearer JWT tokens for internal frontend clients, scoped API keys (`X-API-Key`) for external enterprise integrations.
