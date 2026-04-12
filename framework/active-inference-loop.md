# The Active Inference Loop

Centaurion's execution engine. Seven steps, mapped from PAI's Algorithm (Observe → Think → Plan → Build → Execute → Verify → Learn) and annotated with Active Inference semantics from Karl Friston's Free Energy Principle.

## The Loop

```
SENSE → PREDICT → COMPARE → ROUTE → ACT → OBSERVE OUTCOME → REMEMBER → (repeat)
```

---

## Step 1: SENSE (PAI: Observe)

> Load context. What do I know? What's changed?

**L0 Identity:** Load TELOS files — purpose, mission, goals, preferences, current priorities.
**Recent context:** Pull from Supermemory — what was the last conversation about? What was Malik working on?
**Active alerts:** Check L3 tripwires — any threshold breaches since last session?
**Task context:** Read the current request. What is being asked?

**Output:** A grounded understanding of who I am (Cortex/Nova/Daemon), what the human values, what's currently happening, and what's being asked.

**Failure mode:** Acting without context → generic responses that ignore Malik's ventures, preferences, or recent work. This violates the Hierarchy Law.

---

## Step 2: PREDICT (PAI: Think)

> Form a hypothesis. What's the best approach? How confident am I?

Based on the sensed context, generate a prediction:
- What approach will produce the best outcome?
- What does "good" look like for this task?
- What could go wrong?

**State your confidence.** "I'm 90% confident this is a routine GHL config task" vs. "I'm 40% confident — this touches the AOB membership migration which has unknowns."

**Output:** A stated hypothesis with confidence level. This is the prediction that will be tested against the outcome.

**Failure mode:** Acting without a prediction → no way to learn. If you don't predict the outcome, you can't measure prediction error, and the system doesn't improve.

---

## Step 3: COMPARE (PAI: Plan)

> Identify prediction error. What's unexpected about this task?

Compare the prediction to the actual task requirements:
- Is this task what I expected? Or is there something novel?
- Does my confidence match the actual complexity?
- Are there unknowns that my prediction didn't account for?

**Classify the prediction error:**
- **Low error** (routine): My model handles this well. Proceed.
- **Medium error** (complicated): I can handle this but should flag uncertainties.
- **High error** (complex/novel): My model is insufficient. This needs human input.

**Output:** An explicit classification of how well my current model fits this task.

**Failure mode:** Skipping comparison → no routing. The agent just acts, regardless of whether it should. This violates the Routing Law.

---

## Step 4: ROUTE (PAI: Build)

> Dispatch to the right substrate. Who should handle this?

Apply the Routing Gate:

| Novelty | Stakes | Reversibility | Route |
|---------|--------|---------------|-------|
| Low | Low | High | AI autonomous |
| Low | High | High | AI autonomous, flag for review |
| High | Low | High | AI autonomous, log for learning |
| High | High | Low | **STOP. Surface to Malik.** |
| Any | Any | Any (ambiguous) | Surface to Malik with context |

**If routed to AI:** Proceed to ACT with full context.
**If routed to human:** Present the task, the prediction, the classification, and a recommended action. Wait for Malik's direction. Do not auto-execute.

**Output:** A routing decision with justification.

**Failure mode:** Misrouting. Type 1: AI handles novel/high-stakes (false confidence). Type 2: Human gets routine tasks (wasted attention). Both reduce fitness.

---

## Step 5: ACT (PAI: Execute)

> Execute using the appropriate skill or tool.

Do the work. Use available skills, tools, and knowledge:
- Invoke relevant SKILL.md files
- Use memory (Supermemory recall, wiki lookup, Graphiti query)
- Apply venture-specific context (AOB vs. BuilderBee vs. Centaurion)
- Follow preferences (concise output, structured format, phone-readable)

**Output:** The completed work product.

**Failure mode:** Executing without routing → uncontrolled actions. Executing without identity → generic output that ignores context.

---

## Step 6: OBSERVE OUTCOME (PAI: Verify)

> Compare outcome to prediction. What's the delta?

After acting, assess:
- Did the outcome match my prediction?
- Was the routing decision correct?
- Did the human accept/revise/reject the output?
- What was the rating (if provided)?

**Calculate prediction error:**
- **Outcome matched prediction** → model is calibrated for this type of task.
- **Outcome was better than predicted** → model is too conservative. Adjust.
- **Outcome was worse than predicted** → model is too optimistic. Adjust.

**Output:** An explicit assessment of prediction accuracy for this task.

**Failure mode:** Not observing outcomes → no learning signal. The system stays static.

---

## Step 7: REMEMBER (PAI: Learn)

> Write learnings. Update the shared model.

Based on the outcome observation:
- **Supermemory:** Capture the interaction (auto-capture if enabled).
- **Wiki:** If new knowledge was generated, update the relevant wiki repo.
- **Graphiti:** If entity relationships changed, update the temporal graph (Month 2).
- **Ratings:** If Malik provided a rating, store in ratings tracking.
- **Routing adjustment:** If the routing was wrong, note the correction for threshold tuning.

**This step is mandatory.** Every cycle of the loop must leave the system smarter. If REMEMBER is skipped, the system doesn't compound, and fitness stagnates.

**Output:** Updated memory state. The system is now better prepared for the next cycle.

**Failure mode:** Skipping REMEMBER → the system never improves. This violates the Coupling Law (shared model state decays).

---

## Loop Properties

### Continuous, Not Sequential
The loop runs continuously. A single task may cycle through multiple times (SENSE a subtask, PREDICT, COMPARE, ROUTE, ACT, OBSERVE, REMEMBER, then SENSE the next subtask).

### Multi-Agent
Different agents may run different steps. Nova SENSEs (environmental scanning), Cortex PREDICTS and ROUTES (deep analysis), Daemon maintains the shared model (REMEMBER). The loop doesn't require a single agent.

### Async-Friendly
The loop doesn't require synchronous human interaction. Steps 1-5 can run autonomously for routine tasks. Steps 6-7 can capture outcome data asynchronously (Malik rates in the morning, data flows in). Only ROUTE step 4 requires synchronous human input, and only for high-novelty/high-stakes tasks.
