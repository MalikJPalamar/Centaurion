# STATE — Session Memory

## Current Phase
Phase 1: Core Loop

## Current Status
Implementation complete. Verification pending.

## Decisions Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-04-12 | Unified repo (exo-cortex + existing dashboard) | User preference. Don't split into separate repos. |
| 2026-04-12 | Native build, not PAI fork | PAI's TypeScript/Bun assumptions don't fit phone-first, multi-runtime. Cherry-pick patterns only. |
| 2026-04-12 | All markdown + JSON, no TypeScript hooks | Portability across runtimes. Intelligence in prompts, not compiled code. |
| 2026-04-12 | Course-corrected to GSD spec-driven approach | Initial implementation skipped specs/tests. Now adding verification before proceeding. |
| 2026-04-12 | Prototype branch for GSD validation | Preserve Phase 0 work on feature branch, validate on prototype branch. |

## Blockers
None currently.

## Open Questions
- Should CLAUDE.md be minimal (pointer to skills) or comprehensive (full loop inline)?
  - Decision: Comprehensive. CLAUDE.md IS the execution schema. Skills provide detail.
- How to test "agent behavior" from a markdown-only framework?
  - Decision: Structural verification (files exist, content correct, cross-refs valid) + manual UAT.

## Branch Map
| Branch | Purpose | Status |
|--------|---------|--------|
| `main` | Production (existing dashboard + exo-cortex) | Stable |
| `claude/centaurion-pai-fork-g9XC7` | Phase 0 implementation | Complete, pushed |
| `prototype/centaurion-core-loop` | GSD validation + verification | Active |
