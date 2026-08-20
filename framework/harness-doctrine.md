# Harness Doctrine

> Canonical. Any harness proposed for any Centaurion project is graded on these four properties.

A harness is fit for any of the three projects only if it has all four properties:

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

## Ordering

Revert what you can → audit what you can't revert → heal from what you audited → evolve from what you healed.

## Scoring

Any harness/tool proposed for any project is graded on these four properties **in addition to** Gate 0 + the four gates (Fit, Cost, Risk, Opportunity).
