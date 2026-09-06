#!/usr/bin/env python3
"""
PHASE 2 - deterministic construction of the timeframe grid from the M1 master.

RULES (frozen in Phase 1, enforced here):
  L1  volume is NEVER loaded, never used, never derived  -> not even read
  L2  no gap filling: a bar aggregates ONLY the M1 bars that exist
  L3  no price homogenisation: source OHLC are copied verbatim
  L5  2026 is built but flagged partial (never a selection driver)
  L7  source fragments are read-only; the master is read-only

CONSTRUCTION CONTRACT
  origin      : 1970-01-01 00:00:00 UTC (unix epoch)
  alignment   : bar id = floor(epoch_minutes / k), k = bar length in minutes
  timezone    : UTC (the master timestamps are tz-aware UTC)
  open        : first  open  of the window
  high        : max    high  of the window
  low         : min    low   of the window
  close       : last   close of the window
  validity    : a bar exists if and only if >= 1 real M1 bar is present.
                No bar is invented, no window is padded, no OHLC is modified.

Each aggregated bar also carries integrity counters so that a bar spanning a
market closure or a missing minute can never be silently mistaken for a
complete bar:
  n_m1                   number of real M1 bars aggregated
  internal_missing       minutes missing strictly INSIDE the bar
                         (between its first and its last M1 bar)
  internal_breaks        market closures strictly INSIDE the bar
                         (gaps >= 50 min: daily rollover or weekend)
  contig_next            1 if the step previous bar -> this bar contains no
                         missing minute (used to build clean return series)

Usage:
  python build_timeframes.py --master /tmp/xauusd_audit/XAUUSD_M1_reconstructed.parquet \
                             --outdir /tmp/xauusd_audit/timeframes
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from datetime import datetime, timezone

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

GRID = [("M1", 1), ("M2", 2), ("M3", 3), ("M4", 4), ("M5", 5), ("M10", 10),
        ("M15", 15), ("M20", 20), ("M30", 30), ("H1", 60), ("H2", 120),
        ("H4", 240)]

MARKET_BREAK_MIN = 50      # >= 50 min gap = daily rollover or weekend closure
CHUNK = 1 << 20


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for blk in iter(lambda: fh.read(CHUNK), b""):
            h.update(blk)
    return h.hexdigest()


def load_master(path: str) -> dict:
    """Load ONLY timestamp/OHLC. The volume column is deliberately not read."""
    t = pq.read_table(path, columns=["timestamp", "open", "high", "low", "close"])
    ts = t.column("timestamp").to_numpy(zero_copy_only=False)
    o = t.column("open").to_numpy().astype("float64")
    h = t.column("high").to_numpy().astype("float64")
    l = t.column("low").to_numpy().astype("float64")
    c = t.column("close").to_numpy().astype("float64")
    order = np.argsort(ts, kind="stable")
    return {"ts": ts[order], "o": o[order], "h": h[order],
            "l": l[order], "c": c[order]}


def build(m: dict, k: int):
    ts_min = m["ts"].astype("datetime64[m]").astype("int64")
    bucket = ts_min // k
    # boundaries of each bucket (input is sorted by timestamp)
    change = np.flatnonzero(np.diff(bucket)) + 1
    starts = np.concatenate(([0], change))
    ends = np.concatenate((change, [len(bucket)]))
    counts = ends - starts

    o = m["o"][starts]
    c = m["c"][ends - 1]
    h = np.maximum.reduceat(m["h"], starts)
    l = np.minimum.reduceat(m["l"], starts)
    bar_min = bucket[starts] * k

    # --- integrity counters -------------------------------------------------
    gap_next = np.zeros(len(ts_min), dtype="int64")          # missing minutes after i
    gap_next[:-1] = ts_min[1:] - ts_min[:-1] - 1
    is_break = (gap_next >= MARKET_BREAK_MIN).astype("int64")
    cgap = np.concatenate(([0], np.cumsum(gap_next)))        # cgap[i] = sum before i
    cbrk = np.concatenate(([0], np.cumsum(is_break)))
    # minutes missing strictly inside bar [s, e): gaps from s .. e-2
    internal_missing = cgap[np.maximum(ends - 1, 0)] - cgap[starts]
    internal_breaks = cbrk[np.maximum(ends - 1, 0)] - cbrk[starts]
    # contiguity of the step previous bar -> this bar
    contig_next = np.zeros(len(starts), dtype="int8")
    contig_next[1:] = (gap_next[ends[:-1] - 1] == 0).astype("int8")

    return {
        "ts": (bar_min * 60).astype("datetime64[s]").astype("datetime64[ns]"),
        "open": o, "high": h, "low": l, "close": c,
        "n_m1": counts.astype("int32"),
        "internal_missing": internal_missing.astype("int32"),
        "internal_breaks": internal_breaks.astype("int16"),
        "contig_next": contig_next,
        "start_idx": starts.astype("int64"),
        "end_idx": ends.astype("int64"),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--master",
                    default="/tmp/xauusd_audit/XAUUSD_M1_reconstructed.parquet")
    ap.add_argument("--outdir", default="/tmp/xauusd_audit/timeframes")
    args = ap.parse_args()
    os.makedirs(args.outdir, exist_ok=True)

    master_sha = sha256_file(args.master)
    print(f"master sha256: {master_sha}", flush=True)
    m = load_master(args.master)
    n_m1 = len(m["ts"])
    print(f"M1 bars loaded: {n_m1:,} (volume column NOT loaded - L1)", flush=True)

    manifest = {
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "master": args.master,
        "master_sha256": master_sha,
        "m1_bars": int(n_m1),
        "first_ts": str(m["ts"][0]),
        "last_ts": str(m["ts"][-1]),
        "origin": "1970-01-01T00:00:00Z (unix epoch)",
        "alignment": "bar_id = floor(epoch_minutes / k)",
        "timezone": "UTC",
        "aggregation": {"open": "first", "high": "max", "low": "min",
                        "close": "last"},
        "gap_policy": "none - no window is padded, no M1 bar is invented",
        "volume": "excluded (Phase 1 limitation L1)",
        "market_break_threshold_minutes": MARKET_BREAK_MIN,
        "grid": [],
    }

    for name, k in GRID:
        b = build(m, k)
        path = os.path.join(args.outdir, f"XAUUSD_{name}.parquet")
        tbl = pa.table({
            "ts": pa.array(b["ts"], type=pa.timestamp("ns")),
            "open": pa.array(b["open"]),
            "high": pa.array(b["high"]),
            "low": pa.array(b["low"]),
            "close": pa.array(b["close"]),
            "n_m1": pa.array(b["n_m1"]),
            "internal_missing": pa.array(b["internal_missing"]),
            "internal_breaks": pa.array(b["internal_breaks"]),
            "contig_next": pa.array(b["contig_next"]),
        })
        # tz-aware UTC schema, identical convention to the master
        schema = pa.schema([
            pa.field("ts", pa.timestamp("ns", tz="UTC")),
            pa.field("open", pa.float64()), pa.field("high", pa.float64()),
            pa.field("low", pa.float64()), pa.field("close", pa.float64()),
            pa.field("n_m1", pa.int32()), pa.field("internal_missing", pa.int32()),
            pa.field("internal_breaks", pa.int16()),
            pa.field("contig_next", pa.int8()),
        ])
        pq.write_table(tbl.cast(schema), path, compression="snappy")
        rec = {
            "timeframe": name, "minutes": k, "bars": int(len(b["ts"])),
            "file": path,
            "sha256": sha256_file(path),
            "mean_m1_per_bar": round(float(b["n_m1"].mean()), 4),
            "bars_with_internal_data_gap": int(np.sum(b["internal_missing"] > 0)),
            "bars_with_internal_market_break": int(np.sum(b["internal_breaks"] > 0)),
            "contiguous_steps": int(np.sum(b["contig_next"][1:] == 1)),
            "first_ts": str(b["ts"][0]), "last_ts": str(b["ts"][-1]),
        }
        manifest["grid"].append(rec)
        print(f"  {name:4s} k={k:4d}  bars={rec['bars']:>9,}  "
              f"mean M1/bar={rec['mean_m1_per_bar']:7.3f}  "
              f"gaps={rec['bars_with_internal_data_gap']:>7,}  "
              f"breaks={rec['bars_with_internal_market_break']:>7,}", flush=True)

    with open(os.path.join(args.outdir, "manifest.json"), "w") as fh:
        json.dump(manifest, fh, indent=2)
    print("manifest written")


if __name__ == "__main__":
    main()
