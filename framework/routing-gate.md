# The Routing Gate

The Routing Law made operational. Before executing any non-trivial task, classify the prediction error and dispatch to the right substrate.

## The Three Dimensions

### Novelty (0-1)
How new is this task relative to the system's experience?

| Score | Description | Examples |
|-------|-------------|----------|
| 0.0-0.2 | Routine — done many times before | Standard GHL config, weekly report generation |
| 0.3-0.5 | Familiar with variations — similar to past tasks | New GHL workflow for existing client vertical |
| 0.6-0.7 | Partially novel — some elements are new | CRM migration involving unfamiliar data schema |
| 0.8-1.0 | Fully novel — never encountered before | New strategic partnership, untested market entry |

### Stakes (0-1)
What's the cost of getting it wrong?

| Score | Description | Examples |
|-------|-------------|----------|
| 0.0-0.2 | Trivial — mistakes are inconsequential | Formatting a report, organizing notes |
| 0.3-0.5 | Moderate — mistakes cost time to fix | Code with a bug, misconfigured workflow |
| 0.6-0.7 | Significant — mistakes affect people or money | Client deliverable, financial transaction |
| 0.8-1.0 | Critical — mistakes are costly or reputational | Public communication, contract terms, data loss |

### Reversibility (0-1)
How easily can the action be undone?

| Score | Description | Examples |
|-------|-------------|----------|
| 0.0-0.2 | Permanent — cannot be undone | Sent email to client, published content, deleted data |
| 0.3-0.5 | Difficult to reverse — requires significant effort | Deployed code to production, modified live CRM |
| 0.6-0.7 | Reversible with effort — can be rolled back | Git commit (revertable), config change (restorable) |
| 0.8-1.0 | Trivially reversible — undo is free | Draft document, local file edit, analysis |

## The Decision Rule

```
IF novelty > 0.7 AND stakes > 0.5 AND reversibility < 0.3:
    → STOP. Surface to Malik with:
      - What the task is
      - Why it's classified as high-risk
      - Your recommended approach
      - What could go wrong
    → Wait for direction. Do NOT auto-execute.

ELSE:
    → Proceed with AI execution.
    → Log the classification for learning.
    → If stakes > 0.5, flag for post-execution review.
```

## Threshold Adjustment

Thresholds are not fixed. They adjust based on outcome data:

**To make the gate MORE conservative** (surface more to human):
- Lower the novelty threshold (e.g., 0.7 → 0.5)
- Lower the stakes threshold (e.g., 0.5 → 0.3)
- Trigger: AI-autonomous tasks are getting low ratings (model overconfidence)

**To make the gate LESS conservative** (automate more):
- Raise the novelty threshold (e.g., 0.7 → 0.8)
- Raise the stakes threshold (e.g., 0.5 → 0.7)
- Trigger: Human-surfaced tasks are consistently rated 5/5 AND Malik says "you could have just done this"

## Classification Log Format

Every routing decision is logged:

```
{
  "timestamp": "2026-04-12T09:30:00Z",
  "task": "Configure GHL workflow for new BuilderBee client",
  "novelty": 0.4,
  "stakes": 0.5,
  "reversibility": 0.7,
  "route": "ai_autonomous",
  "outcome_rating": null,
  "routing_correct": null
}
```

The `outcome_rating` and `routing_correct` fields are filled in after execution, creating the feedback loop that drives threshold adjustment.
