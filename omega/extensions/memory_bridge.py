"""
Memory Bridge — Hermes Extension

Syncs Hermes's memory system with Centaurion's Supermemory.
On session_end: captures interaction summary → Supermemory.
On session_start: recalls recent Supermemory context → injects into session.

This IS the Coupling Law made operational across runtimes.

Install: copy to ~/.hermes/extensions/memory_bridge.py
Requires: SUPERMEMORY_API_KEY in environment or ~/.hermes/.env
"""

import json
import os
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime


CENTAURION_REPO = os.environ.get("CENTAURION_REPO", os.path.expanduser("~/Centaurion"))
SUPERMEMORY_API_KEY = os.environ.get("SUPERMEMORY_API_KEY", "")
SUPERMEMORY_WRITE_URL = "https://api.supermemory.ai/v3/documents"
SUPERMEMORY_SEARCH_URL = "https://api.supermemory.ai/v3/search"

VENTURE_CONTAINERS = {
    "aob": "centaurion-aob",
    "builderbee": "centaurion-builderbee",
    "centaurion": "centaurion-framework",
    "general": "centaurion-malik",
}


def _load_api_key():
    """Load Supermemory API key from env or .env files."""
    global SUPERMEMORY_API_KEY
    if SUPERMEMORY_API_KEY:
        return SUPERMEMORY_API_KEY

    for env_path in [
        Path(CENTAURION_REPO) / ".env",
        Path.home() / ".hermes" / ".env",
        Path.home() / "Centaurion" / ".env",
    ]:
        if env_path.exists():
            for line in env_path.read_text().splitlines():
                if line.startswith("SUPERMEMORY_API_KEY="):
                    SUPERMEMORY_API_KEY = line.split("=", 1)[1].strip().strip('"')
                    return SUPERMEMORY_API_KEY
    return ""


def capture_to_supermemory(content, venture="general", metadata=None):
    """Write a memory document to Supermemory."""
    api_key = _load_api_key()
    if not api_key:
        return {"error": "No SUPERMEMORY_API_KEY configured"}

    container = VENTURE_CONTAINERS.get(venture, VENTURE_CONTAINERS["general"])

    payload = {
        "content": content,
        "spaces": [container],
        "metadata": metadata or {},
    }

    req = urllib.request.Request(
        SUPERMEMORY_WRITE_URL,
        data=json.dumps(payload).encode(),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.URLError as e:
        return {"error": str(e)}


def recall_from_supermemory(query, venture="general", limit=3):
    """Search Supermemory for relevant context."""
    api_key = _load_api_key()
    if not api_key:
        return []

    container = VENTURE_CONTAINERS.get(venture, VENTURE_CONTAINERS["general"])

    payload = {
        "query": query,
        "spaces": [container],
        "limit": limit,
    }

    req = urllib.request.Request(
        SUPERMEMORY_SEARCH_URL,
        data=json.dumps(payload).encode(),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            return data.get("results", [])
    except urllib.error.URLError:
        return []


def _summarize_session(messages):
    """Extract a brief summary from session messages for capture."""
    user_msgs = [m.get("content", "") for m in messages if m.get("role") == "user"]
    assistant_msgs = [m.get("content", "") for m in messages if m.get("role") == "assistant"]

    topics = " | ".join(user_msgs[:5])
    if len(topics) > 500:
        topics = topics[:500]

    return f"Session topics: {topics}"


# ── Hermes Extension Interface ────────────────────────────

class MemoryBridgeExtension:
    """
    Hermes extension that bridges Supermemory with Hermes sessions.
    Captures session summaries on end, recalls context on start.
    """

    def __init__(self, agent):
        self.agent = agent
        self.session_venture = "general"
        self.recalled_context = None

    def on_session_start(self, session):
        """Recall recent context from Supermemory."""
        results = recall_from_supermemory(
            "recent work and context",
            venture="general",
            limit=3,
        )

        if results:
            context_text = "\n".join(
                r.get("content", "")[:200] for r in results
            )
            self.recalled_context = context_text

    def on_message(self, message):
        """Detect venture from message content."""
        if hasattr(message, "content"):
            from centaurion_core import detect_venture
            self.session_venture = detect_venture(message.content)

    def on_session_end(self, session):
        """Capture session summary to Supermemory."""
        if hasattr(session, "messages") and session.messages:
            summary = _summarize_session(session.messages)
            timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

            capture_to_supermemory(
                content=f"[{timestamp}] {summary}",
                venture=self.session_venture,
                metadata={
                    "source": "hermes-centaurion",
                    "venture": self.session_venture,
                    "timestamp": timestamp,
                },
            )


def create_extension(agent):
    """Factory function for Hermes extension loading."""
    return MemoryBridgeExtension(agent)
