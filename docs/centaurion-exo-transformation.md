# Centaurion — ExO 3.0 Transformation Plan

> **Framework:** Building an ExO skill (ExO 3.0 / Intelligence Stack / REWRITE Playbook), *The Organizational Singularity* (OS Outline v20), Salim Ismail with contributors; AI adaptation by Kent Langley for OpenExO. Source: https://openexo.com/organizational-singularity
> **Venture:** Centaurion (Centaurion.me) — a personal AI agent product (an AI agent cryptographically bound to a single user that models the user, persists their memory, and executes risk-classified tasks).
> **Prepared by:** Cortex for Malik. Tag: `centaurion`.
> **Status:** Draft for review. Inputs flagged ASSUMPTION must be confirmed before action. This is a *recursive* application — Centaurion's product literally attempts to be an Intelligence Stack, so the framework is graded against the firm, not the product vision.

---

## 0. The three-part frame
1. **Destination — ExO 3.0:** Centaurion rebuilt around AI as MTP + DRIVE(5) + SHAPE(5).
2. **Operating System — the Intelligence Stack:** build the operating core first. *Centaurion is unusual: the firm's product IS a six-layer cognitive loop. The gap is not the Stack's existence — it is GOVERN/ASSURE.*
3. **Playbook — REWRITE:** six steps, sequence non-negotiable.

Crossing rule: **DRIVE without SHAPE crashes; SHAPE without DRIVE stalls.** (Centaurion's tilt is the *crash* side — see §5.)

---

## 1. Grounded facts vs. assumptions

### Grounded
- Product = a personal AI agent bound to one user; maintains a model of the user (developmental, behavioral, biological parameters), a persistent memory of everything the user encounters, and a risk-classification task engine (the Routing Gate: novelty × stakes × reversibility → auto-execute or escalate).
- Implemented as a markdown/JSON instruction layer on the Claude Code harness (portable via `AGENTS.md`) plus a prototype React/FastAPI dashboard.
- **Pre-launch:** dogfooded by Malik only; no external users; the memory stack (Graphiti/MemPalace) is unproven; Supermemory is the only live memory layer. *(memory: centaurion pre-launch status)*
- **Enforcement is by convention, not code** — the loop, the Routing Gate math, and the mandatory memory-write are instructions to an LLM, not guaranteed code paths.
- A **revenue-agent mandate** exists: Cortex authorized as an autonomous revenue agent with a ~$1K budget cap, $10K MRR target, operating its own external accounts. *(memory: revenue-bot mandate)*
- Team = **Malik solo** + AI agents (Cortex active; Nova/Daemon largely aspirational).
- Single model family today (Anthropic/Claude via Claude Code).

### Assumptions (CONFIRM before acting)
- **A1 — Headcount = 1** (Malik). → Direct Mode, Tier 1–2.
- **A2 — Revenue ≈ $0 / pre-launch.** Target $10K MRR. Banding Tier 1–2.
- **A3 — Business model = per-user subscription** for a person-bound agent (not seat-based enterprise). Unconfirmed.
- **A4 — No formal Agent Specification, Permission Envelope, eval suite, or tested kill switch exists for the autonomous revenue agent.** Treated as baseline: GOVERN/ASSURE not operational as code.
- **A5 — Single model family / single harness dependency** (Anthropic + Claude Code). Cognitive-captivity risk open.
- **A6 — The cryptographic per-user binding is a product *intention*, not yet implemented** (no PKI / key material today).

> Confirm A1/A2 before the mode + tier call is final; confirm A4 before any DRIVE score is treated as more than directional.

---

## 2. Draft MTP — three-layer protocol

**Candidate MTP:** *"Everyone augmented by an intelligence that is truly their own."* (Working line; the protocol below is load-bearing.)

### Constraint Layer (categorically forbidden)
- Never expose, leak, or cross-train one user's model or memory to another user. **The one-to-one binding is the product; violating it destroys it.**
- Never take an irreversible action (money movement, external account changes, public posts) without an explicit Permission-Envelope check and human approval.
- Never represent the agent's output as professional medical, legal, or financial advice — *especially* relevant because the product ingests biological/nervous-system parameters.
- Never persist or transmit sensitive user data outside the user's own encrypted store.

### Decision Layer (weighted priorities)
- **User sovereignty & binding integrity > capability > growth.** A narrower, private, trustworthy agent beats a broader leaky one.
- **Trust/compounding (long-run) > delegation breadth (short-run).**
- **Provable governance > speed of feature shipping** (the inverse of the current default).

### Identity Layer
- Centaurion is a *personal* intelligence — the binding force is the exclusive one-to-one relationship between agent and user, not a shared platform. The company exists to make that relationship trustworthy enough to hand real life and work to.

### Litmus tests
1. *Could an agent, given only this MTP, make a decision leadership would endorse?* — Yes for the refusal cases (decline a cross-user data request; refuse an unapproved money move). **Provisional pass pending Malik signing the Constraint Layer.**
2. *Could it decide what NOT to build?* — Yes: it refuses any feature that weakens per-user isolation or ships an autonomous money-handling path before the control plane exists. **Pass on signing.**

---

## 3. Direct Mode vs. Edge Mode

**Determination: DIRECT MODE, Tier 1–2** (A1: headcount = 1). Apply REWRITE to the whole company in place; no separate Edge Twin entity.

- **Existence proof is exact, not analogical:** Steinberger built OpenClaw solo on a Friday evening (Nov 2025), ran 4–10 agents in parallel, 6,600+ commits in Jan 2026, 145k+ stars, Meta/OpenAI bids — no team, no revenue. Solo-founded startups = 36.3% of new ventures (early 2026). Centaurion *is* the modal new company.
- Even in Direct Mode, Centaurion must adopt the **Edge Twin data-governance discipline** internally — and uniquely so, because the product itself is a data-governance promise (per-user isolation, no fork, encrypted store). The discipline is not a metaphor here; it is the spec.

---

## 4. DRIVE — the Intelligence Engine (1–5 each, /25)

> GOVERN-cap rule applied: with GOVERN/ASSURE not operational as code (A4), DRIVE is **capped at 13/25**.

| Component | Score | Reasoning (grounded) |
|---|---|---|
| **D — Decision Architecture** | **3** | Genuinely above-average for a solo firm: the Routing Gate *is* a two-way/one-way-door model (novelty × stakes × reversibility). But it is enforced by convention, and firm-level decisions still funnel to Malik. |
| **R — Recursive Learning** | **2** | Weekly reviews, routing log, and 1–5 ratings exist and feed threshold tuning *by design*; auto-propagation is not demonstrably automated and compounding is unproven (6-month-old system). |
| **I — Intelligence Stack** | **1** | The Stack is *articulated* (the active-inference loop maps to the six layers) but GOVERN/ASSURE is convention, not code. **Capped at the lowest Four Pillar = 1.** |
| **V — Value Moat** | **3** | Strong moat *sources*: proprietary per-user data + intelligence density + a real switching cost (a deeply calibrated personal agent is irreplaceable once it knows you). Discounted because pre-launch, unproven, and single-model (A5). |
| **E — Elastic Agency** | **3** | Structurally strong: the firm runs on composable Claude Code sub-agents + MCP tools; Malik recomposes agency fluidly. No formal Capability Registry / graduated-authority logic. |
| **Raw total** | **12/25** | |
| **GOVERN status** | **Convention-only** | **Cap 13/25. Effective DRIVE = 12/25.** |

### Four Pillars sub-rubric (inside I; I = minimum)
| Pillar | Score | Note |
|---|---|---|
| Trusted Evals | 1 | No eval suite on the agent's own outputs; 1–5 ratings are coarse and human-gated. |
| Searchable Logs w/ Correlation IDs | 2 | `routing-log.jsonl` exists but is not correlation-ID structured across a task's full chain. |
| Granular Rollback | 1 | No agent/prompt/model rollback; memory writes are append-only. |
| Human Review Queue | 2 | Malik is the de-facto queue via Routing-Gate escalations; informal, no SLA. |
| **Four Pillars Maturity (min)** | **1** | No new agent class — **especially the autonomous revenue agent** — deploys until every pillar ≥ 3. |

**DRIVE headline: 12/25.** Binding constraint **I = 1** (GOVERN/ASSURE as code). Build this first.

---

## 5. SHAPE — the Organizational Form (1–5 each, /25)

| Component | Score | Reasoning (grounded) |
|---|---|---|
| **S — Safe Autonomy** | **1** | No Fiduciary Wedge, Permission Envelope, or tested kill switch for the autonomous revenue agent that has a budget and its own external accounts (A4). **This is a live agent operating with real money under convention-only control — the canonical PocketOS exposure.** |
| **H — Human Architecture** | **3** | Solo: no Middle-60% problem yet, but also no junior loop and no team to develop. Scored 3 (clean but thin); honest absorption math is trivial today and must be revisited at first hire. |
| **A — Adaptive Architecture** | **4** | Real strength: markdown-over-code makes every layer swappable/retargetable; `AGENTS.md` portability is genuine modularity. Held below 5 only because the portability claim is unproven on a second runtime. |
| **P — Purpose Control** | **2** | Strong implicit purpose (PURPOSE/MISSION exist) but the MTP is not yet a signed three-layer protocol for the *venture* (only for Malik personally). §2 is the first draft. |
| **E — Ecosystem Trust** | **2** | Cryptographic identity/trust is the product's headline promise but is **vision-stage** (no PKI today, A6). No agent-to-agent trust infra. This is simultaneously the biggest gap *and* the biggest moat opportunity (trust-as-protocol). |
| **Total** | **12/25** | |
| **Middle-60% absorption modeled?** | **N/A (solo)** | Re-trigger at first hire. |

**SHAPE headline: 12/25.** Highest-leverage moves: **(1) Safe Autonomy — wrap the revenue agent in a Permission Envelope + tested kill switch + Four Pillars before it touches money (S); (2) sign the three-layer MTP (P).**

> **Combined read — the sharp finding:** DRIVE 12 / SHAPE 12, balanced on the *scores* — but the **tilt is toward CRASH, not stall.** Centaurion is the opposite of AOB. AOB has strong human/adaptive bones and no engine → *stall* risk. Centaurion has a designed intelligence engine and an **autonomous money-handling agent running under convention-only governance** → *crash* risk. The cure is identical in name (build GOVERN/ASSURE with the Fiduciary Wedge from day one) but **urgent**, not gradual: the revenue agent must not operate autonomously until Q5/Q6/Q7 of the diagnostic (§9) are off red.

---

## 6. REWRITE Playbook — six steps tailored to Centaurion

GOVERN/ASSURE runs across every step (alert-only → escalation authority → kill-switch capable).

### Step 1 — BACKCAST & DEFINE *(gate: Five Design Conditions)*
One-day founder workshop (Tier 1–2, Malik runs it). Output: signed Destination Architecture, the candidate-workflow pipeline ranked, a written mandate.

| # | Design Condition | At Centaurion | Holds? |
|---|---|---|---|
| 1 | AI-Centric Workflow Architecture | The firm's own ops (research, content, product dev, revenue) designed agent-first. | **Partial** — the loop exists; not all of Malik's work is decomposed. |
| 2 | Recursive Improvement Infrastructure | Routing log + ratings + weekly review propagate improvements at machine speed. | **Partial** — designed, not auto-propagating. |
| 3 | Model Sovereignty & Governed Autonomy | ≥2 model families; owned orchestration; Permission Envelopes + kill switch. | **No** (A5, A4) — single family, convention-only control. |
| 4 | Intelligence Density at Every Layer | Output per human rising as agents absorb work. | **Not yet measured.** |
| 5 | Human Flourishing as Binding Constraint | The product's entire thesis; for the firm, protects Malik's attention. | **Strong intent.** |

**Step 1 is NOT complete until conditions 2, 3, and 4 are credibly instantiated** — conditions 3 (model sovereignty + governed autonomy) is the load-bearing gap.

### Step 2 — ASSESS & PREPARE
Run the Readiness Score (§7); stand up MVIS in week one; choose on-ramp. **For Centaurion, MVIS = the GOVERN/ASSURE plane the product currently lacks** (correlation-ID logging, an eval suite on the agent's outputs, one rollback path, a named Human Review Queue + a *tested* kill switch).

### Step 3 — EXTRACT *(gate: Workflow Data Manifest)*
Elicitation-first. The most sensitive workflow is the **revenue agent** (handles money + external accounts + possibly user data). Produce a one-page Workflow Data Manifest for it (and for the dogfooding loop). Binary rule: if you cannot state why a workflow needs a field/credential/account, the agent does not get it.

### Step 4 — DIAGNOSE & STRIP
Run the Task Decomposition Matrix across Malik's own week (the highest-coordination "function" is the founder). Score each task 1–5 for Agent Readiness; disposition agent_now / pilot_step_5 / stay_human. CAIO = a hat Malik wears.

### Step 5 — BUILD & PROVE *(parallel run as shadow mode + four cold-start feeds)*
Decision Handover Waves: **start with the reversible, no-money workflows** (autoresearch, weekly-review, content), NOT the revenue agent. Parallel-run-then-deprecate, success criteria set first. Cold-start feeds: historical replay (past sessions), shadow comparison (agent rec vs. Malik action vs. outcome on a correlation ID), human-correction capture (override reason taxonomy), synthetic edge cases (cross-user leakage attempt, unapproved money move, contraindicated health claim). **Test of a real twin: the human-override rate falls over time.**

### Step 6 — REWIRE & EVOLVE
Pod = Malik + agents + a tested kill switch as standing rhythm. Sector ratios (information-centric: ~70% AI / ~20% Malik / ~10% elastic external). Make the **Continuous Kill Switch** routine; measure Organizational Half-Life.

---

## 7. Eight-Dimension Readiness Score (/80)

> Sector: information-centric. Mode: Direct (A1).

| # | Dimension | Score | Reasoning |
|---|---|---|---|
| 1 | Organizational Drag | **8** | Solo, zero bureaucracy. |
| 2 | AI Elevation | **9** | Maximal — the founder is building an AI-native firm whose product *is* AI; AI is at the center by definition. |
| 3 | Work Architecture | **5** | The loop is task-level, but not all of Malik's work is decomposed into specs. |
| 4 | Firm Boundary Design | **6** | Agents + MCP = an elastic, composable boundary; no formal Capability Registry. |
| 5 | Decision Autonomy | **4** | Routing Gate designed but convention-enforced; Malik is still the hub. |
| 6 | Network Structure | **4** | Solo; information hubs through Malik; no pods. |
| 7 | Reinvention Cadence | **5** | Actively building; no Continuous Kill Switch or Half-Life metric yet. |
| 8 | Tacit Knowledge Accessibility | **6** | Unusually high — the `identity/` TELOS files + integral baseline already externalize the founder's tacit operating logic. |
| | **Total** | **47/80** | |

**Band: FOUNDATIONAL (33–55), upper end.** Four Pillars Maturity min = 1/5 (below the ≥3 deploy threshold).

**Miura-Ko:** the product *aspires* to L4 (Compounding Operating System, where Value Moats form); **lived reality is L1–L2** (Personal Productivity / Team-of-one workflow, dogfooded by one user). Sharp divergence between a high Readiness Score and a low ladder level = **"bought the architecture, hasn't deployed it" — the most expensive failure mode in the framework.** Trust the ladder: treat Centaurion as **L1–L2**. The remedy is *deployment with real governance*, not more design.

**On-ramp: MVIS + 90-Day Sprint.** Lowest dimensions to work first: Decision Autonomy (4), Network Structure (4), Reinvention Cadence (5).

---

## 8. Smallest safe first workflow

**Recommended Wave 1: instrument and govern the existing reversible loop — autoresearch + weekly-review — with the Four Pillars at MVP level.** High volume, reversible, measurable, no money, no external user data, historical cases available. This proves the GOVERN/ASSURE plane and the falling-override-rate test on safe ground.

**Explicitly NOT first: the autonomous revenue agent.** It is high-stakes, money-handling, externally-facing, and partly irreversible — the worst possible first workflow under convention-only governance. It is **Wave 3**, gated on the diagnostic in §9 going green.

**Pre-set benchmarks:** task cycle time, override rate (must fall), eval pass-rate on agent outputs, % of tasks with a complete correlation-ID audit trail.

---

## 9. Edge-Twin Data-Governance discipline + CIO Diagnostic (applied to the autonomous revenue agent)

The revenue agent is Centaurion's "first governed agent on a live, high-stakes workflow." Apply the full discipline. **No data fork:** workflow-scoped, governed access to exactly the accounts/credentials that workflow needs; read/write separated; every action logged on a correlation ID; short-lived, revocable credentials. **Source-of-truth:** external systems of record (Stripe/bank/platform) win ties; the agent is the reasoning layer, never a second ledger.

### CIO Diagnostic (Appendix F) — red/amber/green
| # | Question | Score | Note |
|---|---|---|---|
| 1 | Allowed to do? (Autonomy Tier + Waves) | **Amber** | Define Tier = recommend_only for spend; execute_within_bounds only for non-destructive, sub-limit actions. Needs written spec. |
| 2 | Source of truth? | **Green** | External ledgers/platforms win (A: confirm). |
| 3 | Data needed & why? (Manifest + HIDO) | **Amber** | Manifest not yet written; credentials/accounts not yet scoped per workflow. |
| 4 | Trains on the data? | **Amber** | Pin no-train + retention/deletion in any model-vendor terms. |
| **5** | **Prevent leakage? (SHAPE)** | **RED** | No Permission Envelope / GOVERN plane catching OWASP failure modes (A4). **BLOCKS BUILD.** |
| **6** | **Identity handling? (SHAPE)** | **RED** | No scoped workload identity / short-lived creds / per-action correlation-ID logging; cryptographic binding is vision-stage (A6). **BLOCKS BUILD.** |
| **7** | **When it's wrong? (SHAPE)** | **RED** | No tested kill switch / rollback / exception queue with SLA. **BLOCKS BUILD.** |
| **8** | **Who is accountable? (SHAPE)** | **Amber** | Malik is the de-facto Fiduciary Wedge; name the roles in writing → Green. |
| 9 | Smallest safe first workflow? | **Green** | But this is NOT it — see §8. The revenue agent is Wave 3. |
| 10 | Measure success? (override rate falls) | **Amber** | Benchmarks listed; baseline before any parallel run. |

**Gate decision: BUILD BLOCKED for autonomous revenue operation.** Q5/Q6/Q7 red. **First build action: stand up the MVIS GOVERN/ASSURE plane + Permission Envelope + a tested kill switch.** This is the PocketOS lesson, and it is directly on the money mandate.

---

## 10. Cognitive captivity & other flags
- **Cognitive captivity (A5):** Centaurion is wholly dependent on one model family *and* one harness (Claude Code). Maintain inference across ≥2 model families and prove the `AGENTS.md` portability before the product is load-bearing for paying users.
- **Customer-side agent inversion:** a person-bound agent product will itself be evaluated by *other* agents; make the value proposition and API legible to buyer-side agents.
- **Silent Drift:** define named eval thresholds (accuracy floor + override-rate ceiling) for the agent's outputs before any external user, or drift surfaces as user complaints instead of dashboards.
- **Sensitive-data gravity:** because the product ingests biological/nervous-system + psychological data, the GOVERN bar is *higher* than a normal SaaS — privacy and binding integrity are existential, not compliance line-items.

---

## 11. Concrete next actions
1. **Confirm A1–A6** (headcount, revenue/stage, business model, current governance state, model sovereignty, crypto-binding status). 15 min; gates everything.
2. **Sign the three-layer MTP** (§2), especially the Constraint Layer (per-user isolation + no-unapproved-money-move are load-bearing).
3. **Freeze autonomous revenue operation** until the GOVERN plane exists. The $1K-budget agent may run in **recommend-only / shadow** mode now; no autonomous money moves.
4. **Stand up MVIS = the GOVERN/ASSURE plane** in week one: correlation-ID logging across a task chain, an eval suite on agent outputs, one rollback path, a named Human Review Queue + a **tested kill switch**. This is the action that moves CIO Q5/Q6/Q7 off red.
5. **Run Step 3 EXTRACT** on the revenue workflow + the dogfooding loop: write and sign the Workflow Data Manifest; scope credentials/accounts per workflow.
6. **Run Step 4 Task Decomposition Matrix** on Malik's own week; name Wave 1/2/3 (Wave 1 = autoresearch+weekly-review; Wave 3 = revenue agent).
7. **Address cognitive captivity:** stand up a second model family path and validate `AGENTS.md` portability.
8. **Re-score at T+90 days:** target lift from Foundational (47) toward Ready (56+) and from lived L1–L2 toward a deployed, governed L3.

---

## Headline Summary

| Item | Result |
|---|---|
| **MTP (working)** | "Everyone augmented by an intelligence that is truly their own" — Constraint/Decision/Identity protocol (§2). |
| **Mode** | **Direct Mode, Tier 1–2** (solo, pre-launch — ASSUMPTION A1/A2). |
| **DRIVE** | **12/25** (cap 13); binding constraint **I = 1** (GOVERN/ASSURE as code). |
| **SHAPE** | **12/25**; strengths A=4, D-arch real; gaps S=1, P=2, E=2. |
| **Combined tilt** | **CRASH-leaning** (autonomous money agent under convention-only governance) — the inverse of AOB's stall risk. |
| **Readiness** | **47/80 — Foundational (upper).** Lived **Miura-Ko L1–L2** vs. aspired L4 → "bought the architecture, hasn't deployed it." |
| **On-ramp** | **MVIS (= the GOVERN/ASSURE plane) + 90-Day Sprint.** |
| **First workflow** | **Instrument + govern autoresearch + weekly-review** (reversible, no money). Revenue agent = Wave 3. |
| **Gate** | **CIO Diagnostic BUILD BLOCKED** for autonomous revenue operation — Q5/Q6/Q7 red. Freeze money moves; build the control plane first. |

*Source: ExO 3.0 / The Organizational Singularity (OS Outline v20), Salim Ismail with contributors. Skill adaptation by Kent Langley for OpenExO — https://openexo.com/organizational-singularity*
