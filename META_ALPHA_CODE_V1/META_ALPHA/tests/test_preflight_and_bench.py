from __future__ import annotations

import json
from pathlib import Path

from metaalpha.bench import bench_partition, extrapolate
from metaalpha.preflight import run_preflight


def test_preflight_ok(drive_root: Path):
    rep = run_preflight(str(drive_root))
    assert rep["status"].startswith("PREFLIGHT_OK")
    assert rep["partitions"]["count"] == 348
    assert rep["certificates"]["PHASE_01"]["sha256"].startswith("sha256:")
    assert rep["certificates"]["PHASE_02"]["fields"]["phase_3_started"] is False
    assert rep["writes_performed"] is False
    assert rep["holdout_touched"] is False


def test_preflight_detects_missing_certificate(drive_root: Path):
    (drive_root / "04_CHECKPOINTS" / "PHASE_01_XAUUSD_PRIMARY_CERTIFIED.json").unlink()
    rep = run_preflight(str(drive_root))
    assert rep["status"] == "BLOCKED_WITH_RESUME"
    assert any("MISSING_CERTIFICATE" in b for b in rep["blocking"])


def test_preflight_detects_wrong_partition_count(drive_root: Path):
    (drive_root / "01_PARQUET/XAUUSD_DGP_CHRONOLOGICAL_V5R10/PARTITIONS/part_000348.parquet").unlink()
    rep = run_preflight(str(drive_root))
    assert rep["status"] == "BLOCKED_WITH_RESUME"
    assert any("PARTITION_COUNT" in b for b in rep["blocking"])


def test_preflight_measures_real_schema(small_corpus: Path):
    rep = run_preflight(str(small_corpus), sample="part_000001.parquet")
    schema = rep["observations"][0]["sample_schema"]
    names = [c["name"] for c in schema["columns"]]
    assert names == ["timestamp", "bid", "ask"]
    assert schema["num_rows"] == 550


def test_bench_measures_and_labels_extrapolation(small_corpus: Path):
    parts = sorted((small_corpus / "01_PARQUET/XAUUSD_DGP_CHRONOLOGICAL_V5R10/PARTITIONS").glob("*.parquet"))
    runs = [bench_partition(p, memory_limit="1GB", threads=1) for p in parts[:3]]
    assert all(r["rows_per_s"] and r["rows_per_s"] > 0 for r in runs)
    ext = extrapolate(runs, n_partitions_total=348, parallelism=1)
    assert "PAS UN BENCHMARK RÉEL" in ext["label"]
    assert ext["eta_hours_high"] >= ext["eta_hours_low"]
