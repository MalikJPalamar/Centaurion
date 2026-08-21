# Cognitive Company Blueprint v1.1: Data Layer, Fifth Property, WO-026

> Audience: Centauri. Cold-start-safe. Extends harness doctrine and docs/company/PRD.md.

## 1. FOUR PROJECTS (discernment update -- supersedes the three-project table)

| Project | Kind | Produces | Notes |
|---|---|---|---|
| Dark Factory | Production system | Verified software | PRD live |
| Cognitive Company | Production system | Business operations | This blueprint fills its data + validation layer |
| GTM Harness | Production system | Demand (campaigns, nurture, pipeline) | Twenty + Mautic + sequence engine = CRM/social layer, already extracted as skills; WO-024 spike DEFERRED |
| Centaurion Symbiote (Centaurion.me R&D) | Research program | A co-evolving agent cognitively + cryptographically encoded to one human | CONSUMES the harness doctrine; its human-development, cognitive/nervous-system encoding and cryptographic binding are its OWN track -- NOT factory work orders. Do not schedule; do not conflate. |

Dependency law unchanged: Factory builds the production systems; Company operates them; GTM funds them; the Symbiote research draws components from all, contributes requirements back through canonical docs only.

## 2. BUSINESS FUNCTION MAP (Scaling Up, completed)

Every function must resolve to: an owner-agent, a data source, and an oracle.

| Function | Agent surface | Data source (canonical/derived) | Oracle (WO-026 type) |
|---|---|---|---|
| People | /agents route, routing thresholds | Omnigent sessions, trajectory log | roster probe = live state |
| Strategy & positioning | Cortex + weekly review | centaurion-wiki | human gate (not oracle-able) |
| Product & features | Factory (specs) | openspec/ + archive | gates exit-0, /opsx:verify |
| Customer knowledge | Twenty CRM skill | Twenty API (source of truth for contacts) | API count/state reconcile |
| Marketing | Mautic + aob-brand-voice + GTM harness | Mautic API, campaign wiki pages | acceptance checks + Mautic API state |
| Sales pipeline | Twenty pipeline + Hyros attribution | Twenty + Hyros | pipeline-stage reconcile |
| Finance | /finances route | Stripe (source of truth) | Stripe API reconcile -- no financial claim without it |
| Cash | /finances + weekly digest | Stripe balances + invoices | balance/invoice reconcile |
| Operations | Nova + browser-harness + auto-fetch | Supermemory inbox -> canonical | three-state connector probes |
| Communication | Hermes (all channels) + Mattermost | session logs (Tier 3) | delivery receipts |
| Data (the central brain) | memory-router | canonical wikis + derived indexes | citation check: every retrieval claim cites canonical |
| Execution rhythm | daily health issue + weekly compaction | Issues + logs | issue-by-08:00 heartbeat |

Rule: a business function without all three columns is not yet cognitive -- it is manual. Track completeness on /doctor.

## 3. HARNESS DOCTRINE v1.1 -- FIFTH PROPERTY

Append to framework/harness-doctrine.md:

> 5. VERIFIABLE (oracle-checked). Logging is not validation. Every material agent claim is checked against a deterministic oracle before it is treated as true. LLM-reviews-LLM (the Symphony pattern) is a smell test, not an oracle.

Ordering update: revert -> audit -> verify -> heal -> evolve.

## 4. WO-026 -- CLAIM LEDGER + ORACLE FRAMEWORK

Purpose: answer, with data evident, (a) "can you audit your agents?" -> WO-025 trajectory; (b) "can you prove their outputs aren't hallucinated?" -> this ledger.

Spec:

1. **Claim typing.** Every material claim emitted by any agent is typed: code | financial | retrieval | ops | content | schedule.
2. **Oracle registry** (`framework/oracles.md` + `skills/oracles/`): code -> tests/gates exit-0 + /opsx:verify; financial/cash -> Stripe API reconcile; customer/pipeline -> Twenty API reconcile; marketing state -> Mautic API; retrieval -> canonical citation resolves; ops -> three-state connector probe; schedule -> calendar/cron state read-back; UI -> visual VERDICT (A2).
3. **Ledger:** append-only JSONL `{ts, agent, wo, claim_type, claim, oracle, result: PASS|FAIL|UNVERIFIABLE, evidence_uri}` in derived store (Tier-3 evidence, NOT canonical wikis). UNVERIFIABLE claims are flagged, never silently accepted.
4. **Surfaces:** /doctor (live pass-rate per agent), /analytics (trend), weekly compaction distills notable FAILs into canonical RCA notes (feeds property 3).
5. **Gate wiring:** any WO whose completion claim lacks a PASS oracle entry cannot reach Gate 2.

Acceptance: demo query answering "show all financial claims this month with oracle results and evidence links" in under 10 seconds. Priority: with WO-025, before first company-WO dispatch.

## 5. COMPETITOR / REFERENCE LEDGER (corrections on record)

- **Symphony by Wix** (launched 2026-08-11): Maestro orchestrator + specialist agents (Outreach, Marketing, Scheduling, Research, Finance, Design), learns-the-business onboarding, mobile approvals, daily standup, accuracy-review agents. Score vs our criteria: gating check, data ingestion check, guardrails ~, validation ~ (LLM-checks-LLM, not oracles), time machine X, audit X, self-evolving X, sovereignty X -> 4/8 cognitive. Treat as market validation + pattern quarry (standup ~ our daily issue; onboarding pipeline worth adapting for BuilderBee). Do not adopt.
- **FounderOS** = Bennettxai/FounderOS-DEMO (MIT). Already quarried: WO-023 route map + three-state connector doctrine.
- **Archestra** = the previously discussed inter-agent platform: A2A gateway + guardrail doctrine (Lethal Trifecta, dual-LLM verification) -- guardrails already adopted as factory law; A2A pattern noted for future company-scale needs; product remains trigger-gated (first RBAC/compliance client).
- Standing competitor watch: OpenHuman, Penpax, Symphony.

## 6. ANTI-BRITTLENESS (restated, binding)

R1-R3 from the harness-doctrine directive apply. Additions:
- **R4** -- no function goes live without its oracle (Section 2 rule).
- **R5** -- the Symbiote track never enters the factory backlog without an explicit new PRD approved at the gate.

## 7. FILING

File as two Issues: (1) Blueprint v1.1 PR -- framework/harness-doctrine.md fifth property + framework/oracles.md + this doc referenced from docs/company/PRD.md; (2) WO-026. Both land at Malik's gate.
