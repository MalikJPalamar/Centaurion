// The 11 Levels of Agentic Engineering.
// Levels 1-8: canonical (Bassim Eledath taxonomy).
// Levels 9-11: Centaurion's extension. Marked isCentaurionExtension=true.

export type Adoption =
  | "Universal"
  | "Mainstream"
  | "Emerging"
  | "Early"
  | "Frontier"
  | "Centaurion practice"
  | "Centaurion research";

export type Level = Readonly<{
  number: string;
  name: string;
  definition: string;
  adoption: Adoption;
  isCentaurionExtension: boolean;
}>;

export const levels: readonly Level[] = [
  {
    number: "01",
    name: "Prompted Assistants",
    definition:
      "A human writes a prompt. A model answers. The responsibility never leaves the human.",
    adoption: "Universal",
    isCentaurionExtension: false,
  },
  {
    number: "02",
    name: "Tool-Augmented Models",
    definition:
      "The model calls defined tools — search, code, retrieval — under one human-authored intent.",
    adoption: "Universal",
    isCentaurionExtension: false,
  },
  {
    number: "03",
    name: "Retrieval-Grounded Agents",
    definition:
      "The model reasons over your indexed knowledge, cites sources, and stays inside a single task.",
    adoption: "Mainstream",
    isCentaurionExtension: false,
  },
  {
    number: "04",
    name: "Single-Agent Workflows",
    definition:
      "An agent plans and executes a multi-step task, then returns to the human at the end.",
    adoption: "Mainstream",
    isCentaurionExtension: false,
  },
  {
    number: "05",
    name: "Multi-Agent Orchestration",
    definition:
      "Specialist agents hand work to each other under an orchestrator. Humans supervise the orchestrator.",
    adoption: "Emerging",
    isCentaurionExtension: false,
  },
  {
    number: "06",
    name: "Agent-Authored Code in CI",
    definition:
      "Agents write, test, and submit code through your review pipeline. Humans gate merges.",
    adoption: "Emerging",
    isCentaurionExtension: false,
  },
  {
    number: "07",
    name: "Agent-Operated Systems",
    definition:
      "Agents run production — incident response, ops, analytics — with human approval on consequential moves.",
    adoption: "Early",
    isCentaurionExtension: false,
  },
  {
    number: "08",
    name: "Agent-Initiated Strategy",
    definition:
      "Agents propose strategic moves with full reasoning chains. Humans accept, reject, or refine.",
    adoption: "Frontier",
    isCentaurionExtension: false,
  },
  {
    number: "09",
    name: "Autonomous Deployment Pipelines",
    definition:
      "A voice command reaches an agent swarm. The swarm builds, simulates, deploys, monitors. Zero humans in the execution loop.",
    adoption: "Centaurion practice",
    isCentaurionExtension: true,
  },
  {
    number: "10",
    name: "Simulation-First Development",
    definition:
      "Every deployment stages in a synthetic environment first. Nothing hits production until simulation meets threshold.",
    adoption: "Centaurion practice",
    isCentaurionExtension: true,
  },
  {
    number: "11",
    name: "Physical-Digital Bridge",
    definition:
      "Agents act in the physical world through robotics, IoT, and embodied sensors. Digital reasoning closes on material consequence.",
    adoption: "Centaurion research",
    isCentaurionExtension: true,
  },
] as const;
