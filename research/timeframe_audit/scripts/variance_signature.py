#!/usr/bin/env python3
"""
Variance-vs-sampling-frequency signature, computed on CONTIGUOUS steps only.

Why a separate module: the generic per-timeframe variance in analyze_timeframes.py
is the standard deviation of log returns between *consecutive rows*, and a
consecutive pair may straddle a missing-data gap (weekend, daily break, outage).
A gap-spanning return carries minutes of price movement that are not attributed
to any bar, which inflates the variance of the fine granularities far more than
the coarse ones (a gap is ~0.27% of M1 steps but ~16% of H4 bars).  A variance
ratio built on those returns is therefore biased and cannot be read as a
microstructure signature.

This module recomputes, per timeframe:
  * the standard deviation of log returns over contiguous steps only
    (bar_id[i+1] == bar_id[i] + 1  AND  no missing M1 minute inside either bar)
  * the variance ratio  VR(k) = var_k / (k * var_1)  on the same clean basis
  * the same after temporarily excluding |return| > 5 sigma (sensitivity, NOT deletion)
and writes variance_signature.json.

INFERENCE / PROXY: this is a statistical signature computed from OHLC bars.
It is NOT an order-book measurement; no bid/ask, no tick, no microstructure
observation exists in this dataset.

Usage:  python variance_signature.py --tfdir /tmp/xauusd_audit/timeframes
"""
from __future__ import annotations

import argparse
import json

import numpy as np
import pyarrow.parquet as pq

GRID = ["M1", "M2", "M3", "M4", "M5", "M10", "M15", "M20", "M30", "H1", "H2", "H4"]
K = {"M1": 1, "M2": 2, "M3": 3, "M4": 4, "M5": 5, "M10": 10, "M15": 15,
     "M20": 20, "M30": 30, "H1": 60, "H2": 120, "H4": 240}


def contiguous_returns(path, tf_name):
    tab = pq.read_table(path, columns=["ts", "close", "internal_missing"])
    close = tab.column("close").to_numpy().astype("float64")
    miss = tab.column("internal_missing").to_numpy().astype("int64")
    ts_ns = tab.column("ts").to_numpy().astype("int64")
    # bar_id recomputed from the timestamp, never read from a stored column:
    # bar_id = floor(epoch_minutes / k), epoch-aligned UTC (see build_timeframes.py)
    bid = ts_ns // (K[tf_name] * 60 * 10**9)
    lr = np.diff(np.log(close))
    ok = (np.diff(bid) == 1) & (miss[:-1] == 0) & (miss[1:] == 0)
    return lr, ok


def stats(lr, ok, label):
    x = lr[ok]
    x = x[np.isfinite(x)]
    n = x.size
    sd = float(np.std(x, ddof=1))
    out = {"label": label, "n": int(n), "std": sd, "std_bps": sd * 1e4}
    # 5-sigma sensitivity: exclude, do not delete
    for _ in range(2):
        s = float(np.std(x, ddof=1))
        m = np.abs(x - np.mean(x)) <= 5 * s
        x = x[m]
    out["n_excl5s"] = int(x.size)
    out["std_excl5s"] = float(np.std(x, ddof=1))
    out["std_bps_excl5s"] = out["std_excl5s"] * 1e4
    out["excl_pct"] = 100.0 * (1 - x.size / n)
    # ACF(1) on contiguous pairs of contiguous steps
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tfdir", default="/tmp/xauusd_audit/timeframes")
    ap.add_argument("--out", default="/tmp/xauusd_audit/variance_signature.json")
    a = ap.parse_args()

    res = {}
    for t in GRID:
        lr, ok = contiguous_returns(f"{a.tfdir}/XAUUSD_{t}.parquet", t)
        s = stats(lr, ok, t)
        # ACF(1) restricted to pairs of consecutive contiguous steps
        okk = ok[:-1] & ok[1:]
        x = lr[:-1][okk]
        y = lr[1:][okk]
        x = x - x.mean()
        y = y - y.mean()
        s["acf1_contiguous"] = float(np.sum(x * y) / np.sum(x * x))
        s["n_acf1"] = int(x.size)
        s["contiguous_step_rate"] = float(ok.mean())
        res[t] = s
        print(f"{t:4} n={s['n']:>9} std_bps={s['std_bps']:8.4f} "
              f"excl5s_bps={s['std_bps_excl5s']:8.4f} ({s['excl_pct']:.3f}%) "
              f"acf1={s['acf1_contiguous']:+.5f}")

    v1 = res["M1"]["std"] ** 2
    v1e = res["M1"]["std_excl5s"] ** 2
    for t in GRID:
        k = K[t]
        res[t]["variance_ratio"] = res[t]["std"] ** 2 / (k * v1)
        res[t]["variance_ratio_excl5s"] = res[t]["std_excl5s"] ** 2 / (k * v1e)
        res[t]["vr_implied_by_acf1"] = 1 + 2 * res[t]["acf1_contiguous"]
    print()
    for t in GRID:
        print(f"{t:4} VR={res[t]['variance_ratio']:.4f} "
              f"VR_excl5s={res[t]['variance_ratio_excl5s']:.4f} "
              f"VR_from_acf1={res[t]['vr_implied_by_acf1']:.4f}")

    out = {"grid": GRID, "minutes": K, "timeframes": res,
           "note": ("contiguous steps only; variance ratio vs M1; "
                    "INFERENCE/PROXY - OHLC bars, not an order book")}
    with open(a.out, "w") as fh:
        json.dump(out, fh, indent=1)
    print("wrote", a.out)


if __name__ == "__main__":
    main()
