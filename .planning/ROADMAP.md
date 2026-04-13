# ROADMAP — Centaurion

## Phase 1: Core Loop ✅ COMPLETE
> "Does the exo-cortex skeleton work?"

- [x] All v0.1 requirements pass verification (R1-R10)
- [x] Verification script runs green (134/134 pass)
- [ ] CLAUDE.md produces correct agent behavior when opened in Claude Code (manual UAT)

**Definition of Done:** `tests/verify-core-loop.sh` exits 0. All 10 requirement groups pass.
**Status:** 134/134 automated checks pass. Manual UAT pending.

## Phase 2: Memory Integration ✅ COMPLETE
> "Can the exo-cortex remember?"

- [x] Supermemory status set to `connected` in config
- [x] centaurion-wiki created with ≥3 pages of framework knowledge
- [x] State files created (ratings.jsonl, routing-log.jsonl)
- [x] CLAUDE.md REMEMBER step references Supermemory explicitly
- [x] Core skill references Supermemory in SENSE and REMEMBER
- [x] Feedback capture workflow defined
- [x] Weekly review references ratings data source

**Definition of Done:** `tests/verify-memory-integration.sh` exits 0. 14/14 pass.

## Phase 3: Multi-Runtime & Feedback ✅ COMPLETE
> "Can other agents run the same loop?"

- [x] Deploy configs for pi, OpenClaw, Agent Zero
- [x] Deploy README with instructions
- [x] Wiki pages expanded (feedback-loop, multi-runtime-deployment)
- [x] Sample state entries in ratings.jsonl and routing-log.jsonl
- [x] Daily health workflow has concrete checks

**Definition of Done:** `tests/verify-multi-runtime.sh` exits 0. 12/12 pass.

## Phase 4: Knowledge Depth (TDD — tests written, implementation by dev loop)
> "Does the system have deep, cross-linked knowledge?"

- [ ] centaurion-wiki expanded to ≥10 pages with cross-links
- [ ] AOB wiki created with ≥5 foundation pages
- [ ] BuilderBee wiki created with ≥5 foundation pages
- [ ] All identity files are substantial (≥500 bytes)
- [ ] GOALS.md updated to reflect current work

**Definition of Done:** `tests/verify-knowledge-depth.sh` exits 0. All R19-R22 pass.

## Phase 5: Operational Workflows (TDD — tests written, implementation by dev loop)
> "Can the system execute real venture work?"

- [ ] All 5 core skills expanded with examples (≥1000 bytes)
- [ ] AOB operations skill created
- [ ] BuilderBee delivery skill created
- [ ] Client onboarding workflow for BuilderBee
- [ ] Weekly ops workflow for AOB
- [ ] Framework README index linking all docs
- [ ] Every framework file cross-references others

**Definition of Done:** `tests/verify-operational.sh` exits 0. All R23-R26 pass.

## Phase 6: Cross-Venture Coherence (TDD — tests written, implementation by dev loop)
> "Does the system compound knowledge across ventures?"

- [ ] Cross-venture map connecting AOB ↔ BuilderBee ↔ Centaurion
- [ ] Wiki cross-references between ventures
- [ ] System coherence verified (consistent Three Laws, memory tags)
- [ ] Getting started guide + architecture doc
- [ ] CHANGELOG tracking all phases
- [ ] Case study: "Centaurion as its own client"

**Definition of Done:** `tests/verify-coherence.sh` exits 0. All R27-R30 pass.

---

## Meta: Daily Development Loop
> "Does the system develop itself on a schedule?"

- [x] `.github/workflows/daily-dev-loop.yml` runs at 6am CET daily
- [x] Runs all phase verification tests
- [x] Identifies next priority via `tests/identify-next-priority.sh`
- [x] Creates GitHub Issue with TDD plan (red → green → refactor)
- [x] Closes previous day's dev-loop issue automatically
- [ ] Connected to Claude API for autonomous execution (future)

**Definition of Done:** `tests/verify-dev-loop.sh` exits 0. Daily issues appear on GitHub.
