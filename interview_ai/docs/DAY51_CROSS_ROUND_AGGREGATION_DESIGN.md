# Day 51 – Cross-Round Aggregation Engine Design

## 1. Cross-Round Aggregation Architecture

The Cross-Round Aggregation Engine unifies discrete scores from all five evaluation stages into a holistic hiring intelligence score:

```
[ Stage 1: ATS Resume ] ------------+
[ Stage 2: Screening ] -------------|
[ Stage 3: HR Interview ] ----------+--> [ Profile Normalization ] --> [ Weighted Engine ] --> [ Unified Hiring Fit ]
[ Stage 4: Technical Interview ] ---|    (Experience / Role Tier)       (Role-Based Weights)    (Percentage & Recommendation)
[ Stage 5: Machine Test ] ----------+
```

---

## 2. Evaluation Stages Aggregated

1. **ATS Match Score (`ats`):** Resume parsing, keyword overlap, skill matching, and qualifications.
2. **Screening Score (`screening`):** Initial conversational screening assessing communication and background alignment.
3. **HR Interview Score (`hr_interview`):** Cultural fit, behavioral confidence, scenario evaluation, and workplace values.
4. **Technical Interview Score (`technical_interview`):** Conceptual technical depth, architectural reasoning, and domain knowledge.
5. **Machine Test Score (`machine_test`):** Hands-on programming, debugging, system implementation, and sandbox execution metrics.

---

## 3. Role-Based Weightage System

Weights dynamically adjust according to role expectations to prioritize relevant competencies:

| Role Identifier | ATS Match | Screening | HR Interview | Technical Interview | Machine Test | Total |
|---|---|---|---|---|---|---|
| **Software Engineer** | 15% | 15% | 15% | 25% | 30% | **100%** |
| **AI / ML Engineer** | 15% | 15% | 15% | 25% | 30% | **100%** |
| **Data Analyst** | 20% | 15% | 15% | 25% | 25% | **100%** |
| **Product Manager** | 20% | 25% | 25% | 20% | 10% | **100%** |
| **HR Specialist** | 20% | 25% | 35% | 10% | 10% | **100%** |
| **Default Profile** | 20% | 20% | 20% | 20% | 20% | **100%** |

---

## 4. Candidate Profile Normalization

To avoid bias between different career stages, profile multipliers normalize raw performance:
* **Entry-Level / Junior:** Applies a $+5\%$ normalization factor to ATS and Machine Test scores to reward practical coding ability over extensive resume chronologies.
* **Mid-Level:** Standard baseline evaluation ($1.00\times$ across all dimensions).
* **Senior:** Higher expectations on architectural and behavioral leadership ($1.02\times$ HR and high technical thresholds).

---

## 5. Hiring Fit Score (%) Calculation & Recommendations

$$\text{Hiring Fit Score (\%)} = \sum_{i=1}^{5} \left( \text{Normalized Score}_i \times \text{Role Weight}_i \right)$$

* **$\ge 85.00\%$:** **`STRONG_HIRE`** (Exceeds role requirements across technical and behavioral rounds).
* **$70.00\% - 84.99\%$:** **`HIRE`** (Solid cross-round performance meeting team thresholds).
* **$55.00\% - 69.99\%$:** **`BORDERLINE_REVIEW`** (Requires targeted interview review or compensatory strengths).
* **$< 55.00\%$:** **`REJECT`** (Fails to meet minimum qualifying standard).

---

## 6. Transparency & Audit Trail

Every generated score includes an explicit breakdown:
* Raw stage scores and normalization multipliers applied.
* Explicit weight percentages used for the specific job role.
* Weighted points contribution per stage.
* Plain-language audit rationale explaining how the recommendation was formulated.
