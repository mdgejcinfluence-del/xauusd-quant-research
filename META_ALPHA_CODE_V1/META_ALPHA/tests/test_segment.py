"""Tests du segment jetable : la preuve que la session peut mourir à tout moment."""
from __future__ import annotations

import json
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from metaalpha.remote import LocalRemote
from metaalpha.segment import run_segment

ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture
def test_cfg(tmp_path: Path) -> Path:
    """Config de test : seuil disque abaissé (le bac à sable fait 1 Go).
    En production on garde min_free_gb=2 sur Kaggle/Colab (20 Go+)."""
    cfg = json.loads((ROOT / "config" / "execution_config.json").read_text())
    cfg["orchestrator"]["min_free_gb"] = 0.01
    cfg["orchestrator"]["disk_guard_ratio"] = 0.0
    p = tmp_path / "test_config.json"
    p.write_text(json.dumps(cfg))
    return p


@pytest.fixture
def corpus(tmp_path: Path) -> Path:
    """Corpus distant simulé (ce que Drive serait)."""
    root = tmp_path / "drive"
    parts = root / "01_PARQUET/XAUUSD_DGP_CHRONOLOGICAL_V5R10/PARTITIONS"
    parts.mkdir(parents=True)
    (root / "04_CHECKPOINTS").mkdir(parents=True)
    (root / "04_CHECKPOINTS/PHASE_02_DGP_BASE_CHRONOLOGICAL_VALIDATED_V5R10.json").write_text(
        json.dumps({"status": "CERTIFIED", "output_partitions": 348})
    )
    for i in range(1, 5):
        n = 2000
        ts = pa.array([1_600_000_000_000 + j * 200 for j in range(n)], type=pa.timestamp("ms", tz="UTC"))
        bid = pa.array([1900.0 + (j % 53) * 0.01 for j in range(n)], type=pa.float64())
        ask = pa.array([1900.2 + (j % 53) * 0.01 for j in range(n)], type=pa.float64())
        pq.write_table(pa.table({"timestamp": ts, "bid": bid, "ask": ask}),
                       parts / f"part_{i:06d}.parquet")
    return root


def _run(corpus: Path, tmp_path: Path, cfg_path: Path, **kw):
    return run_segment(
        phase="PHASE_2_ANALYTICAL",
        config_path=cfg_path,
        remote=LocalRemote(corpus),
        workdir=tmp_path / "work",
        local_root=str(tmp_path / "research"),
        **kw,
    )


def test_segment_processes_one_batch_then_stops(corpus: Path, tmp_path: Path, test_cfg: Path):
    rep = _run(corpus, tmp_path, test_cfg, max_units=2, segment_minutes=10)
    assert rep["units_executed"] == 2
    assert rep["status"] == "BLOCKED_WITH_RESUME"
    assert rep["resume_from"] is not None          # point de reprise explicite


def test_segment_resumes_without_recomputing(corpus: Path, tmp_path: Path, test_cfg: Path):
    _run(corpus, tmp_path, test_cfg, max_units=2, segment_minutes=10)
    rep2 = _run(corpus, tmp_path, test_cfg, max_units=4, segment_minutes=10)
    assert rep2["units_skipped_from_checkpoint"] == 2   # jamais recalculées
    assert rep2["units_executed"] == 2


def test_segment_finishes_all_units(corpus: Path, tmp_path: Path, test_cfg: Path):
    rep = _run(corpus, tmp_path, test_cfg, max_units=10, segment_minutes=10)
    assert rep["units_executed"] == 4
    assert rep["status"] == "PHASE_COMPLETE_AWAITING_OWNER_REVIEW"


def test_segment_publishes_artifacts_to_remote(corpus: Path, tmp_path: Path, test_cfg: Path):
    _run(corpus, tmp_path, test_cfg, max_units=4, segment_minutes=10)
    derived = list((corpus / "RESEARCH_V1_XAUUSD_TICK_ONLY/20_DERIVED").rglob("*.parquet"))
    ckpts = list((corpus / "RESEARCH_V1_XAUUSD_TICK_ONLY/00_GOVERNANCE/checkpoints").rglob("*.json"))
    assert len(derived) == 4, "les dérivés doivent être publiés sur le backend distant"
    assert len(ckpts) == 4, "les checkpoints doivent être publiés sur le backend distant"


def test_segment_leaves_no_local_bulk_copy(corpus: Path, tmp_path: Path, test_cfg: Path):
    """Une session ne conserve rien : les partitions téléchargées sont purgées."""
    _run(corpus, tmp_path, test_cfg, max_units=2, segment_minutes=10)
    leftovers = list((tmp_path / "work").rglob("*.parquet"))
    assert leftovers == []


def test_segment_time_limit_stops_cleanly(corpus: Path, tmp_path: Path, test_cfg: Path):
    rep = _run(corpus, tmp_path, test_cfg, max_units=100, segment_minutes=0)
    assert rep["status"] in {"BLOCKED_WITH_RESUME", "PHASE_COMPLETE_AWAITING_OWNER_REVIEW"}
    if rep["units_executed"] == 0:
        assert "SEGMENT_TIME_LIMIT" in rep["errors"]


def test_segment_writes_report(corpus: Path, tmp_path: Path, test_cfg: Path):
    _run(corpus, tmp_path, test_cfg, max_units=1, segment_minutes=10)
    reports = list((corpus / "RESEARCH_V1_XAUUSD_TICK_ONLY/40_REPORTS").rglob("*_segment.json"))
    assert reports, "un rapport de segment doit être publié"
    body = json.loads(reports[0].read_text())
    assert body["phase"] == "PHASE_2_ANALYTICAL"
    assert "resume_from" in body
