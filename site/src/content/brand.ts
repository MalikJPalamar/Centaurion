// Centaurion brand canon. Single source of truth for framework facts.
// DO NOT add laws, levels, agents, or principles not present in the brief.

export const equation = {
  numerator: "Predictive Order",
  denominator: "Thermodynamic Cost",
  result: "Fitness",
  caption: "RAISE THE TOP. LOWER THE BOTTOM. SHIP THE RATIO.",
} as const;

export const threeLaws = [
  {
    id: "hierarchy",
    number: "01",
    name: "Hierarchy",
    short:
      "Prediction is layered. Every layer forecasts the one below. Your org chart has to mirror it.",
    long:
      "Prediction is layered. Every layer forecasts the one below it. When your org chart doesn't mirror your prediction stack, error has nowhere to flow. That is what a stuck company feels like from the inside.",
  },
  {
    id: "routing",
    number: "02",
    name: "Routing",
    short:
      "Every signal has a best-fit agent. Route by competence, not by title.",
    long:
      "Every signal has a best-fit agent — human, machine, or paired. Route by competence, not by title, or you pay the same cost twice. Most enterprises route by org chart. That's the tax nobody counts.",
  },
  {
    id: "coupling",
    number: "03",
    name: "Coupling",
    short:
      "One-way automation breaks on contact. Human and agent must update each other, both directions.",
    long:
      "One-way automation breaks under contact. Human and agent must update each other, both directions, every cycle. The coupling is what you are actually buying. Everything else is a demo.",
  },
] as const;

export const sensingLayers = [
  {
    id: 1,
    name: "Inner telemetry",
    example: "Throughput, error rate, agent task completion",
  },
  {
    id: 2,
    name: "Market and competitive",
    example: "Pricing moves, capability releases, hire flows",
  },
  {
    id: 3,
    name: "Macro and geopolitical",
    example: "Energy regime, trade alignment, capital flow",
  },
  {
    id: 4,
    name: "Cultural undercurrent",
    example: "Salience shifts, archetype rotation, taboo breaches",
  },
  {
    id: 5,
    name: "Existential drift",
    example: "Compute trajectory, biosphere state, civilizational rhythm",
  },
] as const;

export const loopSteps = [
  { id: 1, name: "Sense", note: "Pull signal from all five layers." },
  { id: 2, name: "Predict", note: "State the hypothesis. Out loud. On the record." },
  { id: 3, name: "Act", note: "Ship what the hypothesis recommends." },
  { id: 4, name: "Observe", note: "Record what actually happened." },
  { id: 5, name: "Update", note: "Fix the model where it was wrong." },
  {
    id: 6,
    name: "Re-route",
    note: "If error stayed high, the signal was in the wrong hands.",
  },
  {
    id: 7,
    name: "Re-couple",
    note: "If either side stopped learning, the binding is broken.",
  },
] as const;

export const roadmap = [
  { phase: 1, window: "2026", focus: "Sensing Stack — Nova live across the five layers" },
  { phase: 2, window: "2027", focus: "Predictive Layer — Cortex hypothesis engine in production" },
  { phase: 3, window: "2028", focus: "Action Layer — autonomous execution under routing gates" },
  { phase: 4, window: "2029", focus: "Embodied Layer — physical-digital bridge, Level 11" },
] as const;
