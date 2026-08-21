# Orchestrator Post-Mortem — centaurion.me build

**~200 words on what the swarm decided, what it cut, and what it would do differently.**

---

The swarm gated on Section 14 first: a one-paragraph statement of what
*category-defining* meant for centaurion.me, sent for approval before any
agent was assigned. After approval, the orchestrator collapsed the seven
mandated roles into sequenced passes — Architect → Copy → Visual Systems →
Frontend → Motion → QA → Deployment — with each pass declaring its plan in
its artifact header and writing only its scoped deliverable. Two automated
audit gates (`audit:words`, `audit:hex`) were built early and used as
build-blocking checks, catching one substring-overlap on "transformation" in
quoted critique copy and one false-positive on `text-transform` in SVG markup.
Both were resolved cleanly.

Cuts: the optional WebGL particle hero was deferred (could not guarantee
≤80KB plus `client:idle`); fonts ship from Google Fonts in build #1 with a
self-host pass slated as the first post-deploy follow-up; the Method PDF gate
returns a 200 stub, not an actual PDF — copy was treated as the deliverable,
not document production.

With more compute: a real Lighthouse CI run against a preview deploy would
have replaced "engineered-in" with "measured." The Friston citation paragraph
on `/method` should be sharpened by a domain reviewer. The SVG diagrams are
intentionally restrained but a second visual pass could find more compression.
