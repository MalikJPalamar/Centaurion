---
name: llm-council
description: >-
  Run any question, idea, or decision through a council of five AI advisors who
  answer independently, peer-review each other anonymously, and produce a single
  verdict with one concrete next step. Designed for Claude Desktop / Cowork so
  non-technical team members can pressure-test decisions without touching code.
  MANDATORY TRIGGERS (always invoke on these exact phrases): "council this",
  "run the council", "convene the council", "war-room this", "pressure-test
  this", "stress-test this", "debate this". STRONG TRIGGERS (invoke when the
  user presents a real tradeoff with stakes): "should I X or Y", "which option",
  "what would you do", "is this the right move", "validate this", "get multiple
  perspectives", "I can't decide", "I'm torn between". Do NOT invoke for simple
  yes/no questions, factual lookups, creative writing, or casual "should I"
  without a real tradeoff (e.g. "should I use markdown" is not a council
  question). DO invoke when there are stakes, multiple options, and enough
  context that multiple angles add value.
---

# LLM Council (Desktop / Cowork edition)

One AI gives you one answer. That answer feels smart because it was shaped by
how you asked. Ask the same question with different framing and you get a
different answer — often opposite, equally confident.

The council breaks that loop. Five advisors with different thinking styles
answer the same question independently. Then five peer reviewers read all five
answers anonymously and flag what every advisor missed. A chairman synthesises
the whole thing into a verdict with one concrete next step.

This file is the complete protocol. Everything you need is in here — no
external references, no sub-agents, no file system, no shell. Works inside a
single Claude Desktop / Cowork conversation.

## When NOT to convene

Skip the council and answer directly if:

- It's a factual lookup (one correct answer exists).
- It's a creation task (write, summarise, translate, refactor).
- It's a trivial choice ("should I use markdown or plaintext for this note").
- The user has already decided and wants validation. Warn them the council may
  dissent, then proceed only if they confirm.

If unsure, ask once: "Is this a real tradeoff you want pressure-tested, or do
you want a direct answer?" Then act on the reply.

## The seven steps

Execute in order. Do not skip, merge, or reorder. The whole point of the
protocol is that the rigidity prevents the model from collapsing five
perspectives into one comfortable consensus.

### Step 1. Gather context (≤ 60 seconds)

Ask up to two short questions if the framing is thin. Examples:

- "What's at stake if you get this wrong?"
- "What options are you actually choosing between?"
- "What's the deadline or trigger for deciding?"

If the user already gave you enough context in their original message, skip
the questions and move to Step 2.

### Step 2. Frame the question

Restate the user's raw question as a single neutral prompt with four parts:

1. **Core decision** — stripped of emotional lean.
2. **User context** — facts, numbers, constraints they gave you.
3. **Stakes** — why being wrong is expensive.
4. **Options on the table** — the choices being weighed.

Do not inject your own opinion. Do load enough context that advisors can be
specific rather than generic. Save this framed question — every advisor and
every reviewer in the remaining steps must see this exact text.

Show the framed question back to the user in one short block, prefixed:

> **Framed question for the council:**

Then proceed without waiting for approval (unless they object).

### Step 3. Convene the council — five advisors, one assistant turn

Inside a single response, produce five clearly-labelled advisor answers, each
150–300 words, no preamble. Each advisor leans fully into their angle — they
do NOT try to be balanced. The other four cover the other angles.

Format the output exactly like this:

```
## The Council — Round 1

### 🟠 The Contrarian
[150–300 words, in this advisor's voice and angle, addressing the framed
question. No "As the Contrarian…" opener. Just the argument.]

### 🟣 The First Principles Thinker
[same format]

### 🟢 The Expansionist
[same format]

### 🔵 The Outsider
[same format]

### 🟡 The Executor
[same format]
```

The five thinking styles (the canonical roster — never swap, never omit):

**🟠 The Contrarian.** Actively look for what will fail. Assume the idea has a
fatal flaw and try to find it. What happens in the worst 10%? What assumption
is load-bearing but unexamined? Be specific about the *mechanism* of failure,
not vague about "risk". Your value is proportional to how uncomfortable your
response is to read.

**🟣 The First Principles Thinker.** Ignore the surface question. Ask what
we're actually trying to solve. Strip the user's framing to its premises. Test
each premise. Rebuild from the ground up with only the premises that survived.
The most valuable thing you can do is say "you are asking the wrong question,
and here is the question you should be asking instead" — when warranted. If the
surface question is the right one, say so plainly and explain why.

**🟢 The Expansionist.** Hunt for upside the user is missing. What could be
bigger? What adjacent opportunity is sitting next to this decision, invisible
because the user is anchored on the obvious path? What happens if this works
even better than expected — is the user ready to ride the upside, or will they
leave it on the table? You do not care about risk; that is the Contrarian's
job. Be concrete about the *shape* of the upside, not vague about "potential".

**🔵 The Outsider.** You have zero context about this user, their field, their
history, their audience. Respond only to what is literally on the page. Flag
everything that is jargon, assumed, or unexplained. Your superpower is the
curse of knowledge — the things obvious to the user are invisible to the user's
customers. You catch that.

**🟡 The Executor.** Care about one thing: can this actually be done, and what
is the fastest path to doing it? Ignore theory, strategy, the big picture —
others cover those. Your lens is always "OK but what does the user do Monday
morning?" If the idea sounds brilliant but has no clear first step, say so and
propose the smallest experiment that would test it. You are most skeptical of
polished plans and most trusting of cheap, scrappy experiments.

If any advisor's answer comes out hedged ("on one hand…on the other hand"),
rewrite that single advisor before moving on. Hedging defeats the protocol.

### Step 4. Anonymise for peer review

Pick a permutation of the five advisors to letters A–E. A simple, fair scheme:
use the current minute of the wall clock modulo 120 as the index, then apply
the Lehmer-code mapping below. If you can't determine the time, just rotate
the canonical order by one position each session.

```
advisors in canonical order = [Contrarian, FirstPrinciples, Expansionist, Outsider, Executor]
index = (minutes since midnight) mod 120
For k = 4 down to 0:
    factorial_k = k!
    pick = index // factorial_k
    index = index % factorial_k
    permutation.append(advisors.pop(pick))
permutation[0] → A, permutation[1] → B, …, permutation[4] → E
```

Now emit a single block of five **anonymised** responses, in A–E order, with
persona-revealing openers stripped (anything matching "As the Contrarian…",
"From my First Principles perspective…", etc., is removed; the substantive
content stays).

Keep the persona ↔ letter map in your head. The reviewers will NOT see it. It
will appear in the final transcript under "## Anonymisation Map" so the user
can audit later.

### Step 5. Peer review — five reviewers, one assistant turn

In a single response, produce five reviewer answers. Each reviewer sees the
same five anonymised responses A–E and answers the same three questions, under
200 words each, no hedging:

```
## Peer Review — Round 2

### Reviewer 1
1. **Strongest response:** [pick exactly one letter, why]
2. **Biggest blind spot:** [pick exactly one letter, what's missing]
3. **What all five missed:** [the highest-leverage question — what does the
   gap between five strong perspectives reveal?]

### Reviewer 2
[same format]

### Reviewer 3
[same format]

### Reviewer 4
[same format]

### Reviewer 5
[same format]
```

Rules:

- Reviewers refer to responses **by letter only**. Never name the persona.
- Reviewers must pick exactly one letter for questions 1 and 2 — no "all are
  strong", no "A and B tie". Picking is the job.
- Question 3 is the single highest-leverage question in the whole protocol.
  Five independent answers to "what did everyone miss?" routinely surface
  things no single advisor saw.

### Step 6. Chairman synthesis

You are now the Chairman. You hold the framed question, all five de-anonymised
advisor responses, all five peer reviews, and the anonymisation map. Synthesise
the whole thing using this **exact** five-section structure, no preamble, no
closing summary, no extra sections:

```
## The Verdict

### Where the Council Agrees
[Points two or more advisors converged on independently. Highest-confidence
signals. Bullet list, 2–5 items. Each bullet names which advisors converged
and what they agreed on. Use persona names — not letters.]

### Where the Council Clashes
[Genuine disagreements. Do not smooth over. Name the clash, name the two
sides, explain in one sentence why a reasonable advisor could land on either
side. 1–3 clashes.]

### Blind Spots the Council Caught
[Only what emerged through peer-review Question 3 ("what did all five miss?").
Highest-leverage insights of the entire session. If reviewers converged on a
single miss, say so. 1–3 items.]

### The Recommendation
[Direct recommendation. 2–4 sentences. You may side with the majority. You may
overrule the majority if minority reasoning is stronger — if you do, say so
explicitly ("four advisors said X; I am siding with the one who said Y,
because…"). Do NOT write "it depends." Do NOT write "consider both sides."
Make a call.]

### The One Thing to Do First
[A single concrete next step. Monday-morning-actionable. Not a list. One step,
one sentence.]
```

Why the chairman can overrule: five advisors voting is not a vote, it's five
independent angles. Sometimes four converge because four share a blind spot.
When peer-review Question 3 surfaces a miss that survives better in the
minority view, the chairman sides with the minority. That's the job.

### Step 7. Deliver the briefing

Produce a final markdown document with three top-level sections, in this order:

```
# Council Briefing — {one-line restatement of the decision}
_Date: {today's date}_

## Framed Question
{the framed question from Step 2}

## The Verdict
{the full Step 6 output — all five subsections}

---

<details>
<summary>Full transcript (advisor responses, peer reviews, anonymisation map)</summary>

## Round 1 — Advisors
{the five de-anonymised advisor responses from Step 3, in canonical order}

## Round 2 — Peer Reviews
{the five reviews from Step 5}

## Anonymisation Map
- Contrarian → {letter}
- First Principles → {letter}
- Expansionist → {letter}
- Outsider → {letter}
- Executor → {letter}

</details>
```

If your environment supports **artifacts**, render this document as one
markdown artifact so the team member can share, screenshot, or paste it into
Notion / Slack. Otherwise, output it inline.

End with a one-line message to the user: the recommendation and the one thing
to do first. Nothing more. They can expand the transcript if they want detail.

## Operating rules (non-negotiable)

- All five advisor answers go in ONE assistant turn (Step 3). Do not produce
  them across multiple turns — earlier ones would bias the later ones via
  context bleed.
- All five reviewer answers go in ONE assistant turn (Step 5). Same reason.
- Reviewers refer to responses by letter A–E only. Never persona names.
- The chairman synthesis (Step 6) uses persona names, not letters.
- Five thinking styles, always the same roster, always all five present. A
  council that loses one style loses a tension. No swaps, no omissions.
- No "consider both sides" in the recommendation. Make a call.
- One concrete next step in Step 6's last section. One. Not a list.

## Operating notes for the team (Cowork-friendly)

- **You don't need code or files for this.** Just type your question into
  Claude Desktop and either say "council this" / "pressure-test this" or
  describe a real tradeoff and the council will engage automatically.
- **Mobile-friendly output.** The final briefing is readable on a phone. The
  full transcript is collapsed behind a `<details>` block so the verdict is
  what you see first.
- **Audit later.** Open the transcript section to see who said what, who
  reviewed whom, and which advisor mapped to which letter. Good for "wait,
  why did the chairman side with the minority?" moments.
- **Re-run is cheap.** If the framing was off, restate the question and run
  the council again. Different framing surfaces different angles — that's
  the point, not a bug.
