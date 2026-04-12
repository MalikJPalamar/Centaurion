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

## v0.2 Requirements (Future — Not in Scope)

- Supermemory actually connected and capturing
- Wiki repos created and populated
- Syncthing running
- gh-aw workflows executing on schedule
- Nova deployed on OpenClaw
- Graphiti + Neo4j deployed
