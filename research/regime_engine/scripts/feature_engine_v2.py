#!/usr/bin/env python3
"""
PHASE 3 V2 - STEP 3.3: FEATURE ENGINE IMPLEMENTATION
====================================================
Implements EXACTLY the 25 features of the FROZEN specification
`research/regime_engine/PHASE3_V2_FEATURE_SPEC.md` (authority), on the FROZEN
data contract `research/regime_engine/PHASE3_V2_DATA_CONTRACT.md`.

Rules enforced:
  * past-only, no future data, no centered window, no volume, no gap fill,
    no external data, no global normalization, NaN preserved, no observation
    removed from the master.
  * every window is a POSITION window [i-W+1, i] on the validated grids;
    M1/H1 are INPUTS aligned to the closed M3 bar t (endM1(t), h(t)).
  * estimators pinned by the spec: std/var ddof=1, quantiles linear
    interpolation, skew/kurt population moments, Pearson pairwise-complete,
    VR non-overlapping q=2 disjoint blocks (invalid blocks skipped).

Outputs:
  research/regime_engine/XAUUSD_FEATURES_V2.parquet   (ts_min, bar_id, 25 features)
  research/regime_engine/features_v2_meta.json        (per-feature metadata)

Usage:  python3 feature_engine_v2.py
"""
from __future__ import annotations

import hashlib
import json
import os
import time
from datetime import datetime, timezone

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

OUT = "/home/user/xauusd-quant-research/research/regime_engine"
MASTER = "/tmp/xauusd_audit/XAUUSD_M1_reconstructed.parquet"
M3_GRID = "/tmp/xauusd_audit/regime_engine/m3_grid.parquet"
H1_GRID = "/tmp/xauusd_audit/regime_engine/h1_grid.parquet"

MASTER_SHA = "fdce55a8c8a76c417765ad020794866bb36e5b166c130d2bb4deb2aeeeab91d0"
MASTER_ROWS = 5_874_003
M3_ROWS = 1_963_826
H1_ROWS = 98_412
M3_SHA = "c1eb3e09532cb92f46d6753f3d0abeda9a810dc8208a78d7e7105f2593b8a06f"
H1_SHA = "0372b46dd26bfcca6b29375a7103e4862a56a1f6b70bb7a876c62f9c8b5e12b7"
SHOCK_MULT = 3.0

# windows / MIN_OBS (FROZEN spec)
W3_D, MO3_D = 480, 120
W3_M, MO3_M = 14_400, 3_600
W1_D, MO1_D = 1_440, 360
WH_D, MOH_D = 24, 12
WH_M, MOH_M = 336, 84
MO_SHAPE = 120
MO_EXT = 30

FEATURES = [
    # (name, family, timeframe_source, window, min_obs, units, formula_ref)
    ("m3_vol_ratio_day_month", "A", "M3", "480 / 14400 (M3 pos)", "120 / 3600",
     "dimensionless", "S3.2-A1"),
    ("m3_m1_noise_ratio", "A", "M3 + M1", "1440 M1 pos / 480 M3 pos", "360 / 120",
     "dimensionless", "S3.2-A2"),
    ("h1_vol_ratio_day_month", "A", "M3 + H1", "24 / 336 H1 pos", "12 / 84",
     "dimensionless", "S3.2-A3"),
    ("m3_acf1_day", "B", "M3", "480 (M3 pos)", "120 pairs",
     "dimensionless", "S3.2-B1"),
    ("m3_vr2_month", "B", "M3", "14400 (q=2, disjoint blocks)", "3600 blocks",
     "dimensionless", "S3.2-B2"),
    ("m3_scf_day", "B", "M3", "480 (M3 pos)", "120 pairs",
     "[0,1]", "S3.2-B3"),
    ("m3_run_month", "B", "M3", "14400 (M3 pos)", "3600 signs",
     "bars", "S3.2-B4"),
    ("m3_dir_month", "B", "M3", "14400 (M3 pos)", "3600",
     "dimensionless", "S3.2-B5"),
    ("h1_acf1_month", "B", "M3 + H1", "336 (H1 pos)", "84 pairs",
     "dimensionless", "S3.2-B6"),
    ("m3_range_sigma_day", "C", "M3", "480 (M3 pos)", "120",
     "dimensionless", "S3.2-C1"),
    ("m3_tr_sigma_day", "C", "M3", "480 (M3 pos)", "120",
     "dimensionless", "S3.2-C2"),
    ("m3_tr_expansion_day", "C", "M3", "480 (M3 pos)", "120 deltas",
     "bps", "S3.2-C3"),
    ("m3_body_range_day", "D", "M3", "480 (M3 pos)", "120 bars",
     "[0,1]", "S3.2-D1"),
    ("m3_up_wick_day", "D", "M3", "480 (M3 pos)", "120 bars",
     "[0,1]", "S3.2-D2"),
    ("m3_low_wick_day", "D", "M3", "480 (M3 pos)", "120 bars",
     "[0,1]", "S3.2-D3"),
    ("m3_close_pos_day", "D", "M3", "480 (M3 pos)", "120 bars",
     "[0,1]", "S3.2-D4"),
    ("m3_body_dir_day", "D", "M3", "480 (M3 pos)", "120 bars",
     "[-1,1]", "S3.2-D5"),
    ("m3_ext_rate_month", "E", "M3", "14400 (M3 pos)", "3600",
     "[0,1]", "S3.2-E1"),
    ("m3_kurtosis_month", "E", "M3", "14400 (M3 pos)", "3600",
     "dimensionless", "S3.2-E2"),
    ("m3_skew_month", "E", "M3", "14400 (M3 pos)", "3600",
     "dimensionless", "S3.2-E3"),
    ("m1_ext_rate_day", "E", "M3 + M1", "1440 (M1 pos closed at t)", "360",
     "[0,1]", "S3.2-E4"),
    ("m3_ext_sign_month", "E", "M3", "14400 (M3 pos)", "30 extremes",
     "[0,1]", "S3.2-E5"),
    ("m3_storm_clust_month", "F", "M3", "14400 (+5) (M3 pos)", "30 extremes",
     "[0,1]", "S3.2-F1"),
    ("m3_storm_p90_run_month", "F", "M3", "14400 (M3 pos)", "30 extremes",
     "bars", "S3.2-F2"),
    ("m3_ext_spacing_month", "F", "M3", "14400 (M3 pos)", "30 extremes",
     "bars", "S3.2-F3"),
]
assert len(FEATURES) == 25


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def rolling_arr(x: np.ndarray, w: int, mo: int, fn: str) -> np.ndarray:
    """Positional rolling [i-w+1, i]; NaN excluded from the window (min_periods)."""
    s = pd.Series(x.copy())
    r = getattr(s.rolling(w, min_periods=mo), fn)()
    return r.to_numpy(dtype="float64")


def roll_sums4(x: np.ndarray, w: int, mo: int):
    s = pd.Series(x.copy())
    cnt = s.rolling(w, min_periods=1).count().to_numpy(dtype="float64")
    s1 = s.rolling(w, min_periods=mo).sum().to_numpy(dtype="float64")
    s2 = (s * s).rolling(w, min_periods=mo).sum().to_numpy(dtype="float64")
    s3 = (s ** 3).rolling(w, min_periods=mo).sum().to_numpy(dtype="float64")
    s4 = (s ** 4).rolling(w, min_periods=mo).sum().to_numpy(dtype="float64")
    return cnt, s1, s2, s3, s4


def prefix_cum(x: np.ndarray) -> np.ndarray:
    return np.concatenate(([0.0], np.cumsum(x)))


def prefix_mask(valid: np.ndarray) -> np.ndarray:
    return np.concatenate(([0], np.cumsum(valid.astype(np.int64))))


def shift1(x: np.ndarray) -> np.ndarray:
    return np.concatenate(([np.nan], x[:-1]))


def pair_prefixes(x: np.ndarray):
    """Pair arrays (a=x[s], b=x[s-1]) for s=1..n-1; prefixes indexed by s (len n)."""
    a = x[1:]
    b = x[:-1]
    valid = np.isfinite(a) & np.isfinite(b)
    an = np.where(valid, a, 0.0)
    bn = np.where(valid, b, 0.0)
    return (prefix_mask(valid), prefix_cum(an), prefix_cum(bn),
            prefix_cum(an * an), prefix_cum(bn * bn), prefix_cum(an * bn))


def acf_vec(P, idx, lo_pairs: int, mo: int):
    """ACF over pair windows [idx-lo_pairs, idx]; P = pair prefixes; mo = MIN pairs."""
    p_n, p_a, p_b, p_a2, p_b2, p_ab = P
    lo = idx - lo_pairs
    n = p_n[idx] - p_n[np.maximum(lo - 1, 0)]
    n = np.where(lo >= 1, n, 0.0)
    sa = p_a[idx] - p_a[np.maximum(lo - 1, 0)]
    sb = p_b[idx] - p_b[np.maximum(lo - 1, 0)]
    sa2 = p_a2[idx] - p_a2[np.maximum(lo - 1, 0)]
    sb2 = p_b2[idx] - p_b2[np.maximum(lo - 1, 0)]
    sab = p_ab[idx] - p_ab[np.maximum(lo - 1, 0)]
    num = n * sab - sa * sb
    den2 = (n * sa2 - sa * sa) * (n * sb2 - sb * sb)
    out = np.full(idx.shape, np.nan)
    ok = (n >= mo) & (den2 > 0)
    out[ok] = num[ok] / np.sqrt(den2[ok])
    return out


class Fenwick:
    def __init__(self, size: int):
        self.n = size
        self.tree = [0] * (size + 1)

    def add(self, idx: int, delta: int) -> None:
        i = idx + 1
        while i <= self.n:
            self.tree[i] += delta
            i += i & (-i)

    def total(self) -> int:
        s, i = 0, self.n
        while i > 0:
            s += self.tree[i]
            i -= i & (-i)
        return s

    def select(self, k: int) -> int:
        idx, bit, rem = 0, 1 << (self.n.bit_length()), k + 1
        while bit:
            nxt = idx + bit
            if nxt <= self.n and self.tree[nxt] < rem:
                idx = nxt
                rem -= self.tree[nxt]
            bit >>= 1
        return idx


def main() -> None:
    t0 = time.time()
    print("verifying SHA...", flush=True)
    assert sha256_file(MASTER) == MASTER_SHA
    assert sha256_file(M3_GRID) == M3_SHA
    assert sha256_file(H1_GRID) == H1_SHA
    print("master + grids verified", flush=True)

    # ================= M1 substrate =========================================
    t1 = pq.read_table(MASTER, columns=["timestamp", "close"])
    ts = t1.column("timestamp").to_numpy(zero_copy_only=False)
    c1 = t1.column("close").to_numpy().astype("float64")
    del t1
    t_min1 = ts.astype("datetime64[m]").astype("int64")
    del ts
    n1 = len(t_min1)
    assert n1 == MASTER_ROWS
    assert np.all(np.diff(t_min1) > 0)
    r1 = np.full(n1, np.nan)
    r1[1:] = np.log(c1[1:]) - np.log(c1[:-1])
    del c1
    clean1 = np.zeros(n1, dtype=bool)
    clean1[1:] = (t_min1[1:] - t_min1[:-1]) == 1
    clean1 &= np.isfinite(r1)
    r1 = np.where(clean1, r1, np.nan)
    del clean1
    s1_day = rolling_arr(r1, W1_D, MO1_D, "std")        # [j-1439, j]
    s1_prev = shift1(s1_day)                            # [j-1440, j-1]
    cls1 = np.isfinite(s1_prev) & (s1_prev > 0)
    ext1 = np.zeros(n1, dtype=np.int64)
    ext1[cls1] = (np.abs(r1[cls1]) > SHOCK_MULT * s1_prev[cls1]).astype(np.int64)
    p_ext1 = prefix_mask(ext1)
    p_cls1 = prefix_mask(cls1)
    del r1, s1_prev, cls1, ext1
    print("M1 ready", flush=True)

    # ================= H1 context ===========================================
    th = pq.read_table(H1_GRID, columns=["t_min", "close", "contig_next"])
    t_h1 = th.column("t_min").to_numpy(zero_copy_only=False).astype("int64")
    c_h1 = th.column("close").to_numpy().astype("float64")
    cont_h1 = th.column("contig_next").to_numpy(zero_copy_only=False)
    del th
    nH = len(t_h1)
    assert nH == H1_ROWS
    assert np.all(np.diff(t_h1) > 0)
    rH = np.full(nH, np.nan)
    rH[1:] = np.log(c_h1[1:]) - np.log(c_h1[:-1])
    del c_h1
    cleanH = cont_h1.astype(bool) & np.isfinite(rH)
    rH = np.where(cleanH, rH, np.nan)
    del cleanH, cont_h1
    sH24 = rolling_arr(rH, WH_D, MOH_D, "std")
    sH336 = rolling_arr(rH, WH_M, MOH_M, "std")
    PH = pair_prefixes(rH)
    del rH
    print("H1 ready", flush=True)

    # ================= M3 grid ==============================================
    g = pq.read_table(M3_GRID, columns=["t_min", "bar_id", "open", "high", "low",
                                        "close", "contig_next"])
    t3 = g.column("t_min").to_numpy(zero_copy_only=False).astype("int64")
    bid3 = g.column("bar_id").to_numpy(zero_copy_only=False).astype("int64")
    o3 = g.column("open").to_numpy().astype("float64")
    h3 = g.column("high").to_numpy().astype("float64")
    l3 = g.column("low").to_numpy().astype("float64")
    c3 = g.column("close").to_numpy().astype("float64")
    cont3 = g.column("contig_next").to_numpy(zero_copy_only=False)
    del g
    n = len(t3)
    assert n == M3_ROWS
    assert np.all(np.diff(t3) > 0) and np.all(np.diff(bid3) > 0)

    endM1 = t3 + 2
    j_idx = np.searchsorted(t_min1, endM1, side="right") - 1
    assert np.all(t_min1[j_idx] // 3 == t3 // 3)
    hb = (endM1 // 60) * 60
    h_idx = np.searchsorted(t_h1, hb, side="right") - 1
    assert np.all(t_h1[h_idx] == hb)

    r3 = np.full(n, np.nan)
    r3[1:] = np.log(c3[1:]) - np.log(c3[:-1])
    clean3 = np.zeros(n, dtype=bool)
    clean3[1:] = cont3[1:].astype(bool)
    clean3 &= np.isfinite(r3)
    r3 = np.where(clean3, r3, np.nan)
    del clean3, cont3

    pos = np.arange(n)
    availD = pos >= W3_D - 1
    availM = pos >= W3_M - 1
    out = {"ts_min": t3, "bar_id": bid3}

    # rolling sigmas
    s3_day = rolling_arr(r3, W3_D, MO3_D, "std")     # [i-479, i]
    s3_prev = shift1(s3_day)                         # [s-480, s-1]
    s3_mon = rolling_arr(r3, W3_M, MO3_M, "std")
    print("rolling sigmas ready", flush=True)

    # ---------- A1 -----------------------------------------------------------
    v = s3_day / s3_mon
    out["m3_vol_ratio_day_month"] = np.where(availM & (s3_day > 0) & (s3_mon > 0), v, np.nan)

    # ---------- A2 -----------------------------------------------------------
    s1_j = s1_day[j_idx]
    v = (np.sqrt(3.0) * s1_j) / s3_day
    m = availD & (j_idx >= W1_D - 1) & (s1_j > 0) & (s3_day > 0)
    out["m3_m1_noise_ratio"] = np.where(m, v, np.nan)
    del s1_j, v

    # ---------- A3 -----------------------------------------------------------
    v = sH24[h_idx] / sH336[h_idx]
    m = (h_idx >= WH_M - 1) & (sH24[h_idx] > 0) & (sH336[h_idx] > 0)
    out["h1_vol_ratio_day_month"] = np.where(m, v, np.nan)
    del v

    # ---------- B1 -----------------------------------------------------------
    P = pair_prefixes(r3)
    res = acf_vec(P, pos, W3_D - 2, MO3_D)
    out["m3_acf1_day"] = np.where(availD, res, np.nan)
    del P, res

    # ---------- B3 -----------------------------------------------------------
    a = r3[1:]
    b = r3[:-1]
    valid2 = np.isfinite(a) & np.isfinite(b) & (a != 0) & (b != 0)
    chg = valid2 & ((a > 0) != (b > 0))
    pn2 = prefix_mask(valid2)
    pc2 = prefix_mask(chg)
    loB3 = pos - (W3_D - 2)
    nv = pn2[pos] - pn2[np.maximum(loB3 - 1, 0)]
    nc = pc2[pos] - pc2[np.maximum(loB3 - 1, 0)]
    nv = np.where(loB3 >= 1, nv, 0.0)
    nc = np.where(loB3 >= 1, nc, 0.0)
    v = np.where(nv > 0, nc / np.maximum(nv, 1), np.nan)
    out["m3_scf_day"] = np.where(availD & (nv >= MO3_D), v, np.nan)
    del a, b, valid2, chg, pn2, pc2, v, nv, nc

    # ---------- B5 (mean/std) ------------------------------------------------
    rnz = np.where(np.isfinite(r3), r3, 0.0)
    cnt_r = prefix_mask(np.isfinite(r3))
    s_r = prefix_cum(rnz)
    q_r = prefix_cum(rnz * rnz)
    lo5 = pos - (W3_M - 1)
    nc5 = cnt_r[pos + 1] - cnt_r[np.maximum(lo5, 0)]
    ss5 = s_r[pos + 1] - s_r[np.maximum(lo5, 0)]
    qq5 = q_r[pos + 1] - q_r[np.maximum(lo5, 0)]
    mean_r = np.where(nc5 > 0, ss5 / np.maximum(nc5, 1), np.nan)
    var_r = np.where(nc5 > 1, (qq5 - ss5 * ss5 / np.maximum(nc5, 1)) / (nc5 - 1), np.nan)
    v = mean_r / np.sqrt(np.maximum(var_r, 0.0))
    out["m3_dir_month"] = np.where(availM & (nc5 >= MO3_M) & (var_r > 0), v, np.nan)
    del rnz, cnt_r, s_r, q_r, v, mean_r

    # ---------- B2 (VR q=2 disjoint blocks) ----------------------------------
    pb = np.zeros(n - 1)
    sb = np.zeros(n - 1)
    vb = np.isfinite(r3[1:]) & np.isfinite(r3[:-1])
    pb[vb] = 1.0
    sb[vb] = r3[1:][vb] + r3[:-1][vb]
    qb = sb * sb
    par = (pos - (W3_M - 1)) % 2          # parity of block-start position loB2
    # per-parity prefix arrays over block start positions p (0..n-2)
    ev = np.zeros(n - 1); sv = np.zeros(n - 1); qv = np.zeros(n - 1)
    ev[::2] = pb[::2]; sv[::2] = sb[::2]; qv[::2] = qb[::2]
    eo = np.zeros(n - 1); so = np.zeros(n - 1); qo = np.zeros(n - 1)
    eo[1::2] = pb[1::2]; so[1::2] = sb[1::2]; qo[1::2] = qb[1::2]
    Ce = prefix_cum(ev); Se = prefix_cum(sv); Qe = prefix_cum(qv)
    Co = prefix_cum(eo); So = prefix_cum(so); Qo = prefix_cum(qo)
    loB2 = pos - (W3_M - 1)
    hiB2 = pos - 1
    loB2c = np.maximum(loB2, 0)
    C = np.where(par == 0, Ce[np.maximum(hiB2, 0)] - Ce[np.maximum(loB2c - 1, 0)],
                 Co[np.maximum(hiB2, 0)] - Co[np.maximum(loB2c - 1, 0)])
    S = np.where(par == 0, Se[np.maximum(hiB2, 0)] - Se[np.maximum(loB2c - 1, 0)],
                 So[np.maximum(hiB2, 0)] - So[np.maximum(loB2c - 1, 0)])
    Q = np.where(par == 0, Qe[np.maximum(hiB2, 0)] - Qe[np.maximum(loB2c - 1, 0)],
                 Qo[np.maximum(hiB2, 0)] - Qo[np.maximum(loB2c - 1, 0)])
    C = np.where(loB2 >= 0, C, 0.0)
    S = np.where(loB2 >= 0, S, 0.0)
    Q = np.where(loB2 >= 0, Q, 0.0)
    vb_var = np.where(C > 1, (Q - S * S / np.maximum(C, 1)) / (C - 1), np.nan)
    v = vb_var / (2.0 * var_r)
    out["m3_vr2_month"] = np.where(availM & (C >= MO3_M) & (var_r > 0), v, np.nan)
    del pb, sb, qb, vb, ev, sv, qv, eo, so, qo, Ce, Se, Qe, Co, So, Qo, v, vb_var, C, S, Q, var_r

    # ---------- B4 (mean run length) -----------------------------------------
    sign = np.where(r3 > 0, 1, np.where(r3 < 0, -1, 0))
    nz = sign != 0
    prev_same = np.zeros(n, dtype=bool)
    prev_same[1:] = nz[1:] & nz[:-1] & (sign[1:] == sign[:-1])
    is_start = nz & ~prev_same
    p_nz = prefix_mask(nz)
    p_st = prefix_mask(is_start)
    lo4 = np.maximum(pos - (W3_M - 1), 0)
    edge_start = (nz & ~is_start).astype(np.int64)   # 1 iff position continues a run from p-1
    n_bars = p_nz[pos + 1] - p_nz[lo4]
    n_runs = p_st[pos + 1] - p_st[lo4] + edge_start[lo4]
    v = np.where(n_runs > 0, n_bars / np.maximum(n_runs, 1), np.nan)
    out["m3_run_month"] = np.where(availM & (n_bars >= MO3_M) & (n_runs > 0), v, np.nan)
    del sign, nz, prev_same, is_start, p_nz, p_st, v, n_bars, n_runs

    # ---------- B6 (H1 ACF) ---------------------------------------------------
    res = acf_vec(PH, h_idx, WH_M - 2, MOH_M)
    out["h1_acf1_month"] = np.where(h_idx >= WH_M - 1, res, np.nan)
    del res, PH

    # ---------- C1/C2/C3 ------------------------------------------------------
    c_prev = shift1(c3)
    rbps = np.where(np.isfinite(c3) & (c3 > 0), 10000.0 * (h3 - l3) / c3, np.nan)
    tr = np.maximum.reduce([h3 - l3, np.abs(h3 - c_prev), np.abs(l3 - c_prev)])
    trbps = np.where(np.isfinite(c_prev) & (c_prev > 0) & np.isfinite(tr) & (tr > 0),
                     10000.0 * tr / c_prev, np.nan)
    sig_bps = 10000.0 * s3_prev
    c1 = rbps / sig_bps
    c1 = np.where(np.isfinite(s3_prev) & (s3_prev > 0), c1, np.nan)
    c2 = trbps / sig_bps
    c2 = np.where(np.isfinite(s3_prev) & (s3_prev > 0), c2, np.nan)
    tr_prev = shift1(trbps)
    c3d = 10000.0 * np.log(trbps / tr_prev)
    c3d = np.where(np.isfinite(trbps) & np.isfinite(tr_prev) & (trbps > 0) & (tr_prev > 0),
                   c3d, np.nan)
    for key, arr in (("m3_range_sigma_day", c1), ("m3_tr_sigma_day", c2),
                     ("m3_tr_expansion_day", c3d)):
        med = rolling_arr(arr, W3_D, MO_SHAPE, "median")
        out[key] = np.where(availD, med, np.nan)
        del med
    del c1, c2, c3d, rbps, tr, trbps, tr_prev, sig_bps, c_prev

    # ---------- D1..D5 --------------------------------------------------------
    rng = h3 - l3
    ok = np.isfinite(rng) & (rng > 0)
    den = np.maximum(rng, 1e-300)
    dd = [np.where(ok, np.abs(c3 - o3) / den, np.nan),
          np.where(ok, (h3 - np.maximum(o3, c3)) / den, np.nan),
          np.where(ok, (np.minimum(o3, c3) - l3) / den, np.nan),
          np.where(ok, (c3 - l3) / den, np.nan),
          np.where(ok, (c3 - o3) / den, np.nan)]
    for key, arr in (("m3_body_range_day", dd[0]), ("m3_up_wick_day", dd[1]),
                     ("m3_low_wick_day", dd[2]), ("m3_close_pos_day", dd[3]),
                     ("m3_body_dir_day", dd[4])):
        med = rolling_arr(arr, W3_D, MO_SHAPE, "median")
        out[key] = np.where(availD, med, np.nan)
        del med
    del dd, rng, ok, den

    # ---------- E1 / E5 -------------------------------------------------------
    cls3 = np.isfinite(s3_prev) & (s3_prev > 0)
    ext3 = np.zeros(n, dtype=np.int64)
    ext3[cls3] = (np.abs(r3[cls3]) > SHOCK_MULT * s3_prev[cls3]).astype(np.int64)
    p_ext3 = prefix_mask(ext3)
    p_cls3 = prefix_mask(cls3)
    loE = np.maximum(pos - (W3_M - 1), 0)
    n_ext = p_ext3[pos + 1] - p_ext3[loE]
    n_cls = p_cls3[pos + 1] - p_cls3[loE]
    v = np.where(n_cls > 0, n_ext / np.maximum(n_cls, 1), np.nan)
    out["m3_ext_rate_month"] = np.where(availM & (n_cls >= MO3_M), v, np.nan)
    p_pos = prefix_mask((ext3 == 1) & (r3 > 0))
    n_pos = p_pos[pos + 1] - p_pos[loE]
    v = np.where(n_ext > 0, n_pos / np.maximum(n_ext, 1), np.nan)
    out["m3_ext_sign_month"] = np.where(availM & (n_ext >= MO_EXT), v, np.nan)
    del v, n_pos, p_pos

    # ---------- E4 --------------------------------------------------------
    lo_j = np.maximum(j_idx - (W1_D - 1), 0)
    n_ext1 = p_ext1[j_idx + 1] - p_ext1[lo_j]
    n_cls1 = p_cls1[j_idx + 1] - p_cls1[lo_j]
    v = np.where(n_cls1 > 0, n_ext1 / np.maximum(n_cls1, 1), np.nan)
    out["m1_ext_rate_day"] = np.where((j_idx >= W1_D - 1) & (n_cls1 >= MO1_D), v, np.nan)
    del v, n_ext1, n_cls1, lo_j, p_ext1, p_cls1

    # ---------- E2/E3 ---------------------------------------------------------
    cnt4, s1_4, s2_4, s3_4, s4_4 = roll_sums4(r3, W3_M, MO3_M)
    mn = s1_4 / np.maximum(cnt4, 1)
    m2 = s2_4 / np.maximum(cnt4, 1) - mn * mn
    m3_ = s3_4 / np.maximum(cnt4, 1) - 3.0 * mn * (s2_4 / np.maximum(cnt4, 1)) + 2.0 * mn ** 3
    m4 = s4_4 / np.maximum(cnt4, 1) - 4.0 * mn * (s3_4 / np.maximum(cnt4, 1)) \
        + 6.0 * mn ** 2 * (s2_4 / np.maximum(cnt4, 1)) - 3.0 * mn ** 4
    okm = availM & (cnt4 >= MO3_M) & (m2 > 0)
    out["m3_skew_month"] = np.where(okm, m3_ / np.power(np.maximum(m2, 0.0), 1.5), np.nan)
    out["m3_kurtosis_month"] = np.where(okm, m4 / (np.maximum(m2, 0.0) ** 2) - 3.0, np.nan)
    del cnt4, s1_4, s2_4, s3_4, s4_4, mn, m2, m3_, m4, okm

    # ---------- F1 ------------------------------------------------------------
    hit = np.zeros(n, dtype=np.int64)
    for k in range(1, 6):
        hit[k:] |= ext3[:n - k]
    c_hit = np.where(ext3 == 1, hit, 0)
    p_hit = prefix_mask(c_hit)
    loF = np.maximum(pos - (W3_M - 1), 0)
    hiF = pos - 5
    hiFok = pos >= 5
    n_hit = p_hit[np.maximum(hiF, 0)] - p_hit[loF]
    n_elig = p_ext3[np.maximum(hiF, 0)] - p_ext3[loF]
    n_hit = np.where(hiFok, n_hit, 0.0)
    n_elig = np.where(hiFok, n_elig, 0.0)
    v = np.where(n_elig > 0, n_hit / np.maximum(n_elig, 1), np.nan)
    # availability: full 14400-position window AND the +5 co-occurrence lag
    f1_avail = availM & (pos >= W3_M + 4)
    out["m3_storm_clust_month"] = np.where(f1_avail & (n_elig >= MO_EXT), v, np.nan)
    del hit, c_hit, p_hit, v

    # ---------- F2 (P90 extreme run length) ----------------------------------
    rid = np.full(n, -1, dtype=np.int64)
    run_s = []
    run_e = []
    cur = -1
    for p in range(n):
        if ext3[p]:
            if p > 0 and ext3[p - 1]:
                rid[p] = cur
                run_e[cur] = p
            else:
                cur += 1
                rid[p] = cur
                run_s.append(p)
                run_e.append(p)
    res = np.full(n, np.nan)
    if cur >= 0 and n >= W3_M:
        seg_len = {}
        hist = {}
        for r_ in range(cur + 1):
            if run_s[r_] <= W3_M - 1:
                ln = int(min(run_e[r_], W3_M - 1) - run_s[r_] + 1)
                seg_len[r_] = ln
                hist[ln] = hist.get(ln, 0) + 1
        keys = sorted(hist)

        def p90_now():
            tot = sum(hist.values())
            if tot == 0:
                return np.nan
            k = 0.9 * (tot - 1)
            low = int(np.floor(k))
            frac = k - low
            cum = 0
            v_lo = None
            for ln in sorted(hist):
                if hist[ln] == 0:
                    continue
                cum += hist[ln]
                if v_lo is None and cum >= low + 1:
                    v_lo = ln
                    if frac == 0.0:
                        return float(ln)
                if frac > 0.0 and v_lo is not None and cum >= int(np.ceil(k)) + 1:
                    return v_lo + frac * (ln - v_lo)
            return float(v_lo) if v_lo is not None else np.nan

        for i in range(W3_M - 1, n):
            if i > W3_M - 1:
                p_old = i - W3_M
                if ext3[p_old]:
                    rv = int(rid[p_old])
                    L = seg_len[rv]
                    hist[L] -= 1
                    if hist[L] == 0:
                        del hist[L]
                    L -= 1
                    if L >= 1:
                        seg_len[rv] = L
                        hist[L] = hist.get(L, 0) + 1
                    else:
                        del seg_len[rv]
                p_new = i
                if ext3[p_new]:
                    rv = int(rid[p_new])
                    if rv in seg_len:
                        L = seg_len[rv] + 1
                        hist[L - 1] -= 1
                        if hist[L - 1] == 0:
                            del hist[L - 1]
                        seg_len[rv] = L
                        hist[L] = hist.get(L, 0) + 1
                    else:
                        seg_len[rv] = 1
                        hist[1] = hist.get(1, 0) + 1
            if availM[i] and n_ext[i] >= MO_EXT:
                res[i] = p90_now()
    out["m3_storm_p90_run_month"] = res
    del res, rid, run_s, run_e
    if cur >= 0 and n >= W3_M:
        del seg_len, hist

    # ---------- F3 (median extreme spacing) ----------------------------------
    pos_e = np.flatnonzero(ext3 == 1)
    res = np.full(n, np.nan)
    n_ev = len(pos_e)
    if n_ev >= 2:
        gaps = np.diff(pos_e).astype(np.int64)
        events = []
        for k in range(n_ev - 1):
            g = int(gaps[k])
            if g >= W3_M:          # can never be active inside a W-window
                continue
            events.append((int(pos_e[k]) + g, 1, g))   # active when second ext enters
            events.append((int(pos_e[k]) + W3_M, -1, g))  # inactive when first ext leaves
        events.sort(key=lambda e: e[0])
        fw = Fenwick(W3_M)
        # unique event times >= W-1, plus sentinel
        change_times = sorted({e[0] for e in events})
        ev_i = 0
        ne_ev = len(events)

        def median_active():
            tot = fw.total()
            if tot == 0:
                return np.nan
            k = 0.5 * (tot - 1)
            low = int(np.floor(k))
            frac = k - low
            v_lo = fw.select(low) + 1
            if frac == 0.0:
                return float(v_lo)
            v_hi = fw.select(int(np.ceil(k))) + 1
            return v_lo + frac * (v_hi - v_lo)

        prev_t = W3_M - 1
        # state at prev_t
        while ev_i < ne_ev and events[ev_i][0] <= prev_t:
            fw.add(events[ev_i][2] - 1, events[ev_i][1])
            ev_i += 1
        for ct in change_times:
            if ct < W3_M - 1 or ct > n - 1:
                continue
            mv = median_active()
            hi_fill = min(ct, n) - 1
            if prev_t <= hi_fill:
                res[prev_t:hi_fill + 1] = mv
            while ev_i < ne_ev and events[ev_i][0] <= ct:
                fw.add(events[ev_i][2] - 1, events[ev_i][1])
                ev_i += 1
            prev_t = ct + 1
        if prev_t <= n - 1:
            while ev_i < ne_ev and events[ev_i][0] <= n - 1:
                fw.add(events[ev_i][2] - 1, events[ev_i][1])
                ev_i += 1
            res[prev_t:] = median_active()
    out["m3_ext_spacing_month"] = np.where(availM & (n_ext >= MO_EXT), res, np.nan)
    del res, pos_e

    # ================= assemble + write ======================================
    names = [k for k in out if k not in ("ts_min", "bar_id")]
    assert len(out) == 27, len(out)
    assert sorted(names) == sorted([f[0] for f in FEATURES])
    table = pa.table({k: pa.array(v) for k, v in out.items()})
    out_path = os.path.join(OUT, "XAUUSD_FEATURES_V2.parquet")
    pq.write_table(table, out_path, compression="snappy")
    print("parquet written:", out_path, os.path.getsize(out_path), "bytes", flush=True)

    n_valid = {}
    n_nan = {}
    for name, _, _, _, _, _, _ in FEATURES:
        col = out[name]
        n_valid[name] = int(np.isfinite(col).sum())
        n_nan[name] = int(np.isnan(col).sum())

    meta = {
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "engine": "feature_engine_v2.py",
        "engine_version": "V2_STEP3.3_1",
        "contract": "PHASE3_V2_DATA_CONTRACT.md (FROZEN)",
        "specification": "PHASE3_V2_FEATURE_SPEC.md (FROZEN)",
        "authority": "SPECIFICATION",
        "dataset": out_path,
        "rows": int(n),
        "columns": list(out.keys()),
        "master_sha256": MASTER_SHA,
        "master_rows": MASTER_ROWS,
        "m3_grid": {"file": M3_GRID, "sha256": M3_SHA, "rows": M3_ROWS},
        "h1_grid": {"file": H1_GRID, "sha256": H1_SHA, "rows": H1_ROWS},
        "row_anchor": "M3 grid (bar_id ascending; ts_min = bucket start, UTC)",
        "m1_alignment": "endM1(t) = last M1 minute <= T+2 (closed M3 bucket)",
        "h1_alignment": "h(t) = closed H1 bucket containing minute T+2",
        "volume": "NOT_LOADED (volume column never read - L1)",
        "window_basis": "position windows [i-W+1, i] on validated grids; gaps preserved",
        "pit_policy": "past-only; no centered window; no t+k; no global normalization",
        "nan_policy": "NaN preserved exactly as specified; no fill, no backfill",
        "features": [],
    }
    for name, fam, tfs, win, mo, units, ref in FEATURES:
        meta["features"].append({
            "name": name, "family": fam, "timeframe_source": tfs,
            "formula/version": "SPEC_V2_FROZEN_2026-09-06", "spec_ref": ref,
            "window": win, "min_obs": mo, "units": units,
            "status": "OK",
            "n_valid": n_valid[name], "n_nan": n_nan[name],
        })
    meta_path = os.path.join(OUT, "features_v2_meta.json")
    with open(meta_path, "w") as fh:
        json.dump(meta, fh, indent=2)
    print("meta written:", meta_path, flush=True)

    summary = {
        "rows": int(n),
        "cols": len(out),
        "features_present": len(names),
        "all_25": len(names) == 25,
        "ts_monotonic": bool(np.all(np.diff(t3) > 0)),
        "no_dup_bar_id": int(np.unique(bid3).size) == n,
        "matches_m3_grid": bool(np.array_equal(t3, pq.read_table(out_path,
                                    columns=["ts_min"])["ts_min"].to_numpy())),
        "volume_loaded": "volume" in out,
        "nan_summary": {k: {"n_valid": n_valid[k], "n_nan": n_nan[k],
                            "nan_rate": round(n_nan[k] / n, 5)} for k in names},
    }
    print(json.dumps(summary, indent=2, default=str))
    print("elapsed", round(time.time() - t0, 1), "s", flush=True)


if __name__ == "__main__":
    main()
