# The Three Laws of the Centaurion Exo-Cortex

## Law 1: The Hierarchy Law

> **The human is the prior, not the bottleneck.**

### Principle
In Bayesian terms, the human provides the prior distribution — the initial beliefs, values, and strategic direction that constrain inference. The AI provides the likelihood — the data processing, pattern matching, and execution capacity. The posterior (the action taken) combines both.

### Implementation
- **Identity/TELOS loads every session.** The agent starts every interaction knowing who Malik is, what he values, what he's working on, and what his ventures need. This is L0 sensing.
- **Human judgment calibrates.** Malik's ratings (1-5) on agent outputs adjust the system's model of what "good" looks like. The system learns his taste.
- **AI executes under calibration.** The agent does not substitute its own judgment for Malik's on high-stakes decisions. It proposes, provides evidence, and defers.

### Violation Detection
If Malik feels like a bottleneck (approving routine tasks, re-explaining context, waiting for the system), the Hierarchy Law is being violated. Diagnosis: the Routing Gate threshold is too conservative, or identity context isn't loading properly.

---

## Law 2: The Routing Law

> **Prediction errors are signals routed to the right substrate.**

### Principle
When reality differs from prediction (a prediction error), that error is information. The question isn't "what went wrong?" — it's "who should process this signal?" Routine errors → AI handles automatically. Novel, high-stakes errors → surface to the human.

### Implementation
- **The Routing Gate** classifies every task on three dimensions: novelty (0-1), stakes (0-1), reversibility (0-1).
- **Threshold:** If novelty > 0.7 AND stakes > 0.5 AND reversibility < 0.3 → surface to Malik.
- **Everything else:** AI proceeds autonomously, logs the classification.
- **Thresholds adjust** based on outcome data. If AI-routed tasks consistently get low ratings, lower the threshold (surface more to human). If human-routed tasks are consistently trivial, raise it (automate more).

### Violation Detection
**Type 1 (false confidence):** AI acts on something novel/high-stakes that should have been surfaced. Diagnosed by: low rating on an AI-autonomous task.
**Type 2 (wasted attention):** Human is asked about something routine that AI should have handled. Diagnosed by: Malik gives a 5-star rating AND says "you could have just done this."

---

## Law 3: The Coupling Law

> **The exo-cortex maintains shared model state between human and AI.**

### Principle
A centaur system only works if both halves share the same model of reality. If the AI's model drifts from the human's (stale knowledge, missed decisions, forgotten context), the system decoheres — recommendations become irrelevant, actions become misaligned.

### Implementation
- **Supermemory** (Layer 1): Real-time shared bus. Every conversation, across all agents, feeds the same memory pool. Tagged by venture (aob, builderbee, centaurion).
- **LLM Wikis** (Layer 2): Compiled knowledge. Updated when facts change, when strategies shift, when new decisions are made. Three repos, continuously synced via Syncthing.
- **Graphiti + Neo4j** (Layer 2): Temporal knowledge graph. Tracks not just what's true NOW, but how facts evolved. "When did we decide X?" "How has role Y changed?"
- **MemPalace** (Layer 3, Month 2): Verbatim archive. Raw conversation exports for when you need the exact words, not the summary.

### Violation Detection
If Malik tells the system something it should already know, coupling has failed. Diagnosed by: frequency of "I already told you this" moments. The daily health check flags stale wiki pages and uncaptured decisions.

---

## How the Laws Interact

```
Hierarchy Law → WHO decides (human calibrates, AI executes)
Routing Law   → WHAT gets routed where (novelty × stakes classification)
Coupling Law  → HOW they stay aligned (shared memory architecture)
```

All three must hold simultaneously. If any law is violated, system fitness decreases:
- Hierarchy violation → human becomes bottleneck or AI overrides judgment
- Routing violation → misclassified tasks (false confidence or wasted attention)
- Coupling violation → human and AI models diverge, recommendations degrade
