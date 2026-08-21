"""
Routing Gate — Hermes Extension + composable core.

The Centaurion Routing Law made operational: every non-trivial action is
classified through (novelty × stakes × reversibility) and either auto-executed,
flagged for review, or surfaced to the operator.

This module exposes both:

  - **Top-level functions** (`classify_tool_call`, `classify_tool_creation`,
    `log_classification`, `RoutingGateExtension`) — backward-compatible API
    used by Hermes and the dev_loop.
  - **Composable core** (§14.4 refactor) — four ABCs that make every dimension
    swappable:
        * `StorageBackend`     — where decisions are persisted
        * `OperatorProfile`    — operator-specific calibration vector
        * `ThresholdPolicy`    — base + calibrated thresholds
        * `EscalationChannel`  — surfaces decisions when route == surface_to_human
    Composed together by `RoutingGate(...)`.

The top-level functions delegate to a default `RoutingGate` instance with
sensible defaults: JsonlFileBackend(memory/state/routing-log.jsonl),
DefaultOperatorProfile, StaticThresholdPolicy(0.7, 0.5, 0.3), NullEscalationChannel.

Install (Hermes): copy to ~/.hermes/extensions/routing_gate.py
"""

from __future__ import annotations

import json
import os
import re
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Optional


# ─── Paths ──────────────────────────────────────────────────────────


CENTAURION_REPO = os.environ.get(
    "CENTAURION_REPO", os.path.expanduser("~/Centaurion")
)
STATE_DIR = Path(CENTAURION_REPO) / "memory" / "state"


# ─── Tool taxonomy (legacy, retained) ──────────────────────────────


SAFE_TOOLS = {
    "read", "Read", "cat", "ls", "grep", "Grep", "Glob",
    "search", "screenshot", "page_info", "current_tab",
}

SENSITIVE_TOOLS = {
    "Bash", "bash", "Write", "Edit", "http_post", "http_put",
    "send_message", "send_email", "create_issue", "deploy",
    "delete", "drop", "rm",
}

BLOCKED_TOOLS = {
    "git push --force", "rm -rf", "drop database",
    "send_email_to_client", "publish", "deploy_production",
}


# ─── Tool-creation events (forge integration) ───────────────────────

TOOL_CREATION_EVENTS = {
    "scaffold",
    "sandbox_exec",
    "promote",
    "promote_blocked",
    "approve",
    "reject",
}


# ═══════════════════════════════════════════════════════════════════
#                       §14.4 — INTERFACES
# ═══════════════════════════════════════════════════════════════════


# ─── Thresholds value object ──────────────────────────────────────


@dataclass(frozen=True)
class Thresholds:
    """Immutable threshold tuple. The Routing Gate inequality reads:

        novelty > T.novelty ∧ stakes > T.stakes ∧ reversibility < T.reversibility
            ⇒ surface_to_human
    """

    novelty: float = 0.7
    stakes: float = 0.5
    reversibility: float = 0.3

    def adjusted(self, calibration: dict) -> "Thresholds":
        """Return a new Thresholds offset by `calibration` and clamped to [0, 1]."""
        def _clamp(x: float) -> float:
            return max(0.0, min(1.0, x))
        return Thresholds(
            novelty=_clamp(self.novelty + calibration.get("novelty", 0.0)),
            stakes=_clamp(self.stakes + calibration.get("stakes", 0.0)),
            reversibility=_clamp(self.reversibility + calibration.get("reversibility", 0.0)),
        )


# ─── StorageBackend ────────────────────────────────────────────────


class StorageBackend(ABC):
    """Persists routing-classification entries."""

    @abstractmethod
    def append(self, entry: dict) -> None: ...

    @abstractmethod
    def read_all(self) -> list[dict]: ...


@dataclass
class JsonlFileBackend(StorageBackend):
    """JSONL on disk. Default backend for production."""

    path: Path

    def __init__(self, path):
        self.path = Path(path)

    def append(self, entry: dict) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a") as f:
            f.write(json.dumps(entry) + "\n")

    def read_all(self) -> list[dict]:
        if not self.path.exists():
            return []
        return [
            json.loads(line)
            for line in self.path.read_text().splitlines()
            if line.strip()
        ]


@dataclass
class InMemoryBackend(StorageBackend):
    """In-process backend for tests and short-lived processes."""

    _entries: list[dict] = field(default_factory=list)

    def append(self, entry: dict) -> None:
        self._entries.append(dict(entry))

    def read_all(self) -> list[dict]:
        return list(self._entries)


# ─── OperatorProfile ───────────────────────────────────────────────


class OperatorProfile(ABC):
    """Operator-specific threshold calibration.

    Returns a dict with optional keys 'novelty', 'stakes', 'reversibility'
    that adjust the base thresholds (positive = more conservative for novelty
    and stakes; positive = require more reversibility before surfacing).
    """

    @abstractmethod
    def calibration(self) -> dict[str, float]: ...


class DefaultOperatorProfile(OperatorProfile):
    """No calibration — uses base thresholds verbatim."""

    def calibration(self) -> dict[str, float]:
        return {}


_BASELINE_LINE = re.compile(
    r"^\s*[-*]\s*(novelty|stakes|reversibility)\s*:\s*([+-]?\d*\.?\d+)\s*$",
    re.IGNORECASE,
)


@dataclass
class TelosOperatorProfile(OperatorProfile):
    """Reads `BASELINE-INTEGRAL.md` from a TELOS identity directory.

    Adjustments are parsed from list items under the heading
    `## Routing Gate Adjustments`, e.g.::

        ## Routing Gate Adjustments
        - novelty: -0.1
        - stakes: +0.05
        - reversibility: 0
    """

    identity_dir: Path

    def __init__(self, identity_dir):
        self.identity_dir = Path(identity_dir)

    def calibration(self) -> dict[str, float]:
        baseline = self.identity_dir / "BASELINE-INTEGRAL.md"
        if not baseline.exists():
            return {}
        adjustments: dict[str, float] = {}
        in_section = False
        for raw in baseline.read_text().splitlines():
            stripped = raw.strip()
            if stripped.startswith("##"):
                in_section = "routing gate adjustments" in stripped.lower()
                continue
            if not in_section:
                continue
            match = _BASELINE_LINE.match(raw)
            if match:
                key = match.group(1).lower()
                adjustments[key] = float(match.group(2))
        return adjustments


# ─── ThresholdPolicy ──────────────────────────────────────────────


class ThresholdPolicy(ABC):
    """Returns the active Thresholds tuple."""

    @abstractmethod
    def thresholds(self) -> Thresholds: ...


@dataclass
class StaticThresholdPolicy(ThresholdPolicy):
    """Fixed Thresholds — no calibration."""

    _t: Thresholds = field(default_factory=Thresholds)

    def __init__(self, thresholds: Optional[Thresholds] = None):
        self._t = thresholds if thresholds is not None else Thresholds()

    def thresholds(self) -> Thresholds:
        return self._t


@dataclass
class CalibratedThresholdPolicy(ThresholdPolicy):
    """Composes a base ThresholdPolicy with an OperatorProfile's calibration."""

    base: ThresholdPolicy
    operator: OperatorProfile

    def thresholds(self) -> Thresholds:
        return self.base.thresholds().adjusted(self.operator.calibration())


# ─── EscalationChannel ────────────────────────────────────────────


class EscalationChannel(ABC):
    """Surfaces a classification when route == surface_to_human."""

    @abstractmethod
    def escalate(self, classification: dict) -> None: ...


@dataclass
class NullEscalationChannel(EscalationChannel):
    """No-op escalation that records what would have been surfaced.

    Useful in tests, in dry-run modes, and when escalation happens via a
    separate channel (e.g., a chatbot that already shows the classification).
    """

    escalations: list[dict] = field(default_factory=list)

    def escalate(self, classification: dict) -> None:
        self.escalations.append(dict(classification))


class StderrEscalationChannel(EscalationChannel):
    """Prints surfaced decisions to stderr — for terminal/CLI agents."""

    def escalate(self, classification: dict) -> None:
        task = classification.get("task", classification.get("tool_name", "?"))
        n = classification.get("novelty", "?")
        s = classification.get("stakes", "?")
        r = classification.get("reversibility", "?")
        print(
            f"[ROUTING GATE] surface to operator: {task} "
            f"(n={n}, s={s}, r={r})",
            file=sys.stderr,
        )


# ═══════════════════════════════════════════════════════════════════
#                  Composed RoutingGate (§14.4)
# ═══════════════════════════════════════════════════════════════════


@dataclass
class RoutingGate:
    """Composes the four interfaces into a working Routing Gate.

    All dependencies are optional — sensible defaults are wired up if absent.
    """

    storage: StorageBackend
    operator: OperatorProfile
    policy: ThresholdPolicy
    escalation: EscalationChannel

    def __init__(
        self,
        *,
        storage: Optional[StorageBackend] = None,
        operator: Optional[OperatorProfile] = None,
        policy: Optional[ThresholdPolicy] = None,
        escalation: Optional[EscalationChannel] = None,
    ):
        self.storage = storage if storage is not None else JsonlFileBackend(
            STATE_DIR / "routing-log.jsonl"
        )
        self.operator = operator if operator is not None else DefaultOperatorProfile()
        self.policy = (
            policy if policy is not None
            else CalibratedThresholdPolicy(StaticThresholdPolicy(), self.operator)
        )
        self.escalation = (
            escalation if escalation is not None else NullEscalationChannel()
        )

    # ── Classification ────────────────────────────────────────────

    def classify_tool_call(self, tool_name: str, tool_args: Any):
        return _classify_tool_call(tool_name, tool_args, self.policy.thresholds())

    def classify_tool_creation(
        self, *, event: str, tool_name: str, sandboxed: bool,
    ):
        return _classify_tool_creation(
            event=event, tool_name=tool_name, sandboxed=sandboxed,
            thresholds=self.policy.thresholds(),
        )

    # ── Logging + escalation ─────────────────────────────────────

    def log_and_maybe_escalate(self, entry: dict) -> None:
        """Persist `entry` and surface it if route == surface_to_human."""
        self.storage.append(entry)
        if entry.get("route") == "surface_to_human":
            self.escalation.escalate(entry)


# ═══════════════════════════════════════════════════════════════════
#                Pure classification (uses Thresholds)
# ═══════════════════════════════════════════════════════════════════


def _classify_tool_call(tool_name, tool_args, thresholds: Thresholds):
    """Classify a tool call. Returns (route, novelty, stakes, reversibility)."""

    if tool_name in SAFE_TOOLS:
        return "ai_autonomous", 0.1, 0.1, 0.9

    args_str = json.dumps(tool_args) if tool_args else ""
    for blocked in BLOCKED_TOOLS:
        if blocked in tool_name or blocked in args_str:
            return "surface_to_human", 0.9, 0.9, 0.1

    if tool_name in SENSITIVE_TOOLS:
        novelty = 0.4
        stakes = 0.4
        reversibility = 0.6

        if tool_args:
            args_str_lower = args_str.lower()
            if any(w in args_str_lower for w in
                   ["production", "client", "external", "public"]):
                stakes += 0.3
            if any(w in args_str_lower for w in
                   ["delete", "remove", "drop", "force"]):
                reversibility -= 0.3
                stakes += 0.2
            if any(w in args_str_lower for w in
                   ["email", "message", "post", "publish"]):
                reversibility -= 0.4

        if (
            novelty > thresholds.novelty
            and stakes > thresholds.stakes
            and reversibility < thresholds.reversibility
        ):
            return "surface_to_human", novelty, stakes, reversibility
        if stakes > thresholds.stakes:
            return "ai_with_review", novelty, stakes, reversibility

    return "ai_autonomous", 0.2, 0.2, 0.8


def _classify_tool_creation(
    *, event: str, tool_name: str, sandboxed: bool, thresholds: Thresholds,
):
    """Classify a tool-forge lifecycle event.

    `thresholds` is currently informational for the tool_creation taxonomy —
    routes are determined by event type because the lifecycle is fixed.
    Operators can later use thresholds to nudge promote-tier sensitivity if
    the auto-pruning of low-quality scaffolds becomes desired.
    """
    if event not in TOOL_CREATION_EVENTS:
        raise ValueError(
            f"Unknown tool_creation event: {event!r}. "
            f"Expected one of {sorted(TOOL_CREATION_EVENTS)}."
        )

    if event == "scaffold":
        return "ai_autonomous", 0.3, 0.2, 0.95
    if event == "sandbox_exec":
        return "ai_autonomous", 0.4, 0.3, 0.9
    if event == "promote_blocked":
        return "ai_autonomous", 0.4, 0.2, 0.95
    if event == "approve":
        return "ai_autonomous", 0.2, 0.5, 0.6
    if event == "reject":
        return "ai_autonomous", 0.2, 0.2, 0.95

    # event == "promote": ALWAYS surfaces (high stakes, partial reversibility).
    return "surface_to_human", 0.75, 0.65, 0.4


# ═══════════════════════════════════════════════════════════════════
#       Module-level functions (backward-compat — Hermes/dev_loop)
# ═══════════════════════════════════════════════════════════════════


# Default thresholds (kept as module constants for legacy callers).
NOVELTY_THRESHOLD = 0.7
STAKES_THRESHOLD = 0.5
REVERSIBILITY_THRESHOLD = 0.3


_default_gate: Optional[RoutingGate] = None


def _gate() -> RoutingGate:
    global _default_gate
    if _default_gate is None:
        _default_gate = RoutingGate()
    return _default_gate


def reset_default_gate() -> None:
    """Reset the module-level singleton (test hygiene)."""
    global _default_gate
    _default_gate = None


def classify_tool_call(tool_name, tool_args):
    """Classify a tool call through the default Routing Gate."""
    return _gate().classify_tool_call(tool_name, tool_args)


def classify_tool_creation(*, event, tool_name, sandboxed):
    """Classify a tool-forge lifecycle event through the default Routing Gate."""
    return _gate().classify_tool_creation(
        event=event, tool_name=tool_name, sandboxed=sandboxed,
    )


def log_classification(tool_name, route, novelty, stakes, reversibility):
    """Legacy logger used by Hermes extension. Routes via the default gate."""
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
    _gate().log_and_maybe_escalate(entry)


# ─── Hermes Extension Interface (unchanged behaviour) ──────────────


class RoutingGateExtension:
    """Hermes extension that applies the Routing Gate to every tool call."""

    def __init__(self, agent):
        self.agent = agent
        self.blocked_count = 0
        self.auto_count = 0

    def on_tool_call(self, tool_name, tool_args, context=None):
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
                ),
            }

        if route == "ai_with_review":
            pass  # Don't block, but flag for post-execution review.

        self.auto_count += 1
        return None

    def on_session_end(self, session):
        if self.blocked_count > 0 or self.auto_count > 0:
            pass


def create_extension(agent):
    """Factory function for Hermes extension loading."""
    return RoutingGateExtension(agent)


__all__ = [
    # Legacy / top-level API
    "BLOCKED_TOOLS",
    "NOVELTY_THRESHOLD",
    "REVERSIBILITY_THRESHOLD",
    "RoutingGateExtension",
    "SAFE_TOOLS",
    "SENSITIVE_TOOLS",
    "STAKES_THRESHOLD",
    "TOOL_CREATION_EVENTS",
    "classify_tool_call",
    "classify_tool_creation",
    "create_extension",
    "log_classification",
    "reset_default_gate",
    # §14.4 interfaces
    "CalibratedThresholdPolicy",
    "DefaultOperatorProfile",
    "EscalationChannel",
    "InMemoryBackend",
    "JsonlFileBackend",
    "NullEscalationChannel",
    "OperatorProfile",
    "RoutingGate",
    "StaticThresholdPolicy",
    "StderrEscalationChannel",
    "StorageBackend",
    "TelosOperatorProfile",
    "ThresholdPolicy",
    "Thresholds",
]
