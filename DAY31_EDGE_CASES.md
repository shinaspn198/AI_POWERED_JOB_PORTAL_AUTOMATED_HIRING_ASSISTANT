\# Day 31 – Edge Case \& Failure Handling



\## Objective



Ensure system stability in real-world interview conditions.



\## 1. Poor Audio



The system checks audio confidence.



\- Low confidence → retry

\- Medium confidence → warning

\- Good confidence → continue



\## 2. Language Mixing



The system detects whether an answer contains mixed-language text.



Examples:



\- English only → normal

\- Malayalam + English → mixed\_language



The system continues processing mixed-language answers.



\## 3. Missing Answers



If no answer is received:



\- Ask the candidate to try again.

\- Increase the retry count.

\- After maximum retries, activate fallback.



\## 4. Background Noise



The system handles unclear audio caused by background noise.



\- Severe noise → retry

\- Moderate noise → warning

\- Acceptable audio → continue



\## 5. Retry Logic



Maximum retries:



```text

3 attempts

