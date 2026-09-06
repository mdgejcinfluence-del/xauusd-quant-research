#!/usr/bin/env python3
"""
PHASE 2 - scoring, deliverables and figures.

SCORING CONTRACT (fixed BEFORE any metric was inspected - see section 15-17 of
the report for the rationale; no weight was tuned after seeing a result):

  S  SIGNAL / NOISE            0.25
  A  AMPLITUDE / COST          0.20
  C  STRUCTURAL PRESERVATION   0.25
  D  TEMPORAL STABILITY        0.15
  E  DATA CONTINUITY           0.05
  F  INFORMATION RETENTION     0.10

Every component is a min-max normalisation across the 12 granularities
(sometimes after a log10 transform, always declared), so 1.0 = best of the
grid and 0.0 = worst of the grid on that component.  Normalisation is
relative to the grid, NOT an absolute quality judgement.

No strategy, no backtest, no profit, no Sharpe, no drawdown, no hit rate,
no expectancy, no regime, no volume anywhere in this file.

Usage:
  python score_and_render.py --metrics /tmp/xauusd_audit/metrics_tf.json \
                             --tfdir  /tmp/xauusd_audit/timeframes \
                             --outdir research/timeframe_audit
"""

from __future__ import annotations

import argparse
import csv
import json
import os

import numpy as np
import pyarrow.parquet as pq

GRID = ["M1", "M2", "M3", "M4", "M5", "M10", "M15", "M20", "M30", "H1", "H2", "H4"]
K = {"M1": 1, "M2": 2, "M3": 3, "M4": 4, "M5": 5, "M10": 10, "M15": 15,
     "M20": 20, "M30": 30, "H1": 60, "H2": 120, "H4": 240}

# --- composite weights (fixed a priori) ------------------------------------ #
W = {"S": 0.25, "A": 0.20, "C": 0.25, "D": 0.15, "E": 0.05, "F": 0.10}


def mm(values: dict, invert=False, log=False):
    """Min-max normalisation across the grid. Returns {tf: score in [0,1]}."""
    v = {k: (np.log10(x) if (log and x is not None and x > 0) else x)
         for k, x in values.items()}
    good = {k: x for k, x in v.items() if x is not None and np.isfinite(x)}
    if not good:
        return {k: float("nan") for k in values}
    lo, hi = min(good.values()), max(good.values())
    if hi == lo:
        return {k: (0.5 if k in good else float("nan")) for k in values}
    out = {}
    for k in values:
        x = v[k]
        if x is None or not np.isfinite(x):
            out[k] = float("nan")
            continue
        s = (x - lo) / (hi - lo)
        out[k] = (1.0 - s) if invert else s
    return out


def cv(vals):
    vals = [v for v in vals if v is not None and np.isfinite(v)]
    if len(vals) < 3:
        return float("nan")
    m = float(np.mean(vals))
    s = float(np.std(vals, ddof=1))
    if m == 0:
        return float("nan")
    return abs(s / m)


def stability_score(per_year: dict, tf: str, key, path=None):
    vals = []
    for y, d in per_year.items():
        if y == "2026":
            continue
        v = d
        for p in (path or []):
            v = v.get(p, {}) if isinstance(v, dict) else None
            if v is None:
                break
        if v is None:
            continue
        v = v.get(key)
        if v is not None and np.isfinite(v):
            vals.append(v)
    c = cv(vals)
    if not np.isfinite(c):
        return float("nan"), float("nan"), len(vals)
    return 1.0 / (1.0 + c), c, len(vals)


# --------------------------------------------------------------------------- #
def build_scores(M: dict) -> dict:
    tf = M["timeframes"]
    years = [str(y) for y in range(2010, 2026)]

    # ---------------- S : signal / noise -----------------------------------
    disp_acf1 = {}
    for t in GRID:
        v = [tf[t]["by_year"][y]["acf"]["lag1"] for y in years
             if y in tf[t]["by_year"] and tf[t]["by_year"][y]["acf"]["lag1"]
             is not None and np.isfinite(tf[t]["by_year"][y]["acf"]["lag1"])]
        disp_acf1[t] = float(np.std(v, ddof=1)) if len(v) > 3 else float("nan")
    var_stab = {}
    for t in GRID:
        v = [tf[t]["by_year"][y]["returns"]["std"] for y in years
             if y in tf[t]["by_year"] and tf[t]["by_year"][y]["returns"]["std"]
             is not None]
        c = cv(v)
        var_stab[t] = (1.0 / (1.0 + c)) if np.isfinite(c) else float("nan")

    S1 = mm(disp_acf1, invert=True)                       # stability of ACF(1)
    S2 = mm({t: 1.0 - tf[t]["full"]["sign_change_freq"] for t in GRID})
    S3 = mm({t: tf[t]["full"]["runs"]["mean_run"] for t in GRID})
    S4 = mm({t: tf[t]["full"]["de_tf_h10"] for t in GRID})
    S5 = mm(var_stab)
    S6 = mm({t: tf[t]["full"]["returns"]["excess_kurtosis"] for t in GRID},
            invert=True, log=True)
    Sw = {"S1_acf_stability": (0.15, S1), "S2_low_alternation": (0.20, S2),
          "S3_run_persistence": (0.15, S3), "S4_directional_efficiency": (0.20, S4),
          "S5_variance_stability": (0.15, S5), "S6_tail_stability": (0.15, S6)}

    # ---------------- A : amplitude / cost ---------------------------------
    costs = {name: val for name, val in M["cost_scenarios"]}
    c3 = costs["COST_SCENARIO_3"]
    c5 = costs["COST_SCENARIO_5"]
    exceed = {}      # fraction of bars whose range exceeds the largest cost
    for t in GRID:
        tab = pq.read_table(os.path.join(M["_tfdir"], f"XAUUSD_{t}.parquet"),
                            columns=["high", "low"])
        rng = (tab.column("high").to_numpy().astype("float64") -
               tab.column("low").to_numpy().astype("float64"))
        frac = (rng > c5).mean()
        frac = float(frac) if np.isfinite(frac) else float("nan")
        exceed[t] = frac
    A1 = mm({t: tf[t]["full"]["amplitude"]["range_bps"]["median"] for t in GRID},
            log=True)
    A2 = mm({t: tf[t]["full"]["amplitude"]["range_bps"]["p90"] for t in GRID},
            log=True)
    A3 = mm({t: tf[t]["full"]["amplitude"]["range_usd"]["median"] / c3
             for t in GRID}, log=True)
    A4 = {}
    for t in GRID:
        v = [tf[t]["by_year"][y]["amplitude"]["range_bps"]["median"]
             for y in years if y in tf[t]["by_year"]]
        c = cv(v)
        A4[t] = (1.0 / (1.0 + c)) if np.isfinite(c) else float("nan")
    A4 = mm(A4)
    A5 = mm(exceed)
    Aw = {"A1_median_range": (0.25, A1), "A2_p90_range": (0.20, A2),
          "A3_cost_ratio_mid_scenario": (0.25, A3),
          "A4_cost_ratio_stability": (0.15, A4),
          "A5_cost_tolerance": (0.15, A5)}

    # ---------------- C : structural preservation vs the M1 substrate ------
    n_m1 = tf["M1"]["full"]["bars"]
    C1 = mm({t: tf[t]["full"]["bars"] / n_m1 for t in GRID}, log=True)
    C2 = mm({t: 1.0 / K[t] for t in GRID}, log=True)
    C3 = mm({t: 1.0 / max(tf[t]["intrabar"]["m1_pivots_per_bar"], 1e-9)
             for t in GRID}, log=True)
    Cw = {"C1_observations_retained": (0.40, C1),
          "C2_timing_precision": (0.35, C2),
          "C3_swing_resolution": (0.25, C3)}

    # ---------------- D : temporal stability --------------------------------
    D1 = mm({t: stability_score(tf[t]["by_year"], t, "lag1", ["acf"])[0]
             for t in GRID})
    D2 = mm({t: stability_score(tf[t]["by_year"], t, "sign_change_freq")[0]
             for t in GRID})
    D3 = mm({t: stability_score(tf[t]["by_year"], t, "median",
                                ["amplitude", "range_bps"])[0] for t in GRID})
    D4 = mm({t: stability_score(tf[t]["by_year"], t, "de_tf_h10")[0]
             for t in GRID})
    Dw = {"D1_acf1_stability": (0.30, D1), "D2_alternation_stability": (0.25, D2),
          "D3_range_stability": (0.25, D3), "D4_efficiency_stability": (0.20, D4)}

    # ---------------- E : data continuity -----------------------------------
    E1 = mm({t: 1.0 - tf[t]["full"]["integrity"]["bars_with_internal_data_gap"]
             for t in GRID})
    E2 = mm({t: 1.0 - tf[t]["full"]["integrity"]["bars_with_internal_market_break"]
             for t in GRID})
    Ew = {"E1_no_internal_data_gap": (0.60, E1),
          "E2_no_internal_market_break": (0.40, E2)}

    # ---------------- F : information retention ------------------------------
    F1 = mm({t: tf[t]["intrabar"]["path_retention_ratio"] for t in GRID})
    F2 = mm({t: 1.0 / (1.0 + tf[t]["intrabar"]["mean_intrabar_reversals"])
             for t in GRID}, log=True)
    F3 = mm({t: tf[t]["full"]["integrity"]["contiguous_step_rate"] for t in GRID})
    Fw = {"F1_path_retention": (0.45, F1), "F2_reversal_retention": (0.30, F2),
          "F3_series_continuity": (0.25, F3)}

    comps = {"S": (W["S"], Sw), "A": (W["A"], Aw), "C": (W["C"], Cw),
             "D": (W["D"], Dw), "E": (W["E"], Ew), "F": (W["F"], Fw)}
    scores = {}
    for t in GRID:
        row = {}
        for grp, (gw, parts) in comps.items():
            val = 0.0
            wsum = 0.0
            for cname, (w, d) in parts.items():
                x = d[t]
                row[cname] = x
                if x is not None and np.isfinite(x):
                    val += w * x
                    wsum += w
            row[grp] = val / wsum if wsum > 0 else float("nan")
        row["GQS"] = sum(W[g] * row[g] for g in "SACDEF"
                         if np.isfinite(row[g])) / \
            sum(W[g] for g in "SACDEF" if np.isfinite(row[g]))
        scores[t] = row
    order = sorted(GRID, key=lambda t: -scores[t]["GQS"])
    for i, t in enumerate(order, 1):
        scores[t]["rank"] = i
    return {"components": scores, "rank_order": order,
            "weights": {"composite": W,
                        "S": {k: v[0] for k, v in Sw.items()},
                        "A": {k: v[0] for k, v in Aw.items()},
                        "C": {k: v[0] for k, v in Cw.items()},
                        "D": {k: v[0] for k, v in Dw.items()},
                        "E": {k: v[0] for k, v in Ew.items()},
                        "F": {k: v[0] for k, v in Fw.items()}},
            "raw": {"acf1_dispersion": disp_acf1, "var_stability": var_stab,
                    "exceed_cost5": exceed}}


# =========================================================================== #
#  CSV DELIVERABLES
# =========================================================================== #
def write_csv(path, header, rows):
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        w.writerows(rows)


def csv_timeframe_comparison(M, outdir):
    tf = M["timeframes"]
    header = ["TIMEFRAME", "MINUTES", "BARS", "MEAN_M1_PER_BAR",
              "FIRST_TS_UTC", "LAST_TS_UTC",
              "ACF_LAG1", "ACF_LAG2", "ACF_LAG3", "ACF_LAG4", "ACF_LAG8",
              "SIGN_CHANGE_FREQ", "MEAN_RUN", "MEDIAN_RUN", "P90_RUN",
              "REVERSAL_FREQ", "MEDIAN_RECOVERY_RATIO", "FULL_RECOVERY_RATE",
              "MEAN_RECOVERY_DELAY_BARS", "MEAN_RECOVERY_DELAY_MIN",
              "NO_RECOVERY_WITHIN_20_BARS",
              "RET_STD_BPS", "ANN_VOL_PCT", "RET_SKEW", "RET_EXCESS_KURTOSIS",
              "TAIL_2S", "TAIL_3S",
              "DE_TF_H5", "DE_TF_H10", "DE_TF_H20",
              "DE_M1_H5", "DE_M1_H10", "DE_M1_H20",
              "NEW_EXTREME_RATE_20", "BREAKOUT_RATE_20",
              "BREAKOUT_PERSISTENCE", "REINTEGRATION_RATE_5",
              "RANGE_EXPANSION_STD_LOG", "MEAN_BODY_OVER_RANGE",
              "MEDIAN_RANGE_USD", "MEAN_RANGE_USD", "P25_RANGE_USD",
              "P75_RANGE_USD", "P90_RANGE_USD", "P95_RANGE_USD", "P99_RANGE_USD",
              "MEDIAN_RANGE_BPS", "P75_RANGE_BPS", "P90_RANGE_BPS",
              "P95_RANGE_BPS", "P99_RANGE_BPS",
              "MEDIAN_BODY_BPS", "P90_BODY_BPS",
              "BARS_WITH_INTERNAL_DATA_GAP_PCT",
              "BARS_WITH_INTERNAL_MARKET_BREAK_PCT", "CONTIGUOUS_STEP_RATE_PCT",
              "VARIANCE_RATIO_VS_M1", "MEAN_PRICE_USD"]
    var_m1 = tf["M1"]["full"]["returns"]["std"] ** 2
    rows = []
    for t in GRID:
        f = tf[t]["full"]
        a, r, am = f["acf"], f["returns"], f["amplitude"]
        rv, st = f["reversal"], f["structure"]
        it = f["integrity"]
        mn = tf[t]["minutes"]
        rows.append([
            t, mn, f["bars"], round(it["mean_m1_per_bar"], 4),
            M["_manifest"][t]["first_ts"], M["_manifest"][t]["last_ts"],
            *[round(a[f"lag{l}"], 6) for l in (1, 2, 3, 4, 8)],
            round(f["sign_change_freq"], 6),
            round(f["runs"]["mean_run"], 4), round(f["runs"]["median_run"], 2),
            round(f["runs"]["p90_run"], 2),
            round(rv["reversal_freq"], 6), round(rv["median_recovery_ratio"], 6),
            round(rv["full_recovery_rate"], 6),
            round(rv["mean_recovery_delay"], 4),
            round(rv["mean_recovery_delay"] * mn, 3),
            round(rv["no_recovery_within_h"], 6),
            round(r["std"] * 1e4, 5), round(f["ann_vol"] * 100, 4),
            round(r["skew"], 5), round(r["excess_kurtosis"], 4),
            round(r["tail_2s"], 6), round(r["tail_3s"], 6),
            round(f["de_tf_h5"], 6), round(f["de_tf_h10"], 6),
            round(f["de_tf_h20"], 6),
            round(f["de_m1_h5"], 6) if f["de_m1_h5"] is not None else "",
            round(f["de_m1_h10"], 6) if f["de_m1_h10"] is not None else "",
            round(f["de_m1_h20"], 6) if f["de_m1_h20"] is not None else "",
            round(st["new_extreme_rate"], 6), round(st["breakout_rate"], 6),
            round(st["breakout_persistence"], 6),
            round(st["reintegration_rate_within_5"], 6),
            round(st["range_expansion_std_log"], 6),
            round(st["mean_body_over_range"], 6),
            round(am["range_usd"]["median"], 5), round(am["range_usd"]["mean"], 5),
            round(am["range_usd"]["p25"], 5), round(am["range_usd"]["p75"], 5),
            round(am["range_usd"]["p90"], 5), round(am["range_usd"]["p95"], 5),
            round(am["range_usd"]["p99"], 5),
            round(am["range_bps"]["median"], 4), round(am["range_bps"]["p75"], 4),
            round(am["range_bps"]["p90"], 4), round(am["range_bps"]["p95"], 4),
            round(am["range_bps"]["p99"], 4),
            round(am["body_bps"]["median"], 4), round(am["body_bps"]["p90"], 4),
            round(it["bars_with_internal_data_gap"] * 100, 5),
            round(it["bars_with_internal_market_break"] * 100, 5),
            round(it["contiguous_step_rate"] * 100, 4),
            round(r["std"] ** 2 / (mn * var_m1), 5),
            round(f["mean_price"], 3),
        ])
    write_csv(os.path.join(outdir, "XAUUSD_TIMEFRAME_COMPARISON.csv"),
              header, rows)


def csv_signal_noise(M, outdir):
    tf = M["timeframes"]
    header = ["TIMEFRAME", "MINUTES", "BARS",
              "ACF_LAG1", "ACF_LAG2", "ACF_LAG3", "ACF_LAG4", "ACF_LAG8",
              "SIGN_CHANGE_FREQ", "ULTRA_SHORT_REVERSAL_FREQ",
              "MEAN_RUN_BARS", "P90_RUN_BARS", "MAX_RUN_BARS",
              "MEAN_RUN_MINUTES", "MEDIAN_RECOVERY_RATIO",
              "MEAN_RECOVERY_RATIO_ROBUST", "FULL_RECOVERY_RATE",
              "FULL_RECOVERY_RATE_BIG_MOVES", "MEAN_RECOVERY_DELAY_BARS",
              "MEDIAN_RECOVERY_DELAY_BARS", "NO_RECOVERY_WITHIN_20_PCT",
              "RET_STD", "RET_STD_BPS", "ANN_VOL_PCT",
              "RET_MEDIAN_BPS", "RET_Q01_BPS", "RET_Q99_BPS",
              "SKEW", "EXCESS_KURTOSIS", "TAIL_FRAC_2S", "TAIL_FRAC_3S",
              "VARIANCE_RATIO_VS_M1", "VARIANCE_STABILITY_SCORE",
              "ACF1_INTERANNUAL_DISPERSION",
              "DE_TF_H5", "DE_TF_H10", "DE_TF_H20",
              "DE_M1_H5", "DE_M1_H10", "DE_M1_H20",
              "DE_TF_OVER_DE_M1_H10"]
    var_m1 = tf["M1"]["full"]["returns"]["std"] ** 2
    rows = []
    for t in GRID:
        f = tf[t]["full"]
        a, r, rv = f["acf"], f["returns"], f["reversal"]
        mn = tf[t]["minutes"]
        raw = M["_scores"]["raw"]
        de_ratio = (f["de_tf_h10"] / f["de_m1_h10"]
                    if f["de_m1_h10"] not in (None, 0) else "")
        rows.append([
            t, mn, f["bars"],
            *[round(a[f"lag{l}"], 6) for l in (1, 2, 3, 4, 8)],
            round(f["sign_change_freq"], 6), round(rv["reversal_freq"], 6),
            round(f["runs"]["mean_run"], 4), round(f["runs"]["p90_run"], 2),
            f["runs"]["max_run"],
            round(f["runs"]["mean_run"] * mn, 3),
            round(rv["median_recovery_ratio"], 6),
            round(rv.get("mean_recovery_ratio_robust", float("nan")), 6),
            round(rv["full_recovery_rate"], 6),
            round(rv.get("full_recovery_rate_big_moves", float("nan")), 6),
            round(rv["mean_recovery_delay"], 4),
            round(rv["median_recovery_delay"], 4),
            round(rv["no_recovery_within_h"] * 100, 4),
            round(r["std"], 9), round(r["std"] * 1e4, 5),
            round(f["ann_vol"] * 100, 4),
            round(r["median"] * 1e4, 5), round(r["q01"] * 1e4, 5),
            round(r["q99"] * 1e4, 5),
            round(r["skew"], 5), round(r["excess_kurtosis"], 4),
            round(r["tail_2s"], 6), round(r["tail_3s"], 6),
            round(r["std"] ** 2 / (mn * var_m1), 5),
            round(raw["var_stability"].get(t, float("nan")), 5),
            round(raw["acf1_dispersion"].get(t, float("nan")), 7),
            round(f["de_tf_h5"], 6), round(f["de_tf_h10"], 6),
            round(f["de_tf_h20"], 6),
            round(f["de_m1_h5"], 6) if f["de_m1_h5"] is not None else "",
            round(f["de_m1_h10"], 6) if f["de_m1_h10"] is not None else "",
            round(f["de_m1_h20"], 6) if f["de_m1_h20"] is not None else "",
            round(de_ratio, 4) if de_ratio != "" else "",
        ])
    write_csv(os.path.join(outdir, "XAUUSD_SIGNAL_NOISE_ANALYSIS.csv"),
              header, rows)


def csv_amplitude_cost(M, outdir):
    tf = M["timeframes"]
    header = ["ROW_TYPE", "TIMEFRAME", "MINUTES", "COST_SCENARIO", "COST_USD",
              "COST_BPS_AT_MEAN_PRICE", "STATISTIC", "VALUE_USD", "VALUE_BPS",
              "RANGE_OVER_COST", "COST_OVER_RANGE", "PCT_OF_RANGE",
              "BARS_WITH_RANGE_ABOVE_COST_PCT"]
    rows = []
    stats = [("MEDIAN_RANGE", "median"), ("P75_RANGE", "p75"),
             ("P90_RANGE", "p90"), ("P95_RANGE", "p95")]
    for t in GRID:
        f = tf[t]["full"]
        am = f["amplitude"]
        mp = f["mean_price"]
        for cname, cost in M["cost_scenarios"]:
            cost_bps = cost / mp * 1e4
            for sname, skey in stats:
                v_usd = am["range_usd"][skey]
                v_bps = am["range_bps"][skey]
                rows.append(["RATIO", t, tf[t]["minutes"], cname, cost,
                             round(cost_bps, 5), sname, round(v_usd, 5),
                             round(v_bps, 4), round(v_usd / cost, 4),
                             round(cost / v_usd, 6), round(cost / v_usd * 100, 4),
                             round(M["_scores"]["raw"]["exceed_cost5"].get(t, 0)
                                   * 100, 4)])
        # cost-dominance thresholds: independent of any scenario
        for pct in (1, 2, 5, 10, 20):
            for sname, skey in stats:
                v_usd = am["range_usd"][skey]
                rows.append([f"MAX_COST_FOR_{pct}PCT", t, tf[t]["minutes"],
                             "N/A", round(v_usd * pct / 100.0, 6),
                             round(am["range_bps"][skey] * pct / 100.0, 5),
                             sname, round(v_usd, 5),
                             round(am["range_bps"][skey], 4), "", "", pct, ""])
    write_csv(os.path.join(outdir, "XAUUSD_AMPLITUDE_COST_ANALYSIS.csv"),
              header, rows)


def csv_scorecard(M, outdir):
    sc = M["_scores"]["components"]
    w = M["_scores"]["weights"]
    groups = {"S": "SIGNAL_NOISE", "A": "AMPLITUDE_COST",
              "C": "STRUCTURAL_PRESERVATION", "D": "TEMPORAL_STABILITY",
              "E": "DATA_CONTINUITY", "F": "INFORMATION_RETENTION"}
    header = ["TIMEFRAME", "MINUTES", "RANK", "GRANULARITY_QUALITY_SCORE"]
    for g, gname in groups.items():
        header.append(f"{gname}_SCORE")
    for g, gname in groups.items():
        for cname in w[g]:
            header.append(cname.upper())
    header.append("COMPOSITE_WEIGHTS")
    rows = []
    for t in GRID:
        row = [t, K[t], sc[t]["rank"], round(sc[t]["GQS"], 5)]
        for g in groups:
            row.append(round(sc[t][g], 5))
        for g in groups:
            for cname in w[g]:
                v = sc[t].get(cname, float("nan"))
                row.append(round(v, 5) if np.isfinite(v) else "")
        row.append(";".join(f"{g}={w['composite'][g]}" for g in groups))
        rows.append(row)
    write_csv(os.path.join(outdir, "XAUUSD_GRANULARITY_SCORECARD.csv"),
              header, rows)


def csv_information_loss(M, outdir):
    tf = M["timeframes"]
    n_m1 = tf["M1"]["full"]["bars"]
    header = ["TIMEFRAME", "MINUTES", "BARS", "OBSERVATIONS_RETAINED_PCT",
              "M1_BARS_PER_BAR", "INTRABAR_REVERSALS_LOST_PER_BAR",
              "INTRABAR_REVERSALS_LOST_TOTAL", "M1_SWINGS_PER_BAR",
              "INTRABAR_PATH_USD", "INTRABAR_NET_USD",
              "PATH_RETENTION_RATIO", "TIMING_RESOLUTION_MIN",
              "TIMING_PRECISION_RELATIVE", "EXTREMES_PRESERVED",
              "ORDER_OF_MOVES", "STRUCTURAL_DISTORTION",
              "BARS_WITH_INTERNAL_DATA_GAP_PCT",
              "BARS_WITH_INTERNAL_MARKET_BREAK_PCT", "CONTIGUITY_IMPACT",
              "INFORMATION_RETAINED", "INFORMATION_LOST"]
    rows = []
    for t in GRID:
        ib = tf[t]["intrabar"]
        f = tf[t]["full"]
        it = f["integrity"]
        k = K[t]
        rev_lost_total = int(round(ib["mean_intrabar_reversals"] * f["bars"]))
        retained = ib["path_retention_ratio"]
        dist = ("none (source resolution)" if t == "M1" else
                "low" if k <= 5 else "moderate" if k <= 20 else
                "high" if k <= 60 else "severe")
        gap_pct = it["bars_with_internal_data_gap"] * 100
        cont = ("none" if gap_pct < 0.5 else "minor" if gap_pct < 3 else
                "notable" if gap_pct < 10 else "major")
        rows.append([
            t, k, f["bars"], round(100.0 * f["bars"] / n_m1, 5),
            round(it["mean_m1_per_bar"], 4),
            round(ib["mean_intrabar_reversals"], 4), rev_lost_total,
            round(ib["m1_pivots_per_bar"], 4),
            round(ib["mean_path_usd"], 5), round(ib["mean_net_usd"], 5),
            round(retained, 5), k, round(1.0 / k, 5),
            "100% (high=max, low=min by construction)",
            "lost" if k > 1 else "preserved", dist,
            round(gap_pct, 5), round(it["bars_with_internal_market_break"] * 100, 5),
            cont,
            "full" if t == "M1" else f"net move only ({retained*100:.1f}% of path)",
            ("nothing" if t == "M1" else
             ("ordering of the 2 component minutes only "
              "(partly recoverable from open/high/low/close); 0 reversals, 0 path"
              if rev_lost_total == 0 else
              f"{rev_lost_total:,} intrabar reversals + intrabar path/timing/ordering")),
        ])
    write_csv(os.path.join(outdir, "XAUUSD_INFORMATION_LOSS.csv"), header, rows)


def csv_yearly_stability(M, outdir):
    tf = M["timeframes"]
    header = ["TIMEFRAME", "MINUTES", "YEAR", "BARS", "ACF_LAG1",
              "SIGN_CHANGE_FREQ", "MEAN_RUN", "RET_STD_BPS",
              "EXCESS_KURTOSIS", "DE_TF_H10", "MEDIAN_RANGE_BPS",
              "P90_RANGE_BPS", "MEDIAN_RANGE_USD",
              "MEDIAN_RANGE_OVER_COST_SCENARIO_3",
              "CONTIGUOUS_STEP_RATE_PCT", "BARS_WITH_INTERNAL_GAP_PCT"]
    rows = []
    for t in GRID:
        for y in sorted(tf[t]["by_year"]):
            d = tf[t]["by_year"][y]
            rows.append([t, K[t], y, d["bars"],
                         round(d["acf"]["lag1"], 6),
                         round(d["sign_change_freq"], 6),
                         round(d["runs"]["mean_run"], 4),
                         round(d["returns"]["std"] * 1e4, 5),
                         round(d["returns"]["excess_kurtosis"], 4),
                         round(d["de_tf_h10"], 6) if d["de_tf_h10"] is not None else "",
                         round(d["amplitude"]["range_bps"]["median"], 4),
                         round(d["amplitude"]["range_bps"]["p90"], 4),
                         round(d["amplitude"]["range_usd"]["median"], 5),
                         round(d["amplitude"]["range_usd"]["median"] / 0.25, 4),
                         round(d["integrity"]["contiguous_step_rate"] * 100, 4),
                         round(d["integrity"]["bars_with_internal_data_gap"] * 100, 4)])
    # stability summary block
    rows.append([])
    rows.append(["--- INTERANNUAL STABILITY 2010-2025 (2026 EXCLUDED) ---"])
    rows.append(["TIMEFRAME", "METRIC", "MEAN", "STD", "CV", "STABILITY_SCORE"])
    for t in GRID:
        for metric, path, key in (("ACF_LAG1", ["acf"], "lag1"),
                                  ("SIGN_CHANGE_FREQ", [], "sign_change_freq"),
                                  ("RET_STD_BPS", ["returns"], "std"),
                                  ("MEDIAN_RANGE_BPS", ["amplitude", "range_bps"],
                                   "median"),
                                  ("DE_TF_H10", [], "de_tf_h10"),
                                  ("EXCESS_KURTOSIS", ["returns"],
                                   "excess_kurtosis")):
            vals = []
            for y in sorted(tf[t]["by_year"]):
                if y == "2026":
                    continue
                v = tf[t]["by_year"][y]
                for p in path:
                    v = v[p]
                v = v[key]
                if v is not None and np.isfinite(v):
                    vals.append(v)
            if len(vals) < 3:
                continue
            c = cv(vals)
            scale = 1e4 if metric == "RET_STD_BPS" else 1.0
            rows.append([t, metric, round(np.mean(vals) * scale, 6),
                         round(np.std(vals, ddof=1) * scale, 6), round(c, 5),
                         round(1.0 / (1.0 + c), 5) if np.isfinite(c) else ""])
    # --- volatility strata: years ranked by M1 realised volatility ----------
    rows.append([])
    rows.append(["--- VOLATILITY STRATA (descriptive, year-level, NOT a regime) ---"])
    rows.append(["STRATUM", "YEARS", "TIMEFRAME", "MEDIAN_RANGE_BPS",
                 "RET_STD_BPS", "ACF_LAG1", "DE_TF_H10"])
    vol = {}
    for y in sorted(tf["M1"]["by_year"]):
        if y == "2026":
            continue
        vol[y] = tf["M1"]["by_year"][y]["returns"]["std"]
    order = sorted(vol, key=lambda y: vol[y])
    n = len(order)
    strata = {"LOW_VOL_YEARS": order[:n // 3],
              "MID_VOL_YEARS": order[n // 3:2 * n // 3],
              "HIGH_VOL_YEARS": order[2 * n // 3:]}
    for sname, ys in strata.items():
        for t in GRID:
            vals = {k: [] for k in ("rng", "std", "acf", "de")}
            for y in ys:
                d = tf[t]["by_year"].get(y)
                if not d:
                    continue
                vals["rng"].append(d["amplitude"]["range_bps"]["median"])
                vals["std"].append(d["returns"]["std"] * 1e4)
                vals["acf"].append(d["acf"]["lag1"])
                if d["de_tf_h10"] is not None:
                    vals["de"].append(d["de_tf_h10"])
            rows.append([sname, ",".join(ys), t,
                         round(np.mean(vals["rng"]), 4),
                         round(np.mean(vals["std"]), 4),
                         round(np.mean(vals["acf"]), 6),
                         round(np.mean(vals["de"]), 5) if vals["de"] else ""])
    write_csv(os.path.join(outdir, "XAUUSD_YEARLY_STABILITY.csv"), header, rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--metrics", default="/tmp/xauusd_audit/metrics_tf.json")
    ap.add_argument("--tfdir", default="/tmp/xauusd_audit/timeframes")
    ap.add_argument("--outdir", default="research/timeframe_audit")
    ap.add_argument("--scores-out", default="/tmp/xauusd_audit/scores.json")
    a = ap.parse_args()
    M = json.load(open(a.metrics))
    M["_tfdir"] = a.tfdir
    man = json.load(open(os.path.join(a.tfdir, "manifest.json")))
    M["_man"] = man
    M["_manifest"] = {g["timeframe"]: g for g in man["grid"]}
    sc = build_scores(M)
    M["_scores"] = sc
    with open(a.scores_out, "w") as fh:
        json.dump(sc, fh, indent=1, default=float)
    os.makedirs(a.outdir, exist_ok=True)
    csv_timeframe_comparison(M, a.outdir)
    csv_signal_noise(M, a.outdir)
    csv_amplitude_cost(M, a.outdir)
    csv_scorecard(M, a.outdir)
    csv_information_loss(M, a.outdir)
    csv_yearly_stability(M, a.outdir)
    print("scores ->", a.scores_out)
    for f in sorted(os.listdir(a.outdir)):
        if f.endswith(".csv"):
            p = os.path.join(a.outdir, f)
            print(f"  {f:44} {os.path.getsize(p):>9,} B  "
                  f"{sum(1 for _ in open(p)):>6} lines")


if __name__ == "__main__":
    main()
