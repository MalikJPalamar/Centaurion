# Feedback Capture Workflow

How outcome ratings and routing decisions flow into the system's state, enabling the feedback loops that make Centaurion improve over time.

## Rating Capture

### When
After every task completion where Malik provides a rating (1-5).

### How
Ratings are appended to `memory/state/ratings.jsonl`:

```json
{
  "timestamp": "2026-04-12T10:30:00Z",
  "task": "Configure GHL workflow for BuilderBee client",
  "venture": "builderbee",
  "rating": 4,
  "routing_correct": true,
  "notes": "Good result, minor formatting issue"
}
```

### Where Ratings Flow
- **L1 sensing:** Immediate signal — was this task successful?
- **L2 sensing (weekly review):** Trend analysis — are ratings improving?
- **Routing Gate adjustment:** Low-rated AI-autonomous tasks → lower thresholds

## Routing Decision Capture

### When
Every time the Routing Gate classifies a task (automatically during ROUTE step).

### How
Routing decisions are appended to `memory/state/routing-log.jsonl`:

```json
{
  "timestamp": "2026-04-12T10:00:00Z",
  "task": "Configure GHL workflow",
  "novelty": 0.3,
  "stakes": 0.5,
  "reversibility": 0.8,
  "route": "ai_autonomous",
  "outcome_rating": null,
  "routing_correct": null
}
```

The `outcome_rating` and `routing_correct` fields are backfilled when Malik rates the output, creating the feedback loop.

### Where Routing Logs Flow
- **L2 sensing (weekly review):** Routing accuracy trends
- **L4 sensing (monthly review):** Threshold adjustment decisions
- **Routing Gate thresholds:** Direct input to threshold tuning

## The Feedback Loop

```
Task → Routing Gate classifies → Agent executes → Malik rates outcome
  │                                                       │
  │                                                       ▼
  │                                            Rating stored in state
  │                                                       │
  │                                                       ▼
  │                                           Weekly review analyzes
  │                                                       │
  │                                                       ▼
  └──────────────── Routing thresholds adjust ◄───────────┘
```

## State Files

| File | Purpose | Format |
|------|---------|--------|
| `memory/state/ratings.jsonl` | Outcome ratings from Malik | Append-only JSONL |
| `memory/state/routing-log.jsonl` | Routing Gate classifications | Append-only JSONL |
