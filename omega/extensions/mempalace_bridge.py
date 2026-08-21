"""
MemPalace Bridge — Hermes Extension

Layer 3: Verbatim archive. Mines Claude conversation exports,
Telegram logs, and agent session transcripts for exact recall.

Uses ChromaDB (vector store) + SQLite locally on VPS2.
Zero API cost — all processing is local.

Install: copy to ~/.hermes/extensions/mempalace_bridge.py
Requires: mempalace installed (pip install mempalace)
"""

import os
import json
from pathlib import Path
from datetime import datetime


CENTAURION_REPO = os.environ.get("CENTAURION_REPO", os.path.expanduser("~/Centaurion"))
MEMPALACE_DIR = os.environ.get("MEMPALACE_DIR", os.path.expanduser("~/.mempalace"))

INGEST_SOURCES = {
    "claude_exports": "~/claude-exports/",
    "hermes_sessions": "~/.hermes/state.db",
    "telegram_logs": "~/nanoclaw/logs/",
    "centaurion_wikis": f"{CENTAURION_REPO}/docs/",
}


def search_archive(query, limit=5):
    """Search the verbatim archive for exact recall."""
    try:
        import mempalace
        mp = mempalace.MemPalace(MEMPALACE_DIR)
        results = mp.search(query, limit=limit)
        return [
            {
                "content": r.get("content", "")[:500],
                "source": r.get("metadata", {}).get("source", "unknown"),
                "date": r.get("metadata", {}).get("date", ""),
                "score": r.get("score", 0),
            }
            for r in results
        ]
    except Exception as e:
        return [{"error": str(e)}]


def ingest_file(filepath, source_tag="manual"):
    """Ingest a single file into the archive."""
    try:
        import mempalace
        mp = mempalace.MemPalace(MEMPALACE_DIR)
        path = Path(filepath).expanduser()
        if not path.exists():
            return {"error": f"File not found: {filepath}"}

        content = path.read_text()
        mp.add(
            content=content,
            metadata={
                "source": source_tag,
                "filename": path.name,
                "date": datetime.utcnow().strftime("%Y-%m-%d"),
                "venture": _detect_venture(content),
            },
        )
        return {"status": "ingested", "file": str(path), "size": len(content)}
    except Exception as e:
        return {"error": str(e)}


def ingest_directory(dirpath, source_tag="batch"):
    """Ingest all markdown/text files from a directory."""
    try:
        import mempalace
        mp = mempalace.MemPalace(MEMPALACE_DIR)
        path = Path(dirpath).expanduser()
        if not path.exists():
            return {"error": f"Directory not found: {dirpath}"}

        count = 0
        for f in path.rglob("*.md"):
            content = f.read_text()
            if len(content) < 50:
                continue
            mp.add(
                content=content,
                metadata={
                    "source": source_tag,
                    "filename": str(f.relative_to(path)),
                    "date": datetime.utcnow().strftime("%Y-%m-%d"),
                    "venture": _detect_venture(content),
                },
            )
            count += 1

        return {"status": "ingested", "directory": str(path), "files": count}
    except Exception as e:
        return {"error": str(e)}


def get_stats():
    """Get archive statistics."""
    try:
        import mempalace
        mp = mempalace.MemPalace(MEMPALACE_DIR)
        return {
            "status": "active",
            "location": MEMPALACE_DIR,
            "backend": "chromadb + sqlite",
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}


def _detect_venture(text):
    """Quick venture detection for tagging."""
    text_lower = text.lower()
    if any(w in text_lower for w in ["aob", "art of breath", "breathwork", "facilitator"]):
        return "aob"
    elif any(w in text_lower for w in ["builderbee", "ghl", "gohighlevel", "client onboarding"]):
        return "builderbee"
    elif any(w in text_lower for w in ["centaurion", "three laws", "precision ratio", "active inference"]):
        return "centaurion"
    return "general"


def get_setup_instructions():
    return """
# MemPalace Setup for Centaurion Centaurion

## Already Done
  pip install mempalace ✓ (ChromaDB + SQLite included)

## Initialize
  python3 -c "import mempalace; mp = mempalace.MemPalace(); print('MemPalace ready')"

## Ingest Centaurion Wikis
  hermes
  > ingest the centaurion wiki docs into mempalace

## Ingest Claude Conversation Exports
  1. Export conversations from claude.ai (Settings → Export)
  2. Place in ~/claude-exports/
  3. hermes > ingest claude exports into mempalace

## Infrastructure Impact
  - RAM: ~100-200MB for ChromaDB
  - Disk: Grows with data (~1MB per 1000 documents)
  - CPU: Embedding generation on ingest (one-time per document)
  - API cost: $0 (all local)

## What MemPalace Answers
  - "Show me the raw conversation where we discussed GHL migration"
  - "What exactly did I say about facilitator selection last month?"
  - "Find the 45-minute debate about Ontraport vs GHL"
"""


# ── Hermes Extension Interface ────────────────────────────

class MemPalaceExtension:
    """
    Hermes extension that provides verbatim archive search
    and ingestion tools via MemPalace (ChromaDB + SQLite).
    """

    def __init__(self, agent):
        self.agent = agent

    def on_session_start(self, session):
        """Register MemPalace tools."""
        if hasattr(self.agent, 'register_tool'):
            self.agent.register_tool(
                name="mempalace_search",
                function=search_archive,
                description="Search the verbatim archive for exact recall of past conversations and documents.",
                parameters={
                    "query": {"type": "string", "description": "Search query"},
                    "limit": {"type": "integer", "description": "Max results", "default": 5},
                },
            )
            self.agent.register_tool(
                name="mempalace_ingest",
                function=ingest_file,
                description="Ingest a file into the verbatim archive for future recall.",
                parameters={
                    "filepath": {"type": "string", "description": "Path to file"},
                    "source_tag": {"type": "string", "description": "Source label", "default": "manual"},
                },
            )
            self.agent.register_tool(
                name="mempalace_ingest_dir",
                function=ingest_directory,
                description="Ingest all markdown files from a directory into the archive.",
                parameters={
                    "dirpath": {"type": "string", "description": "Directory path"},
                    "source_tag": {"type": "string", "description": "Source label", "default": "batch"},
                },
            )
            self.agent.register_tool(
                name="mempalace_stats",
                function=get_stats,
                description="Get MemPalace archive statistics.",
                parameters={},
            )

    def on_session_end(self, session):
        """Auto-archive session transcript."""
        if not hasattr(session, 'messages') or not session.messages:
            return

        user_msgs = [m.get('content', '') for m in session.messages if m.get('role') == 'user']
        if not user_msgs:
            return

        transcript = "\n---\n".join(user_msgs[:20])
        if len(transcript) < 100:
            return

        try:
            ingest_file_content(
                content=transcript,
                source_tag="hermes-session",
                filename=f"session-{datetime.utcnow().strftime('%Y%m%d-%H%M')}.md",
            )
        except Exception:
            pass


def ingest_file_content(content, source_tag="auto", filename="auto"):
    """Ingest raw content (not from file)."""
    try:
        import mempalace
        mp = mempalace.MemPalace(MEMPALACE_DIR)
        mp.add(
            content=content,
            metadata={
                "source": source_tag,
                "filename": filename,
                "date": datetime.utcnow().strftime("%Y-%m-%d"),
                "venture": _detect_venture(content),
            },
        )
    except Exception:
        pass


def create_extension(agent):
    """Factory function for Hermes extension loading."""
    return MemPalaceExtension(agent)
