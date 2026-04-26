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

# Part 3 · Rubric unpacking + Comet & Kimi K2.6 comparison

> Follow-up requests: (a) define the agency and future-proofing axes operationally and show the evidence behind each score; (b) examine Agent Zero's "computer-as-tool + Docker" pattern and compare it to Perplexity Comet and Moonshot Kimi K2.6, which appear to offer superior agentic execution while preserving safety.

---

## 15 · Agency rubric — 8 axes unpacked

**Scoring scale (0–3):**
- **0** = Absent. Capability not present.
- **1** = Reactive / shallow. Capability present but only when explicitly invoked, narrow, or stub-quality.
- **2** = Operational. Capability present with depth; recognizable as a real feature.
- **3** = First-class / structural. Capability is core to the design and used by default.

| # | Axis | Operational definition |
|---|---|---|
| A1 | **Reactivity** | Can it respond meaningfully to a user-issued task? |
| A2 | **Proactivity** | Does it initiate work without an immediate user prompt (cron, watchers, scheduled scans)? |
| A3 | **Autonomy** | Can it complete tasks end-to-end without human-in-the-loop confirmation? |
| A4 | **Self-improvement** | Does the system get measurably better over time from outcome data, not from re-prompting? |
| A5 | **Self-modification** | Can it write/modify executable code that becomes part of its own runtime? |
| A6 | **Goal-orientation** | Does it pursue long-horizon objectives across many sessions, not just single-task scope? |
| A7 | **Multi-agent coordination** | Does it coordinate with other agents to solve sub-tasks? |
| A8 | **Embodiment** | How many distinct execution substrates can it run on? |

### 15.1 Per-axis evidence

| Axis | Centaurion | score | Agent Zero | score |
|---|---|:-:|---|:-:|
| A1 Reactivity | Cortex/Nova/Daemon respond to task instructions; full SKILL.md library invoked on demand | **3** | Agent 0 responds to chat; tools invoked dynamically | **3** |
| A2 Proactivity | `skills/autoresearch/` runs overnight; `skills/sa-scan/` scheduled stock scans; `skills/weekly-review/`; `dev_loop.py` is a Hermes cron task; `workflows/feedback-capture.md` automation | **2** | No scheduler in stock framework; agent waits for user input. Subordinate spawning is reactive not proactive | **1** |
| A3 Autonomy | Bounded by Routing Gate. Most tasks (low-stakes/reversible) execute end-to-end without surfacing | **2** | Unbounded — explicit "Can be dangerous!" warning. Agent acts until user intervenes | **3** |
| A4 Self-improvement | `memory/state/ratings.jsonl` + `routing-log.jsonl` feed threshold tuning; outcome data → policy update; documented in `framework/routing-gate.md` | **3** | Memorizes prior solutions for faster recall on similar tasks; no closed-loop policy update | **2** |
| A5 Self-modification | None today (skills are hand-authored). Becomes **3** after §11 (dynamic tool forge with sandbox + promotion) | **0 → 3** | Writes Python at runtime via terminal tool; no formal lifecycle but unlimited surface | **3** |
| A6 Goal-orientation | `identity/GOALS.md` + `identity/MISSION.md` loaded every session; venture tagging persists context across tasks; long-horizon TELOS pursuit is L0 prior | **3** | Task-scoped; no persistent goal model across sessions beyond memorized solutions | **1** |
| A7 Multi-agent | Federated: Cortex (reasoning) ↔ Nova (sensing) ↔ Daemon (memory) across runtimes; coordinated via shared memory | **3** | Recursive: Agent N spawns Agent N+1 for sub-tasks; parent-child message passing. Deep but homogeneous | **3** |
| A8 Embodiment | Verified runtimes: Claude Code, OpenClaw, Hermes, Pi, Agent Zero (`deploy/agent-zero/`), browser-harness — 6 substrates with same SKILL.md | **3** | Docker container only | **1** |

### 15.2 Totals

| | Today | After §11 ships |
|---|:-:|:-:|
| Centaurion | 19 | **22** |
| Agent Zero | 17 | 17 |

Centaurion's *bounded* autonomy (A3=2 vs A2.AZ=3) is intentional, not a deficit. Agent Zero's high autonomy carries the explicit cost it acknowledges: it can be dangerous.

---

## 16 · Future-proofing rubric — 10 axes unpacked

**Scoring:** Winner per axis (Centaurion / Agent Zero / tie). Reasoning shows the durability mechanism.

| # | Axis | Operational definition | Why it matters in 2027–2030 |
|---|---|---|---|
| F1 | **LLM provider lock-in** | How tightly is the system bound to one provider? | Provider economics + capability rankings shift constantly |
| F2 | **Standards alignment** | How many open standards does it adopt (MCP, SKILL.md, OpenAI API shape, etc.)? | Standards reduce migration cost when ecosystem shifts |
| F3 | **Substrate portability** | How many execution targets work without code change? | Edge agents, mobile, embedded — substrate diversity is growing |
| F4 | **Theoretical durability** | Is the foundation a principle that survives model generations? | Ad-hoc patterns rot; principles compound |
| F5 | **Capability-shift adaptation** | When models get smarter, does the system absorb the gain or get bypassed? | Each generation reshapes "what's worth automating" |
| F6 | **Memory portability** | Can memory move between deployments without loss? | Lock-in to a memory store is silent vendor capture |
| F7 | **Spec robustness** | Is there a fixed spec that can be audited/versioned? | Required for regulated deployments + reproducibility |
| F8 | **Community resilience** | Does the project survive its lead maintainer leaving? | Bus-factor risk |
| F9 | **Documentation maturity** | Can a stranger onboard from docs alone? | Predicts adoption + contribution |
| F10 | **Vendor lock-in risk** | Aggregate of F1+F3+F6 — how trapped are users? | Strategic optionality |

### 16.1 Per-axis evidence

| Axis | Centaurion evidence | Agent Zero evidence | Winner |
|---|---|---|---|
| F1 LLM lock-in | `OPENAI_API_KEY`, `ANTHROPIC_API_KEY` env-var swappable; SKILL.md is provider-agnostic | Multi-provider via config; provider-agnostic | **tie** |
| F2 Standards | SKILL.md (Anthropic) + MCP server (Daemon) + JSON memory pointers + Three Laws as informal spec | SKILL.md (Anthropic) + Docker + Playwright | **Centaurion** (more standards) |
| F3 Substrate portability | 6 verified runtimes (Claude Code, OpenClaw, Hermes, Pi, Agent Zero, browser-harness) | Docker only (1) | **Centaurion** |
| F4 Theoretical durability | Free Energy Principle is 20+ years old, generation-independent | "Organic"/prompt-driven — depends on current model behavior | **Centaurion** |
| F5 Capability-shift adaptation | Skill auto-creation (after §11) + threshold tuning absorb new capability | Dynamic tool creation absorbs new capability natively (today) | **tie after §11** |
| F6 Memory portability | JSON-config service swap; memory layers are pointers not data | Internal contextual store; harder to extract | **Centaurion** |
| F7 Spec robustness | Three Laws + Routing Gate inequality + 7-step loop = auditable contract | No fixed spec by design — emergent from prompts | **Centaurion** |
| F8 Community resilience | Single-author bus factor | 17.3k★ but lead-maintainer bus factor too | **Agent Zero** |
| F9 Documentation maturity | Internal-density; assumes reader knows TELOS / FEP / AQAL | Public install guides, troubleshooting, video tutorials | **Agent Zero** |
| F10 Vendor lock-in | Low (open standards + multi-runtime + portable memory) | Low (open-source, but Docker-coupled and single-runtime) | **Centaurion** |

### 16.2 Totals

| | Wins | Ties |
|---|:-:|:-:|
| Centaurion | **7** | 2 |
| Agent Zero | **2** | 2 |

The single most future-proof property is **F4 + F7 + F10 combined**: theoretical foundation + auditable spec + low lock-in. That cluster is what makes a system survive an ecosystem shift, not just a model upgrade.

---

## 17 · Agent Zero's "computer as tool" pattern — concrete unpacking

> User intuition: Comet and Kimi seem superior for agentic execution while still safe through Docker. Let's verify this claim against what each system actually does.

### 17.1 What Agent Zero actually does

From the README + architecture investigation:

```
┌────────────────────────────────────────────────────────────┐
│  HOST MACHINE                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  DOCKER CONTAINER  (agent0ai/agent-zero image)       │  │
│  │  ┌────────────────────────────────────────────────┐  │  │
│  │  │  Agent Zero framework (Python)                 │  │  │
│  │  │  ├── Web UI (port 80)                          │  │  │
│  │  │  ├── Prompt loader → LLM provider              │  │  │
│  │  │  ├── Tool: code_execution → exec'd IN-CONTAINER│  │  │
│  │  │  ├── Tool: terminal     → bash IN-CONTAINER    │  │  │
│  │  │  ├── Tool: browser      → Playwright Chromium  │  │  │
│  │  │  └── Subordinate agents → spawned IN-CONTAINER │  │  │
│  │  └────────────────────────────────────────────────┘  │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────┘
```

**Key fact:** the Docker container is the *whole framework's* runtime, not a separate per-task sandbox. Code the agent writes runs in the **same** container as the agent itself — there is no inner sandbox boundary. Isolation is a single, coarse host-vs-container line.

**Implications:**
- **Pro:** Simple, explicit, easy to reason about. The host is safe.
- **Con:** A compromised tool can compromise the agent (within-container blast radius is total). Memory + credentials + browser cookies all share the same trust domain.
- **Con:** Persistence: anything the agent installs/writes persists in the container. Useful, but also means a poisoned step poisons future steps.

### 17.2 Perplexity Comet — different pattern

| Component | Where it runs |
|---|---|
| Perplexity backend | Perplexity cloud (Opus 4.5 reasoning) |
| Browser UI | Local Chromium fork |
| Browser automation | Custom Chrome Extension(s) controlling the actual browser |
| Communication | SSE (sidepanel) + WebSocket (automation) |

**Comet is not Docker-based.** It runs the agent inside the user's *real* browser, with the user's real cookies and sessions. This is the source of both its power (can do real shopping/checkout/email tasks) and its danger.

**Verified safety profile (2026):** Comet has had visible security stumbles — the [Zenity reverse-engineering analysis](https://labs.zenity.io/p/perplexity-comet-a-reversing-story) and [coverage of 2026-Q1 instability](https://mwm.ai/articles/comet-ai-browser-viral-sensation-2026-03-23) show prompt-injection and session-hijack vectors because there is **no sandbox layer** between the agentic intent and the user's authenticated browser session.

**Verdict on the user's intuition:** Comet is *not* safer than Agent Zero through "Docker containers" — it doesn't use Docker at all. Its execution power comes from running directly in the user's authenticated browser, which is **less** safe than Agent Zero's container, not more. Comet is more capable for browser tasks; Agent Zero is more isolated.

### 17.3 Moonshot Kimi K2.6 — yet another pattern

Kimi K2.6 (released 2026-04-20) is fundamentally a **model + coordination protocol**, not a runtime. It provides:

- 1T-param MoE backbone (32B active, 384 experts, 8 activated/token, MLA attention)
- Agent swarm scaling: 300 sub-agents, 4,000 coordinated steps
- **Claw Groups** (research preview): heterogeneous external agents/humans collaborate as peers in a shared operational space — each carrying its own toolkits, skills, persistent memory contexts, deployable on laptops, mobile, or cloud

**Where the sandbox is:** wherever the user puts it. Each Claw Group participant brings its own execution substrate. Kimi itself is BYO-runtime — it doesn't ship a Docker isolation layer the way Agent Zero does. Safety is the deployer's responsibility.

**Verdict on the user's intuition:** Kimi K2.6's agentic execution power is real (300-agent swarm is genuinely impressive), but the safety story is **"bring your own sandbox"**, not "Docker container included." Where users wrap Kimi in Docker, isolation is comparable to Agent Zero. Where they don't, it's worse.

### 17.4 Side-by-side — execution & safety

| Property | Centaurion | Agent Zero | Comet | Kimi K2.6 |
|---|---|---|---|---|
| Where the agent runs | 6 runtimes (skill-portable) | Docker container | User's actual Chromium | BYO substrate (laptop/mobile/cloud) |
| Code execution sandbox | None today; Docker after §11 | Docker (same as agent) | None — runs in real browser | BYO |
| Browser execution | `browser-harness` (self-healing) | Playwright in container | Native Chromium (user's actual session) | BYO |
| Network isolation | Per-runtime | Container-level | None — uses user's real network/cookies | BYO |
| Per-task isolation | No (shared agent state) | No (shared container) | No (shared browser session) | No (BYO) |
| Safety primitive | **Routing Gate (code)** | Container boundary | Verification-first prompts | None built-in |
| Worst-case blast radius | Bounded by Gate refusal | Within-container | User's full digital identity | Wherever deployed |

### 17.5 Reframing the user's claim

> *"Perplexity Comet and Kimi computer seem superior for agentic execution while still safe through docker containers"*

This claim conflates three things. Disentangling:

| Claim | Reality |
|---|---|
| "Superior for agentic execution" | **Partly true.** Comet wins on browser tasks because it's *in* the browser. Kimi wins on parallel sub-agent throughput (300 agents). Agent Zero is more general-purpose than either. |
| "Safe through Docker containers" | **False for Comet** (no Docker). **Conditional for Kimi** (BYO). **True for Agent Zero** (Docker is the safety primitive). |
| "Superior to Centaurion + Agent Zero" | **No** — they're different design centers. Centaurion + Agent Zero is constitution + runtime. Comet is a browser-embedded agent. Kimi is a model + swarm protocol. |

### 17.6 What Centaurion can actually borrow

| From | What | How |
|---|---|---|
| Agent Zero | Docker-based code-execution sandbox | Adopt for §11 dynamic tool forge tier 2 (already recommended in §11.5) |
| Comet | In-browser execution model | Already partial via `browser-harness` (`deploy/browser-harness/`) — could extend to authenticated sessions for specific high-value workflows, *with* Routing Gate surfacing for any cookie-using action |
| Kimi K2.6 | Agent-swarm pattern (N sub-agents, coordinated) | Cortex's federation is currently 3 named roles. A swarm pattern could decompose research/codegen/ops into parallel sub-agents — but only worth it once dynamic tool creation lands. Sequence: §11 first, swarm later |
| Kimi K2.6 | **Claw Groups protocol** | Most interesting borrow. Heterogeneous agents + humans as peers in a shared operational space maps almost directly onto the Centaurion Coupling Law. Worth tracking as a potential interop standard. |

---

## 18 · Updated open questions

7. After §11 ships (dynamic tool forge with Docker sandbox), is it worth exploring a **swarm pattern** (Kimi-style sub-agent decomposition) for Cortex, or does the federated Cortex/Nova/Daemon model already cover that need? *(Recommendation: ship §11 first, gather operational data for 60 days, then evaluate. The federated model may already be sufficient at single-operator scale.)*
8. Should Centaurion track **Claw Groups** (Kimi K2.6's interop protocol) as a potential future integration target? *(Recommendation: yes — the principle (heterogeneous agents/humans as peers in shared operational space) is structurally compatible with the Coupling Law.)*

---

## Sources

### Centaurion (local)
- `CENTAURION.md`, `README.md`, `framework/three-laws.md`, `framework/active-inference-loop.md`, `framework/routing-gate.md`, `agents/Cortex.md`, `skills/*/SKILL.md`, `centaurion/extensions/routing_gate.py`, `memory/*.json`, `deploy/agent-zero/system-prompt.md`

### Agent Zero
- [agent0ai/agent-zero — README](https://github.com/agent0ai/agent-zero) (repo metadata as of 2026-04-26)

### Perplexity Comet
- [Comet Browser: a Personal AI Assistant](https://www.perplexity.ai/comet)
- [Introducing Comet: Browse at the speed of thought](https://www.perplexity.ai/hub/blog/introducing-comet)
- [Perplexity Comet 2026 Review — security and stability of the verification-first agentic browser (FlowFi, Medium)](https://medium.com/@FlowFi/perplexity-comet-2026-review-is-it-safe-enough-for-daily-use-agentic-browser-7c5aed839bd3)
- [Perplexity Comet: A Reversing Story (Zenity Labs)](https://labs.zenity.io/p/perplexity-comet-a-reversing-story)
- [Perplexity AI's Comet Browser Plummets from #3 to 'Not Ranked' Amid Security Flaws and Instability (MWM)](https://mwm.ai/articles/comet-ai-browser-viral-sensation-2026-03-23)

### Kimi K2.6
- [Moonshot AI Releases Kimi K2.6 with Long-Horizon Coding, Agent Swarm Scaling (MarkTechPost)](https://www.marktechpost.com/2026/04/20/moonshot-ai-releases-kimi-k2-6-with-long-horizon-coding-agent-swarm-scaling-to-300-sub-agents-and-4000-coordinated-steps/)
- [Kimi K2.6 Officially Released: The Agentic Coding Era Enters Production](https://kimi-k2.org/blog/24-kimi-k2-6-release)
- [Kimi K2.6 Has Arrived: An Open-Weight Powerhouse for Agentic Work (Kilo blog)](https://blog.kilo.ai/p/kimi-k26-has-arrived-an-open-weight)
- [Moonshot AI releases Kimi-K2.6 model with 1T parameters (SiliconANGLE)](https://siliconangle.com/2026/04/20/moonshot-ai-releases-kimi-k2-6-model-1t-parameters-attention-optimizations/)
