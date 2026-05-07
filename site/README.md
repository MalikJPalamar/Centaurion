# Centaurion.me

The public website for Centaurion — a human-AI augmentation advisory practice.

> Predictive order, per unit thermodynamic cost.

---

## Stack

- **Astro 4** (static output, zero-JS by default)
- **React 18** (islands only — Advisory form, etc.)
- **Tailwind 3.4** with a CSS-variable token layer
- **TypeScript** strict mode (`noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`)
- **Framer Motion + native CSS** for motion (scroll fades, button sheen)
- **React Hook Form + Zod** for the Advisory form
- **Cloudflare Pages** (deploy) + **Pages Functions** (form endpoints)

## Repo layout

```
site/
├─ architecture.md       Information Architect output
├─ design-system.md      Visual Systems Designer output
├─ qa-report.md          QA Auditor output
├─ DEPLOYMENT.md         Deployment Engineer output
├─ copy/                 Copy Lead source-of-truth markdown
├─ artifacts/            Orchestrator post-mortem
├─ scripts/              Audit gates (forbidden-words, hex-codes)
├─ functions/api/        Cloudflare Pages Functions (form endpoints)
├─ public/               Static assets (favicon, robots, OG image)
└─ src/
   ├─ pages/             /, /method, /levels, /engage
   ├─ layouts/Base.astro
   ├─ components/        Section + UI components, SVG library
   ├─ content/           Brand canon (equation, laws, levels, agents)
   └─ styles/            tokens.css + globals.css
```

## Local development

```bash
cd site
npm install
npm run dev          # Astro dev server, http://localhost:4321
```

## Quality gates (run before every commit)

```bash
npm run audit:words    # Brand canon: zero forbidden buzzwords
npm run audit:hex      # Design system: hex codes only in tokens.css
npm run check          # Astro/TypeScript type-check
npm run build          # Production build
```

## Brand canon — non-negotiable

This site uses ONLY the framework facts from the project brief:

- The Centaurion Equation (Fitness = Predictive Order / Thermodynamic Cost)
- The Three Laws (Hierarchy, Routing, Coupling)
- The Five Sensing Layers
- The Active Inference Loop (7 steps)
- The 11 Levels of Agentic Engineering (Levels 9–11 are Centaurion's extension)
- The named agents: Nova (perception), Cortex (reasoning)

Do not add laws, levels, agents, or principles. The audit script enforces voice;
content edits go through `src/content/*.ts` so the four pages stay synchronized.

## Deployment

See `DEPLOYMENT.md`. The `/strategic-foresight-dashboard` route is served by
an existing Cloudflare Worker on the same hostname and must remain untouched.

## License

© 2026 Centaurion. All rights reserved.
