"""
Honcho Integration — Hermes Extension

Enables dialectic reasoning about the user. After sessions, Honcho
analyzes the interaction to build a deeper model of WHY Malik makes
decisions — not just WHAT he decided.

Hermes has native Honcho support. This extension configures it
for Centaurion's three-venture context.

Install: copy to ~/.hermes/extensions/honcho_bridge.py
Config: add honcho section to ~/.hermes/config.yaml

Honcho is free-tier for personal use (honcho.dev).
"""

import os
import json
from pathlib import Path


CENTAURION_REPO = os.environ.get("CENTAURION_REPO", os.path.expanduser("~/Centaurion"))


# ── Hermes Honcho Configuration ──────────────────────────
# This generates the config.yaml snippet for Hermes's native Honcho support.

HONCHO_CONFIG = {
    "honcho": {
        "enabled": True,
        "app_name": "centaurion",
        "user_id": "malik-palamar",
        "contextCadence": 5,      # Refresh base context every 5 messages
        "dialecticCadence": 10,    # Run dialectic reasoning every 10 messages
        "tools": {
            "honcho_profile": True,     # User profile and characteristics
            "honcho_search": True,      # Search past interactions
            "honcho_context": True,     # Get current context window
            "honcho_reasoning": True,   # Dialectic reasoning about user
            "honcho_conclude": True,    # Conclude and store insights
        },
        "centaurion_context": {
            "ventures": ["aob", "builderbee", "centaurion"],
            "identity_source": "identity/",
            "routing_gate_active": True,
            "three_laws_enforcement": True,
        },
    }
}


def generate_honcho_config():
    """Generate the Honcho config snippet for config.yaml."""
    return HONCHO_CONFIG


def get_setup_instructions():
    """Return setup instructions for Honcho."""
    return """
# Honcho Setup for Centaurion

## 1. Sign up at honcho.dev (free tier)
   - Create an app named "centaurion"
   - Get your API key

## 2. Add to Hermes .env
   echo 'HONCHO_API_KEY=your-key-here' >> ~/.hermes/.env

## 3. Add to Hermes config.yaml
   hermes config edit
   # Add under the root level:
   honcho:
     enabled: true
     app_name: centaurion

## 4. Verify
   hermes
   > /honcho status

## What Honcho Adds
- Dialectic reasoning: LLM analyzes interactions to model user preferences
- Deep profile: understands WHY Malik prefers certain approaches
- Venture-aware context: tracks decision patterns per venture
- Auto-refreshes: base context every 5 messages, dialectic every 10
"""


# ── Hermes Extension Interface ────────────────────────────

class HonchoBridgeExtension:
    """
    Configures Hermes's native Honcho integration with
    Centaurion-specific context (ventures, Three Laws, routing).
    """

    def __init__(self, agent):
        self.agent = agent

    def on_session_start(self, session):
        """Inject Centaurion context into Honcho's user profile."""
        if hasattr(self.agent, 'honcho') and self.agent.honcho:
            # Add venture context to Honcho's understanding
            venture_context = (
                "User runs three ventures: AOB (Art of Breath, Head of IT), "
                "BuilderBee (AI automation, Fractional CEO), "
                "Centaurion.me (framework, Founder). "
                "Prefers concise output, thinks in systems, reviews on phone."
            )
            if hasattr(self.agent.honcho, 'add_context'):
                self.agent.honcho.add_context(venture_context)


def create_extension(agent):
    """Factory function for Hermes extension loading."""
    return HonchoBridgeExtension(agent)
