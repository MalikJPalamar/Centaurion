"""Tests for the trajectory logger and reader (WO-025)."""

import tempfile
from pathlib import Path

from backend.lib.trajectory import TrajectoryEntry, TrajectoryLogger, TrajectoryReader


def test_roundtrip():
    with tempfile.TemporaryDirectory() as tmp:
        logger = TrajectoryLogger("WO-025", session_id="test1", log_dir=tmp)
        logger.log(
            phase="build",
            action="tool_call",
            source="skills/PAI/SKILL.md",
            tool="Edit",
            result="success",
            cost=0.002,
        )
        logger.log(
            phase="verify",
            action="decision",
            source="harness-doctrine#2-AUDITABLE",
            tool="",
            result="skip",
            cost=0.0,
        )

        reader = TrajectoryReader(log_dir=tmp)
        files = reader.list_files()
        assert len(files) == 1
        assert files[0].name == "WO-025-test1.jsonl"

        entries = reader.read_file(files[0])
        assert len(entries) == 2
        assert entries[0].source == "skills/PAI/SKILL.md"
        assert entries[1].action == "decision"


def test_provenance_query():
    with tempfile.TemporaryDirectory() as tmp:
        logger = TrajectoryLogger("WO-025", session_id="s1", log_dir=tmp)
        for i in range(5):
            logger.log(
                phase="build",
                action=f"action_{i}",
                source=f"source_{i}",
                tool="",
                result="success",
            )

        reader = TrajectoryReader(log_dir=tmp)
        entry = reader.provenance("WO-025", 3)
        assert entry is not None
        assert entry.action == "action_3"
        assert entry.source == "source_3"

        # Out of range returns None
        assert reader.provenance("WO-025", 99) is None


def test_filter_by_phase():
    with tempfile.TemporaryDirectory() as tmp:
        logger = TrajectoryLogger("WO-025", session_id="s2", log_dir=tmp)
        logger.log(phase="build", action="a", source="s", result="success")
        logger.log(phase="verify", action="b", source="s", result="fail")

        reader = TrajectoryReader(log_dir=tmp)
        build_only = reader.query(phase="build")
        assert len(build_only) == 1
        assert build_only[0].action == "a"
