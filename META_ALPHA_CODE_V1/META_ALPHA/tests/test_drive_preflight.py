"""Le préflight doit refuser de démarrer sur une baseline non vérifiable.

C'est le test le plus important du dépôt public : il prouve que le système ne
peut pas produire d'artéfact scientifique à partir d'un Drive vide, mal monté
ou modifié.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from metaalpha.drive_preflight import (
    CERT_P1_REL, CERT_P2_REL, EXPECTED_PARTITIONS, PARTITIONS_REL,
    PreflightFailure, check_certificates, check_partitions, run_preflight,
)
from metaalpha.remote import LocalRemote


def _cert(status="CERTIFIED") -> dict:
    return {"status": status, "symbol": "XAUUSD", "phase": "test"}


@pytest.fixture()
def fake_drive(tmp_path: Path) -> Path:
    root = tmp_path / "META_ALPHA_XAUUSD_DGP"
    (root / "04_CHECKPOINTS").mkdir(parents=True)
    (root / CERT_P1_REL).write_text(json.dumps(_cert()))
    (root / CERT_P2_REL).write_text(json.dumps(_cert()))
    parts = root / PARTITIONS_REL
    parts.mkdir(parents=True)
    for i in range(1, EXPECTED_PARTITIONS + 1):
        (parts / f"part_{i:06d}.parquet").write_bytes(b"PAR1")
    return root


def test_preflight_passes_on_complete_baseline(fake_drive):
    rep = run_preflight(LocalRemote(fake_drive))
    assert rep["status"] == "PASS"
    assert rep["baseline_manifest"]["partitions_count"] == EXPECTED_PARTITIONS
    assert len(rep["baseline_manifest"]["p1_sha256_canonical"]) == 64


def test_missing_certificate_blocks(fake_drive):
    (fake_drive / CERT_P2_REL).unlink()
    with pytest.raises(PreflightFailure) as e:
        check_certificates(LocalRemote(fake_drive))
    assert e.value.code == "CERTIFICATE_MISSING"


def test_uncertified_certificate_blocks(fake_drive):
    (fake_drive / CERT_P1_REL).write_text(json.dumps(_cert("PARTIAL")))
    with pytest.raises(PreflightFailure) as e:
        check_certificates(LocalRemote(fake_drive))
    assert e.value.code == "CERTIFICATE_NOT_CERTIFIED"


def test_missing_partition_blocks_and_never_rounds_up(fake_drive):
    (fake_drive / PARTITIONS_REL / "part_000042.parquet").unlink()
    with pytest.raises(PreflightFailure) as e:
        check_partitions(LocalRemote(fake_drive))
    assert e.value.code == "PARTITION_COUNT_MISMATCH"
    assert "347" in e.value.detail


def test_unexpected_partition_name_blocks(fake_drive):
    (fake_drive / PARTITIONS_REL / "part_000001.parquet").rename(
        fake_drive / PARTITIONS_REL / "backup_000001.parquet")
    with pytest.raises(PreflightFailure) as e:
        check_partitions(LocalRemote(fake_drive))
    assert e.value.code == "PARTITION_NAMING_UNEXPECTED"


def test_no_backend_reports_instead_of_crashing(monkeypatch):
    monkeypatch.delenv("METAALPHA_LOCAL_ROOT", raising=False)
    monkeypatch.delenv("GDRIVE_SA_JSON", raising=False)
    monkeypatch.delenv("GDRIVE_ROOT_FOLDER_ID", raising=False)
    rep = run_preflight()
    assert rep["status"] == "BLOCKED_NO_BACKEND"
    assert rep["steps"][0]["ok"] is False


def test_baseline_hash_changes_if_certificate_content_changes(fake_drive):
    r = LocalRemote(fake_drive)
    h1 = run_preflight(r)["baseline_manifest"]["p2_sha256_canonical"]
    doc = json.loads((fake_drive / CERT_P2_REL).read_text())
    doc["note"] = "retouche"
    (fake_drive / CERT_P2_REL).write_text(json.dumps(doc))
    h2 = run_preflight(r)["baseline_manifest"]["p2_sha256_canonical"]
    assert h1 != h2   # toute modification du certificat est détectée


def test_partitions_listing_hash_is_order_independent(fake_drive):
    r = LocalRemote(fake_drive)
    h1 = run_preflight(r)["baseline_manifest"]["partitions_listing_sha256"]
    h2 = run_preflight(r)["baseline_manifest"]["partitions_listing_sha256"]
    assert h1 == h2
