"""
Graphiti Bridge — Hermes Extension

Connects Centaurion to a Graphiti temporal knowledge graph backed by Neo4j.
Tracks HOW facts and relationships change over time — not just what's true now.

This IS the Coupling Law at its deepest: the system tracks the evolution
of its own model of reality.

Install: copy to ~/.hermes/extensions/graphiti_bridge.py
Requires: Neo4j running (Docker), graphiti-core installed (pip)

Infrastructure:
  Neo4j: Docker container on VPS2, ports 7474 (HTTP) + 7687 (Bolt)
  RAM: ~512MB-1GB for Neo4j
  Disk: ~200MB base + grows with data
  Graphiti: Python library, connects via Bolt protocol
"""

import os
import json
from pathlib import Path
from datetime import datetime


CENTAURION_REPO = os.environ.get("CENTAURION_REPO", os.path.expanduser("~/Centaurion"))

# Neo4j connection defaults (override via env)
NEO4J_URI = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.environ.get("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.environ.get("NEO4J_PASSWORD", "")
GRAPHITI_MCP_PORT = int(os.environ.get("GRAPHITI_MCP_PORT", "8765"))

# Centaurion entities to seed the graph with
SEED_ENTITIES = {
    "people": [
        {"name": "Malik Palamar", "role": "operator", "ventures": ["aob", "builderbee", "centaurion"]},
        {"name": "Anthony", "role": "AOB Founder & Lead"},
        {"name": "Chrissy", "role": "AOB Operations"},
        {"name": "Anna", "role": "AOB Program Director"},
        {"name": "Renārs", "role": "AOB Technical"},
        {"name": "Amy", "role": "AOB Marketing"},
        {"name": "Tania", "role": "AOB Community"},
        {"name": "Katerina", "role": "AOB Admin"},
        {"name": "Moni", "role": "AOB Support"},
    ],
    "tools": [
        {"name": "GoHighLevel", "type": "CRM/automation", "ventures": ["aob", "builderbee"]},
        {"name": "Ontraport", "type": "CRM (migrating from)", "ventures": ["aob"]},
        {"name": "Mighty Networks", "type": "community platform", "ventures": ["aob"]},
        {"name": "Hermes Agent", "type": "AI agent runtime", "ventures": ["centaurion"]},
        {"name": "Claude Code", "type": "AI dev tool", "ventures": ["centaurion"]},
        {"name": "NanoClaw", "type": "AI agent (Nova)", "ventures": ["centaurion"]},
        {"name": "Supermemory", "type": "shared memory bus", "ventures": ["centaurion"]},
    ],
    "ventures": [
        {"name": "AOB", "full_name": "Art of Breath", "role": "Head of IT"},
        {"name": "BuilderBee", "full_name": "BuilderBee AI", "role": "Fractional CEO"},
        {"name": "Centaurion", "full_name": "Centaurion.me", "role": "Founder"},
    ],
    "concepts": [
        {"name": "Three Laws", "type": "governance framework"},
        {"name": "Precision Ratio", "type": "optimization target"},
        {"name": "Active Inference", "type": "execution loop"},
        {"name": "Routing Gate", "type": "decision classifier"},
        {"name": "Markov Blanket", "type": "boundary concept"},
    ],
}


def get_docker_compose():
    """Return Docker Compose config for Neo4j."""
    return """
# Neo4j for Centaurion Graphiti — add to docker-compose.yml
services:
  neo4j:
    image: neo4j:5-community
    container_name: centaurion-neo4j
    restart: unless-stopped
    ports:
      - "7474:7474"   # HTTP browser
      - "7687:7687"   # Bolt protocol
    environment:
      NEO4J_AUTH: neo4j/${NEO4J_PASSWORD:-centaurion2026}
      NEO4J_PLUGINS: '["apoc"]'
      NEO4J_server_memory_heap_initial__size: 256m
      NEO4J_server_memory_heap_max__size: 512m
    volumes:
      - neo4j-data:/data
      - neo4j-logs:/logs

volumes:
  neo4j-data:
  neo4j-logs:
"""


def get_setup_instructions():
    """Return setup instructions for Graphiti + Neo4j."""
    return """
# Graphiti + Neo4j Setup for Centaurion

## Infrastructure Impact
  - RAM: ~512MB-1GB for Neo4j (your VPS2 has 56% memory used, should be fine)
  - Disk: ~200MB base, grows with data
  - Ports: 7474 (Neo4j browser), 7687 (Bolt protocol)
  - CPU: Minimal except during graph traversals

## 1. Deploy Neo4j (Docker)
   docker run -d --name centaurion-neo4j \\
     --restart unless-stopped \\
     -p 7474:7474 -p 7687:7687 \\
     -e NEO4J_AUTH=neo4j/centaurion2026 \\
     -e NEO4J_PLUGINS='["apoc"]' \\
     -e NEO4J_server_memory_heap_initial__size=256m \\
     -e NEO4J_server_memory_heap_max__size=512m \\
     -v neo4j-data:/data \\
     neo4j:5-community

## 2. Install Graphiti
   pip3 install graphiti-core --break-system-packages

## 3. Add to Hermes .env
   echo 'NEO4J_URI=bolt://localhost:7687' >> ~/.hermes/.env
   echo 'NEO4J_USER=neo4j' >> ~/.hermes/.env
   echo 'NEO4J_PASSWORD=centaurion2026' >> ~/.hermes/.env

## 4. Seed the graph
   python3 -c "from centaurion.extensions.graphiti_bridge import seed_graph; seed_graph()"

## 5. Verify
   # Open Neo4j browser at http://your-vps2-ip:7474
   # Run: MATCH (n) RETURN n LIMIT 25

## What Graphiti Answers
  - "When did we decide to migrate from Ontraport?"
  - "How has Anna's role evolved over the last 6 months?"
  - "What tools are shared between AOB and BuilderBee?"
  - "What changed about the GHL migration plan since March?"
"""


def seed_graph():
    """Seed the Neo4j graph with Centaurion entities."""
    try:
        from graphiti_core import Graphiti
    except ImportError:
        print("graphiti-core not installed. Run: pip3 install graphiti-core")
        return

    try:
        g = Graphiti(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
    except Exception as e:
        print(f"Cannot connect to Neo4j at {NEO4J_URI}: {e}")
        return

    timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

    for category, entities in SEED_ENTITIES.items():
        for entity in entities:
            g.add_episode(
                name=f"seed_{category}_{entity['name']}",
                body=json.dumps(entity),
                source="centaurion-seed",
                timestamp=timestamp,
            )
    print(f"Seeded {sum(len(v) for v in SEED_ENTITIES.values())} entities into graph")


# ── Hermes Extension Interface ────────────────────────────

class GraphitiBridgeExtension:
    """
    Hermes extension that logs entity changes to Graphiti.
    Captures temporal relationships — when facts change.
    """

    def __init__(self, agent):
        self.agent = agent
        self.graphiti = None
        self._connect()

    def _connect(self):
        """Try to connect to Graphiti/Neo4j."""
        if not NEO4J_PASSWORD:
            return
        try:
            from graphiti_core import Graphiti
            self.graphiti = Graphiti(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
        except Exception:
            self.graphiti = None

    def on_session_end(self, session):
        """Log session context as a temporal episode."""
        if not self.graphiti:
            return

        if hasattr(session, 'messages') and session.messages:
            user_msgs = [m.get('content', '') for m in session.messages if m.get('role') == 'user']
            summary = ' | '.join(user_msgs[:3])[:500]

            try:
                self.graphiti.add_episode(
                    name=f"session_{datetime.utcnow().strftime('%Y%m%d_%H%M')}",
                    body=summary,
                    source="hermes-centaurion",
                    timestamp=datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
                )
            except Exception:
                pass


def create_extension(agent):
    """Factory function for Hermes extension loading."""
    return GraphitiBridgeExtension(agent)
