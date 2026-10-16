# Day 49 – Malpractice & Integrity Detection Design

## 1. Integrity Detection Framework

The Integrity Detection Framework continuously collects and processes client and audio/visual telemetry events during an automated interview session:

```
[ Client Telemetry ]   --> [ Signal Ingestion ] --> [ Anomaly & Threshold Engine ]
(Tabs, Focus, Gaze, Audio)                                 |
                                                            v
[ Behavioral Integration ] <-- [ Risk Tagging ]  <-- [ Pattern Correlation ]
```

### Monitored Malpractice Signals

| Signal Key | Name | Tracking Mechanism | Severity Weight |
|---|---|---|---|
| `tab_switching_frequency` | Tab Switching Frequency | Browser `visibilitychange` & window `blur` listener counts | 0.25 |
| `screen_focus_loss` | Loss of Screen Focus | Cumulative duration (seconds) outside active interview viewport | 0.25 |
| `external_voice_detection` | External Voice Detection | Speaker diarization / secondary pitch & formant analysis | 0.30 |
| `repeated_looking_away` | Repeated Looking Away | Head pose estimation (yaw/pitch > ±25°) & eye-gaze tracking | 0.20 |

---

## 2. Malpractice Detection Logic

### A. Threshold-Based Flags

| Signal | Warning Level (Toast) | Flag Level (Audit Log) | Critical Level (Escalate) |
|---|---|---|---|
| Tab Switching | $\ge 2$ switches | $\ge 4$ switches | $\ge 7$ switches |
| Screen Focus Loss | $\ge 15.0$ seconds | $\ge 45.0$ seconds | $\ge 90.0$ seconds |
| External Voice Detection | $\ge 1$ occurrence | $\ge 2$ occurrences | $\ge 4$ occurrences |
| Repeated Looking Away | $\ge 4$ instances | $\ge 8$ instances | $\ge 14$ instances |

### B. Pattern Recognition Logic

Pattern recognition correlates multi-modal events across time:
1. **Real-time External Prompting**: External voice detection co-occurring with gaze deviation and sudden fluently delivered responses.
2. **Immediate Question Lookup**: Tab switch or focus loss occurring within 10 seconds of question delivery.
3. **Secondary Screen Reading**: Continuous off-center gaze (>5s) during answer delivery without pause or hesitation.
4. **Rapid Micro-Switching**: Frequent short tab switches (<3s) indicative of copy-pasting or quick cheat-sheet referencing.

---

## 3. Warning & Flagging System Design

### A. Real-Time Alerts (Candidate Experience)
- **Notice Tier**: Gentle, non-punitive UI toast on first anomaly (e.g., *"Please keep the interview screen in focus"*).
- **Warning Tier**: Modal reminder on 2nd breach (e.g., *"Warning: Background voice detected. Ensure you are alone"*).
- **Critical Tier**: Persistent badge indicating that continuous violations will flag the session for human proctor audit.

### B. Interview Risk Tagging (Recruiter Dashboard)

$$\text{Integrity Score} = 100 - \sum(\text{Threshold Penalties}) - \sum(\text{Pattern Penalties})$$

- **LOW_RISK** ($\text{Score} \ge 85$): Clean session; proceed automatically.
- **MEDIUM_RISK** ($65 \le \text{Score} < 85$): Minor technical slips or incidental distractions; proceed with scrutiny.
- **HIGH_RISK** ($40 \le \text{Score} < 65$): Multiple corroborated violations; mandatory recruiter review.
- **CRITICAL_RISK** ($\text{Score} < 40$): High probability of external assistance/cheating; disqualification recommended.

---

## 4. Integration with Behavioral Signals

Integrity signals calibrate and contextualize behavioral confidence scores:
- **Confidence Deflation**: When high confidence coincides with low integrity, the system applies an integrity discount factor to prevent inflated confidence metrics resulting from external answers:
  $$\text{Adjusted Confidence} = \text{Baseline Confidence} \times \left(0.5 + 0.5 \times \frac{\text{Integrity Score}}{100}\right)$$
- **Contradiction Cross-Reference**: Inconsistencies detected during external voice or tab-switching intervals are tagged with high priority.
