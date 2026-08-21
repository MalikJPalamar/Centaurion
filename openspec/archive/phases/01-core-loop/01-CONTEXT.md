# Phase 1 Context — Core Loop

## What We're Validating

The Centaurion exo-cortex skeleton: identity loading, Active Inference loop, Routing Gate, agent personalities, framework coherence, skills architecture, memory config, and multi-runtime support.

## Design Decisions Locked

1. **CLAUDE.md is comprehensive** — contains the full execution schema inline, not just a pointer to skills. This ensures any Claude Code session loads the complete loop without needing to read additional files.

2. **SKILL.md uses YAML frontmatter** — following PAI's pattern. Frontmatter has `name`, `description`, and optional `use-when` trigger.

3. **Framework files are reference docs** — CLAUDE.md is the operational schema; framework/ files provide detailed context for each concept. They're read on-demand, not loaded every session.

4. **Identity files loaded selectively** — L0 sensing loads PURPOSE, MISSION, GOALS, PREFERENCES. Other identity files (BELIEFS, HISTORY, OPINIONS, etc.) are available but not auto-loaded every session.

5. **Routing Gate is a skill, not a hook** — No TypeScript. The Routing Gate is instructions in a SKILL.md that the agent follows as part of the ROUTE step.

6. **Verification is structural** — We can't unit-test markdown prompts, but we CAN verify: files exist, contain required content, cross-references resolve, no broken paths, consistent terminology.

## Acceptance Criteria

All requirements R1-R10 in REQUIREMENTS.md pass. The verification script `tests/verify-core-loop.sh` exits 0.
