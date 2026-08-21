# Oracle Registry

> Canonical. Maps claim types to their deterministic verification oracles. Logging is not validation (Doctrine property 5: VERIFIABLE).

## Claim Types

Every material claim emitted by any agent must be typed. An untyped claim is UNVERIFIABLE by definition.

| Claim type | Oracle | Mechanism | Notes |
|---|---|---|---|
| `code` | tests/gates exit-0 + `/opsx:verify` | Run test suite, check gate exit code | Deterministic. Zero ambiguity. |
| `financial` | Stripe API reconcile | Compare claimed amount/state against Stripe API response | No financial claim accepted without Stripe confirmation |
| `cash` | Stripe balances + invoices reconcile | Balance/invoice read-back vs claim | Same API, different endpoints |
| `customer` | Twenty API reconcile | Compare claimed contact/pipeline state against Twenty GraphQL | Source of truth for contacts |
| `pipeline` | Twenty pipeline-stage reconcile | Stage transitions verified against Twenty API | |
| `marketing` | Mautic API state check | Campaign/segment/contact state verified against Mautic REST API | Acceptance checks + API state |
| `retrieval` | Canonical citation resolves | Every retrieval claim must cite a canonical source; citation is verified to exist and contain the claimed content | |
| `ops` | Three-state connector probe | Probe returns `connected`, `not_configured`, or `error` | Adopted from FounderOS (WO-023) |
| `schedule` | Calendar/cron state read-back | Verify claimed schedule exists in Google Calendar or cron registry | |
| `content` | Acceptance checks (brand-voice, format) | Deterministic format/structure checks; brand-voice is smell-test tier, not oracle | |
| `ui` | Visual VERDICT (A2) | Screenshot comparison or accessibility check | |

## Rules

1. **Oracle-first.** Prefer deterministic oracles (API reconcile, exit codes, file existence) over LLM judgment. LLM-reviews-LLM is a smell test, not an oracle.
2. **UNVERIFIABLE is a flag, not a pass.** Claims that cannot be oracle-checked are logged as UNVERIFIABLE and surfaced on /doctor. They are never silently accepted as true.
3. **Gate 2 requires PASS.** Any WO whose completion claim lacks a PASS oracle entry in the claim ledger cannot reach Gate 2.
4. **R4 binding.** No business function goes live without its oracle (Blueprint §2 rule).

## Ledger Format

Append-only JSONL in `logs/claims/` (Tier-3 evidence, NOT canonical wikis):

```json
{"ts": "...", "agent": "cortex", "wo": "WO-026", "claim_type": "financial", "claim": "Stripe MRR is $4200", "oracle": "stripe_api_reconcile", "result": "PASS", "evidence_uri": "logs/claims/evidence/2026-08-20-stripe-mrr.json"}
```

Results: `PASS` | `FAIL` | `UNVERIFIABLE`

## Surfaces

- `/doctor` -- live pass-rate per agent
- `/analytics` -- trend over time
- Weekly compaction distills notable FAILs into canonical RCA notes (feeds Doctrine property 3: SELF-HEALING)
