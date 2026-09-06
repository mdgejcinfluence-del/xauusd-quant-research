#!/usr/bin/env python3
"""
PHASE 2 - multi-scale measurement engine (no strategy, no backtest, no regime).

Everything computed here is a DESCRIPTIVE property of the price series at a
given sampling frequency.  Nothing is a profit, a return of a strategy, a
Sharpe, a drawdown, a hit-rate or an expectancy.

Microstructure statements are PROXIES / INFERENCES (we have OHLC, not an order
book): sign alternation, short-lag autocorrelation, ultra-short reversal,
variance-vs-sampling-frequency, directional efficiency.  They are labelled
INFERENCE in the report, never FACT.

Volume is never loaded (L1). Gaps are never filled (L2). Prices are never
homogenised (L3). Sources are never modified (L7).

Usage:
  python analyze_timeframes.py --master ... --tfdir ... --out metrics_tf.json
"""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

GRID = [("M1", 1), ("M2", 2), ("M3", 3), ("M4", 4), ("M5", 5), ("M10", 10),
        ("M15", 15), ("M20", 20), ("M30", 30), ("H1", 60), ("H2", 120),
        ("H4", 240)]

# hypothetical all-in round-trip costs, in USD of price. NOT broker quotes.
COST_SCENARIOS = [("COST_SCENARIO_1", 0.05), ("COST_SCENARIO_2", 0.10),
                  ("COST_SCENARIO_3", 0.25), ("COST_SCENARIO_4", 0.50),
                  ("COST_SCENARIO_5", 1.00)]
LOOKBACK = 20          # structure lookback (bars)
RECOVERY_HORIZON = 20  # max bars allowed for a move to be retraced


# --------------------------------------------------------------------------- #
def load_m1_context(master: str) -> dict:
    t = pq.read_table(master, columns=["timestamp", "close"])
    ts = t.column("timestamp").to_numpy(zero_copy_only=False)
    c = t.column("close").to_numpy().astype("float64")
    order = np.argsort(ts, kind="stable")
    ts, c = ts[order], c[order]
    ts_min = ts.astype("datetime64[m]").astype("int64")
    gap_next = np.zeros(len(ts_min), dtype="int64")
    gap_next[:-1] = ts_min[1:] - ts_min[:-1] - 1
    d = np.diff(c)
    cumabs = np.concatenate(([0.0], np.cumsum(np.abs(d))))
    cumgap = np.concatenate(([0], np.cumsum(gap_next)))
    return {"c": c, "cumabs": cumabs, "cumgap": cumgap, "ts": ts}


def load_tf(tfdir: str, name: str) -> dict:
    t = pq.read_table(os.path.join(tfdir, f"XAUUSD_{name}.parquet"))
    return {
        "ts": t.column("ts").to_numpy(zero_copy_only=False),
        "o": t.column("open").to_numpy().astype("float64"),
        "h": t.column("high").to_numpy().astype("float64"),
        "l": t.column("low").to_numpy().astype("float64"),
        "c": t.column("close").to_numpy().astype("float64"),
        "n_m1": t.column("n_m1").to_numpy().astype("int64"),
        "im": t.column("internal_missing").to_numpy().astype("int64"),
        "ib": t.column("internal_breaks").to_numpy().astype("int64"),
        "contig": t.column("contig_next").to_numpy().astype("int64"),
    }


# --------------------------------------------------------------------------- #
def subset(d: dict, sel_idx: np.ndarray) -> dict:
    """Select bars and recompute in-subset contiguity (never fills anything)."""
    out = {k: d[k][sel_idx] for k in ("ts", "o", "h", "l", "c", "n_m1", "im",
                                      "ib", "contig")}
    if len(sel_idx) > 1:
        consecutive = np.zeros(len(sel_idx), dtype="int64")
        consecutive[1:] = (np.diff(sel_idx) == 1).astype("int64")
        out["contig"] = out["contig"] * consecutive
    else:
        out["contig"] = np.zeros(len(sel_idx), dtype="int64")
    out["contig"][0] = 0
    out["idx"] = sel_idx
    return out


def acf(r: np.ndarray, valid: np.ndarray, lag: int) -> tuple[float, int]:
    """Autocorrelation at `lag` using only fully contiguous windows."""
    n = len(r)
    if n <= lag + 2:
        return float("nan"), 0
    cv = np.concatenate(([0], np.cumsum(valid.astype("int64"))))
    t = np.arange(0, n - lag)
    ok = (cv[t + lag + 1] - cv[t]) == (lag + 1)
    if ok.sum() < 100:
        return float("nan"), int(ok.sum())
    x = r[t[ok]]
    y = r[t[ok] + lag]
    sx, sy = x.std(), y.std()
    if sx == 0 or sy == 0:
        return float("nan"), int(ok.sum())
    return float(np.mean((x - x.mean()) * (y - y.mean())) / (sx * sy)), int(ok.sum())


def run_stats(r: np.ndarray, valid: np.ndarray) -> dict:
    """Sign runs on contiguous, non-zero returns."""
    iv = np.flatnonzero(valid & (r != 0))
    if len(iv) < 10:
        return {"mean_run": float("nan"), "median_run": float("nan"),
                "p90_run": float("nan"), "max_run": float("nan"),
                "n_runs": 0, "n_elements": int(len(iv))}
    adj = np.diff(iv) == 1
    sg = np.sign(r[iv])
    change = sg[1:] != sg[:-1]
    start = np.ones(len(iv), dtype=bool)
    start[1:] = (~adj) | change
    run_id = np.cumsum(start) - 1
    lens = np.bincount(run_id)
    return {"mean_run": float(lens.mean()), "median_run": float(np.median(lens)),
            "p90_run": float(np.percentile(lens, 90)), "max_run": int(lens.max()),
            "n_runs": int(len(lens)), "n_elements": int(len(iv))}


def recovery(r: np.ndarray, valid: np.ndarray, logc: np.ndarray) -> dict:
    """Ultra-short reversal: how a move is retraced by the following bars."""
    n = len(r)
    pair = np.flatnonzero(valid[:-1] & valid[1:] & (r[:-1] != 0) & (r[1:] != 0))
    if len(pair) < 100:
        return {"reversal_freq": float("nan"), "mean_recovery_ratio": float("nan"),
                "median_recovery_ratio": float("nan"),
                "full_recovery_rate": float("nan"), "mean_recovery_delay": float("nan"),
                "no_recovery_within_h": float("nan")}
    a, b = r[pair], r[pair + 1]
    oppo = np.sign(a) != np.sign(b)
    res = {"reversal_freq": float(oppo.mean())}
    if oppo.sum() > 50:
        ratio = np.abs(b[oppo]) / np.abs(a[oppo])
        res["median_recovery_ratio"] = float(np.median(ratio))
        res["full_recovery_rate"] = float((ratio >= 1.0).mean())
        # robust mean: restricted to meaningful moves (the raw mean is dominated
        # by microscopic denominators)
        mag = np.abs(a[oppo])
        thr = np.median(np.abs(a))
        big = mag >= thr
        res["mean_recovery_ratio_robust"] = (float(ratio[big].mean())
                                             if big.sum() > 50 else float("nan"))
        res["full_recovery_rate_big_moves"] = (float((ratio[big] >= 1.0).mean())
                                               if big.sum() > 50 else float("nan"))
    else:
        res.update({"median_recovery_ratio": float("nan"),
                    "full_recovery_rate": float("nan"),
                    "mean_recovery_ratio_robust": float("nan"),
                    "full_recovery_rate_big_moves": float("nan")})
    # time (in bars) needed to retrace the move
    big = np.flatnonzero(valid & (r != 0))
    if len(big) == 0:
        res.update({"mean_recovery_delay": float("nan"),
                    "no_recovery_within_h": float("nan")})
        return res
    move = r[big]
    p0 = logc[big + 1]           # price level after the move
    delay = np.full(len(big), -1, dtype="int64")
    todo = np.ones(len(big), dtype=bool)
    H = min(RECOVERY_HORIZON, n - 1)
    for hh in range(1, H + 1):
        cand = np.flatnonzero(todo & (big + 1 + hh <= n))
        if len(cand) == 0:
            break
        disp = logc[big[cand] + 1 + hh] - p0[cand]
        hit = (disp * move[cand] < 0) & (np.abs(disp) >= np.abs(move[cand]))
        delay[cand[hit]] = hh
        todo[cand[hit]] = False
    found = delay > 0
    res["mean_recovery_delay"] = float(delay[found].mean()) if found.any() else float("nan")
    res["median_recovery_delay"] = float(np.median(delay[found])) if found.any() else float("nan")
    res["no_recovery_within_h"] = float((~found).mean())
    return res


def directional_efficiency(d: dict, m1: dict, h: int) -> dict:
    """|net displacement| / path length, at TF resolution and at M1 resolution."""
    c = d["c"]
    n = len(c)
    if n <= h + 2:
        return {"de_tf": float("nan"), "de_m1": float("nan"), "n_windows": 0}
    step = np.abs(np.diff(c))
    cumabs = np.concatenate(([0.0], np.cumsum(step)))
    valid = d["contig"][1:].astype("int64") if len(d["contig"]) == n else None
    cv = np.concatenate(([0], np.cumsum(valid)))
    t = np.arange(0, n - h)
    ok = (cv[t + h] - cv[t]) == h
    path_tf = cumabs[t + h] - cumabs[t]
    net = np.abs(c[t + h] - c[t])
    good = ok & (path_tf > 0)
    de_tf = float(np.mean(net[good] / path_tf[good])) if good.sum() > 50 else float("nan")

    # M1-resolution path over the same window (needs the TF bar boundaries)
    if "idx" in d:
        # a subset: recover end indices from the full-series end index table
        end_idx = m1["end_idx"][d["idx"]]
    else:
        end_idx = m1["end_idx"]
    if len(end_idx) != n:
        return {"de_tf": de_tf, "de_m1": float("nan"), "n_windows": int(good.sum())}
    a = end_idx[t] - 1
    b = end_idx[t + h] - 1
    path_m1 = m1["cumabs"][b] - m1["cumabs"][a]
    contig_m1 = (m1["cumgap"][b] - m1["cumgap"][a]) == 0
    net_m1 = np.abs(m1["c"][b] - m1["c"][a])
    good2 = contig_m1 & (path_m1 > 0)
    de_m1 = float(np.mean(net_m1[good2] / path_m1[good2])) if good2.sum() > 50 else float("nan")
    return {"de_tf": de_tf, "de_m1": de_m1, "n_windows": int(good.sum()),
            "n_windows_m1": int(good2.sum())}


def moments(x: np.ndarray) -> dict:
    x = x[np.isfinite(x)]
    if len(x) < 100:
        return {k: float("nan") for k in
                ("mean", "std", "median", "q01", "q05", "q25", "q50", "q75",
                 "q95", "q99", "skew", "excess_kurtosis", "tail_2s", "tail_3s")}
    m = x.mean()
    s = x.std()
    z = (x - m) / s if s > 0 else x * 0
    m2 = np.mean((x - m) ** 2)
    m3 = np.mean((x - m) ** 3)
    m4 = np.mean((x - m) ** 4)
    return {
        "mean": float(m), "std": float(s),
        "median": float(np.median(x)),
        "q01": float(np.percentile(x, 1)), "q05": float(np.percentile(x, 5)),
        "q25": float(np.percentile(x, 25)), "q50": float(np.percentile(x, 50)),
        "q75": float(np.percentile(x, 75)), "q95": float(np.percentile(x, 95)),
        "q99": float(np.percentile(x, 99)),
        "skew": float(m3 / m2 ** 1.5) if m2 > 0 else float("nan"),
        "excess_kurtosis": float(m4 / m2 ** 2 - 3.0) if m2 > 0 else float("nan"),
        "tail_2s": float(np.mean(np.abs(z) > 2)),
        "tail_3s": float(np.mean(np.abs(z) > 3)),
    }


def structure(d: dict) -> dict:
    o, h, l, c = d["o"], d["h"], d["l"], d["c"]
    n = len(c)
    if n < LOOKBACK + 30:
        return {}
    sh, sl, sc = pd.Series(h), pd.Series(l), pd.Series(c)
    hh = sh.rolling(LOOKBACK).max().shift(1).to_numpy()
    ll = sl.rolling(LOOKBACK).min().shift(1).to_numpy()
    ok = np.isfinite(hh) & np.isfinite(ll)
    new_hi = ok & (h > hh)
    new_lo = ok & (l < ll)
    brk = ok & ((c > hh) | (c < ll))
    # reintegration: close back inside [ll, hh] within 5 bars after a breakout
    idx_b = np.flatnonzero(brk)
    idx_b = idx_b[idx_b + 5 < n]
    if len(idx_b) > 50:
        rein = np.zeros(len(idx_b), dtype=bool)
        for j in range(1, 6):
            cc = c[idx_b + j]
            inside = (cc <= hh[idx_b]) & (cc >= ll[idx_b])
            rein |= inside
        reintegration_rate = float(rein.mean())
    else:
        reintegration_rate = float("nan")
    rng = h - l
    prev = rng[:-1]
    prev = np.where(prev > 0, prev, np.nan)
    lr = np.log(np.where(rng[1:] > 0, rng[1:], np.nan) / prev)
    lr = lr[np.isfinite(lr)]
    body = np.abs(c - o)
    with np.errstate(divide="ignore", invalid="ignore"):
        body_ratio = np.where(rng > 0, body / rng, np.nan)
        up_wick = np.where(rng > 0, (h - np.maximum(o, c)) / rng, np.nan)
        dn_wick = np.where(rng > 0, (np.minimum(o, c) - l) / rng, np.nan)
    return {
        "new_extreme_rate": float(np.mean(ok & (new_hi | new_lo))),
        "breakout_rate": float(brk[ok].mean()) if ok.sum() else float("nan"),
        "reintegration_rate_within_5": reintegration_rate,
        "breakout_persistence": (1.0 - reintegration_rate
                                 if reintegration_rate == reintegration_rate
                                 else float("nan")),
        "range_expansion_std_log": float(lr.std()) if len(lr) > 100 else float("nan"),
        "range_expansion_freq": float(np.mean(rng[1:] > rng[:-1])),
        "mean_body_over_range": float(np.nanmean(body_ratio)),
        "mean_upper_wick_over_range": float(np.nanmean(up_wick)),
        "mean_lower_wick_over_range": float(np.nanmean(dn_wick)),
    }


def amplitude(d: dict) -> dict:
    h, l, c, o = d["h"], d["l"], d["c"], d["o"]
    rng = h - l
    with np.errstate(divide="ignore", invalid="ignore"):
        rng_bps = rng / c * 1e4
        body_bps = np.abs(c - o) / c * 1e4
    out = {}
    for key, arr in (("range_usd", rng), ("range_bps", rng_bps),
                     ("body_bps", body_bps)):
        arr = arr[np.isfinite(arr)]
        out[key] = {
            "mean": float(arr.mean()), "median": float(np.median(arr)),
            "p25": float(np.percentile(arr, 25)), "p50": float(np.percentile(arr, 50)),
            "p75": float(np.percentile(arr, 75)), "p90": float(np.percentile(arr, 90)),
            "p95": float(np.percentile(arr, 95)), "p99": float(np.percentile(arr, 99)),
            "max": float(arr.max()),
        }
    return out


def core(d: dict, k: int, m1: dict, span_years: float, deep: bool = True) -> dict:
    c, h, l, o = d["c"], d["h"], d["l"], d["o"]
    n = len(c)
    res: dict = {"bars": int(n)}
    if n < 50:
        return res
    valid = (d["contig"][1:] == 1)
    with np.errstate(divide="ignore", invalid="ignore"):
        r = np.diff(np.log(c))
    rv = r[valid]
    rv = rv[np.isfinite(rv)]

    # --- A. autocorrelation
    res["acf"] = {}
    for lag in (1, 2, 3, 4, 8):
        v, cnt = acf(r, valid, lag)
        res["acf"][f"lag{lag}"] = v
        res["acf"][f"lag{lag}_n"] = cnt

    # --- B. alternation / runs
    rs = run_stats(r, valid)
    res["runs"] = rs
    pair = np.flatnonzero(valid[:-1] & valid[1:] & (r[:-1] != 0) & (r[1:] != 0))
    if len(pair) > 100:
        sc = (np.sign(r[pair]) != np.sign(r[pair + 1])).mean()
        res["sign_change_freq"] = float(sc)
    else:
        res["sign_change_freq"] = float("nan")

    # --- C. ultra-short reversal
    res["reversal"] = (recovery(r, valid, np.log(c)) if deep
                       else {"reversal_freq": float("nan")})

    # --- D. variance / volatility
    m = moments(rv)
    res["returns"] = m
    bars_per_year = n / span_years if span_years > 0 else float("nan")
    res["bars_per_year"] = float(bars_per_year)
    res["ann_vol"] = float(m["std"] * np.sqrt(bars_per_year))
    res["ann_vol_bps"] = float(m["std"] * 1e4 * np.sqrt(bars_per_year))

    # --- E. distribution of bar-to-bar absolute relative moves
    with np.errstate(divide="ignore", invalid="ignore"):
        absrel = np.abs(r) * 1e4
    res["abs_move_bps"] = moments(absrel[valid & np.isfinite(absrel)])

    # --- F. directional efficiency
    for hh in (5, 10, 20):
        de = directional_efficiency(d, m1, hh)
        res[f"de_tf_h{hh}"] = de["de_tf"]
        res[f"de_m1_h{hh}"] = de["de_m1"]
        res[f"de_n_h{hh}"] = de["n_windows"]

    # --- structure, amplitude, integrity
    res["structure"] = structure(d) if deep else {}
    res["amplitude"] = amplitude(d)
    res["integrity"] = {
        "bars_with_internal_data_gap": float(np.mean(d["im"] > 0)),
        "bars_with_internal_market_break": float(np.mean(d["ib"] > 0)),
        "mean_m1_per_bar": float(np.mean(d["n_m1"])),
        "contiguous_step_rate": float(np.mean(d["contig"][1:] == 1)),
        "mean_internal_missing_min": float(np.mean(d["im"])),
    }
    res["mean_price"] = float(np.mean(c))
    return res


# --------------------------------------------------------------------------- #
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--master",
                    default="/tmp/xauusd_audit/XAUUSD_M1_reconstructed.parquet")
    ap.add_argument("--tfdir", default="/tmp/xauusd_audit/timeframes")
    ap.add_argument("--out", default="/tmp/xauusd_audit/metrics_tf.json")
    ap.add_argument("--only", default=None,
                    help="comma separated subset of the grid, for smoke tests")
    args = ap.parse_args()
    grid = GRID
    if args.only:
        keep = set(x.strip() for x in args.only.split(","))
        grid = [g for g in GRID if g[0] in keep]

    m1 = load_m1_context(args.master)
    m1["end_idx"] = None  # filled per timeframe
    print("M1 context ready", flush=True)

    out = {
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "cost_scenarios": COST_SCENARIOS,
        "grid": [n for n, _ in GRID],
        "timeframes": {},
    }
    span_years = (m1["ts"][-1] - m1["ts"][0]) / np.timedelta64(365 * 24 * 60, "m") \
        if False else (m1["ts"][-1] - m1["ts"][0]) / np.timedelta64(1, "D") / 365.25
    out["span_years"] = float(span_years)

    for name, k in grid:
        print(f"--- {name} (k={k}) ---", flush=True)
        d = load_tf(args.tfdir, name)
        end_idx = np.cumsum(d["n_m1"])
        m1["end_idx"] = end_idx
        assert len(end_idx) == len(d["c"])

        tf = {"minutes": k, "full": core(d, k, m1, span_years, deep=True)}

        # ---- per year -----------------------------------------------------
        years = d["ts"].astype("datetime64[Y]").astype(int) + 1970
        tf["by_year"] = {}
        for y in sorted(set(years.tolist())):
            sel = np.flatnonzero(years == y)
            if len(sel) < 50:
                continue
            sub = subset(d, sel)
            span_y = 1.0
            tf["by_year"][str(y)] = core(sub, k, m1, span_y, deep=False)
            tf["by_year"][str(y)]["bars"] = int(len(sel))
        print(f"    years: {len(tf['by_year'])}", flush=True)

        # ---- 2013 session-convention break ---------------------------------
        for lab, sel in (("pre2013", np.flatnonzero(years <= 2012)),
                         ("post2013", np.flatnonzero((years >= 2013) & (years <= 2025))),
                         ("y2026", np.flatnonzero(years == 2026))):
            if len(sel) < 50:
                continue
            sub = subset(d, sel)
            nyears = {"pre2013": 3.0, "post2013": 13.0, "y2026": 0.663}[lab]
            tf[lab] = core(sub, k, m1, nyears, deep=True)
        print("    2013 split + 2026 done", flush=True)

        # ---- sensitivity: temporary exclusion of extreme returns -----------
        valid = d["contig"][1:] == 1
        r = np.diff(np.log(d["c"]))
        s = np.nanstd(r[valid])
        keep = np.ones(len(d["c"]), dtype=bool)
        idx_ext = np.flatnonzero(np.abs(r) > 5 * s)
        drop = np.zeros(len(d["c"]), dtype=bool)
        drop[idx_ext + 1] = True   # drop the bar that ENDS the extreme move
        sel = np.flatnonzero(~drop)
        if len(sel) > 50:
            tf["sensitivity_excl_5sigma"] = core(subset(d, sel), k, m1,
                                                 span_years, deep=False)
            tf["sensitivity_excl_5sigma"]["bars_dropped"] = int(drop.sum())
            tf["sensitivity_excl_5sigma"]["bars_dropped_pct"] = float(drop.mean() * 100)

        # ---- M1-level path statistics for the information-loss table -------
        start_idx = end_idx - d["n_m1"]
        a, b = start_idx, end_idx - 1
        path = m1["cumabs"][b] - m1["cumabs"][a]
        net = np.abs(m1["c"][b] - m1["c"][a])
        good = path > 0
        tf["intrabar"] = {
            "mean_path_usd": float(np.mean(path)),
            "mean_net_usd": float(np.mean(net)),
            # k == 1: a single M1 bar has no internal path -> nothing to lose
            "path_retention_ratio": (1.0 if k == 1
                                     else float(np.mean(net[good] / path[good]))),
            "mean_intrabar_reversals": float(_reversals_in_bar(m1, start_idx, end_idx)),
        }
        # pivots at M1 resolution collapsed into one TF bar
        tf["intrabar"]["m1_pivots_per_bar"] = float(
            _pivots_per_bar(m1, start_idx, end_idx))
        out["timeframes"][name] = tf
        print("    done", flush=True)

    with open(args.out, "w") as fh:
        json.dump(out, fh, indent=1, default=_json_default)
    print(f"written {args.out}")


def _events_per_bar(events_pos: np.ndarray, start_idx: np.ndarray,
                    n_bars: int, strict_inside: bool = False,
                    end_idx: np.ndarray | None = None) -> float:
    """Mean number of M1-level events collapsed into one aggregated bar.

    events_pos   : M1 indices of the events (reversals, pivots, ...)
    strict_inside: if True, an event sitting exactly on the FIRST M1 index of a
                   bar is not counted: that step is the transition from the
                   previous bar and remains visible as open-vs-previous-close.
                   With M1 bars (k=1) nothing can be inside a bar, so the
                   count is 0 - which is the correct value for "lost events".
    end_idx      : exclusive end of each bar. When given together with
                   strict_inside, an event on the LAST M1 index of a bar is
                   also excluded.

    Off-by-one note (reversals).  A reversal is recorded at position p when the
    sign of step (p-1 -> p) differs from the sign of step (p -> p+1).  The bar
    spans M1 indices [a, b] with b = end_idx-1, so its *internal* steps are
    d1[a .. b-1].  A junction is invisible in the aggregated series only if
    BOTH steps are internal, i.e. p in [a+1, b-1].  The junction at p = b
    involves the step b -> b+1, which is the first step of the next bar and is
    therefore still visible as the aggregated return between the two bars.
    Counting it would overstate the information loss by exactly one junction
    per bar.
    """
    if len(events_pos) == 0 or n_bars == 0:
        return 0.0
    bar_of = np.searchsorted(start_idx, events_pos, side="right") - 1
    ok = (bar_of >= 0) & (bar_of < n_bars)
    clip = np.clip(bar_of, 0, n_bars - 1)
    if strict_inside:
        ok &= events_pos > start_idx[clip]
        if end_idx is not None:
            ok &= events_pos <= end_idx[clip] - 2
    bar_of = bar_of[ok]
    if len(bar_of) == 0:
        return 0.0
    counts = np.bincount(bar_of, minlength=n_bars)
    return float(counts.mean())


def _reversals_in_bar(m1, start_idx, end_idx) -> float:
    """Mean number of M1 sign reversals that aggregation collapses into a bar.

    Only junctions whose two steps both lie strictly inside the bar are
    counted (see the off-by-one note in _events_per_bar).
    """
    c = m1["c"]
    d1 = np.diff(c)
    s = np.sign(d1)
    idx = np.flatnonzero(s != 0)
    sv = s[idx]
    ch = np.zeros(len(idx), dtype=bool)
    ch[1:] = (sv[1:] != sv[:-1]) & (np.diff(idx) == 1)
    return _events_per_bar(idx[ch], start_idx, len(start_idx),
                           strict_inside=True, end_idx=end_idx)


def _pivots_per_bar(m1, start_idx, end_idx) -> float:
    """Mean number of M1 local extrema collapsed into one aggregated bar."""
    c = m1["c"]
    piv = np.zeros(len(c), dtype=bool)
    piv[1:-1] = ((c[1:-1] > c[:-2]) & (c[1:-1] > c[2:])) | \
                ((c[1:-1] < c[:-2]) & (c[1:-1] < c[2:]))
    return _events_per_bar(np.flatnonzero(piv), start_idx, len(start_idx))


def _json_default(o):
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        v = float(o)
        return None if not np.isfinite(v) else v
    if isinstance(o, (np.bool_,)):
        return bool(o)
    return str(o)


if __name__ == "__main__":
    main()
