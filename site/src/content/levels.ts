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
      "A human writes a prompt; a model returns a response. The interface is conversational; the responsibility is entirely human.",
    adoption: "Universal",
    isCentaurionExtension: false,
  },
  {
    number: "02",
    name: "Tool-Augmented Models",
    definition:
      "Models call defined tools — search, code execution, retrieval — under a single human-authored intent.",
    adoption: "Universal",
    isCentaurionExtension: false,
  },
  {
    number: "03",
    name: "Retrieval-Grounded Agents",
    definition:
      "Models reason over indexed knowledge bases, citing sources, with bounded autonomy on a single task.",
    adoption: "Mainstream",
    isCentaurionExtension: false,
  },
  {
    number: "04",
    name: "Single-Agent Workflows",
    definition:
      "An agent executes a multi-step task with its own planning loop, returning to the human at completion.",
    adoption: "Mainstream",
    isCentaurionExtension: false,
  },
  {
    number: "05",
    name: "Multi-Agent Orchestration",
    definition:
      "Specialist agents hand work to one another under an orchestrator, with the human supervising the orchestrator.",
    adoption: "Emerging",
    isCentaurionExtension: false,
  },
  {
    number: "06",
    name: "Agent-Authored Code in CI",
    definition:
      "Agents write, test, and submit code through review pipelines; humans gate merges.",
    adoption: "Emerging",
    isCentaurionExtension: false,
  },
  {
    number: "07",
    name: "Agent-Operated Systems Under Review",
    definition:
      "Agents run production systems — incident response, ops, analytics — with human approval on consequential actions.",
    adoption: "Early",
    isCentaurionExtension: false,
  },
  {
    number: "08",
    name: "Agent-Initiated Strategy",
    definition:
      "Agents propose strategic moves with full reasoning chains; humans accept, reject, or refine.",
    adoption: "Frontier",
    isCentaurionExtension: false,
  },
  {
    number: "09",
    name: "Autonomous Deployment Pipelines",
    definition:
      "A voice command on a phone reaches an agent swarm; the swarm builds, simulates, deploys, and monitors live infrastructure with no human in the execution loop.",
    adoption: "Centaurion practice",
    isCentaurionExtension: true,
  },
  {
    number: "10",
    name: "Simulation-First Development",
    definition:
      "Agents stage every deployment in a synthetic environment that models the production system to fidelity, and only commit to production once simulation outcomes meet preset thresholds.",
    adoption: "Centaurion practice",
    isCentaurionExtension: true,
  },
  {
    number: "11",
    name: "Physical-Digital Bridge",
    definition:
      "Agents act in the physical world through robotics, IoT actuators, and embodied sensors, closing the loop between digital reasoning and material consequence.",
    adoption: "Centaurion research",
    isCentaurionExtension: true,
  },
] as const;
