---
name: onboarding
description: First-run onboarding flow for anyone installing Centaurion. Detects first-time setup, delivers AQAL+ILP baseline assessment (Light or Deep), writes private BASELINE-INTEGRAL.md, schedules follow-up reminders, and marks onboarding complete so it never re-runs. USE WHEN identity/BASELINE-INTEGRAL.md is missing OR memory/state/onboarding-state.json has onboarding_complete=false.
---

# Onboarding — First-Run Integral Baseline

## Purpose

Every new operator who clones Centaurion gets an **integral calibration pass** before the system starts routing work. The exo-cortex is only as precise as its operator model; no baseline = generic founder defaults = wasted precision.

This skill is **idempotent**: it runs exactly once per installation, never again unless a refresh is explicitly requested or the 90-day clock expires.

## Trigger Conditions

Cortex should invoke this skill when ANY of:

1. `identity/BASELINE-INTEGRAL.md` does not exist (first install)
2. `memory/state/onboarding-state.json` missing OR `onboarding_complete = false`
3. `next_refresh_due` date has passed (90-day rolling refresh)

Do NOT invoke if `onboarding_complete = true` AND `next_refresh_due` is in the future.

## Flow

### Step 1 — Detect state

```bash
STATE_FILE=memory/state/onboarding-state.json
if [ -f "$STATE_FILE" ]; then
  COMPLETE=$(jq -r '.onboarding_complete' "$STATE_FILE")
  NEXT_DUE=$(jq -r '.next_refresh_due' "$STATE_FILE")
  # If complete AND not due for refresh → exit silently
fi
```

### Step 2 — Greet + depth choice

Surface in the first session:

> Welcome to Centaurion. Before I start routing work for you, I need an **integral baseline** — it calibrates every agent's confidence, automation bias, and surfacing thresholds to **you** specifically.
>
> Two depths:
> - **Light** — 25 questions · ~15 min · AQAL quadrants + ILP core modules. Good enough to start; refined later.
> - **Deep** — 75 questions · ~50 min · adds lines of development + stage + ILP auxiliaries. Permanent calibration.
> - **Skip for now** — I'll remind you in 48 hours. System runs with generic defaults until then.
>
> Which would you like?

### Step 3 — Deliver assessment

- **Light chosen:** invoke `skills/integral-baseline/assessment-light.md`, deliver in 5 Parts of 5 questions each. Persist answers after each Part to `memory/state/baseline-*-in-progress.md` + Supermemory (if connected).
- **Deep chosen:** invoke `skills/integral-baseline/assessment-deep.md`, deliver in 6 Parts (4 quadrants × 15Q + ILP + Lines/Stage).
- **Skip chosen:** schedule a 48-hour reminder, mark state `onboarding_complete=false, deferred_until=<T+48h>`, exit.

### Step 4 — Score + write

Invoke `skills/integral-baseline/scoring.md` rubric. Write:
- `identity/BASELINE-INTEGRAL.md` — the full synthesis (gitignored by default — personal data)
- `memory/state/onboarding-state.json` — the state sentinel (see schema below)
- Capture summary to Supermemory if connected (`centaurion-malik` container)

### Step 5 — Schedule follow-up

| If Light was chosen | Schedule **Deep assessment** reminder **T+7 days** via Google Calendar / ClickUp / `memory/state/reminders.jsonl` fallback |
| If Deep was chosen | Schedule **90-day refresh** reminder `next_refresh_due` via same channels |
| If Skipped | Schedule **48-hour nudge** reminder |

Apply the scheduling tool in this order (first that's connected wins):
1. `mcp__claude_ai_Google_Calendar__create_event`
2. `mcp__claude_ai_ClickUp__clickup_create_reminder`
3. `memory/state/reminders.jsonl` fallback (picked up by daily health check)

### Step 6 — Apply Routing Gate adjustments

Read the baseline's routing-adjustment section. Append entries to `memory/state/routing-adjustments.jsonl` so future SENSE steps load them. Do NOT overwrite previous adjustments — append with timestamp.

### Step 7 — Mark complete + exit

Write final state, confirm to operator, exit onboarding mode. Normal Active Inference loop resumes on next turn.

## State File Schema — `memory/state/onboarding-state.json`

```json
{
  "$schema": "centaurion-onboarding-v1",
  "onboarding_complete": true,
  "first_baseline_type": "light|deep|skipped",
  "first_baseline_date": "YYYY-MM-DD",
  "baseline_path": "identity/BASELINE-INTEGRAL.md",
  "deep_reminder_scheduled": "YYYY-MM-DD | null",
  "next_refresh_due": "YYYY-MM-DD",
  "deferred_until": "YYYY-MM-DDTHH:MMZ | null",
  "routing_adjustments_applied": ["R1", "R2", "..."],
  "operator_id": "optional — hash or handle for multi-operator deployments"
}
```

## Integration Points

### CLAUDE.md SENSE step
```
Before normal context loading: read memory/state/onboarding-state.json.
If missing OR onboarding_complete=false → invoke skills/onboarding/ first.
If next_refresh_due < today → gently surface refresh prompt, continue normally.
Else → continue with full SENSE flow.
```

### install.sh
```
After cron jobs are set up, before "Installed" banner:
  if [ ! -f "$REPO_DIR/memory/state/onboarding-state.json" ]; then
    echo "  ℹ Onboarding will run on first Claude Code session"
    echo "  Start with: cd $REPO_DIR && claude"
  fi
```

### Daily health check
Scan for `deferred_until` in the past → surface nudge.
Scan for `next_refresh_due` < today + 14 → surface 2-week warning.

## Idempotency Guarantees

- **Runs exactly once per install** unless refresh is due
- **Survives session breaks** via `baseline-*-in-progress.md` (resume mid-assessment)
- **Survives repo re-clone** ONLY IF operator also backs up `memory/state/` (which is tracked in git for non-personal state). `identity/BASELINE-INTEGRAL.md` is NOT tracked — operator's responsibility to back up private data.
- **Re-onboard explicitly:** operator can trigger `/onboard --force` or delete `memory/state/onboarding-state.json`

## Routing

Onboarding itself is:
- Novelty: 0.3 (templated flow)
- Stakes: 0.6 (baseline shapes all future routing — meaningful)
- Reversibility: 0.8 (can re-onboard)
→ `ai_autonomous` for delivery, `ai_with_review` for the final baseline write (operator confirms before it becomes canonical).
