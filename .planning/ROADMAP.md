# ROADMAP — Centaurion

## Phase 1: Core Loop ✅ COMPLETE
> "Does the exo-cortex skeleton work?"

- [x] All v0.1 requirements pass verification (R1-R10)
- [x] Verification script runs green (134/134 pass)
- [ ] CLAUDE.md produces correct agent behavior when opened in Claude Code (manual UAT)

**Definition of Done:** `tests/verify-core-loop.sh` exits 0. All 10 requirement groups pass.
**Status:** 134/134 automated checks pass. Manual UAT pending.

## Phase 2: Memory Integration (current — TDD: tests written, implementation pending)
> "Can the exo-cortex remember?"

- [ ] Supermemory status set to `connected` in config
- [ ] centaurion-wiki created with ≥3 pages of framework knowledge
- [ ] State files created (ratings.jsonl, routing-log.jsonl)
- [ ] CLAUDE.md REMEMBER step references Supermemory explicitly
- [ ] Core skill references Supermemory in SENSE and REMEMBER
- [ ] Feedback capture workflow defined
- [ ] Weekly review references ratings data source

**Definition of Done:** `tests/verify-memory-integration.sh` exits 0. All R15-R16 requirements pass.
**TDD Status:** Tests written. All currently FAILING (expected — implementation not started).

## Phase 3: Multi-Runtime Deployment
> "Can other agents run the same loop?"

- [ ] Nova personality loaded on OpenClaw (VPS 1)
- [ ] Pi scaffold sharing Centaurion skills (VPS 1)
- [ ] Agent Zero configured with Centaurion context (VPS 2)
- [ ] Syncthing running between VPSs

**Definition of Done:** Nova on OpenClaw responds to a Telegram message using Centaurion identity.

## Phase 4: Feedback Loops
> "Does the system improve itself?"

- [ ] Daily health check creating GitHub Issues
- [ ] Weekly gap analysis running
- [ ] Routing accuracy tracked and thresholds adjustable
- [ ] Ratings captured and trending

**Definition of Done:** Weekly review Issue shows measurable trend data.

## Phase 5: Knowledge Graph (Month 2)
> "Does the system track how knowledge evolves?"

- [ ] Neo4j deployed on VPS 1
- [ ] Graphiti connected via MCP
- [ ] Temporal entity tracking live
- [ ] All three wiki repos with InfraNodus gap analysis

**Definition of Done:** Agent answers "When did we decide to migrate from Ontraport?" from Graphiti.

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
