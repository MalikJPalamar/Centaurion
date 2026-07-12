# HyperFrames Composition Project — 9:16 Viral Cut

Companion to the 1920×1080 manifesto reel. Intentionally breaks brand for feed virality.

## Commands

```bash
npm run dev          # preview in browser
npm run check        # lint + validate + inspect
npm run render       # render to MP4
```

## Key Rules

1. Every timed element needs `data-start`, `data-duration`, `data-track-index`, and `class="clip"`.
2. Timelines must be paused and registered on `window.__timelines["main"]`.
3. Only deterministic logic.
