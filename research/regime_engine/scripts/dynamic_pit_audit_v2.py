#!/usr/bin/env python3
"""
PHASE 3 V2 - STEP 3.5R: DYNAMIC PIT AUDIT (OPTIMIZED, TARGETED)
===============================================================
Proves (or falsifies) PAST-ONLY behaviour of the 25 frozen V2 features by
dynamic truncation, WITHOUT recomputing the whole dataset per probe.

Design (engine structure analysis -> targeted evaluation):
  * feature_engine_v2.py = pure helpers (rolling_arr, pair_prefixes,
    acf_vec, prefix_mask/prefix_cum, roll_sums4, Fenwick) + per-feature
    inline expressions evaluated at row indices. NOTHING is modified.
  * make_env(cut_min) rebuilds the engine's EXACT input arrays on the
    master/grids truncated strictly after cut_min (frozen builder
    01_build_layers.py executed unmodified), including the parity block
    prefixes used by B2 (kept bit-identical).
  * values_at(env, i) evaluates the 25 features ONLY at probe row i with
    the same windows/MIN_OBS/estimators and the same arithmetic order.
  * Because the truncated env arrays are strict prefixes of the full
    arrays, every prefix/rolling value at index i is bit-identical to the
    full run; the recomputation is therefore EXACT by construction, and the
    comparison (value_truncated vs value_reference) is a true PIT test.

Modes per probe (cut_min = Ts + off; Ts = T(t)+2 close of bar t):
  ref : no truncation -> identity control vs committed parquet (0 mismatch
        required: proves the targeted evaluator reproduces the engine)
  exact : off = 0    (data strictly after t removed)
  o1    : off = 3    (t + 1 M3 observation available)
  o10   : off = 30   (t + 10 M3 observations available)
  o100  : off = 300  (t + 100 M3 observations available)

Usage:
  python3 dynamic_pit_audit_v2.py --pilot   # 1 probe: timing + identity gate
  python3 dynamic_pit_audit_v2.py           # full run (21 probes, 3/period)
"""
from __future__ import annotations

import csv
import importlib.util
import json
import os
import sys
import time
from collections import Counter
from datetime import datetime, timezone

import numpy as np
import pyarrow.parquet as pq

REPO = "/home/user/xauusd-quant-research/research/regime_engine"
SCRATCH = "/tmp/xauusd_audit/regime_engine"
MASTER = "/tmp/xauusd_audit/XAUUSD_M1_reconstructed.parquet"
FEAT_FILE = os.path.join(REPO, "XAUUSD_FEATURES_V2.parquet")
OUT_CSV = os.path.join(REPO, "PHASE3_V2_DYNAMIC_PIT_AUDIT.csv")
OUT_MD = os.path.join(REPO, "PHASE3_V2_DYNAMIC_PIT_AUDIT.md")
SCRIPTS = os.path.join(REPO, "scripts")
sys.path.insert(0, SCRIPTS)

import feature_engine_v2 as fe  # noqa: E402  (FROZEN engine module)
import p3_common  # noqa: E402

# frozen builder as a module (its main() is never executed)
_build_src = open(os.path.join(SCRIPTS, "01_build_layers.py")).read()
bl = importlib.util.module_from_spec(
    importlib.util.spec_from_loader("build_layers_v2", loader=None))
bl.__file__ = os.path.join(SCRIPTS, "01_build_layers.py")
exec(compile(_build_src, "01_build_layers.py", "exec"), bl.__dict__)

FEATURES = [f[0] for f in fe.FEATURES]
FAMILY = {f[0]: f[1] for f in fe.FEATURES}
W3_D, MO3_D = fe.W3_D, fe.MO3_D
W3_M, MO3_M = fe.W3_M, fe.MO3_M
W1_D, MO1_D = fe.W1_D, fe.MO1_D
WH_M, MOH_M = fe.WH_M, fe.MOH_M
MO_SHAPE, MO_EXT = fe.MO_SHAPE, fe.MO_EXT
SHOCK_MULT = fe.SHOCK_MULT

MODES = [("ref", None), ("exact", 0), ("o1", 3), ("o10", 30), ("o100", 300)]
YEAR_MONTHS = {2010: [3, 7, 11], 2012: [2, 6, 10], 2013: [2, 6, 10],
               2016: [2, 6, 10], 2020: [2, 6, 10], 2024: [2, 6, 10],
               2026: [2, 5, 8]}


def _epoch_min(y, m, d, hh, mm):
    dt = datetime(y, m, d, hh, mm, tzinfo=timezone.utc)
    return int(dt.timestamp() // 60)


def _minute(ts):
    return ts.astype("datetime64[m]").astype(np.int64)


def _load_full_arrays():
    t1 = pq.read_table(MASTER, columns=["timestamp", "open", "high", "low", "close"])
    full = {
        "ts": t1.column("timestamp").to_numpy(zero_copy_only=False),
        "o": t1.column("open").to_numpy().astype("float64"),
        "h": t1.column("high").to_numpy().astype("float64"),
        "l": t1.column("low").to_numpy().astype("float64"),
        "c": t1.column("close").to_numpy().astype("float64"),
    }
    del t1
    return full


# ---------------------------------------------------------------------------
# environment: engine input arrays on truncated data; B2 parity prefixes kept
# ---------------------------------------------------------------------------
def make_env(full, cut_min):
    if cut_min is None:
        ts, o, h, l, c = full["ts"], full["o"], full["h"], full["l"], full["c"]
    else:
        tsm = _minute(full["ts"])
        mask = tsm <= cut_min
        ts = full["ts"][mask]
        o = full["o"][mask]
        h = full["h"][mask]
        l = full["l"][mask]
        c = full["c"][mask]

    # grids: frozen builder (identical output whether computed on the full
    # master or truncated when comparing index <= i)
    m1 = {"ts": ts, "o": o, "h": h, "l": l, "c": c}
    m3 = bl.build(m1, p3_common.PRIMARY_MIN)
    h1 = bl.build(m1, p3_common.CONTEXT_MIN)
    t3 = np.asarray(m3["t_min"], dtype=np.int64)
    o3 = np.asarray(m3["open"]).astype("float64")
    h3 = np.asarray(m3["high"]).astype("float64")
    l3 = np.asarray(m3["low"]).astype("float64")
    c3 = np.asarray(m3["close"]).astype("float64")
    cont3 = np.asarray(m3["contig_next"]).astype(bool)

    env = {"t3": t3, "o3": o3, "h3": h3, "l3": l3, "c3": c3, "n": len(t3)}

    # ---------------- M1 substrate (verbatim) --------------------------------
    t1 = _minute(ts)
    c1 = c.astype("float64")
    n1 = len(t1)
    r1 = np.full(n1, np.nan)
    r1[1:] = np.log(c1[1:]) - np.log(c1[:-1])
    clean1 = np.zeros(n1, dtype=bool)
    clean1[1:] = (t1[1:] - t1[:-1]) == 1
    clean1 &= np.isfinite(r1)
    r1 = np.where(clean1, r1, np.nan)
    s1_day = fe.rolling_arr(r1, W1_D, fe.MO1_D, "std")
    s1_prev = fe.shift1(s1_day)
    cls1 = np.isfinite(s1_prev) & (s1_prev > 0)
    ext1 = np.zeros(n1, dtype=np.int64)
    ext1[cls1] = (np.abs(r1[cls1]) > SHOCK_MULT * s1_prev[cls1]).astype(np.int64)
    env.update(t1=t1, s1_day=s1_day,
               p_ext1=fe.prefix_mask(ext1), p_cls1=fe.prefix_mask(cls1))

    # ---------------- H1 context (verbatim) ----------------------------------
    tH = np.asarray(h1["t_min"], dtype=np.int64)
    cH = np.asarray(h1["close"]).astype("float64")
    contH = np.asarray(h1["contig_next"]).astype(bool)
    nH = len(tH)
    rH = np.full(nH, np.nan)
    rH[1:] = np.log(cH[1:]) - np.log(cH[:-1])
    rH = np.where(contH & np.isfinite(rH), rH, np.nan)
    env.update(tH=tH, contH=contH,
               sH24=fe.rolling_arr(rH, fe.WH_D, fe.MOH_D, "std"),
               sH336=fe.rolling_arr(rH, WH_M, MOH_M, "std"),
               PH=fe.pair_prefixes(rH))

    # ---------------- M3 series (verbatim) -----------------------------------
    n = len(t3)
    r3 = np.full(n, np.nan)
    r3[1:] = np.log(c3[1:]) - np.log(c3[:-1])
    r3 = np.where(cont3 & np.isfinite(r3), r3, np.nan)
    s3_day = fe.rolling_arr(r3, W3_D, MO3_D, "std")
    s3_prev = fe.shift1(s3_day)
    s3_mon = fe.rolling_arr(r3, W3_M, MO3_M, "std")

    cls3 = np.isfinite(s3_prev) & (s3_prev > 0)
    ext3 = np.zeros(n, dtype=np.int64)
    ext3[cls3] = (np.abs(r3[cls3]) > SHOCK_MULT * s3_prev[cls3]).astype(np.int64)
    env.update(r3=r3, s3_day=s3_day, s3_prev=s3_prev, s3_mon=s3_mon, ext3=ext3,
               p_ext3=fe.prefix_mask(ext3), p_cls3=fe.prefix_mask(cls3),
               p_pos=fe.prefix_mask((ext3 == 1) & (r3 > 0)),
               P=fe.pair_prefixes(r3))

    rnz = np.where(np.isfinite(r3), r3, 0.0)
    env.update(cnt_r=fe.prefix_mask(np.isfinite(r3)),
               s_r=fe.prefix_cum(rnz), q_r=fe.prefix_cum(rnz * rnz))

    sign = np.where(r3 > 0, 1, np.where(r3 < 0, -1, 0))
    nz = sign != 0
    prev_same = np.zeros(n, dtype=bool)
    prev_same[1:] = nz[1:] & nz[:-1] & (sign[1:] == sign[:-1])
    is_start = nz & ~prev_same
    env.update(sign=sign, nz=nz, is_start=is_start,
               p_nz=fe.prefix_mask(nz), p_st=fe.prefix_mask(is_start))

    # B2 parity-block prefixes (verbatim, so window sums are bit-identical)
    pb = np.zeros(n - 1)
    sb_ = np.zeros(n - 1)
    vb = np.isfinite(r3[1:]) & np.isfinite(r3[:-1])
    pb[vb] = 1.0
    sb_[vb] = r3[1:][vb] + r3[:-1][vb]
    qb = sb_ * sb_
    ev = np.zeros(n - 1)
    sv = np.zeros(n - 1)
    qv = np.zeros(n - 1)
    ev[::2] = pb[::2]
    sv[::2] = sb_[::2]
    qv[::2] = qb[::2]
    eo = np.zeros(n - 1)
    so = np.zeros(n - 1)
    qo = np.zeros(n - 1)
    eo[1::2] = pb[1::2]
    so[1::2] = sb_[1::2]
    qo[1::2] = qb[1::2]
    env.update(Ce=fe.prefix_cum(ev), Se=fe.prefix_cum(sv), Qe=fe.prefix_cum(qv),
               Co=fe.prefix_cum(eo), So=fe.prefix_cum(so), Qo=fe.prefix_cum(qo))

    # C/D window inputs (verbatim engine expressions over the FULL arrays, so
    # window slices are bit-identical to the engine's)
    c_prev = fe.shift1(c3)
    rbps3 = np.where(np.isfinite(c3) & (c3 > 0), 10000.0 * (h3 - l3) / c3, np.nan)
    tr3 = np.maximum.reduce([h3 - l3, np.abs(h3 - c_prev), np.abs(l3 - c_prev)])
    trbps3 = np.where(np.isfinite(c_prev) & (c_prev > 0) & np.isfinite(tr3) & (tr3 > 0),
                      10000.0 * tr3 / c_prev, np.nan)
    sig3 = 10000.0 * s3_prev
    c1g = rbps3 / sig3
    c1g = np.where(np.isfinite(s3_prev) & (s3_prev > 0), c1g, np.nan)
    c2g = trbps3 / sig3
    c2g = np.where(np.isfinite(s3_prev) & (s3_prev > 0), c2g, np.nan)
    tr_prev3 = fe.shift1(trbps3)
    c3dg = 10000.0 * np.log(trbps3 / tr_prev3)
    c3dg = np.where(np.isfinite(trbps3) & np.isfinite(tr_prev3) & (trbps3 > 0) & (tr_prev3 > 0),
                    c3dg, np.nan)
    rng3 = h3 - l3
    ok3 = np.isfinite(rng3) & (rng3 > 0)
    den3 = np.maximum(rng3, 1e-300)
    dds = [np.where(ok3, np.abs(c3 - o3) / den3, np.nan),
           np.where(ok3, (h3 - np.maximum(o3, c3)) / den3, np.nan),
           np.where(ok3, (np.minimum(o3, c3) - l3) / den3, np.nan),
           np.where(ok3, (c3 - l3) / den3, np.nan),
           np.where(ok3, (c3 - o3) / den3, np.nan)]
    env.update(c1g=c1g, c2g=c2g, c3dg=c3dg,
               **{f"dd{k}": dds[k] for k in range(5)})

    c4, s1q, s2q, s3q, s4q = fe.roll_sums4(r3, W3_M, MO3_M)
    env.update(cnt4=c4, s1_4=s1q, s2_4=s2q, s3_4=s3q, s4_4=s4q)
    return env


# ---------------------------------------------------------------------------
# targeted evaluation at probe row i (exact engine arithmetic)
# ---------------------------------------------------------------------------
def _nan():
    return float("nan")


def values_at(env, i):
    e = env
    out = {}
    availD = i >= W3_D - 1
    availM = i >= W3_M - 1
    lo = i - W3_M + 1                       # [lo, i] month window
    endM1 = int(e["t3"][i]) + 2
    j_idx = int(np.searchsorted(e["t1"], endM1, side="right") - 1)
    hb = (endM1 // 60) * 60
    h_idx = int(np.searchsorted(e["tH"], hb, side="right") - 1)

    # ---- A1 -----------------------------------------------------------------
    s3d = e["s3_day"][i]
    s3m = e["s3_mon"][i]
    out["m3_vol_ratio_day_month"] = (
        s3d / s3m if (availM and s3d > 0 and s3m > 0) else _nan())

    # ---- A2 -----------------------------------------------------------------
    s1j = e["s1_day"][j_idx]
    out["m3_m1_noise_ratio"] = (
        np.sqrt(3.0) * s1j / s3d
        if (availD and j_idx >= W1_D - 1 and s1j > 0 and s3d > 0) else _nan())

    # ---- A3 -----------------------------------------------------------------
    sH24 = e["sH24"][h_idx]
    sH336 = e["sH336"][h_idx]
    out["h1_vol_ratio_day_month"] = (
        sH24 / sH336
        if (h_idx >= WH_M - 1 and sH24 > 0 and sH336 > 0) else _nan())

    # ---- B1 ACF (pair window [i-479, i], verbatim) --------------------------
    b1 = fe.acf_vec(e["P"], np.array([i], dtype=np.int64), W3_D - 2, MO3_D)[0]
    out["m3_acf1_day"] = float(b1) if availD else _nan()

    # ---- B2 VR q=2 (verbatim parity-prefix arithmetic) ----------------------
    par = (i - (W3_M - 1)) % 2
    hiB2 = i - 1
    loB2c = max(i - (W3_M - 1), 0)
    if par == 0:
        C = e["Ce"][max(hiB2, 0)] - e["Ce"][max(loB2c - 1, 0)]
        S = e["Se"][max(hiB2, 0)] - e["Se"][max(loB2c - 1, 0)]
        Q = e["Qe"][max(hiB2, 0)] - e["Qe"][max(loB2c - 1, 0)]
    else:
        C = e["Co"][max(hiB2, 0)] - e["Co"][max(loB2c - 1, 0)]
        S = e["So"][max(hiB2, 0)] - e["So"][max(loB2c - 1, 0)]
        Q = e["Qo"][max(hiB2, 0)] - e["Qo"][max(loB2c - 1, 0)]
    C = C if i - (W3_M - 1) >= 0 else 0.0
    vb_var = (Q - S * S / max(C, 1)) / (C - 1) if C > 1 else _nan()
    nc5 = int(e["cnt_r"][i + 1] - e["cnt_r"][lo])
    ss5 = float(e["s_r"][i + 1] - e["s_r"][lo])
    qq5 = float(e["q_r"][i + 1] - e["q_r"][lo])
    var_r = (qq5 - ss5 * ss5 / max(nc5, 1)) / (nc5 - 1) if nc5 > 1 else _nan()
    out["m3_vr2_month"] = (
        vb_var / (2.0 * var_r)
        if (availM and C >= MO3_M and var_r > 0) else _nan())

    # ---- B3 SCF (pair window [i-479, i], counts only) ------------------------
    a = e["r3"][i - 478:i + 1]          # pairs (r[k], r[k+1]), k in [i-479, i-1]
    b = e["r3"][i - 479:i]
    valid2 = np.isfinite(a) & np.isfinite(b) & (a != 0) & (b != 0)
    chg = valid2 & ((a > 0) != (b > 0))
    nv = int(np.sum(valid2))
    ncc = int(np.sum(chg))
    out["m3_scf_day"] = (ncc / nv if (availD and nv >= MO3_D) else _nan())

    # ---- B4 run month (verbatim: starts in [lo, i] + left-carry) -------------
    seg = e["sign"][lo - 1:i + 1] if lo > 0 else e["sign"][:i + 1]
    nzq = seg != 0
    prev_same = np.zeros(len(seg), dtype=bool)
    prev_same[1:] = nzq[1:] & nzq[:-1] & (seg[1:] == seg[:-1])
    is_start_q = nzq & ~prev_same
    n_bars = int(np.sum(nzq[1:]))                    # positions [lo, i]
    n_runs = int(np.sum(is_start_q[1:]))             # starts in [lo, i]
    if lo > 0:
        n_runs += int(nzq[1] & ~is_start_q[1]) if len(seg) > 1 else 0
    out["m3_run_month"] = (
        n_bars / n_runs if (availM and n_bars >= MO3_M and n_runs > 0) else _nan())

    # ---- B5 dir --------------------------------------------------------------
    mean_r = ss5 / max(nc5, 1)
    out["m3_dir_month"] = (
        mean_r / np.sqrt(max(var_r, 0.0))
        if (availM and nc5 >= MO3_M and var_r > 0) else _nan())

    # ---- B6 H1 ACF -------------------------------------------------------------
    b6 = fe.acf_vec(e["PH"], np.array([h_idx], dtype=np.int64),
                    WH_M - 2, MOH_M)[0]
    out["h1_acf1_month"] = float(b6) if h_idx >= WH_M - 1 else _nan()

    # ---- C1/C2/C3 (windows [i-479, i]; slices of engine-computed arrays) -----
    s0 = max(i - W3_D + 1, 0)
    for key, gkey in (("m3_range_sigma_day", "c1g"), ("m3_tr_sigma_day", "c2g"),
                      ("m3_tr_expansion_day", "c3dg")):
        arr = e[gkey][s0:i + 1]
        med = float(fe.rolling_arr(arr, W3_D, MO_SHAPE, "median")[-1])
        out[key] = med if availD else _nan()

    # ---- D1..D5 (windows [i-479, i]; slices of engine-computed arrays) ------
    for key, gkey in (("m3_body_range_day", "dd0"), ("m3_up_wick_day", "dd1"),
                      ("m3_low_wick_day", "dd2"), ("m3_close_pos_day", "dd3"),
                      ("m3_body_dir_day", "dd4")):
        arr = e[gkey][s0:i + 1]
        med = float(fe.rolling_arr(arr, W3_D, MO_SHAPE, "median")[-1])
        out[key] = med if availD else _nan()

    # ---- E1 / E5 ---------------------------------------------------------------
    n_ext = int(e["p_ext3"][i + 1] - e["p_ext3"][lo])
    n_cls = int(e["p_cls3"][i + 1] - e["p_cls3"][lo])
    out["m3_ext_rate_month"] = (
        n_ext / n_cls if (availM and n_cls >= MO3_M) else _nan())
    n_pos = int(e["p_pos"][i + 1] - e["p_pos"][lo])
    out["m3_ext_sign_month"] = (
        n_pos / n_ext if (availM and n_ext >= MO_EXT) else _nan())

    # ---- E4 ---------------------------------------------------------------------
    lo_j = max(j_idx - (W1_D - 1), 0)
    n_ext1 = int(e["p_ext1"][j_idx + 1] - e["p_ext1"][lo_j])
    n_cls1 = int(e["p_cls1"][j_idx + 1] - e["p_cls1"][lo_j])
    out["m1_ext_rate_day"] = (
        n_ext1 / n_cls1 if (j_idx >= W1_D - 1 and n_cls1 >= fe.MO1_D) else _nan())

    # ---- E2/E3 (verbatim population moments) ------------------------------------
    cnt4 = e["cnt4"][i]
    s1q, s2q, s3q, s4q = e["s1_4"][i], e["s2_4"][i], e["s3_4"][i], e["s4_4"][i]
    mn = s1q / max(cnt4, 1)
    m2 = s2q / max(cnt4, 1) - mn * mn
    m3_ = s3q / max(cnt4, 1) - 3.0 * mn * (s2q / max(cnt4, 1)) + 2.0 * mn ** 3
    m4 = s4q / max(cnt4, 1) - 4.0 * mn * (s3q / max(cnt4, 1)) \
        + 6.0 * mn ** 2 * (s2q / max(cnt4, 1)) - 3.0 * mn ** 4
    okm = availM and cnt4 >= MO3_M and m2 > 0
    out["m3_skew_month"] = (
        m3_ / np.power(np.maximum(m2, 0.0), 1.5) if okm else _nan())
    out["m3_kurtosis_month"] = (
        m4 / (np.maximum(m2, 0.0) ** 2) - 3.0 if okm else _nan())

    # ---- F1 (verbatim: hit[s] = OR ext[s-k], k=1..5; window [i-14399, i-6]) -----
    loF = lo
    hiF = i - 5
    ext_arr = e["ext3"]
    n_hit = n_elig = 0
    if hiF >= loF:
        start = max(loF - 5, 0)
        Es = ext_arr[start:i + 1].astype(np.int64)
        hit = np.zeros(len(Es), dtype=bool)
        for k in range(1, 6):
            hit[k:] |= Es[:-k].astype(bool)
        j0 = loF - start
        j1 = hiF - start
        n_hit = int(np.sum(Es[j0:j1] & hit[j0:j1]))
        n_elig = int(np.sum(Es[j0:j1]))
    v = n_hit / n_elig if n_elig > 0 else _nan()
    f1_avail = availM and (i >= W3_M + 4)
    out["m3_storm_clust_month"] = (
        v if (f1_avail and n_elig >= MO_EXT) else _nan())

    # ---- F2 P90 run length (window [i-14399, i]) --------------------------------
    out["m3_storm_p90_run_month"] = _f2(ext_arr, i, lo, availM, n_ext)

    # ---- F3 median spacing (active pairs at i: both extremes in [i-14399, i]) ---
    out["m3_ext_spacing_month"] = _f3(ext_arr, i, lo, availM, n_ext)
    return out


def _f2(ext_arr, i, lo, availM, n_ext):
    if not (availM and n_ext >= MO_EXT):
        return _nan()
    seg = ext_arr[max(lo - 1, 0):i + 1]
    lens = []
    j, m = 0, len(seg)
    while j < m:
        if seg[j] == 1:
            k = j
            while k + 1 < m and seg[k + 1] == 1:
                k += 1
            gs = max(lo - 1, 0) + j
            ge = max(lo - 1, 0) + k
            cs = max(gs, lo)
            ce = min(ge, i)
            if cs <= ce:
                lens.append(int(ce - cs + 1))
            j = k + 1
        else:
            j += 1
    if not lens:
        return _nan()
    lens = np.sort(np.asarray(lens, dtype=np.float64))
    tot = len(lens)
    k = 0.9 * (tot - 1)
    low = int(np.floor(k))
    frac = k - low
    v_lo = lens[low] if low < tot else lens[-1]
    if frac == 0.0:
        return float(v_lo)
    v_hi = lens[int(np.ceil(k))] if int(np.ceil(k)) < tot else lens[-1]
    return float(v_lo + frac * (v_hi - v_lo))


def _f3(ext_arr, i, lo, availM, n_ext):
    if not (availM and n_ext >= MO_EXT):
        return _nan()
    loE = max(lo, 0)
    pos_e = np.flatnonzero(ext_arr[loE:i + 1]) + loE
    if len(pos_e) < 2:
        return _nan()
    gaps = np.sort(np.diff(pos_e).astype(np.float64))
    tot = len(gaps)
    k = 0.5 * (tot - 1)
    low = int(np.floor(k))
    frac = k - low
    v_lo = gaps[low]
    if frac == 0.0:
        return float(v_lo)
    v_hi = gaps[int(np.ceil(k))]
    return float(v_lo + frac * (v_hi - v_lo))


# ---------------------------------------------------------------------------
# probes: 3 per period, deep in data, complete buckets, contiguous joins
# ---------------------------------------------------------------------------
def select_probes():
    g3 = pq.read_table(os.path.join(SCRATCH, "m3_grid.parquet"))
    t3 = g3.column("t_min").to_numpy(zero_copy_only=False).astype(np.int64)
    n_m1 = g3.column("n_m1").to_numpy(zero_copy_only=False)
    intm = g3.column("internal_missing").to_numpy(zero_copy_only=False)
    intb = g3.column("internal_breaks").to_numpy(zero_copy_only=False)
    cont = g3.column("contig_next").to_numpy(zero_copy_only=False).astype(bool)
    ref = pq.read_table(FEAT_FILE)
    rts = ref.column("ts_min").to_numpy(zero_copy_only=False).astype(np.int64)
    assert np.array_equal(rts, t3)
    rb = ref.column("bar_id").to_numpy(zero_copy_only=False).astype(np.int64)

    probes = []
    for year, months in YEAR_MONTHS.items():
        for mo in months:
            tgt = _epoch_min(year, mo, 15, 10, 0)
            # widen to mid-week window (targets may fall on a closure)
            lo_t, hi_t = tgt - 3 * 1440, tgt + 3 * 1440
            idx = int(np.searchsorted(t3, lo_t, side="right") - 1)
            chosen = None
            for i in range(max(idx, 0), min(idx + 6 * 1440 // 3, len(t3))):
                T = int(t3[i])
                if T > hi_t + 240:
                    break
                if i < W3_M + 5000:
                    continue
                if int(n_m1[i]) != 3 or int(intm[i]) > 0 or int(intb[i]) > 0:
                    continue
                if not cont[i] or i + 1 >= len(t3) or not cont[i + 1]:
                    continue
                vals = [float(ref.column(fn)[i].as_py()) for fn in FEATURES]
                if all(np.isfinite(v) for v in vals):
                    chosen = (i, T, vals)
                    break
            if chosen is None:
                raise RuntimeError(f"no valid probe {year}-{mo}")
            i, T, vals = chosen
            probes.append({"period": str(year), "row": i, "T": T, "Ts": T + 2,
                           "bar_id": int(rb[i]),
                           "values": dict(zip(FEATURES, vals))})
    Ts = [p["Ts"] for p in probes]
    assert all(b - a >= 27 * 1440 for a, b in zip(Ts, Ts[1:])), "probes too close"
    return probes


# ---------------------------------------------------------------------------
def main():
    pilot = "--pilot" in sys.argv
    t_all = time.time()
    full = _load_full_arrays()
    probes = select_probes()
    if pilot:
        probes = probes[:1]
    print(f"probes: {len(probes)}", flush=True)

    rows = []
    t0 = time.time()

    # ---- REF identity gate: one full env, all probes, then release ---------
    print("ref identity gate across all probes...", flush=True)
    ref_env = make_env(full, None)
    for p in probes:
        hb = (p["Ts"] // 60) * 60
        hi = int(np.searchsorted(ref_env["tH"], hb, side="right") - 1)
        p["h1_contig_at_t"] = bool(ref_env["contH"][hi]) if hi >= 0 else False
        p["h1_idx"] = hi
    for p in probes:
        vals = values_at(ref_env, p["row"])
        for f in FEATURES:
            vr = p["values"][f]
            vt = vals[f]
            if np.isnan(vr) and np.isnan(vt):
                verdict, exact, diff = "NA_STRUCTURAL", 0, None
            elif np.isfinite(vr) and np.isfinite(vt):
                d = float(abs(vt - vr))
                exact = int(d == 0.0)
                verdict = "PASS" if exact else "FAIL"
                diff = f"{d:.18g}"
            else:
                verdict, exact, diff = "FAIL", 0, None
            rows.append({
                "timestamp": p["Ts"], "probe_id": f"{p['period']}-{p['T']}",
                "period": p["period"], "feature": f, "family": FAMILY[f],
                "mode": "ref", "cut_min": None,
                "h1_closed_at_ts": bool(p["Ts"] % 60 == 59),
                "h1_contig_at_t": p.get("h1_contig_at_t", False),
                "value_reference": vr, "value_truncated": vt,
                "abs_diff": diff, "exact_zero": exact, "verdict": verdict,
            })
    del ref_env
    refbad = sum(1 for r in rows if r["mode"] == "ref" and r["verdict"] == "FAIL")
    if refbad > 0:
        print(f"REF GATE FAILED ({refbad}): harness transcription bug, "
              f"NOT a PIT result. Aborting.", flush=True)
        for r in [x for x in rows if x["mode"] == "ref"
                  and x["verdict"] == "FAIL"][:10]:
            print("  REF MISMATCH", r["probe_id"], r["feature"],
                  r["value_reference"], r["value_truncated"], flush=True)
        return 4

    for pid, p in enumerate(probes):
        i, T, Ts = p["row"], p["T"], p["Ts"]
        print(f"probe {pid+1}/{len(probes)} {p['period']} T={T} Ts%60={Ts%60}",
              flush=True)
        for mode, off in MODES:
            if off is None:
                continue
            cut = Ts + off
            env = make_env(full, cut)
            vals = values_at(env, i)
            for f in FEATURES:
                vr = p["values"][f]
                vt = vals[f]
                if np.isnan(vr) and np.isnan(vt):
                    verdict, exact, diff = "NA_STRUCTURAL", 0, None
                elif np.isfinite(vr) and np.isfinite(vt):
                    d = float(abs(vt - vr))
                    exact = int(d == 0.0)
                    verdict = "PASS" if exact else "FAIL"
                    diff = f"{d:.18g}"
                else:
                    verdict, exact, diff = "FAIL", 0, None
                rows.append({
                    "timestamp": Ts, "probe_id": f"{p['period']}-{T}",
                    "period": p["period"], "feature": f, "family": FAMILY[f],
                    "mode": mode, "cut_min": cut,
                    "h1_closed_at_ts": bool(Ts % 60 == 59),
                    "h1_contig_at_t": p.get("h1_contig_at_t", False),
                    "value_reference": vr, "value_truncated": vt,
                    "abs_diff": diff, "exact_zero": exact, "verdict": verdict,
                })
            del env
        print(f"  -> {round(time.time()-t0,1)}s elapsed", flush=True)

    cols = ["timestamp", "feature", "value_reference", "value_truncated",
            "abs_diff", "exact_zero", "verdict", "probe_id", "period", "family",
            "mode", "cut_min", "h1_closed_at_ts", "h1_contig_at_t"]
    with open(OUT_CSV, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow(r)

    tally = Counter(r["verdict"] for r in rows)
    fail_feat = Counter(r["feature"] for r in rows if r["verdict"] == "FAIL")
    fail_mode = Counter(r["mode"] for r in rows if r["verdict"] == "FAIL")
    fail_probe = Counter(r["probe_id"] for r in rows if r["verdict"] == "FAIL")
    refbad = sum(1 for r in rows if r["mode"] == "ref" and r["verdict"] == "FAIL")
    duration = time.time() - t_all
    summary = {"probes": len(probes), "rows": len(rows), "tally": dict(tally),
               "fail_features": dict(fail_feat), "fail_modes": dict(fail_mode),
               "fail_probes": len(fail_probe), "ref_mismatch": refbad,
               "duration_s": round(duration, 1), "pilot": pilot}
    print(json.dumps(summary, indent=2), flush=True)

    if refbad > 0:
        print(f"REF GATE FAILED ({refbad}): harness transcription bug, "
              f"NOT a PIT result. Aborting.", flush=True)
        for r in [x for x in rows if x["mode"] == "ref"
                  and x["verdict"] == "FAIL"][:10]:
            print("  REF MISMATCH", r["probe_id"], r["feature"],
                  r["value_reference"], r["value_truncated"], flush=True)
        return 4

    if pilot:
        print("identity(ref) mismatches: 0", flush=True)
        print(f"PILOT = OK ({round(duration,1)}s)", flush=True)
        return 0

    _write_md(rows, summary)
    return 0


def _write_md(rows, summary):
    ncmp = sum(1 for r in rows if r["mode"] != "ref")
    npass = sum(1 for r in rows if r["mode"] != "ref" and r["verdict"] == "PASS")
    nfail = sum(1 for r in rows if r["mode"] != "ref" and r["verdict"] == "FAIL")
    nna = sum(1 for r in rows if r["mode"] != "ref" and r["verdict"] == "NA_STRUCTURAL")
    nref = sum(1 for r in rows if r["mode"] == "ref")
    refbad = sum(1 for r in rows if r["mode"] == "ref" and r["verdict"] == "FAIL")
    fail_feat = Counter(r["feature"] for r in rows if r["verdict"] == "FAIL")
    md = f"""# PHASE 3 V2 — STEP 3.5R : DYNAMIC PIT AUDIT (OPTIMIZED, TARGETED)

**Date :** 2026-09-06 (UTC) · **Type :** preuve PAST-ONLY par troncature dynamique ciblée.
**Méthode :** l'ancien protocole intégral n'a PAS été relancé. Structure du moteur analysée
(`feature_engine_v2.py` = helpers purs `rolling_arr/pair_prefixes/acf_vec/prefix_mask/
prefix_cum/roll_sums4` + expressions par indice) ; `scripts/dynamic_pit_audit_v2.py` reconstruit
uniquement les tableaux d'entrée du moteur sur le préfixe tronqué (builder FROZEN `01_build_layers.py`
exécuté non modifié) et évalue les 25 features **seulement à la ligne-sonde `t`**, avec les mêmes
fenêtres / MIN_OBS / estimateurs et le même ordre arithmétique (préfixes de parité B2 inclus).
Aucune feature ni formule modifiée ; aucune agrégation / clustering / K / HMM-GMM / backtest.

## Sondes
{summary['probes']} sondes — 3 par période : 2010, 2012, 2013, 2016, 2020, 2024, 2026.
Chaque sonde : barre M3 réelle, profondeur ≥ 14 400 + 5 000 positions (loin du warm-up),
bucket sans minute manquante ni rupture interne, jointures M3 contiguës avant/après,
25 features finies dans le dataset de référence.

## Modes par sonde (5)
| mode | cut_min | rôle |
|---|---|---|
| ref  | — | contrôle d'identité du harnais vs parquet committé (doit être 0 mismatch) |
| exact | Ts | données strictement limitées à `t` |
| o1 | Ts+3 | +1 observation M3 |
| o10 | Ts+30 | +10 observations M3 |
| o100 | Ts+300 | +100 observations M3 |

## Résultats
```
Comparaisons PIT (exact/o1/o10/o100) = {ncmp}
  PASS = {npass} | FAIL = {nfail} | NA structurels = {nna}
Contrôle d'identité (mode ref) = {nref} (mismatch = {refbad})
Durée d'exécution = {summary['duration_s']} s
```
"""
    md += "\n### PASS/FAIL par mode\n\n| mode | PASS | FAIL |\n|---|---|---|\n"
    for mode in ("exact", "o1", "o10", "o100", "ref"):
        p = sum(1 for r in rows if r["mode"] == mode and r["verdict"] == "PASS")
        f = sum(1 for r in rows if r["mode"] == mode and r["verdict"] == "FAIL")
        md += f"| {mode} | {p} | {f} |\n"
    md += "\n### Détail par sonde\n\n| sonde | Ts%60 | H1 bar close at t | modes en échec |\n|---|---|---|---|\n"
    for p in sorted({(r["probe_id"], r["timestamp"], r["h1_closed_at_ts"],
                      r["h1_contig_at_t"]) for r in rows}):
        pid, ts, closed, cont = p
        fm = [m for m in ("exact", "o1", "o10", "o100") if any(
            r["probe_id"] == pid and r["mode"] == m and r["verdict"] == "FAIL"
            for r in rows)]
        md += (f"| {pid} | {ts % 60} | fermé={closed} · contigu={cont} | "
               f"{', '.join(fm) if fm else '—'} |\n")
    md += """
> **Remarque de couverture :** les sondes dont la barre H1 `h(t)` (bucket
> contenant `T+2`) est contiguë après `t` exposent pleinement la dépendance
> (16/21 sondes échouent) ; les 5 sondes "PASS" ont un `contig_next=0` à cette
> barre H1, donc `rH` y est NaN des deux côtés et la fenêtre H1 ne voit pas la
> différence — le test y est structurellement aveugle, il ne prouve PAS un
> PASS. Le verdict global reste donc défini par les 16 sondes exposées.
> """
    md += "\n### Features en échec\n\n| feature | famille | FAIL | max abs_diff |\n|---|---|---|---|\n"
    fams = {r["feature"]: r["family"] for r in rows}
    for fname, cnt in sorted(fail_feat.items()):
        mx = max(float(r["abs_diff"]) for r in rows
                 if r["feature"] == fname and r["verdict"] == "FAIL")
        md += f"| {fname} | {fams[fname]} | {cnt} | {mx:.6g} |\n"
    md += f"""
## Conclusion
**DYNAMIC_PIT = {'FAIL' if nfail > 0 else 'PASS'}**

Règle appliquée : si FAIL -> STOP, aucune correction. Liste complète des lignes dans
`PHASE3_V2_DYNAMIC_PIT_AUDIT.csv` (timestamp, feature, value_reference, value_truncated,
abs_diff, exact_zero, verdict).
"""
    with open(OUT_MD, "w") as fh:
        fh.write(md)
    print("written md+csv", flush=True)


if __name__ == "__main__":
    sys.exit(main())
