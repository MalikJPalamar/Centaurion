# REQUIREMENTS — Centaurion v0.1

## Scope: What v0.1 Must Do

The minimum viable exo-cortex. When a user opens this repo in Claude Code, the agent:
1. Identifies as Cortex
2. Knows who Malik is (loads identity)
3. Follows the Active Inference loop (7 steps)
4. Classifies tasks through the Routing Gate
5. Knows about the three ventures
6. Produces phone-readable output

## v0.1 Requirements (Testable)

### R1: Identity Loading (L0 Sensing)
- **R1.1:** `CLAUDE.md` exists at repo root and is auto-loaded by Claude Code
- **R1.2:** `CLAUDE.md` references Cortex as the agent identity
- **R1.3:** `CLAUDE.md` references all 4 core identity files: PURPOSE.md, MISSION.md, GOALS.md, PREFERENCES.md
- **R1.4:** All 10 identity files exist in `identity/` and are non-empty
- **R1.5:** `identity/PURPOSE.md` contains the Fitness Equation (`Predictive Order / Thermodynamic Cost`)
- **R1.6:** `identity/MISSION.md` contains all Three Laws (Hierarchy, Routing, Coupling)
- **R1.7:** `identity/MISSION.md` references all three ventures (AOB, BuilderBee, Centaurion)

### R2: Active Inference Loop
- **R2.1:** `CLAUDE.md` defines all 7 loop steps: SENSE, PREDICT, COMPARE, ROUTE, ACT, OBSERVE OUTCOME, REMEMBER
- **R2.2:** `framework/active-inference-loop.md` exists with detailed step descriptions
- **R2.3:** Each step maps to a PAI Algorithm phase (OBSERVE→SENSE, THINK→PREDICT, etc.)
- **R2.4:** REMEMBER step is marked as mandatory
- **R2.5:** Loop references the Routing Gate in the ROUTE step

### R3: Routing Gate
- **R3.1:** `skills/routing-gate/SKILL.md` exists with frontmatter (name, description, use-when)
- **R3.2:** Defines three classification dimensions: novelty (0-1), stakes (0-1), reversibility (0-1)
- **R3.3:** Contains the decision rule: `novelty > 0.7 AND stakes > 0.5 AND reversibility < 0.3 → STOP`
- **R3.4:** `framework/routing-gate.md` exists with scoring rubrics for each dimension
- **R3.5:** Decision rule instructs agent to surface to Malik (not auto-execute) when thresholds met

### R4: Agent Personalities
- **R4.1:** `agents/Cortex.md` exists and identifies as "reasoning agent"
- **R4.2:** `agents/Nova.md` exists and identifies as "sensing agent"
- **R4.3:** `agents/Daemon.md` exists and identifies as "identity root"
- **R4.4:** Each agent file defines: Identity, Role, Runtime, Principles
- **R4.5:** `CLAUDE.md` references `agents/Cortex.md`

### R5: Framework Coherence
- **R5.1:** `framework/three-laws.md` defines Hierarchy, Routing, and Coupling laws
- **R5.2:** `framework/fitness-equation.md` contains the equation and its components
- **R5.3:** `framework/five-sensing-layers.md` defines L0-L4 with triggers and descriptions
- **R5.4:** All framework files are cross-referenced (Three Laws reference Routing Gate, etc.)
- **R5.5:** `framework/markov-blanket.md` defines the boundary concept and maps it to Daemon

### R6: Skills Architecture
- **R6.1:** All SKILL.md files have YAML frontmatter with `name` and `description`
- **R6.2:** `skills/centaurion-core/SKILL.md` references identity files for L0 loading
- **R6.3:** At least 5 skills exist: centaurion-core, routing-gate, weekly-review, sa-scan, gap-analysis
- **R6.4:** CLAUDE.md lists available skills with directory paths

### R7: Memory Configuration
- **R7.1:** `memory/supermemory.json` exists with container tags for all three ventures
- **R7.2:** `memory/wiki-repos.json` exists with URLs for three wiki repos
- **R7.3:** `memory/graphiti.json` exists with `planned_month_2` status
- **R7.4:** No actual API keys committed (all use REPLACE_WITH_ placeholder)

### R8: Multi-Runtime Support
- **R8.1:** `AGENTS.md` exists at repo root for non-Claude-Code runtimes
- **R8.2:** `AGENTS.md` contains the same Three Laws and Active Inference loop as CLAUDE.md
- **R8.3:** `AGENTS.md` includes runtime-specific notes for pi, OpenClaw, Agent Zero, Codex

### R9: Output & Style
- **R9.1:** `CLAUDE.md` specifies concise, phone-readable output format
- **R9.2:** `identity/PREFERENCES.md` specifies structured output (tables, headers, bullets)
- **R9.3:** `CLAUDE.md` instructs agent to surface tradeoffs and state reasoning

### R10: Structural Integrity
- **R10.1:** All paths referenced in CLAUDE.md exist as actual files
- **R10.2:** All paths referenced in AGENTS.md exist as actual files
- **R10.3:** All internal cross-references between framework files resolve
- **R10.4:** No broken links between skills and framework files
- **R10.5:** README.md accurately describes the directory structure

---

## v0.2 Requirements — Daily Dev Loop & Feedback Infrastructure (Testable)

### R11: Daily Development Loop
- **R11.1:** `.github/workflows/daily-dev-loop.yml` exists and is valid YAML
- **R11.2:** Workflow triggers on `schedule` with cron `0 4 * * *` (6am CEST / 5am CET)
- **R11.3:** Workflow also triggers on `workflow_dispatch` for manual runs
- **R11.4:** Workflow runs `tests/verify-core-loop.sh` as first step
- **R11.5:** Workflow runs `tests/verify-dev-loop.sh` for dev loop self-test
- **R11.6:** Workflow runs `tests/identify-next-priority.sh` to detect next critical requirement
- **R11.7:** Workflow creates a GitHub Issue with status report + development plan
- **R11.8:** Issue title follows format: `[dev-loop] YYYY-MM-DD — Phase N: description`
- **R11.9:** Issue body contains: current pass/fail counts, next priority, TDD plan (test → implement → verify)
- **R11.10:** Workflow labels issues with `dev-loop`, `automated`

### R12: Priority Identification
- **R12.1:** `tests/identify-next-priority.sh` exists and is executable
- **R12.2:** Script reads verification output and determines highest-priority failing requirement group
- **R12.3:** Script outputs structured JSON: `{"phase": N, "requirement": "RXX", "description": "...", "test_file": "..."}`
- **R12.4:** Priority order follows ROADMAP phases: Phase 1 gaps first, then Phase 2, etc.
- **R12.5:** If all current phase requirements pass, script advances to next phase
- **R12.6:** Script exits 0 with output even when nothing is failing (reports "all current requirements pass")

### R13: TDD Cycle Structure
- **R13.1:** Each phase has a verification script: `tests/verify-phase-{N}.sh`
- **R13.2:** Phase 1 verification exists: `tests/verify-core-loop.sh` (already built)
- **R13.3:** Phase 2 verification exists: `tests/verify-memory-integration.sh`
- **R13.4:** Phase 2 tests are written BEFORE Phase 2 implementation (tests fail initially = correct TDD)
- **R13.5:** `tests/run-all.sh` exists and runs all phase verification scripts in order
- **R13.6:** `tests/run-all.sh` produces combined pass/fail counts and overall exit code

### R14: Dev Loop Self-Test
- **R14.1:** `tests/verify-dev-loop.sh` exists and verifies the loop infrastructure itself
- **R14.2:** Checks that daily-dev-loop.yml is valid workflow syntax
- **R14.3:** Checks that identify-next-priority.sh is executable and produces valid JSON
- **R14.4:** Checks that all phase verification scripts exist for defined roadmap phases
- **R14.5:** Checks that ROADMAP.md and REQUIREMENTS.md are in sync (same phase names)

### R15: Phase 2 — Memory Integration (Tests Written Now, Implementation Later)
- **R15.1:** `memory/supermemory.json` has `status` field set to `connected` (currently `planned`)
- **R15.2:** `memory/wiki-repos.json` has at least one repo with `status: active` (currently all `planned`)
- **R15.3:** A file `memory/state/ratings.jsonl` exists for capturing outcome ratings
- **R15.4:** A file `memory/state/routing-log.jsonl` exists for capturing routing decisions
- **R15.5:** `skills/centaurion-core/SKILL.md` references Supermemory recall in the SENSE step
- **R15.6:** `skills/centaurion-core/SKILL.md` references memory write in the REMEMBER step
- **R15.7:** Wiki content for centaurion-wiki exists with at least 3 pages of framework knowledge
- **R15.8:** `CLAUDE.md` REMEMBER step references Supermemory capture explicitly

### R16: Phase 3 — Feedback Infrastructure (Tests Written Now, Implementation Later)
- **R16.1:** `workflows/daily-health.md` references actual monitoring endpoints (not just template)
- **R16.2:** `memory/state/` directory exists with initialized state files
- **R16.3:** `skills/weekly-review/SKILL.md` references `memory/state/ratings.jsonl` as data source
- **R16.4:** A `workflows/feedback-capture.md` exists defining how ratings flow into state
- **R16.5:** `framework/routing-gate.md` documents threshold adjustment procedure with examples

## v0.3 Requirements (Future — Not in Scope)

- Supermemory actually connected and capturing live conversations
- Nova deployed on OpenClaw with Centaurion personality
- Syncthing running between VPSs
- Graphiti + Neo4j deployed and connected
- Autoresearch overnight iteration running
