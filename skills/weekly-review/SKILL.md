---
name: weekly-review
description: L2 sensing — structured weekly comparison of outcomes vs predictions. USE WHEN running the weekly review cycle or when Malik asks for a week-in-review summary.
---

# Weekly Review — L2 Structured Comparison

## Purpose

Compare this week's outcomes to predictions and last week's performance. Identify trends, patterns, regressions, and cross-venture connections. Output a phone-readable summary for Malik.

## Procedure

### 1. Gather Data
- Outcome ratings from the past 7 days (if captured)
- Routing decisions and their accuracy (was the classification correct?)
- Wiki repos: what pages were added/updated this week?
- Supermemory: volume and distribution across venture containers
- Any L3 tripwire alerts that fired

### 2. Analyze Trends
- **Rating trend:** Are outcome ratings improving, declining, or stable?
- **Routing accuracy:** Fewer misclassifications than last week?
- **Knowledge growth:** Are wikis expanding? Any stale areas?
- **Cross-venture patterns:** Does an AOB learning apply to BuilderBee? Does a BuilderBee workflow solve a Centaurion problem?
- **Prediction accuracy:** How well did this week's predictions match outcomes?

### 3. Identify Actions
- What should we do MORE of? (Things that got high ratings)
- What should we do LESS of? (Things that got low ratings or were misrouted)
- What's MISSING? (Topics encountered but not documented, questions raised but not answered)
- Should routing thresholds be adjusted?

### 4. Output

Format as a GitHub Issue titled: `[weekly-review] Week of {date}`

```markdown
## This Week at a Glance
- Tasks completed: X
- Average rating: X/5 (trend: ↑/↓/→)
- Routing accuracy: X% (trend: ↑/↓/→)

## Key Wins
- [Bullet points of highest-rated outcomes]

## Areas for Improvement
- [Bullet points of lowest-rated outcomes or misroutes]

## Cross-Venture Connections
- [Any patterns that span AOB/BuilderBee/Centaurion]

## Knowledge Gaps
- [Topics encountered but not yet in wikis]

## Recommended Adjustments
- [Specific threshold changes, priority shifts, or process tweaks]
```

## Example

For example, a weekly review might surface: "AOB routing accuracy dropped from 85% to 70% — three community-management tasks were misclassified as routine when they required Malik's input on facilitator selection. Recommended adjustment: increase stakes weight for facilitator-related tasks."

## Frequency

Weekly. Triggered by gh-aw scheduled workflow or manual invocation via `/weekly-review`.
