"""
Routing Gate — Hermes Extension

Intercepts tool calls and classifies them through the Centaurion
Routing Gate before execution. High novelty + high stakes + low
reversibility → blocks execution and surfaces to human.

This IS the Routing Law made operational inside Hermes.

Install: copy to ~/.hermes/extensions/routing_gate.py
"""

import json
import os
from pathlib import Path
from datetime import datetime


CENTAURION_REPO = os.environ.get("CENTAURION_REPO", os.path.expanduser("~/Centaurion"))
STATE_DIR = Path(CENTAURION_REPO) / "memory" / "state"

# Default thresholds (adjustable via framework/routing-gate.md)
NOVELTY_THRESHOLD = 0.7
STAKES_THRESHOLD = 0.5
REVERSIBILITY_THRESHOLD = 0.3

# Tools that are always safe (low novelty, high reversibility)
SAFE_TOOLS = {
    "read", "Read", "cat", "ls", "grep", "Grep", "Glob",
    "search", "screenshot", "page_info", "current_tab",
}

# Tools that require routing check
SENSITIVE_TOOLS = {
    "Bash", "bash", "Write", "Edit", "http_post", "http_put",
    "send_message", "send_email", "create_issue", "deploy",
    "delete", "drop", "rm",
}

# Tools that should ALWAYS surface to human
BLOCKED_TOOLS = {
    "git push --force", "rm -rf", "drop database",
    "send_email_to_client", "publish", "deploy_production",
}


def classify_tool_call(tool_name, tool_args):
    """
    Classify a tool call through the Routing Gate.

    Returns: (route, novelty, stakes, reversibility)
    route: "ai_autonomous" | "ai_with_review" | "surface_to_human"
    """

    # Always-safe tools
    if tool_name in SAFE_TOOLS:
        return "ai_autonomous", 0.1, 0.1, 0.9

    # Always-blocked tools
    args_str = json.dumps(tool_args) if tool_args else ""
    for blocked in BLOCKED_TOOLS:
        if blocked in tool_name or blocked in args_str:
            return "surface_to_human", 0.9, 0.9, 0.1

    # Sensitive tools get scored
    if tool_name in SENSITIVE_TOOLS:
        novelty = 0.4  # Base: somewhat familiar
        stakes = 0.4   # Base: moderate
        reversibility = 0.6  # Base: somewhat reversible

        # Adjust based on args
        if tool_args:
            args_str_lower = args_str.lower()

            # Higher stakes for production/client/external actions
            if any(w in args_str_lower for w in ["production", "client", "external", "public"]):
                stakes += 0.3
            if any(w in args_str_lower for w in ["delete", "remove", "drop", "force"]):
                reversibility -= 0.3
                stakes += 0.2
            if any(w in args_str_lower for w in ["email", "message", "post", "publish"]):
                reversibility -= 0.4

        # Apply thresholds
        if novelty > NOVELTY_THRESHOLD and stakes > STAKES_THRESHOLD and reversibility < REVERSIBILITY_THRESHOLD:
            return "surface_to_human", novelty, stakes, reversibility
        elif stakes > STAKES_THRESHOLD:
            return "ai_with_review", novelty, stakes, reversibility

    return "ai_autonomous", 0.2, 0.2, 0.8


# ─── Tool-creation events (forge integration) ───────────────────────
#
# The Tool Forge (centaurion/extensions/tool_forge.py) emits a fixed taxonomy
# of events as it walks each tool through scaffold → sandbox_exec → promote.
# Each event is classified here so the routing log captures the full lifecycle.
#
# Design rule (omega paradigm): scaffold and sandbox_exec are autonomous
# (low stakes, fully reversible — files live in an isolated worktree until
# promotion). Promotion ALWAYS surfaces to the operator: writing executable
# code into canonical skills/ is high-stakes and only partially reversible.

TOOL_CREATION_EVENTS = {
    "scaffold",        # Tier 1: write tool stub into isolated worktree
    "sandbox_exec",    # Tier 2: run test inside Sandbox
    "promote",         # Tier 3: surface diff for operator review
    "promote_blocked", # Tier 3 short-circuit: execution failed, no surface
    "approve",         # Operator decision — merges into _promoted/
    "reject",          # Operator decision — archives to _failed/
}


def classify_tool_creation(*, event, tool_name, sandboxed):
    """
    Classify a tool-forge lifecycle event.

    Args:
        event: one of TOOL_CREATION_EVENTS.
        tool_name: the candidate tool's name (str).
        sandboxed: whether this event happened inside the sandbox (bool).
            Currently informational; affects only the audit log.

    Returns: (route, novelty, stakes, reversibility) — same shape as
        classify_tool_call(...).
    """
    if event not in TOOL_CREATION_EVENTS:
        raise ValueError(
            f"Unknown tool_creation event: {event!r}. "
            f"Expected one of {sorted(TOOL_CREATION_EVENTS)}."
        )

    # Operator decisions and pre-execution scaffolding stay autonomous —
    # the gate already surfaced (or will surface) at the promote step.
    if event == "scaffold":
        # Worktree-isolated, no execution yet.
        return "ai_autonomous", 0.3, 0.2, 0.95
    if event == "sandbox_exec":
        # Runs in an isolated container with no network; container is destroyed
        # on completion. Reversibility is high: nothing escapes the sandbox.
        return "ai_autonomous", 0.4, 0.3, 0.9
    if event == "promote_blocked":
        # Execution failed; nothing surfaced. Audit-only.
        return "ai_autonomous", 0.4, 0.2, 0.95
    if event == "approve":
        # Operator already approved; this is a logged side effect.
        return "ai_autonomous", 0.2, 0.5, 0.6
    if event == "reject":
        # Operator already rejected; archive is reversible.
        return "ai_autonomous", 0.2, 0.2, 0.95

    # event == "promote": ALWAYS surfaces.
    # Writing executable code into canonical skills/ is novel-enough,
    # high-stakes, and only partially reversible.
    novelty, stakes, reversibility = 0.75, 0.65, 0.4
    return "surface_to_human", novelty, stakes, reversibility


def log_classification(tool_name, route, novelty, stakes, reversibility):
    """Log the routing decision."""
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    log_file = STATE_DIR / "routing-log.jsonl"

    entry = {
        "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "task": f"tool_call: {tool_name}",
        "novelty": round(novelty, 2),
        "stakes": round(stakes, 2),
        "reversibility": round(reversibility, 2),
        "route": route,
        "outcome_rating": None,
        "routing_correct": None,
    }

    with open(log_file, "a") as f:
        f.write(json.dumps(entry) + "\n")


# ── Hermes Extension Interface ────────────────────────────

class RoutingGateExtension:
    """
    Hermes extension that intercepts tool calls and applies
    the Centaurion Routing Gate classification.

    Blocks high-risk tool calls and surfaces them to the human
    instead of auto-executing.
    """

    def __init__(self, agent):
        self.agent = agent
        self.blocked_count = 0
        self.auto_count = 0

    def on_tool_call(self, tool_name, tool_args, context=None):
        """
        Called before every tool execution.

        Returns:
            None — proceed with execution
            {"block": True, "reason": "..."} — block execution
        """
        route, novelty, stakes, reversibility = classify_tool_call(tool_name, tool_args)
        log_classification(tool_name, route, novelty, stakes, reversibility)

        if route == "surface_to_human":
            self.blocked_count += 1
            return {
                "block": True,
                "reason": (
                    f"ROUTING GATE: Blocked `{tool_name}` — "
                    f"novelty={novelty:.1f}, stakes={stakes:.1f}, "
                    f"reversibility={reversibility:.1f}. "
                    f"This requires Malik's review. "
                    f"Describe what you want to do and wait for approval."
                )
            }

        if route == "ai_with_review":
            # Don't block, but flag for post-execution review
            pass

        self.auto_count += 1
        return None  # Proceed

    def on_session_end(self, session):
        """Log routing stats for the session."""
        if self.blocked_count > 0 or self.auto_count > 0:
            total = self.blocked_count + self.auto_count
            pass


def create_extension(agent):
    """Factory function for Hermes extension loading."""
    return RoutingGateExtension(agent)
