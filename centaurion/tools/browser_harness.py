"""
Browser-Harness — Hermes Tool Registration

Registers browser-harness as a Hermes tool, enabling web automation
through the Centaurion agent. Self-healing: the underlying browser-harness
can edit its own helpers.py when encountering new patterns.

Install: copy to ~/.hermes/tools/browser_harness.py
Requires: browser-harness installed (pip install browser-harness)
"""

import subprocess
import json
import os
from pathlib import Path


BROWSER_HARNESS_DIR = os.environ.get(
    "BROWSER_HARNESS_DIR",
    os.path.expanduser("~/browser-harness")
)


def browser_navigate(url: str) -> str:
    """Navigate the browser to a URL and return page info."""
    return _run_browser_command(f"""
from helpers import goto, page_info
goto("{url}")
print(page_info())
""")


def browser_screenshot(filename: str = "screenshot.png") -> str:
    """Take a screenshot of the current browser page."""
    return _run_browser_command(f"""
from helpers import screenshot
screenshot("{filename}")
print("Screenshot saved to {filename}")
""")


def browser_click(x: int, y: int) -> str:
    """Click at coordinates (x, y) on the page."""
    return _run_browser_command(f"""
from helpers import click
click({x}, {y})
print("Clicked at ({x}, {y})")
""")


def browser_type_text(text: str) -> str:
    """Type text into the currently focused element."""
    return _run_browser_command(f"""
from helpers import type_text
type_text("{text}")
print("Typed: {text}")
""")


def browser_js(script: str) -> str:
    """Execute JavaScript in the browser and return the result."""
    return _run_browser_command(f"""
from helpers import js
result = js('''{script}''')
print(result)
""")


def browser_extract_text() -> str:
    """Extract all visible text from the current page."""
    return _run_browser_command("""
from helpers import js
text = js("document.body.innerText")
print(text[:5000])
""")


def _run_browser_command(python_code: str) -> str:
    """Execute a browser command via browser-harness."""
    bh_dir = Path(BROWSER_HARNESS_DIR)
    if not bh_dir.exists():
        return f"Error: browser-harness not found at {BROWSER_HARNESS_DIR}"

    try:
        result = subprocess.run(
            ["python3", "-c", python_code],
            cwd=str(bh_dir),
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return f"Error: {result.stderr.strip()}"
    except subprocess.TimeoutExpired:
        return "Error: Browser command timed out (30s)"
    except Exception as e:
        return f"Error: {str(e)}"


# ── Hermes Tool Registration ─────────────────────────────

TOOLS = {
    "browser_navigate": {
        "function": browser_navigate,
        "description": "Navigate the browser to a URL. Returns page title and info.",
        "parameters": {
            "url": {"type": "string", "description": "The URL to navigate to"}
        },
    },
    "browser_screenshot": {
        "function": browser_screenshot,
        "description": "Take a screenshot of the current browser page.",
        "parameters": {
            "filename": {"type": "string", "description": "Filename for the screenshot", "default": "screenshot.png"}
        },
    },
    "browser_click": {
        "function": browser_click,
        "description": "Click at specific coordinates on the page.",
        "parameters": {
            "x": {"type": "integer", "description": "X coordinate"},
            "y": {"type": "integer", "description": "Y coordinate"},
        },
    },
    "browser_type_text": {
        "function": browser_type_text,
        "description": "Type text into the currently focused element.",
        "parameters": {
            "text": {"type": "string", "description": "Text to type"}
        },
    },
    "browser_js": {
        "function": browser_js,
        "description": "Execute JavaScript in the browser and return the result.",
        "parameters": {
            "script": {"type": "string", "description": "JavaScript code to execute"}
        },
    },
    "browser_extract_text": {
        "function": browser_extract_text,
        "description": "Extract all visible text from the current page (first 5000 chars).",
        "parameters": {},
    },
}


def register_tools(registry):
    """Register all browser tools with Hermes tool registry."""
    for name, tool in TOOLS.items():
        registry.register(
            name=name,
            function=tool["function"],
            description=tool["description"],
            parameters=tool.get("parameters", {}),
        )
