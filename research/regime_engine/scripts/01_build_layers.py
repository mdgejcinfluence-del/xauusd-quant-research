#!/usr/bin/env python3
"""
PHASE 3 - build M3 (primary) and H1 (context) grids from the master M1 file.

RECOVERY NOTE (2026-09-06): the original Phase-3 `01_build_layers.py` was lost
in the workspace reset. This file re-implements the SAME construction contract
from the COMMITTED Phase-2B source `research/timeframe_audit/scripts/
build_timeframes.py` (SHA-256 02d4fcdb77a325cce3b8f3b220f7c44b3b326512bf789e8cb1928d4d7a78adcc),
whose protocol and outputs are recorded in the committed Phase-2B reports.
The protocol is therefore a genuine, auditable source (not a reconstruction
guess):

  origin        : 1970-01-01 00:00:00 UTC
  alignment     : bar_id = floor(epoch_minutes / k)
  timezone      : UTC
  bucket        : t_min // k  (bars are grouped by epoch-aligned buckets)
  validity      : a bar exists iff >= 1 real M1 bar is in its bucket - NO
                  completeness requirement, NO invented bar, NO padding
  open/high/low/close : first / max / min / last of the real M1 bars
  volume        : NEVER read (Phase 1 L1)
  counters      : n_m1, internal_missing, internal_breaks (>=50 min),
                  contig_next - identical to the Phase-2B builder

Output column naming follows the Phase-2B convention (ts, open, high, low,
close, n_m1, internal_missing, internal_breaks, contig_next), extended with
the deterministic helpers bar_id (Int64) and t_min (Int64, minutes).

Usage:
  python3 01_build_layers.py
    writes:
      /tmp/xauusd_audit/regime_engine/m3_grid.parquet
      /tmp/xauusd_audit/regime_engine/h1_grid.parquet
      /tmp/xauusd_audit/regime_engine/grid_manifest.json
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from datetime import datetime, timezone

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from p3_common import (  # noqa: E402
    CONTEXT_MIN, MASTER, MASTER_SHA, MASTER_ROWS, MARKET_BREAK_MIN,
    PRIMARY_MIN, SCRATCH, sha256_file,
)

CHUNK = 1 << 20


def load_master(path: str) -> dict:
    """Load ONLY timestamp/OHLC; the volume column is deliberately not read (L1)."""
    t = pq.read_table(path, columns=["timestamp", "open", "high", "low", "close"])
    ts = t.column("timestamp").to_numpy(zero_copy_only=False)
    o = t.column("open").to_numpy().astype("float64")
    h = t.column("high").to_numpy().astype("float64")
    l = t.column("low").to_numpy().astype("float64")
    c = t.column("close").to_numpy().astype("float64")
    order = np.argsort(ts, kind="stable")
    return {"ts": ts[order], "o": o[order], "h": h[order],
            "l": l[order], "c": c[order]}


def build(m: dict, k: int) -> dict:
    """Exact port of build_timeframes.build() (Phase-2B committed source)."""
    ts_min = m["ts"].astype("datetime64[m]").astype("int64")
    bucket = ts_min // k
    change = np.flatnonzero(np.diff(bucket)) + 1
    starts = np.concatenate(([0], change))
    ends = np.concatenate((change, [len(bucket)]))
    counts = ends - starts

    o = m["o"][starts]
    c = m["c"][ends - 1]
    h = np.maximum.reduceat(m["h"], starts)
    l = np.minimum.reduceat(m["l"], starts)
    bar_min = bucket[starts] * k

    # integrity counters (identical to the Phase-2B builder)
    gap_next = np.zeros(len(ts_min), dtype="int64")
    gap_next[:-1] = ts_min[1:] - ts_min[:-1] - 1
    is_break = (gap_next >= MARKET_BREAK_MIN).astype("int64")
    cgap = np.concatenate(([0], np.cumsum(gap_next)))
    cbrk = np.concatenate(([0], np.cumsum(is_break)))
    internal_missing = cgap[np.maximum(ends - 1, 0)] - cgap[starts]
    internal_breaks = cbrk[np.maximum(ends - 1, 0)] - cbrk[starts]
    contig_next = np.zeros(len(starts), dtype="int8")
    contig_next[1:] = (gap_next[ends[:-1] - 1] == 0).astype("int8")

    return {
        "bar_id": bucket[starts].astype("int64"),
        "t_min": bar_min.astype("int64"),
        "ts": (bar_min * 60).astype("datetime64[s]").astype("datetime64[ns]"),
        "open": o, "high": h, "low": l, "close": c,
        "n_m1": counts.astype("int32"),
        "internal_missing": internal_missing.astype("int32"),
        "internal_breaks": internal_breaks.astype("int16"),
        "contig_next": contig_next,
    }


def write_grid(b: dict, path: str) -> None:
    schema = pa.schema([
        pa.field("bar_id", pa.int64()),
        pa.field("t_min", pa.int64()),
        pa.field("ts", pa.timestamp("ns", tz="UTC")),
        pa.field("open", pa.float64()), pa.field("high", pa.float64()),
        pa.field("low", pa.float64()), pa.field("close", pa.float64()),
        pa.field("n_m1", pa.int32()), pa.field("internal_missing", pa.int32()),
        pa.field("internal_breaks", pa.int16()), pa.field("contig_next", pa.int8()),
    ])
    tbl = pa.table({
        "bar_id": pa.array(b["bar_id"]),
        "t_min": pa.array(b["t_min"]),
        "ts": pa.array(b["ts"], type=pa.timestamp("ns")),
        "open": pa.array(b["open"]), "high": pa.array(b["high"]),
        "low": pa.array(b["low"]), "close": pa.array(b["close"]),
        "n_m1": pa.array(b["n_m1"]), "internal_missing": pa.array(b["internal_missing"]),
        "internal_breaks": pa.array(b["internal_breaks"]),
        "contig_next": pa.array(b["contig_next"]),
    })
    pq.write_table(tbl.cast(schema), path, compression="snappy")


def main() -> None:
    os.makedirs(SCRATCH, exist_ok=True)

    master_sha = sha256_file(MASTER)
    assert master_sha == MASTER_SHA, f"master SHA mismatch: {master_sha}"
    m = load_master(MASTER)
    assert len(m["ts"]) == MASTER_ROWS, f"master rows {len(m['ts'])} != {MASTER_ROWS}"

    # sanity: epoch-even start and sorted input
    tsm = m["ts"].astype("datetime64[m]").astype("int64")
    assert int(tsm[0]) % 2 == 0
    assert np.all(np.diff(tsm) > 0)

    manifest = {
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "master": MASTER, "master_sha256": master_sha,
        "m1_bars": int(len(tsm)),
        "first_ts": str(m["ts"][0]), "last_ts": str(m["ts"][-1]),
        "protocol_source": "research/timeframe_audit/scripts/build_timeframes.py",
        "protocol_source_sha256": "02d4fcdb77a325cce3b8f3b220f7c44b3b326512bf789e8cb1928d4d7a78adcc",
        "alignment": "bar_id = floor(epoch_minutes / k)",
        "timezone": "UTC",
        "aggregation": {"open": "first", "high": "max", "low": "min", "close": "last"},
        "validity": "bar exists iff >= 1 real M1 bar present (no padding, no invented bar)",
        "volume": "excluded (Phase 1 L1)",
        "grid": [],
    }

    for name, k in (("M3", PRIMARY_MIN), ("H1", CONTEXT_MIN)):
        b = build(m, k)
        path = os.path.join(SCRATCH, f"{name.lower()}_grid.parquet")
        write_grid(b, path)
        manifest["grid"].append({
            "timeframe": name, "minutes": k, "bars": int(len(b["bar_id"])),
            "file": path, "sha256": sha256_file(path),
            "first_ts": str(b["ts"][0]), "last_ts": str(b["ts"][-1]),
            "bar_id_first": int(b["bar_id"][0]), "bar_id_last": int(b["bar_id"][-1]),
            "mean_m1_per_bar": round(float(b["n_m1"].mean()), 4),
            "bars_with_internal_data_gap": int(np.sum(b["internal_missing"] > 0)),
            "bars_with_internal_market_break": int(np.sum(b["internal_breaks"] > 0)),
        })
        print(json.dumps(manifest["grid"][-1], indent=2), flush=True)

    with open(os.path.join(SCRATCH, "grid_manifest.json"), "w") as fh:
        json.dump(manifest, fh, indent=2)
    print("grid manifest written")


if __name__ == "__main__":
    main()
