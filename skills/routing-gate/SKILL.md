---
name: routing-gate
description: Classify prediction errors before dispatch. USE WHEN about to execute any non-trivial task to determine if it should proceed autonomously or surface to Malik.
---

# Routing Gate — The Routing Law Made Operational

## When to Use

Before executing any task that isn't trivially routine. This skill implements the Routing Law: "Prediction errors are signals routed to the right substrate."

## Classification Dimensions

Rate the current task on three dimensions:

### Novelty (0-1)
How new is this task relative to what the system has done before?
- 0.0-0.3: Routine — done many times
- 0.4-0.6: Familiar with variations
- 0.7-1.0: Novel — new territory

### Stakes (0-1)
What's the cost of getting it wrong?
- 0.0-0.3: Trivial — easily absorbed
- 0.4-0.6: Moderate — costs time/effort to fix
- 0.7-1.0: Critical — affects people, money, or reputation

### Reversibility (0-1)
How easily can the action be undone?
- 0.0-0.3: Permanent — sent emails, published content, deleted data
- 0.4-0.6: Difficult — deployed code, modified live systems
- 0.7-1.0: Trivial — local edits, drafts, analysis

## Decision Rule

```
IF novelty > 0.7 AND stakes > 0.5 AND reversibility < 0.3:
    → STOP.
    → Tell Malik:
      1. What the task is (one line)
      2. Classification: Novelty=X, Stakes=Y, Reversibility=Z
      3. Your recommended approach
      4. What could go wrong
    → Wait for direction.

ELSE IF stakes > 0.5:
    → Proceed, but flag for post-execution review.

ELSE:
    → Proceed autonomously. Log the classification.
```

## Output Format

When logging a routing decision:

```
ROUTING: [task summary]
  Novelty: [score] | Stakes: [score] | Reversibility: [score]
  Route: [ai_autonomous | ai_with_review | surface_to_human]
  Rationale: [one line]
```

## Threshold Adjustment

Current thresholds (adjustable based on outcome data):
- Novelty trigger: 0.7
- Stakes trigger: 0.5
- Reversibility trigger: 0.3

If AI-autonomous tasks consistently get low ratings → lower thresholds (more conservative).
If human-surfaced tasks are consistently trivial → raise thresholds (more autonomous).

See `framework/routing-gate.md` for full details and examples.
