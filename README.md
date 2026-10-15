# 🤖 Zecpath AI – Intelligent Recruitment & Interview System

Zecpath AI is an AI-powered recruitment and job portal system designed to automate and improve the hiring process for both Job Seekers and Recruiters.

The system combines ATS (Applicant Tracking System), AI resume screening, candidate scoring, shortlisting, HR screening, adaptive interviews, communication analysis, sentiment analysis, confidence detection, and edge-case handling into a single recruitment workflow.

---

## 📑 Table of Contents

- [Project Overview](#-project-overview)
- [Main Objectives](#-main-objectives)
- [User Roles](#-user-roles)
- [AI Recruitment Pipeline](#-ai-recruitment-pipeline)
- [Key Features](#-key-features)
- [Project Architecture](#️-project-architecture)
- [Technology Stack](#️-technology-stack)
- [Project Structure](#-project-structure)
- [FastAPI Backend](#️-fastapi-backend)
- [Installation](#️-installation)
- [API Documentation](#-api-documentation)
- [Testing](#-testing)
- [Example Candidate Evaluation](#-example-candidate-evaluation)
- [Development Progress](#-development-progress)
- [Future Improvements](#-future-improvements)
- [Learning Outcomes](#-learning-outcomes)
- [Developer](#-developer)
- [Project Links](#-project-links)
- [Project Vision](#-project-vision)
- [License](#-license)

---

## 🚀 Project Overview

Traditional recruitment involves manually reviewing resumes, conducting initial screening, and evaluating candidates. This can be time-consuming and inconsistent.

Zecpath AI provides an intelligent recruitment pipeline that helps recruiters:

- Analyze candidate resumes
- Calculate ATS scores
- Match candidates with job requirements
- Automatically shortlist candidates
- Conduct AI-based screening
- Generate HR interview questions
- Ask adaptive follow-up questions
- Analyze candidate communication
- Detect sentiment and confidence
- Handle incomplete or low-quality answers
- Support language-mixed responses
- Evaluate candidates using configurable rules

The goal is to make the recruitment process faster, structured, and AI-assisted.

---

## 🎯 Main Objectives

- Automate initial candidate screening
- Reduce manual resume evaluation
- Match candidate skills with job requirements
- Provide structured candidate scoring
- Support AI-based HR interviews
- Analyze candidate communication
- Handle real-world interview edge cases
- Provide useful information to recruiters for decision-making

---

## 👥 User Roles

### 👨‍💻 Job Seeker

Job seekers can:

- Create/manage their profile
- Upload resumes
- Apply for jobs
- Receive AI-based resume evaluation
- Participate in AI screening
- Participate in AI interviews
- Receive evaluation results

### 🧑‍💼 Recruiter

Recruiters can:

- Create job postings
- Define job requirements
- View applicants
- Analyze resumes
- View ATS scores
- Shortlist candidates
- Conduct AI screening
- Conduct AI interviews
- Review candidate evaluation results

---

## 🧠 AI Recruitment Pipeline

```text
                 ┌───────────────────┐
                 │    Job Seeker     │
                 └─────────┬─────────┘
                           │
                           ▼
                 ┌───────────────────┐
                 │   Resume Upload   │
                 └─────────┬─────────┘
                           │
                           ▼
                 ┌───────────────────┐
                 │ Resume Processing │
                 └─────────┬─────────┘
                           │
                           ▼
                 ┌───────────────────┐
                 │    ATS Scoring    │
                 └─────────┬─────────┘
                           │
                           ▼
                 ┌───────────────────┐
                 │ Candidate Matching│
                 └─────────┬─────────┘
                           │
                           ▼
                 ┌───────────────────┐
                 │   Shortlisting    │
                 └─────────┬─────────┘
                           │
                           ▼
                 ┌───────────────────┐
                 │   AI Screening    │
                 └─────────┬─────────┘
                           │
                           ▼
                 ┌───────────────────┐
                 │   HR Interview    │
                 └─────────┬─────────┘
                           │
                           ▼
                 ┌───────────────────┐
                 │ AI Evaluation     │
                 │ Communication     │
                 │ Confidence        │
                 │ Sentiment         │
                 └─────────┬─────────┘
                           │
                           ▼
                 ┌───────────────────┐
                 │ Recruiter Review  │
                 └───────────────────┘
```

---

## ✨ Key Features

### 📄 1. AI Resume Screening

The system processes candidate resumes and extracts relevant information such as:

- Skills
- Experience
- Education
- Job-related keywords
- Required technologies

The extracted information is used for ATS evaluation.

### 📊 2. ATS Scoring

Zecpath AI calculates a candidate's ATS score based on job requirements.

Example factors include:

- Required skills
- Technical skills
- Experience
- Job location
- Availability
- Role requirements

For an AI Engineer role, example requirements can include:

```text
Python
Machine Learning
FastAPI
0–3 years experience
Remote / Bangalore
Immediate / 15 / 30 days availability
```

### 🎯 3. Candidate Shortlisting

Candidates are categorized according to their evaluation score.

Example:

| Score    | Category          |
| -------- | ----------------- |
| 80+      | Strong Candidate  |
| 60–79    | Review            |
| 40–59    | Needs Improvement |
| Below 40 | Rejected          |

These thresholds are configurable according to the recruitment requirements.

### 🤖 4. AI Screening

The AI screening system provides structured questions to candidates.

The system contains a question bank and generates questions based on the candidate's context.

It can evaluate:

- Candidate answers
- Relevance
- Communication
- Confidence
- Technical understanding
- Behavioral responses

### 🗣️ 5. HR Interview Engine

The HR Interview Engine provides structured interview questions.

Interview sections include:

**Introduction**
Basic candidate introduction and background.

**Core HR**
Questions related to:

- Motivation
- Strengths
- Weaknesses
- Teamwork
- Career goals

**Role Evaluation**
Questions related to:

- Technical skills
- Job experience
- Role understanding
- Problem solving

**Closing**
Final interview questions and candidate questions.

### 🔄 6. Adaptive Questioning

The interview system can change the next question based on the candidate's previous answer.

Example:

```text
Candidate Answer
       │
       ▼
Analyze Answer
       │
       ├── Clear Answer
       │       ↓
       │   Next Question
       │
       ├── Incomplete Answer
       │       ↓
       │   Clarification
       │
       └── Interesting Answer
               ↓
          Deep Follow-up
```

Follow-up types include:

- Clarification
- Deepening
- Example-based questions

### 🎧 7. Edge Case Handling

The system handles common real-world interview problems.

Examples:

**Poor Audio**
Detects low-quality audio and prevents incorrect evaluation.

**Incomplete Answers**
Identifies answers that do not contain enough information.

**Language Mixing**
Detects mixed-language responses such as English + Malayalam.

**Background Noise**
Handles audio quality issues that may affect the interview.

**Very Short Answers**
Identifies responses that are too short for meaningful evaluation.

### 📈 8. Communication Analysis

The system evaluates candidate communication.

Example factors:

- Clarity
- Relevance
- Completeness
- Sentence structure
- Response quality

Example output:

```text
Communication Score: 80.5 / 100
```

Scores are normalized between `0` and `100`.

### 💬 9. Sentiment Analysis

The system analyzes the emotional tone of candidate responses.

Example:

```text
Input:
"I am confident and comfortable working with Python."

Output:
Positive
```

The sentiment engine generates a sentiment score that can be used as an additional evaluation signal.

### 🧠 10. Confidence Analysis

Candidate responses can be analyzed for confidence indicators.

The confidence analyzer considers characteristics of the response and produces a normalized score.

Example:

```text
Confidence Score: 78.5 / 100
```

### 🔎 11. Contradiction Detection

The system can identify contradictions in candidate responses.

For example:

```text
Question:
Do you have previous work experience?

Answer 1:
I have no experience.

Later Answer:
In my previous company, I worked for two years.
```

The system can flag a potential contradiction for further review.

### 🧩 12. Modular AI Architecture

The project is divided into separate modules so that each AI capability can be developed and tested independently.

Example modules:

```text
screening_ai/
interview_ai/
```

Important components include:

```text
question_engine.py
hr_question_engine.py
interview_state.py
follow_up_engine.py
adaptive_questioning.py
decision_tree.py
communication_score.py
communication_evaluator.py
confidence_analyzer.py
sentiment_engine.py
```

---

## 🏗️ Project Architecture

```text
                 ┌─────────────────────┐
                 │      Frontend       │
                 │   Job Seeker / HR   │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │      FastAPI        │
                 │       Backend       │
                 └──────────┬──────────┘
                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
          ▼                 ▼                 ▼
    Resume API        Scoring API       Jobs API
          │                 │                 │
          └─────────────────┼─────────────────┘
                            │
                            ▼
                  ┌──────────────────┐
                  │  AI Recruitment  │
                  │     Engine       │
                  └────────┬─────────┘
                           │
          ┌────────────────┼─────────────────┐
          │                │                 │
          ▼                ▼                 ▼
      Screening         Interview        Evaluation
          │                │                 │
          ▼                ▼                 ▼
     Question          Adaptive          Communication
      Engine           Questions         Confidence
                                           Sentiment
```

---

## 🛠️ Technology Stack

**Backend**

- Python
- FastAPI
- Pydantic
- Uvicorn

**AI / Machine Learning**

- Python-based AI modules
- Natural Language Processing
- ATS scoring
- Candidate matching
- Sentiment analysis
- Communication analysis
- Confidence analysis
- Adaptive questioning

**Frontend**

- Web-based recruitment interface
- Job Seeker workflow
- Recruiter workflow

**Data**

- JSON question banks
- Structured candidate data
- Job requirement data
- Resume information

---

## 📁 Project Structure

```text
Zecpath-AI-System/
│
├── api/
│   ├── routes/
│   │   ├── resume.py
│   │   ├── scoring.py
│   │   ├── shortlisting.py
│   │   └── jobs.py
│   │
│   ├── errors/
│   └── logger.py
│
├── screening_ai/
│   ├── screening.py
│   ├── question_engine.py
│   └── ...
│
├── interview_ai/
│   ├── hr_interview.py
│   ├── hr_question_engine.py
│   ├── interview_state.py
│   ├── follow_up_engine.py
│   ├── adaptive_questioning.py
│   └── decision_tree.py
│
├── evaluation/
│   ├── communication_score.py
│   ├── communication_evaluator.py
│   ├── confidence_analyzer.py
│   ├── sentiment_engine.py
│   └── contradiction_detector.py
│
├── data/
│   └── hr_screening_questions.json
│
├── tests/
│
├── main.py
├── requirements.txt
└── README.md
```

> The exact folder structure may vary depending on the current project version.

---

## ⚙️ FastAPI Backend

The project uses FastAPI as the backend API framework.

Main application:

```python
app = FastAPI(
    title="Zecpath AI ATS API",
    description="API layer for the Zecpath AI recruitment and interview system"
)
```

The API includes separate routers for:

- Resume
- Scoring
- Shortlisting
- Jobs

This modular structure makes the backend easier to maintain and extend.

---

## ▶️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/shinaspn198/Zecpath-AI-System.git
cd Zecpath-AI-System
```

### 2. Create Virtual Environment

**Windows**

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run FastAPI

From the project directory:

```bash
uvicorn main:app --reload
```

If the FastAPI application is inside another module, use the corresponding module path.

Example:

```bash
uvicorn app.main:app --reload
```

The API will normally be available at:

```text
http://127.0.0.1:8000
```

---

## 📚 API Documentation

FastAPI automatically provides interactive API documentation.

**Swagger UI**

```text
http://127.0.0.1:8000/docs
```

**ReDoc**

```text
http://127.0.0.1:8000/redoc
```

Swagger can be used to test API endpoints directly from the browser.

---

## 🧪 Testing

The project includes testing for different recruitment components.

Testing areas include:

- Resume processing
- ATS scoring
- Candidate shortlisting
- Screening questions
- HR interview
- Follow-up questions
- Adaptive questioning
- Communication evaluation
- Confidence analysis
- Sentiment analysis
- Contradiction detection
- Edge-case handling

Example:

```bash
pytest
```

---

## 📊 Example Candidate Evaluation

A candidate can go through the following pipeline:

```text
Resume
  ↓
ATS Score
  ↓
Eligibility Check
  ↓
Shortlisting
  ↓
AI Screening
  ↓
HR Interview
  ↓
Communication Analysis
  ↓
Confidence Analysis
  ↓
Sentiment Analysis
  ↓
Final Recruiter Review
```

---

## 📌 Development Progress

The project was developed incrementally through multiple stages.

### Days 1–28

Initial recruitment platform development:

- Product requirement analysis
- Recruitment workflows
- Job seeker workflow
- Recruiter workflow
- ATS functionality
- Resume scoring
- Candidate shortlisting
- Backend integration

### Day 30

- Frontend and backend integration
- Job Seeker workflow
- Recruiter workflow
- Integration testing

### Day 31

- Edge-case handling
- Poor audio
- Incomplete answers
- Language mixing
- Background noise

### Day 32

- AI screening system
- Screening question engine
- Screening evaluation

### Day 33

- HR interview engine
- HR question bank
- Interview state management
- Follow-up questions
- Adaptive questioning

### Day 36

- Communication scoring
- Communication evaluation
- Confidence analysis
- Sentiment analysis
- Contradiction detection
- Stress-related indicators
- Evaluation testing

---

## 🔮 Future Improvements

Possible future improvements include:

- Advanced LLM-based candidate evaluation
- Multilingual interview support
- Voice-based AI interviews
- Real-time speech analysis
- Better resume parsing
- Explainable AI evaluation
- Recruiter analytics dashboard
- Candidate comparison dashboard
- Interview transcript generation
- Cloud deployment
- Authentication and authorization
- Database integration
- Advanced candidate-job semantic matching

---

## 🎓 Learning Outcomes

This project provided practical experience with:

- Python
- FastAPI
- REST APIs
- Machine Learning concepts
- NLP
- ATS systems
- AI-based recruitment
- Modular backend architecture
- API integration
- Testing
- Edge-case handling
- Interview automation
- Candidate evaluation
- AI system design

---

## 👨‍💻 Developer

**Shinas PN**
BCA – AI Specialization

**Areas of Interest**

- Artificial Intelligence
- Machine Learning
- NLP
- Generative AI
- FastAPI
- AI Engineering
- Intelligent Recruitment Systems

---

## 🔗 Project Links

**GitHub**

- [Zecpath AI](https://github.com/shinaspn198/Zecpath-AI-System)

**Live Project**

- [https://zecpath-day1.vercel.app/](https://zecpath-day1.vercel.app/)

---

## ⭐ Project Vision

Zecpath AI aims to create an intelligent recruitment ecosystem where AI assists recruiters throughout the hiring pipeline — from resume screening to AI interviews and candidate evaluation — while keeping the recruitment process structured and transparent.

---

## 📜 License

This project is developed for educational, internship, and portfolio purposes.
