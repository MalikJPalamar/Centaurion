"""Tests for the pluggable Routing Gate interfaces (§14.4 refactor).

The Routing Gate decomposes into four ABCs:

  - StorageBackend       — where classification entries are persisted
  - OperatorProfile      — operator-specific calibration vector
  - ThresholdPolicy      — base + calibrated thresholds
  - EscalationChannel    — surfaces decisions when route == surface_to_human

Default implementations live in centaurion/extensions/routing_gate.py and the
module-level classify_tool_call / classify_tool_creation functions delegate to
a default RoutingGate that wires sensible defaults.

All four interfaces must be swappable without changing callers.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from centaurion.extensions.routing_gate import (
    CalibratedThresholdPolicy,
    DefaultOperatorProfile,
    EscalationChannel,
    InMemoryBackend,
    JsonlFileBackend,
    NullEscalationChannel,
    OperatorProfile,
    RoutingGate,
    StaticThresholdPolicy,
    StderrEscalationChannel,
    StorageBackend,
    TelosOperatorProfile,
    Thresholds,
    ThresholdPolicy,
)


# ─── Thresholds value object ────────────────────────────────────────


class TestThresholds:
    def test_default_values(self):
        t = Thresholds()
        assert t.novelty == 0.7
        assert t.stakes == 0.5
        assert t.reversibility == 0.3

    def test_is_frozen(self):
        t = Thresholds()
        with pytest.raises((AttributeError, Exception)):
            t.novelty = 0.5  # type: ignore[misc]

    def test_clamps_to_unit_interval(self):
        # Adding calibration should never push thresholds outside [0, 1]
        t = Thresholds(novelty=0.95, stakes=0.5, reversibility=0.3)
        clamped = t.adjusted({"novelty": 0.5})
        assert 0.0 <= clamped.novelty <= 1.0


# ─── StorageBackend ─────────────────────────────────────────────────


class TestStorageBackendInterface:
    def test_storage_backend_is_abstract(self):
        with pytest.raises(TypeError):
            StorageBackend()  # type: ignore[abstract]


class TestJsonlFileBackend:
    def test_append_creates_parent_dirs(self, tmp_path: Path):
        path = tmp_path / "a" / "b" / "log.jsonl"
        backend = JsonlFileBackend(path)
        backend.append({"x": 1})
        assert path.exists()

    def test_append_and_read_round_trip(self, tmp_path: Path):
        path = tmp_path / "log.jsonl"
        backend = JsonlFileBackend(path)
        backend.append({"a": 1})
        backend.append({"b": 2})
        assert backend.read_all() == [{"a": 1}, {"b": 2}]

    def test_read_missing_file_returns_empty(self, tmp_path: Path):
        backend = JsonlFileBackend(tmp_path / "nope.jsonl")
        assert backend.read_all() == []


class TestInMemoryBackend:
    def test_isolation_between_instances(self):
        a = InMemoryBackend()
        b = InMemoryBackend()
        a.append({"x": 1})
        assert b.read_all() == []
        assert a.read_all() == [{"x": 1}]


# ─── OperatorProfile ────────────────────────────────────────────────


class TestOperatorProfileInterface:
    def test_operator_profile_is_abstract(self):
        with pytest.raises(TypeError):
            OperatorProfile()  # type: ignore[abstract]


class TestDefaultOperatorProfile:
    def test_returns_empty_calibration(self):
        assert DefaultOperatorProfile().calibration() == {}


class TestTelosOperatorProfile:
    def test_missing_baseline_returns_empty(self, tmp_path: Path):
        assert TelosOperatorProfile(tmp_path).calibration() == {}

    def test_baseline_with_no_adjustments_returns_empty(self, tmp_path: Path):
        (tmp_path / "BASELINE-INTEGRAL.md").write_text(
            "# BASELINE\nNo routing-gate adjustments configured.\n"
        )
        assert TelosOperatorProfile(tmp_path).calibration() == {}

    def test_baseline_with_adjustments_returns_them(self, tmp_path: Path):
        (tmp_path / "BASELINE-INTEGRAL.md").write_text(
            "# BASELINE-INTEGRAL\n"
            "## Routing Gate Adjustments\n"
            "- novelty: -0.1\n"
            "- stakes: +0.05\n"
            "- reversibility: 0\n"
        )
        cal = TelosOperatorProfile(tmp_path).calibration()
        assert cal["novelty"] == pytest.approx(-0.1)
        assert cal["stakes"] == pytest.approx(0.05)
        assert cal["reversibility"] == pytest.approx(0.0)


# ─── ThresholdPolicy ────────────────────────────────────────────────


class TestThresholdPolicyInterface:
    def test_threshold_policy_is_abstract(self):
        with pytest.raises(TypeError):
            ThresholdPolicy()  # type: ignore[abstract]


class TestStaticThresholdPolicy:
    def test_returns_supplied_thresholds(self):
        t = Thresholds(novelty=0.8, stakes=0.4, reversibility=0.2)
        policy = StaticThresholdPolicy(t)
        assert policy.thresholds() == t

    def test_default_uses_canonical_values(self):
        t = StaticThresholdPolicy().thresholds()
        assert t.novelty == 0.7
        assert t.stakes == 0.5
        assert t.reversibility == 0.3


class TestCalibratedThresholdPolicy:
    def test_no_calibration_returns_base(self):
        base = StaticThresholdPolicy(Thresholds(0.7, 0.5, 0.3))
        cal = CalibratedThresholdPolicy(base, DefaultOperatorProfile())
        assert cal.thresholds() == Thresholds(0.7, 0.5, 0.3)

    def test_calibration_adjusts_thresholds(self):
        class CustomOp(OperatorProfile):
            def calibration(self):
                return {"novelty": -0.1, "stakes": 0.05}

        base = StaticThresholdPolicy(Thresholds(0.7, 0.5, 0.3))
        cal = CalibratedThresholdPolicy(base, CustomOp())
        t = cal.thresholds()
        assert t.novelty == pytest.approx(0.6)
        assert t.stakes == pytest.approx(0.55)
        assert t.reversibility == pytest.approx(0.3)


# ─── EscalationChannel ─────────────────────────────────────────────


class TestEscalationChannelInterface:
    def test_escalation_channel_is_abstract(self):
        with pytest.raises(TypeError):
            EscalationChannel()  # type: ignore[abstract]


class TestNullEscalationChannel:
    def test_records_escalations(self):
        ch = NullEscalationChannel()
        ch.escalate({"task": "x", "route": "surface_to_human"})
        ch.escalate({"task": "y", "route": "surface_to_human"})
        assert len(ch.escalations) == 2

    def test_starts_empty(self):
        assert NullEscalationChannel().escalations == []


class TestStderrEscalationChannel:
    def test_writes_to_stderr(self, capsys):
        ch = StderrEscalationChannel()
        ch.escalate({"task": "do thing", "route": "surface_to_human",
                     "novelty": 0.8, "stakes": 0.7, "reversibility": 0.2})
        captured = capsys.readouterr()
        assert "ROUTING GATE" in captured.err
        assert "do thing" in captured.err


# ─── Composed RoutingGate ───────────────────────────────────────────


class TestRoutingGateComposition:
    def test_default_construction_provides_all_components(self):
        rg = RoutingGate()
        assert isinstance(rg.storage, StorageBackend)
        assert isinstance(rg.operator, OperatorProfile)
        assert isinstance(rg.policy, ThresholdPolicy)
        assert isinstance(rg.escalation, EscalationChannel)

    def test_custom_components_are_used(self):
        storage = InMemoryBackend()
        operator = DefaultOperatorProfile()
        policy = StaticThresholdPolicy(Thresholds(0.5, 0.5, 0.5))
        escalation = NullEscalationChannel()
        rg = RoutingGate(storage=storage, operator=operator,
                         policy=policy, escalation=escalation)
        assert rg.storage is storage
        assert rg.policy.thresholds().novelty == 0.5

    def test_log_and_maybe_escalate_writes_to_storage(self):
        storage = InMemoryBackend()
        escalation = NullEscalationChannel()
        rg = RoutingGate(storage=storage, escalation=escalation)
        rg.log_and_maybe_escalate({"route": "ai_autonomous", "task": "x"})
        assert len(storage.read_all()) == 1
        assert escalation.escalations == []  # autonomous does not escalate

    def test_log_and_maybe_escalate_surfaces_when_routed_to_human(self):
        storage = InMemoryBackend()
        escalation = NullEscalationChannel()
        rg = RoutingGate(storage=storage, escalation=escalation)
        rg.log_and_maybe_escalate({"route": "surface_to_human", "task": "deploy"})
        assert len(storage.read_all()) == 1
        assert len(escalation.escalations) == 1

    def test_classify_tool_call_passes_through_to_classifier(self):
        rg = RoutingGate(storage=InMemoryBackend(),
                         escalation=NullEscalationChannel())
        route, n, s, r = rg.classify_tool_call("Read", {"path": "x"})
        assert route == "ai_autonomous"

    def test_classify_tool_creation_passes_through(self):
        rg = RoutingGate(storage=InMemoryBackend(),
                         escalation=NullEscalationChannel())
        route, n, s, r = rg.classify_tool_creation(
            event="promote", tool_name="x", sandboxed=True,
        )
        assert route == "surface_to_human"
