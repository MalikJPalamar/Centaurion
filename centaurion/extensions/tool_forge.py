"""
Tool Forge — dynamic tool/skill creation behind the Routing Gate.

Three-tier flow (Centaurion omega paradigm):

  1. SCAFFOLD     — Cortex writes tool stub + tests inside an isolated git
                    worktree branch (`auto/<job_id>`). Routing Gate: autonomous.
  2. SANDBOX EXEC — run the test harness inside Sandbox (Docker by default).
                    Routing Gate: autonomous.
  3. PROMOTION    — surface the diff to the operator. Routing Gate: surface.
                    On approve, files merge into `skills/auto-generated/_promoted/`.
                    On reject, files archive to `skills/auto-generated/_failed/`.

Every step is logged to `memory/state/tool-creation-log.jsonl` with a routing
classification, so the dev_loop watchdog can audit the forge end to end.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any

from .routing_gate import classify_tool_creation
from .sandbox import Sandbox, SandboxResult, Worktree


# ─── Errors ──────────────────────────────────────────────────────────


class ForgeError(Exception):
    """Raised on invalid input or out-of-order forge operations."""


# ─── Result types ───────────────────────────────────────────────────


_SAFE_TOOL_NAME = re.compile(r"^[a-z][a-z0-9_]{0,47}$")


@dataclass
class ScaffoldResult:
    job_id: str
    tool_name: str
    worktree: Worktree
    skill_md_path: Path
    implementation_path: Path
    test_path: Path


@dataclass(frozen=True)
class ExecutionResult:
    passed: bool
    exit_code: int
    stdout: str
    stderr: str
    duration_s: float
    timed_out: bool

    @classmethod
    def from_sandbox(cls, r: SandboxResult) -> "ExecutionResult":
        return cls(
            passed=(r.exit_code == 0 and not r.timed_out),
            exit_code=r.exit_code,
            stdout=r.stdout,
            stderr=r.stderr,
            duration_s=r.duration_s,
            timed_out=r.timed_out,
        )


class PromotionDecision(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


@dataclass
class PromotionProposal:
    job_id: str
    tool_name: str
    diff: str
    route: str
    decision: PromotionDecision = PromotionDecision.PENDING
    scaffold: ScaffoldResult | None = field(default=None, repr=False)


# ─── ToolForge ───────────────────────────────────────────────────────


_DEFAULT_LOG_REL = Path("memory/state/tool-creation-log.jsonl")
_STAGING_REL = Path("skills/auto-generated/_staging")
_PROMOTED_REL = Path("skills/auto-generated/_promoted")
_FAILED_REL = Path("skills/auto-generated/_failed")


class ToolForge:
    """Orchestrate scaffold → sandbox → promotion through the Routing Gate."""

    def __init__(
        self,
        repo: Path,
        sandbox: Sandbox,
        *,
        log_path: Path | None = None,
        sandbox_image_present: bool = True,
    ) -> None:
        self.repo = Path(repo).resolve()
        self.sandbox = sandbox
        self.log_path = (log_path or (self.repo / _DEFAULT_LOG_REL)).resolve()
        # `sandbox_image_present` lets callers signal that the sandbox is real
        # (Docker daemon up); it influences the audit log only.
        self._sandbox_image_present = sandbox_image_present

    # ── Tier 1: SCAFFOLD ─────────────────────────────────────────────

    def scaffold(
        self,
        tool_name: str,
        description: str,
        implementation: str,
        test_code: str,
    ) -> ScaffoldResult:
        if not _SAFE_TOOL_NAME.match(tool_name or ""):
            raise ForgeError(
                f"Unsafe tool_name: {tool_name!r}. "
                f"Must match {_SAFE_TOOL_NAME.pattern}"
            )
        if not description.strip():
            raise ForgeError("description must be non-empty")
        if "def " not in implementation and "class " not in implementation:
            raise ForgeError("implementation must define a function or class")
        if "assert" not in test_code and "raise" not in test_code:
            raise ForgeError("test_code must include at least one assertion")

        job_id = uuid.uuid4().hex[:12]
        wt = Worktree.create(self.repo, job_id=job_id)

        try:
            tool_dir = wt.path / _STAGING_REL / tool_name
            tool_dir.mkdir(parents=True, exist_ok=True)
            skill_md = tool_dir / "SKILL.md"
            impl_py = tool_dir / "impl.py"
            test_py = tool_dir / "test.py"

            skill_md.write_text(self._render_skill_md(
                tool_name=tool_name,
                description=description,
                job_id=job_id,
            ))
            impl_py.write_text(implementation)
            test_py.write_text(test_code)

            self._git(wt.path, ["add", "-A"])
            self._git(wt.path, ["commit", "-q", "-m",
                                f"forge: scaffold {tool_name} ({job_id})"])

            result = ScaffoldResult(
                job_id=job_id,
                tool_name=tool_name,
                worktree=wt,
                skill_md_path=skill_md,
                implementation_path=impl_py,
                test_path=test_py,
            )
        except Exception:
            wt.remove()
            raise

        self._log_event(
            event="scaffold",
            job_id=job_id,
            tool_name=tool_name,
            details={"branch": wt.branch, "files": ["SKILL.md", "impl.py", "test.py"]},
        )
        return result

    # ── Tier 2: SANDBOX EXEC ─────────────────────────────────────────

    def execute(self, scaffold: ScaffoldResult, *, timeout_s: int = 30) -> ExecutionResult:
        tool_dir = scaffold.skill_md_path.parent
        sandbox_result = self.sandbox.run(
            ["python", "test.py"],
            workdir=tool_dir,
            timeout_s=timeout_s,
            mem_mb=256,
            network=False,
        )
        execution = ExecutionResult.from_sandbox(sandbox_result)
        self._log_event(
            event="sandbox_exec",
            job_id=scaffold.job_id,
            tool_name=scaffold.tool_name,
            details={
                "exit_code": execution.exit_code,
                "passed": execution.passed,
                "duration_s": round(execution.duration_s, 3),
                "timed_out": execution.timed_out,
                "sandboxed": True,
            },
        )
        return execution

    # ── Tier 3: PROMOTION (surface to operator) ─────────────────────

    def propose_promotion(
        self,
        scaffold: ScaffoldResult,
        execution: ExecutionResult,
    ) -> PromotionProposal:
        if not execution.passed:
            self._log_event(
                event="promote_blocked",
                job_id=scaffold.job_id,
                tool_name=scaffold.tool_name,
                details={"reason": "execution_failed", "exit_code": execution.exit_code},
            )
            raise ForgeError(
                f"Cannot promote {scaffold.tool_name}: sandbox execution failed "
                f"(exit {execution.exit_code})."
            )

        diff = scaffold.worktree.diff(against="main")
        proposal = PromotionProposal(
            job_id=scaffold.job_id,
            tool_name=scaffold.tool_name,
            diff=diff,
            route="surface_to_human",
            decision=PromotionDecision.PENDING,
            scaffold=scaffold,
        )
        self._log_event(
            event="promote",
            job_id=scaffold.job_id,
            tool_name=scaffold.tool_name,
            details={"diff_lines": len(diff.splitlines())},
        )
        return proposal

    def approve(self, proposal: PromotionProposal) -> None:
        if proposal.decision is not PromotionDecision.PENDING:
            raise ForgeError(
                f"Proposal already {proposal.decision.value}; cannot approve."
            )
        scaffold = proposal.scaffold
        if scaffold is None:
            raise ForgeError("Proposal is missing its scaffold reference.")

        target = self.repo / _PROMOTED_REL / proposal.tool_name
        if target.exists():
            shutil.rmtree(target)
        target.mkdir(parents=True, exist_ok=True)

        # Copy the three canonical artifacts from the worktree into main.
        for artifact in ("SKILL.md", "impl.py", "test.py"):
            src = scaffold.skill_md_path.parent / artifact
            shutil.copy2(src, target / artifact)

        proposal.decision = PromotionDecision.APPROVED
        self._log_event(
            event="approve",
            job_id=proposal.job_id,
            tool_name=proposal.tool_name,
            details={"target": str(target.relative_to(self.repo))},
        )
        self.cleanup(scaffold)

    def reject(self, proposal: PromotionProposal, *, reason: str) -> None:
        if proposal.decision is not PromotionDecision.PENDING:
            raise ForgeError(
                f"Proposal already {proposal.decision.value}; cannot reject."
            )
        scaffold = proposal.scaffold
        if scaffold is None:
            raise ForgeError("Proposal is missing its scaffold reference.")

        archive = self.repo / _FAILED_REL / f"{proposal.job_id}-{proposal.tool_name}"
        archive.mkdir(parents=True, exist_ok=True)
        for artifact in ("SKILL.md", "impl.py", "test.py"):
            src = scaffold.skill_md_path.parent / artifact
            if src.exists():
                shutil.copy2(src, archive / artifact)
        (archive / "REASON.txt").write_text(reason + "\n")

        proposal.decision = PromotionDecision.REJECTED
        self._log_event(
            event="reject",
            job_id=proposal.job_id,
            tool_name=proposal.tool_name,
            details={"reason": reason, "archive": str(archive.relative_to(self.repo))},
        )
        self.cleanup(scaffold)

    # ── Cleanup ──────────────────────────────────────────────────────

    def cleanup(self, scaffold: ScaffoldResult) -> None:
        scaffold.worktree.remove()

    # ── Internals ────────────────────────────────────────────────────

    def _render_skill_md(self, *, tool_name: str, description: str, job_id: str) -> str:
        return (
            "---\n"
            f"name: {tool_name}\n"
            f"description: {description}\n"
            "origin: tool_forge\n"
            f"job_id: {job_id}\n"
            "stage: staging\n"
            "---\n"
            "\n"
            f"# {tool_name}\n\n"
            f"{description}\n\n"
            "## Lifecycle\n\n"
            "1. **Scaffold** — generated by Cortex inside an isolated worktree.\n"
            "2. **Sandbox exec** — `test.py` runs inside an isolated container.\n"
            "3. **Promotion** — surfaced to operator via Routing Gate; merged on approval.\n"
        )

    def _log_event(
        self,
        *,
        event: str,
        job_id: str,
        tool_name: str,
        details: dict[str, Any],
    ) -> None:
        route, n, s, r = classify_tool_creation(
            event=event,
            tool_name=tool_name,
            sandboxed=True,
        )
        entry = {
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "job_id": job_id,
            "event": event,
            "tool_name": tool_name,
            "route": route,
            "novelty": round(n, 2),
            "stakes": round(s, 2),
            "reversibility": round(r, 2),
            "details": details,
        }
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        with self.log_path.open("a") as f:
            f.write(json.dumps(entry) + "\n")

    def _git(self, cwd: Path, args: list[str]) -> None:
        result = subprocess.run(
            ["git", *args], cwd=str(cwd), capture_output=True, text=True,
        )
        if result.returncode != 0:
            raise ForgeError(
                f"git {' '.join(args)} failed: {result.stderr.strip() or result.stdout.strip()}"
            )


__all__ = [
    "ExecutionResult",
    "ForgeError",
    "PromotionDecision",
    "PromotionProposal",
    "ScaffoldResult",
    "ToolForge",
]
