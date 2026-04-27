# Tool Forge — Dynamic Skill Creation in the Omega Paradigm

> **What:** A three-tier mechanism that lets Cortex write executable code at
> runtime while keeping every step within the Three Laws.
> **Why:** Without runtime tool creation, the agent is bounded by what was
> hand-authored. With it (and only with it), the system can absorb capability
> shifts as they happen.
> **How:** scaffold → sandbox exec → operator-gated promotion. Files never touch
> `main` until the operator approves a diff.

---

## The Routing-Gate problem

A naive "agent writes code, then runs it" loop fails the Routing Gate inequality:
runtime code is novel (by definition), high-stakes (it executes), and only
partially reversible (it persists). Surfacing **every** code-write to the
operator kills autonomy. Surfacing **none** of them violates the Hierarchy Law.

The forge resolves this by **decomposing** the operation into three tiers,
each classified separately:

| Tier | Event | What it does | Stakes | Reversibility | Routing |
|------|-------|---|:-:|:-:|---|
| 1 | `scaffold` | Cortex writes `SKILL.md` + `impl.py` + `test.py` into an isolated git worktree on branch `auto/<job_id>` | low | very high (worktree is throwaway) | `ai_autonomous` |
| 2 | `sandbox_exec` | Run `python test.py` inside a hardened Docker container (no network, dropped caps, RO root, memory cap, timeout) | low | very high (container destroyed on completion) | `ai_autonomous` |
| 3 | `promote` | Compute `git diff main..auto/<job_id>` → surface to operator | high | partial | **`surface_to_human`** |

Operator decisions emit two terminal events:

| Event | Action | Routing |
|---|---|---|
| `approve` | Copy artifacts into `skills/auto-generated/_promoted/<tool_name>/` | logged, autonomous (decision was already made) |
| `reject`  | Archive to `skills/auto-generated/_failed/<job_id>-<tool_name>/` with `REASON.txt` | logged, autonomous |

A short-circuit event `promote_blocked` is logged when sandbox execution
fails — the proposal is never created, so the operator is not bothered.

---

## Safety primitives

### Worktree isolation (`Worktree`)

- Each job gets a fresh git worktree at
  `$TMPDIR/centaurion-forge/<repo_name>/job-<id>` on a new branch
  `auto/<job_id>`.
- Job IDs must match `^[A-Za-z0-9][A-Za-z0-9_\-]{0,63}$` — no path traversal.
- `worktree.remove()` is idempotent; tears down both the path and the branch.
- The main repo's `main` is **never** modified by the forge — only
  `approve()` (which the operator has authorized) writes into the canonical
  worktree.

### Sandbox isolation (`DockerSandbox`)

Defaults err on safety:

| Property | Default | Flag |
|---|---|---|
| Network | off | `--network none` |
| Memory cap | 256 MB | `--memory 256m --memory-swap 256m` |
| CPU cap | 1.0 cores | `--cpus 1.0` |
| PID limit | 256 | `--pids-limit 256` |
| Capabilities | all dropped | `--cap-drop ALL` |
| Privilege escalation | disabled | `--security-opt no-new-privileges` |
| Root filesystem | read-only | `--read-only` |
| Tmpfs | 64 MB at `/tmp` | `--tmpfs /tmp:size=64m` |
| Workdir | mounted RW at `/work` | `-v <workdir>:/work:rw -w /work` |
| Lifecycle | ephemeral | `--rm` |
| Wall-clock timeout | 30 s | enforced by parent process |

The same `Sandbox` interface is implemented by `MockSandbox` (tests) and
will be implemented by a future `FirecrackerSandbox` (Phase 2 — microVM-grade
isolation, ~125 ms boot, kernel separation).

---

## Files & layout

```
centaurion/extensions/
  ├── routing_gate.py     # adds classify_tool_creation(event, ...)
  ├── sandbox.py          # Worktree, Sandbox ABC, DockerSandbox, MockSandbox
  ├── tool_forge.py       # ToolForge: scaffold/execute/propose/approve/reject
  └── forge_demo.py       # `python3 -m centaurion.extensions.forge_demo`

skills/auto-generated/
  ├── .template/SKILL.md  # frontmatter the forge emits
  ├── _staging/.gitkeep   # transient (worktree-only) — kept empty in main
  ├── _promoted/          # operator-approved tools land here
  └── _failed/            # operator-rejected tools archive here with REASON.txt

memory/state/
  └── tool-creation-log.jsonl   # full audit trail of forge events

tests/
  ├── conftest.py
  ├── pytest.ini
  ├── test_sandbox.py
  ├── test_tool_forge.py
  ├── test_routing_gate.py
  └── verify-tool-forge.sh   # phase 14 verification (29 checks)

framework/
  └── tool-forge.md       # this document
```

---

## Audit-log schema

`memory/state/tool-creation-log.jsonl` — one JSON object per line:

```json
{
  "timestamp": "2026-04-26T22:18:43Z",
  "job_id": "07297cf1310a",
  "event": "promote",
  "tool_name": "precision_ratio",
  "route": "surface_to_human",
  "novelty": 0.75,
  "stakes": 0.65,
  "reversibility": 0.4,
  "details": { "diff_lines": 54 }
}
```

The `dev_loop.py` watchdog can grep this log to verify the Three Laws
held during every forge cycle.

---

## Phase 1 → Phase 2 upgrade path

| Phase | Sandbox | Boot time | Isolation | Status |
|---|---|---|---|---|
| **1** | `DockerSandbox` (Linux container) | sub-second | namespaces + cgroups | **shipped** |
| **2** | `FirecrackerSandbox` (microVM) | ~125 ms | hardware virtualization | future |

The interface is identical (`Sandbox.run(command, workdir, *, timeout_s, mem_mb, network)`)
so the upgrade is a swap of one class for another — no caller changes.

---

## Open follow-ups (deferred)

- **Promotion lifecycle gating.** Once a tool has been used N≥5 times in
  `_promoted/` with positive ratings, fast-track to `skills/canonical/`.
  Implementation deferred until 60 days of operational data exist.
- **Cross-tool composition.** v1 forbids auto-generated tools from calling
  *other* auto-generated tools (trust boundary). Revisit after operational
  data.
- **Live `DockerSandbox` integration tests.** Today these run in CI/local
  whenever a Docker daemon is available; they `skip` cleanly otherwise.
