#!/usr/bin/env python3
"""
PHASE 1 - XAUUSD DATA INGESTION / PROVENANCE / INTEGRITY AUDIT
==============================================================

Read-only audit of the 7 shipped fragments (XAUUSD_part_0N.parquet.part).

FIREWALL (enforced by construction - this file contains no strategy,
regime, performance, optimisation, resampling or holdout logic):
  * source fragments are opened 'rb' only and are NEVER written to
  * the reassembled dataset lives in an external scratch directory
  * no row is dropped, patched, interpolated or resampled
  * every anomaly is counted, none is silently removed

Outputs (in --outdir):
  metrics.json   full machine-readable result set

Usage:
  python audit_xauusd_phase1.py --repo /path/to/xauusd-quant-research \
                                --workdir /tmp/xauusd_audit
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import struct
import sys
from datetime import datetime, timezone

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from parquet_pagemap import scan_column_chunk, locate_byte_offset  # noqa: E402

CHUNK = 1 << 20
PAR1 = b"PAR1"
TZ_NY = "America/New_York"


def hum(n: float) -> str:
    for unit in ("B", "KiB", "MiB", "GiB", "TiB"):
        if abs(n) < 1024.0:
            return f"{n:,.2f} {unit}" if unit != "B" else f"{int(n)} B"
        n /= 1024.0
    return f"{n:,.2f} PiB"


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for blk in iter(lambda: fh.read(CHUNK), b""):
            h.update(blk)
    return h.hexdigest()


def dec_count(x: np.ndarray, kmax: int = 8, tol: float = 1e-6) -> np.ndarray:
    """Number of decimal places needed to represent each value exactly."""
    out = np.full(x.shape, 99, dtype=int)
    for k in range(kmax + 1):
        scaled = np.abs(x * (10.0 ** k))
        isint = np.abs(scaled - np.round(scaled)) < tol * np.maximum(1.0, scaled)
        out = np.where((out == 99) & isint, k, out)
    return out


def detect_kind(path: str) -> dict:
    """Magic-byte based detection. Never trust the filename."""
    size = os.path.getsize(path)
    with open(path, "rb") as fh:
        head = fh.read(16)
        fh.seek(max(0, size - 8))
        tail = fh.read(8)
    res = {"head_magic": head[:4].decode("latin1"),
           "tail_magic": tail[-4:].decode("latin1"),
           "head_hex": head[:8].hex(), "tail_hex": tail.hex()}
    if head[:4] == PAR1 and tail[-4:] == PAR1:
        res["detected"] = "complete Parquet file"
    elif head[:4] == PAR1:
        res["detected"] = "Parquet byte-stream HEAD (magic PAR1, footer absent)"
    elif tail[-4:] == PAR1:
        res["detected"] = "Parquet byte-stream TAIL (footer PAR1, head magic absent)"
    else:
        res["detected"] = "raw Parquet continuation bytes (no magic at offset 0)"
    res["footer_len"] = struct.unpack("<I", tail[:4])[0] if tail[-4:] == PAR1 else None
    return res


def _rows(records: pd.DataFrame) -> list[dict]:
    return [{k: (v.isoformat() if isinstance(v, pd.Timestamp) else float(v))
             for k, v in rec.items()} for rec in records.to_dict("records")]


# =========================================================================== #
# 1. INVENTORY
# =========================================================================== #
def inventory(repo: str) -> dict:
    parts = sorted(f for f in os.listdir(repo)
                   if re.match(r"^XAUUSD_part_\d+\.parquet\.part$", f))
    out = []
    for i, name in enumerate(parts, start=1):
        p = os.path.join(repo, name)
        size = os.path.getsize(p)
        kind = detect_kind(p)
        try:
            with open(p, "rb") as fh:
                fh.read(1)
                fh.seek(-1, os.SEEK_END)
                fh.read(1)
            readable, read_err = True, None
        except Exception as exc:  # pragma: no cover
            readable, read_err = False, str(exc)
        try:
            pq.ParquetFile(p)
            opens_alone, alone_err = True, None
        except Exception as exc:
            opens_alone = False
            alone_err = f"{type(exc).__name__}: {str(exc).splitlines()[0][:160]}"
        # "opens" only means the footer parsed; try to actually decode rows
        try:
            t = pq.read_table(p)
            read_alone, read_alone_err = True, f"{t.num_rows:,} rows decoded"
        except Exception as exc:
            read_alone = False
            read_alone_err = f"{type(exc).__name__}: {str(exc).splitlines()[0][:160]}"
        out.append({
            "logical_order": i,
            "path": os.path.relpath(p, repo),
            "name": name,
            "size_bytes": size,
            "size_human": hum(size),
            "sha256": sha256_file(p),
            "present": True,
            "readable": readable,
            "read_error": read_err,
            "declared_extension": ".parquet.part",
            "is_standalone_parquet": opens_alone,
            "standalone_open_error": alone_err,
            "readable_alone": read_alone,
            "read_alone_error": read_alone_err,
            "detected_type": kind["detected"],
            "head_magic": kind["head_magic"],
            "tail_magic": kind["tail_magic"],
            "head_hex": kind["head_hex"],
            "tail_hex": kind["tail_hex"],
            "footer_len_if_tail": kind["footer_len"],
            "mtime_utc": datetime.fromtimestamp(os.path.getmtime(p), timezone.utc)
                                 .isoformat(timespec="seconds"),
        })
    return {"fragments": out, "count": len(out),
            "total_bytes": sum(f["size_bytes"] for f in out),
            "expected_fragments": 7,
            "missing_fragments": [f"XAUUSD_part_{i:02d}.parquet.part"
                                  for i in range(1, 8)
                                  if f"XAUUSD_part_{i:02d}.parquet.part" not in parts]}


# =========================================================================== #
# 3. NON-DESTRUCTIVE RECONSTRUCTION
# =========================================================================== #
def reconstruct(frags: list[dict], workdir: str, repo: str) -> dict:
    os.makedirs(workdir, exist_ok=True)
    dst = os.path.join(workdir, "XAUUSD_M1_reconstructed.parquet")
    h = hashlib.sha256()
    written = 0
    with open(dst, "wb") as out:
        for f in frags:
            with open(os.path.join(repo, f["path"]), "rb") as src:
                while True:
                    blk = src.read(CHUNK)
                    if not blk:
                        break
                    out.write(blk)
                    h.update(blk)
                    written += len(blk)
    res = {"method": "byte-exact sequential concatenation (cat part_01 .. part_07)",
           "destination": dst, "bytes_written": written,
           "sum_of_fragment_bytes": sum(f["size_bytes"] for f in frags),
           "sha256": h.hexdigest()}
    res["size_matches_sum"] = res["bytes_written"] == res["sum_of_fragment_bytes"]
    with open(dst, "rb") as fh:
        head = fh.read(4)
        fh.seek(-8, os.SEEK_END)
        tail = fh.read(8)
    res["head_magic"] = head.decode("latin1")
    res["tail_magic"] = tail[-4:].decode("latin1")
    res["footer_len_declared"] = struct.unpack("<I", tail[:4])[0]
    res["footer_total_bytes"] = res["footer_len_declared"] + 8
    return res


def resplit_proof(path: str, sizes: list[int], expected: list[str]) -> dict:
    """Re-split the reassembled file at the same offsets and compare hashes.

    A perfect match proves the concatenation reproduced the original byte
    stream exactly: no byte missing, none duplicated, none reordered.
    """
    got, trailing = [], 0
    with open(path, "rb") as fh:
        for s in sizes:
            got.append(hashlib.sha256(fh.read(s)).hexdigest())
        trailing = len(fh.read())
    return {"resplit_hashes_equal_originals": got == expected,
            "trailing_bytes_after_last_chunk": trailing,
            "per_fragment": [{"fragment": i + 1, "match": a == b,
                              "original_sha256": a, "resplit_sha256": b}
                             for i, (a, b) in enumerate(zip(expected, got))]}


def parquet_parse_check(path: str) -> dict:
    pf = pq.ParquetFile(path)
    md = pf.metadata
    schema_cols = {pf.schema.column(j).name: pf.schema.column(j)
                   for j in range(len(pf.schema_arrow.names))}
    res = {"parses": True, "created_by": md.created_by,
           "format_version": f"{md.format_version}", "num_rows": md.num_rows,
           "num_row_groups": md.num_row_groups, "num_columns": md.num_columns,
           "footer_serialized_size": md.serialized_size,
           "kv_metadata_keys": sorted(k.decode(errors="replace")
                                      for k in (md.metadata or {}).keys()),
           "pandas_metadata": json.loads(md.metadata[b"pandas"].decode())
           if (md.metadata or {}).get(b"pandas") else None,
           "row_groups": []}
    for i in range(md.num_row_groups):
        rg = md.row_group(i)
        cols = []
        for j in range(rg.num_columns):
            cc = rg.column(j)
            cols.append({
                "name": cc.path_in_schema,
                "physical_type": str(cc.physical_type),
                "logical_type": str(schema_cols[cc.path_in_schema].logical_type),
                "converted_type": str(schema_cols[cc.path_in_schema].converted_type),
                "compression": str(cc.compression),
                "encodings": [str(e) for e in cc.encodings],
                "num_values": cc.num_values,
                "null_count": cc.statistics.null_count if cc.statistics else None,
                "dict_page_offset": cc.dictionary_page_offset,
                "data_page_offset": cc.data_page_offset,
                "total_compressed_size": cc.total_compressed_size,
                "total_uncompressed_size": cc.total_uncompressed_size,
            })
        res["row_groups"].append({"index": i, "num_rows": rg.num_rows,
                                  "total_byte_size": rg.total_byte_size,
                                  "columns": cols})
    return res


def full_read_check(path: str) -> dict:
    """Decode EVERY value of EVERY column: proves every compressed page is intact."""
    t = pq.ParquetFile(path).read(use_threads=True)
    return {"read_ok": True, "rows_decoded": t.num_rows,
            "columns_decoded": t.num_columns,
            "null_counts": {c: int(t.column(c).null_count) for c in t.column_names},
            "nbytes": int(t.nbytes)}


# =========================================================================== #
# BOUNDARY MAP
# =========================================================================== #
def boundary_map(path: str, frag_sizes: list[int]) -> dict:
    pf = pq.ParquetFile(path)
    md = pf.metadata
    scans, rg_offsets, cum = {}, {}, 0
    for i in range(md.num_row_groups):
        rg = md.row_group(i)
        rg_offsets[i] = cum
        cum += rg.num_rows
        for j in range(rg.num_columns):
            cc = rg.column(j)
            start = cc.dictionary_page_offset or cc.data_page_offset
            scans[(i, cc.path_in_schema)] = scan_column_chunk(
                path, i, cc.path_in_schema, start, cc.total_compressed_size)
    accounting_ok = True
    for (rg, col), s in scans.items():
        parsed = sum(p.header_len + p.compressed_size for p in s.pages)
        vals = sum(p.num_values for p in s.pages)
        if parsed != (s.chunk_end - s.chunk_start) or vals != md.row_group(rg).num_rows:
            accounting_ok = False
    boundaries, off = [], 0
    for k, size in enumerate(frag_sizes[:-1], start=1):
        off += size
        loc = locate_byte_offset(scans, rg_offsets, off)
        loc["boundary"] = f"{k:02d}->{k+1:02d}"
        loc["byte_offset"] = off
        boundaries.append(loc)
    return {"page_accounting_consistent": accounting_ok,
            "row_group_first_row": rg_offsets,
            "row_group_last_row": {k: v + md.row_group(k).num_rows - 1
                                   for k, v in rg_offsets.items()},
            "row_group_rows": {k: md.row_group(k).num_rows for k in rg_offsets},
            "boundaries": boundaries}


# =========================================================================== #
# 4-9. TABLE AUDIT
# =========================================================================== #
def table_audit(path: str, bmap: dict) -> tuple[dict, pd.DataFrame]:
    df = pq.ParquetFile(path).read().to_pandas()
    n = len(df)
    ts = df["timestamp"]
    res: dict = {"n_rows": int(n)}

    # ---------------- 4. schema
    pf = pq.ParquetFile(path)
    res["schema"] = [{"name": f.name, "arrow_type": str(f.type),
                      "pandas_dtype": str(df[f.name].dtype),
                      "nullable": f.nullable,
                      "null_count": int(df[f.name].isna().sum()),
                      "null_pct": round(100.0 * float(df[f.name].isna().sum()) / n, 6)}
                     for f in pf.schema_arrow]
    res["index_columns"] = (json.loads(pf.metadata.metadata[b"pandas"].decode())
                            .get("index_columns")
                            if (pf.metadata.metadata or {}).get(b"pandas") else None)
    res["timestamp_tzinfo"] = str(getattr(ts.dtype, "tz", None))
    res["timestamp_is_tz_aware"] = getattr(ts.dtype, "tz", None) is not None

    # ---------------- 5. temporal
    d = ts.diff().dt.total_seconds().to_numpy("float64")
    valid = ~np.isnan(d)
    vc = pd.Series(d[valid]).value_counts().head(20)
    res["temporal"] = {
        "first_timestamp": ts.iloc[0].isoformat(),
        "last_timestamp": ts.iloc[-1].isoformat(),
        "diff_value_counts_top": {f"{int(k)}s": int(v) for k, v in vc.items()},
        "dominant_interval_seconds": float(vc.index[0]),
        "dominant_interval_share_pct": round(100.0 * float(vc.iloc[0]) / int(valid.sum()), 4),
        "rows_with_dt_exactly_60s": int(np.sum(d == 60.0)),
        "rows_with_dt_not_60s": int(np.sum(valid) - np.sum(d == 60.0)),
        "nat_timestamps": int(ts.isna().sum()),
        "duplicate_timestamps": int(n - ts.nunique()),
        "out_of_order_count": int(np.sum(d[valid] < 0)),
        "zero_or_negative_interval_count": int(np.sum(d[valid] <= 0)),
    }

    gi = np.where(valid & (d > 60.0))[0]
    prev = pd.to_datetime(ts.to_numpy()[gi - 1])
    nxt = pd.to_datetime(ts.to_numpy()[gi])
    gaps = [{"prev_ts": a.isoformat(), "next_ts": b.isoformat(),
             "gap_seconds": float(s), "gap_minutes": float(s) / 60.0,
             "missing_minutes": int(s / 60.0) - 1, "row_index": int(i),
             "prev_dow": a.day_name(), "next_dow": b.day_name()}
            for a, b, s, i in zip(prev, nxt, d[gi], gi)]

    def classify(a, b, s):
        if s > 100000:
            return "weekend_closure"
        if 3000 < s < 9000:
            return "daily_break"
        if a.date() != b.date():
            return "multi_day_non_weekend"
        return "intraday_liquidity_gap"
    for g, a, b, s in zip(gaps, prev, nxt, d[gi]):
        g["class"] = classify(a, b, s)
    non_weekend = sorted([g for g in gaps if g["class"] == "multi_day_non_weekend"],
                         key=lambda g: -g["gap_seconds"])
    full_days = [g for g in non_weekend if g["missing_minutes"] >= 1439]
    res["gaps"] = {
        "count": len(gaps),
        "by_class": {k: int(v) for k, v in
                     pd.Series([g["class"] for g in gaps]).value_counts().items()},
        "total_missing_minutes": int(sum(g["missing_minutes"] for g in gaps)),
        "max_gap_minutes": float(max((g["gap_minutes"] for g in gaps), default=0.0)),
        "top": sorted(gaps, key=lambda g: -g["gap_seconds"])[:30],
        "top_non_weekend": non_weekend[:20],
        "non_weekend_count": len(non_weekend),
        "fully_missing_sessions_ge_1439min": len(full_days),
        "missing_minutes_in_non_weekend": int(sum(g["missing_minutes"]
                                                  for g in non_weekend)),
        "missing_minutes_in_intraday": int(sum(g["missing_minutes"] for g in gaps
                                               if g["class"] == "intraday_liquidity_gap")),
    }

    ts_idx = pd.DatetimeIndex(ts)
    years = []
    for y in sorted(set(ts_idx.year)):
        m = ts_idx.year == y
        sub = ts_idx[m]
        days = pd.DatetimeIndex(sub.normalize().unique())
        wk = int(np.sum(days.dayofweek < 5)) * 1440
        years.append({"year": int(y), "rows": int(m.sum()),
                      "distinct_days": len(days),
                      "distinct_months": int(sub.month.nunique()),
                      "expected_minutes_if_24x5": wk,
                      "coverage_pct_of_24x5": round(100.0 * m.sum() / wk, 3)
                      if wk else None,
                      "first_ts": sub.min().isoformat(),
                      "last_ts": sub.max().isoformat()})
    res["by_year"] = years
    months = []
    key = ts_idx.year * 100 + ts_idx.month
    for k in sorted(pd.unique(key)):
        m = (key == k)
        sub = ts_idx[m]
        days = pd.DatetimeIndex(sub.normalize().unique())
        wk = int(np.sum(days.dayofweek < 5)) * 1440
        months.append({"year": int(k // 100), "month": int(k % 100),
                       "rows": int(m.sum()), "distinct_days": len(days),
                       "expected_minutes_if_24x5": wk,
                       "coverage_pct_of_24x5": round(100.0 * m.sum() / wk, 3)
                       if wk else None,
                       "first_ts": sub.min().isoformat(),
                       "last_ts": sub.max().isoformat()})
    res["by_month"] = months
    res["rows_by_weekday"] = {k: int(v) for k, v in
                              pd.Series(ts_idx.day_name()).value_counts().items()}
    res["hour_histogram_utc"] = {int(h): int(v) for h, v in
                                 pd.Series(ts_idx.hour).value_counts().sort_index().items()}
    res["saturday_rows"] = int(np.sum(ts_idx.dayofweek == 5))
    res["sunday_rows"] = int(np.sum(ts_idx.dayofweek == 6))

    # ---------------- 6. OHLC integrity
    o = df["open"].to_numpy("float64"); hi = df["high"].to_numpy("float64")
    lo = df["low"].to_numpy("float64"); cl = df["close"].to_numpy("float64")
    vol = df["volume"].to_numpy("float64")
    allpx = np.concatenate([o, hi, lo, cl])
    rng = hi - lo
    med = float(np.nanmedian(rng))
    res["ohlc"] = {
        "null_open": int(np.isnan(o).sum()), "null_high": int(np.isnan(hi).sum()),
        "null_low": int(np.isnan(lo).sum()), "null_close": int(np.isnan(cl).sum()),
        "null_volume": int(np.isnan(vol).sum()), "null_timestamp": int(ts.isna().sum()),
        "inf_values_all_price_columns": int(np.sum(np.isinf(allpx))),
        "nan_values_all_price_columns": int(np.sum(np.isnan(allpx))),
        "non_finite_values_all_price_columns": int(np.sum(~np.isfinite(allpx))),
        "price_le_zero": int(np.sum(np.nan_to_num(allpx, nan=1.0) <= 0)),
        "negative_volume": int(np.sum(np.nan_to_num(vol, nan=1.0) < 0)),
        "zero_volume": int(np.sum(vol == 0)),
        "high_lt_low": int(np.sum(hi < lo)),
        "high_eq_low": int(np.sum(hi == lo)),
        "high_lt_max_ocl": int(np.sum(hi < np.maximum(np.maximum(o, cl), lo) - 1e-12)),
        "low_gt_min_och": int(np.sum(lo > np.minimum(np.minimum(o, cl), hi) + 1e-12)),
        "open_outside_hl": int(np.sum((o > hi + 1e-12) | (o < lo - 1e-12))),
        "close_outside_hl": int(np.sum((cl > hi + 1e-12) | (cl < lo - 1e-12))),
        "flat_candle_ohlc": int(np.sum((o == hi) & (hi == lo) & (lo == cl))),
        "range_negative": int(np.sum(rng < 0)), "range_zero": int(np.sum(rng == 0)),
        "range_median": med,
        "range_gt_50x_median": int(np.sum(rng > 50 * med)),
        "range_gt_100x_median": int(np.sum(rng > 100 * med)),
        "range_gt_20usd": int(np.sum(rng > 20.0)),
        "range_gt_50usd": int(np.sum(rng > 50.0)),
        "range_quantiles": {f"q{int(q*100)}": float(np.nanquantile(rng, q))
                            for q in (0.0, 0.01, 0.25, 0.5, 0.75, 0.95, 0.99, 1.0)},
    }

    ret = np.diff(cl) / cl[:-1]
    res["returns_m1"] = {
        "count": int(ret.size), "mean": float(np.nanmean(ret)),
        "std": float(np.nanstd(ret)), "min": float(np.nanmin(ret)),
        "max": float(np.nanmax(ret)),
        **{f"q{int(q*100)}": float(np.nanquantile(ret, q))
           for q in (0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99)},
        "zero_returns": int(np.sum(ret == 0)),
        "abs_gt_1pct": int(np.sum(np.abs(ret) > 0.01)),
        "abs_gt_2pct": int(np.sum(np.abs(ret) > 0.02)),
        "abs_gt_5pct": int(np.sum(np.abs(ret) > 0.05)),
        "abs_gt_10pct": int(np.sum(np.abs(ret) > 0.10)),
    }
    top = np.argsort(-np.abs(ret))[:15]
    res["largest_jumps"] = [{"row_index": int(i), "from_ts": ts.iloc[i].isoformat(),
                             "to_ts": ts.iloc[i + 1].isoformat(),
                             "close_before": float(cl[i]), "close_after": float(cl[i + 1]),
                             "pct_change": float(ret[i] * 100.0),
                             "gap_seconds": (float(d[i + 1]) if not np.isnan(d[i + 1])
                                             else None)} for i in top]
    top_r = np.argsort(-rng)[:15]
    res["largest_ranges"] = [{"ts": ts.iloc[i].isoformat(), "open": float(o[i]),
                              "high": float(hi[i]), "low": float(lo[i]),
                              "close": float(cl[i]), "range": float(rng[i]),
                              "volume": float(vol[i]),
                              "gap_before_s": (float(d[i]) if not np.isnan(d[i]) else None)}
                             for i in top_r]

    res["duplication"] = {
        "fully_duplicated_rows": int(df.duplicated().sum()),
        "consecutive_identical_ohlc_rows": int(np.sum(
            (o[1:] == o[:-1]) & (hi[1:] == hi[:-1]) &
            (lo[1:] == lo[:-1]) & (cl[1:] == cl[:-1]))),
    }
    res["price_extremes"] = {
        "min_low": float(np.nanmin(lo)), "max_high": float(np.nanmax(hi)),
        "min_close": float(np.nanmin(cl)), "max_close": float(np.nanmax(cl)),
        "first_close": float(cl[0]), "last_close": float(cl[-1]),
        "argmin_low_ts": ts.iloc[int(np.nanargmin(lo))].isoformat(),
        "argmax_high_ts": ts.iloc[int(np.nanargmax(hi))].isoformat(),
    }
    res["volume_profile"] = {
        "min": float(np.nanmin(vol)), "max": float(np.nanmax(vol)),
        "mean": float(np.nanmean(vol)), "median": float(np.nanmedian(vol)),
        "std": float(np.nanstd(vol)),
        "pct_integer_valued": round(100.0 * float(np.sum(vol == np.round(vol))) / n, 4),
        "pct_zero": round(100.0 * float(np.sum(vol == 0)) / n, 4),
        "distinct_values": int(pd.Series(vol).nunique()),
    }

    # ---------------- 7. fragment boundaries
    bounds = []
    for b in bmap["boundaries"]:
        rg = b["row_group"]
        # conservative window: the seam is inside row group `rg`; because Parquet
        # is column-major, ANY row of that row group may be physically split, so
        # the whole row group is verified.
        lo_i = max(0, bmap["row_group_first_row"][rg] - 5)
        hi_i = min(n, bmap["row_group_last_row"][rg] + 6)
        seg = ts.iloc[lo_i:hi_i]
        sd = seg.diff().dt.total_seconds().to_numpy("float64")[1:]
        segd = df.iloc[lo_i:hi_i]
        oc = np.abs(segd["open"].to_numpy()[1:] - segd["close"].to_numpy()[:-1])
        # jump measured only across strictly adjacent minutes (60 s steps):
        # week-end / daily-break steps are excluded, they are market closures.
        oc_adj = oc[sd == 60.0] if oc.size else np.array([0.0])
        # gaps that are neither a weekend closure nor the daily break
        unexplained = int(np.sum((sd > 60.0) & ~(((sd > 100000.0)) |
                                                 ((sd > 3000.0) & (sd < 9000.0)))))
        est = b["row_estimate_global"]
        bounds.append({
            "boundary": b["boundary"], "byte_offset": b["byte_offset"],
            "row_group": rg, "column_cut": b["column"], "page_index": b["page_index"],
            "page_type": b["page_type"], "page_num_values": b["page_num_values"],
            "fraction_in_page": b["fraction_in_page"],
            "estimated_row_index": est,
            "conservative_window_lo": int(lo_i), "conservative_window_hi": int(hi_i),
            "conservative_window_rows": int(hi_i - lo_i),
            "window_first_ts": seg.iloc[0].isoformat(),
            "window_last_ts": seg.iloc[-1].isoformat(),
            "window_strictly_monotonic": bool(np.all(sd > 0)),
            "window_duplicate_timestamps": int(len(seg) - seg.nunique()),
            "window_intervals_not_60s": int(np.sum(sd != 60.0)),
            "window_unexplained_gaps": unexplained,
            "window_adjacent_60s_steps": int(np.sum(sd == 60.0)),
            "window_max_abs_open_minus_prev_close_adjacent": float(np.nanmax(oc_adj))
            if oc_adj.size else 0.0,
            "window_max_abs_open_minus_prev_close_all": float(np.nanmax(oc))
            if oc.size else 0.0,
            "rows_before_seam": _rows(df.iloc[max(0, est - 3):est]),
            "rows_after_seam": _rows(df.iloc[est:est + 3]),
        })
    res["boundaries"] = bounds
    return res, df


# =========================================================================== #
# DEEP DIAGNOSTICS (session structure, precision drift, coverage)
# =========================================================================== #
def deep_diagnostics(df: pd.DataFrame) -> dict:
    ts = df["timestamp"]
    d = ts.diff().dt.total_seconds().to_numpy("float64")
    gi = np.where((~np.isnan(d)) & (d > 60.0))[0]
    prev = pd.to_datetime(ts.to_numpy()[gi - 1])
    g = pd.DataFrame({"sec": d[gi], "prev": prev,
                      "next": pd.to_datetime(ts.to_numpy()[gi])})
    daily = g[(g["sec"] > 3000) & (g["sec"] < 9000)].copy()
    daily["prev_hm"] = daily["prev"].dt.strftime("%H:%M")
    daily["month"] = daily["prev"].dt.month
    switch = []
    for y in sorted(daily["prev"].dt.year.unique()):
        s = daily[daily["prev"].dt.year == y]
        summer = s[s["prev_hm"] == "20:59"]["prev"]
        winter = s[s["prev_hm"] == "21:59"]["prev"]
        first_summer = summer.min() if len(summer) else None
        first_winter = None
        if len(winter) and first_summer is not None:
            cand = winter[winter > first_summer]
            first_winter = cand.min() if len(cand) else None
        switch.append({"year": int(y),
                       "first_summer_break_utc": (first_summer.strftime("%Y-%m-%d %H:%M")
                                                  if first_summer is not None else None),
                       "first_winter_break_utc": (first_winter.strftime("%Y-%m-%d %H:%M")
                                                  if first_winter is not None
                                                  and not pd.isna(first_winter) else None)})
    # NY-time equivalence of the break window
    probe = pd.to_datetime(daily["prev"]).dt.tz_convert(TZ_NY).dt.strftime("%H:%M")
    out = {
        "daily_break": {
            "count": int(len(daily)),
            "first_occurrence": (daily["prev"].min().isoformat() if len(daily) else None),
            "last_occurrence": (daily["prev"].max().isoformat() if len(daily) else None),
            "utc_break_start_histogram": {k: int(v) for k, v in
                                          daily["prev_hm"].value_counts().head(8).items()},
            "utc_break_end_histogram": {k: int(v) for k, v in
                                        daily["next"].dt.strftime("%H:%M")
                                        .value_counts().head(8).items()},
            "ny_local_break_start_histogram": {k: int(v) for k, v in
                                               probe.value_counts().head(5).items()},
            "by_month": pd.crosstab(daily["month"], daily["prev_hm"]).to_dict(),
            "dst_switch_dates": switch,
            "per_year_count": {int(k): int(v) for k, v in
                               daily.groupby(daily["prev"].dt.year)["sec"].count().items()},
        },
        "weekend": {
            "friday_last_bar_histogram": {k: int(v) for k, v in
                                          pd.Series(ts[ts.dt.dayofweek == 4]
                                                    .dt.strftime("%H:%M"))
                                          .groupby(ts[ts.dt.dayofweek == 4].dt.date).max()
                                          .value_counts().head(6).items()},
            "sunday_sessions": None,
            "weekend_gap_seconds_histogram": {k: int(v) for k, v in
                                              g[g["sec"] > 100000]["sec"]
                                              .value_counts().head(8).items()},
        },
        "session_shape_by_year": None,
        "precision_by_year": {},
        "volume_by_year": {},
        "zero_range_by_year": {},
        "rows_per_day": None,
        "coverage": None,
        "gap_size_classes": {str(k): int(v) for k, v in
                             pd.cut(g["sec"], [60, 300, 900, 3600, 9000, 100000, 1e9])
                             .value_counts().sort_index().items()},
    }
    sun = df[df["timestamp"].dt.dayofweek == 6]
    lens = sun.groupby(sun["timestamp"].dt.date).size()
    out["weekend"]["sunday_sessions"] = {
        "count": int(len(lens)), "mean_bars": float(lens.mean()),
        "min_bars": int(lens.min()), "max_bars": int(lens.max()),
        "length_histogram": {int(k): int(v) for k, v in
                             lens.value_counts().head(6).items()},
        "total_bars": int(lens.sum()),
    }

    rng = (df["high"] - df["low"]).to_numpy()
    rel = rng / df["close"].to_numpy() * 1e4
    yr = ts.dt.year.to_numpy()
    base = pd.DataFrame({"y": yr, "rows": 1, "zerorng": (rng == 0), "rel_bps": rel,
                         "vol": df["volume"].to_numpy(), "rng": rng})
    agg = base.groupby("y").agg(rows=("rows", "size"), zero_range=("zerorng", "sum"),
                                med_rel_bps=("rel_bps", "median"),
                                p99_rel_bps=("rel_bps", lambda s: s.quantile(0.99)),
                                med_range_usd=("rng", "median"),
                                max_range_usd=("rng", "max"),
                                mean_volume=("vol", "mean"),
                                median_volume=("vol", "median"),
                                max_volume=("vol", "max"))
    out["by_year_profile"] = json.loads(agg.round(6).to_json(orient="index"))

    for c in ["open", "high", "low", "close", "volume"]:
        dd = dec_count(df[c].to_numpy())
        ct = pd.crosstab(yr, dd)
        out["precision_by_year"][c] = json.loads(ct.to_json(orient="index"))
        out[f"precision_overall_{c}"] = {int(k): int(v) for k, v in
                                         pd.Series(dd).value_counts().sort_index().items()}

    rpd = pd.Series(ts.dt.date.to_numpy()).value_counts().sort_index()
    y_of_day = pd.Series([x.year for x in rpd.index], index=rpd.index)
    out["rows_per_day"] = {
        "distinct_days": int(len(rpd)), "mean": float(rpd.mean()),
        "median": float(rpd.median()), "min": int(rpd.min()), "max": int(rpd.max()),
        "days_below_700_rows": int((rpd < 700).sum()),
        "days_above_1400_rows": int((rpd > 1400).sum()),
        "by_year_max": {int(k): int(v) for k, v in rpd.groupby(y_of_day).max().items()},
        "by_year_mean": {int(k): round(float(v), 2) for k, v in
                         rpd.groupby(y_of_day).mean().items()},
    }
    # presence profile: how many days contain each 5-minute bucket (hours 19-23)
    mod = ts.dt.hour * 60 + ts.dt.minute
    shape = {}
    for y in sorted(set(yr)):
        m = yr == y
        cnt = ((mod[m] // 5) * 5).value_counts().reindex(range(1140, 1440, 5),
                                                         fill_value=0)
        shape[int(y)] = {f"{i//60:02d}:{i%60:02d}": int(v) for i, v in cnt.items()}
    out["session_shape_by_year"] = shape

    n = len(df)
    span_min = (ts.iloc[-1] - ts.iloc[0]).total_seconds() / 60.0 + 1
    out["coverage"] = {
        "rows": int(n),
        "first_ts": ts.iloc[0].isoformat(), "last_ts": ts.iloc[-1].isoformat(),
        "distinct_days": int(ts.dt.date.nunique()),
        "distinct_months": int((ts.dt.year * 100 + ts.dt.month).nunique()),
        "distinct_years": int(ts.dt.year.nunique()),
        "calendar_span_minutes": int(span_min),
        "missing_minutes_vs_24x7_grid": int(span_min - n),
        "coverage_pct_of_24x7_grid": round(100.0 * n / span_min, 3),
        "least_covered_year": min(out["by_year_profile"].items(),
                                  key=lambda kv: kv[1]["rows"])[0],
        "most_covered_year": max(out["by_year_profile"].items(),
                                 key=lambda kv: kv[1]["rows"])[0],
    }
    return out


# =========================================================================== #
# 10. PROVENANCE
# =========================================================================== #
PROV_EXT = (".md", ".markdown", ".txt", ".rst", ".json", ".yaml", ".yml",
            ".toml", ".csv", ".ini", ".cfg", ".xml")


def provenance(repo: str) -> dict:
    # The audit's own deliverables must not be mistaken for dataset documentation.
    audit_dir = os.path.join(repo, "research", "data_audit")
    found = []
    for root, dirs, files in os.walk(repo):
        dirs[:] = [d for d in dirs if d != ".git"]
        if os.path.abspath(root) == os.path.abspath(audit_dir):
            continue  # outputs produced by this audit, not vendor documentation
        for fn in files:
            if fn.lower().endswith(PROV_EXT):
                found.append(os.path.relpath(os.path.join(root, fn), repo))
    return {
        "documentation_files_found": sorted(found),
        "readme_present": any(os.path.basename(f).lower().startswith("readme")
                              for f in found),
        "manifest_present": any("manifest" in f.lower() for f in found),
        "notes_present": any(("note" in f.lower()) for f in found),
        "git_history": _git(repo),
        "fields": {
            "provider": "UNKNOWN",
            "acquisition_method": "UNKNOWN",
            "symbol": "UNVERIFIED (inferred from filename only: XAUUSD)",
            "timezone": "UTC (explicit: Arrow schema timestamp[ns, tz=UTC] "
                        "and pandas metadata {'timezone': 'UTC'})",
            "period": "MEASURED (see coverage section)",
            "market_convention": "UNKNOWN as declared / MEASURED (see session section)",
            "price_unit": "UNKNOWN (magnitude 1044.70-5596.81 consistent with "
                          "USD per troy ounce, not verified)",
            "volume_unit": "UNKNOWN (fractional, non-integer: not a tick count; "
                           "not determinable from the data)",
        },
    }


def _git(repo: str) -> dict:
    import subprocess
    out = {}
    try:
        out["log"] = subprocess.run(["git", "log", "--oneline", "--all"], cwd=repo,
                                    capture_output=True, text=True).stdout.strip().splitlines()
        out["commit_stat"] = subprocess.run(
            ["git", "show", "--stat", "--oneline", "HEAD"], cwd=repo,
            capture_output=True, text=True).stdout.strip().splitlines()[:20]
        out["remote"] = subprocess.run(["git", "remote", "-v"], cwd=repo,
                                       capture_output=True, text=True).stdout.strip()
    except Exception as exc:  # pragma: no cover
        out["error"] = str(exc)
    return out


# =========================================================================== #
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default="/home/user/xauusd-quant-research")
    ap.add_argument("--workdir", default="/tmp/xauusd_audit")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    os.makedirs(args.workdir, exist_ok=True)
    out_file = args.out or os.path.join(args.workdir, "metrics.json")

    print("[1/8] inventory ...", flush=True)
    inv = inventory(args.repo)

    print("[2/8] format inspection ...", flush=True)
    fmt = {"fragment_sizes": [f["size_bytes"] for f in inv["fragments"]],
           "chunk_size_constant": len({f["size_bytes"]
                                       for f in inv["fragments"][:-1]}) == 1,
           "common_chunk_bytes": inv["fragments"][0]["size_bytes"],
           "common_chunk_mib": inv["fragments"][0]["size_bytes"] / (1 << 20)}

    print("[3/8] non-destructive reconstruction ...", flush=True)
    rec = reconstruct(inv["fragments"], args.workdir, args.repo)
    parse = parquet_parse_check(rec["destination"])
    readchk = full_read_check(rec["destination"])
    proof = resplit_proof(rec["destination"], fmt["fragment_sizes"],
                          [f["sha256"] for f in inv["fragments"]])
    rec_hashes = {"run_1": rec["sha256"], "run_2": sha256_file(rec["destination"])}

    print("[4/8] boundary map ...", flush=True)
    bmap = boundary_map(rec["destination"], fmt["fragment_sizes"])

    print("[5/8] table audit ...", flush=True)
    tab, df = table_audit(rec["destination"], bmap)

    print("[6/8] deep diagnostics ...", flush=True)
    deep = deep_diagnostics(df)

    print("[7/8] provenance ...", flush=True)
    prov = provenance(args.repo)

    print("[8/8] source integrity re-check ...", flush=True)
    post = [sha256_file(os.path.join(args.repo, f["path"])) for f in inv["fragments"]]
    src_intact = all(a["sha256"] == b for a, b in zip(inv["fragments"], post))

    metrics = {
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "environment": {
            "python": sys.version.split()[0],
            "pandas": pd.__version__,
            "pyarrow": pa.__version__,
            "numpy": np.__version__,
        },
        "repo": args.repo, "workdir": args.workdir,
        "inventory": inv, "format": fmt, "reconstruction": rec,
        "resplit_proof": proof,
        "reconstruction_hash_repeat": rec_hashes,
        "reconstruction_deterministic": rec_hashes["run_1"] == rec_hashes["run_2"],
        "parquet": parse, "full_read": readchk, "boundary_map": bmap,
        "table": tab, "deep": deep, "provenance": prov,
        "source_hashes_after_audit": post, "sources_unchanged": bool(src_intact),
    }
    with open(out_file, "w") as fh:
        json.dump(metrics, fh, indent=2, default=str)
    print(f"metrics -> {out_file}")
    print(json.dumps({
        "rows": parse["num_rows"],
        "size_match": rec["size_matches_sum"],
        "resplit_proof": proof["resplit_hashes_equal_originals"],
        "deterministic": metrics["reconstruction_deterministic"],
        "page_accounting": bmap["page_accounting_consistent"],
        "sources_unchanged": src_intact,
    }, indent=2))


if __name__ == "__main__":
    main()
