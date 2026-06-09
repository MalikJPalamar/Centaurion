# Centaurion — Product Description for roxx.ai

> Prepared for **roxx.ai** as a product-development partner. This document describes what Centaurion is today, the model it runs on, its current architecture and capabilities, and where external product work would add the most leverage. It is grounded in the actual repository contents, not aspiration; where something is planned-but-not-built, it is flagged as such.

---

## 1. Executive Summary

Centaurion is an **exo-cortex** — a composite human-AI operating system designed to let a single founder run multiple ventures with less cognitive load, not more. It pairs a human operator (who supplies values, taste, and strategic direction) with a set of AI agents (who supply analysis, memory, and tireless execution). The product is currently implemented as a **markdown-and-JSON instruction layer that runs inside an agentic harness** (primarily Claude Code, with portability to other agent runtimes). Every task is executed through a seven-step "active inference" loop and gated by a routing rule that decides whether the AI proceeds autonomously or surfaces the decision to the human. The organizing first principle is the **Precision Ratio** — get better at predicting what the operator needs while spending less time, money, and attention doing it.

---

## 2. The Problem & The Operator Persona

**The problem:** A founder running several businesses at once is the bottleneck. Context lives in their head, decisions queue behind them, and the cost of staying coordinated across ventures grows faster than the value created. Most "AI assistant" products make this worse — they require the human to be present, re-explain context every session, and review everything.

**The operator persona (the design target):** A founder operating three ventures simultaneously — in the reference instance: AOB (breathwork education / CRM + membership ops), BuilderBee (an AI-automation consultancy on GoHighLevel), and Centaurion.me (the framework itself, as thought leadership). Key behavioral facts that drive the product:

- **Reviews from a phone.** Output must be scannable on a small screen. GitHub Issues and chat/Telegram are the primary review surfaces, not a desktop dashboard.
- **Thinks in systems and metaphors.** First-principles, visual-spatial, prefers tradeoffs over single recommendations.
- **Batches direction, expects async execution.** Sets priorities in a focused morning session; agents work in the background; the operator rates outputs rather than writing reviews.

Centaurion is built so this operator can act as the *prior* (the calibrating intelligence) without being the *throughput limit*.

---

## 3. Core Concept: The Exo-Cortex & The Active Inference Loop

Centaurion frames the human + AI pair as a single cognitive system ("a centaur"). It borrows vocabulary from the Free Energy Principle / active inference, but for a product team the important part is the **execution loop every task runs through**:

| Step | What happens | Product implication |
|------|--------------|---------------------|
| **1. SENSE** | Load context: operator identity, recent memory, active alerts, the request itself | The system always starts grounded in who the operator is and what's in progress |
| **2. PREDICT** | State the intended approach and a confidence level | Outputs are transparent about certainty |
| **3. COMPARE** | Identify prediction error — is this routine or novel? | Drives the routing decision |
| **4. ROUTE** | Apply the Routing Gate (see below) — proceed autonomously or escalate | The core safety/trust mechanism |
| **5. ACT** | Execute using skills and tools | The work product |
| **6. OBSERVE** | Did the outcome match the prediction? Was routing correct? | Generates the learning signal |
| **7. REMEMBER** | Write to shared memory; log the routing decision; capture ratings | Makes the system compound over time |

The loop is **continuous, multi-agent, and async-friendly**: routine tasks can run steps 1–5 unattended, and the human's input is only structurally required at step 4 for genuinely novel/high-stakes work.

---

## 4. The Three Laws (and what they imply for UX)

Centaurion's behavior is constrained by three "laws" that are always in effect. Each one has a direct product consequence:

1. **Hierarchy Law — "The human is the prior, not the bottleneck."** The operator's identity loads every session; the AI proposes and executes but never overrides high-stakes judgment. *UX implication:* identity/context must be cheap to load and always present; if the operator feels like an approval queue, that's a product failure (a routing mis-tune), not a human failure.

2. **Routing Law — "Prediction errors are routed to the right substrate."** Every task is classified before execution. *UX implication:* the product needs a clear, low-friction escalation surface and a visible classification, so the operator trusts that the right things — and only the right things — reach them.

3. **Coupling Law — "The exo-cortex maintains shared model state between human and AI."** All agents read/write the same memory. *UX implication:* memory must be observable and correctable; "I already told you that" is the canonical failure to design against.

---

## 5. Architecture & Components

Centaurion is deliberately **all markdown + JSON, with no compiled hooks** — the intelligence lives in prompts so any agent runtime that can read files can run it. The repository is the product.

| Directory | What it is | Role |
|-----------|-----------|------|
| `identity/` | The operator's "TELOS" profile — PURPOSE, MISSION, GOALS, PREFERENCES, plus deeper files (BELIEFS, HISTORY, MODELS, etc.) and an optional `BASELINE-INTEGRAL.md` calibration file | The prior. Loaded at SENSE on every session |
| `framework/` | The reasoning rules — Three Laws, Precision Ratio, the Active Inference loop, the Routing Gate (with explicit 0–1 novelty/stakes/reversibility scoring), and supporting models (Markov Blanket, sensing layers) | How the system thinks |
| `agents/` | Agent personas (see below) | Who is acting |
| `skills/` | Portable `SKILL.md` capability files | What the system can do |
| `memory/` | JSON pointers/config for the memory stack (Supermemory, wiki repos, Graphiti, MemPalace) plus `memory/state/` runtime files (routing log, ratings, health/onboarding state) | Where it remembers |
| `workflows/` | Recurring automations described as markdown specs (daily health check, weekly review, gap analysis, feedback capture) | What runs on a schedule |

**Agent personas** (currently personality definitions, not separately deployed services):
- **Cortex** — the reasoning agent (prefrontal cortex). Runs the full loop; classifies, routes, executes. This is the default persona in Claude Code.
- **Nova** — the sensing agent (afferent nervous system). Environmental scanning, signal detection, filtering noise; intended to run on a lightweight always-on runtime with Telegram.
- **Daemon** — the identity-root agent (the Markov-blanket boundary). Maintains coherence across agents and is intended to expose a personal MCP API.

**The skill system:** Each skill is a self-contained `SKILL.md` with a name, a "USE WHEN" trigger, and a procedure. This is the primary extension point — adding a capability means adding a markdown file, and skills are portable across runtimes (Claude Code, and via `AGENTS.md`, other agents like Codex/pi/OpenClaw/Agent Zero).

There is also an **existing web surface** (`frontend/` React + TypeScript, `backend/` FastAPI) deployed via Docker/Render, currently a thin dashboard shell over the system rather than the primary interaction surface.

---

## 6. Current Capabilities (Installed Skills)

| Skill | What it does |
|-------|--------------|
| `centaurion-core` | Loads identity, the Three Laws, and the loop at session start |
| `routing-gate` | Classifies a task on novelty/stakes/reversibility and decides autonomous-vs-escalate |
| `onboarding` | First-run, idempotent setup flow; delivers an integral baseline assessment, writes `identity/BASELINE-INTEGRAL.md`, and marks onboarding complete |
| `integral-baseline` | AQAL + Integral Life Practice assessment (Light 25Q / Deep 75Q) to calibrate the operator model |
| `weekly-review` | L2 structured weekly comparison of outcomes vs. predictions; phone-readable summary |
| `gap-analysis` | Knowledge-topology gap analysis over the wiki repos (intended to use InfraNodus) |
| `sa-scan` | Daily "situational awareness" scan over a tracked set of stock tickers |
| `autoresearch` | Autonomous overnight research iteration on a defined question/metric |
| `aob-ops` | Venture skill: AOB CRM/membership/facilitator operations |
| `builderbee-delivery` | Venture skill: BuilderBee client delivery / GoHighLevel setup |
| `building-an-exo` | A substantial methodology skill (ExO 3.0 / Intelligence Stack / "REWRITE" playbook) for redesigning a firm around AI |

**Scheduled workflows** (markdown specs): a daily health check that opens a GitHub Issue for phone review, a weekly review, a weekly gap analysis, client/venture ops workflows, and a feedback-capture loop that backfills ratings into routing accuracy.

---

## 7. Integrations & Surfaces

- **Runtime:** Runs inside an agentic harness. Primary: Claude Code (`CLAUDE.md` auto-loads the schema). Portable to other runtimes via `AGENTS.md` (Codex, pi, OpenClaw, Agent Zero).
- **Review surfaces:** Phone-first — chat app, Telegram (for the Nova sensing agent), and GitHub Issues (the daily health check is delivered as an issue). No dependency on a desktop.
- **Memory / MCP:** `Supermemory` is wired as an MCP server (`.mcp.json`) and is the real-time shared memory bus, with venture-scoped containers (aob / builderbee / centaurion / personal) and auto-capture/auto-recall. The broader memory architecture also references **wiki repos** (synced peer-to-peer via Syncthing), **InfraNodus** for topology, **Graphiti/Neo4j** for a temporal graph, and **MemPalace** for verbatim archive.
- **State:** Append-only JSONL files (`routing-log.jsonl`, `ratings.jsonl`) plus JSON status files for health/onboarding/autoresearch.
- **Automation cadence:** A "dev loop" runs the system against itself on a schedule (reported as 3×/day on a VPS), exercising the loop and self-verification tests.

A large catalog of additional MCP integrations is available to the harness (CRM/GoHighLevel, GitHub, calendar/email, analytics, design/video tooling, etc.), which is what lets the venture skills actually touch live systems.

---

## 8. Key Product Principles

- **Precision Ratio = predictive order ÷ thermodynamic cost.** Every feature should either improve predictions or reduce cost (time, money, cognitive load). If it does neither, it shouldn't ship.
- **Human-as-prior.** Calibrate to the specific operator; defer on high-stakes/irreversible decisions; never make the human an approval queue for routine work.
- **Compounding memory.** Every interaction must leave the system smarter — the REMEMBER step is mandatory, not optional.
- **Concise, structured, phone-readable.** Tables and three-bullet summaries over prose. Surface tradeoffs rather than a single "obvious" answer.
- **Portability over lock-in.** Markdown skills and instructions so the system isn't tied to one runtime.

---

## 9. Current State vs. Gaps

**What is real today:**
- The full reasoning schema (loop, Three Laws, routing gate with concrete scoring) is written and loads automatically in Claude Code.
- A working set of skills and workflow specs, plus self-verification tests.
- Supermemory MCP connected with live capture; routing/ratings state files defined; an onboarding/calibration flow.
- An existing (thin) web dashboard and a deployment path.

**What is prototype-level or aspirational (honest gaps):**
- **The "product" is currently a prompt/instruction layer, not an application.** Behavior depends on the agent faithfully following markdown; there is no enforcement engine, no typed schema for skills, and no runtime that guarantees the loop executes.
- **Memory is partly pointers.** Supermemory is live, but wiki repos, Graphiti/Neo4j, InfraNodus, and MemPalace are mostly planned/config-only. There is no unified observability over what the system "knows."
- **Routing learning is manual/file-based.** Thresholds are described as adjustable from ratings, but the feedback loop is JSONL append + human interpretation, not an automated tuning system.
- **Multi-agent is mostly personas, not deployed services.** Nova and Daemon are well-specified but not running as independent, coordinated processes; the Daemon MCP API is conceptual.
- **The web dashboard is minimal** relative to the richness of the underlying model — it does not yet visualize routing, memory, ratings trends, or multi-venture status.
- **No real onboarding/review UI.** Today everything is text-in-a-harness; non-technical operators cannot easily install, calibrate, or review.

---

## 10. Suggested Product-Development Asks for roxx.ai

These are derived from the gaps above and ranked by leverage on the Precision Ratio:

1. **Mobile review surface.** A phone-first inbox where the operator sees what the system did, what it's escalating (with the novelty/stakes/reversibility classification visible), and can rate outputs 1–5 in one tap. This is the single highest-leverage surface — it operationalizes the Hierarchy and Routing Laws.
2. **Onboarding & calibration UX.** Turn the `onboarding` + `integral-baseline` skills into a guided, non-technical flow that produces the operator profile and sets initial routing thresholds — so Centaurion can be adopted by founders who don't live in a terminal.
3. **Memory & observability layer.** A real, queryable, *correctable* view of shared memory (Supermemory + wikis + temporal graph) with a way to fix stale/wrong facts. Directly addresses the Coupling Law and the "I already told you that" failure.
4. **Routing engine + auto-tuning.** Promote the routing gate from a markdown rule + JSONL log into an instrumented service that records classifications, ties them to ratings, and adjusts thresholds with the human in the loop. Make routing accuracy a first-class, charted metric.
5. **Multi-venture dashboard.** A single view across ventures (AOB / BuilderBee / Centaurion-style tagging) showing status, alerts, ratings trends, and cross-venture connections — the "highest-value insights" the framework explicitly wants surfaced.
6. **Skill framework / marketplace.** Formalize the `SKILL.md` contract (schema, triggers, versioning, tests) and build a way to author, validate, share, and install skills — turning the extension model into a real platform surface.
7. **Agent orchestration.** Stand up Nova and Daemon as actual coordinated services (sensing + coherence/identity API) rather than personas, with the Daemon MCP boundary as the integration point for external systems.

---

## Appendix: Source Files (for grounding)

- Execution schema: `CLAUDE.md`, `AGENTS.md`
- Identity: `identity/` (PURPOSE, MISSION, GOALS, PREFERENCES, BELIEFS, HISTORY, MODELS, …)
- Framework: `framework/` (three-laws, precision-ratio, routing-gate, active-inference-loop, sensing layers, markov-blanket)
- Agents: `agents/` (Cortex, Nova, Daemon)
- Skills: `skills/*/SKILL.md`
- Memory: `memory/*.json`, `memory/state/*`
- Workflows: `workflows/*.md`
- Web surface: `frontend/`, `backend/`, `render.yaml`, `Dockerfile`
- State/planning: `.planning/STATE.md`, `docs/architecture.md`
