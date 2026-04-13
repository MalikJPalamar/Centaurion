# Feedback Loop Infrastructure

The mechanism by which Centaurion improves over time. Every interaction leaves a signal; every signal updates the model.

## The Coupling Law

> Every interaction updates shared memory. The system must compound.

The feedback loop is the implementation of the Coupling Law. Without it, each session starts from zero.

## Data Flows

```
Malik rates output
       ↓
ratings.jsonl (append)
       ↓
Dev loop reads ratings
       ↓
Routing calibration improves
```

```
Cortex routes a task
       ↓
routing-log.jsonl (append)
       ↓
Pattern analysis identifies systematic misroutes
       ↓
Routing Gate thresholds adjusted
```

## State Files

| File | Schema | Purpose |
|------|--------|---------|
| `memory/state/routing-log.jsonl` | `centaurion-routing-v1` | Log every routing decision with novelty/stakes/reversibility scores |
| `memory/state/ratings.jsonl` | `centaurion-rating-v1` | Malik's 1–5 ratings on task outcomes, with routing correctness |

Both files are append-only. Never edit existing lines — only add new ones.

## Rating Schema

```json
{
  "timestamp": "2026-04-12T10:00:00Z",
  "task": "Description of what was done",
  "venture": "centaurion|aob|builderbee",
  "rating": 4,
  "routing_correct": true,
  "notes": "Optional free text"
}
```

## Routing Log Schema

```json
{
  "timestamp": "2026-04-12T10:00:00Z",
  "task": "Description of what was routed",
  "venture": "centaurion",
  "novelty": 0.3,
  "stakes": 0.4,
  "reversibility": 0.8,
  "route": "ai_autonomous",
  "outcome_rating": null,
  "routing_correct": null
}
```

`outcome_rating` and `routing_correct` are null until Malik reviews the result.

## Daily Health Check

The dev loop reviews feedback state as part of `workflows/daily-health.md`. Key signals:
- Rating trend (is system quality improving?)
- Routing accuracy (are high-stakes tasks being surfaced correctly?)
- Wiki growth (is knowledge being captured?)

## Related

- [Active Inference Loop](active-inference-loop.md) — The REMEMBER step that feeds this
- [Routing Gate](routing-gate.md) — What the routing log captures
- [Multi-Runtime Deployment](multi-runtime-deployment.md) — Where feedback originates
