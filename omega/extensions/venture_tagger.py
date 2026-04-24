"""
Venture Tagger — Hermes Extension

Auto-detects which venture (AOB, BuilderBee, Centaurion) an interaction
relates to and tags memory, skills, and tool outputs accordingly.

This enables the Coupling Law: shared memory across ventures with
proper separation and cross-venture pattern detection.

Install: copy to ~/.hermes/extensions/venture_tagger.py
"""

import json
import os
from pathlib import Path
from datetime import datetime


CENTAURION_REPO = os.environ.get("CENTAURION_REPO", os.path.expanduser("~/Centaurion"))
STATE_DIR = Path(CENTAURION_REPO) / "memory" / "state"

VENTURE_KEYWORDS = {
    "aob": [
        "aob", "art of breath", "alchemy of breath", "breathwork",
        "facilitator", "certification", "ontraport", "mighty networks",
        "anthony", "chrissy", "anna", "renārs", "amy", "tania",
        "katerina", "moni", "breathe the world", "pranayama",
        "retreat", "workshop", "membership",
    ],
    "builderbee": [
        "builderbee", "builder bee", "ghl", "gohighlevel",
        "go high level", "client onboarding", "programmatic ads",
        "fractional ceo", "automation consultancy", "sub-account",
        "funnel", "pipeline", "lead capture", "nurture sequence",
    ],
    "centaurion": [
        "centaurion", "exo-cortex", "three laws", "precision ratio",
        "active inference", "routing gate", "free energy", "markov",
        "cortex", "nova", "daemon", "omega", "telos", "hermes agent",
        "dev loop", "framework", "11 levels",
    ],
}


def classify_venture(text):
    """
    Classify text into a venture based on keyword density.
    Returns: (venture, confidence, matched_keywords)
    """
    text_lower = text.lower()
    scores = {}
    matches = {}

    for venture, keywords in VENTURE_KEYWORDS.items():
        matched = [k for k in keywords if k in text_lower]
        scores[venture] = len(matched)
        matches[venture] = matched

    if not any(scores.values()):
        return "general", 0.0, []

    best = max(scores, key=scores.get)
    total = sum(scores.values())
    confidence = scores[best] / total if total > 0 else 0.0

    return best, confidence, matches[best]


def log_venture_classification(task, venture, confidence, keywords):
    """Append venture classification to state log."""
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    log_file = STATE_DIR / "venture-tags.jsonl"

    entry = {
        "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "task": task[:200],
        "venture": venture,
        "confidence": round(confidence, 2),
        "keywords": keywords[:5],
    }

    with open(log_file, "a") as f:
        f.write(json.dumps(entry) + "\n")


# ── Hermes Extension Interface ────────────────────────────

class VentureTaggerExtension:
    """
    Hermes extension that auto-tags every interaction by venture.
    Enables cross-venture pattern detection and proper memory tagging.
    """

    def __init__(self, agent):
        self.agent = agent
        self.current_venture = "general"
        self.session_ventures = []

    def on_message(self, message):
        """Classify each message by venture."""
        if hasattr(message, "content") and message.content:
            venture, confidence, keywords = classify_venture(message.content)

            if confidence > 0.3:
                self.current_venture = venture
                self.session_ventures.append(venture)

                log_venture_classification(
                    task=message.content[:100],
                    venture=venture,
                    confidence=confidence,
                    keywords=keywords,
                )

    def on_tool_call(self, tool_name, tool_args, context=None):
        """Tag tool calls with current venture context."""
        if tool_args and isinstance(tool_args, dict):
            tool_args["_venture"] = self.current_venture
        return None  # Don't block

    def on_session_end(self, session):
        """Log session venture summary."""
        if self.session_ventures:
            # Count venture mentions in this session
            from collections import Counter
            venture_counts = Counter(self.session_ventures)
            dominant = venture_counts.most_common(1)[0][0]

            log_venture_classification(
                task="SESSION_END_SUMMARY",
                venture=dominant,
                confidence=1.0,
                keywords=[f"{v}:{c}" for v, c in venture_counts.items()],
            )


def create_extension(agent):
    """Factory function for Hermes extension loading."""
    return VentureTaggerExtension(agent)
