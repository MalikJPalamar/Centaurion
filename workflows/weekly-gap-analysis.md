---
on:
  schedule: weekly
permissions:
  contents: read
  issues: read
safe-outputs:
  create-issue:
    title-prefix: "[gap-analysis] "
    labels: [research, weekly]
    close-older-issues: true
---

# Weekly Knowledge Gap Analysis

L4 sensing element — run InfraNodus gap analysis on all three wiki repos. Identify disconnected clusters, generate research questions that bridge gaps, and add to wiki todo lists.

## Procedure

### 1. Wiki Health Check
For each wiki (aob-wiki, builderbee-wiki, centaurion-wiki):
- Count total pages
- Identify pages not updated in > 14 days
- List topics from recent work that have NO corresponding wiki page

### 2. Topology Analysis
Using InfraNodus (when connected) or manual content review:
- What are the main topic clusters in each wiki?
- Which clusters are disconnected (no links between them)?
- What bridge concepts could connect them?

### 3. Cross-Wiki Bridges
The highest-value gaps are between wikis:
- AOB operational knowledge ↔ BuilderBee client patterns
- BuilderBee GHL expertise ↔ AOB CRM migration
- Centaurion methodology ↔ both ventures' operational reality

### 4. Research Question Generation
For each gap, generate an actionable research question:
- Questions should be answerable through research or experimentation
- Prioritize questions that bridge ventures (highest compound value)

## Output Format

GitHub Issue titled: `[gap-analysis] Week of {date}`

```markdown
## Wiki Coverage
| Wiki | Pages | Stale (>14d) | Missing Topics |
|------|-------|-------------|----------------|
| aob-wiki | X | Y | [list] |
| builderbee-wiki | X | Y | [list] |
| centaurion-wiki | X | Y | [list] |

## Disconnected Clusters
- [Wiki]: [Cluster A] has no connection to [Cluster B]
  - Bridge concept: [suggestion]

## Cross-Wiki Opportunities
- [Opportunity description]

## Research Questions
- [ ] [Question 1] (bridges: wiki_a ↔ wiki_b)
- [ ] [Question 2]
- [ ] [Question 3]

## Recommended Wiki Updates
- [ ] Create page: [topic] in [wiki]
- [ ] Update page: [topic] in [wiki] (stale since [date])
```
