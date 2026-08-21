"""
Wiki Manager — Hermes Tool

CRUD operations for Centaurion venture wikis.
Enables agents to read, create, update, and search wiki content
across AOB, BuilderBee, and Centaurion wikis.

Install: copy to ~/.hermes/tools/wiki_manager.py
"""

import os
import json
from pathlib import Path
from datetime import datetime


CENTAURION_REPO = os.environ.get("CENTAURION_REPO", os.path.expanduser("~/Centaurion"))

WIKI_DIRS = {
    "aob": "docs/aob-wiki",
    "builderbee": "docs/builderbee-wiki",
    "centaurion": "docs/centaurion-wiki",
}


def wiki_list(venture: str = "all") -> str:
    """List all wiki pages for a venture (or all ventures)."""
    repo = Path(CENTAURION_REPO)
    results = {}

    wikis = WIKI_DIRS if venture == "all" else {venture: WIKI_DIRS.get(venture, "")}

    for v, wiki_path in wikis.items():
        full_path = repo / wiki_path
        if full_path.exists():
            pages = sorted(
                f.stem for f in full_path.glob("*.md") if f.name != "README.md"
            )
            results[v] = {"path": wiki_path, "pages": pages, "count": len(pages)}
        else:
            results[v] = {"path": wiki_path, "pages": [], "count": 0, "status": "not found"}

    return json.dumps(results, indent=2)


def wiki_read(venture: str, page: str) -> str:
    """Read a specific wiki page."""
    repo = Path(CENTAURION_REPO)
    wiki_dir = WIKI_DIRS.get(venture)
    if not wiki_dir:
        return f"Unknown venture: {venture}. Use: aob, builderbee, centaurion"

    page_path = repo / wiki_dir / f"{page}.md"
    if not page_path.exists():
        return f"Page not found: {wiki_dir}/{page}.md"

    return page_path.read_text()


def wiki_write(venture: str, page: str, content: str) -> str:
    """Create or update a wiki page."""
    repo = Path(CENTAURION_REPO)
    wiki_dir = WIKI_DIRS.get(venture)
    if not wiki_dir:
        return f"Unknown venture: {venture}. Use: aob, builderbee, centaurion"

    page_path = repo / wiki_dir / f"{page}.md"
    page_path.parent.mkdir(parents=True, exist_ok=True)

    is_new = not page_path.exists()
    page_path.write_text(content)

    action = "Created" if is_new else "Updated"
    return f"{action}: {wiki_dir}/{page}.md ({len(content)} chars)"


def wiki_search(query: str, venture: str = "all") -> str:
    """Search across wiki pages for a keyword or phrase."""
    repo = Path(CENTAURION_REPO)
    results = []

    wikis = WIKI_DIRS if venture == "all" else {venture: WIKI_DIRS.get(venture, "")}

    for v, wiki_path in wikis.items():
        full_path = repo / wiki_path
        if not full_path.exists():
            continue

        for page in full_path.glob("*.md"):
            content = page.read_text()
            if query.lower() in content.lower():
                # Find the matching line for context
                for i, line in enumerate(content.splitlines()):
                    if query.lower() in line.lower():
                        results.append({
                            "venture": v,
                            "page": page.stem,
                            "line": i + 1,
                            "context": line.strip()[:150],
                        })
                        break

    if not results:
        return f"No results for '{query}' across {venture} wikis."

    return json.dumps(results, indent=2)


# ── Hermes Tool Registration ─────────────────────────────

TOOLS = {
    "wiki_list": {
        "function": wiki_list,
        "description": "List all wiki pages. Use venture='all' for all, or 'aob', 'builderbee', 'centaurion'.",
        "parameters": {
            "venture": {"type": "string", "description": "Venture name or 'all'", "default": "all"}
        },
    },
    "wiki_read": {
        "function": wiki_read,
        "description": "Read a specific wiki page content.",
        "parameters": {
            "venture": {"type": "string", "description": "Venture: aob, builderbee, centaurion"},
            "page": {"type": "string", "description": "Page name (without .md extension)"},
        },
    },
    "wiki_write": {
        "function": wiki_write,
        "description": "Create or update a wiki page. Content should be markdown.",
        "parameters": {
            "venture": {"type": "string", "description": "Venture: aob, builderbee, centaurion"},
            "page": {"type": "string", "description": "Page name (without .md extension)"},
            "content": {"type": "string", "description": "Markdown content for the page"},
        },
    },
    "wiki_search": {
        "function": wiki_search,
        "description": "Search across wiki pages for a keyword or phrase.",
        "parameters": {
            "query": {"type": "string", "description": "Search query"},
            "venture": {"type": "string", "description": "Venture to search or 'all'", "default": "all"},
        },
    },
}


def register_tools(registry):
    """Register all wiki tools with Hermes tool registry."""
    for name, tool in TOOLS.items():
        registry.register(
            name=name,
            function=tool["function"],
            description=tool["description"],
            parameters=tool.get("parameters", {}),
        )
