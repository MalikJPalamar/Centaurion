# Centaurion — Positioning & GTM Brief (roxx.ai input)

> **Purpose:** Raw material to feed into [roxx.ai](https://roxx.ai) — the AI positioning/GTM tool — to generate Centaurion's positioning, messaging, and a draft landing page. roxx.ai's flow starts from a one-sentence product description and builds outward, so this brief leads with that sentence and then supplies the angle, audience, differentiation, objections, and proof it needs.
>
> **Note:** roxx.ai is a *positioning/messaging* tool, not a build partner. This brief is written to make the product *sell-able*, not to scope engineering. (Engineering scope lives in `centaurion-product-description.md`.)

---

## 1. One-sentence description (the roxx.ai seed)

> **Centaurion is an AI agent framework for a single operator running multiple businesses: it processes each task through a fixed sequence, auto-executes low-risk tasks, escalates high-risk ones for user approval, and stores context across sessions.**

Plain-language variants to test:
- "Software framework that runs an AI agent to handle recurring operational tasks across several businesses for one user, with approval gating on high-risk actions."
- "AI agent system for managing multiple businesses: automated task execution, rule-based escalation to the user, and persistent memory across sessions."

**What it is, factually:** a set of structured Markdown/JSON instruction files that run inside the Claude Code agent environment, plus a prototype web dashboard (React front end, FastAPI back end). It is a configuration/instruction layer plus supporting scripts, not a packaged SaaS product.

**What it does:** runs each task through a seven-step sequence (load context → propose approach → assess → classify → execute → evaluate → record); classifies tasks by novelty, stakes, and reversibility to decide auto-execute vs. escalate; writes each interaction to memory so context persists.

**Main components:** session-loaded user/business config; the task-sequence and escalation rule set (thresholds adjust on 1–5 user ratings); a library of 11 skill modules; Supermemory integration (live, per-business); JSONL logs of classifications and ratings; scheduled runs via GitHub Actions/VPS; a prototype review dashboard (mock data).

**Status:** single user; the task sequence and memory-write are enforced by instruction, not code; the dashboard and several memory layers are prototype-stage.

---

## 2. Who it's for (target persona)

- **Primary:** The multi-venture solo operator / "company of one at scale" — a founder running 2–4 businesses simultaneously who is the bottleneck for every business.
- **Secondary:** Fractional executives, solopreneurs, and small founding teams drowning in cross-context switching.
- **Behavioral signature:** thinks in systems and metaphors, reviews work from a phone, wants to *direct and rate* rather than micromanage, distrusts AI that needs constant re-explaining.

---

## 3. The pain (what they feel)

- "I'm the bottleneck. Everything waits on me."
- "Context lives in my head; nothing compounds. Every AI session starts from zero."
- "AI assistants create *more* work — I have to babysit and re-review everything."
- "I can't tell what's safe to delegate vs. what genuinely needs me."

**Core tension to name:** building/doing is cheap now; *staying coordinated across ventures without becoming the single point of failure* is the unsolved problem.

---

## 4. Strongest angle (the wedge)

**"The human is the prior, not the bottleneck."**

Centaurion's whole design inverts the default AI-assistant relationship. Instead of you serving the AI prompts, the AI runs a disciplined loop on your behalf and **only interrupts you when a decision is genuinely novel, high-stakes, and hard to reverse** — surfaced as a ≤5-line, phone-readable card you can rate 1–5. Everything else it does autonomously and remembers forever.

Two ideas do the selling:
1. **The Routing Gate** — it knows when to act and when to ask (novelty × stakes × reversibility). This is the trust mechanism.
2. **Compounding memory** — every interaction makes the system smarter; you never re-explain context.

---

## 5. Differentiation (vs. the alternatives)

| Alternative | Why Centaurion is different |
|---|---|
| Generic AI chat (ChatGPT/Claude) | Stateless and reactive; you drive every step. Centaurion is stateful, proactive, and self-governing across sessions. |
| AI "assistants" / copilots | Built to help *inside one task/app*. Centaurion runs *across all your ventures* and decides what reaches you. |
| Agent frameworks / AutoGPT-style tools | Autonomy without judgment — they over-act or spin out. Centaurion gates autonomy by reversibility and learns thresholds from your ratings. |
| Hiring a chief-of-staff / VA | Expensive, needs onboarding, doesn't scale to 3 ventures. Centaurion calibrates to *you* (an integral baseline assessment) and works 24/7. |

**One-line moat:** it's the only one built on an explicit *human-as-prior + adaptive routing + mandatory memory* contract — trust and compounding are the product, not features.

---

## 6. Outcomes / value (what they get)

- Decisions stop queueing behind you; routine work runs without you.
- A single, phone-first review surface across every venture.
- Cross-venture insight (the highest-value output for a multi-business operator).
- A system that gets *more* useful the longer you use it, not noisier.

**Value frame (Precision Ratio):** more predictive order per unit of your time, money, and attention.

---

## 7. Objections to preempt

- *"Will it act without me on something it shouldn't?"* → The Routing Gate + escalation contract; high-stakes/irreversible work always surfaces.
- *"Another tool I have to babysit."* → It reviews itself and batches what reaches you; you rate, you don't manage.
- *"My context is too specific."* → It loads your identity every session and calibrates to you up front.
- *"Is my data safe across ventures?"* → Memory is scoped per venture (separate containers).

---

## 8. Proof & credibility (use honestly)

- Working active-inference loop + Three Laws encoded and running; live shared memory (Supermemory) round-trip verified.
- Real usage artifacts: routing log, weekly reviews, and a worked ExO 3.0 transformation applied to a live venture (AOB).
- **Honesty guardrail for GTM copy:** several components are prototype/planned (enforcement-by-convention, dashboards, the Daemon/coherence layer). Position around the *operating model and the trust contract* — which are real — not around an enterprise-grade platform that doesn't exist yet. Don't claim multi-tenant or "autonomous enterprise" capability.

---

## 9. Category / framing options to test in roxx.ai

- "Exo-cortex" (ownable, distinctive, needs explanation)
- "AI operating system for multi-venture founders" (clear, searchable)
- "Self-governing AI chief-of-staff" (familiar handle + the differentiator)

---

## 10. Suggested roxx.ai run

Paste §1 as the product sentence; pick the **"Developer Tool"** or **"Service / Agency"** example archetype as the closest starting template; then layer in §2 (persona), §4 (angle), and §5 (differentiation) when it asks for positioning inputs. Re-run after Malik confirms the AOB assumptions and once any prototype gap in §8 closes, since the honest claim set will widen.
