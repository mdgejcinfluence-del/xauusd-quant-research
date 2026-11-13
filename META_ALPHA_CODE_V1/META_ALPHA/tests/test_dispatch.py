"""Tests de la couche de lancement (sessions temporaires, sans navigateur)."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from metaalpha.dispatch import build_kernel_dir, plan_units, read_done_from_drive
from metaalpha.remote import LocalRemote


# --------------------------------------------------------------- plan_units
def test_plan_units_respects_state_and_batch():
    units = [f"part_{i:06d}" for i in range(1, 11)]
    done = {"part_000001", "part_000002", "part_000004"}
    batch = plan_units(units, done, 3)
    assert batch == ["part_000003", "part_000005", "part_000006"]


def test_plan_units_never_duplicates_work():
    units = ["a", "b", "c"]
    assert plan_units(units, set(), 5) == ["a", "b", "c"]
    assert plan_units(units, {"a", "b", "c"}, 5) == []


def test_plan_units_is_deterministic():
    units = [f"u{i}" for i in range(20)]
    assert plan_units(units, {"u3"}, 4) == plan_units(units, {"u3"}, 4)


def test_plan_units_survives_lost_segment():
    """Un kernel mort sans rien publier => replanification identique."""
    units = [f"u{i}" for i in range(10)]
    done_before = {"u0", "u1"}
    first = plan_units(units, done_before, 3)
    # le segment n'a rien publié : l'état n'a pas bougé
    again = plan_units(units, done_before, 3)
    assert first == again == ["u2", "u3", "u4"]


# ------------------------------------------------------- build_kernel_dir
def test_kernel_metadata_is_valid_and_no_gpu(tmp_path: Path):
    d = build_kernel_dir(tmp_path / "k", kernel_id="owner/meta-alpha-segment",
                         phase="PHASE_2_ANALYTICAL", n_units=40)
    meta = json.loads((d / "kernel-metadata.json").read_text())
    assert meta["id"] == "owner/meta-alpha-segment"
    assert meta["title"] == "meta-alpha-segment"      # slug == titre (sinon 403/409 Kaggle)
    assert meta["code_file"] == "main.py"
    assert meta["kernel_type"] == "script"            # batch, pas interactif
    assert meta["is_private"] is True
    assert meta["enable_gpu"] is False                # aucun GPU : inutile ici
    assert meta["enable_internet"] is True


def test_kernel_script_contains_no_secret_and_no_formula(tmp_path: Path):
    d = build_kernel_dir(tmp_path / "k", kernel_id="o/s", phase="PHASE_2_ANALYTICAL", n_units=5)
    src = (d / "main.py").read_text()
    # aucun secret en dur
    for bad in ("BEGIN PRIVATE KEY", "nvapi-", "client_secret", "AKIA"):
        assert bad not in src
    # les secrets viennent de Kaggle Secrets, jamais du dépôt
    assert "UserSecretsClient" in src
    # le kernel ne fait que cloner le dépôt et appeler run_segment
    assert '"git", "clone"' in src and "run_segment" in src


def test_kernel_id_must_be_owner_slug(tmp_path: Path):
    with pytest.raises(ValueError):
        build_kernel_dir(tmp_path / "k", kernel_id="pas-de-slash",
                         phase="PHASE_2_ANALYTICAL", n_units=1)


# ------------------------------------------------------ read_done_from_drive
def test_read_done_from_drive(tmp_path: Path):
    root = tmp_path / "remote"
    ck_dir = root / "RESEARCH_V1_XAUUSD_TICK_ONLY/00_GOVERNANCE/checkpoints/PHASE_2_ANALYTICAL"
    ck_dir.mkdir(parents=True)
    (ck_dir / "part_000001.json").write_text(json.dumps({"unit_id": "part_000001", "status": "VALID"}))
    (ck_dir / "part_000002.json").write_text(json.dumps({"unit_id": "part_000002", "status": "INVALIDATED"}))
    done = read_done_from_drive("PHASE_2_ANALYTICAL", remote=LocalRemote(root))
    assert done == {"part_000001"}          # un checkpoint invalidé n'est PAS fait


def test_read_done_resilient_when_absent(tmp_path: Path):
    assert read_done_from_drive("PHASE_9_MQL5", remote=LocalRemote(tmp_path)) == set()


# -------------------------------------------------------- anti-boucle
def test_autonomy_loop_stops_when_no_progress(tmp_path: Path, monkeypatch):
    """Un segment qui ne publie rien ne doit PAS être repoussé indéfiniment."""
    from metaalpha import dispatch

    calls = {"n": 0}

    def fake_push(run_dir, dry_run=False):
        calls["n"] += 1
        return dispatch.DispatchResult(True, "", str(run_dir), "push", "ok")

    def fake_wait(kernel_id, dest, **kw):
        return {"kernel_id": kernel_id, "final_status": "COMPLETE"}

    monkeypatch.setattr(dispatch, "push", fake_push)
    monkeypatch.setattr(dispatch, "wait_and_collect", fake_wait)
    monkeypatch.setattr(dispatch, "read_done_from_drive", lambda phase: set())  # rien ne progresse

    res = dispatch.autonomy_loop(
        kernel_id="o/s", phase="PHASE_2_ANALYTICAL",
        units_all=[f"u{i}" for i in range(8)], done=set(), n_units=4,
        run_root=tmp_path, max_segments=5,
        git_url="https://example.invalid/repo.git", dry_run=False,
    )
    assert calls["n"] == 1, "un seul push avant détection de l'absence de progrès"
    assert any(seg.get("state") == "NO_PROGRESS_STOP" for seg in res["segments"])


def test_autonomy_loop_stops_when_all_units_done(tmp_path: Path):
    from metaalpha import dispatch

    res = dispatch.autonomy_loop(
        kernel_id="o/s", phase="PHASE_2_ANALYTICAL",
        units_all=["a", "b"], done={"a", "b"}, n_units=4,
        run_root=tmp_path, max_segments=3,
        git_url="https://example.invalid/repo.git", dry_run=True,
    )
    assert res["segments"][0]["state"] == "ALL_UNITS_DONE"
    assert res["remaining"] == 0
