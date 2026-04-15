---
name: sa-scan
description: Situational Awareness stock scan for 18 tracked tickers. USE WHEN running the daily SA scan or when Malik asks for market status.
---

# SA Scan — Situational Awareness Lens

## Purpose

Run the daily Situational Awareness stock scan across 18 tracked tickers. Detect threshold breaches, volume anomalies, and sector patterns. Route signals appropriately.

## Reference

This skill interfaces with the `MalikJPalamar/situational-awareness-lens` repository, which contains the scan configuration and historical data.

## Tickers

The 18 tickers tracked by the SA Lens (refer to the situational-awareness-lens repo for the current list and thresholds).

## Procedure

### 1. Run Scan
- Pull current price data for all 18 tickers
- Compare against defined thresholds (price levels, % change, volume)
- Identify sector patterns (are multiple tickers in a sector moving together?)

### 2. Classify Signals
For each ticker with activity:
- **Routine:** Within normal range, no threshold breach → Log, don't alert
- **Notable:** Approaching threshold or unusual volume → Include in daily summary
- **Alert:** Threshold breached → Immediate notification via L3 tripwire

### 3. Pattern Detection
- **Sector correlation:** Multiple tickers moving together suggests macro event
- **Divergence:** Ticker moving against sector suggests company-specific event
- **Volume anomaly:** Unusual volume without price movement suggests accumulation/distribution

### 4. Output

**Daily summary** (part of daily health check):
```markdown
## SA Scan — {date}
| Ticker | Price | Change | Volume | Signal |
|--------|-------|--------|--------|--------|
| ... | ... | ... | ... | routine/notable/alert |

### Patterns Detected
- [Any sector correlations, divergences, or volume anomalies]

### Alerts
- [Any threshold breaches requiring attention]
```

**Immediate alerts** (if threshold breached):
Route to Malik via Telegram (Nova) with: ticker, current price, threshold breached, recommended action.

## Example

For example, if NVDA drops 8% on high volume while other semiconductor tickers (AMD, TSM) hold steady, this is a divergence signal — company-specific event, not macro. Classify as **Alert**, route to Malik with: "NVDA -8% on 2.3x avg volume, sector stable. Likely company-specific. Review position."

## Frequency

Daily. Integrated into the `workflows/daily-health.md` workflow.
