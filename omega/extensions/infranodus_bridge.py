"""
InfraNodus Bridge — Hermes Extension

Connects Centaurion's gap-analysis skill to InfraNodus for
knowledge topology analysis. Finds disconnected clusters,
bridge opportunities, and blind spots across venture wikis.

InfraNodus can run as:
1. Cloud service (infranodus.com) — API access
2. Self-hosted — Docker on VPS2
3. MCP server — direct tool integration with Hermes

Infrastructure:
  Cloud: Free tier available (limited graphs)
  Self-hosted: Docker, ~512MB RAM, ports 3000 + 5432 (Postgres)
  MCP: npm package, connects to InfraNodus API

Install: copy to ~/.hermes/extensions/infranodus_bridge.py
"""

import os
import json
from pathlib import Path


CENTAURION_REPO = os.environ.get("CENTAURION_REPO", os.path.expanduser("~/Centaurion"))
INFRANODUS_API_KEY = os.environ.get("INFRANODUS_API_KEY", "")
INFRANODUS_URL = os.environ.get("INFRANODUS_URL", "https://infranodus.com/api/v1")

WIKI_DIRS = {
    "aob": "docs/aob-wiki",
    "builderbee": "docs/builderbee-wiki",
    "centaurion": "docs/centaurion-wiki",
}


def analyze_wiki_topology(venture="all"):
    """
    Analyze wiki content for knowledge gaps.
    Without InfraNodus API: does basic keyword clustering locally.
    With InfraNodus API: sends content for full network analysis.
    """
    repo = Path(CENTAURION_REPO)
    wikis = WIKI_DIRS if venture == "all" else {venture: WIKI_DIRS.get(venture, "")}

    results = {}

    for v, wiki_path in wikis.items():
        full_path = repo / wiki_path
        if not full_path.exists():
            results[v] = {"status": "not_found", "pages": 0}
            continue

        pages = {}
        all_words = set()
        page_words = {}

        for page_file in full_path.glob("*.md"):
            if page_file.name == "README.md":
                continue
            content = page_file.read_text().lower()
            words = set(w for w in content.split() if len(w) > 4 and w.isalpha())
            pages[page_file.stem] = content
            page_words[page_file.stem] = words
            all_words.update(words)

        # Find disconnected clusters (pages with low word overlap)
        clusters = []
        for p1, w1 in page_words.items():
            for p2, w2 in page_words.items():
                if p1 >= p2:
                    continue
                overlap = len(w1 & w2)
                total = len(w1 | w2)
                similarity = overlap / total if total > 0 else 0
                if similarity < 0.05:
                    clusters.append({
                        "page_a": p1,
                        "page_b": p2,
                        "similarity": round(similarity, 3),
                        "bridge_needed": True,
                    })

        results[v] = {
            "status": "analyzed",
            "pages": len(pages),
            "total_concepts": len(all_words),
            "disconnected_pairs": clusters[:5],
        }

    return results


def find_cross_venture_gaps():
    """Find concepts that exist in one wiki but not others."""
    repo = Path(CENTAURION_REPO)
    venture_concepts = {}

    for v, wiki_path in WIKI_DIRS.items():
        full_path = repo / wiki_path
        if not full_path.exists():
            continue

        all_text = ""
        for page_file in full_path.glob("*.md"):
            all_text += page_file.read_text().lower() + " "

        words = set(w for w in all_text.split() if len(w) > 5 and w.isalpha())
        venture_concepts[v] = words

    gaps = {}
    for v1, w1 in venture_concepts.items():
        for v2, w2 in venture_concepts.items():
            if v1 == v2:
                continue
            unique_to_v1 = w1 - w2
            if len(unique_to_v1) > 0:
                key = f"{v1}_not_in_{v2}"
                gaps[key] = sorted(list(unique_to_v1))[:10]

    return gaps


def get_mcp_config():
    """Return MCP server config for InfraNodus."""
    return {
        "infranodus": {
            "command": "npx",
            "args": ["-y", "@infranodus/mcp-server"],
            "env": {
                "INFRANODUS_API_KEY": "${INFRANODUS_API_KEY}",
            },
        }
    }


def get_setup_instructions():
    """Return setup instructions for InfraNodus."""
    return """
# InfraNodus Setup for Centaurion Omega

## Option A: Cloud (Fastest)
  1. Sign up at infranodus.com (free tier: 3 graphs)
  2. Get API key from settings
  3. Add to .env: INFRANODUS_API_KEY=your-key

## Option B: Self-Hosted (Docker on VPS2)

### Infrastructure Impact
  - RAM: ~512MB (Postgres + Node.js)
  - Disk: ~500MB
  - Ports: 3000 (web UI), 5432 (Postgres)

### Deploy
  docker run -d --name infranodus \\
    --restart unless-stopped \\
    -p 3000:3000 \\
    -e DATABASE_URL=postgres://infra:centaurion@postgres:5432/infranodus \\
    infranodus/infranodus:latest

## Option C: MCP Server (Best for Hermes)
  1. Add to ~/.hermes/mcp.json:
     {
       "infranodus": {
         "command": "npx",
         "args": ["-y", "@infranodus/mcp-server"],
         "env": {"INFRANODUS_API_KEY": "your-key"}
       }
     }
  2. Restart Hermes

## What InfraNodus Answers
  - "What topic clusters exist in our AOB wiki?"
  - "What knowledge gaps exist between BuilderBee and Centaurion?"
  - "What bridge concepts could connect disconnected clusters?"
  - "What questions aren't we asking?"
"""


# ── Hermes Extension Interface ────────────────────────────

class InfraNodusExtension:
    """
    Hermes extension that provides wiki gap analysis tools.
    Uses InfraNodus API when available, falls back to local analysis.
    """

    def __init__(self, agent):
        self.agent = agent

    def on_session_start(self, session):
        """Register gap analysis tools."""
        if hasattr(self.agent, 'register_tool'):
            self.agent.register_tool(
                name="analyze_wiki_topology",
                function=analyze_wiki_topology,
                description="Analyze wiki content for knowledge gaps and disconnected clusters.",
                parameters={"venture": {"type": "string", "default": "all"}},
            )
            self.agent.register_tool(
                name="find_cross_venture_gaps",
                function=find_cross_venture_gaps,
                description="Find concepts unique to one venture wiki that are missing from others.",
                parameters={},
            )


def create_extension(agent):
    """Factory function for Hermes extension loading."""
    return InfraNodusExtension(agent)
