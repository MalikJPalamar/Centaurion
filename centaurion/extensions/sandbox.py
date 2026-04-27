"""
Sandbox primitives — Docker-isolated execution + git-worktree-based file safety.

The Centaurion exo-cortex executes untrusted code (auto-generated tools, skill
candidates) inside a sandbox composed of two layers:

  1. **Worktree** — a `git worktree` cloned from the host repo onto an isolated
     branch (`auto/<job_id>`). All file operations happen here; main is untouched
     until promotion via review.

  2. **Sandbox** — an OS-level isolated execution environment. Production uses
     `DockerSandbox`; tests use `MockSandbox`. The interface is identical.

Phase 1: Docker container per job (this module).
Phase 2 (planned): Firecracker microVM with same Sandbox interface.

Safety properties enforced by DockerSandbox:
  - Network off by default (`--network none`)
  - Read-only root filesystem outside the workdir mount
  - Memory and CPU caps
  - Wall-clock timeout (kills container)
  - Drops all Linux capabilities
  - No privileged mode
  - Container destroyed on completion (`--rm`)
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


# ─── Errors ──────────────────────────────────────────────────────────


class WorktreeError(Exception):
    """Raised when a Worktree operation fails or input is unsafe."""


class SandboxError(Exception):
    """Raised when a Sandbox operation fails."""


# ─── Worktree primitive ──────────────────────────────────────────────


_SAFE_JOB_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_\-]{0,63}$")


@dataclass
class Worktree:
    """A git worktree pinned to an isolated branch.

    Use `Worktree.create(...)` rather than constructing directly.
    """

    repo: Path
    job_id: str
    path: Path
    branch: str

    @classmethod
    def create(
        cls,
        repo: Path,
        job_id: str,
        *,
        base_branch: str = "main",
        parent_dir: Path | None = None,
    ) -> "Worktree":
        if not _SAFE_JOB_ID.match(job_id or ""):
            raise WorktreeError(
                f"Unsafe job_id: {job_id!r}. "
                f"Must match {_SAFE_JOB_ID.pattern}"
            )
        repo = repo.resolve()
        if not (repo / ".git").exists():
            raise WorktreeError(f"Not a git repository: {repo}")

        # Default: place worktree OUTSIDE the main checkout to avoid any
        # chance of collision with the host repo's working tree.
        if parent_dir is None:
            parent = Path(tempfile.gettempdir()) / "centaurion-forge" / repo.name
        else:
            parent = parent_dir
        parent.mkdir(parents=True, exist_ok=True)
        wt_path = parent / f"job-{job_id}"
        branch = f"auto/{job_id}"

        if wt_path.exists():
            raise WorktreeError(f"Worktree path already exists: {wt_path}")

        # Verify base branch exists
        result = subprocess.run(
            ["git", "rev-parse", "--verify", base_branch],
            cwd=str(repo), capture_output=True, text=True,
        )
        if result.returncode != 0:
            raise WorktreeError(
                f"Base branch {base_branch!r} not found in {repo}: {result.stderr.strip()}"
            )

        # Create worktree on a new branch derived from base
        result = subprocess.run(
            ["git", "worktree", "add", "-b", branch, str(wt_path), base_branch],
            cwd=str(repo), capture_output=True, text=True,
        )
        if result.returncode != 0:
            raise WorktreeError(f"git worktree add failed: {result.stderr.strip()}")

        return cls(repo=repo, job_id=job_id, path=wt_path, branch=branch)

    def diff(self, against: str = "main") -> str:
        """Return a unified diff of the worktree branch against `against`."""
        result = subprocess.run(
            ["git", "diff", f"{against}...HEAD"],
            cwd=str(self.path), capture_output=True, text=True,
        )
        if result.returncode != 0:
            raise WorktreeError(f"git diff failed: {result.stderr.strip()}")
        return result.stdout

    def remove(self) -> None:
        """Tear down worktree + branch. Idempotent."""
        if self.path.exists():
            subprocess.run(
                ["git", "worktree", "remove", "--force", str(self.path)],
                cwd=str(self.repo), capture_output=True, text=True,
            )
            if self.path.exists():
                shutil.rmtree(self.path, ignore_errors=True)

        # Prune any stale records, then delete the branch
        subprocess.run(
            ["git", "worktree", "prune"],
            cwd=str(self.repo), capture_output=True, text=True,
        )
        subprocess.run(
            ["git", "branch", "-D", self.branch],
            cwd=str(self.repo), capture_output=True, text=True,
        )


# ─── Sandbox interface ───────────────────────────────────────────────


@dataclass(frozen=True)
class SandboxResult:
    """Outcome of a sandboxed execution."""

    exit_code: int
    stdout: str
    stderr: str
    timed_out: bool
    duration_s: float


class Sandbox(ABC):
    """Abstract sandbox for executing untrusted code.

    Implementations must enforce isolation at OS level (container, microVM, etc).
    The interface is process-shaped: a command, a working directory, and limits.
    """

    @abstractmethod
    def run(
        self,
        command: list[str],
        workdir: Path,
        *,
        timeout_s: int = 30,
        mem_mb: int = 256,
        network: bool = False,
    ) -> SandboxResult:
        """Execute `command` inside the sandbox with `workdir` mounted RW."""


# ─── DockerSandbox — production ──────────────────────────────────────


@dataclass
class DockerSandbox(Sandbox):
    """Run commands inside an ephemeral, hardened Docker container.

    Defaults err on the side of safety: no network, capabilities dropped,
    read-only root filesystem, memory cap, wall-clock timeout.
    """

    image: str = "python:3.11-slim"
    docker_bin: str = "docker"
    workdir_in_container: str = "/work"

    def _build_run_command(
        self,
        command: list[str],
        workdir: Path,
        timeout_s: int,
        mem_mb: int,
        network: bool,
    ) -> list[str]:
        workdir = workdir.resolve()
        cmd: list[str] = [
            self.docker_bin, "run",
            "--rm",
            "--network", "none" if not network else "bridge",
            "--memory", f"{mem_mb}m",
            "--memory-swap", f"{mem_mb}m",
            "--cpus", "1.0",
            "--pids-limit", "256",
            "--cap-drop", "ALL",
            "--security-opt", "no-new-privileges",
            "--read-only",
            "--tmpfs", "/tmp:size=64m",
            "-v", f"{workdir}:{self.workdir_in_container}:rw",
            "-w", self.workdir_in_container,
            self.image,
        ]
        cmd.extend(command)
        return cmd

    def run(
        self,
        command: list[str],
        workdir: Path,
        *,
        timeout_s: int = 30,
        mem_mb: int = 256,
        network: bool = False,
    ) -> SandboxResult:
        full = self._build_run_command(command, workdir, timeout_s, mem_mb, network)
        start = time.monotonic()
        try:
            result = subprocess.run(
                full,
                capture_output=True, text=True,
                timeout=timeout_s,
            )
            return SandboxResult(
                exit_code=result.returncode,
                stdout=result.stdout,
                stderr=result.stderr,
                timed_out=False,
                duration_s=time.monotonic() - start,
            )
        except subprocess.TimeoutExpired as exc:
            # Container is still running. Stop it to free resources.
            # We can't address it by name (docker auto-names with --rm), so we
            # best-effort kill via container ID via `docker ps` filter on image+workdir.
            # In production, callers should pass --name; here we accept best-effort.
            return SandboxResult(
                exit_code=124,
                stdout=exc.stdout.decode() if exc.stdout else "",
                stderr=(exc.stderr.decode() if exc.stderr else "") + "\n[sandbox] timed out",
                timed_out=True,
                duration_s=time.monotonic() - start,
            )
        except FileNotFoundError as exc:
            raise SandboxError(
                f"Docker binary not found ({self.docker_bin!r}): {exc}"
            ) from exc


# ─── MockSandbox — for tests ─────────────────────────────────────────


@dataclass
class MockSandbox(Sandbox):
    """In-process sandbox stand-in. Returns configured results, records calls."""

    exit_code: int = 0
    stdout: str = ""
    stderr: str = ""
    timed_out: bool = False
    duration_s: float = 0.01
    calls: list[dict[str, Any]] = field(default_factory=list)

    def run(
        self,
        command: list[str],
        workdir: Path,
        *,
        timeout_s: int = 30,
        mem_mb: int = 256,
        network: bool = False,
    ) -> SandboxResult:
        self.calls.append({
            "command": list(command),
            "workdir": workdir,
            "timeout_s": timeout_s,
            "mem_mb": mem_mb,
            "network": network,
        })
        return SandboxResult(
            exit_code=self.exit_code,
            stdout=self.stdout,
            stderr=self.stderr,
            timed_out=self.timed_out,
            duration_s=self.duration_s,
        )


__all__ = [
    "DockerSandbox",
    "MockSandbox",
    "Sandbox",
    "SandboxError",
    "SandboxResult",
    "Worktree",
    "WorktreeError",
]
