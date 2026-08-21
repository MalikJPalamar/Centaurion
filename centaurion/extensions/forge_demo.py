"""
End-to-end Tool Forge demo.

Run from the repo root:

    python3 -m centaurion.extensions.forge_demo

This is a self-contained demonstration:
  1. Initializes a throwaway git repo in a temp dir.
  2. Uses MockSandbox so it works without a Docker daemon.
  3. Walks the full lifecycle: scaffold → sandbox_exec → propose → approve.
  4. Prints the routing-log.jsonl entries that would be emitted.

For a *production* run, swap MockSandbox for DockerSandbox (Docker daemon
required) and pass the real Centaurion repo path.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from centaurion.extensions.sandbox import MockSandbox  # noqa: E402
from centaurion.extensions.tool_forge import ToolForge  # noqa: E402


_IMPL = """\
def precision_ratio(predictive_order: float, thermodynamic_cost: float) -> float:
    \"\"\"Centaurion's fitness metric: order produced per unit cost.\"\"\"
    if thermodynamic_cost <= 0:
        raise ValueError("thermodynamic_cost must be positive")
    return predictive_order / thermodynamic_cost
"""

_TEST = """\
from impl import precision_ratio

assert precision_ratio(1.0, 1.0) == 1.0
assert precision_ratio(2.0, 1.0) == 2.0
assert precision_ratio(1.0, 2.0) == 0.5

try:
    precision_ratio(1.0, 0.0)
except ValueError:
    pass
else:
    raise AssertionError("zero cost must raise")

print("ok")
"""


def _bootstrap_repo(path: Path) -> None:
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=path, check=True)
    for k, v in (("user.email", "demo@centaurion.local"),
                 ("user.name", "Centaurion Demo"),
                 ("commit.gpgsign", "false"),
                 ("tag.gpgsign", "false")):
        subprocess.run(["git", "config", k, v], cwd=path, check=True)
    (path / "README.md").write_text("demo repo\n")
    subprocess.run(["git", "add", "-A"], cwd=path, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "init"], cwd=path, check=True)


def main() -> int:
    print("Centaurion Tool Forge — end-to-end demo")
    print("=" * 60)

    tmp = Path(tempfile.mkdtemp(prefix="forge-demo-"))
    try:
        _bootstrap_repo(tmp)
        sb = MockSandbox(exit_code=0, stdout="ok\n")
        forge = ToolForge(repo=tmp, sandbox=sb)

        print("\n[1/4] SCAFFOLD ─ writes tool stub into isolated worktree")
        scaffold = forge.scaffold(
            tool_name="precision_ratio",
            description="Compute Predictive Order / Thermodynamic Cost",
            implementation=_IMPL,
            test_code=_TEST,
        )
        print(f"      job_id        = {scaffold.job_id}")
        print(f"      branch        = {scaffold.worktree.branch}")
        print(f"      worktree path = {scaffold.worktree.path}")

        print("\n[2/4] SANDBOX EXEC ─ run test inside Sandbox (Mock here, Docker in prod)")
        execution = forge.execute(scaffold)
        print(f"      passed     = {execution.passed}")
        print(f"      exit_code  = {execution.exit_code}")
        print(f"      duration_s = {execution.duration_s:.3f}")

        print("\n[3/4] PROPOSE PROMOTION ─ Routing Gate surfaces diff to operator")
        proposal = forge.propose_promotion(scaffold, execution)
        print(f"      route    = {proposal.route}")
        print(f"      decision = {proposal.decision.value}")
        print(f"      diff     = {len(proposal.diff.splitlines())} lines")

        print("\n[4/4] APPROVE ─ operator merges into canonical _promoted/")
        forge.approve(proposal)
        promoted = tmp / "skills" / "auto-generated" / "_promoted" / "precision_ratio"
        print("      files in _promoted/:")
        for f in sorted(promoted.iterdir()):
            print(f"        {f.name}  ({f.stat().st_size} bytes)")

        print("\nRouting log (memory/state/tool-creation-log.jsonl):")
        log = tmp / "memory" / "state" / "tool-creation-log.jsonl"
        for raw in log.read_text().splitlines():
            entry = json.loads(raw)
            print(f"  {entry['event']:<18} route={entry['route']:<18} "
                  f"n={entry['novelty']} s={entry['stakes']} r={entry['reversibility']}")

        print("\n✓ Demo complete. Worktree cleaned up; main is unchanged until approve.")
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
