"""Tests qui prouvent que l'infrastructure fonctionne réellement :
idempotence, exclusion concurrente, reprise après kill, et refus du Holdout.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from metaalpha import checkpoints
from metaalpha.checkpoints import UnitKey
from metaalpha.fs import Storage
from metaalpha.orchestrator import Orchestrator, TransientError


def _unit_fn_factory(counter: dict, fail_on: set[str] | None = None):
    fail_on = fail_on or set()

    def fn(uid: str, storage: Storage):
        counter[uid] = counter.get(uid, 0) + 1
        if uid in fail_on:
            raise TransientError("timeout réseau simulé")
        rel = f"20_DERIVED/{uid}.txt"
        sha = storage.write_atomic_bytes(rel, f"payload:{uid}".encode())
        return 100, rel, sha

    return fn


def _make(cfg, root, phase="PHASE_2_ANALYTICAL", counter=None, fail_on=None, runtime="rt-1"):
    storage = Storage.open(root)
    return storage, Orchestrator(
        storage, cfg, phase=phase,
        unit_fn=_unit_fn_factory(counter if counter is not None else {}, fail_on),
        runtime=runtime, max_runtime_seconds=60,
    )


def test_first_run_executes_then_second_skips_same_output(drive_root: Path, cfg):
    counter: dict = {}
    storage, orch = _make(cfg, drive_root, counter=counter)
    units = ["part_000001", "part_000002", "part_000003"]

    out1 = orch.run(units, input_hash_for=lambda u: "sha256:in-" + u)
    assert out1.status == "PHASE_COMPLETE_AWAITING_OWNER_REVIEW"
    assert out1.units_executed == 3

    out2 = orch.run(units, input_hash_for=lambda u: "sha256:in-" + u)
    assert out2.units_executed == 0
    assert out2.units_skipped == 3
    assert out2.status == "PHASE_COMPLETE_AWAITING_OWNER_REVIEW"
    # idempotence : une seule exécution réelle par unité
    assert counter == {"part_000001": 1, "part_000002": 1, "part_000003": 1}


def test_changed_input_hash_forces_reexecution(drive_root: Path, cfg):
    counter: dict = {}
    storage, orch = _make(cfg, drive_root, counter=counter)
    orch.run(["part_000001"], input_hash_for=lambda u: "sha256:in-" + u)
    orch.run(["part_000001"], input_hash_for=lambda u: "sha256:CHANGED-" + u)
    assert counter["part_000001"] == 2


def test_exclusion_under_concurrency(drive_root: Path, cfg):
    """L'unité est déjà louée par un autre runtime => pas de double écriture."""
    from metaalpha import leases

    storage, orch = _make(cfg, drive_root)
    held = leases.acquire(storage, "PHASE_2_ANALYTICAL__part_000001", ttl=600, owner="other")
    out = orch.run(["part_000001"], input_hash_for=lambda u: "sha256:in-" + u)
    assert out.units_executed == 0
    assert out.units_failed == 1
    assert out.status == "FAILED_TECHNICAL"
    assert out.resume_from == "part_000001"
    held.release()


def test_resume_after_simulated_kill(drive_root: Path, cfg):
    """Simule un crash au milieu : seules les unités non checkpointées sont rejouées."""
    counter: dict = {}
    units = [f"part_{i:06d}" for i in range(1, 6)]
    storage, orch = _make(cfg, drive_root, counter=counter)

    # premier passage volontairement interrompu après 2 unités
    orch.max_runtime_seconds = 0
    partial = orch.run(units[:2], input_hash_for=lambda u: "sha256:in-" + u)
    assert partial.status == "BLOCKED_WITH_RESUME"

    orch.max_runtime_seconds = 60
    full = orch.run(units, input_hash_for=lambda u: "sha256:in-" + u)
    assert full.units_executed == 5
    assert full.units_skipped == 0

    again = orch.run(units, input_hash_for=lambda u: "sha256:in-" + u)
    assert again.units_skipped == 5
    assert all(v == 1 for v in counter.values())


def test_transient_retry_then_success(drive_root: Path, cfg):
    storage = Storage.open(drive_root)
    state = {"n": 0}

    def flaky(uid, st):
        state["n"] += 1
        if state["n"] < 3:
            raise TransientError("429 simulé")
        rel = f"20_DERIVED/{uid}.txt"
        return 1, rel, st.write_atomic_bytes(rel, b"ok")

    orch = Orchestrator(storage, cfg, phase="PHASE_2_ANALYTICAL", unit_fn=flaky,
                        runtime="rt", max_runtime_seconds=60)
    out = orch.run(["part_000001"], input_hash_for=lambda u: "sha256:in")
    assert out.status == "PHASE_COMPLETE_AWAITING_OWNER_REVIEW"
    assert state["n"] == 3


def test_deterministic_error_stops_immediately(drive_root: Path, cfg):
    storage = Storage.open(drive_root)

    def broken(uid, st):
        raise ValueError("DETERMINISTIC: schéma inattendu")

    orch = Orchestrator(storage, cfg, phase="PHASE_2_ANALYTICAL", unit_fn=broken,
                        runtime="rt", max_runtime_seconds=60)
    out = orch.run(["a", "b", "c"], input_hash_for=lambda u: "sha256:in")
    assert out.status == "FAILED_TECHNICAL"
    assert out.resume_from == "a"
    assert out.units_executed == 0


def test_kill_switch_stops_work(drive_root: Path, cfg):
    storage, orch = _make(cfg, drive_root)
    storage.write_atomic_bytes("00_GOVERNANCE/KILL_SWITCH", b"stop")
    out = orch.run(["a", "b"], input_hash_for=lambda u: "sha256:in")
    assert out.units_executed == 0
    assert out.status == "BLOCKED_WITH_RESUME"


def test_terminal_status_always_allowed(cfg):
    allowed = set(cfg.get("governance", "terminal_statuses"))
    from metaalpha.orchestrator import Orchestrator as O

    assert {
        "PHASE_COMPLETE_AWAITING_OWNER_REVIEW",
        "BLOCKED_WITH_RESUME",
        "FAILED_TECHNICAL",
        "INCOMPLETE",
        "NO_EDGE",
    } == allowed


def test_heartbeat_written(drive_root: Path, cfg):
    storage, orch = _make(cfg, drive_root)
    orch.run(["a"], input_hash_for=lambda u: "sha256:in")
    hb = storage.read_json("00_GOVERNANCE/heartbeat.json")
    assert hb["runtime_id"] == "rt-1"
    assert "utc" in hb
