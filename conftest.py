"""Root conftest: ensures project root is on sys.path for pytest collection."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))


def pytest_configure(config):
    config.addinivalue_line("markers", "docker: requires a live Docker daemon (skipped if unavailable)")
    config.addinivalue_line("markers", "integration: end-to-end across forge + sandbox + routing gate")
