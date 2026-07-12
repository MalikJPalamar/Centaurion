# Centaurion Viral Reel — 9:16 Design

A maximalist viral reel built for IG Reels / TikTok / Shorts. **Intentionally breaks** the editorial-silence brand of the 1920 manifesto reel. This is the feed-stopper cut — the manifesto reel is for the website.

Tone: pain stacks → mechanism revealed → counter-positioning slam. Hormozi/Goggins energy, not editorial silence.

## Palette

| Token       | Hex       | Use                                                     |
| ----------- | --------- | ------------------------------------------------------- |
| `--bg`      | `#000000` | Pure black. Maximum contrast for the feed.              |
| `--fg`      | `#FFFFFF` | Display text. Pure white for slam scenes.               |
| `--accent`  | `#FF3535` | Hot red — the price of agreement. Used on warnings.     |
| `--gold`    | `#E8B872` | Amber — only on CENTAURION brand reveal. Bridges to 1920 reel. |
| `--cream`   | `#ECE5D5` | Paper off-white — only on the brand outro. Same as 1920. |
| `--ghost`   | `#3A3A3A` | Residual bias names behind active text.                 |

## Typography

| Voice     | Font                        | Weight | Use                                       |
| --------- | --------------------------- | ------ | ----------------------------------------- |
| Slam      | Anton (fallback Impact)     | 400    | Hook, bias names, the BIG number.         |
| Body      | Inter                       | 900    | Statements, pivots.                       |
| Brand     | Instrument Serif            | 400    | Centaurion wordmark + tagline.            |
| Mono      | JetBrains Mono              | 500    | "meanwhile," / domain / metadata.         |

Tracking on slam type: `-0.02em`. Tracking on mono caps: `0.16em`. Brand serif: `0.04em`.

## Motion

- **Hard cuts** are the rule. No crossfades except into the brand outro.
- **White-flash frames** at major beat transitions: 1 frame at opacity 1, decays in 0.15s.
- **Camera shake** on slams — quick rotate + translate, decays in 0.4s.
- **Glitch**: RGB-split via dual text-shadow (red -10px / cyan +10px) animated on/off in 0.12s bursts.
- **No drift** on display text. Static between hits — energy comes from cuts, not motion.
- **Tempo**: cuts every 0.4–0.8s in the bias wall, breath holds only on the hook and brand outro.

## Beat Plan (22s total)

| Beat | Window  | Content                                       |
| ---- | ------- | --------------------------------------------- |
| 1    | 0.0–2.0 | HOOK: "YOUR AI / AGREES WITH YOU."            |
| 2    | 2.0–4.5 | STACK: 5 affirmations cascading (GENIUS → PERFECT) |
| 3    | 4.5–6.0 | PIVOT: black, mono "...meanwhile,"            |
| 4    | 6.0–10.0 | BIAS WALL: 8 named biases                    |
| 5    | 10.0–12.5 | NUMBER: "188" — "known cognitive biases."   |
| 6    | 12.5–15.0 | PRICE: "every YES makes them compound."     |
| 7    | 15.0–18.5 | FLIP: "what if your AI / PUSHED BACK?"      |
| 8    | 18.5–22.0 | BRAND: CENTAURION wordmark + tagline + URL  |

## What NOT to Do

- No animated GIFs, no emojis, no stock B-roll.
- No buzzwords ("AI-powered", "next-gen", "revolutionary").
- No gradients except the final brand fade.
- No music inline — composition ships silent so trending audio can be added in IG/TikTok.
