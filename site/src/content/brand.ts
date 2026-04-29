// Centaurion brand canon. Single source of truth for framework facts.
// DO NOT add laws, levels, agents, or principles not present in the brief.

export const equation = {
  numerator: "Predictive Order",
  denominator: "Thermodynamic Cost",
  result: "Fitness",
  caption: "ADAPTED FROM FRISTON. ENGINEERED FOR ENTERPRISE.",
} as const;

export const threeLaws = [
  {
    id: "hierarchy",
    number: "01",
    name: "Hierarchy",
    short:
      "Cognition is layered. Each layer predicts the layer below. Architecture must mirror this.",
    long:
      "Cognition is layered. Each layer predicts the layer below. An organization whose architecture does not mirror this will spend its energy correcting itself.",
  },
  {
    id: "routing",
    number: "02",
    name: "Routing",
    short:
      "Information flows to the agent — human or machine — with the lowest prediction error for that signal class.",
    long:
      "Information must reach the agent — human or machine — with the lowest prediction error for that signal class. Misrouting is the dominant cost in most enterprises. Most do not know they are paying it.",
  },
  {
    id: "coupling",
    number: "03",
    name: "Coupling",
    short:
      "Human and machine agents must be bidirectionally coupled. One-way automation is brittle; co-evolution is anti-fragile.",
    long:
      "Human and machine agents must be bidirectionally coupled. One-way automation is brittle. Co-evolution is anti-fragile. The coupling is the product.",
  },
] as const;

export const sensingLayers = [
  {
    id: 1,
    name: "Inner operational telemetry",
    example: "Throughput, error rate, agent task completion",
  },
  {
    id: 2,
    name: "Outer market and competitive",
    example: "Pricing moves, capability releases, hire flows",
  },
  {
    id: 3,
    name: "Macro and geopolitical foresight",
    example: "Energy regime, trade alignment, capital flow",
  },
  {
    id: 4,
    name: "Cultural and narrative undercurrent",
    example: "Salience shifts, archetype rotation, taboo breaches",
  },
  {
    id: 5,
    name: "Existential and long-horizon drift",
    example: "Compute trajectory, biosphere state, civilizational rhythm",
  },
] as const;

export const loopSteps = [
  { id: 1, name: "Sense", note: "Acquire signal across the five layers." },
  { id: 2, name: "Predict", note: "Form an explicit hypothesis about what comes next." },
  { id: 3, name: "Act", note: "Take the action the hypothesis recommends." },
  { id: 4, name: "Observe", note: "Record what actually happened." },
  { id: 5, name: "Update", note: "Adjust the model where it was wrong." },
  {
    id: 6,
    name: "Re-route",
    note: "Move the signal to a better-fitting agent if prediction error stayed high.",
  },
  {
    id: 7,
    name: "Re-couple",
    note: "Adjust the human-machine binding if either side stopped learning.",
  },
] as const;

export const roadmap = [
  { phase: 1, window: "2026", focus: "Sensing Stack — Nova online across the five layers" },
  { phase: 2, window: "2027", focus: "Predictive Layer — Cortex hypothesis engine in production" },
  { phase: 3, window: "2028", focus: "Action Layer — autonomous execution under human routing gates" },
  { phase: 4, window: "2029", focus: "Embodied Layer — physical-digital bridge, Level 11" },
] as const;
