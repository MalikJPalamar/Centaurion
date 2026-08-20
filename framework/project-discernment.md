# Project Discernment Doctrine

> Canonical. Three production systems, same shape, different products. They share a doctrine, never a core runtime.

## The Three Projects

| Project | Produces | Input | Current state |
|---|---|---|---|
| **Dark Factory** | Verified software (spec → PR, 2 human touches) | Approved OpenSpec change | docs/factory/PRD.md, P0' in progress |
| **Cognitive Company** | Business operations under human priors | Priors + signals | Framework live in this repo; infrastructure = WO-001..023, built BY the factory |
| **GTM Harness** | Demand: campaigns, nurture, pipeline | Offer + audience | Greenfield. Seed = 3 strip-mined GTM skills (Twenty client, Mautic nurture, GTM sequence engine). Spike = WO-024 |

## Dependency Law

Factory builds the other two. Company operates all three. GTM funds them.

## Anti-Conflation Rules (hard)

- **R1.** No single runtime serves two projects' cores. (The claudeclaw fork violated this and was archived.)
- **R2.** Anything shared lives canonical and runtime-agnostic: skills in `~/.claude/skills/` + this repo, specs in `openspec/`, doctrine in `framework/`. Runtimes are disposable bodies.
- **R3.** Cross-project traffic moves through canonical artifacts (specs, Issues, wikis) — never runtime-to-runtime side channels.
