# Auto-generated skills (Tool Forge)

Skills authored by Cortex at runtime via `centaurion/extensions/tool_forge.py`.

## Subdirectories

| Dir | Lifecycle stage | Routing Gate |
|---|---|---|
| `_staging/` | Tier 1+2: scaffolded inside an isolated git worktree, sandbox-tested | `ai_autonomous` |
| `_promoted/` | Tier 3 success: operator approved, merged from worktree into canonical | surfaced at `promote`; logged at `approve` |
| `_failed/` | Tier 3 fail: operator rejected; archived with `REASON.txt` | logged at `reject` |
| `.template/` | Reference SKILL.md template the forge uses to scaffold |

## Audit trail

Every forge event is logged to `memory/state/tool-creation-log.jsonl` with:

- `timestamp`, `job_id`, `event`, `tool_name`
- `route` (per Routing Gate classification)
- `novelty`, `stakes`, `reversibility` scores
- `details` (event-specific)

## How a tool is born

```
Cortex needs capability X
  ↓
forge.scaffold(name, description, impl, test)        ← Tier 1: writes to _staging in worktree
  ↓
forge.execute(scaffold)                              ← Tier 2: runs test in Docker sandbox
  ↓
forge.propose_promotion(scaffold, execution)         ← Tier 3: surfaces diff to operator
  ↓
operator approves → forge.approve(proposal)          ← merges to _promoted/
operator rejects → forge.reject(proposal, reason)    ← archives to _failed/
```

## What lives in the canonical worktree (this dir) vs the forge worktree

Only `_promoted/` and `_failed/` artifacts are committed to the canonical
worktree. Active `_staging/` work happens in throwaway git worktrees under
`$TMPDIR/centaurion-forge/<repo_name>/job-<id>` and never touches `main`
unless promoted.
