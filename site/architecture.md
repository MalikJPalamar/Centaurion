# Centaurion.me — Architecture

**Author:** Information Architect (orchestrator)
**Status:** Authoritative. Downstream agents must not deviate without orchestrator approval.
**Date:** 2026-04-27

---

## 1. Repository decision

The site lives at `/site/` inside the existing `MalikJPalamar/Centaurion` monorepo (working directory `/home/user/Centaurion`). Rationale:

- The brand canon, identity files, and framework definitions already live in this repo. A separate `centaurion-site` repo would force a sync surface and duplicate the source of truth for the Three Laws / 11 Levels / Equation copy.
- The existing Cloudflare Worker that serves `/strategic-foresight-dashboard` is configured outside this repo; the new Pages project will be a separate Cloudflare resource that resolves to `centaurion.me` with the existing Worker route preserved at the domain level (see `DEPLOYMENT.md`).
- `/site/` is isolated from `frontend/`, `marketing/`, `deploy/`, and `omega/` — no collisions.

## 2. Stack decision

**Astro 4.x + React islands + Tailwind 3.4 + TypeScript strict.**

| Concern | Choice | Why |
|---|---|---|
| Framework | Astro 4 | Zero-JS by default. Marketing site is mostly static. Hits LCP and Lighthouse budgets without Next overhead. |
| Interactivity | React 18 islands | Only forms and motion-bearing components ship JS. |
| Styling | Tailwind 3.4 | Token layer maps brand colors to CSS variables. Tree-shakes to <10KB. |
| Motion | Framer Motion (islands only) + CSS scroll-driven animations | Framer for micro-interactions; native CSS for scroll fades. `prefers-reduced-motion` honored at the CSS layer. |
| Forms | React Hook Form + Zod | Strict validation; islands. |
| Type | TypeScript strict, no `any` | Brief mandate. |
| Fonts | Self-hosted Inter + JetBrains Mono (woff2 subset) | Two families, four weights total. ~80KB. |
| Deploy | Cloudflare Pages | Co-exists with the existing Worker route on `centaurion.me`. |

## 3. Sitemap

```
/                                       Landing (long-scroll)
/method                                 The Centaurion Method
/levels                                 The 11 Levels of Agentic Engineering
/engage                                 Engagement tiers + advisory form
/strategic-foresight-dashboard          (preserved — served by existing Worker)
```

Footer-only links: Brief subscribe input, Strategic Foresight Dashboard, ©2026.

## 4. Route → component map

### `/` Landing

| # | Section | Component | Notes |
|---|---|---|---|
| 1 | Hero (100vh) | `<HeroEquation>` | Wordmark, thesis, equation, Tier-1 CTA |
| 2 | The Problem | `<ProblemSection>` | Two paragraphs, single column |
| 3 | Three Laws | `<LawPanel>` x 3 | Scroll-locked panels with SVG diagrams |
| 4 | Nova & Cortex | `<AgentsBrief>` | Two-column, named agents |
| 5 | 11 Levels preview | `<LevelsPreview>` | Tease 9–11, link to /levels |
| 6 | Method preview | `<MethodPreview>` | Tease Active Inference Loop, link to /method |
| 7 | Engagement tiers | `<TiersGrid>` | Three cards with hierarchy |
| 8 | Footer | `<SiteFooter>` | Brief input + minimal nav |

### `/method`

| Section | Component |
|---|---|
| Hero | `<MethodHero>` (Equation centerpiece) |
| Equation derivation | `<EquationProse>` |
| Three Laws (deeper) | `<LawDeepDive>` x 3 |
| Five Sensing Layers | `<SensingLayers>` |
| Active Inference Loop | `<LoopDiagram>` (SVG) + caption |
| Four-phase roadmap | `<Roadmap>` |
| Tier-2 CTA | `<DownloadMethodCTA>` |

### `/levels`

| Section | Component |
|---|---|
| Hero | `<LevelsHero>` |
| Levels table | `<LevelsTable>` (rows 1–8 standard, 9–11 emphasized) |
| Tier-3 CTA | `<AdvisoryCTA>` |

### `/engage`

| Section | Component |
|---|---|
| Hero | `<EngageHero>` |
| Tiers comparison | `<TiersComparison>` (Brief / Method / Advisory) |
| Advisory form | `<AdvisoryForm>` (5 fields, RHF + Zod) |

### Global

| Component | Used on |
|---|---|
| `<NavBar>` | All routes (minimal: wordmark + 3 links) |
| `<SiteFooter>` | All routes |
| `<StickyAdvisoryCTA>` | `/`, `/levels` (after 70% scroll) |
| `<EquationGlyph>` | Hero of `/`, `/method`; footer mark |
| `<PlatinumWordmark>` | NavBar, hero |

## 5. Content model

Source of truth lives in `/site/src/content/`:

```
content/
  brand.ts        Equation, Three Laws (id/name/body), Five Sensing Layers, Loop steps, Roadmap phases
  levels.ts       11 Levels (id, name, definition, adoption status, isCentaurionExtension)
  agents.ts       Nova, Cortex
  copy/
    landing.ts    Per-section copy keys
    method.ts
    levels.ts
    engage.ts
```

This means a single edit to `levels.ts` updates both the preview on `/` and the table on `/levels`. Copy Lead will populate these files; Frontend Engineer will type them strictly.

## 6. Design token surface (delegated to Visual Systems Designer)

Tokens flow through `tailwind.config.ts` → CSS variables in `:root` → component classes. Hex codes appear ONLY in the token file. Token surface:

- `colors`: obsidian, carbon, graphite, mercury, mist, signal-blue, platinum-from/via/to
- `fontFamily`: display (Inter Display), body (Inter), mono (JetBrains Mono)
- `fontSize`: display-1 (96px), display-2 (72px), display-3 (56px), body (18px), caption (14px)
- `letterSpacing`: display (-0.03em), caption (+0.08em)
- `lineHeight`: display (1.05), body (1.6)
- `spacing`: 8pt grid scale (4, 8, 16, 24, 32, 48, 64, 96, 128, 192)
- `transitionTimingFunction`: ease-out-expo for scroll fades; ease-out for hover
- `transitionDuration`: 200ms (hover), 800ms (scroll)

## 7. CTA wiring

| Tier | Endpoint | Validation |
|---|---|---|
| Tier 1 (Brief) | `POST /api/subscribe` | `{ email: z.string().email() }` |
| Tier 2 (Method PDF) | `POST /api/method-download` | `{ email, role, company }` |
| Tier 3 (Advisory) | `POST /api/advisory-request` | `{ name, role, company, maturity (1-11), challenge (max 280) }` |

For initial launch, endpoints are Cloudflare Pages Functions in `site/functions/api/`. They log to console and return 200. Real fulfillment (mailing list, PDF gating, Calendly handoff) is out of scope for this build.

## 8. Performance budget enforcement

- Hero route ships zero React JS. The Brief subscribe form on the hero is a native HTML `<form action="/api/subscribe" method="POST">` with progressive enhancement.
- All other forms ship as React islands (`client:visible`).
- Images: only inline SVGs. No raster.
- Optional WebGL particle field on hero is **deferred** — only ships if it can be ≤80KB and `client:idle`. Default off; flag-controlled.
- Fonts: `font-display: swap`, woff2 subset, preload only the display weight used in hero.

## 9. Accessibility contract

- One `<h1>` per route; semantic landmarks (`<header>`, `<main>`, `<nav>`, `<footer>`).
- All interactive elements reachable by keyboard; visible focus rings (2px Signal Blue, 2px offset).
- Body text contrast ≥ 7:1 against Obsidian (Mercury `#C0C0C0` on `#050505` = 12.6:1; Mist `#6B6B6B` on `#050505` = 4.95:1 — Mist used only for captions ≥14px and disclosed in QA).
- `prefers-reduced-motion: reduce` disables all opacity/translate animations and the parallax layer; fades become instant.

## 10. SEO contract

- Per-route OpenGraph + Twitter card meta via Astro `<SEO>` partial.
- JSON-LD `Organization` schema on `/` (name: Centaurion, founder: Malik J. Palamar, sameAs: [centaurion.me]).
- `sitemap.xml` generated by `@astrojs/sitemap`.
- `robots.txt` allows all, sitemap reference.

## 11. Repo layout

```
site/
  README.md                Local dev instructions
  DEPLOYMENT.md            Cloudflare Pages + Worker preservation
  architecture.md          (this file)
  design-system.md         Visual Systems output
  qa-report.md             QA Auditor output
  copy/
    landing.md
    method.md
    levels.md
    engage.md
  artifacts/
    post-mortem.md         Orchestrator post-mortem
  astro.config.mjs
  tailwind.config.ts
  tsconfig.json
  package.json
  src/
    pages/
      index.astro
      method.astro
      levels.astro
      engage.astro
    layouts/
      Base.astro
    components/
      hero/
      sections/
      ui/
      svg/
    content/
      brand.ts
      levels.ts
      agents.ts
      copy/
    styles/
      tokens.css
      globals.css
  public/
    fonts/
    favicon.svg
    og-default.png
  functions/
    api/
      subscribe.ts
      method-download.ts
      advisory-request.ts
```

## 12. Handoff contract to downstream agents

- **Copy Lead:** populate `site/copy/{landing,method,levels,engage}.md` AND structured exports in `site/src/content/copy/*.ts`. Voice gate is non-negotiable. Run forbidden-word grep on your own output before handing back.
- **Visual Systems Designer:** populate `site/design-system.md`, `site/tailwind.config.ts` (token layer), `site/src/styles/tokens.css`, and SVG assets in `site/src/components/svg/` (Three Laws diagrams, Active Inference Loop, wordmark, equation glyph).
- **Frontend Engineer:** consume the content model and design system. No hex codes outside tokens. Strict TS. Build must pass.
- **Motion Engineer:** layer motion on existing components. No new components. Honor `prefers-reduced-motion`.
- **QA Auditor:** verify against brief Section 11 quality gates line by line.
- **Deployment Engineer:** Cloudflare Pages config + DNS + Worker preservation.
