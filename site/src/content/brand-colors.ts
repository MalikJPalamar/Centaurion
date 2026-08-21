// Brand color values for non-CSS contexts (HTML meta tags, JSON-LD, etc.)
// CSS consumers MUST use the token variables in src/styles/tokens.css.
// This file is the single allowlist exception for hex literals.

export const brandColors = {
  obsidian: "#050505",
  platinum: "#B7B5B2",
} as const;
