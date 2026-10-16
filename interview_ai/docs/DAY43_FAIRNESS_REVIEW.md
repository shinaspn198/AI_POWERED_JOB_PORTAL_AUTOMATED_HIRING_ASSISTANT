# Day 43 – Fairness Review Notes

## Scope

This review examines the existing scoring logic for fairness and consistency.

## Scoring Review

### Standard Score Engine

The standard score engine validates ATS and interview scores as
numeric values between 0 and 100.

The final score is calculated using equal weighting:

ATS = 50%
Interview = 50%

The same calculation is applied to candidates using the provided scores.

### Unified Scoring

The unified scoring configuration contains role-based weights for:

- ATS
- Screening
- Interview

The configured roles are:

- AI Engineer
- Software Engineer
- HR

The same configured weights are applied to candidates within the
corresponding role.

## Fairness Observation

The reviewed scoring formulas do not directly use demographic
attributes as scoring inputs.

The reviewed formulas operate on recruitment-related scores.

## Review Limitation

This review covers the scoring files inspected for Day 43.

The Day 43 PDF does not specify replacement weights or a new scoring
formula, so no scoring weights or formulas were changed during this
review.

## Result

The existing scoring logic has been reviewed for consistency and
direct demographic inputs.

No scoring formula was changed as part of this review.