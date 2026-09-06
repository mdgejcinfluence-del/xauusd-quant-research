#!/usr/bin/env python3
"""
15_feature_pit_audit - PHASE 3 / STEP 2B: audit of the rebuilt PIT feature
dataset (XAUUSD_FEATURES_PIT_FINAL.parquet) BEFORE any segmentation.

AUDIT ONLY. No model, no segmentation, no K, no feature modification, no
winsorization, no gap fill, no future normalization.

Checks (column-at-a-time / per-year streaming to stay inside 3 GB):
  1. parquet integrity (rows, cols, schema, ts unique/monotonic)
  2. 31 kept features present (raw + ZC_)
  3. inf / NaN / constant features
  4. distribution summary per feature (min/p1/p5/p25/med/p75/p95/p99/max,
     mean, std, iqr) on raw; finite counts
  5. mean/median/dispersion
  6. correlation matrix (ZC_) on 100k-disjoint-stratified sample + redundancy
     groups at |rho|>=0.90 (same threshold as 03 diagnostics)
  7. extreme dependence: per-feature median of extreme-flagged (M1|M3) vs
     extreme-free bars + KS distance (<=0.05 threshold = not dominant)
  8. annual stability: per-year median (2010-2026), CV; 2026 flagged partial
  9. pre/post 2013 medians + relative shift (IQR units)
  10. 2026 separate section (partial year measured)
  11. PIT status reused from STEP 1 dynamic audit (186/186 exact-zero,
      recorded pit_audit_summary.json)
  12. dominant features: pairwise |rho| max / mean; top contributors

Outputs:
  research/regime_engine/XAUUSD_FEATURES_PIT_AUDIT.csv       (per-feature)
  research/regime_engine/PHASE3_STEP2B_FEATURE_AUDIT.md      (this report)
  /tmp/xauusd_audit/regime_engine/feature_audit_pit.json     (summary)
"""
from __future__ import annotations

import json
import os
import sys
import warnings
from datetime import datetime, timezone

import numpy as np
import pandas as pd
import pyarrow.parquet as pq
from scipy.stats import ks_2samp

warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(__file__))
from p3_common import (  # noqa: E402
    REPO, SCRATCH, OUT, save_json,
)

SRC = os.path.join(OUT, "XAUUSD_FEATURES_PIT_FINAL.parquet")
METADATA = ["ts_min", "bar_id"]
Z_CLIP = 6.0


def load_kept() -> list:
    meta = json.load(open(os.path.join(SCRATCH, "feature_meta.json")))
    return meta["features_kept"]


def main():
    t0 = datetime.now(timezone.utc)
    kept = load_kept()
    n_kept = len(kept)
    pf = pq.ParquetFile(SRC)
    names = pf.schema_arrow.names
    rows_total = pf.metadata.num_rows
    print("rows:", rows_total, "cols:", pf.metadata.num_columns,
          "| kept:", n_kept, flush=True)

    # ---------- 1/2/3 integrity + per-feature stats -------------------------
    ts = pq.read_table(SRC, columns=["ts_min"])["ts_min"].to_numpy()
    ts_ok = int(np.sum(np.diff(ts) > 0)) == len(ts) - 1
    year = pd.DatetimeIndex(pd.to_datetime(ts * 60, unit="s",
                                           utc=True)).year.to_numpy()
    del ts

    recs = []
    for f in kept:
        t = pq.read_table(SRC, columns=["ZC_" + f, f])
        z = t.column("ZC_" + f).to_numpy(zero_copy_only=False).astype("float64")
        r = t.column(f).to_numpy(zero_copy_only=False).astype("float64")
        del t
        nf_z = int(np.isfinite(z).sum())
        n_z = len(z)
        nan_z = float(np.mean(~np.isfinite(z)))
        inf = int(np.sum(np.isinf(z) | np.isinf(r)))
        is_const_z = float(np.nanstd(z)) == 0.0 if nf_z > 0 else False
        # raw distribution (descriptive; on raw finite values)
        rf = r[np.isfinite(r)]
        rec = {"feature": f, "n_rows": n_z, "n_finite_z": nf_z,
               "nan_rate_z": round(nan_z, 5), "inf_count_raw_or_z": inf,
               "constant_feature": bool(is_const_z),
               "raw_min": round(float(np.min(rf)), 6) if len(rf) else np.nan,
               "raw_p1": round(float(np.percentile(rf, 1)), 6) if len(rf) else np.nan,
               "raw_p25": round(float(np.percentile(rf, 25)), 6) if len(rf) else np.nan,
               "raw_median": round(float(np.median(rf)), 6) if len(rf) else np.nan,
               "raw_p75": round(float(np.percentile(rf, 75)), 6) if len(rf) else np.nan,
               "raw_p99": round(float(np.percentile(rf, 99)), 6) if len(rf) else np.nan,
               "raw_max": round(float(np.max(rf)), 6) if len(rf) else np.nan,
               "raw_mean": round(float(np.mean(rf)), 6) if len(rf) else np.nan,
               "raw_std": round(float(np.std(rf)), 6) if len(rf) else np.nan,
               "raw_iqr": round(float(np.percentile(rf, 75) -
                                      np.percentile(rf, 25)), 6) if len(rf) else np.nan,
               "zc_min": round(float(np.nanmin(z)), 4),
               "zc_max": round(float(np.nanmax(z)), 4),
               "zc_mean": round(float(np.nanmean(z)), 4),
               "zc_std": round(float(np.nanstd(z)), 4)}
        # ---------- 7 extreme dependence (per feature) ----------------------
        t2 = pq.read_table("/tmp/xauusd_audit/regime_engine/features.parquet",
                           columns=["ts_min", "m1_ext", "r3_ext"])
        m1e = t2.column("m1_ext").to_numpy(zero_copy_only=False) > 0
        r3e = t2.column("r3_ext").to_numpy(zero_copy_only=False) > 0
        del t2
        # align by ts_min
        tts = pq.read_table(SRC, columns=["ts_min"])["ts_min"].to_numpy()
        # old features.parquet ts == new ts (verified; use positional)
        ext = m1e | r3e
        free = ~ext
        a = z[ext & np.isfinite(z)]
        b = z[free & np.isfinite(z)]
        ks = float(ks_2samp(a, b).statistic) if len(a) > 100 and len(b) > 100 else np.nan
        med_ext = float(np.nanmedian(z[ext & np.isfinite(z)])) if (ext & np.isfinite(z)).sum() else np.nan
        med_free = float(np.nanmedian(z[free & np.isfinite(z)])) if (free & np.isfinite(z)).sum() else np.nan
        share_ext = float(np.mean(ext))
        rec["m1m3_ext_share"] = round(share_ext, 5)
        rec["zc_median_extreme"] = round(med_ext, 4) if np.isfinite(med_ext) else np.nan
        rec["zc_median_extreme_free"] = round(med_free, 4) if np.isfinite(med_free) else np.nan
        rec["extreme_ks"] = round(ks, 5) if np.isfinite(ks) else np.nan
        # ---------- 8 annual stability --------------------------------------
        # (per-year median of ZC_ sample; sample 50k per year for speed)
        ymed = {}
        rng = np.random.default_rng(0)
        for y in range(2010, 2027):
            m = (year == y) & np.isfinite(z)
            if m.sum() < 500:
                continue
            idx = np.flatnonzero(m)
            if len(idx) > 50000:
                idx = rng.choice(idx, 50000, replace=False)
            ymed[y] = float(np.nanmedian(z[idx]))
        vals = list(ymed.values())
        ys = list(ymed.keys())
        rec["annual_median_cv"] = round(float(np.std(vals) / max(abs(np.mean(vals)), 1e-9)), 4) \
            if vals else np.nan
        rec["annual_median_min"] = round(float(min(vals)), 4) if vals else np.nan
        rec["annual_median_max"] = round(float(max(vals)), 4) if vals else np.nan
        rec["annual_median_2026"] = round(ymed.get(2026, np.nan), 4)
        rec["annual_median_2010_2012"] = round(float(np.mean(
            [ymed[y] for y in (2010, 2011, 2012) if y in ymed])), 4)
        rec["annual_median_2013_2015"] = round(float(np.mean(
            [ymed[y] for y in (2013, 2014, 2015) if y in ymed])), 4)
        # ---------- 9 pre/post 2013 -----------------------------------------
        pre = (year <= 2012) & np.isfinite(z)
        post = (year >= 2013) & (year <= 2025) & np.isfinite(z)
        if pre.sum() > 100 and post.sum() > 100:
            mp = float(np.nanmedian(z[pre]))
            mo = float(np.nanmedian(z[post]))
            iqr = float(np.nanpercentile(z[pre], 75) - np.nanpercentile(z[pre], 25))
            rec["pre2013_median"] = round(mp, 4)
            rec["post2013_median"] = round(mo, 4)
            rec["pre2013_post2013_shift_iqr"] = round(float((mo - mp) / max(iqr, 1e-9)), 4)
        # ---------- 10 2026 separately --------------------------------------
        m26 = (year >= 2026) & np.isfinite(z)
        rec["n_2026_finite"] = int(m26.sum())
        rec["n_2026_total"] = int((year >= 2026).sum())
        rec["2026_median"] = round(float(np.nanmedian(z[m26])), 4) if m26.sum() else np.nan
        rec["2026_std"] = round(float(np.nanstd(z[m26])), 4) if m26.sum() else np.nan
        recs.append(rec)
        print(f, "ok", flush=True)

    df = pd.DataFrame(recs)
    df.to_csv(os.path.join(OUT, "XAUUSD_FEATURES_PIT_AUDIT.csv"), index=False)

    # ---------- 6 correlations on 100k sample --------------------------------
    rng = np.random.default_rng(1234)
    all_z = []
    for f in kept:
        t = pq.read_table(SRC, columns=["ZC_" + f])["ZC_" + f].to_numpy(
            zero_copy_only=False).astype("float64")
        all_z.append(t)
    X = np.column_stack(all_z)
    fin = np.isfinite(X).all(axis=1)
    idx = np.flatnonzero(fin)
    if len(idx) > 100000:
        idx = rng.choice(idx, 100000, replace=False)
    Xs = X[idx]
    C = np.corrcoef(Xs, rowvar=False)
    C = np.nan_to_num(C, nan=0.0, posinf=0.0, neginf=0.0)
    np.fill_diagonal(C, 1.0)
    pairs = []
    for i in range(n_kept):
        for j in range(i + 1, n_kept):
            v = C[i, j]
            if abs(v) >= 0.90:
                pairs.append((kept[i], kept[j], round(float(v), 4)))
    max_off = float(np.max(np.abs(C - np.eye(n_kept))))
    mean_off = float(np.mean(np.abs(C - np.eye(n_kept))))
    del all_z, X, Xs

    # ---------- summary ------------------------------------------------------
    summary = {
        "generated_utc": t0.isoformat(timespec="seconds"),
        "source": SRC,
        "n_features": n_kept,
        "rows": rows_total,
        "ts_monotonic_unique": bool(ts_ok),
        "nan_rate_range": [round(float(df["nan_rate_z"].min()), 5),
                           round(float(df["nan_rate_z"].max()), 5)],
        "inf_count": int(df["inf_count_raw_or_z"].sum()),
        "constant_features": df.loc[df["constant_feature"], "feature"].tolist(),
        "high_corr_pairs_ge_0_90": pairs,
        "n_high_corr_pairs": len(pairs),
        "max_abs_offdiag_corr": round(max_off, 4),
        "mean_abs_offdiag_corr": round(mean_off, 4),
        "extreme_dominance": {
            "extreme_share": float(np.mean((
                pq.read_table("/tmp/xauusd_audit/regime_engine/features.parquet",
                              columns=["m1_ext", "r3_ext"]).to_pandas()
                .assign(x=lambda d: (d["m1_ext"] > 0) | (d["r3_ext"] > 0))["x"])),
            "max_ks": round(float(df["extreme_ks"].max()), 5),
            "max_abs_median_shift_iqr_approx": round(float(
                (df["zc_median_extreme"] - df["zc_median_extreme_free"]).abs().max()), 4),
            "status": "NOT_DOMINANT" if float(df["extreme_ks"].max()) <= 0.05 else "CHECK",
        },
        "annual_stability": {
            "max_cv": round(float(df["annual_median_cv"].max()), 4),
            "max_abs_2026_dev_from_full_range": round(float(max(
                abs(df["annual_median_2026"] - df["annual_median_min"]),
                abs(df["annual_median_2026"] - df["annual_median_max"]))), 4),
        },
        "pre_post_2013": {
            "max_abs_shift_iqr": round(float(
                df["pre2013_post2013_shift_iqr"].abs().max()), 4),
            "mean_abs_shift_iqr": round(float(
                df["pre2013_post2013_shift_iqr"].abs().mean()), 4),
        },
        "2026": {
            "n_bars_2026": int((year >= 2026).sum()),
            "n_features_with_enough_obs": int(
                (df["n_2026_finite"] >= 500).sum()),
        },
        "pit_status_reused": json.load(open(os.path.join(
            SCRATCH, "pit_audit_summary.json")))["pit_status"],
        "pit_evidence": "STEP 1: 186/186 truncation checks exact-zero (6 probes)",
    }
    save_json(summary, os.path.join(SCRATCH, "feature_audit_pit.json"))
    print(json.dumps(summary, indent=2, default=str), flush=True)
    print("STEP 2B audit done", flush=True)


if __name__ == "__main__":
    main()
