export const namedAgents = [
  {
    id: "nova",
    name: "Nova",
    role: "Perception",
    description:
      "Nova handles the five sensing layers: inner telemetry, outer market, macro foresight, cultural undercurrent, existential drift. Nova reduces a thousand signals to the ones that matter.",
  },
  {
    id: "cortex",
    name: "Cortex",
    role: "Reasoning",
    description:
      "Cortex handles prediction, planning, hypothesis. Cortex turns Nova's signal into decisions a human can act on, and surfaces the ones a human must.",
  },
] as const;
