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

## Sources

- Centaurion: `CENTAURION.md`, `README.md`, `framework/three-laws.md`, `framework/active-inference-loop.md`, `framework/routing-gate.md`, `agents/Cortex.md`, `skills/*/SKILL.md`, `centaurion/extensions/routing_gate.py`, `memory/*.json`, `deploy/agent-zero/system-prompt.md`
- Agent Zero: <https://github.com/agent0ai/agent-zero> (README, repo metadata as of 2026-04-26)
