"""Tests for centaurion/extensions/sandbox.py — Sandbox + Worktree primitives."""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from centaurion.extensions.sandbox import (
    DockerSandbox,
    MockSandbox,
    Sandbox,
    SandboxResult,
    Worktree,
    WorktreeError,
)


# ─── Worktree primitive ──────────────────────────────────────────────


class TestWorktree:
    def test_create_makes_isolated_branch_and_path(self, tmp_repo: Path):
        wt = Worktree.create(tmp_repo, job_id="abc123")
        try:
            assert wt.path.exists()
            assert wt.path != tmp_repo
            assert wt.branch == "auto/abc123"
            assert (wt.path / "README.md").exists()  # base files materialized
            assert (wt.path / ".git").exists()       # git worktree marker
        finally:
            wt.remove()

    def test_remove_cleans_up_path_and_branch(self, tmp_repo: Path):
        wt = Worktree.create(tmp_repo, job_id="cleanup-test")
        path = wt.path
        branch = wt.branch
        wt.remove()
        assert not path.exists()
        # branch should also be deleted
        result = subprocess.run(
            ["git", "branch", "--list", branch],
            cwd=tmp_repo, capture_output=True, text=True,
        )
        assert branch not in result.stdout

    def test_diff_shows_changes_against_base(self, tmp_repo: Path):
        wt = Worktree.create(tmp_repo, job_id="diff-test")
        try:
            (wt.path / "new_file.txt").write_text("hello\n")
            subprocess.run(["git", "add", "-A"], cwd=wt.path, check=True)
            subprocess.run(
                ["git", "commit", "-q", "-m", "add file"],
                cwd=wt.path, check=True,
            )
            diff = wt.diff()
            assert "new_file.txt" in diff
            assert "+hello" in diff
        finally:
            wt.remove()

    def test_create_rejects_unsafe_job_id(self, tmp_repo: Path):
        for bad in ["../escape", "with/slash", "with space", "", "."]:
            with pytest.raises(WorktreeError):
                Worktree.create(tmp_repo, job_id=bad)

    def test_remove_is_idempotent(self, tmp_repo: Path):
        wt = Worktree.create(tmp_repo, job_id="idempotent")
        wt.remove()
        wt.remove()  # second call must not raise


# ─── Sandbox ABC ──────────────────────────────────────────────────────


class TestSandboxInterface:
    def test_sandbox_is_abstract(self):
        with pytest.raises(TypeError):
            Sandbox()  # type: ignore[abstract]

    def test_sandbox_result_is_immutable(self):
        r = SandboxResult(
            exit_code=0, stdout="", stderr="",
            timed_out=False, duration_s=0.1,
        )
        with pytest.raises((AttributeError, Exception)):
            r.exit_code = 1  # type: ignore[misc]


# ─── MockSandbox (test double, used by forge tests) ───────────────────


class TestMockSandbox:
    def test_returns_configured_result(self):
        sb = MockSandbox(exit_code=0, stdout="ok", stderr="")
        r = sb.run(["echo", "hi"], workdir=Path("/tmp"))
        assert r.exit_code == 0
        assert r.stdout == "ok"
        assert isinstance(r, SandboxResult)

    def test_records_invocations(self):
        sb = MockSandbox()
        sb.run(["a"], workdir=Path("/tmp"))
        sb.run(["b"], workdir=Path("/tmp"), timeout_s=10)
        assert len(sb.calls) == 2
        assert sb.calls[0]["command"] == ["a"]
        assert sb.calls[1]["timeout_s"] == 10

    def test_can_simulate_timeout(self):
        sb = MockSandbox(timed_out=True, exit_code=124)
        r = sb.run(["sleep", "999"], workdir=Path("/tmp"))
        assert r.timed_out is True
        assert r.exit_code == 124


# ─── DockerSandbox (live integration — skipped without daemon) ────────


@pytest.mark.docker
class TestDockerSandboxLive:
    def test_runs_in_isolated_container(self, tmp_path: Path):
        sb = DockerSandbox(image="python:3.11-slim")
        r = sb.run(["python", "-c", "print('hello from sandbox')"], workdir=tmp_path)
        assert r.exit_code == 0
        assert "hello from sandbox" in r.stdout

    def test_network_off_by_default(self, tmp_path: Path):
        sb = DockerSandbox(image="python:3.11-slim")
        r = sb.run(
            ["python", "-c",
             "import urllib.request, sys;\n"
             "try: urllib.request.urlopen('http://example.com', timeout=2); print('REACHED')\n"
             "except Exception as e: print('BLOCKED:', type(e).__name__); sys.exit(0)"],
            workdir=tmp_path,
        )
        assert "REACHED" not in r.stdout
        assert "BLOCKED" in r.stdout

    def test_timeout_kills_long_running(self, tmp_path: Path):
        sb = DockerSandbox(image="python:3.11-slim")
        r = sb.run(["python", "-c", "import time; time.sleep(60)"],
                   workdir=tmp_path, timeout_s=2)
        assert r.timed_out is True

    def test_workdir_is_writable_inside_sandbox(self, tmp_path: Path):
        (tmp_path / "input.txt").write_text("seed\n")
        sb = DockerSandbox(image="python:3.11-slim")
        r = sb.run(
            ["python", "-c",
             "import pathlib; "
             "pathlib.Path('/work/output.txt').write_text('written')"],
            workdir=tmp_path,
        )
        assert r.exit_code == 0
        assert (tmp_path / "output.txt").read_text() == "written"


# ─── DockerSandbox unit-level (no daemon required) ────────────────────


class TestDockerSandboxConfig:
    def test_constructs_run_command_with_safety_flags(self):
        sb = DockerSandbox(image="python:3.11-slim")
        cmd = sb._build_run_command(
            command=["echo", "hi"],
            workdir=Path("/tmp/x"),
            timeout_s=10,
            mem_mb=128,
            network=False,
        )
        # Network off
        assert "--network" in cmd
        idx = cmd.index("--network")
        assert cmd[idx + 1] == "none"
        # Memory cap
        assert "--memory" in cmd
        idx = cmd.index("--memory")
        assert cmd[idx + 1] == "128m"
        # Workdir mount as RW; sandbox mount path is /work
        joined = " ".join(cmd)
        assert "/tmp/x:/work" in joined
        assert "--rm" in cmd
        # No privileged escalation
        assert "--privileged" not in cmd
        # Drops capabilities
        assert "--cap-drop" in cmd
        # Read-only root filesystem outside the workdir
        assert "--read-only" in cmd

    def test_network_can_be_explicitly_enabled(self):
        sb = DockerSandbox(image="python:3.11-slim")
        cmd = sb._build_run_command(
            command=["echo", "hi"], workdir=Path("/tmp/x"),
            timeout_s=10, mem_mb=128, network=True,
        )
        idx = cmd.index("--network")
        assert cmd[idx + 1] != "none"
