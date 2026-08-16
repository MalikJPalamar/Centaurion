# PRD — Dark Factory v0.5
Target path: docs/factory/PRD.md in MalikJPalamar/Centaurion
Owner: Malik Palamar (Gate 1: spec approval · Gate 2: merge) · Implementer: Centauri (main agent)
Status: Supersedes dark-factory-v0.4-handoff.md. Repo exists (90 commits) — Phase 0 is an AUDIT, not a create.

## 1. Product
A software production line: OpenSpec work order in → verified PR out. Exactly 2 human touches per order. Everything between runs lights-out under enforced policy.

## 2. LineINTENT → OpenSpec /opsx:explore → proposal+specs+tasks
  ■ GATE 1 (Malik approves, phone)
→ Omnigent dispatch (Polly pattern, parallel git worktrees, policies enforced)
→ BUILD cells: Claude Code / pi / Codex (cloud) · local pi cell (websites, $0)
→ QA: gstack /review → /cso → /qa  +  visual verdict for UI (A2)
→ VERIFY: /opsx:verify + gate semantics (A1)
→ CI: gh-aw tests/lint + /understand-diff ripple (>5 nodes → escalate)
  ■ GATE 2 (Malik merges, phone)
→ /opsx:archive → wiki → Understand-Anything graph refresh

## 3. v0.5 Amendments (the enrichment ledger)
| # | Amendment | Source | Requirement |
|---|---|---|---|
| A1 | Refusal-to-complete gates. /goal declares success criteria; registered gate commands must exit 0; session cannot self-declare done while gates fail; unchanged-workspace loop detection kills fake fixes | marks-pi-harness gate.ts | Port as Omnigent policy + pi extension on every cell |
| A2 | Visual verdict for UI work. Screenshot via headless Chrome + expect string → model must answer VERDICT: PASS/FAIL. Log-based "looks done" is banned. No console error is "someone else's problem" | marks-pi-harness browser.ts | Mandatory QA step for any deliverable with a UI |
| A3 | Budget tripwires per cell. Per-turn line: calls spent, context %, dig-vs-pivot rule. 3+ near-identical calls → forced structural pivot | marks-pi-harness budget.ts | Install on all cells |
| A4 | Failure triad detection. Trajectory repetition, error-action repetition, pseudo-termination → kill cell + escalate to Malik | OmniAgent Deep Reflexion | Omnigent monitor rule |
| A5 | LLM preflight reviewer. Cheap-model review of planned actions BEFORE policy engine (completes 4-layer scan: LLM review → policy → approval → sandbox) | OmniAgent Hyper-Harness | Omnigent pre-dispatch hook |
| A6 | Local $0 cell class. Proven: local 122B one-shots verified websites headless (4 builds, 0 tool errors). Routing Law on economics: routine product classes → local cells; novel/high-stakes → frontier cloud | marks-pi-harness receipts | Website WOs route local when Apple Silicon lands; cloud until then |
| A7 | Cross-vendor review stays mandatory for cloud cells. Single-model self-verify accepted ONLY on local website cells where visual verdict compensates | v0.4 + A2 | Polly routing rule |
| A8 | design-history.md append-only no-repeat registry for generated sites (WO-020 clients: no two alike) | marks-pi-harness | Repo file + skill rule |
| A9 | Skill-pack routers. One-line-per-skill tables load specialists on demand; kills catalog-sprawl tax (gstack+ASE+centaurion coexistence) | marks-pi-harness pattern | skills/_router/ |
| A10 | Hermes = sole gateway. Telegram/Slack/WhatsApp/Discord/Signal/Email from one process. pi-mom deployments struck; pattern reference only | NousResearch repo | Config, not new runtimes |
| A11 | Archon correction. Knowledge+task seat = OpenSpec Stores + memory-router + Understand-Anything. No YAML-DAG engine anywhere; DAG duties = Omnigent/Polly + gh-aw | coleam00 re-ground | Doc fix |

## 4. Stations & Tools
| Station | Tool | State |
|---|---|---|
| Intake | OpenSpec | install |
| Orchestration+law | Omnigent (pinned, alpha) + policies (`ask_on_os_tools`, 50 calls/session, $5 cap ask@$3, A1/A3/A4/A5) | install VPS 1 |
| Cells | Claude Code, pi, Codex; KiloClaw/Deep Agent overflow; local pi cell (A6, trigger-gated) | partial |
| QA | gstack personas + visual verdict (A2) | install |
| Verify | /opsx:verify + gate semantics (A1) | install |
| CI | gh-aw + /understand-diff | install |
| Archive | /opsx:archive → wikis → UA auto-update | exists partial |

## 5. Phases
P0′ — Audit (repo exists): collapse Framework/`+`framework/ dupe · README Nova runtime → Hermes · fold openspec/, orchestration/, domain-skills/, docs/factory/ · triage 6 open PRs + 1 issue · rotate OpenRouter key · hermes gateway uninstall --system on VPS 2 · verify identity/ untouched by agents.
P1 — Line assembly: OpenSpec init · Omnigent + policy file (incl. A1–A5) · Polly worktrees · gstack QA wiring · gh-aw CI + daily health issue.
P2 — Calibration: one trivial spec end-to-end; measure touches (=2), wall-clock, cost.
P3 — Open: overflow cells connected · autoresearch loop · 3 parallel specs no collision · begin company backlog (companion PRD).

## 6. SLA
Approved spec → verified PR at exactly 2 touches · 100% cross-vendor review on cloud diffs · policy engine provably blocks a deliberate violation · daily health issue by 08:00 CET · cost/spec measured and trending down · archive queryable via UA graph.

## 7. Out of Scope (permanent human territory)
Identity authorship · normalization judgment · secrets (Omnigent env only) · policy thresholds · the two gates · claudeclaw-os-fork as gateway (channels stay Hermes's; see company PRD WO-022 for its only sanctioned mode).
