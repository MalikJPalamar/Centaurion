"""
Trajectory Logger — per-action provenance for the factory line.

WO-025: Adds structured append-only JSONL logging so every action in a cell
session can answer "which skill/policy caused action N?" after the fact.

Storage: logs/trajectory/{wo}-{session_id}.jsonl  (Tier-3, runtime evidence)
"""

from __future__ import annotations

import fcntl
import json
import os
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator, Optional


# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------

@dataclass
class TrajectoryEntry:
    ts: str           # ISO 8601
    wo: str           # e.g. "WO-025"
    phase: str        # build | review | verify | plan | execute
    action: str       # tool_call | file_write | file_read | agent_spawn | decision | ...
    source: str       # skill / policy / prompt that caused the action
    tool: str         # tool name if applicable, else ""
    result: str       # success | fail | skip | brief description
    cost: float       # estimated token cost in USD

    def to_json(self) -> str:
        return json.dumps(asdict(self), separators=(",", ":"))

    @classmethod
    def from_json(cls, line: str) -> "TrajectoryEntry":
        return cls(**json.loads(line))


# ---------------------------------------------------------------------------
# Logger
# ---------------------------------------------------------------------------

_DEFAULT_LOG_DIR = Path(__file__).resolve().parents[2] / "logs" / "trajectory"


class TrajectoryLogger:
    """Append-only JSONL logger for factory-line provenance.

    One file per cell session: ``{wo}-{session_id}.jsonl``.
    Writes are atomic (``fcntl.flock`` advisory lock per append).
    """

    def __init__(
        self,
        wo: str,
        session_id: str | None = None,
        log_dir: Path | str | None = None,
    ) -> None:
        self.wo = wo
        self.session_id = session_id or uuid.uuid4().hex[:12]
        self.log_dir = Path(log_dir) if log_dir else _DEFAULT_LOG_DIR
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self._path = self.log_dir / f"{self.wo}-{self.session_id}.jsonl"

    @property
    def path(self) -> Path:
        return self._path

    # -- writing -----------------------------------------------------------

    def log(
        self,
        phase: str,
        action: str,
        source: str,
        tool: str = "",
        result: str = "success",
        cost: float = 0.0,
    ) -> TrajectoryEntry:
        """Append a single entry. Thread-safe via advisory file lock."""
        entry = TrajectoryEntry(
            ts=datetime.now(timezone.utc).isoformat(),
            wo=self.wo,
            phase=phase,
            action=action,
            source=source,
            tool=tool,
            result=result,
            cost=cost,
        )
        line = entry.to_json() + "\n"
        with open(self._path, "a") as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            try:
                f.write(line)
                f.flush()
            finally:
                fcntl.flock(f, fcntl.LOCK_UN)
        return entry


# ---------------------------------------------------------------------------
# Reader (for /doctor console route)
# ---------------------------------------------------------------------------

class TrajectoryReader:
    """Read and query trajectory JSONL files."""

    def __init__(self, log_dir: Path | str | None = None) -> None:
        self.log_dir = Path(log_dir) if log_dir else _DEFAULT_LOG_DIR

    def list_files(self, wo: Optional[str] = None) -> list[Path]:
        """List trajectory files, optionally filtered by WO prefix."""
        if not self.log_dir.exists():
            return []
        files = sorted(self.log_dir.glob("*.jsonl"))
        if wo:
            files = [f for f in files if f.name.startswith(wo)]
        return files

    def read_file(self, path: Path) -> list[TrajectoryEntry]:
        """Parse all entries from a single JSONL file."""
        entries: list[TrajectoryEntry] = []
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line:
                    entries.append(TrajectoryEntry.from_json(line))
        return entries

    def query(
        self,
        wo: Optional[str] = None,
        phase: Optional[str] = None,
        after: Optional[str] = None,
        before: Optional[str] = None,
    ) -> list[TrajectoryEntry]:
        """Query entries across all files with optional filters.

        Args:
            wo: Filter by work-order (e.g. "WO-025")
            phase: Filter by phase (e.g. "build")
            after: ISO 8601 lower bound (inclusive)
            before: ISO 8601 upper bound (exclusive)
        """
        results: list[TrajectoryEntry] = []
        for path in self.list_files(wo=wo):
            for entry in self.read_file(path):
                if phase and entry.phase != phase:
                    continue
                if after and entry.ts < after:
                    continue
                if before and entry.ts >= before:
                    continue
                results.append(entry)
        return results

    def provenance(self, wo: str, action_index: int) -> Optional[TrajectoryEntry]:
        """Answer: 'which skill/policy caused action N in WO-xxx?'

        Actions are numbered 0-based across all sessions for the given WO,
        ordered by timestamp.
        """
        entries = sorted(self.query(wo=wo), key=lambda e: e.ts)
        if 0 <= action_index < len(entries):
            return entries[action_index]
        return None


# ---------------------------------------------------------------------------
# Weekly Compaction (spec — not yet automated)
# ---------------------------------------------------------------------------
#
# COMPACTION PROTOCOL  (run weekly, e.g. via cron or harness hook)
#
# 1. Scan logs/trajectory/ for .jsonl files with all entries older than 7 days.
#
# 2. For each qualifying file:
#    a. Extract entries where result == "fail" or action == "decision"
#       (these are the RCA-relevant signals).
#    b. Group failures by (wo, phase, source) and count occurrences.
#    c. Emit a compact summary line per group into
#       logs/trajectory/compacted/{wo}-week-{iso_week}.jsonl
#       with schema: {wo, phase, source, fail_count, sample_result, first_ts, last_ts}
#
# 3. Move the original raw file to logs/trajectory/archive/
#    (retain for 90 days, then delete).
#
# 4. The compacted summaries feed Harness Doctrine property #3 (SELF-HEALING):
#    recurring failures by source/phase surface as candidates for automatic
#    policy or skill patches.
#
# Implementation deferred to WO-026 or a future maintenance WO.
# ---------------------------------------------------------------------------
