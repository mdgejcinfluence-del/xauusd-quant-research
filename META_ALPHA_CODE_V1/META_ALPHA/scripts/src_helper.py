"""Petit utilitaire de démonstration : construit un corpus distant simulé."""
from __future__ import annotations

import json
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq


def build_corpus(root: Path, n_parts: int = 10, rows: int = 1500) -> Path:
    parts = root / "01_PARQUET" / "XAUUSD_DGP_CHRONOLOGICAL_V5R10" / "PARTITIONS"
    parts.mkdir(parents=True, exist_ok=True)
    (root / "04_CHECKPOINTS").mkdir(parents=True, exist_ok=True)
    (root / "04_CHECKPOINTS" / "PHASE_02_DGP_BASE_CHRONOLOGICAL_VALIDATED_V5R10.json").write_text(
        json.dumps({"status": "CERTIFIED", "output_partitions": 348, "phase_3_started": False})
    )
    for i in range(1, n_parts + 1):
        ts = pa.array([1_600_000_000_000 + j * 200 for j in range(rows)],
                      type=pa.timestamp("ms", tz="UTC"))
        base = 1900.0 + i
        bid = pa.array([base + (j % 53) * 0.01 for j in range(rows)], type=pa.float64())
        ask = pa.array([base + 0.2 + (j % 53) * 0.01 for j in range(rows)], type=pa.float64())
        pq.write_table(pa.table({"timestamp": ts, "bid": bid, "ask": ask}),
                       parts / f"part_{i:06d}.parquet")
    return root
