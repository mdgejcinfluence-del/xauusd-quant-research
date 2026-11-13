"""Fixtures communes. Toutes les données de test sont SYNTHÉTIQUES et
ne prouvent rien sur le marché : elles ne testent que les chemins de code.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from metaalpha.config import Config

ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture
def cfg() -> Config:
    return Config.load(ROOT / "config" / "execution_config.json")


@pytest.fixture
def drive_root(tmp_path: Path) -> Path:
    root = tmp_path / "META_ALPHA_XAUUSD_DGP"
    (root / "04_CHECKPOINTS").mkdir(parents=True)
    (root / "01_PARQUET" / "XAUUSD_DGP_CHRONOLOGICAL_V5R10" / "PARTITIONS").mkdir(parents=True)

    (root / "04_CHECKPOINTS" / "PHASE_01_XAUUSD_PRIMARY_CERTIFIED.json").write_text(
        json.dumps(
            {
                "status": "CERTIFIED",
                "symbol": "XAUUSD",
                "raw_files": 11136,
                "parquet_files": 11136,
                "total_ticks_validated": 685118625,
                "synthetic_data": False,
                "interpolation": False,
            }
        )
    )
    (root / "04_CHECKPOINTS" / "PHASE_02_DGP_BASE_CHRONOLOGICAL_VALIDATED_V5R10.json").write_text(
        json.dumps(
            {
                "status": "CERTIFIED",
                "phase": "PHASE_02",
                "output_partitions": 348,
                "output_rows": 685118625,
                "observation_unit": "NATIVE_XAUUSD_TICK_EVENT",
                "chronological_order": True,
                "phase_3_started": False,
                "formula_registry_status": "PARTIAL",
                "scientific_families_undefined": 19,
            }
        )
    )
    for i in range(1, 349):
        (root / "01_PARQUET" / "XAUUSD_DGP_CHRONOLOGICAL_V5R10" / "PARTITIONS" / f"part_{i:06d}.parquet").write_bytes(b"")
    return root


@pytest.fixture
def small_corpus(tmp_path: Path) -> Path:
    """6 vraies partitions Parquet avec des ticks synthétiques."""
    import pyarrow as pa
    import pyarrow.parquet as pq

    root = tmp_path / "META_ALPHA_XAUUSD_DGP"
    parts = root / "01_PARQUET" / "XAUUSD_DGP_CHRONOLOGICAL_V5R10" / "PARTITIONS"
    parts.mkdir(parents=True)
    (root / "04_CHECKPOINTS").mkdir(parents=True)
    for name, body in (
        ("PHASE_01_XAUUSD_PRIMARY_CERTIFIED.json", {"status": "CERTIFIED", "raw_files": 11136,
                                                    "total_ticks_validated": 685118625}),
        ("PHASE_02_DGP_BASE_CHRONOLOGICAL_VALIDATED_V5R10.json",
         {"status": "CERTIFIED", "output_partitions": 348, "output_rows": 685118625,
          "observation_unit": "NATIVE_XAUUSD_TICK_EVENT", "chronological_order": True,
          "phase_3_started": False}),
    ):
        (root / "04_CHECKPOINTS" / name).write_text(json.dumps(body))
    for i in range(1, 7):
        n = 500 + i * 50
        ts = pa.array([1700000000000 + j * 150 for j in range(n)], type=pa.timestamp("ms", tz="UTC"))
        bid = pa.array([2000.0 + (j % 97) * 0.01 for j in range(n)], type=pa.float64())
        ask = pa.array([2000.2 + (j % 97) * 0.01 for j in range(n)], type=pa.float64())
        pq.write_table(
            pa.table({"timestamp": ts, "bid": bid, "ask": ask}), parts / f"part_{i:06d}.parquet"
        )
    return root
