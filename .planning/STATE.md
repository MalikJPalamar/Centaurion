# STATE — Session Memory

## Current Phase
Phase 2: Memory Integration (TDD — tests written, implementation pending)

## Current Status
Phase 1 COMPLETE (134/134 pass). Phase 2 tests written (expected to fail until implemented).
Daily dev loop infrastructure built and ready to validate.

## Decisions Log

| Date | Decision | Rationale |
|------|----------|-----------|
| 2026-04-12 | Unified repo (exo-cortex + existing dashboard) | User preference. Don't split into separate repos. |
| 2026-04-12 | Native build, not PAI fork | PAI's TypeScript/Bun assumptions don't fit phone-first, multi-runtime. Cherry-pick patterns only. |
| 2026-04-12 | All markdown + JSON, no TypeScript hooks | Portability across runtimes. Intelligence in prompts, not compiled code. |
| 2026-04-12 | Course-corrected to GSD spec-driven approach | Initial implementation skipped specs/tests. Now adding verification before proceeding. |
| 2026-04-12 | Prototype branch for GSD validation | Preserve Phase 0 work on feature branch, validate on prototype branch. |
| 2026-04-12 | Phase 1 COMPLETE | 134/134 verification checks pass. |
| 2026-04-12 | Added daily dev loop | 6am CET GitHub Actions workflow: verify → identify priority → create Issue with TDD plan. |
| 2026-04-12 | TDD for Phase 2 | Tests written BEFORE implementation. All Phase 2 tests expected to fail until work is done. |

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
