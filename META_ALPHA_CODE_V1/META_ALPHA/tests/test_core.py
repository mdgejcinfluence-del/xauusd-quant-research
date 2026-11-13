from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from metaalpha import checkpoints, leases, registry
from metaalpha.checkpoints import UnitKey
from metaalpha.fs import Storage, WriteDenied
from metaalpha.governance import (
    CostKind,
    CostSemanticError,
    HoldoutSealedError,
    PhaseTransitionError,
    PolicyMissingError,
    ReadOnlyView,
    approve_phase,
    assert_cost_semantics,
    assert_phase_authorized,
    open_holdout_once,
    require_policy,
    seal_holdout,
)


# ---------------------------------------------------------------- fs
def test_write_allowed_inside_research_zone(drive_root: Path):
    s = Storage.open(drive_root)
    sha = s.write_atomic_json("10_REGISTRIES/x.json", {"a": 1})
    assert sha.startswith("sha256:")
    assert (drive_root / "RESEARCH_V1_XAUUSD_TICK_ONLY" / "10_REGISTRIES" / "x.json").exists()


@pytest.mark.parametrize("rel", ["01_PARQUET/t.parquet", "04_CHECKPOINTS/c.json", "00_RAW/r.bin"])
def test_write_denied_on_certified_base(drive_root: Path, rel: str):
    s = Storage.open(drive_root)
    with pytest.raises(WriteDenied):
        s.write_atomic_json(rel, {"x": 1})


def test_atomic_write_leaves_no_tmp(drive_root: Path):
    s = Storage.open(drive_root)
    s.write_atomic_json("40_REPORTS/r.json", {"ok": True})
    assert not list(drive_root.rglob("*.tmp"))


# ------------------------------------------------------------- leases
def test_lease_exclusion(drive_root: Path):
    s = Storage.open(drive_root)
    a = leases.acquire(s, "unit", ttl=60, owner="runtime-A")
    with pytest.raises(leases.LeaseHeld):
        leases.acquire(s, "unit", ttl=60, owner="runtime-B")
    a.release()
    b = leases.acquire(s, "unit", ttl=60, owner="runtime-B")  # libéré -> réacquérable
    assert b.owner == "runtime-B"


def test_expired_lease_can_be_taken(drive_root: Path):
    s = Storage.open(drive_root)
    rel = "00_GOVERNANCE/leases/unit.lease"
    s.write_atomic_json(rel, {"owner": "dead", "expires": 0, "pid": 1})
    got = leases.acquire(s, "unit", ttl=60, owner="alive")
    assert got.owner == "alive"


# --------------------------------------------------------- checkpoints
def test_checkpoint_validity_tracks_hashes(drive_root: Path):
    s = Storage.open(drive_root)
    s.write_atomic_json("20_DERIVED/out.parquet.sha", {"x": 1})
    key = UnitKey("PHASE_2_ANALYTICAL", "u1", "sha256:a", "sha256:b", "sha256:c")
    assert not checkpoints.is_valid(s, key)
    checkpoints.write(s, key, output_rel="20_DERIVED/out.parquet.sha",
                      output_sha="sha256:dead", rows=10, elapsed_s=1.0,
                      runtime="t", attempts=1)
    assert checkpoints.is_valid(s, key)
    # config modifiée => checkpoint invalidé
    key2 = UnitKey("PHASE_2_ANALYTICAL", "u1", "sha256:a", "sha256:b", "sha256:DIFFERENT")
    assert not checkpoints.is_valid(s, key2)


# -------------------------------------------------------- governance
def test_phase_sequence_enforced(drive_root: Path):
    s = Storage.open(drive_root)
    with pytest.raises(PhaseTransitionError):
        assert_phase_authorized(s, "PHASE_2_ANALYTICAL")  # non approuvée
    approve_phase(s, "PHASE_2_ANALYTICAL", "je-approuve-phase-2", "revue initiale")
    assert_phase_authorized(s, "PHASE_2_ANALYTICAL")
    with pytest.raises(PhaseTransitionError):
        assert_phase_authorized(s, "PHASE_3_MINING")  # P2 non terminée


def test_approval_requires_signature(drive_root: Path):
    s = Storage.open(drive_root)
    with pytest.raises(PhaseTransitionError):
        approve_phase(s, "PHASE_2_ANALYTICAL", "court")


def test_holdout_sealed_without_key(drive_root: Path, monkeypatch):
    s = Storage.open(drive_root)
    monkeypatch.delenv("HOLDOUT_SEAL_KEY", raising=False)
    with pytest.raises(HoldoutSealedError):
        seal_holdout(s, "sha256:s", "sha256:l")


def test_holdout_single_open_and_tamper_detection(drive_root: Path, monkeypatch):
    s = Storage.open(drive_root)
    monkeypatch.setenv("HOLDOUT_SEAL_KEY", "cle-secrete-hors-drive")
    seal_holdout(s, "sha256:s", "sha256:l")
    open_holdout_once(s, "sha256:s", "sha256:l")
    with pytest.raises(HoldoutSealedError):          # seconde ouverture interdite
        open_holdout_once(s, "sha256:s", "sha256:l")


def test_holdout_seal_detects_modified_manifest(drive_root: Path, monkeypatch):
    s = Storage.open(drive_root)
    monkeypatch.setenv("HOLDOUT_SEAL_KEY", "k")
    seal_holdout(s, "sha256:s", "sha256:l")
    with pytest.raises(HoldoutSealedError):          # lock manifest modifié
        open_holdout_once(s, "sha256:s", "sha256:AUTRE")


def test_policy_missing_blocks_promotion(drive_root: Path):
    s = Storage.open(drive_root)
    with pytest.raises(PolicyMissingError):
        require_policy(s, ["min_trades", "max_drawdown"])


def test_unknown_cost_is_never_zero():
    with pytest.raises(CostSemanticError):
        assert_cost_semantics({"spread": "OBSERVED", "swap": CostKind.UNKNOWN.value})
    assert_cost_semantics({"spread": "OBSERVED", "swap": "SCENARIO"})


# ---------------------------------------------------------- registries
def test_registry_requires_human_authorship(drive_root: Path):
    s = Storage.open(drive_root)
    registry.init_registries(s)
    with pytest.raises(registry.OwnerAttributionError):
        registry.register_formula(
            s,
            {
                "formula_id": "F1", "version": "1", "name": "x",
                "mathematical_definition": "inventée par un LLM",
                "inputs": [], "parameters": {}, "nan_policy": "KEEP",
                "event_alignment_rule": "t", "execution_definition": "e",
                "cost_definition": "c", "created_by": "LLM",
            },
        )


def test_formula_status_cannot_skip(drive_root: Path):
    s = Storage.open(drive_root)
    registry.init_registries(s)
    registry.register_formula(
        s,
        {
            "formula_id": "F1", "version": "1", "name": "x",
            "mathematical_definition": "def", "inputs": ["bid"], "parameters": {"w": 30},
            "nan_policy": "KEEP", "event_alignment_rule": "t",
            "execution_definition": "e", "cost_definition": "c", "created_by": "HUMAN",
        },
    )
    with pytest.raises(registry.RegistryCycleError):
        registry.advance_formula(s, "F1@1", "CAUSALITY_AUDITED", {"artifact_sha": "sha256:x"})
    registry.advance_formula(s, "F1@1", "PREREGISTERED", {"artifact_sha": "sha256:x"})


def test_trial_ledger_is_append_only(drive_root: Path):
    s = Storage.open(drive_root)
    registry.init_registries(s)
    base = {k: "" for k in registry.TRIAL_LEDGER_HEADER}
    base.update({"trial_id": "T1", "outcome": "NEGATIVE", "value": "-0.1"})
    registry.log_trial(s, base)
    base.update({"trial_id": "T2", "outcome": "NEGATIVE"})
    registry.log_trial(s, base)
    assert registry.count_trials(s) == 2          # y compris l'essai négatif
    content = (drive_root / "RESEARCH_V1_XAUUSD_TICK_ONLY" / "10_REGISTRIES" / "TRIAL_LEDGER.csv").read_text()
    assert "T1" in content and "T2" in content


# ------------------------------------------------------------ IA
def test_ai_has_no_write_access(drive_root: Path, cfg):
    from metaalpha.ai_supervisor import Supervisor

    s = Storage.open(drive_root)
    sup = Supervisor(ReadOnlyView(s), cfg)
    with pytest.raises(PermissionError):
        sup.write_anything("10_REGISTRIES/hack.json", {"status": "CERTIFIED"})


def test_ai_rejects_out_of_schema(drive_root: Path, cfg):
    from metaalpha.ai_supervisor import AIResponseInvalid, validate

    with pytest.raises(AIResponseInvalid):
        validate({"resume": "ok", "incoherences": [], "manquants": [], "questions": [],
                  "edge_certified": True})
    assert validate({"resume": "r", "incoherences": [], "manquants": [], "questions": []})
