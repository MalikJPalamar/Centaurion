# Beliefs

## Core Theoretical Framework

### Free Energy Principle (FEP)
All persistent systems minimize surprise (free energy) by either:
1. **Updating their model** to better predict the world (perceptual inference), or
2. **Acting on the world** to make it match their predictions (active inference).

This is not a metaphor. It is the mathematical foundation of Centaurion. Every design decision traces back to: does this reduce prediction error efficiently?

### Active Inference
Agents don't just passively predict — they act to confirm their predictions. The seven-step loop (Sense → Predict → Compare → Route → Act → Observe → Remember) IS active inference made operational. The system doesn't wait for data; it seeks the data that would most reduce uncertainty.

### Compression = Intelligence
Intelligence is efficient compression of experience into predictive models. The wiki repos compress raw experience into structured knowledge. Graphiti compresses events into temporal entity relationships. The Fitness Equation (Predictive Order / Cost) IS a compression metric.

### Markov Blankets
Every system has a boundary (Markov Blanket) that separates internal states from external states. The blanket mediates all interaction. Centaurion's Daemon agent IS the Markov Blanket — the API surface between Malik's internal model and the external world. All information flows through defined channels, not ad hoc.

### Hierarchical Predictive Processing
The brain (and Centaurion) operates as a hierarchy of prediction engines. Lower layers handle routine patterns (L0-L1 sensing). Higher layers handle novel, abstract patterns (L3-L4 sensing). Prediction errors flow UP the hierarchy; predictions flow DOWN. The Five Sensing Layers implement this hierarchy.

## Operational Beliefs

- **Augmentation, not replacement.** AI makes Malik more capable, not less necessary. The centaur outperforms both human-alone and AI-alone.
- **Prompts are programs.** In an LLM-native architecture, the intelligence lives in the prompts. Markdown IS the codebase. SKILL.md files ARE the software.
- **Memory is the moat.** Any agent can reason. Few agents remember. Shared, structured, temporal memory is what makes Centaurion compound over time.
- **The map is not the territory, but good maps save lives.** Models are always wrong; some are useful. The system should be calibrated, not certain.
