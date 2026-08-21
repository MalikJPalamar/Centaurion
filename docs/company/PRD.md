# PRD — Cognitive Company v0.5
Target path: docs/company/PRD.md in MalikJPalamar/Centaurion
Owner: Malik Palamar · Implementer: the Dark Factory (Centauri dispatching)
Status: Supersedes ai-native-company-v0.4-handoff.md. The company is the factory's first product and its acceptance test.

## 1. Product
Business operations (AOB, BuilderBee, Centaurion.me) run by agents under human priors. Every component below is an OpenSpec work order consumed by the factory. Prerequisite: Factory P3 (companion PRD) open.

## 2. Doctrine (settled, non-negotiable)
Canonical = partitioned markdown wikis (personal/aob/builderbee/centaurion) — single source of truth. Vector + graph = derived, disposable indexes rebuilt on commit. Supermemory = ephemeral inbox; weekly review = compaction. One write door (canonical), one read door (memory-router). Invariant: no durable knowledge exists only in a derived index. Precision = Predictive Order / Thermodynamic Cost.

## 3. Work-Order Backlog
| WO | Deliverable | Acceptance |
|---|---|---|
| 001 | browser-harness on VPS 2, encrypted sessions | pi fetches AOB title via harness |
| 002 | skills/browser-task/SKILL.md + domain-skill auto-commit | invocable from Claude Code/pi/Hermes |
| 003 | Nova as Omnigent YAML agent (prompt from `agents/Nova.md`) | Telegram persona reply; out-of-scope write blocked |
| 004 | domain-skill: WordPress AOB | second runtime reuses skill, zero re-learn |
| 005 | 4 canonical wikis, frontmatter schema | UA /understand-knowledge renders graphs |
| 006 | derivation pipeline (post-commit embed + graph extract) | delete indexes → rebuild → identical retrieval |
| 007 | memory-router skill/MCP (verb-routed, RRF-fused, canonical citations) | 3 verb queries return correct pages |
| 008 | Supermemory on 5 runtimes, container tags | cross-runtime write/read correct container |
| 009 | weekly compaction job (mines Hermes FTS5 sessions → draft wiki PR) | first PR: valid pages with source traces |
| 010 | 1000-page ingestion: graphify draft → Malik curates → personal-wiki | ≥95% valid frontmatter; entities reconciled |
| 011 | auto-fetch loop (20-30 min, browser-harness → Supermemory) | Cortex opens with <30-min context |
| 012 | routing-gate skill (novelty×stakes×reversibility) | high-stakes escalates; routine proceeds; logged |
| 013 | SA scan 21:00 CET → PR | 3 consecutive nightly PRs |
| 014 | daily company health issue by 08:00 | phone-readable, R/A/G per subsystem |
| 015 | TokenJuice middleware in pi-ai | ≥30% measured token reduction |
| 016 | domain-skills: Ontraport, Mighty Networks, GHL, Stripe | WO-004 pattern each |
| 017 | InfraNodus monthly gap loop → wiki todos | first report issue |
| 018 | MemPalace cold archive (M2) | verbatim recall skill works |
| 019 | Graphiti+Neo4j temporal graph (M2) | router gains time-verb |
| 020 | BuilderBee client template (wiki+domain-skills+policies+`/understand-onboard`) + design-history.md no-repeat registry (A8) | first billable deploy; no two sites alike |
| 021 | Agent Zero team appliance: Projects per venture, wiki→knowledge sync, charter prompt, secrets for team creds; no factory/repo access | Tania operates Ontraport task without holding password |
| 022 | Cortex-daemon (conditional): claudeclaw-os-fork as always-on Cortex body — channels OFF (Hermes owns messaging), Omnigent-governed, identity loaded from repo, heartbeat+cron only | passes policy violation test; zero gateway overlap |

## 4. v0.5 Amendments
Hermes single-gateway (all channels, one process — pi-mom struck) · Agent Zero scoped to WO-021 charter · Archon seat confirmed = Stores+router+UA (validation, not adoption) · local $0 cells route routine website WOs when hardware lands (factory A6) · Archestra remains the enterprise chassis, trigger-gated (first RBAC/compliance client or AOB rollout).

### A12 — Animated onboarding for Centaurion
Centaurion ("the symbiotic co-evolving agent") gets an animated terminal onboarding flow inspired by OpenSpec's interactive setup wizard. First-run experience walks the operator through identity binding, agent roster, gateway config, and knowledge-layer bootstrap. Scope: CLI-first (terminal ASCII art + step-by-step prompts), portable to web later. Reference: OpenSpec `openspec init` onboarding UX.

## 5. Human-Only (permanent)
Identity files · WO-010 curation judgment · secrets · policy thresholds · the two gates.

## 6. Operating Protocol (steady state)
Morning ≤10 min: health issue → approve specs → merge PRs → Nova priority.
Daytime: lights out (auto-fetch, routing-gate escalations only). Evening: health workflow, SA scan, autoresearch, Syncthing. Weekly: compaction PR review, gap analysis, threshold tuning.

## 7. Acceptance Test — "Can the factory build the company?"
WO-001…022 shipped through the line at exactly 2 touches each (WO-010 curation exempt) · Sprints 1-3 ≤30 days from factory-open · zero hand-built components outside §5 · cost/WO trending down · Week 5: one full week where Malik's only inputs are gates + priorities. Fail on any WO → the factory receives a spec to fix itself first. Either way the factory improves — that is the flywheel.
