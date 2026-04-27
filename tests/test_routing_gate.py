"""Tests for centaurion/extensions/routing_gate.py — including new tool_creation event type."""

from __future__ import annotations

import pytest

from centaurion.extensions.routing_gate import (
    classify_tool_call,
    classify_tool_creation,
)


# ─── Existing tool_call classification (regression coverage) ──────────


class TestExistingClassification:
    def test_safe_tool_is_autonomous(self):
        route, n, s, r = classify_tool_call("Read", {"path": "x"})
        assert route == "ai_autonomous"
        assert n < 0.3 and r > 0.7

    def test_blocked_tool_surfaces(self):
        route, n, s, r = classify_tool_call("Bash", {"command": "rm -rf /home/user"})
        assert route == "surface_to_human"

    def test_sensitive_tool_with_low_args_passes(self):
        route, _, _, _ = classify_tool_call("Edit", {"path": "x", "content": "ok"})
        assert route in {"ai_autonomous", "ai_with_review"}


# ─── New: tool_creation event classification ────────────────────────


class TestToolCreationClassification:
    def test_scaffold_is_autonomous(self):
        route, n, s, r = classify_tool_creation(
            event="scaffold", tool_name="hello_world", sandboxed=False,
        )
        assert route == "ai_autonomous"

    def test_sandbox_exec_is_autonomous(self):
        route, n, s, r = classify_tool_creation(
            event="sandbox_exec", tool_name="hello_world", sandboxed=True,
        )
        assert route == "ai_autonomous"

    def test_promote_surfaces_to_human(self):
        route, n, s, r = classify_tool_creation(
            event="promote", tool_name="hello_world", sandboxed=True,
        )
        assert route == "surface_to_human"
        assert s >= 0.5  # promotion is high-stakes
        assert r <= 0.5  # less reversible (executable code in repo)

    def test_unsandboxed_promote_still_surfaces(self):
        route, _, _, _ = classify_tool_creation(
            event="promote", tool_name="x", sandboxed=False,
        )
        assert route == "surface_to_human"

    def test_unknown_event_raises(self):
        with pytest.raises(ValueError):
            classify_tool_creation(event="nope", tool_name="x", sandboxed=True)

    def test_approval_is_autonomous_when_proposal_was_already_surfaced(self):
        # Operator-driven approval is logged but does not re-surface;
        # the surface already happened at `promote`.
        route, _, _, _ = classify_tool_creation(
            event="approve", tool_name="x", sandboxed=True,
        )
        assert route == "ai_autonomous"

    def test_reject_is_autonomous(self):
        route, _, _, _ = classify_tool_creation(
            event="reject", tool_name="x", sandboxed=True,
        )
        assert route == "ai_autonomous"
