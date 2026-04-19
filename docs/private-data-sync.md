# Private Data Sync — Layer 5

How Centaurion keeps personal operator data out of the public repo while still giving you multi-machine git access to it.

## Architecture

```
┌──────────────────────────────┐      ┌───────────────────────────────┐
│ MalikJPalamar/Centaurion     │      │ MalikJPalamar/centaurion-     │
│ (PUBLIC)                     │      │ private (PRIVATE)             │
│                              │      │                               │
│ Framework, skills, agents,   │      │ identity/BASELINE-*.md        │
│ workflows, public identity,  │      │ memory/state/baseline-*       │
│ deploy scripts               │      │ memory/state/onboarding-state │
│                              │      │ routing-adjustments.jsonl     │
└──────────┬───────────────────┘      └──────────┬────────────────────┘
           │ clone                                │ clone
           ▼                                      ▼
    ~/Centaurion  ◀─── sync-private.sh ───▶  ~/centaurion-private
```

Both repos clone to the same machine. A one-way sync script copies gitignored personal files from the public checkout into the private one, commits, and pushes — never the other direction (the private repo is source of truth for its files).

Cortex reads **both** paths via the local filesystem. The two repos are not submodules; they are independent git histories on different visibility boundaries.

## Setup on a New Machine

```bash
# Public repo (already standard)
git clone https://github.com/MalikJPalamar/Centaurion.git ~/Centaurion

# Private companion (requires token with repo scope)
git clone git@github.com:MalikJPalamar/centaurion-private.git ~/centaurion-private

# Wire them together — restores local gitignored personal files
cp ~/centaurion-private/identity/BASELINE-INTEGRAL.md  ~/Centaurion/identity/ 2>/dev/null
cp ~/centaurion-private/memory/state/baseline-*       ~/Centaurion/memory/state/ 2>/dev/null
cp ~/centaurion-private/memory/state/onboarding-state.json ~/Centaurion/memory/state/ 2>/dev/null
```

After this, `cd ~/Centaurion && claude` sees the personal files via the public checkout — same as if onboarding had just run here.

## Ongoing Sync

After any baseline write / onboarding event / routing adjustment:

```bash
bash ~/Centaurion/deploy/vps1/sync-private.sh
```

Or cron it:
```cron
# Every day at 21:00 UTC, sync personal data to private repo
0 21 * * * cd ~/Centaurion && bash deploy/vps1/sync-private.sh >> ~/Centaurion/logs/sync-private.log 2>&1
```

## What Gets Synced

The sync script has an explicit allow-list of paths — additions go in `deploy/vps1/sync-private.sh` `PATHS` array. Current set:

| Path | Contents |
|---|---|
| `identity/BASELINE-INTEGRAL.md` | Scored AQAL+ILP baseline |
| `memory/state/baseline-light-in-progress.md` | Raw Light responses |
| `memory/state/baseline-deep-in-progress.md` | Raw Deep responses |
| `memory/state/onboarding-state.json` | Per-operator sentinel |
| `memory/state/routing-adjustments.jsonl` | Baseline-driven gate tweaks |
| `memory/state/autoresearch-ur-protocol-results.md` | UR Protocol research output |
| `memory/state/autoresearch-spof-mitigation-results.md` | SPOF research output |

## Safety Guards

The script refuses to run if:
- Public repo not found at `$CENTAURION_REPO`
- Private repo not found at `$PRIVATE_DIR`
- Private repo's `origin` points at the PUBLIC repo (prevents catastrophic cross-repo push)

## Why Not Submodules?

A git submodule would tie the private repo's commit SHA into the public repo's history — exposing existence + timestamps of personal writes. Separate independent repos keep visibility boundaries clean.

## Why Not Syncthing?

Syncthing is still useful for **VPS-to-VPS** sync of working state (logs, caches). The private repo pattern is specifically for **versioned history of personal data with git semantics** (blame, revert, branch per operator on multi-operator deploys).
