# ROADMAP — Centaurion

## Phase 1: Core Loop (current)
> "Does the exo-cortex skeleton work?"

- [ ] All v0.1 requirements pass verification (R1-R10)
- [ ] Verification script runs green
- [ ] CLAUDE.md produces correct agent behavior when opened in Claude Code

**Definition of Done:** `tests/verify-core-loop.sh` exits 0. All 10 requirement groups pass.

## Phase 2: Memory Integration
> "Can the exo-cortex remember?"

- [ ] Supermemory plugin installed and connected
- [ ] centaurion-wiki repo created and populated with framework content
- [ ] Supermemory auto-capture working in Claude Code sessions
- [ ] Wiki content accessible via agent recall

**Definition of Done:** Agent can answer "What did we discuss yesterday?" using Supermemory recall.

## Phase 3: Multi-Runtime Deployment
> "Can other agents run the same loop?"

- [ ] Nova personality loaded on OpenClaw (VPS 1)
- [ ] Pi scaffold sharing Centaurion skills (VPS 1)
- [ ] Agent Zero configured with Centaurion context (VPS 2)
- [ ] Syncthing running between VPSs

**Definition of Done:** Nova on OpenClaw responds to a Telegram message using Centaurion identity.

## Phase 4: Feedback Loops
> "Does the system improve itself?"

- [ ] Daily health check creating GitHub Issues
- [ ] Weekly gap analysis running
- [ ] Routing accuracy tracked and thresholds adjustable
- [ ] Ratings captured and trending

**Definition of Done:** Weekly review Issue shows measurable trend data.

## Phase 5: Knowledge Graph (Month 2)
> "Does the system track how knowledge evolves?"

- [ ] Neo4j deployed on VPS 1
- [ ] Graphiti connected via MCP
- [ ] Temporal entity tracking live
- [ ] All three wiki repos with InfraNodus gap analysis

**Definition of Done:** Agent answers "When did we decide to migrate from Ontraport?" from Graphiti.
