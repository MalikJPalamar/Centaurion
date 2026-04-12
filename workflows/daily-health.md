---
on:
  schedule: daily
permissions:
  contents: read
  issues: read
safe-outputs:
  create-issue:
    title-prefix: "[centaurion-health] "
    labels: [report, daily]
    close-older-issues: true
---

# Daily Centaurion Health Check

L3 sensing — environmental tripwires and system health monitoring. Creates a GitHub Issue that Malik reads on his phone each morning.

## Checks to Perform

### System Health
- VPS 1 uptime and Docker container status
- VPS 2 uptime and Agent Zero accessibility
- OpenClaw running status (Telegram responsiveness)
- Syncthing sync status (any conflicts or failures?)
- API key expiration warnings

### Memory Health
- Supermemory: tokens used vs. free tier limit (1M)
- Supermemory: distribution across venture containers
- Wiki repos: last commit date per repo (stale if > 7 days)
- Any routing classification logs since last check

### SA Scan Summary
- Run SA scan across tracked tickers (see `skills/sa-scan/SKILL.md`)
- Highlight any threshold breaches or notable patterns
- Flag any tickers requiring attention

### Routing Accuracy
- Review routing decisions from the past 24 hours
- Flag any misclassifications (from outcome data if available)
- Note current threshold settings

## Output Format

GitHub Issue titled: `[centaurion-health] {date}`

```markdown
## System Status
| Component | Status | Notes |
|-----------|--------|-------|
| VPS 1 | ✅/⚠️/❌ | ... |
| VPS 2 | ✅/⚠️/❌ | ... |
| OpenClaw | ✅/⚠️/❌ | ... |
| Syncthing | ✅/⚠️/❌ | ... |

## Memory
- Supermemory: X/1M tokens used
- Wikis: aob (last: date), builderbee (last: date), centaurion (last: date)

## SA Scan
[Summary table or "No alerts"]

## Routing (24h)
- Decisions: X total, Y autonomous, Z surfaced
- Accuracy: X% (if outcome data available)

## Action Items
- [ ] [Any items requiring Malik's attention]
```
