"""Pytest fixtures and Docker availability detection."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def _docker_alive() -> bool:
    if shutil.which("docker") is None:
        return False
    try:
        result = subprocess.run(
            ["docker", "info", "--format", "{{.ServerVersion}}"],
            capture_output=True,
            timeout=3,
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, OSError):
        return False


DOCKER_AVAILABLE = _docker_alive()


def pytest_collection_modifyitems(config, items):
    skip_docker = pytest.mark.skip(reason="Docker daemon not available")
    for item in items:
        if "docker" in item.keywords and not DOCKER_AVAILABLE:
            item.add_marker(skip_docker)


@pytest.fixture
def repo_root() -> Path:
    return REPO_ROOT


@pytest.fixture
def tmp_repo(tmp_path: Path) -> Path:
    """A throwaway git repo with one commit on `main`."""
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=tmp_path, check=True)
    for key, value in (
        ("user.email", "test@centaurion.local"),
        ("user.name", "Centaurion Test"),
        ("commit.gpgsign", "false"),
        ("tag.gpgsign", "false"),
        ("gpg.format", "openpgp"),
    ):
        subprocess.run(["git", "config", key, value], cwd=tmp_path, check=True)
    (tmp_path / "README.md").write_text("test repo\n")
    subprocess.run(["git", "add", "-A"], cwd=tmp_path, check=True)
    subprocess.run(
        ["git", "commit", "-q", "-m", "initial"],
        cwd=tmp_path, check=True,
        env={**os.environ, "GIT_COMMITTER_NAME": "Centaurion Test",
             "GIT_COMMITTER_EMAIL": "test@centaurion.local"},
    )
    return tmp_path
