import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}"],
  theme: {
    extend: {
      colors: {
        obsidian: "var(--color-obsidian)",
        carbon: "var(--color-carbon)",
        graphite: "var(--color-graphite)",
        mercury: "var(--color-mercury)",
        mist: "var(--color-mist)",
        "signal-blue": "var(--color-signal-blue)",
        "platinum-from": "var(--color-platinum-from)",
        "platinum-via": "var(--color-platinum-via)",
        "platinum-to": "var(--color-platinum-to)",
      },
      fontFamily: {
        display: ["'Inter Display'", "Inter", "system-ui", "sans-serif"],
        body: ["Inter", "system-ui", "sans-serif"],
        mono: ["'JetBrains Mono'", "ui-monospace", "monospace"],
      },
      fontSize: {
        "display-1": [
          "clamp(3.5rem, 8vw, 6rem)",
          { lineHeight: "1.05", letterSpacing: "-0.03em", fontWeight: "800" },
        ],
        "display-2": [
          "clamp(2.75rem, 6vw, 4.5rem)",
          { lineHeight: "1.05", letterSpacing: "-0.03em", fontWeight: "800" },
        ],
        "display-3": [
          "clamp(2.25rem, 4.5vw, 3.5rem)",
          { lineHeight: "1.1", letterSpacing: "-0.025em", fontWeight: "700" },
        ],
        "body-lg": [
          "clamp(1.125rem, 1.4vw, 1.25rem)",
          { lineHeight: "1.6", letterSpacing: "-0.005em", fontWeight: "400" },
        ],
        body: [
          "clamp(1rem, 1.2vw, 1.125rem)",
          { lineHeight: "1.6", fontWeight: "400" },
        ],
        caption: [
          "0.875rem",
          { lineHeight: "1.4", letterSpacing: "0.08em", fontWeight: "400" },
        ],
      },
      spacing: {
        section: "clamp(6rem, 12vw, 12rem)",
      },
      maxWidth: {
        prose: "68ch",
        container: "80rem",
      },
      transitionDuration: {
        hover: "200ms",
        fade: "800ms",
      },
      transitionTimingFunction: {
        "out-expo": "cubic-bezier(0.16, 1, 0.3, 1)",
      },
      backgroundImage: {
        platinum:
          "linear-gradient(135deg, var(--color-platinum-from) 0%, var(--color-platinum-via) 50%, var(--color-platinum-to) 100%)",
      },
    },
  },
  plugins: [],
};

export default config;
