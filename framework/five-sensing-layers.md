# Five Sensing Layers

Centaurion implements hierarchical predictive processing through five sensing layers. Lower layers handle routine patterns at high frequency. Higher layers handle novel, abstract patterns at lower frequency. Prediction errors flow UP the hierarchy; predictions flow DOWN.

## L0 — Identity Load (Every Session)

**Trigger:** Session start (any agent, any runtime)
**What it does:** Loads TELOS identity context — who Malik is, what he values, what he's working on, what the Three Laws require.
**Maps to:** PAI's TELOS + SessionStart hook
**Implementation:** `skills/centaurion-core/SKILL.md` — loaded automatically via CLAUDE.md

**Content loaded:**
- identity/PURPOSE.md (Precision Ratio)
- identity/MISSION.md (Three Laws, ventures)
- identity/GOALS.md (current priorities)
- identity/PREFERENCES.md (communication and work style)
- Recent items from Supermemory (what was I doing last time?)

**Success criteria:** Agent can answer "What are Malik's three ventures?" and "What's the Routing Law?" without being told.

---

## L1 — Micro-Feedback (Every Task Completion)

**Trigger:** Task completion, agent stop signal
**What it does:** Captures a signal about how the task went. Minimal friction — a rating, a one-line note, or an implicit signal (task accepted vs. task revised).
**Maps to:** PAI's StopOrchestrator hook, ratings.jsonl
**Implementation:** Integrated into the Active Inference loop's REMEMBER phase

**Signals captured:**
- Outcome rating (1-5, when provided by Malik)
- Task classification accuracy (was the routing correct?)
- Time-to-completion
- Whether the task required human revision

**Success criteria:** After every task, at least one data point flows into memory. No task completes in a vacuum.

---

## L2 — Structured Comparison (Weekly)

**Trigger:** Weekly schedule (gh-aw or manual invocation)
**What it does:** Compares this week's outcomes to last week's. Identifies trends, patterns, regressions. Updates WISDOM/ with synthesized insights.
**Maps to:** New — `skills/weekly-review/SKILL.md`
**Implementation:** Weekly review skill + gh-aw workflow

**Analysis performed:**
- Rating trends (improving, declining, stable?)
- Routing accuracy trends (fewer misclassifications?)
- Wiki coverage gaps (topics we encountered but didn't document?)
- Cross-venture patterns (does an AOB learning apply to BuilderBee?)
- Prediction vs. outcome comparison (were our forecasts accurate?)

**Output:** GitHub Issue titled "[weekly-review] Week of {date}" with findings, published for Malik's phone review.

**Success criteria:** Malik reads the weekly review on his phone and adjusts one routing threshold or priority based on its findings.

---

## L3 — Environmental Tripwires (Threshold Breach)

**Trigger:** Automated monitoring detects a threshold breach
**What it does:** Fires an alert when a pre-defined condition is met. These are "set and forget" monitors that run continuously.
**Maps to:** New — AlertMonitor concept, gh-aw daily health check
**Implementation:** `workflows/daily-health.md` + external monitors

**Tripwires configured:**
- **Stock price alerts:** SA scan tickers breach defined thresholds (via situational-awareness-lens repo)
- **CRM metrics:** Lead response time exceeds target, pipeline value drops below threshold
- **System health:** VPS uptime, Docker container status, API key expiration
- **Memory health:** Supermemory approaching free tier limit, wiki repos stale > 7 days
- **Routing drift:** Misclassification rate exceeds 20% over rolling 7-day window

**Output:** GitHub Issue with alert details + recommended action. Telegram notification via Nova.

**Success criteria:** Malik is never surprised by something the system should have caught. Alerts arrive before problems become crises.

---

## L4 — Full Closed-Loop Review (Monthly)

**Trigger:** Monthly schedule
**What it does:** Complete system review — compares all predictions to all outcomes for the month. Identifies systematic biases, updates the model, adjusts routing thresholds.
**Maps to:** New — `skills/gap-analysis/SKILL.md` (partial)
**Implementation:** Monthly skill invocation + InfraNodus gap analysis

**Analysis performed:**
- **Prediction accuracy audit:** Sample 20+ predictions from the month. Score hit rate.
- **Routing threshold review:** Are current thresholds optimal? Adjust based on month's data.
- **Knowledge graph audit:** Run InfraNodus gap analysis on all three wikis. What clusters are disconnected? What questions aren't being asked?
- **Memory utilization:** How much of Supermemory's capacity is used? What's the signal-to-noise ratio?
- **Fitness assessment:** Has the Precision Ratio improved? Is predictive order increasing faster than cost?

**Output:** GitHub Issue titled "[closed-loop] Month of {date}" with comprehensive findings, trend charts (where possible), and recommended adjustments.

**Success criteria:** Each monthly review produces at least one concrete adjustment to the system (a threshold change, a new tripwire, a wiki restructure, a workflow modification).

---

## The Hierarchy in Practice

```
L4 (Monthly)   ────── Strategic: "Is the system getting smarter?"
  │
L3 (Tripwire)  ────── Reactive: "Something just breached a threshold"
  │
L2 (Weekly)    ────── Tactical: "How did this week compare to last?"
  │
L1 (Per-task)  ────── Operational: "How did this specific task go?"
  │
L0 (Session)   ────── Foundational: "Who am I? What am I doing?"
```

Prediction errors at lower layers are handled automatically. Errors that can't be resolved at one layer propagate UP to the next. The human (Malik) primarily operates at L2-L4, reviewing synthesized signals rather than raw data.
