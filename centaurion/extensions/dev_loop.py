"""
Dev Loop — Hermes Extension

Registers the Centaurion TDD development loop as a Hermes cron task.
Replaces the bash cron on VPS1 with Hermes-native scheduling.

The loop: pull → test → identify priority → develop → push → report

Install: copy to ~/.hermes/extensions/dev_loop.py
Schedule: hermes cron add "centaurion-dev" "0 4,12,20 * * *" "Run Centaurion dev loop"
"""

import json
import os
import subprocess
from pathlib import Path
from datetime import datetime


CENTAURION_REPO = os.environ.get("CENTAURION_REPO", os.path.expanduser("~/Centaurion"))


def run_dev_loop():
    """
    Execute the Centaurion TDD development loop.
    Returns a summary dict with results.
    """
    repo = Path(CENTAURION_REPO)
    if not repo.exists():
        return {"error": f"Repo not found at {CENTAURION_REPO}"}

    results = {
        "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "steps": {},
    }

    # Step 1: Pull latest
    pull = _run(["git", "pull", "origin", "main"], cwd=str(repo))
    results["steps"]["pull"] = "ok" if pull.returncode == 0 else "failed"

    if pull.returncode != 0:
        results["error"] = "git pull failed"
        return results

    # Step 2: Identify priority
    priority = _run(
        ["bash", "tests/identify-next-priority.sh"],
        cwd=str(repo),
    )
    try:
        priority_json = json.loads(priority.stdout)
    except (json.JSONDecodeError, TypeError):
        priority_json = {"status": "error", "phase": 0}

    results["priority"] = priority_json
    status = priority_json.get("status", "unknown")
    results["steps"]["identify"] = status

    if status == "all_passing":
        results["summary"] = "All tests passing. Nothing to develop."
        _write_status(results)
        return results

    # Step 3: The dev loop script handles Claude execution
    # Call the existing bash script for now (Hermes cron triggers it)
    dev_script = repo / "deploy" / "vps1" / "centaurion-dev-loop.sh"
    if dev_script.exists():
        dev = _run(
            ["bash", str(dev_script)],
            cwd=str(repo),
            env={**os.environ, "CENTAURION_REPO": str(repo)},
            timeout=600,
        )
        results["steps"]["develop"] = "ok" if dev.returncode == 0 else f"exit:{dev.returncode}"
    else:
        results["steps"]["develop"] = "script_not_found"

    # Step 4: Post-verification
    post = _run(
        ["bash", "tests/identify-next-priority.sh"],
        cwd=str(repo),
    )
    try:
        post_json = json.loads(post.stdout)
        results["post_priority"] = post_json
        pre_fail = priority_json.get("overall", {}).get("fail", 0)
        post_fail = post_json.get("overall", {}).get("fail", 0)
        results["tests_fixed"] = max(0, pre_fail - post_fail)
    except (json.JSONDecodeError, TypeError):
        results["tests_fixed"] = 0

    results["summary"] = (
        f"Phase {priority_json.get('phase', '?')}: "
        f"fixed {results['tests_fixed']} tests, "
        f"{post_json.get('overall', {}).get('fail', '?')} remaining"
    )

    _write_status(results)
    return results


def _run(cmd, cwd=None, env=None, timeout=120):
    """Run a subprocess and return the result."""
    try:
        return subprocess.run(
            cmd,
            cwd=cwd,
            env=env,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        class TimeoutResult:
            returncode = 1
            stdout = ""
            stderr = "timeout"
        return TimeoutResult()


def _write_status(results):
    """Write dev loop status to state file."""
    state_dir = Path(CENTAURION_REPO) / "memory" / "state"
    state_dir.mkdir(parents=True, exist_ok=True)
    status_file = state_dir / "dev-loop-status.json"

    status = {
        "timestamp": results.get("timestamp", ""),
        "date": datetime.utcnow().strftime("%Y-%m-%d"),
        "status": results.get("priority", {}).get("status", "unknown"),
        "phase": results.get("priority", {}).get("phase", 0),
        "tests_fixed": results.get("tests_fixed", 0),
        "summary": results.get("summary", ""),
    }

    with open(status_file, "w") as f:
        json.dump(status, f, indent=2)


# ── Hermes Cron Integration ──────────────────────────────

CRON_SCHEDULE = "0 4,12,20 * * *"  # 6am, 2pm, 10pm CET
CRON_NAME = "centaurion-dev-loop"
CRON_DESCRIPTION = "Centaurion TDD dev loop: pull → test → develop → push"


def register_cron(cron_manager):
    """Register the dev loop as a Hermes cron task."""
    cron_manager.add(
        name=CRON_NAME,
        schedule=CRON_SCHEDULE,
        description=CRON_DESCRIPTION,
        function=run_dev_loop,
    )


# ── Hermes Extension Interface ────────────────────────────

class DevLoopExtension:
    """
    Hermes extension that provides the Centaurion dev loop
    as a callable function and cron-schedulable task.
    """

    def __init__(self, agent):
        self.agent = agent

    def on_session_start(self, session):
        """Register dev loop as a tool the agent can invoke."""
        if hasattr(self.agent, "register_tool"):
            self.agent.register_tool(
                name="run_dev_loop",
                function=run_dev_loop,
                description=(
                    "Run the Centaurion TDD development loop. "
                    "Pulls latest, identifies failing tests, "
                    "runs Claude to fix them, pushes results."
                ),
                parameters={},
            )


def create_extension(agent):
    """Factory function for Hermes extension loading."""
    return DevLoopExtension(agent)
