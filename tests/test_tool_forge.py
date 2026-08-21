"""Tests for centaurion/extensions/tool_forge.py — dynamic tool creation."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from centaurion.extensions.sandbox import MockSandbox, SandboxResult
from centaurion.extensions.tool_forge import (
    ExecutionResult,
    ForgeError,
    PromotionDecision,
    PromotionProposal,
    ScaffoldResult,
    ToolForge,
)


# ─── Helpers ──────────────────────────────────────────────────────────


def _good_impl() -> str:
    return (
        "def greet(name):\n"
        "    return f'hello, {name}'\n"
    )


def _good_test() -> str:
    return (
        "from impl import greet\n"
        "assert greet('world') == 'hello, world'\n"
        "print('ok')\n"
    )


# ─── ScaffoldResult shape ─────────────────────────────────────────────


class TestScaffoldResult:
    def test_carries_paths_and_metadata(self, tmp_repo: Path):
        sb = MockSandbox()
        forge = ToolForge(repo=tmp_repo, sandbox=sb)
        s = forge.scaffold(
            tool_name="greet",
            description="Say hello",
            implementation=_good_impl(),
            test_code=_good_test(),
        )
        assert isinstance(s, ScaffoldResult)
        assert s.tool_name == "greet"
        assert s.job_id  # non-empty
        assert s.skill_md_path.exists()
        assert s.implementation_path.exists()
        assert s.test_path.exists()
        assert "name: greet" in s.skill_md_path.read_text()
        assert "Say hello" in s.skill_md_path.read_text()


# ─── Scaffold — Tier 1 (autonomous) ──────────────────────────────────


class TestScaffold:
    def test_writes_to_staging_worktree(self, tmp_repo: Path):
        sb = MockSandbox()
        forge = ToolForge(repo=tmp_repo, sandbox=sb)
        s = forge.scaffold("widget", "make a widget", _good_impl(), _good_test())
        try:
            # Files live inside an isolated git worktree, NOT main worktree
            assert tmp_repo not in s.skill_md_path.parents
            assert "auto-generated" in str(s.skill_md_path)
        finally:
            forge.cleanup(s)

    def test_logs_scaffold_event(self, tmp_repo: Path):
        sb = MockSandbox()
        log_path = tmp_repo / "creation.jsonl"
        forge = ToolForge(repo=tmp_repo, sandbox=sb, log_path=log_path)
        s = forge.scaffold("widget", "make", _good_impl(), _good_test())
        try:
            entries = [json.loads(l) for l in log_path.read_text().splitlines() if l]
            scaffold_entries = [e for e in entries if e["event"] == "scaffold"]
            assert len(scaffold_entries) == 1
            assert scaffold_entries[0]["tool_name"] == "widget"
            assert scaffold_entries[0]["job_id"] == s.job_id
            assert scaffold_entries[0]["route"] == "ai_autonomous"
        finally:
            forge.cleanup(s)

    def test_rejects_invalid_tool_names(self, tmp_repo: Path):
        forge = ToolForge(repo=tmp_repo, sandbox=MockSandbox())
        for bad in ["", "..", "name with space", "name/slash", "name;rm-rf"]:
            with pytest.raises(ForgeError):
                forge.scaffold(bad, "x", _good_impl(), _good_test())


# ─── Execute — Tier 2 (autonomous, sandboxed) ─────────────────────────


class TestExecute:
    def test_runs_test_in_sandbox(self, tmp_repo: Path):
        sb = MockSandbox(exit_code=0, stdout="ok\n")
        forge = ToolForge(repo=tmp_repo, sandbox=sb)
        s = forge.scaffold("widget", "make", _good_impl(), _good_test())
        try:
            r = forge.execute(s)
            assert isinstance(r, ExecutionResult)
            assert r.passed is True
            assert r.exit_code == 0
            # Sandbox was invoked with a python command in the worktree
            assert len(sb.calls) == 1
            call = sb.calls[0]
            assert call["workdir"] == s.skill_md_path.parent
            assert call["network"] is False  # default safety
            assert call["timeout_s"] >= 5
        finally:
            forge.cleanup(s)

    def test_failing_test_marks_execution_failed(self, tmp_repo: Path):
        sb = MockSandbox(exit_code=1, stderr="AssertionError")
        forge = ToolForge(repo=tmp_repo, sandbox=sb)
        s = forge.scaffold("widget", "make", _good_impl(), _good_test())
        try:
            r = forge.execute(s)
            assert r.passed is False
            assert "AssertionError" in r.stderr
        finally:
            forge.cleanup(s)

    def test_logs_sandbox_exec_event(self, tmp_repo: Path):
        sb = MockSandbox(exit_code=0)
        log_path = tmp_repo / "creation.jsonl"
        forge = ToolForge(repo=tmp_repo, sandbox=sb, log_path=log_path)
        s = forge.scaffold("widget", "make", _good_impl(), _good_test())
        try:
            forge.execute(s)
            entries = [json.loads(l) for l in log_path.read_text().splitlines() if l]
            events = [e["event"] for e in entries]
            assert "sandbox_exec" in events
        finally:
            forge.cleanup(s)


# ─── Propose promotion — Tier 3 (surface to operator) ────────────────


class TestProposePromotion:
    def test_passing_execution_yields_proposal(self, tmp_repo: Path):
        sb = MockSandbox(exit_code=0, stdout="ok\n")
        forge = ToolForge(repo=tmp_repo, sandbox=sb)
        s = forge.scaffold("widget", "make", _good_impl(), _good_test())
        try:
            ex = forge.execute(s)
            prop = forge.propose_promotion(s, ex)
            assert isinstance(prop, PromotionProposal)
            assert prop.tool_name == "widget"
            assert prop.diff  # non-empty git diff
            assert prop.route == "surface_to_human"
            assert prop.decision == PromotionDecision.PENDING
        finally:
            forge.cleanup(s)

    def test_failing_execution_blocks_proposal(self, tmp_repo: Path):
        sb = MockSandbox(exit_code=1, stderr="oops")
        forge = ToolForge(repo=tmp_repo, sandbox=sb)
        s = forge.scaffold("widget", "make", _good_impl(), _good_test())
        try:
            ex = forge.execute(s)
            with pytest.raises(ForgeError):
                forge.propose_promotion(s, ex)
        finally:
            forge.cleanup(s)

    def test_logs_promote_event_with_surface_route(self, tmp_repo: Path):
        sb = MockSandbox(exit_code=0)
        log_path = tmp_repo / "creation.jsonl"
        forge = ToolForge(repo=tmp_repo, sandbox=sb, log_path=log_path)
        s = forge.scaffold("widget", "make", _good_impl(), _good_test())
        try:
            ex = forge.execute(s)
            forge.propose_promotion(s, ex)
            entries = [json.loads(l) for l in log_path.read_text().splitlines() if l]
            promote_entries = [e for e in entries if e["event"] == "promote"]
            assert len(promote_entries) == 1
            assert promote_entries[0]["route"] == "surface_to_human"
        finally:
            forge.cleanup(s)


# ─── Promotion — accept/reject (operator decision) ───────────────────


class TestApproveAndReject:
    def test_approve_merges_into_canonical(self, tmp_repo: Path):
        sb = MockSandbox(exit_code=0)
        forge = ToolForge(repo=tmp_repo, sandbox=sb)
        s = forge.scaffold("widget", "make", _good_impl(), _good_test())
        ex = forge.execute(s)
        prop = forge.propose_promotion(s, ex)

        forge.approve(prop)

        canonical_dir = tmp_repo / "skills" / "auto-generated" / "_promoted" / "widget"
        assert (canonical_dir / "SKILL.md").exists()
        assert "name: widget" in (canonical_dir / "SKILL.md").read_text()

    def test_reject_archives_to_failed(self, tmp_repo: Path):
        sb = MockSandbox(exit_code=0)
        forge = ToolForge(repo=tmp_repo, sandbox=sb)
        s = forge.scaffold("widget", "make", _good_impl(), _good_test())
        ex = forge.execute(s)
        prop = forge.propose_promotion(s, ex)

        forge.reject(prop, reason="not aligned with TELOS")

        failed_dir = tmp_repo / "skills" / "auto-generated" / "_failed"
        archived = list(failed_dir.glob(f"*{s.job_id}*"))
        assert len(archived) >= 1


# ─── End-to-end happy path ───────────────────────────────────────────


@pytest.mark.integration
class TestEndToEnd:
    def test_full_lifecycle_scaffold_exec_propose_approve(self, tmp_repo: Path):
        sb = MockSandbox(exit_code=0, stdout="ok\n")
        log_path = tmp_repo / "creation.jsonl"
        forge = ToolForge(repo=tmp_repo, sandbox=sb, log_path=log_path)

        s = forge.scaffold(
            tool_name="hello_world",
            description="Returns a friendly greeting",
            implementation=_good_impl(),
            test_code=_good_test(),
        )
        ex = forge.execute(s)
        assert ex.passed
        prop = forge.propose_promotion(s, ex)
        assert prop.decision == PromotionDecision.PENDING
        forge.approve(prop)

        # Tool now lives under canonical _promoted
        promoted = tmp_repo / "skills" / "auto-generated" / "_promoted" / "hello_world"
        assert (promoted / "SKILL.md").exists()
        assert (promoted / "impl.py").exists()
        assert (promoted / "test.py").exists()

        # Log records all four events
        entries = [json.loads(l) for l in log_path.read_text().splitlines() if l]
        events = [e["event"] for e in entries]
        assert events == ["scaffold", "sandbox_exec", "promote", "approve"]
