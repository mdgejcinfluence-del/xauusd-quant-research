#!/usr/bin/env python3
"""
PHASE 2B - DEEP GRANULARITY AUDIT / STRESS TEST / MICROSTRUCTURE PROXY
Resolutions under test: M1, M3, H1 only.

PRE-REGIME, PRE-STRATEGY.  This module measures MARKET BEHAVIOUR only.
There is no trade, no position, no entry, no exit, no PnL, no Sharpe, no
drawdown, no hit rate, no expectancy, no optimisation, no regime object and
no regime label anywhere in this file.  The volume column is never loaded
(Phase 1 limitation L1).  Missing data is never filled (L2).  Extremes are
never removed or winsorised (L6).

==========================================================================
EX ANTE SPECIFICATION - fixed before any metric was computed
==========================================================================
VW_MIN          trailing volatility windows, WALL-CLOCK minutes: 60 / 240 /
                1440.  Chosen for temporal-resolution reasons (1 hour, 4
                hours, 1 day), NOT because of any ranking they produce.
                Implemented as W/k bars so the wall-clock horizon is the
                same at every resolution.
SESSION_WINDOWS fixed UTC hour ranges partitioning the 24h day, declared as
                pure TIME WINDOWS.  They are not attributed to any class of
                market participant.
SHOCK_RULE      |log return of one bar| > 3 * sigma, where sigma is the
                trailing rolling standard deviation of the same series over
                the previous 1440 wall-clock minutes, past data only.
HURST_LAGS      lag set in BARS, identical across resolutions: 2,4,8,16,32,64.
COST_SCENARIOS  five hypothetical all-in round-trip costs in USD of price.
                HYPOTHETICAL.  BROKER_COST_STATUS = EXTERNAL_INPUT_REQUIRED.
VOL_CLASSES     HIGH_VOL if the bar's trailing 1440-min sigma exceeds the
                trailing 1-year MEAN of that same sigma (both strictly
                past-only), else LOW_VOL.

Usage:
  python deep_audit.py --out /tmp/xauusd_audit/deep_metrics.json
"""
from __future__ import annotations

import argparse
import json
import os

import numpy as np
import pyarrow.parquet as pq

# --------------------------------------------------------------------------- #
#  EX ANTE SPECIFICATION (see module docstring)
# --------------------------------------------------------------------------- #
TF = ["M1", "M3", "H1"]
K = {"M1": 1, "M3": 3, "H1": 60}
VW_MIN = (60, 240, 1440)
SESSION_WINDOWS = (("UTC_WINDOW_00_06", 0, 6), ("UTC_WINDOW_06_12", 6, 12),
                   ("UTC_WINDOW_12_16", 12, 16), ("UTC_WINDOW_16_21", 16, 21),
                   ("UTC_WINDOW_21_24", 21, 24))
SHOCK_SIGMA_MIN = 1440
SHOCK_K = 3.0
HURST_LAGS = (2, 4, 8, 16, 32, 64)
COST_SCENARIOS = [("COST_SCENARIO_1", 0.05), ("COST_SCENARIO_2", 0.10),
                  ("COST_SCENARIO_3", 0.25), ("COST_SCENARIO_4", 0.50),
                  ("COST_SCENARIO_5", 1.00)]
COST_DOMINATION_PCT = (0.5, 1, 2, 5, 10, 20)
ACF_LAGS = (1, 2, 3, 4, 5)
SHOCK_TOP_N = 40


# --------------------------------------------------------------------------- #
def load(path):
    t = pq.read_table(path)
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


def subset(d, sel):
    out = {k: d[k][sel] for k in ("ts", "o", "h", "l", "c", "n_m1", "im", "ib",
                                  "contig")}
    if len(sel) > 1:
        consec = np.zeros(len(sel), dtype="int64")
        consec[1:] = (np.diff(sel) == 1).astype("int64")
        out["contig"] = out["contig"] * consec
    else:
        out["contig"] = np.zeros(len(sel), dtype="int64")
    out["contig"][0] = 0
    out["idx"] = sel
    return out


def q(x, ps=(50, 75, 90, 95, 99)):
    x = x[np.isfinite(x)]
    if len(x) < 30:
        return {f"p{p}": float("nan") for p in ps}
    return {f"p{p}": float(np.percentile(x, p)) for p in ps}


def moments(x):
    x = x[np.isfinite(x)]
    n = len(x)
    if n < 100:
        return {k: float("nan") for k in ("mean", "std", "median", "skew",
                                          "excess_kurtosis")}
    m = x.mean()
    s = x.std()
    m2 = np.mean((x - m) ** 2)
    m3 = np.mean((x - m) ** 3)
    m4 = np.mean((x - m) ** 4)
    return {"mean": float(m), "std": float(s), "median": float(np.median(x)),
            "skew": float(m3 / m2 ** 1.5) if m2 > 0 else float("nan"),
            "excess_kurtosis": float(m4 / m2 ** 2 - 3.0) if m2 > 0
            else float("nan")}


def acf(r, valid, lag):
    """Autocorrelation using only fully contiguous lag-windows."""
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
    return (float(np.mean((x - x.mean()) * (y - y.mean())) / (sx * sy)),
            int(ok.sum()))


def run_stats(r, valid):
    iv = np.flatnonzero(valid & (r != 0))
    if len(iv) < 10:
        return {"mean_run": float("nan"), "median_run": float("nan"),
                "p90_run": float("nan"), "max_run": 0, "n_runs": 0}
    adj = np.diff(iv) == 1
    sg = np.sign(r[iv])
    change = sg[1:] != sg[:-1]
    start = np.ones(len(iv), dtype=bool)
    start[1:] = (~adj) | change
    lens = np.bincount(np.cumsum(start) - 1)
    return {"mean_run": float(lens.mean()),
            "median_run": float(np.median(lens)),
            "p90_run": float(np.percentile(lens, 90)),
            "max_run": int(lens.max()), "n_runs": int(len(lens))}


def rolling_std(x, m):
    """Trailing std over the m observations ENDING BEFORE index i (past-only).
    out[i] = std(x[i-m : i]) for i >= m ; NaN elsewhere."""
    n = len(x)
    out = np.full(n, np.nan)
    if n <= m:
        return out
    cs = np.concatenate(([0.0], np.cumsum(x)))
    cs2 = np.concatenate(([0.0], np.cumsum(x * x)))
    s1 = cs[m:n] - cs[:n - m]       # windows [i-m, i) for i = m..n-1
    s2 = cs2[m:n] - cs2[:n - m]
    mu = s1 / m
    var = s2 / m - mu * mu
    var = np.maximum(var, 0.0)
    out[m:] = np.sqrt(var)
    return out


def rolling_mean(x, m):
    """Trailing mean over the m observations ending before index i."""
    n = len(x)
    out = np.full(n, np.nan)
    if n <= m:
        return out
    cs = np.concatenate(([0.0], np.cumsum(np.nan_to_num(x))))
    out[m:] = (cs[m:n] - cs[:n - m]) / m
    return out


def variance_ratio(r, valid, lag):
    """VR(q) on strictly contiguous q-step windows.

    Non-overlapping windows (stride = lag) so the estimator is not dominated
    by overlap-induced correlation.  Vectorised with a cumulative sum: a
    Python loop over up to 2.9M windows would not terminate in reasonable
    time at M1 resolution.
    """
    n = len(r)
    if n < lag * 50:
        return float("nan"), 0
    cv = np.concatenate(([0], np.cumsum(valid.astype("int64"))))
    t = np.arange(0, n - lag + 1)
    ok = (cv[t + lag] - cv[t]) == lag
    if ok.sum() < 100:
        return float("nan"), int(ok.sum())
    t = t[ok][::lag]                       # non-overlapping
    cs = np.concatenate(([0.0], np.cumsum(r)))
    sums = cs[t + lag] - cs[t]
    base = r[valid.astype(bool)]
    if len(base) < 100 or base.std() == 0 or sums.std() == 0:
        return float("nan"), int(len(t))
    return float(sums.var() / (lag * base.var())), int(len(t))


MAX_RS_BLOCKS = 20000      # cap on R/S blocks, for tractability at M1
MIN_RS_WINDOW = 8          # R/S is not meaningful on very short blocks


def hurst_rs(r, valid, m):
    """Classical rescaled-range estimate over contiguous blocks of length m.

    Only fully contiguous blocks are used; the block count is capped by even
    striding so that an M1 series of 5.9M bars stays tractable.  The cap and
    the minimum window are declared ex ante in MAX_RS_BLOCKS / MIN_RS_WINDOW.
    """
    n = len(r)
    if m < MIN_RS_WINDOW or n < m * 20:
        return float("nan"), 0
    nb = n // m
    if nb == 0:
        return float("nan"), 0
    stride = max(1, int(np.ceil(nb / MAX_RS_BLOCKS)))
    vals = []
    for b in range(0, nb, stride):
        x = r[b * m:(b + 1) * m]
        v = valid[b * m:(b + 1) * m]
        if v.sum() < m:            # require a fully contiguous block
            continue
        x = x - x.mean()
        z = np.cumsum(x)
        rng = z.max() - z.min()
        sd = x.std()
        if sd > 0 and rng > 0:
            vals.append(rng / sd)
    if len(vals) < 10:
        return float("nan"), len(vals)
    return float(np.mean(vals)), len(vals)


def de(d, h):
    """Directional efficiency |net|/path at this resolution, horizon h bars."""
    c = d["c"]
    n = len(c)
    if n <= h + 2:
        return float("nan")
    step = np.abs(np.diff(c))
    cum = np.concatenate(([0.0], np.cumsum(step)))
    valid = (d["contig"][1:] == 1).astype("int64")
    cv = np.concatenate(([0], np.cumsum(valid)))
    t = np.arange(0, n - h)
    ok = (cv[t + h] - cv[t]) == h
    path = cum[t + h] - cum[t]
    net = np.abs(c[t + h] - c[t])
    good = ok & (path > 0)
    return float(np.mean(net[good] / path[good])) if good.sum() > 50 \
        else float("nan")


# --------------------------------------------------------------------------- #
def base_block(d, k, deep=True):
    """Metric block computed on an arbitrary subset of bars."""
    c, o, h, l = d["c"], d["o"], d["h"], d["l"]
    n = len(c)
    res = {"bars": int(n)}
    if n < 200:
        return res
    valid = (d["contig"][1:] == 1)
    with np.errstate(divide="ignore", invalid="ignore"):
        r = np.diff(np.log(c))
    rv = r[valid]
    rv = rv[np.isfinite(rv)]

    res["acf"] = {}
    for lag in ACF_LAGS:
        v, cnt = acf(r, valid, lag)
        res["acf"][f"lag{lag}"] = v
        res["acf"][f"lag{lag}_n"] = cnt

    res["runs"] = run_stats(r, valid)
    pair = np.flatnonzero(valid[:-1] & valid[1:] & (r[:-1] != 0) & (r[1:] != 0))
    res["sign_change_freq"] = float((np.sign(r[pair]) != np.sign(r[pair + 1])).mean()) \
        if len(pair) > 100 else float("nan")

    res["returns"] = moments(rv)

    # ---- amplitude: USD, % of price, wick/body structure -------------------
    rng = h - l
    body = np.abs(c - o)
    with np.errstate(divide="ignore", invalid="ignore"):
        rng_pct = rng / c * 100.0
        rng_bps = rng / c * 1e4
        body_pct = body / c * 100.0
        up_wick = (h - np.maximum(o, c))
        dn_wick = (np.minimum(o, c) - l)
        br = np.where(rng > 0, body / rng, np.nan)
        uw = np.where(rng > 0, up_wick / rng, np.nan)
        dw = np.where(rng > 0, dn_wick / rng, np.nan)
        wb = np.where(body > 0, (up_wick + dn_wick) / body, np.nan)
    res["amplitude_usd"] = {
        "range": {**moments(rng), **q(rng)},
        "body": {**moments(body), **q(body)},
        "upper_wick": {**moments(up_wick), **q(up_wick)},
        "lower_wick": {**moments(dn_wick), **q(dn_wick)},
    }
    res["amplitude_pct"] = {"range": {**moments(rng_pct), **q(rng_pct)},
                            "body": {**moments(body_pct), **q(body_pct)}}
    res["amplitude_bps"] = {"range": {**moments(rng_bps), **q(rng_bps)}}
    res["shape"] = {"mean_body_over_range": float(np.nanmean(br)),
                    "mean_upper_wick_over_range": float(np.nanmean(uw)),
                    "mean_lower_wick_over_range": float(np.nanmean(dw)),
                    "mean_wick_over_body": float(np.nanmean(wb)),
                    "median_body_over_range": float(np.nanmedian(br))}

    # ---- volatility-normalised amplitude (ex ante windows) ----------------
    mret = len(r)
    sig = {}
    norm = {}
    for W in VW_MIN:
        m = max(2, int(round(W / k)))
        if m >= mret:
            continue
        s = rolling_std(r, m)              # past-only trailing sigma
        # align: sigma at bar i uses returns [i-m, i) -> applies to bar i
        idx = np.arange(m, mret)           # bar indices i that have a sigma
        rr = r[idx]
        vv = valid[idx]
        ss = s[idx]
        ok = vv & np.isfinite(ss) & (ss > 0) & np.isfinite(rr)
        rng_i = rng[idx]
        body_i = body[idx]
        with np.errstate(divide="ignore", invalid="ignore"):
            rn = rng_i / c[idx] / ss       # range in units of recent vol
            bn = body_i / c[idx] / ss
            an = np.abs(rr) / ss
        sig[f"w{W}"] = {"sigma_median": float(np.nanmedian(ss[ok])),
                        "n": int(ok.sum())}
        norm[f"w{W}"] = {
            "range_over_sigma": {**q(rn[ok]), "mean": float(np.nanmean(rn[ok]))},
            "body_over_sigma": {**q(bn[ok]), "mean": float(np.nanmean(bn[ok]))},
            "absret_over_sigma": {**q(an[ok]), "mean": float(np.nanmean(an[ok]))},
        }
    res["sigma"] = sig
    res["vol_normalised"] = norm

    # ---- directional efficiency -------------------------------------------
    res["de"] = {f"h{h_}": de(d, h_) for h_ in (5, 10, 20)}

    # ---- continuity --------------------------------------------------------
    res["integrity"] = {
        "bars_with_internal_data_gap": float(np.mean(d["im"] > 0)),
        "bars_with_internal_market_break": float(np.mean(d["ib"] > 0)),
        "incomplete_windows": float(np.mean((d["n_m1"] < k) & (d["im"] == 0))),
        "mean_m1_per_bar": float(np.mean(d["n_m1"])),
        "mean_internal_missing_min": float(np.mean(d["im"])),
        "total_missing_min": float(np.sum(d["im"])),
        "contiguous_step_rate": float(np.mean(valid)),
        "non_contiguous_steps": int((~valid).sum()),
    }
    res["mean_price"] = float(np.mean(c))
    return res


def persistence_block(d, r, valid, rs=True):
    """Variance ratio + Hurst family, for the H1 persistence section.

    rs=False skips the rescaled-range estimator (used for the split blocks,
    where only the cheap VR-implied Hurst is carried).
    """
    out = {"vr": {}, "hurst_rs": {}, "hurst_vr": {}}
    for lag in HURST_LAGS:
        v, cnt = variance_ratio(r, valid, lag)
        out["vr"][f"q{lag}"] = v
        out["vr"][f"q{lag}_n"] = cnt
    # VR-implied Hurst: log VR(q) = (2H-1) log q
    xs, ys = [], []
    for lag in HURST_LAGS:
        v = out["vr"][f"q{lag}"]
        if v is not None and np.isfinite(v) and v > 0:
            xs.append(np.log(lag))
            ys.append(np.log(v))
    if len(xs) >= 3:
        slope = float(np.polyfit(xs, ys, 1)[0])
        out["hurst_vr"]["all_lags"] = float((slope + 1.0) / 2.0)
        # window sensitivity: fit on the lower half and upper half of lags
        lo = HURST_LAGS[:len(HURST_LAGS) // 2]
        hi = HURST_LAGS[len(HURST_LAGS) // 2:]
        for nm, sub in (("short_lags", lo), ("long_lags", hi)):
            xs2, ys2 = [], []
            for lag in sub:
                v = out["vr"][f"q{lag}"]
                if v is not None and np.isfinite(v) and v > 0:
                    xs2.append(np.log(lag))
                    ys2.append(np.log(v))
            if len(xs2) >= 2:
                out["hurst_vr"][nm] = float(
                    (float(np.polyfit(xs2, ys2, 1)[0]) + 1.0) / 2.0)
            else:
                out["hurst_vr"][nm] = float("nan")
    else:
        out["hurst_vr"]["all_lags"] = float("nan")
    # R/S Hurst on the same bar-lag set
    if rs:
        xs, ys = [], []
        for m in HURST_LAGS:
            v, cnt = hurst_rs(r, valid, m)
            out["hurst_rs"][f"m{m}"] = v
            out["hurst_rs"][f"m{m}_blocks"] = cnt
            if v is not None and np.isfinite(v) and v > 0:
                xs.append(np.log(m))
                ys.append(np.log(v))
        out["hurst_rs"]["fitted"] = float(np.polyfit(xs, ys, 1)[0]) \
            if len(xs) >= 3 else float("nan")
    else:
        out["hurst_rs"]["fitted"] = None
    return out


# --------------------------------------------------------------------------- #
def shock_analysis(d, k):
    """3-sigma shock detection + descriptive recovery / clustering. Shocks are
    NEVER removed from the sample: this is a parallel descriptive block."""
    c = d["c"]
    n = len(c)
    valid = (d["contig"][1:] == 1)
    with np.errstate(divide="ignore", invalid="ignore"):
        r = np.diff(np.log(c))
    m = max(2, int(round(SHOCK_SIGMA_MIN / k)))
    if m >= len(r):
        return {"error": "window longer than series"}
    s = rolling_std(r, m)
    ok = np.isfinite(s) & (s > 0)
    z = np.full(len(r), np.nan)
    z[ok] = r[ok] / s[ok]
    is_shock = np.zeros(len(r), dtype=bool)
    is_shock[ok] = (np.abs(r[ok]) > SHOCK_K * s[ok])

    idx = np.flatnonzero(is_shock)
    n_years = 16.663
    out = {
        "sigma_window_min": SHOCK_SIGMA_MIN, "sigma_bars": int(m),
        "k_sigma": SHOCK_K, "n_shocks": int(idx.size),
        "shock_rate_per_bar": float(idx.size / max(n - m, 1)),
        "shocks_per_year": float(idx.size / n_years),
        "sigma_defined_bars": int(ok.sum()),
        "never_removed": True,
    }
    if idx.size == 0:
        return out
    mag = np.abs(r[idx])
    out["magnitude_bps"] = {**moments(mag * 1e4), **q(mag * 1e4)}
    out["magnitude_usd"] = {
        "median": float(np.median(np.abs(c[idx + 1] - c[idx]))),
        "mean": float(np.mean(np.abs(c[idx + 1] - c[idx]))),
        "p90": float(np.percentile(np.abs(c[idx + 1] - c[idx]), 90)),
    }
    out["z_score"] = {**moments(np.abs(z[idx]))}
    # clustering: share of shocks followed by another shock within 5 bars
    fwd = np.zeros(idx.size, dtype=bool)
    for j in range(1, 6):
        nxt = idx + j
        okj = nxt < len(r)
        fwd[okj] |= is_shock[nxt[okj]]
    out["clustering_shock_within_5"] = float(fwd.mean())
    out["clustering_baseline_rate"] = float(idx.size / len(r))
    gaps = np.diff(idx)
    out["intershock_gap_bars"] = {**moments(gaps.astype(float)), **q(gaps.astype(float))}
    # conditional mean gap vs unconditional expectation
    out["clustering_ratio"] = float(out["intershock_gap_bars"]["mean"] *
                                    out["clustering_baseline_rate"])
    # recovery / reversion after a shock (descriptive, no position taken)
    for hh in (5, 20):
        disp = np.full(idx.size, np.nan)
        rev = np.full(idx.size, np.nan)
        for a, i in enumerate(idx):
            j = i + 1
            if j + hh >= n:
                continue
            disp[a] = (c[j + hh] - c[j]) / c[j]
            rev[a] = -(c[j + hh] - c[j]) * np.sign(r[i]) / c[j]
        out[f"mean_abs_displacement_after_{hh}_bps"] = float(
            np.nanmean(np.abs(disp)) * 1e4)
        out[f"mean_reversion_after_{hh}_bps"] = float(np.nanmean(rev) * 1e4)
        out[f"reversion_sign_positive_share_{hh}"] = float(
            np.nanmean(rev > 0))
    # persistence: does the shock direction continue?
    cont = np.full(idx.size, np.nan)
    for a, i in enumerate(idx):
        j = i + 1
        if j + 5 >= n:
            continue
        cont[a] = np.sign(c[j + 5] - c[j]) == np.sign(r[i])
    out["direction_persistence_after_5"] = float(np.nanmean(cont))
    return out


# --------------------------------------------------------------------------- #
#  CONTINUITY CARTOGRAPHY (section 14)
# --------------------------------------------------------------------------- #
def continuity_block(d, k, years):
    """Precise mapping of interruptions. Nothing is filled."""
    n = len(d["c"])
    im, ib, nm1 = d["im"], d["ib"], d["n_m1"]
    valid = (d["contig"][1:] == 1)
    years_full = years[1:] if len(years) == len(d["c"]) else years
    res = {
        "bars": int(n),
        "bars_with_internal_data_gap": int((im > 0).sum()),
        "pct_bars_with_internal_data_gap": float(np.mean(im > 0) * 100),
        "bars_with_internal_market_break": int((ib > 0).sum()),
        "pct_bars_with_internal_market_break": float(np.mean(ib > 0) * 100),
        "incomplete_windows": int(((nm1 < k) & (im == 0)).sum()),
        "pct_incomplete_windows": float(np.mean((nm1 < k) & (im == 0)) * 100),
        "total_missing_minutes": float(np.sum(im)),
        "mean_missing_min_per_bar": float(np.mean(im)),
        "p99_missing_min_per_bar": float(np.percentile(im, 99)),
        "max_missing_min_per_bar": float(np.max(im)),
        "non_contiguous_steps": int((~valid).sum()),
        "pct_non_contiguous_steps": float(np.mean(~valid) * 100),
        "missing_min_distribution": q(im.astype(float), (50, 75, 90, 95, 99)),
    }
    # interruption lengths in minutes, on the affected bars only
    mi = im[im > 0].astype(float)
    if mi.size > 30:
        res["gap_len_minutes_when_present"] = {**moments(mi), **q(mi)}
    # per-year incidence
    per_year = {}
    uy = np.unique(years)
    for y in uy:
        sel = years == y
        if sel.sum() < 50:
            continue
        per_year[str(int(y))] = {
            "bars": int(sel.sum()),
            "pct_internal_gap": float(np.mean(im[sel] > 0) * 100),
            "pct_market_break": float(np.mean(ib[sel] > 0) * 100),
            "pct_incomplete": float(np.mean((nm1[sel] < k) & (im[sel] == 0)) * 100),
            "missing_min": float(np.sum(im[sel])),
            "pct_non_contiguous": float(np.mean(d["contig"][sel][1:] != 1) * 100),
        }
    res["per_year"] = per_year
    return res


# --------------------------------------------------------------------------- #
#  SHOCK AGGREGATION M1 -> M3 -> H1 (section 16)
# --------------------------------------------------------------------------- #
def shock_aggregation(m1, m3, h1, idx_shock, top_n=SHOCK_TOP_N):
    m1_min = m1["ts"].astype("datetime64[m]").astype("int64")
    c = m1["c"]
    o1 = m1["o"]
    n = len(c)
    with np.errstate(divide="ignore", invalid="ignore"):
        r = np.diff(np.log(c))
    cumabs = np.concatenate(([0.0], np.cumsum(np.abs(np.diff(c)))))
    # order by magnitude of the M1 move, keep the largest
    order = idx_shock[np.argsort(-np.abs(r[idx_shock]))][:top_n]

    rid3 = m1_min // 3
    rid60 = m1_min // 60
    m3_id = m3["ts"].astype("datetime64[m]").astype("int64") // 3
    h1_id = h1["ts"].astype("datetime64[m]").astype("int64") // 60

    rows = []
    for rank, i in enumerate(order, 1):
        if i + 1 >= n:
            continue
        mag_usd = float(abs(c[i + 1] - c[i]))
        rec = {
            "SHOCK_ID": f"S{rank:03d}",
            "UTC": str(m1["ts"][i + 1])[:19],
            "M1_MAGNITUDE_USD": mag_usd,
            "M1_MAGNITUDE_BPS": float(abs(r[i]) * 1e4),
        }
        for label, rid, tf_d, tf_id, kk in (("M3", rid3, m3, m3_id, 3),
                                            ("H1", rid60, h1, h1_id, 60)):
            key = rid[i + 1]
            pos = int(np.searchsorted(tf_id, key))
            if pos >= len(tf_d["c"]) or tf_id[pos] != key:
                rec.update({f"{label}_MAGNITUDE_USD": None,
                            f"{label}_RANGE_USD": None,
                            f"{label}_BODY_USD": None,
                            f"{label}_TIMING_PRESERVED": None,
                            f"{label}_TIMING_LOST": None,
                            f"{label}_LAG_MIN": None,
                            f"{label}_STRUCT_LOST": None})
                continue
            bar_o = tf_d["o"][pos]
            bar_c = tf_d["c"][pos]
            body = float(abs(bar_c - bar_o))
            rng = float(tf_d["h"][pos] - tf_d["l"][pos])
            # first / last M1 index inside the aggregated bar
            a = int(np.searchsorted(rid, key, side="left"))
            b = int(np.searchsorted(rid, key, side="right")) - 1
            path = float(cumabs[b] - cumabs[a]) if b > a else 0.0
            net = float(abs(c[b] - c[a])) if b > a else 0.0
            struct_lost = float(1.0 - net / path) if path > 0 else 0.0
            at_open = (m1_min[i + 1] % kk) == 0
            rec.update({
                f"{label}_MAGNITUDE_USD": body,
                f"{label}_RANGE_USD": rng,
                f"{label}_BODY_USD": body,
                f"{label}_TIMING_PRESERVED": bool(at_open),
                f"{label}_TIMING_LOST": bool(not at_open),
                f"{label}_LAG_MIN": float(m1_min[b] - m1_min[i + 1]),
                f"{label}_STRUCT_LOST": struct_lost,
            })
        # overall verdict
        lost = []
        if rec.get("M3_TIMING_LOST"):
            lost.append("M3 timing")
        if rec.get("H1_TIMING_LOST"):
            lost.append("H1 timing")
        m3s = rec.get("M3_STRUCT_LOST")
        h1s = rec.get("H1_STRUCT_LOST")
        if m3s is not None and m3s > 0.5:
            lost.append("M3 intrabar path")
        if h1s is not None and h1s > 0.9:
            lost.append("H1 intrabar path")
        rec["STRUCTURAL_INFORMATION_LOST"] = "; ".join(lost) if lost else "none"
        rec["VISIBLE_IN_M3"] = bool(rec.get("M3_MAGNITUDE_USD") is not None)
        rec["VISIBLE_IN_H1"] = bool(rec.get("H1_MAGNITUDE_USD") is not None)
        rows.append(rec)
    return rows


# --------------------------------------------------------------------------- #
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tfdir", default="/tmp/xauusd_audit/timeframes")
    ap.add_argument("--out", default="/tmp/xauusd_audit/deep_metrics.json")
    a = ap.parse_args()

    out = {
        "spec": {
            "timeframes": TF, "minutes": K,
            "volatility_windows_min": list(VW_MIN),
            "session_windows": [{"name": n, "start_utc": s, "end_utc": e}
                                for n, s, e in SESSION_WINDOWS],
            "shock_rule": {"sigma_window_min": SHOCK_SIGMA_MIN,
                           "k_sigma": SHOCK_K,
                           "measure": "|log return of one bar| > k * trailing "
                                      "rolling std of the same series"},
            "hurst_lags_bars": list(HURST_LAGS),
            "hurst_estimators": ["VR-implied (log VR(q) on log q, slope=2H-1)",
                                 "classical rescaled range R/S"],
            "cost_scenarios": COST_SCENARIOS,
            "cost_domination_pct": list(COST_DOMINATION_PCT),
            "acf_lags": list(ACF_LAGS),
            "vol_class_rule": "HIGH_VOL if trailing 1440-min sigma > trailing "
                              "1-year mean of that sigma (both past-only)",
            "broker_cost_status": "EXTERNAL_INPUT_REQUIRED",
            "volume_used": False, "gaps_filled": False,
            "extremes_removed": False, "regime_built": False,
            "strategy_tested": False,
        },
        "timeframes": {}, "hurst": {}, "continuity": {},
        "shocks": {}, "shock_aggregation": [], "discrimination": {},
    }

    data = {}
    for t in TF:
        print(f"--- loading {t}", flush=True)
        d = load(os.path.join(a.tfdir, f"XAUUSD_{t}.parquet"))
        d["years"] = d["ts"].astype("datetime64[Y]").astype(int) + 1970
        d["hour"] = (d["ts"].astype("datetime64[h]").astype("int64") % 24)
        data[t] = d

    for t in TF:
        print(f"=== {t}", flush=True)
        d = data[t]
        k = K[t]
        years = d["years"]
        n = len(d["c"])
        span = 16.663
        blk = base_block(d, k)
        blk["span_years"] = span
        print("  base done", flush=True)

        # ---- persistence / Hurst ------------------------------------------
        valid = (d["contig"][1:] == 1)
        with np.errstate(divide="ignore", invalid="ignore"):
            r = np.diff(np.log(d["c"]))
        blk["persistence"] = persistence_block(d, r, valid)
        print("  persistence done", flush=True)

        # ---- vol classes (past-only) --------------------------------------
        m = max(2, int(round(SHOCK_SIGMA_MIN / k)))
        sig = rolling_std(r, m)
        bars_per_year = n / span
        sig_series = np.concatenate(([np.nan], sig))   # align to bars
        rm = rolling_mean(np.nan_to_num(sig_series), int(bars_per_year))
        cls = np.full(n, -1, dtype="int8")
        okv = np.isfinite(sig_series) & np.isfinite(rm)
        cls[okv & (sig_series > rm)] = 1               # HIGH_VOL
        cls[okv & (sig_series <= rm)] = 0              # LOW_VOL
        blk["vol_class_share"] = {
            "HIGH_VOL": float(np.mean(cls == 1)),
            "LOW_VOL": float(np.mean(cls == 0)),
            "UNCLASSIFIED": float(np.mean(cls == -1)),
        }

        # ---- splits --------------------------------------------------------
        blk["by_year"] = {}
        for y in sorted(set(years.tolist())):
            sel = np.flatnonzero(years == y)
            if len(sel) < 200:
                continue
            blk["by_year"][str(y)] = base_block(subset(d, sel), k)

        blk["by_session"] = {}
        for nm, h0, h1_ in SESSION_WINDOWS:
            sel = np.flatnonzero((d["hour"] >= h0) & (d["hour"] < h1_))
            if len(sel) < 200:
                continue
            b = base_block(subset(d, sel), k)
            # white-noise benchmark interval for ACF: +/- 1.96 / sqrt(n)
            for lag in ACF_LAGS:
                nn = b["acf"].get(f"lag{lag}_n", 0)
                v = b["acf"].get(f"lag{lag}")
                if v is not None and np.isfinite(v) and nn and nn > 0:
                    hw = 1.96 / np.sqrt(nn)
                    b["acf"][f"lag{lag}_ci_lo"] = v - hw
                    b["acf"][f"lag{lag}_ci_hi"] = v + hw
            blk["by_session"][nm] = b

        blk["by_volclass"] = {}
        for nm, cv in (("HIGH_VOL", 1), ("LOW_VOL", 0)):
            sel = np.flatnonzero(cls == cv)
            if len(sel) < 200:
                continue
            blk["by_volclass"][nm] = base_block(subset(d, sel), k)

        for nm, sel in (("pre2013", np.flatnonzero(years <= 2012)),
                        ("post2013", np.flatnonzero((years >= 2013) & (years <= 2025))),
                        ("y2026", np.flatnonzero(years == 2026))):
            if len(sel) < 200:
                continue
            blk[nm] = base_block(subset(d, sel), k)

        # ---- shocks --------------------------------------------------------
        blk["shocks"] = shock_analysis(d, k)
        print("  shocks done", flush=True)

        out["timeframes"][t] = blk
        out["continuity"][t] = continuity_block(d, k, d["years"])
        out["hurst"][t] = {
            "vr": blk["persistence"]["vr"],
            "hurst_vr": blk["persistence"]["hurst_vr"],
            "hurst_rs": blk["persistence"]["hurst_rs"],
            "by_year": {}, "by_volclass": {},
        }
        # Hurst stability: per year and per vol class
        for y in sorted(blk["by_year"]):
            sel = np.flatnonzero(years == int(y))
            if len(sel) < 500:
                continue
            sd = subset(d, sel)
            with np.errstate(divide="ignore", invalid="ignore"):
                rr = np.diff(np.log(sd["c"]))
            vv = (sd["contig"][1:] == 1)
            out["hurst"][t]["by_year"][y] = persistence_block(
                sd, rr, vv, rs=False)["hurst_vr"]
        for nm, cv in (("HIGH_VOL", 1), ("LOW_VOL", 0)):
            sel = np.flatnonzero(cls == cv)
            if len(sel) < 500:
                continue
            sd = subset(d, sel)
            with np.errstate(divide="ignore", invalid="ignore"):
                rr = np.diff(np.log(sd["c"]))
            vv = (sd["contig"][1:] == 1)
            out["hurst"][t]["by_volclass"][nm] = persistence_block(
                sd, rr, vv, rs=False)["hurst_vr"]
        print("  hurst done", flush=True)

    # ---- shock aggregation -------------------------------------------------
    print("=== shock aggregation", flush=True)
    d1 = data["M1"]
    valid1 = (d1["contig"][1:] == 1)
    with np.errstate(divide="ignore", invalid="ignore"):
        r1 = np.diff(np.log(d1["c"]))
    s1 = rolling_std(r1, SHOCK_SIGMA_MIN)
    ok1 = np.isfinite(s1) & (s1 > 0)
    is_shock = np.zeros(len(r1), dtype=bool)
    is_shock[ok1] = np.abs(r1[ok1]) > SHOCK_K * s1[ok1]
    idx = np.flatnonzero(is_shock)
    out["shocks"]["M1_index_count"] = int(idx.size)
    out["shock_aggregation"] = shock_aggregation(d1, data["M3"], data["H1"], idx)

    # ---- M1 vs M3 discrimination (paired by year) ---------------------------
    print("=== discrimination", flush=True)
    METRICS = [
        ("acf_lag1", lambda b: b["acf"]["lag1"]),
        ("acf_lag2", lambda b: b["acf"]["lag2"]),
        ("acf_lag3", lambda b: b["acf"]["lag3"]),
        ("acf_lag4", lambda b: b["acf"]["lag4"]),
        ("acf_lag5", lambda b: b["acf"]["lag5"]),
        ("sign_change_freq", lambda b: b["sign_change_freq"]),
        ("excess_kurtosis", lambda b: b["returns"]["excess_kurtosis"]),
        ("median_range_bps", lambda b: b["amplitude_bps"]["range"]["median"]),
        ("p90_range_bps", lambda b: b["amplitude_bps"]["range"]["p90"]),
        ("median_range_usd", lambda b: b["amplitude_usd"]["range"]["median"]),
        ("range_over_sigma_w1440_median",
         lambda b: b["vol_normalised"].get("w1440", {})
         .get("range_over_sigma", {}).get("p50", float("nan"))),
        ("body_over_range", lambda b: b["shape"]["mean_body_over_range"]),
        ("de_h10", lambda b: b["de"]["h10"]),
        ("contiguous_step_rate", lambda b: b["integrity"]["contiguous_step_rate"]),
        ("pct_internal_gap", lambda b: b["integrity"]["bars_with_internal_data_gap"]),
    ]
    disc = {}
    yrs = [y for y in out["timeframes"]["M1"]["by_year"] if y != "2026"]
    for name, fn in METRICS:
        d_ = []
        for y in yrs:
            try:
                v1 = fn(out["timeframes"]["M1"]["by_year"][y])
                v3 = fn(out["timeframes"]["M3"]["by_year"][y])
            except Exception:
                continue
            if v1 is None or v3 is None:
                continue
            if not (np.isfinite(v1) and np.isfinite(v3)):
                continue
            d_.append(v3 - v1)
        d_ = np.array(d_, dtype=float)
        if d_.size < 6:
            disc[name] = {"n_years": int(d_.size), "status": "INSUFFICIENT"}
            continue
        m_ = float(d_.mean())
        sd = float(d_.std(ddof=1))
        se = sd / np.sqrt(d_.size)
        pos = float(np.mean(d_ > 0))
        disc[name] = {
            "n_years": int(d_.size),
            "mean_diff_M3_minus_M1": m_,
            "sd_across_years": sd,
            "se_of_mean_diff": float(se),
            "ci95_lo": float(m_ - 1.96 * se),
            "ci95_hi": float(m_ + 1.96 * se),
            "share_years_M3_greater": pos,
            "sign_consistency": float(max(pos, 1 - pos)),
            "effect_vs_year_noise": float(abs(m_) / sd) if sd > 0 else float("nan"),
            "excludes_zero_95ci": bool((m_ - 1.96 * se) * (m_ + 1.96 * se) > 0),
        }
    out["discrimination"] = disc

    with open(a.out, "w") as fh:
        json.dump(out, fh, indent=1, default=_jd)
    print("written", a.out, flush=True)


def _jd(o):
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        v = float(o)
        return None if not np.isfinite(v) else v
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    raise TypeError(str(type(o)))


if __name__ == "__main__":
    main()
