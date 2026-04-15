---
name: gap-analysis
description: Knowledge gap analysis using InfraNodus topology on wiki repos. USE WHEN running the weekly/monthly gap analysis or when Malik asks "what are we missing?"
---

# Gap Analysis — Knowledge Topology

## Purpose

Analyze the three LLM Wiki repos (aob-wiki, builderbee-wiki, centaurion-wiki) for knowledge gaps, disconnected clusters, and unexplored connections. This is L4 sensing — the highest-level review of what the system knows and what it's missing.

## Prerequisites

- InfraNodus MCP server connected (or InfraNodus skill installed)
- At least one wiki repo with content to analyze
- Wiki repos: `MalikJPalamar/aob-wiki`, `MalikJPalamar/builderbee-wiki`, `MalikJPalamar/centaurion-wiki`

## Procedure

### 1. Load Wiki Content
Pull current content from all three wiki repos. Identify:
- Total pages per wiki
- Last updated dates
- Topic coverage (what subjects have pages?)

### 2. Run Gap Analysis
Using InfraNodus (or manual analysis if MCP not yet connected):
- **Cluster detection:** What are the main topic clusters in each wiki?
- **Disconnected clusters:** Which clusters have no links between them?
- **Bridge opportunities:** What concepts COULD connect disconnected clusters?
- **Missing topics:** Based on identity/GOALS.md and recent work, what topics SHOULD have wiki pages but don't?

### 3. Cross-Wiki Analysis
The highest-value gaps are often BETWEEN wikis:
- Does AOB knowledge about community management apply to BuilderBee client retention?
- Does BuilderBee's GHL expertise apply to AOB's CRM migration?
- Does Centaurion's framework methodology apply to how AOB structures its facilitator program?

### 4. Generate Research Questions
For each identified gap, generate a research question:
- "How does [concept from wiki A] relate to [concept from wiki B]?"
- "What would happen if we applied [AOB pattern] to [BuilderBee problem]?"
- "What's the relationship between [disconnected cluster 1] and [disconnected cluster 2]?"

### 5. Output

**Weekly format** (GitHub Issue: `[gap-analysis] Week of {date}`):
```markdown
## Knowledge Coverage
| Wiki | Pages | Last Updated | Coverage Score |
|------|-------|-------------|----------------|
| aob-wiki | X | date | X% |
| builderbee-wiki | X | date | X% |
| centaurion-wiki | X | date | X% |

## Gaps Identified
1. [Gap description + why it matters]
2. [Gap description + why it matters]

## Cross-Wiki Connections
- [Potential bridge between wikis]

## Research Questions Generated
- [ ] [Question 1]
- [ ] [Question 2]
- [ ] [Question 3]

## Recommended Actions
- [Specific wiki pages to create or update]
```

## Example

For example, gap analysis might reveal that the AOB wiki has a "facilitator onboarding" cluster and BuilderBee wiki has a "client onboarding" cluster, but they are disconnected. The bridge question: "Can the facilitator onboarding checklist pattern be reused for BuilderBee client onboarding?" — creating a cross-venture template.

## Frequency

Weekly (automated via gh-aw). Monthly deep analysis as part of L4 closed-loop review.
