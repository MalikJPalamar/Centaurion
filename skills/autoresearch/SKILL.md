---
name: autoresearch
description: Autonomous overnight research iteration. Define a metric or question, let the agent iterate, review results in the morning. USE WHEN a research question needs depth beyond a single session.
---

# Autoresearch — Autonomous Overnight Iteration

## Purpose

Define a research question or improvement metric. The agent iterates autonomously (overnight or during off-hours), producing a structured report. Malik reviews results in the morning.

This implements the Autoresearch-Goenka pattern from the handoff: "define a metric, let the agent iterate overnight, review in morning."

## When to Use

- A research question needs multiple rounds of investigation
- A metric needs to be tracked and improved iteratively
- A wiki topic needs deep sourcing beyond what one session provides
- Cross-venture analysis requires comparing data across AOB, BuilderBee, Centaurion

## Procedure

### 1. Define the Research Brief

Create a file `memory/state/autoresearch-active.json`:

```json
{
  "question": "What are the best free/low-cost models on OpenRouter for Nova's scanning role?",
  "venture": "centaurion",
  "metric": "model quality vs cost for classification tasks",
  "max_iterations": 5,
  "max_turns_per_iteration": 10,
  "deadline": "2026-04-20T06:00:00Z",
  "sources": ["openrouter.ai/models", "arena.lmsys.org"],
  "output": "memory/state/autoresearch-results.md"
}
```

### 2. Run the Research Loop

```bash
CENTAURION_REPO=~/Centaurion bash deploy/vps1/autoresearch.sh
```

Or schedule via cron for overnight execution:
```bash
0 22 * * * cd ~/Centaurion && CENTAURION_REPO=~/Centaurion bash deploy/vps1/autoresearch.sh >> ~/Centaurion/logs/cron.log 2>&1
```

### 3. Review Results

The output file (`memory/state/autoresearch-results.md`) contains:
- Summary of findings
- Sources consulted
- Confidence level
- Recommended actions
- Open questions for next iteration

### Example

Research brief: "How should AOB structure its GHL migration to minimize downtime?"

Iteration 1: Maps current Ontraport setup (contacts, sequences, pages, payments)
Iteration 2: Identifies GHL equivalents for each Ontraport feature
Iteration 3: Designs migration sequence (what moves first, what runs in parallel)
Iteration 4: Documents rollback plan and testing checklist
Iteration 5: Produces final migration playbook for AOB wiki

Output: `docs/aob-wiki/crm-migration-playbook.md` — a complete, sourced, actionable migration plan.

## Routing

Autoresearch tasks are medium-novelty, low-stakes, highly reversible → auto-execute. The agent runs autonomously and produces a report. Malik reviews and decides what to act on.

Exception: if research uncovers a high-stakes decision (e.g., "Ontraport has a feature GHL can't replicate"), the agent flags it in the report for human review rather than making a recommendation.
