# Centaurion — Product Description for roxx.ai

> Prepared for **roxx.ai** as an external product-development partner. This document describes what Centaurion is today, the model it runs on, its architecture and current capabilities, and where product work would add the most leverage. It is grounded in the actual repository contents. Where something is planned-but-not-yet-built, it is flagged as an assumption or gap rather than presented as shipped.

---

## 1. Executive Summary

**AI agent framework for a single operator managing multiple businesses.** It is built as structured Markdown and JSON instruction files that run inside the Claude Code agent environment (with a portable `AGENTS.md` schema for other runtimes) and ships with a prototype web dashboard (React/FastAPI). The framework configures an AI agent to handle recurring business-operations tasks: each task runs through a fixed seven-step sequence — load user context, propose an approach, assess fit, classify the task, execute, evaluate the result, and log it — and is classified by novelty, stakes, and reversibility, so low-risk tasks are executed automatically and high-risk ones are escalated for the user's approval (escalation thresholds adjust to the user's 1–5 ratings of past output). Context persists across sessions through an external memory service scoped per business and local log files. The framework includes a library of task modules for operations such as weekly review, market scanning, knowledge-gap analysis, research, and CRM/membership work. It is single-user today; the task sequence and memory writes are enforced by instruction to the AI rather than by code, and the dashboard and several memory layers are prototype-stage.

---

## 2. The Problem & The Operator Persona

**The problem.** A founder running several businesses at once *is* the bottleneck. Context lives in their head, decisions queue behind them, and the cost of staying coordinated across ventures grows faster than the value created. Most "AI assistant" products make this worse — they require the human to be present, re-explain context every session, and review everything the assistant does.

**The operator persona.** Centaurion is built for and around one operator (Malik Palamar) running three ventures:

| Venture | Operator Role | Focus |
|---|---|---|
| **AOB (Art of Breath)** | Head of IT & Applied Intelligence | Breathwork education; CRM migration (Ontraport → GoHighLevel); facilitator certification; membership ops |
| **BuilderBee** | Fractional CEO | AI-automation consultancy; GoHighLevel implementations; client delivery |
| **Centaurion.me** | Founder | The framework itself — methodology, thought leadership, advisory |

Operator characteristics (from `identity/PREFERENCES.md`): first-principles thinker, visual-spatial, metaphor-driven, **reviews work from a phone** (Telegram, GitHub mobile, Claude app), prefers concise structured output over prose, batches direction in focused sessions rather than reacting in real time, and gives **1–5 ratings instead of written reviews**.

The product is operator-specific today, but the architecture is generic: the `skills/onboarding/` flow exists to calibrate *any* new operator who clones the repo. This is the seam where Centaurion becomes a product for more than one person.

---

## 3. Core Concept: The Exo-Cortex & the Active Inference Loop

Centaurion frames the human and the AI as two halves of a single cognitive system — a "centaur." The human is the slow, high-judgment half; the AI is the fast, tireless half. The point of contention every other AI tool gets wrong: **the human is the prior, not the bottleneck.**

Every non-trivial task runs through a fixed seven-step loop (defined in `CLAUDE.md` and `framework/active-inference-loop.md`):

1. **SENSE** — Load context: operator identity (`identity/`), recent memory, active alerts, onboarding/calibration state.
2. **PREDICT** — State the intended approach, a confidence level (high/medium/low), and what could go wrong.
3. **COMPARE** — Identify prediction error: is this routine or novel? Does the model fit?
4. **ROUTE** — Apply the Routing Gate (see §4). Decide: act autonomously or escalate to the human.
5. **ACT** — Execute using the relevant skill(s) and tools.
6. **OBSERVE OUTCOME** — Compare result to prediction; assess whether routing was correct.
7. **REMEMBER** — Write the interaction to shared memory; update wikis; log the routing decision; capture any rating.

For a product team, the loop is effectively a **state machine with a mandatory human-escalation branch and a mandatory memory-write step.** Steps 4 and 7 are where the product's differentiation lives — and where most of the UX and observability surface area sits.

---

## 4. The Three Laws (and what they imply for product behavior)

The system is governed by three laws that are *always in effect* (`identity/MISSION.md`, `framework/three-laws.md`):

1. **Hierarchy Law — "The human is the prior, not the bottleneck."**
   Operator identity is loaded every session; the AI proposes and executes but never overrides. *Product implication:* identity/context loading must be automatic and invisible; the human's role is to set direction and rate outcomes, not to babysit.

2. **Routing Law — "Prediction errors are routed to the right substrate."**
   Tasks are classified by **novelty × stakes × reversibility**. The decision rule:
   ```
   IF novelty > 0.7 AND stakes > 0.5 AND reversibility < 0.3:
       → STOP. Surface to the human with task, scores, recommendation, risks.
   ELSE:
       → Proceed autonomously. Log the classification.
   ```
   Thresholds are *adaptive* — they tighten when autonomous work gets low ratings and loosen when escalations are consistently rated 5/5. *Product implication:* the escalation message is a first-class UX object (must be ≤5 lines, phone-readable), and the threshold-tuning loop needs to be visible and tunable.

3. **Coupling Law — "The exo-cortex maintains shared model state between human and AI."**
   Every interaction updates shared memory so the human and AI don't drift apart. *Product implication:* memory write is non-optional; the system "compounds" only if this never silently fails.

---

## 5. Architecture & Components

Centaurion's intelligence lives in markdown and JSON, by design — "any runtime that reads markdown can run Centaurion." The repo is organized into functional directories:

| Directory | Role | What's in it |
|---|---|---|
| `identity/` | **Who the operator is** (TELOS system) | `PURPOSE.md`, `MISSION.md`, `GOALS.md`, `PREFERENCES.md`, plus `BELIEFS`, `MODELS`, `HISTORY`, etc. `BASELINE-INTEGRAL.md` (operator calibration) is generated per-install and gitignored. |
| `framework/` | **How the system thinks** | Three Laws, Precision Ratio, Active Inference loop, Routing Gate, Five Sensing Layers, Markov Blanket, "11 levels." |
| `agents/` | **Who the agents are** | Personas: `Cortex.md`, `Nova.md`, `Daemon.md`. |
| `skills/` | **What the system can do** | Portable `SKILL.md` files (see §6). |
| `memory/` | **Where it remembers** | Pointers/config to the memory layers (`supermemory.json`, `graphiti.json`, `mempalace.json`, `wiki-repos.json`) and live `state/` files (routing log, ratings, onboarding state, weekly reviews). |
| `workflows/` | **What runs automatically** | Markdown specs for daily health, weekly gap analysis, feedback capture, client onboarding, AOB weekly ops. |

**Entry points.** `CLAUDE.md` is the execution schema for Claude Code (loads automatically). `AGENTS.md` is the equivalent for other runtimes (Codex, pi, OpenClaw, Agent Zero). Both encode the same Three Laws and the same loop.

**The agent personas** (metaphor-driven, per operator preference):

- **Cortex** — the reasoning agent ("prefrontal cortex"). Deep analysis, planning, execution. Runs on Claude Code. This is the agent a session usually *is*.
- **Nova** — the sensing agent ("afferent nervous system"). Environmental scanning and signal detection; surfaces only what matters; tags everything by venture. Intended runtime: OpenClaw + Telegram on a VPS.
- **Daemon** — the identity-root agent ("the Greek daimon" / Markov-blanket boundary). Maintains coherence across agents, guards the identity, exposes a personal API (MCP). Partly aspirational (see §9).

**The skill system.** Each skill is a self-contained `SKILL.md` with YAML frontmatter (`name`, `description`, and "USE WHEN" trigger guidance). Skills are runtime-agnostic instruction sets, not code. Richer skills (e.g. `building-an-exo`, `integral-baseline`, `onboarding`) ship with `references/`, `templates/`, and `schema.json` alongside the `SKILL.md`. There is also a `.claude/skills/` mirror for Claude Code's native skill discovery.

---

## 6. Current Capabilities (installed skills)

| Skill | What it does |
|---|---|
| `centaurion-core` | Foundational skill — loads identity, Three Laws, and the Active Inference loop at session start ("L0 sensing"). |
| `routing-gate` | Classifies a task on novelty/stakes/reversibility and decides autonomous-vs-escalate. Operationalizes the Routing Law. |
| `onboarding` | First-run flow for a new operator: detects first install, runs the integral baseline assessment, writes `BASELINE-INTEGRAL.md`, schedules a 90-day refresh, marks onboarding complete (idempotent). |
| `integral-baseline` | AQAL + Integral Life Practice assessment of the operator (Light = 25Q / Deep = 75Q) to calibrate routing confidence, automation bias, and tone to the actual person. |
| `weekly-review` | "L2 sensing" — structured weekly comparison of outcomes vs. predictions; trends in ratings, routing accuracy, knowledge growth, cross-venture patterns. |
| `sa-scan` | Daily situational-awareness scan across 18 tracked stock tickers; detects threshold breaches and sector patterns. |
| `gap-analysis` | "L4 sensing" — knowledge-topology / gap analysis across the wiki repos (InfraNodus). "What are we missing?" |
| `autoresearch` | Autonomous overnight research iteration — define a metric/question, the agent iterates off-hours, operator reviews in the morning. |
| `aob-ops` | AOB operations — CRM hygiene, membership ops, facilitator coordination. |
| `builderbee-delivery` | BuilderBee client delivery — GoHighLevel setup, client onboarding, automation building. |
| `building-an-exo` | A large, citation-heavy methodology skill applying ExO 3.0 / the Intelligence Stack / the REWRITE playbook to redesign a firm around AI. Ships with extensive `references/` and `templates/`. (This is reference IP encoded as a skill, not Centaurion-operational tooling.) |

---

## 7. Integrations & Surfaces

**Runtime / harness.** Centaurion runs inside an agentic harness. The primary one is **Claude Code** (driven from a phone via the Claude app, or desktop). The same instruction set is portable to other runtimes via `AGENTS.md`.

**Review surfaces (phone-first).** The operator reviews from a phone: Telegram, GitHub mobile (Issues are a deliberate review surface), and the Claude app. There is also a **React + TypeScript dashboard** (`frontend/`) backed by a **FastAPI** service (`backend/`) — currently a separate, partly mock-data web UI rather than the primary surface.

**MCP integrations.** The repo declares an MCP connection to **Supermemory** (`.mcp.json`, `https://mcp.supermemory.ai/mcp`). The broader environment also exposes many other MCP servers (GitHub, and a long list of third-party tools), but the only one the repo itself configures is Supermemory.

**Memory stack** (`README.md`, `memory/`):
- **Layer 1 — Supermemory:** real-time shared bus, ambient capture + recall, scoped by venture "containers" (`centaurion-aob`, `-builderbee`, `-framework`, `-malik`). Free tier; round-trip verified; first live capture logged 2026-04-19.
- **Layer 2 — LLM Wikis** (per-venture repos), **InfraNodus** (knowledge topology), **Graphiti/Neo4j** (temporal graph of how facts change).
- **Layer 3 — MemPalace:** verbatim archive of raw conversation exports.

**Automation.** GitHub Actions workflows exist (`.github/workflows/ci.yml`, `daily-dev-loop.yml`), plus deploy scripts for VPS-hosted loops (`deploy/vps1`, `deploy/vps2`) covering autoresearch, weekly review, health checks, and a routing watchdog.

---

## 8. Key Product Principles

- **Precision Ratio** (`Precision = Predictive Order / Thermodynamic Cost`). Every feature should either improve predictions (numerator) or reduce cost in time/money/attention (denominator). If it does neither, question it.
- **Human-as-prior.** The AI never overrides; it proposes, executes, and learns under the operator's calibration.
- **Concise, structured, phone-readable output.** Three bullets beat three paragraphs; tables and headers over prose; surface tradeoffs rather than presenting one option as obvious.
- **Compounding memory.** Every interaction must leave the system smarter; the memory write is mandatory.
- **Markdown over code.** Intelligence lives in prompts and instruction files so any markdown-reading runtime can run it. (This is a strength for portability and a constraint for enforceability — see §9.)
- **Adaptive routing.** Escalation thresholds learn from outcome ratings.

---

## 9. Current State vs. Gaps (honest assessment)

**What is real and working:**
- The instruction layer (`CLAUDE.md`, `AGENTS.md`, `framework/`, `identity/`, `agents/`) is complete and coherent.
- The skill library exists and is well-specified.
- Supermemory is connected and round-trip-verified.
- State files exist and are being written (`routing-log.jsonl`, `ratings.jsonl`, weekly reviews for 2026-W16/W17).
- The onboarding + integral-baseline calibration flow is built and idempotent.

**What is prototype-level or aspirational (gaps):**
- **Enforcement is by convention, not code.** The loop, the Routing Gate math, and the mandatory memory-write are *instructions to an LLM*, not guaranteed code paths. Nothing structurally prevents a step from being skipped. This is the single biggest reliability gap.
- **Routing/ratings are append-only JSONL files.** There is no queryable store, no dashboard over them, and threshold auto-tuning is described but not demonstrably automated.
- **Daemon (the coherence/identity-root agent and personal MCP API) is largely future-state.** Graphiti/Neo4j and MemPalace are referenced as Month-2 layers; only Supermemory is live.
- **Nova** depends on external VPS + Telegram infrastructure that lives outside this repo.
- **The web dashboard is partly mock data** and disconnected from the markdown/agent core — there's no single integrated surface that shows the loop, the routing log, and memory together.
- **Single-operator today.** The onboarding flow anticipates multi-operator, but identity, ventures, and tickers are hard-coded to one person.
- **Some "skills" are reference IP** (notably `building-an-exo`) rather than operational tooling, which can blur "what the product does" vs. "what it knows."

---

## 10. Suggested Product-Development Asks for roxx.ai

Concrete areas where external product work would compound, ordered roughly by leverage:

1. **Make the loop enforceable, not advisory.** A thin orchestration layer (or harness middleware) that *guarantees* the SENSE→…→REMEMBER steps run — especially the Routing Gate evaluation and the memory write — with structured logging at each step. This converts "the model should" into "the system does."

2. **Routing & feedback observability.** A real datastore + dashboard over `routing-log.jsonl` and `ratings.jsonl`: routing accuracy over time, rating trends, escalation volume, and a UI to view/adjust the adaptive thresholds. This is the proof-of-value surface (the Precision Ratio made visible).

3. **Mobile review surface.** A purpose-built, phone-first review experience for the escalation queue and morning batch review — approve/reject/rate in one or two taps, replacing the current GitHub-Issues/Telegram improvisation. Optimize for the ≤5-line escalation card.

4. **Multi-venture dashboard.** A single pane showing per-venture state (AOB / BuilderBee / Centaurion), recent agent work, alerts, and cross-venture connections (the operator explicitly values cross-venture insight as highest-value).

5. **Unified memory & observability layer.** Reconcile the memory stack (Supermemory live; Graphiti/MemPalace planned) behind one interface, with health/coherence checks — effectively building out the "Daemon" coherence role as actual software.

6. **Onboarding UX for new operators.** Productize `skills/onboarding/` + `integral-baseline` into a guided first-run experience that calibrates a *new* operator's identity, ventures, and routing thresholds — the path from single-user system to product.

7. **Skill packaging / marketplace.** A clean format, validator, and install/share mechanism for skills (the `SKILL.md` + `references/` + `templates/` + `schema.json` pattern already gestures at this), so capabilities can be authored, versioned, and distributed.

8. **Integrate or retire the web stack.** Decide whether the existing `frontend/`+`backend/` becomes the real surface (wired to live data) or is replaced; today it's a parallel artifact with mock data.

---

### Open items flagged as assumptions (could not be fully verified from the repo)

- **roxx.ai** does not appear anywhere in the repository; this document is written *for* them, not *about* an existing relationship.
- The **only repo-configured MCP integration is Supermemory.** GitHub and the many other MCP tools available in the operating environment are not declared in `.mcp.json`, so their role in Centaurion proper is inferred, not confirmed.
- **Nova/Daemon runtimes, Graphiti/Neo4j, MemPalace, and InfraNodus** are described in docs/config but their live operational status is not verifiable from repo contents alone — treat as planned/partial.
- The **dashboard's data source** is mock data in the files reviewed; degree of any live wiring is unconfirmed.
- Specific external infra (VPS IPs, Telegram bot, wiki repos under `MalikJPalamar/*`) is referenced but lives outside this repository.
