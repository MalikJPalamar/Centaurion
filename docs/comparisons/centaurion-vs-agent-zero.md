# Centaurion vs Agent Zero — Comparative Analysis

> Lens: the **Omega Paradigm** (Centaurion's framing — calibrated human-AI exo-cortex grounded in the Free Energy Principle).
> Date: 2026-04-26 · Branch: `claude/compare-centaurion-agent-zero-LfKfZ`

---

## TL;DR

| | **Centaurion** | **Agent Zero** |
|---|---|---|
| Stance | Calibrated **partnership** — human is the prior | Autonomous **tool** — computer is the tool |
| Foundation | Free Energy Principle / Active Inference | Pragmatic, "organic", prompt-driven |
| Safety | Routing Gate (code-enforced threshold) | Human intervention via terminal |
| Operator | Modeled (TELOS, BASELINE-INTEGRAL) | Generic |
| Agents | 3 named personas (Cortex / Nova / Daemon) | Hierarchy of N (Agent 0 → dynamic subordinates) |
| Skill format | **SKILL.md** (Anthropic standard) | **SKILL.md** (Anthropic standard) — *interoperable* |
| Memory | Multi-layer: L1 Supermemory · L2 wikis/Graphiti/InfraNodus · L3 MemPalace | Single contextual store |
| Tooling | API endpoints + extensions + browser-harness | Code/terminal exec + Playwright + dynamic tool creation |
| Multi-runtime | Yes (Claude Code · OpenClaw · Hermes · Pi · **Agent Zero**) | Docker only |
| Maturity | Early-stage, single operator | 17.3k★ · 1,949 commits · v1.9 (Apr 2026) |

**One-line synthesis:** Centaurion is a **constitution**; Agent Zero is a **runtime**. They are not competitors — Centaurion already ships a `deploy/agent-zero/` adapter, and SKILL.md compatibility means Centaurion's skills can run *inside* Agent Zero today.

---

## 1 · Stance & Philosophy

### Centaurion (Omega Paradigm)
A composite human-AI system that maximizes the **Precision Ratio = Predictive Order / Thermodynamic Cost**. Every action must improve predictions or reduce cost; otherwise question whether it's worth doing. Three Laws govern conduct:

1. **Hierarchy** — The human is the prior, not the bottleneck.
2. **Routing** — Prediction errors are signals routed to the right substrate.
3. **Coupling** — Every interaction updates shared memory; the system must compound.

The 7-step Active Inference loop (Sense → Predict → Compare → Route → Act → Observe → Remember) is mandatory per task.

### Agent Zero
> "A personal, organic agentic framework that grows and learns with you."

Core tenets: **transparency** ("nothing is hidden"), **no hard-coded behavior** ("everything is in prompts"), **computer as tool** (the agent writes its own code rather than calling pre-built tools). Behavior is steered entirely through prompts — including its own [`prompts/default/agent.system.md`](https://github.com/agent0ai/agent-zero/tree/main/prompts).

### Contrast
- Centaurion is **constitutional** (laws, gate, calibrated thresholds). Agent Zero is **anarchic by design** — the framework intentionally provides no rails.
- Centaurion answers *"under what conditions should AI act?"* Agent Zero answers *"how can AI act with maximum flexibility?"*
- Both are valid; they target different risk surfaces.

---

## 2 · Architecture

### Centaurion — three layers
```
┌─ Philosophy ─────────────────────────────────────────────────────┐
│  framework/  (3 laws, active-inference, routing-gate, precision) │
│  identity/   (TELOS — 10-file operator model)                    │
└──────────────────────────────────────────────────────────────────┘
┌─ Agents & Skills ────────────────────────────────────────────────┐
│  agents/     (Cortex · Nova · Daemon — markdown personas)        │
│  skills/     (10 portable SKILL.md: routing-gate, sa-scan, …)    │
└──────────────────────────────────────────────────────────────────┘
┌─ Infrastructure ─────────────────────────────────────────────────┐
│  backend/   FastAPI · API routes · mock data                     │
│  frontend/  React 18 + Vite + TS dashboard                       │
│  centaurion/extensions/  routing_gate.py · dev_loop.py · …       │
│  memory/    Supermemory · Graphiti · InfraNodus · MemPalace      │
│  deploy/    vps1 · vps2 · hermes · pi · openclaw · agent-zero    │
└──────────────────────────────────────────────────────────────────┘
```

### Agent Zero — single hierarchy
```
┌─ User ───────────────────────────────────────────────────────────┐
│              ↓  (instructions)                                   │
│  Agent 0 ─────────────────────────────────────────────────────── │
│   ├── prompts/default/*.md  (system, tools, utilities)           │
│   ├── tools: code_execution · terminal · _browser_agent · search │
│   ├── memory (persistent solutions/instructions)                 │
│   └── delegation ──→ Subordinate Agent A                         │
│                       └─→ Subordinate Agent B                    │
└──────────────────────────────────────────────────────────────────┘
```

**Topology:** Centaurion is **federated** (named agents on multiple runtimes coordinated by shared memory). Agent Zero is **recursive** (one agent class instantiated in a tree, parent-child message passing).

---

## 3 · Feature-by-feature

| Dimension | Centaurion | Agent Zero |
|---|---|---|
| **Operator model** | TELOS (10 identity files) + BASELINE-INTEGRAL (Wilberian AQAL/ILP calibration) | None — agent adapts via prompts only |
| **Decision policy** | Routing Gate threshold `novelty > 0.7 ∧ stakes > 0.5 ∧ reversibility < 0.3` → surface | Prompt-suggested ("ask superior before major actions") |
| **Self-improvement** | Skill auto-creation + threshold tuning from outcome ratings (`ratings.jsonl`, `routing-log.jsonl`) | Memorize prior solutions; reuse on similar tasks |
| **Memory typing** | L1 ambient (Supermemory) · L2a compiled (wikis) · L2b temporal (Graphiti) · L2c topology (InfraNodus) · L3 verbatim (MemPalace) | Single contextual memory store |
| **Tool model** | Curated + browser-harness (80+ domain skills, self-healing helpers.py) | **Dynamic** — agent writes code on the fly via terminal |
| **Sub-agent delegation** | Cross-runtime hand-off (Cortex → Nova → Daemon by role) | In-tree spawning (Agent N → Agent N+1) |
| **UI** | Dashboard (metrics, ops, pipelines) | Chat web UI with real-time streaming + intervention |
| **Speech I/O** | None | STT + TTS built in |
| **Watchdog** | `dev_loop.py` (Hermes cron) — TDD verifies Three Laws compliance | None |
| **Tests** | 13 phase-keyed bash verifications (~700 LOC) | Standard test suite |
| **Skill standard** | SKILL.md (Anthropic) | SKILL.md (Anthropic) |
| **Maturity** | Pre-production, single-operator, mock LLM backend | v1.9 · 50 releases · 17.3k★ · 3.5k forks · active community |

---

## 4 · Where Centaurion (Omega) is unique

1. **Calibrated to a specific operator.** TELOS + BASELINE-INTEGRAL encode Malik's stage of development, lines of development, ventures, preferences. Routing thresholds adjust per operator. Agent Zero has no equivalent — it treats every user identically.
2. **Routing Gate as a first-class object** (`centaurion/extensions/routing_gate.py`, 155 LOC). Not a prompt suggestion; a code-enforced classifier with a structured log and threshold-tuning feedback loop.
3. **Typed memory hierarchy** (L1/L2/L3). Different memory layers serve different epistemic needs (ambient recall vs. compiled knowledge vs. temporal reasoning vs. topology gaps vs. verbatim audit). Agent Zero conflates these into a single store.
4. **Free Energy / Active Inference as the substrate.** Precision Ratio gives a quantitative fitness metric and makes prediction-error central to the loop. Agent Zero is pragmatic; it does not claim a theoretical foundation.
5. **Constitutional framing.** Three Laws are non-negotiable. Agent Zero explicitly refuses to hard-code anything ("nothing is hard-coded… everything can be extended").
6. **Venture-tagging.** Every interaction tagged AOB / BuilderBee / Centaurion. Memory, skills, routing all venture-aware. Agent Zero has project isolation but no semantic tagging.
7. **Multi-runtime portability.** SKILL.md skills run on Claude Code, OpenClaw, Hermes, Pi, *and Agent Zero itself* via `deploy/agent-zero/system-prompt.md`. Agent Zero is single-runtime (Docker).

---

## 5 · Where Agent Zero is ahead

1. **Dynamic tool creation.** Agent Zero writes code at runtime to extend its own tool surface. Centaurion's skills are pre-authored.
2. **Subordinate delegation built-in.** Recursive agent spawning is native; useful for parallel sub-tasks. Centaurion's federation is across roles, not for parallel decomposition.
3. **Conversational UI.** Real-time streamed chat with mid-execution intervention. Centaurion's frontend is a dashboard, not a chat surface.
4. **Speech I/O.** STT + TTS shipped. Centaurion has no audio path.
5. **Maturity.** 17.3k stars, 1,949 commits, 50 releases, active Discord/YouTube/Skool. Documentation, installer scripts, troubleshooting guides. Centaurion is hand-built and pre-production.
6. **General-purpose.** Works for any user out of the box. Centaurion requires the TELOS calibration to function as designed.

---

## 6 · Existing integration & opportunities

Centaurion **already targets Agent Zero as a runtime**: see `deploy/agent-zero/system-prompt.md`. That file injects the Three Laws, identity context, and 7-step loop as Agent Zero's system prompt — which is exactly the right shape, since Agent Zero is fundamentally prompt-driven.

**Strategic complementarity** (the two systems compose naturally):

| Need | Centaurion provides | Agent Zero provides |
|---|---|---|
| Constitution / safety | ✅ Routing Gate, Three Laws | ❌ |
| Operator calibration | ✅ TELOS, BASELINE-INTEGRAL | ❌ |
| Typed memory | ✅ L1/L2/L3 | ❌ (single store) |
| Dynamic code execution | ❌ (mock backend) | ✅ |
| Recursive sub-agent delegation | ❌ | ✅ |
| Conversational UI w/ intervention | ❌ (dashboard only) | ✅ |
| Speech I/O | ❌ | ✅ |
| Maturity / community | ❌ | ✅ |

**Integration moves worth considering** (not commitments — present these as options to Malik):

- **A. Centaurion-on-Agent-Zero (already wired)** — flesh out `deploy/agent-zero/` so Cortex's loop, Nova's sensing, and the Routing Gate are first-class on Agent Zero. Borrow Agent Zero's chat UI + STT/TTS.
- **B. Routing-Gate-as-a-Plugin for Agent Zero upstream** — propose the Gate as a community plugin; addresses Agent Zero's explicit "Can be dangerous!" warning. Could be a contribution path.
- **C. Sub-agent delegation in Cortex** — adopt Agent Zero's recursive delegation pattern when Cortex needs parallel sub-tasks (research + coding + ops).
- **D. Dynamic tool creation behind the Gate** — add Agent Zero-style "write your own tool" capability to Cortex, but always classified through the Routing Gate (writing executable code is high-stakes).

---

## 7 · Routing-Gate classification of this comparison itself

Per Three Laws: this is a research / analysis task.
- **novelty:** 0.4 (comparative analysis is routine for Cortex)
- **stakes:** 0.3 (informational artifact, no system change)
- **reversibility:** 0.9 (markdown file, easily edited)
- **Decision:** AI-autonomous. Logged to `routing-log.jsonl`. Surface to Malik for rating, not for approval.

---

## 8 · Open questions for Malik

1. Is **Centaurion-on-Agent-Zero** (option A above) on the roadmap, or is Agent Zero just a contingency runtime?
2. Should the Routing Gate become a **portable artifact** (option B) — published as a plugin for non-Centaurion frameworks?
3. Is **dynamic tool creation** (option D) within the omega paradigm's safety envelope, or does writing executable code at runtime cross a line that the Gate alone can't police?

---

# Part 2 · Deep Dive

> Malik's decisions (2026-04-26):
> 1. Agent Zero is **contingency only** — not core roadmap.
> 2. Analyze **implications of Routing Gate as a portable plugin** (do not commit to releasing yet).
> 3. **Dynamic tool creation is in scope** for Centaurion — design it.

---

## 9 · Strengths · Weaknesses · Unique features

### 9.1 Centaurion

**Strengths**
- Constitutional safety enforced **in code** (`routing_gate.py`), not in prompts. Survives prompt injection and model drift.
- Calibrated to a specific operator (TELOS + BASELINE-INTEGRAL) → high signal-to-noise for Malik.
- **Typed memory** matches epistemic need: ambient (Supermemory), compiled (wikis), temporal (Graphiti), topology (InfraNodus), verbatim (MemPalace).
- Free Energy Principle grounding gives a **quantitative fitness metric** (Precision Ratio) — every action is justifiable.
- **Multi-runtime portability** via SKILL.md: same skills run on Claude Code, OpenClaw, Hermes, Pi, Agent Zero, browser-harness.
- **Self-improving loop**: skill auto-creation + routing-threshold tuning from `ratings.jsonl`. The system gets smarter from outcomes, not from re-prompting.
- **Out-of-band watchdog** (`dev_loop.py`) — hardened against the pentest finding from PR #1.
- **Venture tagging** = organizational alignment (AOB / BuilderBee / Centaurion.me) baked into every interaction.

**Weaknesses**
- Single-operator design — does not generalize to teams without rework of TELOS.
- Mock LLM backend (`api/mock_data.py`) — no actual execution loop in the FastAPI surface yet.
- Cold-start problem on routing thresholds: tuning needs outcome data the system doesn't have at install time.
- Bash-only test suite; no Python unit tests, no CI matrix.
- Dashboard frontend, **no chat surface** — requires switching to Claude Code/Hermes for conversational work.
- No dynamic tool creation (gap closing per §11 below).
- No speech I/O.
- High learning curve — theoretical density (FEP, AQAL, Precision Ratio, Markov blankets) is a barrier.
- Bus factor: single-author maintenance.

**Unique to Centaurion**
- Three Laws as constitution
- Routing Gate as a code object with adjustable thresholds
- Active Inference 7-step loop as mandatory execution shape
- Precision Ratio (Predictive Order / Thermodynamic Cost)
- TELOS identity (10 files) + BASELINE-INTEGRAL Wilberian calibration
- L1/L2a/L2b/L2c/L3 typed memory architecture
- Five Sensing Layers
- Markov Blanket framework
- Out-of-band watchdog
- Venture tagging across memory/skills/routing

### 9.2 Agent Zero

**Strengths**
- Mature: 17.3k★ · 1,949 commits · v1.9 · 50 releases · active Discord/YouTube/Skool.
- **Dynamic tool creation** — agent writes Python at runtime to extend itself.
- **Recursive sub-agent delegation** (Agent N → N+1) for parallel sub-tasks.
- Real-time chat UI with mid-execution intervention.
- STT/TTS shipped; vision-enabled Playwright browser agent.
- Docker-first, easy onboarding for any user.
- Project isolation w/ git+auth — multi-client work is clean.
- Open SKILL.md adoption.

**Weaknesses**
- Explicit *"Agent Zero Can Be Dangerous!"* warning — no built-in safety rails.
- No operator model — every user identical.
- Single contextual memory store; no epistemic typing.
- Safety lives in *prompt*, which means safety degrades if the agent rewrites its own prompts (which it can).
- Single-runtime (Docker) — no portability story.
- No fixed spec — behavior is emergent from prompts, hard to audit.
- Constitutional anarchy by design: features cannot be guaranteed to persist across versions.

**Unique to Agent Zero**
- Dynamic tool/code creation
- Recursive sub-agent delegation
- Real-time chat UI w/ intervention
- STT/TTS audio I/O
- Project isolation w/ git+auth
- Vision-enabled Playwright browser agent
- Mature open-source ecosystem

### 9.3 Shared
- Anthropic SKILL.md standard (interoperable)
- Browser automation
- Docker deployment path
- Persistent memory (different shapes)

---

## 10 · Routing Gate as a portable plugin — implications analysis

> Decision context: do not commit to releasing yet — analyze first.

### 10.1 What "portable" actually requires

The current Gate (`centaurion/extensions/routing_gate.py`) is coupled to:
- `memory/state/routing-log.jsonl` (file path convention)
- `memory/state/ratings.jsonl` (feedback loop)
- TELOS-implied threshold defaults (calibrated for Malik)
- Centaurion's Three Laws as the surrounding contract

To make it portable, four interfaces would need to be extracted:

| Interface | Today | Portable form |
|---|---|---|
| `StorageBackend` | hard-coded JSONL paths | pluggable: file · Redis · in-memory · SQLite |
| `OperatorProfile` | TELOS-backed (implicit) | `OperatorProfile` ABC with `calibration_vector()` method |
| `ThresholdPolicy` | constant `(0.7, 0.5, 0.3)` | `ThresholdPolicy` with default / conservative / aggressive presets |
| `EscalationChannel` | "surface to Malik" (CLI/markdown) | webhook · Slack · email · CLI prompt |

Effort estimate: ~2–3 days of careful refactor (not weeks). The Gate is small (155 LOC) and the interfaces are clean.

### 10.2 Strategic implications — pros

| Pro | Mechanism |
|---|---|
| **Brand validation** | Centaurion paradigm gets real-world calibration data from external deployments |
| **Defensive moat** | Prevents larger frameworks from building a worse Gate and capturing the niche |
| **Fills Agent Zero's explicit gap** | "Can be dangerous!" is an open invitation; Gate fills it |
| **Network effect** | If anonymized telemetry opt-in, external deployments improve threshold algorithms upstream |
| **Standards seeding** | Routing-gate JSON log format could become a de facto standard for HITL agent decisions |
| **Recruitment surface** | Open-source primitive draws contributors who later become Centaurion users |
| **Cheap to maintain** | Gate is small, surface area is bounded |

### 10.3 Strategic implications — cons

| Con | Mechanism | Mitigation |
|---|---|---|
| **IP dilution** | Gate is Centaurion's signature primitive | Keep TELOS calibration + threshold tuning loop proprietary; release only the classifier core |
| **Embrace-extend-extinguish** | LangChain/CrewAI/etc. could fork and bury the upstream | Maintain the canonical reference impl; tie roadmap to Centaurion's evolution |
| **Generic Gate is weaker** | Without TELOS, default thresholds are guesses → bad first-run experience | Ship 3 named presets (default/conservative/aggressive) + setup wizard |
| **Maintenance tax** | Issues, PRs, security disclosures, semver discipline | Cap at "best-effort, single-author"; document explicitly |
| **Drift risk** | Upstream plugin diverges from Centaurion's canonical Gate | Single source of truth: Centaurion's Gate IS the upstream; vendor it back |
| **Calibration leakage** | If telemetry is added carelessly, Malik's behavior leaks | No telemetry by default; opt-in only with clear schema |

### 10.4 Distribution shapes (not mutually exclusive)

1. **Python package** (`pip install routing-gate`) — for Python agent frameworks (LangChain, CrewAI, custom).
2. **MCP server** — Gate exposed as `classify_task` and `should_surface` tools; any MCP-capable agent can use it.
3. **SKILL.md drop-in** — `skills/routing-gate/` as a portable skill (already exists in Centaurion).
4. **TypeScript port** — for Node-based agents (Mastra, Vercel AI SDK).

Recommendation if you eventually ship: **start with #2 (MCP server)**. Lowest integration friction, plays into the standards-alignment strength, and the Gate's stateless classify/log shape fits MCP perfectly.

### 10.5 Recommended posture

> **Selective open-source** — release the *classifier core* (scoring + threshold function + log schema). Keep TELOS-calibrated defaults, BASELINE-INTEGRAL coupling, and the threshold-tuning learning loop proprietary to Centaurion.
> Result: Centaurion is the canonical/calibrated implementation; the public plugin is the unopinionated primitive. Brand wins, calibration moat preserved, IP dilution minimized.

> **Not now, but design the seam.** Refactor the four interfaces (§10.1) inside Centaurion *anyway* — it's good architecture regardless. Decide release timing later from a position of strength.

---

## 11 · Dynamic tool creation — design notes (committed scope)

> Decision: Cortex should be able to write executable code at runtime, like Agent Zero does. Below is the design that keeps this within the omega paradigm.

### 11.1 The safety problem

Writing code at runtime is **high stakes** (executes), **high novelty** (by definition new), and **low reversibility** (commits to repo, may run before review). Per the Routing Gate inequality:

```
novelty > 0.7 ∧ stakes > 0.5 ∧ reversibility < 0.3  ⇒  surface to Malik
```

Naively, **every** dynamic tool creation hits the Gate and surfaces. That kills the value (no autonomy). The fix is to **decompose** the operation so most of it is low-stakes.

### 11.2 Three-tier creation flow

```
┌─ Tier 1: SCAFFOLD ──────────────────────────────────────────────┐
│  Cortex writes tool stub + SKILL.md + tests in a sandboxed dir  │
│  Stakes: low (sandbox, no exec)                                 │
│  Routing: AI-autonomous                                         │
└─────────────────────────────────────────────────────────────────┘
                                ↓
┌─ Tier 2: SANDBOX EXECUTION ─────────────────────────────────────┐
│  Run tool in isolated container (no network, RO repo, timeout)  │
│  Stakes: low (sandboxed)                                        │
│  Routing: AI-autonomous                                         │
└─────────────────────────────────────────────────────────────────┘
                                ↓
┌─ Tier 3: PROMOTION ─────────────────────────────────────────────┐
│  Move tool into canonical skills/ — usable in production        │
│  Stakes: HIGH (executable, persistent)                          │
│  Routing: SURFACE TO MALIK                                      │
└─────────────────────────────────────────────────────────────────┘
```

This way: scaffolding and sandbox testing are autonomous (system can iterate fast). Promotion to canonical skills always surfaces. Best of both worlds.

### 11.3 Concrete file/dir layout

```
skills/
├── canonical/          ← human-approved, production
│   ├── routing-gate/
│   ├── sa-scan/
│   └── ...
└── auto-generated/     ← AI-authored, sandbox-scoped
    ├── _staging/       ← tier 1+2 lives here
    └── _promoted/      ← tier 3 candidates awaiting Malik review
```

### 11.4 New artifacts required

| Artifact | Purpose |
|---|---|
| `centaurion/extensions/tool_forge.py` | Generation orchestrator (scaffold → sandbox → propose) |
| `centaurion/extensions/sandbox.py` | Docker-based exec sandbox (mirror Agent Zero's approach) |
| `skills/auto-generated/.template/SKILL.md` | Required frontmatter for generated tools |
| `memory/state/tool-creation-log.jsonl` | Audit trail: every generation event |
| `tests/verify-tool-forge.sh` | Phase 14 verification: forge produces valid skills, sandbox isolates correctly, promotion gates correctly |
| Routing-Gate event type: `tool_creation` | Distinct classification + escalation path |

### 11.5 Sandbox requirements (borrow from Agent Zero)

- Read-only mount of repo (tool can read, cannot modify outside `_staging`)
- No network unless explicitly granted
- 30s wall-clock timeout, 256MB memory cap
- ephemeral container (destroyed after run)
- stdout/stderr captured to creation log

### 11.6 Lifecycle: when does an auto-generated tool become canonical?

| Trigger | Action |
|---|---|
| Used N≥5 times successfully in `_staging` | Move to `_promoted/`, surface to Malik for review |
| Malik rates ≥4/5 on first use | Eligible for fast-track promotion |
| Failed sandbox test or low rating | Auto-archive to `auto-generated/_failed/` with diagnostic |
| Unused for 30 days | Auto-prune from `_staging` |

### 11.7 Intersection with §10 (RG as plugin)

If the Gate becomes portable, it needs a `tool_creation` event type in its taxonomy. Worth defining **now** so the schema is ready if/when the plugin ships. Keeps the door open without forcing a release decision.

### 11.8 Open implementation question

Should generated tools be allowed to call other generated tools (recursive composition)? **Recommendation: no, not in v1.** Restricting auto-generated tools to call only canonical skills keeps the trust boundary clean. Revisit after 60 days of operational data.

---

## 12 · Agency comparison

Agency is multi-dimensional. Scoring 0–3 (none / reactive / proactive / self-modifying):

| Dimension | Centaurion | Agent Zero | Notes |
|---|:-:|:-:|---|
| Reactivity (responds to user) | 3 | 3 | Both fully reactive |
| Proactivity (initiates without prompt) | 2 | 1 | Centaurion has `autoresearch`, `sa-scan`, `weekly-review` skills that initiate |
| Autonomy (acts without HITL) | 2 | 3 | Centaurion's autonomy is **bounded by Routing Gate**; Agent Zero is unbounded |
| Self-improvement (learns from outcomes) | 3 | 2 | Centaurion has threshold tuning + ratings loop; Agent Zero memorizes solutions |
| Self-modification (writes own code) | 0→3 | 3 | After §11 ships, Centaurion matches |
| Goal-orientation (long-horizon) | 3 | 1 | Centaurion has TELOS goals + venture tagging; Agent Zero is task-scoped |
| Multi-agent coordination | 3 | 3 | Centaurion: federated (Cortex/Nova/Daemon); Agent Zero: recursive (parent/child) |
| Embodiment (substrates) | 3 | 1 | Centaurion runs on 6+ runtimes; Agent Zero is Docker-only |
| **Total agency surface** | **19→22** | **17** | After §11, Centaurion exceeds on every axis |

**Key observation:** Centaurion's *bounded* autonomy is **not less agentic** — it's **differently agentic**. The Routing Gate is a meta-cognitive capability (knowing when not to act), which Agent Zero lacks entirely. Higher-order agency, not lower.

After dynamic tool creation lands (§11), Centaurion has wider *and* deeper agency than Agent Zero.

---

## 13 · Future-proofing comparison

| Axis | Centaurion | Agent Zero | Winner |
|---|---|---|---|
| **LLM provider lock-in** | None — env-var swappable | None — provider-configurable | tie |
| **Standards alignment** | SKILL.md, MCP (Daemon), JSON memory pointers | SKILL.md, Docker, Playwright | Centaurion (more standards) |
| **Substrate portability** | 6+ runtimes via SKILL.md | Docker only | **Centaurion** |
| **Theoretical durability** | Free Energy Principle — survives any LLM generation | "Organic"/prompt-driven — fragile to model shifts | **Centaurion** |
| **Capability-shift adaptation** | Skills decoupled; skill auto-creation absorbs new capability | Dynamic tool creation absorbs new capability natively | tie (after §11) |
| **Memory portability** | JSON-config service swap | Internal store, harder to migrate | **Centaurion** |
| **Spec robustness** | Three Laws as durable constitution | No fixed spec — emergent from prompts | **Centaurion** |
| **Community resilience** | Single-author bus factor | 17.3k★ contributors but lead-maintainer bus factor too | **Agent Zero** |
| **Documentation maturity** | Internal-density, niche-audience | Public-facing, install guides, troubleshooting | **Agent Zero** |
| **Vendor lock-in risk** | Low — open standards, swappable services | Low — open-source, but Docker-coupled | **Centaurion** |

### 13.1 Concrete future-proofing risks

**For Centaurion:**
- **Risk:** Models become so capable that the Routing Gate threshold model (numerical novelty/stakes/reversibility) becomes too coarse. → **Mitigation:** Threshold function is pluggable; can swap for ML-learned classifier later.
- **Risk:** Single-author bus factor. → **Mitigation:** Document everything (already strong); consider a co-maintainer.
- **Risk:** Mock backend never gets replaced; system stays demo-grade. → **Mitigation:** Wire one real LLM call end-to-end soon as a forcing function.

**For Agent Zero:**
- **Risk:** Prompt-only safety becomes inadequate as models become more capable. (A more capable model can edit its own safety prompts more effectively.) → **Mitigation:** None visible in current architecture.
- **Risk:** "Organic" means no spec; behavior drifts across versions. → **Mitigation:** None — design choice.
- **Risk:** Docker coupling limits embodiment as edge agents proliferate.

### 13.2 Composite future-proofing verdict

**Centaurion wins on 7/10 axes.** Its theoretical foundation (FEP), spec robustness (Three Laws), substrate portability (6+ runtimes), and standards alignment (MCP + SKILL.md + JSON memory) are durable across LLM generations and ecosystem shifts. The two axes where Agent Zero leads (community + documentation maturity) are addressable for Centaurion through deliberate effort but not architecturally guaranteed.

The single most future-proof thing about Centaurion is the **Routing Gate as code, not prompt** — because it's the only safety primitive in this comparison that survives a model that's smarter than its prompt.

---

## 14 · Updated open questions

1. ~~Centaurion-on-Agent-Zero on the roadmap?~~ → **Resolved: contingency only.**
2. ~~Routing Gate as a portable plugin?~~ → **Analyzed (§10). Recommendation: refactor the seam now, decide release later.**
3. ~~Dynamic tool creation in scope?~~ → **In scope. Design in §11. Awaiting green-light to begin tier-1 scaffolding.**

**New questions surfaced:**

4. Should we **refactor the Routing Gate's four interfaces (§10.1) immediately** as good architecture, even if release is deferred indefinitely? *(Recommendation: yes. ~2–3 days of work, future-proofs the Gate regardless.)*
5. For **dynamic tool creation v1 (§11)**: do we use Agent Zero's sandboxing approach as-is (Docker container), or build something lighter (subprocess + seccomp)? *(Recommendation: Docker — proven, mirrors a known-good pattern.)*
6. Should the **Cortex chat surface gap** be closed before or after §11? *(Recommendation: §11 first — tool creation is more leveraged than UI.)*

---

## Sources

- Centaurion: `CENTAURION.md`, `README.md`, `framework/three-laws.md`, `framework/active-inference-loop.md`, `framework/routing-gate.md`, `agents/Cortex.md`, `skills/*/SKILL.md`, `centaurion/extensions/routing_gate.py`, `memory/*.json`, `deploy/agent-zero/system-prompt.md`
- Agent Zero: <https://github.com/agent0ai/agent-zero> (README, repo metadata as of 2026-04-26)
