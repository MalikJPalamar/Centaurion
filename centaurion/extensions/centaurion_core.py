"""
Centaurion Core — Hermes Extension

Loads Centaurion identity (TELOS) into Hermes at session start.
Injects Three Laws, venture context, and Active Inference loop
into every agent interaction.

Install: copy to ~/.hermes/extensions/centaurion_core.py
"""

import json
import os
from pathlib import Path
from datetime import datetime


CENTAURION_REPO = os.environ.get("CENTAURION_REPO", os.path.expanduser("~/Centaurion"))
IDENTITY_DIR = Path(CENTAURION_REPO) / "identity"
FRAMEWORK_DIR = Path(CENTAURION_REPO) / "framework"
STATE_DIR = Path(CENTAURION_REPO) / "memory" / "state"


def load_identity_context():
    """Load key identity files for session injection."""
    context_parts = []

    priority_files = [
        ("PURPOSE", IDENTITY_DIR / "PURPOSE.md"),
        ("MISSION", IDENTITY_DIR / "MISSION.md"),
        ("GOALS", IDENTITY_DIR / "GOALS.md"),
        ("PREFERENCES", IDENTITY_DIR / "PREFERENCES.md"),
    ]

    for label, path in priority_files:
        if path.exists():
            content = path.read_text().strip()
            # Truncate to keep within Hermes MEMORY.md limits
            if len(content) > 500:
                content = content[:500] + "\n[truncated]"
            context_parts.append(f"## {label}\n{content}")

    return "\n\n".join(context_parts)


def load_routing_thresholds():
    """Load current Routing Gate thresholds from framework config."""
    return {
        "novelty_threshold": 0.7,
        "stakes_threshold": 0.5,
        "reversibility_threshold": 0.3,
    }


def log_routing_decision(task, novelty, stakes, reversibility, route):
    """Append a routing decision to the routing log."""
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    log_file = STATE_DIR / "routing-log.jsonl"

    entry = {
        "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "task": task,
        "novelty": novelty,
        "stakes": stakes,
        "reversibility": reversibility,
        "route": route,
        "outcome_rating": None,
        "routing_correct": None,
    }

    with open(log_file, "a") as f:
        f.write(json.dumps(entry) + "\n")


def detect_venture(text):
    """Detect which venture a task relates to based on keywords."""
    text_lower = text.lower()

    aob_keywords = ["aob", "art of breath", "breathwork", "facilitator", "ontraport",
                     "mighty networks", "certification", "anthony", "chrissy", "anna"]
    bb_keywords = ["builderbee", "builder bee", "ghl", "gohighlevel", "client",
                    "onboarding", "programmatic", "automation consultancy"]
    centaurion_keywords = ["centaurion", "framework", "three laws", "precision ratio",
                           "active inference", "exo-cortex", "routing gate"]

    aob_score = sum(1 for k in aob_keywords if k in text_lower)
    bb_score = sum(1 for k in bb_keywords if k in text_lower)
    c_score = sum(1 for k in centaurion_keywords if k in text_lower)

    if aob_score > bb_score and aob_score > c_score:
        return "aob"
    elif bb_score > aob_score and bb_score > c_score:
        return "builderbee"
    elif c_score > 0:
        return "centaurion"
    return "general"


# ── Hermes Extension Interface ────────────────────────────

class CentaurionCoreExtension:
    """
    Hermes extension that loads Centaurion identity context
    at session start and provides venture detection.
    """

    def __init__(self, agent):
        self.agent = agent
        self.identity_context = None
        self.thresholds = load_routing_thresholds()

    def on_session_start(self, session):
        """Called when a new Hermes session begins."""
        self.identity_context = load_identity_context()

        # Inject identity into session context
        if hasattr(session, 'add_context'):
            session.add_context("centaurion_identity", self.identity_context)

    def on_message(self, message):
        """Called on each user message — detect venture and tag."""
        if hasattr(message, 'content'):
            venture = detect_venture(message.content)
            if hasattr(message, 'metadata'):
                message.metadata['venture'] = venture

    def on_session_end(self, session):
        """Called when session ends — log to state."""
        pass


def create_extension(agent):
    """Factory function for Hermes extension loading."""
    return CentaurionCoreExtension(agent)
