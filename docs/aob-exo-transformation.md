# AOB — ExO 3.0 Transformation Plan

> **Framework:** Building an ExO skill (ExO 3.0 / Intelligence Stack / REWRITE Playbook), encoding *The Organizational Singularity* (OS Outline v20, May 2026), Salim Ismail with contributors. Operational AI adaptation by Kent Langley for OpenExO. Source: https://openexo.com/organizational-singularity
> **Venture:** Art of Breath (AOB) — breathwork education via facilitator-led workshops, certification, and membership.
> **Prepared by:** Cortex (Centaurion exo-cortex) for Malik. Date: 2026-06-09. Tag: `aob`.
> **Status:** Draft for Malik's review. Several inputs are flagged ASSUMPTION and must be confirmed before this plan is acted on.

---

## 0. How to Read This (the three-part frame)

Every ExO 3.0 engagement is anchored on three things and nothing is allowed to crowd them out:

1. **Destination — ExO 3.0.** What AOB looks like rebuilt around AI: MTP + DRIVE (5) + SHAPE (5).
2. **Operating System — the Intelligence Stack.** The operating core (six cognitive layers + GOVERN/ASSURE). Build this first; the other nine characteristics are the context it runs in.
3. **Playbook — REWRITE.** The six-step migration, sequence non-negotiable. Skipping Step 1 is the fastest way to fail.

The crossing rule governs the whole plan: **DRIVE without SHAPE crashes; SHAPE without DRIVE stalls. You need both.**

---

## 1. Grounded Facts vs. Assumptions

### Grounded (from the repo)
- AOB delivers breathwork education through **facilitator-led workshops, a certification program, speaking/corporate contracts, and a membership community**. (`docs/aob-wiki/README.md`, `ventures.md`)
- **Lean team:** Malik (founder/strategy/partnerships), a pool of **certified facilitators** (delivery, semi-independent with playbooks), and **admin support** (scheduling, CRM, client comms). (`docs/aob-wiki/team.md`)
- **Growth lever = the certification pipeline.** More certified facilitators = more concurrent delivery without Malik. (`facilitator-certification.md`)
- **Tech stack:** GoHighLevel (CRM/email/funnels, *migrating in from Ontraport*), Stripe (payments), Zoom (delivery), Google Workspace (collab), Mighty Networks (community), Centaurion (automation/memory, building). (`tech-stack.md`, `aob-ops/SKILL.md`)
- **CRM migration Ontraport → GHL is mid-flight**; rollback plan = keep Ontraport 60 days, run parallel 30 days. (`crm-migration.md`)
- Routine ops are low novelty/low stakes; exceptions routed to Malik: facilitator disputes, bulk CRM changes >100 contacts, pricing/program-structure changes. (`aob-ops/SKILL.md`)

### Assumptions (CONFIRM with Malik before acting)
- **A1 — Headcount ≤ 50.** Repo describes a "lean team" with no number. Assumed well under 50 (likely <10 core + an elastic facilitator pool). *This sets Direct Mode and Tier 2.*
- **A2 — Revenue ≤ ~$2M.** No figure in repo. Assumed Tier 2 banding.
- **A3 — Facilitators are elastic/contract**, not salaried FTE (they "operate semi-independently"). This matters for the firm-boundary score and Elastic Agency.
- **A4 — No agent today has a written Agent Specification, Permission Envelope, or eval suite.** Centaurion is "building"; nothing in the repo shows a deployed, spec'd AOB agent. *Treated as the baseline: GOVERN/ASSURE is not yet operational.*
- **A5 — Source of truth after migration = GoHighLevel + Stripe** (GHL is the system of record for contacts/pipeline; Stripe for money). Used as the "ERP-wins" anchor.
- **A6 — No multi-model-family inference or owned orchestration/fine-tuning data yet** (cognitive-captivity risk open).

> Per the skill's output discipline, every assumption above is a verification gate. *Confirm A1 before the Direct/Edge determination is final; confirm A4 before any DRIVE score is treated as more than directional.*

---

## 2. Draft MTP (Massive Transformative Purpose) — as three-layer protocol

**Candidate MTP statement:** *"A breath away from anyone's best state."* (Working line — Malik owns the final wording; the protocol below is the load-bearing part, not the slogan.)

MTP is encoded as a **machine-readable protocol, not a poster.** Three layers:

### Constraint Layer — what agents are categorically forbidden from doing
- Never make or imply a **health/medical claim** about breathwork outcomes, or give advice to a contraindicated participant (pregnancy, cardiovascular, epilepsy, etc.). Safety copy is non-negotiable.
- Never alter **certification status, pricing, or program structure** autonomously (these are Malik-routed per `aob-ops`).
- Never contact a contact/lead outside consented channels; never exfiltrate the contact database.
- Never represent an **uncertified** person as a certified AOB facilitator.

### Decision Layer — weighted priorities under tradeoff
- **Brand/safety integrity > speed of response > volume.** A slower, on-brand, safe answer beats a fast generic one.
- **Facilitator quality (client-satisfaction-by-facilitator) > raw certification throughput.** Grow the pipeline, but never below the QA bar.
- **Retention of existing members/facilitators ≥ acquisition** when resources are scarce.

### Identity Layer — cultural cohesion that replaces "the office"
- AOB is a *community of practice*, not a content library. The binding force is the felt experience of the work and the facilitator fellowship. Agents exist to **protect facilitators' time for human connection**, not to replace the connection.

### Litmus tests (both must pass before sign-off)
1. *Could an agent, given only this MTP, make a decision leadership would endorse?* — Plausibly yes for triage/scheduling (e.g., decline to answer a medical question and route to a human). **Status: provisional pass, pending Malik's review of the Constraint Layer.**
2. *Could that agent decide what NOT to build/do?* — Yes: the Constraint + Decision layers let it refuse a medical-claim email, refuse an autonomous price change, refuse to over-enroll past QA capacity. **Status: pass once the Constraint Layer is signed.**

---

## 3. Direct Mode vs. Edge Mode

**Determination: DIRECT MODE.** (ASSUMPTION A1: headcount ≤ 50.)

- Rule: **≤50 employees → Direct Mode** (the company IS the edge; no immune system strong enough to reject transformation). **>50 → Edge Mode mandatory** (spawn a 3–5 person board-mandated Edge Twin).
- AOB is a lean team well under 50, so REWRITE is applied **to the whole company in place**. No separate Edge Twin entity is required.
- **Tier:** Tier 2 (≤50 employees, ≤$2M revenue) per A1/A2. Apply REWRITE to the whole company; stand up MVIS in week one; run a 90-Day Sprint on the highest-coordination workflow; Malik can run BACKCAST himself in a one-day workshop.
- **Existence proof (Tier 2 / Direct Mode):** Steinberger built OpenClaw solo on a single Friday evening (Nov 2025), ran 4–10 agents in parallel, 6,600+ commits in Jan 2026, 145k+ GitHub stars, acquisition bids from Meta and OpenAI — no team, no revenue. Solo-founded startups are **36.3% of new ventures** as of early 2026. Direct Mode is the modal new company, not a thought experiment.

> **Note on terminology:** Even in Direct Mode, AOB will use the *Edge Twin data-governance discipline* (Workflow Data Manifest, CIO Diagnostic, no-data-fork, ERP-wins) as the governance pattern for its first agent on a live workflow. The discipline is portable; the separate-entity requirement is not. Where this plan says "twin," read it as "the first governed agent operating on a production AOB workflow."

---

## 4. DRIVE Assessment — the Intelligence Engine (1–5 each, total 25)

> GOVERN-cap rule applied: with GOVERN/ASSURE **absent** (A4), the DRIVE total is **capped at 13/25** regardless of raw sum. The raw sum below already sits at the cap line, so the cap is binding as a ceiling going forward.

| Component | Score | Reasoning (grounded) |
|---|---|---|
| **D — Decision Architecture** | **2** | Some implicit routing exists (`aob-ops` routes disputes/bulk-changes/pricing to Malik), but there is no explicit two-way/one-way-door Agency Map. Most decisions still funnel to Malik. |
| **R — Recursive Learning** | **2** | Weekly ops produces a summary issue and weekly reviews exist (`weekly-review-2026W*.md`), but learnings aren't versioned/propagated at machine speed; no LEARN layer. |
| **I — Intelligence Stack** | **1** | No MVIS yet. Centaurion is "building"; isolated tooling, no event bus / agent registry / central logging / one-agent-per-class. **Capped at the lowest Four Pillar (see sub-rubric) = 1.** |
| **V — Value Moat** | **2** | Genuine moat sources exist (proprietary methodology + curatorial judgment + a facilitator network effect), but today they rest partly on inertia and tacit knowledge. Single-model risk open (A6). |
| **E — Elastic Agency** | **3** | Structurally strong for a small firm: facilitators are *already* an elastic, composable delivery pool (A3) — close to a Capability Registry in spirit. No formal registry/graduated-authority logic yet. |
| **Raw total** | **10/25** | |
| **GOVERN status** | **Absent** | **Cap = 13/25. Effective DRIVE = 10/25.** |

### Four Pillars sub-rubric (inside I — score each 1–5; I = the minimum)
| Pillar | Score | Note |
|---|---|---|
| Trusted Evals | 1 | No eval suites on any agent. |
| Searchable Logs w/ Correlation IDs | 1 | No correlation-ID logging of agent decisions. |
| Granular Rollback | 2 | CRM migration has a rollback plan (60-day Ontraport retention) — workflow-level rollback thinking exists, but not agent/prompt/model rollback. |
| Human Review Queue | 2 | Malik *is* the de-facto review queue for exceptions, but it's informal, no SLAs. |
| **Four Pillars Maturity (minimum)** | **1** | **No new agent class may deploy until every pillar ≥ 3.** |

**DRIVE headline: 10/25 (capped at 13).** The binding constraint is **I = 1**, which is the GOVERN/ASSURE gap. This is the first thing to build.

---

## 5. SHAPE Assessment — the Organizational Form (1–5 each, total 25)

| Component | Score | Reasoning (grounded) |
|---|---|---|
| **S — Safe Autonomy** | **1** | No Fiduciary Wedge, no Permission Envelopes, no written specs, no tested kill switch (A4). Four Pillars at 1s ⇒ S capped at 1. |
| **H — Human Architecture** | **3** | Unusually healthy for the framework: the design intent is to *free human time for connection*, and facilitators are a real apprenticeship pipeline (Application → Foundation → Supervised Delivery → Certification → Ongoing Development) — a built-in junior loop. Held to 3 (not higher) because no explicit Middle-60% absorption math has been done for the admin role, which is the role most exposed to automation. |
| **A — Adaptive Architecture** | **3** | The deliberate consolidation onto GHL (swap-out of Ontraport, point-solutions reduced) shows modular, swappable thinking. Not yet pod-based; Centaurion layer immature. |
| **P — Purpose Control** | **2** | Strong implicit purpose and brand, but the MTP is not yet a three-layer protocol with a Constraint Layer that has teeth. Section 2 of this doc is the first draft; it scores 2 until signed. |
| **E — Ecosystem Trust** | **2** | Vendor relationships are contract/PDF-based; no agent-to-agent auth, no HIDO metadata, no cross-firm liability framework. Fine for today's scale, but a gap before any agent transacts across a firm boundary (e.g., a corporate-client procurement agent). |
| **Total** | **11/25** | |
| **Middle-60% absorption modeled?** | **No** | Triggers the discipline: model the admin-role absorption honestly before any headcount/role change. Not a crisis at this size, but mandatory before Step 5. |

**SHAPE headline: 11/25.** Highest-leverage SHAPE moves: **(1) author and sign the three-layer MTP (P), (2) stand up Safe Autonomy basics — Fiduciary Wedge + Permission Envelope + Four Pillars to ≥3 (S).** H and A are already relative strengths to build from.

> **Combined read:** DRIVE 10 / SHAPE 11. AOB is **SHAPE-leaning relative to DRIVE** — it has good human/adaptive bones but almost no intelligence engine or governance plane yet. The risk is *stall* (SHAPE-without-DRIVE), not *crash*. The cure is to build the Intelligence Stack (MVIS) and GOVERN/ASSURE — but build them *with* the Fiduciary Wedge from day one so DRIVE doesn't outrun SHAPE later.

---

## 6. REWRITE Playbook — six steps, tailored to AOB (sequence non-negotiable)

GOVERN/ASSURE runs across every step: alert-only → escalation authority → kill-switch capable. It is a continuous layer, not a gate.

### Step 1 — BACKCAST & DEFINE  *(gate: the Five Design Conditions)*
**Mechanism:** a **one-day** founder workshop (Tier 2 — Malik can run it himself). **Output:** a signed Destination Architecture, the Five Design Conditions instantiated as a binding exit gate, the candidate-workflow pipeline ranked, and a written mandate.

**Five Design Conditions — Step-1 binding gate (all five must hold; any violation = Step 1 not done):**

| # | Condition | What it looks like at AOB | Holds today? |
|---|---|---|---|
| 1 | AI-Centric Workflow Architecture | Admin/coordination workflows (scheduling, certification-pipeline routing, membership access sync, renewal nudges) designed agent-first, facilitators kept for human delivery. | **Not yet** — design intent only. |
| 2 | Recursive Improvement Infrastructure | Weekly ops + client-satisfaction-by-facilitator feed a LEARN loop that versions and propagates improvements. | **Partial** — weekly cadence exists; no machine-speed propagation. |
| 3 | Model Sovereignty & Governed Autonomy | At least two model families available; owned orchestration logic; Permission Envelopes + kill switch. | **Not yet** (A6, A4). |
| 4 | Intelligence Density at Every Layer | Revenue/throughput per human rising as agents absorb coordination; facilitator time reallocated to delivery. | **Not yet measured.** |
| 5 | Human Flourishing as a Binding Constraint | Automation frees facilitator/admin time for higher-value human work; honest transition support for the admin role. | **Strong intent; not yet engineered with budget.** |

**Exit criteria:** Destination Architecture signed; all five conditions instantiated (today three are "not yet" — those become Step 2 inputs); pipeline ranked; mandate written. **Step 1 is NOT complete until conditions 1, 3, and 4 are credibly instantiated.**

### Step 2 — ASSESS & PREPARE
Run the **Eight-Dimension Readiness Score** (Section 7), add the Four-Pillars Maturity sub-rubric and the Miura-Ko cross-reference, choose the on-ramp. **Stand up MVIS in week one regardless of on-ramp.** Retake every six months.
**Exit:** Readiness scored + banded; on-ramp chosen; MVIS spec'd.

### Step 3 — EXTRACT  *(gate: Workflow Data Manifest)*
Knowledge Archaeology + Extraction Sprint + Elicitation-First Principle. The first agent for any human should be an **elicitation agent**, not a task executor — capture the admin's and facilitators' tacit operating logic (the dominant failure mode is people who can't articulate their own logic). **Produce a one-page Workflow Data Manifest** (Section 9) for the first workflow. Binary rule: *if you cannot state why the workflow needs a field, the agent does not get it.*
**Exit:** tacit knowledge elicited; **Manifest signed** (Step 4 does not begin without it).

### Step 4 — DIAGNOSE & STRIP
Run the **Task Decomposition Matrix** (the single most important diagnostic) across the highest-coordination function (Admin/Operations). Score every task 1–5 for Agent Readiness; disposition agent_now / pilot_step_5 / stay_human. Appoint a **CAIO** — at Tier 2 this is a *hat Malik wears* (technical fluency + P&L literacy already co-located in the founder), not a separate hire.
**Exit:** Matrix scored; Wave 1/2/3 candidates named; absorption delta handed to SHAPE-H.

### Step 5 — BUILD & PROVE  *(parallel run as shadow mode + four cold-start feeds)*
Decision Handover Waves: low-risk → medium → higher-judgment. **Parallel-run-then-deprecate**, success criteria defined *before* the run. Never more than 2–3 parallel workflows at once. Budget **10–15% of savings** for the People Side of Parallel Runs and name a transition leader.
**Cold-start protocol (the parallel run IS shadow mode):** (1) historical replay (curated past cases for *this* workflow), (2) shadow comparison (log every divergence: agent rec vs. human action vs. outcome, on a correlation ID), (3) human-correction capture (override reason from a controlled taxonomy — *no reason, no override*), (4) synthetic edge cases (e.g., contraindicated-participant inquiry, payment dispute). **The test of a real twin: the human-override rate falls over time.** If it doesn't, it's automation with a chat box.
**Exit:** Wave 1 workflow proven against pre-set benchmarks; override rate trending down; legacy workflow not deprecated until the trend holds.

### Step 6 — REWIRE & EVOLVE
Replace the implicit org chart (a latency map) with pod-based working: a small "ops pod" of admin-human + agents + Malik-as-validator. Apply sector-appropriate Elastic Agency ratios (information-centric: ~70% AI / ~20% internal human / ~10% elastic external — directional, expect ~10pt/yr drift toward AI). Make the **Continuous Kill Switch** a permanent rhythm; measure Organizational Half-Life.
**Exit:** pods replace ad-hoc coordination; kill switch is routine; cadence set.

---

## 7. Eight-Dimension Readiness Score

> Scored 1–10 each, total 80. Sector: **Information-centric**. Mode: **Direct (≤50)** per A1.

| # | Dimension | Score | Reasoning |
|---|---|---|---|
| 1 | Organizational Drag | **6** | Lean team, little bureaucracy; drag concentrated in manual admin/coordination and the in-flight CRM migration. |
| 2 | AI Elevation | **5** | AI is a strategic concern at the founder level (Centaurion exists), but no formal CAIO role and the Stack isn't built. Founder-sponsored, not yet C-table-institutionalized. |
| 3 | Work Architecture | **4** | Some task-level thinking (ops checklist, facilitator playbooks) but the unit of analysis is still largely the role, not the task. |
| 4 | Firm Boundary Design | **6** | Facilitators are already an elastic, composable delivery pool (A3) — ahead of most firms — but not deliberately composed via a Capability Registry. |
| 5 | Decision Autonomy | **3** | Most non-routine decisions route up to Malik; little delegated authority and no Permission Envelopes for agents. |
| 6 | Network Structure | **4** | Small enough for peer-to-peer flow, but information still hubs through Malik; no pods. |
| 7 | Reinvention Cadence | **5** | Actively re-platforming (Ontraport→GHL) and building Centaurion; no Continuous Kill Switch or Organizational Half-Life metric yet. |
| 8 | Tacit Knowledge Accessibility | **4** | Playbooks and SOPs exist for facilitation; key ops/strategy knowledge still tacit in Malik. No Elicitation-First practice yet. |
| | **Total** | **37 / 80** | |

**Band: FOUNDATIONAL** (33–55: foundational work needed first). Just inside the band; not survival risk, not yet ready for full REWRITE.

**Four Pillars Maturity (from §4): minimum = 1/5.** Below the ≥3 deploy threshold — no new agent class deploys until raised.

**Miura-Ko cross-reference:** Readiness 37 maps to **L2 (Team Workflow)** on paper. *Lived reality is L1 (Personal Productivity), arguably L0–L1* — there is no compounding team-level AI infrastructure deployed yet; Centaurion is still "building." **Trust-the-ladder rule applies: treat AOB as L1.** The divergence (paper L2 vs. lived L1) is the classic signature of *architecture intended but not yet deployed* — the most expensive failure mode. The remedy is deployment of a real first workflow (Step 5), not more planning.

### On-ramp recommendation
- ☐ MVIS only
- ☑ **MVIS + 90-Day Sprint** ← **recommended**
- ☐ Full REWRITE

**Rationale:** Foundational band + L1 lived reality + Tier 2 = do not attempt full REWRITE. Stand up MVIS in week one (event bus, agent registry, central logging, one agent per class + Four Pillars at MVP level), then run a 90-Day Sprint on one high-coordination, reversible, measurable workflow to move from L1 to a real L2/L3 and lift Four-Pillars Maturity to ≥3.

**Three lowest dimensions to work first:** Decision Autonomy (3), Work Architecture (4), Tacit Knowledge Accessibility (4) / Network Structure (4).

---

## 8. Smallest Safe First Workflow

**Recommended Wave 1 workflow: Facilitator Certification-Pipeline Coordination & Renewal-Risk Detection.**

Why this one (it scores high on every "smallest safe" criterion):
- **High coordination-to-judgment ratio** — application intake, stage-tracking, scheduling supervised deliveries, renewal reminders, directory updates are mostly coordination, not judgment.
- **High-volume & recurring** — the certification pipeline is the explicit growth lever and runs continuously.
- **Rule-clear & measurable** — clear stages and pipeline metrics already defined (applications, conversion, completion, retention, satisfaction-by-facilitator).
- **Reversible & low regulatory exposure** — reminders/routing/status updates are reversible; no money-of-record decision, no medical advice.
- **Historical cases available** — past cohorts give a replay set.
- **Fiduciary Wedge respected** — anything touching pricing, certification *status decisions*, or disputes stays human (matches `aob-ops` routing).

**Runner-up:** Membership access-sync + support triage (GHL ↔ Mighty Networks tag reconciliation). Also a strong "support-triage / order-status-exception" pattern; hold as Wave 1b.

**Explicitly NOT first (bad candidates):** pricing/program-structure changes, certification *pass/fail* judgments, facilitator dispute resolution, any participant medical-safety screening decision — all high-judgment or safety/Fiduciary-Wedge-gated.

**Pre-set success benchmarks (define before the parallel run):** pipeline cycle time (application→certified), reminder/renewal on-time rate, admin hours per cohort, error rate on access-sync, and — above all — **the human-override rate must fall over time** (baseline Day 1, target: halve within 60 days; the trend matters more than the number).

---

## 9. Edge Twin Data-Governance — applied to the first workflow

Even in Direct Mode, the first agent operating on a live AOB workflow gets the full governance discipline. **No data fork:** the agent does not copy the contact estate or get super-user DB access; it gets **workflow-scoped, governed API access** to exactly what the certification-coordination workflow needs. Read/write separated, every call logged on a correlation ID, credentials short-lived and revocable. **ERP-wins:** if the agent and GoHighLevel/Stripe disagree, **GHL/Stripe win** — the agent is the reasoning/orchestration layer, never a second system of record (A5).

### 9a. Workflow Data Manifest — Facilitator Certification Coordination & Renewal-Risk

**Binary rule applied:** any field that cannot be justified by this workflow is removed.

| # | Source (system / dataset) | Purpose (why THIS workflow needs it) | Access | Sensitivity tier | Retention in agent memory | Named data owner |
|---|---|---|---|---|---|---|
| 1 | GHL — facilitator contact records | Identify pipeline stage, contact info to send the right nudge | read | confidential (PII) | zero beyond run | Malik *(ASSUMPTION — confirm owner)* |
| 2 | GHL — certification stage/tag fields | Drive stage transitions and renewal-due detection | read_write *(write = status tag updates only, not pass/fail)* | confidential | zero beyond run | Malik *(confirm)* |
| 3 | GHL — email/SMS workflow triggers | Enroll a facilitator into the correct reminder/renewal sequence | write | internal | zero beyond run | Malik *(confirm)* |
| 4 | Google Calendar — supervised-delivery slots | Schedule/track supervised deliveries with mentors | read_write | internal | zero beyond run | Admin support *(confirm name)* |
| 5 | Client-satisfaction-by-facilitator metric | Renewal-risk signal (QA-gated quality flag) | read | internal | aggregate only | Malik *(confirm)* |
| 6 | Stripe — renewal payment status | Confirm renewal paid before granting continued access | read | restricted (financial) | zero beyond run | Malik *(confirm)* |

**Excluded by the binary rule (examples):** full membership community engagement data, marketing analytics, unrelated CRM segments, any participant health-screening notes — none are justified by *this* workflow, so none travel to the agent.

**HIDO Six Questions** must be answered per object (what is it / who says so / how usable / legal terms / what if wrong / dispute resolution), carried as immutable, hashed, signed metadata. *Status: TO DO in Step 3.*

**Access ≠ training:** pin in the vendor contract — retention, training rights, deletion rights, audit rights, model isolation. The agent retrieves at runtime; it does **not** train on this data by default.

### 9b. CIO Edge Twin Diagnostic (Appendix F) — red/amber/green gate

> Gate rule: any **Red on Q5, Q6, Q7, or Q8** (the SHAPE controls — leakage, identity, recovery, accountability) **blocks the build** until it turns Amber/Green.

| # | Question | Score | Note / gap owner |
|---|---|---|---|
| 1 | What is it allowed to do? (Autonomy Tier + Waves) | **Amber** | Define Tier = `recommend_only` for status/renewal nudges, `execute_within_bounds` only for non-destructive tag/calendar writes. Needs written spec. |
| 2 | Source of truth? (ERP wins) | **Green** | GHL + Stripe win ties (A5). Stated and defensible. |
| 3 | Data needed & why? (Manifest + HIDO) | **Amber** | Manifest drafted above; HIDO per-object not yet answered; data owners unconfirmed. |
| 4 | Trains on our data? (access vs training) | **Amber** | Default no-train; must be pinned in the GHL/model-vendor contract. |
| **5** | **Prevent leakage? (SHAPE)** | **RED** | **No Permission Envelope, no GOVERN/ASSURE plane catching OWASP failure modes yet (A4). BLOCKS BUILD until Amber.** |
| **6** | **Identity handling? (SHAPE)** | **RED** | **No scoped workload identity / short-lived creds / per-action correlation-ID logging yet. BLOCKS BUILD.** |
| **7** | **When it's wrong? (SHAPE)** | **RED** | **No confidence score / rollback path / exception queue / Human Review Queue with SLA yet. BLOCKS BUILD.** |
| **8** | **Who is accountable? (SHAPE)** | **Amber** | Malik is the de-facto Fiduciary Wedge, but roles (process / data / risk / supervisor / CAIO / security owners) are not named in writing. Name them → Green. |
| 9 | Smallest safe first workflow? | **Green** | Certification coordination + renewal-risk fits every criterion (Section 8). |
| 10 | Measure success? (override rate falls) | **Amber** | Benchmarks listed; need baselined before parallel run + weekly review on the calendar. |

**Gate decision: BUILD BLOCKED.** Q5, Q6, Q7 are **Red**. These are exactly the GOVERN/ASSURE + Permission Envelope gaps already flagged in DRIVE (I=1) and SHAPE (S=1). **The first build action is to stand up the MVIS GOVERN/ASSURE plane and a Permission Envelope so Q5–Q7 move to Amber.** This is the PocketOS lesson institutionalized — do not deploy the agent before the control plane exists.

---

## 10. First Agent Specification (skeleton — to complete in Step 3/5)

| Property | Draft for the Certification-Coordination Agent |
|---|---|
| **Purpose** | Keep the facilitator certification pipeline moving and flag renewal risk, freeing admin time — derived from the MTP Identity Layer (protect human time for connection). |
| **Stack layer(s)** | SENSE, INTERPRET, ORCHESTRATE/ACT (+ GOVERN/ASSURE always on). |
| **Autonomy Tier** | `recommend_only` for any status/renewal *decision*; `execute_within_bounds` only for non-destructive writes (tag updates, calendar holds, sequence enrollment). **Never** `execute_within_bounds` for destructive/irreversible ops. |
| **Permission Envelope** | Scoped to the six manifest sources only; no access to pricing, pass/fail certification decisions, or the wider CRM; dollar limit = $0 (no payment actions, read-only on Stripe); approval threshold on any write that changes facilitator status. |
| **Memory Boundary** | May remember within-run workflow context; zero retention beyond run except aggregate satisfaction metric; cannot persist PII. |
| **Escalation Rules** | Disputes, pricing/program questions, contraindication/medical questions, satisfaction-below-threshold → escalate to Malik (default) / admin (backup). |
| **Eval Suite** | Replay set from past cohorts; synthetic edge cases (contraindicated inquiry, payment-failed renewal, mentor no-show); accuracy floor + override-rate ceiling defined. |
| **Telemetry / Audit Trail** | Correlation ID, input snapshot, reasoning trace, envelope-check result, outcome — to central logging (MVIS). |
| **Reusability Scope** | Designed to generalize to other pipeline-coordination workflows (membership onboarding, corporate-contract scheduling); tag for the Capability Registry. |

*No spec, no agent. This skeleton is completed and signed before the parallel run.*

---

## 11. Cognitive Captivity & other flags
- **Cognitive captivity (A6):** maintain inference across **at least two model families** and own orchestration logic + any fine-tuning data before the agent becomes load-bearing. Open risk — confirm.
- **Customer-side agent inversion:** AOB's corporate-workshop buyers will increasingly evaluate via agents. Make pricing, program pages, and availability **legible to buyer-side agents** — a low-cost moat move.
- **Silent Drift:** define named eval thresholds (accuracy floor + override-rate ceiling) for the certification agent *before* go-live, or drift surfaces as facilitator complaints instead of dashboards.
- **Cross-Organizational Accountability:** not needed yet (no cross-firm agent transactions), but required before any corporate-client procurement agent integration — policy-controlled API + HIDO metadata travel + codesigned liability framework.

---

## 12. Concrete Next Actions

1. **Malik — confirm the assumptions** (A1 headcount, A2 revenue, A3 facilitator employment status, A4 current agent/governance state, A5 source-of-truth = GHL+Stripe, A6 model sovereignty). These gate the Direct-Mode determination and every score above. *(15 min.)*
2. **Sign the three-layer MTP** (Section 2), especially the **Constraint Layer** (medical-claim ban is the load-bearing one). Lifts SHAPE-P from 2.
3. **Run Step 1 BACKCAST** as a one-day founder workshop; instantiate the Five Design Conditions; sign the Destination Architecture + written mandate.
4. **Stand up MVIS in week one** — event bus, agent registry, central logging, one-agent-per-class + Four Pillars at MVP level (eval scaffold, correlation-ID logging on by default, one rollback path, a named Human Review Queue owner = Malik with an SLA). **This is the action that moves CIO-Diagnostic Q5/Q6/Q7 off Red.**
5. **Run Step 3 EXTRACT** on the certification workflow: elicitation agent first; **complete and sign the Workflow Data Manifest** (Section 9a) and the HIDO Six Questions; confirm the named data owners.
6. **Run Step 4 Task Decomposition Matrix** on the Admin/Operations function; name Wave 1/2/3; do the **Middle-60% absorption math for the admin role** and hand it to SHAPE-H + the People-Side budget (10–15% of savings, named transition lead).
7. **Re-score the CIO Diagnostic** once MVIS + Permission Envelope exist; only when Q5/Q6/Q7 ≥ Amber and Four-Pillars Maturity ≥ 3 do you **start the 90-Day Sprint / parallel run** on certification coordination, with the four cold-start feeds and a baselined, falling override-rate target.
8. **Retake the Readiness Score at T+6 months;** target: lift from Foundational (37) toward Ready (56+) and from lived L1 toward a real, deployed L2/L3.

---

## Headline Summary

| Item | Result |
|---|---|
| **MTP (working)** | "A breath away from anyone's best state" — encoded as Constraint / Decision / Identity protocol (Section 2). |
| **Mode** | **Direct Mode** (Tier 2, ≤50 — ASSUMPTION A1). Apply REWRITE to the whole company; use the Edge-Twin *governance discipline* without a separate entity. |
| **DRIVE** | **10/25** (raw), GOVERN-capped at 13; binding constraint **I = 1** (Four-Pillars min = 1). |
| **SHAPE** | **11/25**; strengths H=3, A=3; gaps S=1, P=2, E=2. SHAPE-leaning vs DRIVE ⇒ risk is *stall*, not *crash*. |
| **Readiness** | **37/80 — Foundational band.** Lived **Miura-Ko L1** (trust the ladder over the paper L2). |
| **On-ramp** | **MVIS + 90-Day Sprint.** |
| **First workflow** | **Facilitator Certification-Pipeline Coordination & Renewal-Risk Detection** (runner-up: membership access-sync + support triage). |
| **Gate status** | **CIO Diagnostic BUILD BLOCKED** — Q5/Q6/Q7 Red (no Permission Envelope / scoped identity / recovery plane). Build the MVIS GOVERN/ASSURE plane first. |

---

### Validation checkpoints cleared
Five Design Conditions instantiated as Step-1 gate ✓ · MTP as three-layer protocol with both litmus tests ✓ · DRIVE scored + GOVERN-cap applied ✓ · Four Pillars scored, I capped at lowest ✓ · SHAPE scored with Middle-60% flag ✓ · Direct/Edge chosen on headcount ✓ · Readiness 8-dimension + band + Miura-Ko (ladder wins) ✓ · Wave 1 workflow named with success criteria ✓ · Workflow Data Manifest + binary rule ✓ · CIO Diagnostic with red/amber/green gate ✓ · No-data-fork + ERP-wins stated ✓ · Cold-start four feeds named ✓ · Agent Spec skeleton (eight properties) ✓ · Cognitive-captivity flag ✓ · Assumptions flagged for human verification ✓ · Source attribution preserved ✓

*Source: ExO 3.0 / The Organizational Singularity (OS Outline v20), Salim Ismail with contributors. Skill adaptation by Kent Langley for OpenExO — https://openexo.com/organizational-singularity*
