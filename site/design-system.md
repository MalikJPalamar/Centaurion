# Centaurion.me — Design System

**Author:** Visual Systems Designer (orchestrator)
**Status:** Authoritative tokens. Hex codes appear ONLY in `src/styles/tokens.css` and `tailwind.config.ts`.

---

## 1. Colors

| Token | Hex | Role | Usage |
|---|---|---|---|
| `obsidian` | `#050505` | Primary background | `<body>`, page bg |
| `carbon` | `#0E0E10` | Surface elevation 1 | Cards, panels |
| `graphite` | `#1A1A1C` | Surface elevation 2, dividers | Borders, hairlines |
| `mercury` | `#C0C0C0` | Secondary text on dark | Body copy |
| `mist` | `#6B6B6B` | Tertiary text | Captions ≥14px only |
| `signal-blue` | `#5B8DEF` | Active CTA only | Tier-3 button, focus ring |
| `platinum-from` | `#E5E4E2` | Gradient stop 1 | Display headlines |
| `platinum-via` | `#B7B5B2` | Gradient stop 2 | Display headlines |
| `platinum-to` | `#8C8A87` | Gradient stop 3 | Display headlines |

**Platinum gradient (canonical):**
```css
background: linear-gradient(135deg, #E5E4E2 0%, #B7B5B2 50%, #8C8A87 100%);
```
Applied via `background-clip: text` on display text and as a `<linearGradient>` in SVG assets.

**Signal Blue is reserved.** Tier-3 CTA, focus rings, active-state indicators only. Never decorative.

**Contrast verification (against `#050505`):**
- Mercury `#C0C0C0`: 12.6:1 ✓ (AAA body)
- Mist `#6B6B6B`: 4.95:1 ✓ AA only — restricted to caption sizes ≥14px
- Signal Blue `#5B8DEF`: 6.2:1 ✓ AA large

---

## 2. Typography

| Family | Source | Weights loaded |
|---|---|---|
| Inter Display | Google Fonts (self-hosted woff2 subset) | 700, 800 |
| Inter | Google Fonts (self-hosted woff2 subset) | 400 |
| JetBrains Mono | Google Fonts (self-hosted woff2 subset) | 400 |

Total: 4 weights, 2 families, ~80KB woff2 subset.

| Class | Size (desktop) | Size (mobile) | Weight | Tracking | Line-height |
|---|---|---|---|---|---|
| `.text-display-1` | 96px | 56px | 800 | -0.03em | 1.05 |
| `.text-display-2` | 72px | 44px | 800 | -0.03em | 1.05 |
| `.text-display-3` | 56px | 36px | 700 | -0.025em | 1.1 |
| `.text-body-lg` | 20px | 18px | 400 | -0.005em | 1.6 |
| `.text-body` | 18px | 16px | 400 | 0 | 1.6 |
| `.text-caption` | 14px | 13px | 400 | +0.08em | 1.4 |

Captions are mono, uppercase, used as eyebrows above headings.

---

## 3. Spacing (8pt grid)

`4, 8, 16, 24, 32, 48, 64, 96, 128, 192` (px). Tailwind keys: `1, 2, 4, 6, 8, 12, 16, 24, 32, 48`.

Section padding: `py-32` desktop, `py-24` mobile. Container max-width: `1280px`. Gutters: `px-8` desktop, `px-6` mobile.

---

## 4. Motion

| Token | Value | Use |
|---|---|---|
| `duration-hover` | 200ms | Button sheen, link underline |
| `duration-fade` | 800ms | Scroll-triggered fade-up |
| `ease-out-expo` | `cubic-bezier(0.16, 1, 0.3, 1)` | Scroll fades |
| `ease-out` | `cubic-bezier(0.4, 0, 0.2, 1)` | Hover |

Scroll fade-up: `opacity 0 → 1, translateY 24px → 0` over 800ms, staggered by 80ms per child where used.

Parallax on hero: max 40px shift on equation glyph, GPU-accelerated transform only.

`@media (prefers-reduced-motion: reduce)`: all opacity and transform animations become instantaneous; parallax disabled.

---

## 5. Component primitives

### `<Button>` variants

| Variant | Tier | Background | Border | Text |
|---|---|---|---|---|
| `hairline` | 1 | transparent | 1px graphite | mercury |
| `platinum` | 2 | platinum gradient | none | obsidian |
| `signal` | 3 | signal-blue | none | obsidian |

Hover (all): 200ms platinum sheen sweep (linear gradient overlay translating left to right).

Focus: 2px signal-blue ring with 2px obsidian offset.

### `<Input>` (Brief subscribe)

Hairline input: 1px graphite border, transparent bg, mercury text, mist placeholder. Inline arrow button on right edge.

### `<Card>` (Tier grid)

Carbon background (`#0E0E10`), 1px graphite border, 32px padding, 16px border-radius.

---

## 6. SVG asset inventory

Located at `src/components/svg/`:

- `Wordmark.astro` — CENTAURION lettermark, viewBox-scaled, platinum `<linearGradient>` fill.
- `EquationGlyph.astro` — typographic equation rendered as SVG text for the hero.
- `LawHierarchy.astro` — three stacked horizontal lines with bidirectional arrows.
- `LawRouting.astro` — a source node with three diverging paths, the middle path bolded.
- `LawCoupling.astro` — two nodes connected by two opposing arcs (a closed loop).
- `LoopDiagram.astro` — seven nodes arranged in a circle with directional arrows; node labels: Sense, Predict, Act, Observe, Update, Re-route, Re-couple.

All SVG strokes use the platinum gradient via inline `<defs><linearGradient>`. Stroke width: 1.5px. No fills. ViewBox normalized.

---

## 7. Forbidden in this design system

- Drop shadows (none, ever — depth comes from elevation token, not shadow)
- Border-radius >16px (no soft pills)
- Color outside the eight tokens above
- Glassmorphism / backdrop-blur (cliché)
- Gradients outside the canonical platinum
- Icon libraries (every glyph is hand-crafted SVG)
- Any animation easing with overshoot (no spring, no bounce)
