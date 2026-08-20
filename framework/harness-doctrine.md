# Harness Doctrine

> Canonical. Any harness proposed for any Centaurion project is graded on these five properties.

A harness is fit for any of the four projects only if it has all five properties:

## 1. REVERTIBLE (time machine)

Every action carries an inverse or checkpoint.

Mechanisms in stack:
- Cordis/dsh effect disposers
- Git worktrees + Gate 2
- Derived indexes rebuildable from canonical

## 2. AUDITABLE

Every action attributable to its source.

Mechanisms:
- dsh trajectory view (per-action plugin provenance)
- /opsx:archive
- GitHub Issues
- Memory provenance tags (EXTRACTED / INFERRED / AMBIGUOUS)

## 3. SELF-HEALING

Irreversible failures get RCA, learning injected forward.

Mechanisms:
- Failure-triad tripwires (trajectory repetition, error repetition, pseudo-termination)
- Reflexion-style RCA notes compacted to canonical

## 4. SELF-EVOLVING

The harness improves itself, gated.

Mechanisms:
- dsh creator mode
- Skills
- Standing rule: "a failed WO becomes a spec to fix the factory"

## 5. VERIFIABLE (oracle-checked)

Logging is not validation. Every material agent claim is checked against a deterministic oracle before it is treated as true. LLM-reviews-LLM (the Symphony pattern) is a smell test, not an oracle.

Mechanisms:
- WO-026 Claim Ledger (deterministic oracles per business function)
- API state reconciliation (Stripe, Twenty, Mautic)
- Three-state connector probes (connected|not_configured|error)
- Gate exit-code verification (/opsx:verify)

## Ordering

Revert what you can → audit what you can't revert → verify what you audited → heal from what's verified → evolve from what you healed.

## Scoring

Any harness/tool proposed for any project is graded on these five properties **in addition to** Gate 0 + the four gates (Fit, Cost, Risk, Opportunity).

---

## Conventions (adopted patterns, no runtime dependency)

### C1. Disposer Convention

Every skill that acquires resources (files, processes, API sessions, config mutations) must return or register a cleanup function. On skill exit -- normal or abnormal -- all disposers unwind in reverse order.

Pattern (pseudocode):
```
disposers = []
disposers.push(acquire_resource())   # returns cleanup fn
try:
    do_work()
finally:
    for d in reversed(disposers):
        d()
```

Origin: Cordis/dsh effect system. Adopted as convention, not dependency. Satisfies property 1 (REVERTIBLE) at the skill level.

### C2. Scoped Tool Manifests

Every SKILL.md may declare a `## Phase Tools` section listing which tools are relevant per phase. Agents SHOULD prefer phase-scoped tools over the full tool registry to reduce context size and model confusion.

Format in SKILL.md:
```markdown
## Phase Tools
- **build**: tool_a, tool_b
- **review**: tool_c, tool_d
- **verify**: tool_e
```

Estimated impact: ~2.2K tokens/step saved by scoping 15-20 tools down to 3-5. Over a 10-task batch averaging 3 steps: ~66K tokens saved. **This claim is UNVERIFIABLE until measured against a real batch per property 5. First WO-026 oracle entry.**

Origin: dsh `ToolRestriction` / `ctx.tools.restrict()`. Adopted as SKILL.md convention. No runtime enforcement yet -- agents honor it voluntarily; runtime enforcement deferred to when dsh reaches stable or volume justifies it.
