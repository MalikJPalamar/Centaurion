# Markov Blanket

A Markov blanket defines the boundary between a system and its environment — the minimal set of variables that separates internal states from external states. In Active Inference, every persistent agent maintains a Markov blanket.

## In Centaurion

The exo-cortex's Markov blanket is the interface between Malik's cognition and the external world. It consists of:

### Sensory States (inbound)
- Notifications, emails, Slack messages
- Market data, analytics dashboards
- Client feedback, team updates
- The [Five Sensing Layers](five-sensing-layers.md) formalize these inputs

### Active States (outbound)
- Decisions communicated to teams
- Content published, code deployed
- Messages sent, meetings scheduled
- The [Active Inference Loop](active-inference-loop.md) governs these outputs

### Internal States (hidden)
- Malik's mental models, intuitions, preferences
- Captured in `identity/` files and Supermemory
- The [Three Laws](three-laws.md) protect these from being overridden by AI

## Why It Matters

The Markov blanket concept explains **what the exo-cortex actually is**: an extension of the blanket. Centaurion doesn't replace Malik's boundary with the world — it widens it. More sensory states are monitored, more active states are available, and internal states are better preserved across time.

## The Precision Connection

The [Precision Ratio](precision-ratio.md) measures blanket quality:
- **High precision** = the blanket filters signal from noise effectively
- **Low precision** = the blanket lets too much noise through (information overload) or blocks too much signal (blind spots)

## Related

- [Five Sensing Layers](five-sensing-layers.md) — The sensory side of the blanket
- [Active Inference Loop](active-inference-loop.md) — How the blanket processes information
- [Precision Ratio](precision-ratio.md) — How blanket quality is measured
