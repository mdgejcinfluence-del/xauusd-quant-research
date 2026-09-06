#!/usr/bin/env python3
"""PHASE 2 renderer: figures + XAUUSD_TIMEFRAME_SELECTION_REPORT.md."""
from __future__ import annotations

import argparse
import json
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

GRID = ["M1", "M2", "M3", "M4", "M5", "M10", "M15", "M20", "M30", "H1", "H2", "H4"]
K = {"M1": 1, "M2": 2, "M3": 3, "M4": 4, "M5": 5, "M10": 10, "M15": 15,
     "M20": 20, "M30": 30, "H1": 60, "H2": 120, "H4": 240}
XS = range(len(GRID))


def f6(x, n=6):
    return "n/a" if x is None or (isinstance(x, float) and not np.isfinite(x)) \
        else f"{x:.{n}f}"


# =========================================================================== #
#  FIGURES
# =========================================================================== #
def make_figures(M, VS, outdir):
    tf = M["timeframes"]
    figdir = os.path.join(outdir, "figures")
    os.makedirs(figdir, exist_ok=True)
    costs = M["cost_scenarios"]
    ks = [K[t] for t in GRID]

    # ---- 1. variance vs sampling frequency -------------------------------- #
    fig, ax = plt.subplots(2, 2, figsize=(13, 9))
    vr = [VS["timeframes"][t]["variance_ratio"] for t in GRID]
    vre = [VS["timeframes"][t]["variance_ratio_excl5s"] for t in GRID]
    av = [tf[t]["full"]["ann_vol"] * 100 for t in GRID]
    sb = [tf[t]["full"]["returns"]["std"] * 1e4 for t in GRID]
    ac = [tf[t]["full"]["acf"]["lag1"] for t in GRID]

    a = ax[0][0]
    a.plot(XS, vr, "o-", color="#1f4e79", label="variance ratio, all bars")
    a.plot(XS, vre, "s--", color="#c55a11", label="variance ratio, |r|>5σ temporarily excluded")
    a.axhline(1.0, color="grey", lw=1, ls=":")
    a.set_xticks(list(XS)); a.set_xticklabels(GRID)
    a.set_ylabel("VR(k) = var(k-min return) / (k x var(1-min return))")
    a.set_title("(a) Variance ratio vs sampling frequency\ncontiguous steps only")
    a.legend(fontsize=8); a.grid(alpha=.3)

    a = ax[0][1]
    a.plot(XS, av, "o-", color="#1f4e79")
    a.set_xticks(list(XS)); a.set_xticklabels(GRID)
    a.set_ylabel("annualised volatility (%)")
    a.set_title("(b) Annualised volatility vs granularity\n(flat = no variance signature)")
    a.grid(alpha=.3)

    a = ax[1][0]
    a.plot(ks, sb, "o-", color="#1f4e79", label="observed std per bar (bps)")
    ref = sb[0] * np.sqrt(np.array(ks, dtype=float))
    a.plot(ks, ref, "k--", lw=1, label=r"$\sqrt{k}$ benchmark (zero autocorrelation)")
    a.set_xscale("log"); a.set_yscale("log")
    a.set_xticks(ks); a.set_xticklabels(GRID, rotation=45)
    a.set_ylabel("std of log return per bar (bps)")
    a.set_title("(c) Return dispersion vs bar length")
    a.legend(fontsize=8); a.grid(alpha=.3, which="both")

    a = ax[1][1]
    a.bar(list(XS), ac, color=["#c00000" if x > 0 else "#1f4e79" for x in ac])
    a.axhline(0, color="k", lw=.8)
    a.set_xticks(list(XS)); a.set_xticklabels(GRID)
    a.set_ylabel("ACF lag 1")
    a.set_title("(d) First-lag autocorrelation vs granularity")
    a.grid(alpha=.3, axis="y")
    fig.suptitle("XAUUSD — variance vs sampling-frequency signature (INFERENCE / PROXY: "
                 "computed from OHLC bars, NOT an order book)", fontsize=11)
    fig.tight_layout(rect=[0, 0, 1, .97])
    fig.savefig(os.path.join(figdir, "variance_vs_sampling_frequency.png"), dpi=140)
    plt.close(fig)

    # ---- 2. signal / noise ------------------------------------------------- #
    fig, ax = plt.subplots(2, 2, figsize=(13, 9))
    sc = M["_scores"]["components"]
    a = ax[0][0]
    a.bar(list(XS), [abs(tf[t]["full"]["acf"]["lag1"]) for t in GRID], color="#1f4e79")
    a.set_xticks(list(XS)); a.set_xticklabels(GRID)
    a.set_ylabel("|ACF lag 1|")
    a.set_title("(a) Linear dependence is negligible at every granularity")
    a.grid(alpha=.3, axis="y")

    a = ax[0][1]
    s = [tf[t]["full"]["sign_change_freq"] for t in GRID]
    a.bar(list(XS), s, color="#1f4e79")
    a.axhline(0.5, color="#c00000", ls="--", lw=1, label="0.50 = independent coin flip")
    a.set_xticks(list(XS)); a.set_xticklabels(GRID)
    a.set_ylim(min(s) - .005, max(s) + .005)
    a.set_ylabel("sign-change frequency")
    a.set_title("(b) Sign alternation vs the random benchmark")
    a.legend(fontsize=8); a.grid(alpha=.3, axis="y")

    a = ax[1][0]
    ek = [tf[t]["full"]["returns"]["excess_kurtosis"] for t in GRID]
    eks = [tf[t]["sensitivity_excl_5sigma"]["returns"]["excess_kurtosis"] for t in GRID]
    a.plot(XS, ek, "o-", color="#c00000", label="excess kurtosis, all bars")
    a.plot(XS, eks, "s-", color="#2e7d32",
           label="after temporarily excluding |r|>5σ (≤0.47% of bars)")
    a.set_yscale("log")
    a.set_xticks(list(XS)); a.set_xticklabels(GRID)
    a.set_ylabel("excess kurtosis")
    a.set_title("(c) Tail heaviness is carried by <0.5% of bars\n"
                "(extremes are NOT deleted: L6)")
    a.legend(fontsize=8); a.grid(alpha=.3, which="both")

    a = ax[1][1]
    for h, mk, col in ((5, "o", "#1f4e79"), (10, "s", "#c55a11"), (20, "^", "#2e7d32")):
        y = [tf[t]["full"][f"de_m1_h{h}"] for t in GRID]
        x = [K[t] * h for t in GRID]
        a.plot(x, y, mk, color=col, ms=4,
               label=f"h = {h} bars ({h} min at M1)")
    a.set_xscale("log")
    a.set_xlabel("horizon in MINUTES (fixed across timeframes)")
    a.set_ylabel("|net displacement| / path length")
    a.set_title("(d) Directional efficiency at a FIXED minute horizon\n"
                "(comparable across granularities)")
    a.legend(fontsize=8); a.grid(alpha=.3, which="both")
    fig.suptitle("XAUUSD — signal / noise diagnostics by timeframe", fontsize=11)
    fig.tight_layout(rect=[0, 0, 1, .97])
    fig.savefig(os.path.join(figdir, "signal_noise_by_timeframe.png"), dpi=140)
    plt.close(fig)

    # ---- 3. amplitude / cost ---------------------------------------------- #
    fig, ax = plt.subplots(2, 2, figsize=(13, 9))
    a = ax[0][0]
    med = [tf[t]["full"]["amplitude"]["range_bps"]["median"] for t in GRID]
    p90 = [tf[t]["full"]["amplitude"]["range_bps"]["p90"] for t in GRID]
    a.plot(XS, med, "o-", color="#1f4e79", label="median bar range (bps)")
    a.plot(XS, p90, "s--", color="#c55a11", label="P90 bar range (bps)")
    a.set_yscale("log")
    a.set_xticks(list(XS)); a.set_xticklabels(GRID)
    a.set_ylabel("bar range (bps of price)")
    a.set_title("(a) Movement amplitude vs granularity")
    a.legend(fontsize=8); a.grid(alpha=.3, which="both")

    a = ax[0][1]
    cols = ["#1f4e79", "#2e75b6", "#c55a11", "#c00000", "#7030a0"]
    for (name, cost), col in zip(costs, cols):
        y = [tf[t]["full"]["amplitude"]["range_usd"]["median"] / cost for t in GRID]
        a.plot(XS, y, "o-", color=col, ms=3, label=f"{name}: {cost:.2f} USD")
    for lvl, ls in ((1, ":"), (10, "-.")):
        a.axhline(lvl, color="grey", lw=1, ls=ls)
        a.text(len(GRID) - .4, lvl * 1.08, f"{lvl}x", fontsize=8, color="grey")
    a.set_yscale("log")
    a.set_xticks(list(XS)); a.set_xticklabels(GRID)
    a.set_ylabel("median bar range / round-trip cost")
    a.set_title("(b) Amplitude-to-cost ratio\n(hypothetical costs, USD of price)")
    a.legend(fontsize=7); a.grid(alpha=.3, which="both")

    a = ax[1][0]
    for (name, cost), col in zip(costs, cols):
        y = [cost / tf[t]["full"]["amplitude"]["range_usd"]["median"] * 100
             for t in GRID]
        a.plot(XS, y, "o-", color=col, ms=3, label=f"{name}: {cost:.2f} USD")
    a.axhline(100, color="grey", lw=1, ls=":")
    a.set_yscale("log")
    a.set_xticks(list(XS)); a.set_xticklabels(GRID)
    a.set_ylabel("cost as % of the median bar range")
    a.set_title("(c) Cost burden: 100% = cost equals the median bar range")
    a.legend(fontsize=7); a.grid(alpha=.3, which="both")

    a = ax[1][1]
    ex = M["_scores"]["raw"]["exceed_cost5"]
    a.plot(XS, [ex[t] * 100 for t in GRID], "o-", color="#1f4e79")
    a.set_xticks(list(XS)); a.set_xticklabels(GRID)
    a.set_ylabel("% of bars whose range exceeds 1.00 USD")
    a.set_title("(d) Share of bars that clear the largest hypothetical cost")
    a.grid(alpha=.3)
    fig.suptitle("XAUUSD — amplitude vs hypothetical transaction cost "
                 "(BROKER_COST_STATUS = EXTERNAL_INPUT_REQUIRED)", fontsize=11)
    fig.tight_layout(rect=[0, 0, 1, .97])
    fig.savefig(os.path.join(figdir, "amplitude_cost_by_timeframe.png"), dpi=140)
    plt.close(fig)
    print("figures written to", figdir)


# =========================================================================== #
#  REPORT
# =========================================================================== #
def md_table(header, rows, align=None):
    out = ["| " + " | ".join(header) + " |"]
    out.append("|" + "|".join(align or ["---"] * len(header)) + "|")
    for r in rows:
        out.append("| " + " | ".join(str(x) for x in r) + " |")
    return "\n".join(out)


def make_report(M, VS, SC, outdir, verdict):
    tf = M["timeframes"]
    man = M["_man"]
    comp = SC["components"]
    W = SC["weights"]
    costs = M["cost_scenarios"]
    L = []
    A = L.append

    # ------------------------------------------------------------------ #
    A("# PHASE 2 — TIMEFRAME / GRANULARITY / SIGNAL-TO-NOISE / AMPLITUDE-TO-COST")
    A("")
    A("**Asset:** XAUUSD (gold spot, USD per troy ounce — nominal unit as delivered)  ")
    A("**Phase:** 2 of the pre-regime, pre-strategy research programme  ")
    A("**Status of Phase 1:** CLOSED (`DATASET_STATUS = PASS_WITH_LIMITATIONS`, commit `82d0823`)  ")
    A(f"**Phase 2 status:** `PHASE_2_STATUS = COMPLETE`  ")
    A(f"**Generated (UTC):** {M['generated_utc']}  ")
    A("**Scope:** determine the temporal granularity that best balances structure preservation, "
      "noise reduction, observable signal persistence, temporal robustness, movement amplitude and "
      "cost relative to movement. **Not** to find a profitable timeframe.")
    A("")
    A("---")
    A("")

    # ---------------- 1 ------------------------------------------------- #
    A("## 1. Executive summary")
    A("")
    A("Twelve granularities (M1, M2, M3, M4, M5, M10, M15, M20, M30, H1, H2, H4) were built "
      "deterministically from the single Phase-1 M1 substrate (5,874,003 bars, 2010-01-01 → "
      "2026-08-30, UTC) and measured on ~90 statistics each.")
    A("")
    A("**The five findings that survive every robustness check applied:**")
    A("")
    A("1. **No granularity converts noise into signal.** Across the whole grid the first-lag "
      "autocorrelation of log returns stays inside ±0.013 on the full sample (inside ±0.020 on "
      "contiguous steps only), the sign-change frequency stays inside "
      "0.5092–0.5207 against a 0.5000 independent benchmark, and the variance ratio stays inside "
      "0.96–1.06. There is no timeframe in the M1→H4 range at which a linear signal emerges. "
      "Timeframe choice on this dataset cannot be justified on 'signal' grounds.")
    A("2. **The tail gradient is an artefact of <0.5% of bars.** Excess kurtosis falls from 88.6 "
      "(M1) to 15.7 (H4) — apparently a huge noise-reduction gain from aggregation. Temporarily "
      "excluding the ≤0.47% of bars whose return exceeds 5σ collapses it to 4.75 (M1) and 4.19 (H4). "
      "The entire 'coarse timeframes are cleaner' gradient is produced by a few hundred extreme "
      "bars, not by the scale of observation. Extremes were **not** deleted (limitation L6).")
    A("3. **One real structural transition exists, around 30–60 minutes.** On contiguous steps "
      "only, the variance ratio declines from 1.000 (M1) to 0.960 (M10) and then **rises back "
      "above 1** at H1–H4 (1.060 at H4). Below roughly half an hour the series is mildly "
      "mean-reverting; above roughly one hour it is mildly trend-persistent. This is the only "
      "scale-dependent change of character found anywhere in the grid.")
    A("4. **Continuity collapses above H1.** The share of bars that silently contain a missing-data "
      "gap goes 0.00% (M1–M2) → 0.11% (M3) → 3.16% (H1) → **16.46% (H4)**, and 10.23% of H4 bars "
      "contain an internal market break (weekend / overnight). An H4 'bar' is frequently not a "
      "homogeneous observation and is rejected on that basis.")
    o = sorted(GRID, key=lambda t: -comp[t]["GQS"])
    A(f"5. **The composite score has a plateau, not a peak.** The `GRANULARITY_QUALITY_SCORE` "
      f"returns " + ", ".join(f"{t} = {comp[t]['GQS']:.4f}" for t in o[:4]) +
      f" — a {comp[o[0]]['GQS']-comp[o[2]]['GQS']:.4f} spread across the top three against a "
      f"{comp[o[0]]['GQS']-comp[o[-1]]['GQS']:.4f} total range. All eleven robustness variants "
      f"put the winner inside {{M1, M2, M3, M5}}; the ordering *inside* that set flips depending "
      f"on whether three noise-dominated sub-components are included.")
    A("")
    A("**Decision (full justification in §18):** `PRIMARY_TIMEFRAME = M3`, "
      "`SECONDARY_TIMEFRAME = M1`, `CONTEXT_TIMEFRAME = H1`. H4 is rejected. Confidence is HIGH "
      "on the M1–M5 zone, MODERATE on M3 specifically, LOW on any finer distinction.")
    A("")
    A("---")
    A("")

    # ---------------- 2 ------------------------------------------------- #
    A("## 2. Dataset used")
    A("")
    A("| item | value |")
    A("|---|---|")
    A("| Instrument | XAUUSD (gold spot) |")
    A("| Source files | `XAUUSD_part_01..07.parquet.part` (7 fragments, unmodified) |")
    A("| Reconstruction | the 7 fragments are concatenated in their physical parquet row-group/page "
    "order (Phase 1 section 3); no row is dropped, reordered, de-duplicated or modified |")
    A("| Verification | master SHA-256 re-checked at the start of Phase 2 and byte-identical to Phase 1 |")
    A(f"| M1 master | `{man['master']}` |")
    A(f"| M1 master SHA-256 | `{man['master_sha256']}` |")
    A(f"| M1 bars | {man['m1_bars']:,} |")
    A(f"| Span (UTC) | {man['first_ts']} → {man['last_ts']} |")
    A(f"| Years covered | {M['span_years']:.3f} (2010-01-01 → 2026-08-30) |")
    A("| Timezone | UTC throughout; no local-time conversion applied |")
    A("| Volume column | **never loaded** (Phase 1 limitation L1: unit unknown) |")
    A("")
    A("The Phase-1 master SHA-256 above is byte-identical to the file that produced the Phase-1 "
      "report. No source fragment was read for anything other than reading.")
    A("")
    A("---")
    A("")

    # ---------------- 3 ------------------------------------------------- #
    A("## 3. Limitations inherited from Phase 1 (binding in Phase 2)")
    A("")
    A("| id | limitation | consequence in Phase 2 |")
    A("|---|---|---|")
    A("| L1 | Volume unit is unknown | the volume column is never loaded, used or derived; no "
      "volume-weighted statistic exists anywhere in this phase |")
    A("| L2 | No gap filling | aggregation never pads a window; a bar with 1 of 3 M1 minutes "
      "present is a 1-minute bar and is flagged as such |")
    A("| L3 | No price-decimal homogenisation | all amplitude figures are computed on the prices "
      "as delivered, in USD and in basis points of the contemporaneous price |")
    A("| L4 | Session-convention break around 2013 | treated explicitly in §13 as a structural "
      "split, not smoothed away |")
    A("| L5 | 2026 is a partial year (Jan–Aug) | reported as `2026_SANITY_CHECK` only; it never "
      "enters any score, ranking or selection |")
    A("| L6 | Extremes stay in the data | no winsorisation, no trimming; the 5σ exercise in §6 is "
      "a *sensitivity exclusion*, reported side by side and never substituted for the main result |")
    A("| L7 | Sources are never modified | all seven fragments verified unmodified after this phase |")
    A("")
    A("Two Phase-2-specific additions:")
    A("")
    A("* **L8 — no order book.** Everything below is computed from OHLC bars. Any statement about "
      "microstructure is labelled `INFERENCE / PROXY`. No bid, no ask, no tick, no depth was observed.")
    A("* **L9 — no broker cost exists in the repo.** All costs used here are hypothetical scenario "
      "values. `BROKER_COST_STATUS = EXTERNAL_INPUT_REQUIRED`.")
    A("")
    A("---")
    A("")

    # ---------------- 4 ------------------------------------------------- #
    A("## 4. Aggregation method")
    A("")
    A("| parameter | value |")
    A("|---|---|")
    A(f"| Origin | {man['origin']} |")
    A(f"| Alignment | {man['alignment']} |")
    A(f"| Timezone | {man['timezone']} |")
    A(f"| Aggregation | {man['aggregation']} |")
    A(f"| Gap policy | {man['gap_policy']} |")
    A(f"| Volume | {man['volume']} |")
    A(f"| Market-break threshold | {man['market_break_threshold_minutes']} minutes of missing M1 "
      "data inside a bar counts as an internal market break |")
    A("")
    A("Rules, all deterministic and reproducible:")
    A("")
    A("1. Every M1 bar is assigned `bar_id = floor(epoch_minutes_utc / k)`; the origin is the UNIX "
      "epoch, **not** the first bar of the dataset, so the grid is identical for anyone re-running "
      "the script and is independent of where the data happens to start.")
    A("2. `Open = first`, `High = max`, `Low = min`, `Close = last` of the M1 bars in the window, "
      "in timestamp order.")
    A("3. **No gap is filled and no M1 bar is invented.** A window with zero M1 bars does not "
      "exist in the output. A window with 2 of 5 M1 bars produces a bar whose High/Low span only "
      "those 2 minutes.")
    A("4. Volume is dropped at construction time, not later.")
    A("5. Each output bar carries `n_m1`, `internal_missing` (missing M1 minutes strictly inside "
      "the window), `internal_breaks` (market breaks inside) and `contig_next` (is the next "
      "calendar bar present?). These counters are what make §11–§12 auditable.")
    A("")
    A("Everything downstream reads only these files; the M1 master is never re-aggregated ad hoc.")
    A("")
    A("---")
    A("")

    # ---------------- 5 ------------------------------------------------- #
    A("## 5. Granularity grid")
    A("")
    rows = []
    for t in GRID:
        g = [x for x in man["grid"] if x["timeframe"] == t][0]
        f = tf[t]["full"]
        rows.append([t, K[t], f"{f['bars']:,}", f"{100*f['bars']/tf['M1']['full']['bars']:.4f}%",
                     f"{f['integrity']['mean_m1_per_bar']:.3f}",
                     f"{f['integrity']['contiguous_step_rate']*100:.3f}%",
                     g["first_ts"][:19], g["last_ts"][:19]])
    A(md_table(["TF", "min", "bars", "% of M1 bars", "mean M1/bar", "contiguous steps",
                "first (UTC)", "last (UTC)"], rows))
    A("")
    A("**Exclusions.** All twelve granularities are technically sound and all twelve are reported. "
      "No granularity was dropped from the grid. H4 is *rejected as a candidate* in §18 on "
      "continuity grounds, but its measurements are retained everywhere — rejection is a conclusion, "
      "not a deletion.")
    A("")
    A("---")
    A("")

    # ---------------- 6 ------------------------------------------------- #
    A("## 6. Noise diagnostic")
    A("")
    A("### 6.1 Autocorrelation")
    A("")
    rows = []
    for t in GRID:
        a = tf[t]["full"]["acf"]
        rows.append([t] + [f"{a[f'lag{l}']:+.5f}" for l in (1, 2, 3, 4, 8)])
    A(md_table(["TF", "ACF lag1", "lag2", "lag3", "lag4", "lag8"], rows))
    A("")
    A("Every value sits inside ±0.019. Sampling error at the coarsest granularity "
      "(1/√26,452 ≈ 0.0061) is of the same order as the largest value measured, so the *pattern* "
      "across lags carries no information; only the *absence of any material autocorrelation* is a "
      "finding.")
    A("")
    A("### 6.2 Sign alternation and run lengths")
    A("")
    rows = []
    for t in GRID:
        f = tf[t]["full"]
        rows.append([t, f"{f['sign_change_freq']:.5f}", f"{f['runs']['mean_run']:.4f}",
                     f"{f['runs']['median_run']:.1f}", f"{f['runs']['p90_run']:.0f}",
                     f"{f['runs']['max_run']:,}",
                     f"{f['runs']['mean_run']*K[t]:.2f}"])
    A(md_table(["TF", "sign-change freq", "mean run", "median run", "P90 run", "max run",
                "mean run (minutes)"], rows))
    A("")
    A("A sequence of independent up/down signs has sign-change frequency 0.5000 and mean run 2.0. "
      "The whole grid sits at 0.5092–0.5207 and 1.808–1.922 — i.e. uniformly *slightly more "
      "alternating than a coin flip*, which is the same weak negative dependence the ACF shows. "
      "The mean run expressed in **minutes** is the informative column: the average directional "
      "run lasts 1.91 minutes at M1 and 452 minutes at H4 — close to 1.9 x k at every granularity, "
      "i.e. the run length in minutes is just the bar length rescaled. There is no granularity at which directional runs become systematically "
      "longer *in minutes* than the bar that measures them.")
    A("")
    A("### 6.3 Ultra-short reversals")
    A("")
    rows = []
    for t in GRID:
        v = tf[t]["full"]["reversal"]
        rows.append([t, f"{v['reversal_freq']:.5f}", f"{v['median_recovery_ratio']:.4f}",
                     f"{v['full_recovery_rate']:.4f}",
                     f"{v['full_recovery_rate_big_moves']:.4f}",
                     f"{v['mean_recovery_delay']:.3f}", f"{v['median_recovery_delay']:.0f}",
                     f"{v['no_recovery_within_h']*100:.2f}%"])
    A(md_table(["TF", "reversal freq", "median recovery ratio", "full recovery rate",
                "full recovery (big moves)", "mean delay (bars)", "median delay (bars)",
                "no recovery within 20 bars"], rows))
    A("")
    A("Reversal frequency is 0.509–0.521 everywhere: after a down bar, an up bar follows about as "
      "often as a coin decides. The recovery ratio (how far the reversal retraces the triggering "
      "move) falls from 1.000 at M1 to 0.889 at H2 (0.922 at H4), and the mean recovery delay is "
      "**4.4–4.5 bars "
      "at every single granularity** — from 1-minute bars to 4-hour bars. That invariance is the "
      "clearest statement available: the number of observations needed to undo a move is a constant "
      "in *bar count*, not in time, so coarser bars do not make reversals rarer, they only make "
      "them slower in wall-clock terms.")
    A("")
    A("### 6.4 Distribution, moments and tails")
    A("")
    rows = []
    for t in GRID:
        r = tf[t]["full"]["returns"]
        s = tf[t]["sensitivity_excl_5sigma"]["returns"]
        rows.append([t, f"{r['std']*1e4:.4f}", f"{tf[t]['full']['ann_vol']*100:.3f}",
                     f"{r['skew']:+.4f}", f"{r['excess_kurtosis']:.2f}",
                     f"{s['excess_kurtosis']:.2f}",
                     f"{100*(1-s.get('n', tf[t]['sensitivity_excl_5sigma']['bars'])/tf[t]['full']['bars']):.3f}%",
                     f"{r['tail_2s']*100:.3f}%", f"{r['tail_3s']*100:.3f}%"])
    A(md_table(["TF", "std (bps)", "annualised vol %", "skew", "excess kurtosis",
                "excess kurtosis (5σ excl.)", "bars excluded", "|r|>2σ", "|r|>3σ"], rows))
    A("")
    A("**This is the most important table in the phase.** Read the kurtosis columns together. The "
      "apparent gradient 88.6 → 15.7 says 'aggregation removes noise'. The right-hand column says "
      "otherwise: removing between 0.40% and 0.47% of bars takes excess kurtosis to 4.19–4.75 at "
      "*every* granularity — nearly flat, and modest. The heavy tail is not a property of the "
      "sampling frequency; it is a property of a few hundred specific minutes (news, fix-related "
      "spikes, thin-liquidity prints) whose effect aggregation merely smears across a wider window. "
      "Aggregation does not remove those events from the sample, it dilutes their per-bar impact.")
    A("")
    A("Annualised volatility is flat at 16.2–16.6% across a 240× frequency range, which is the same "
      "fact seen from the other side: there is no frequency at which XAUUSD variance behaves "
      "differently in aggregate.")
    A("")
    A("### 6.5 Variance-vs-sampling-frequency signature (INFERENCE / PROXY)")
    A("")
    A("Computed on **contiguous steps only** — a consecutive pair of rows whose `bar_id` differ by "
      "exactly 1 and whose bars contain no missing M1 minute. This matters: a gap-spanning return "
      "carries minutes of movement that belong to no bar, and gaps are 0.27% of M1 steps but affect "
      "16% of H4 bars, so an unfiltered variance ratio is biased against the coarse end.")
    A("")
    rows = []
    for t in GRID:
        v = VS["timeframes"][t]
        rows.append([t, f"{v['n']:,}", f"{v['std_bps']:.4f}", f"{v['std_bps_excl5s']:.4f}",
                     f"{v['variance_ratio']:.4f}", f"{v['variance_ratio_excl5s']:.4f}",
                     f"{v['acf1_contiguous']:+.5f}", f"{v['vr_implied_by_acf1']:.4f}"])
    A(md_table(["TF", "contiguous steps", "std (bps)", "std excl. 5σ (bps)",
                "VR(k)", "VR(k) excl. 5σ", "ACF lag 1 (contiguous)",
                "VR implied by ACF1 alone"], rows))
    A("")
    A("`VR(k) = var(k-minute return) / (k × var(1-minute return))`. VR = 1 is a pure random walk; "
      "VR < 1 indicates mean reversion (or, indistinguishably from OHLC data, a bid/ask-type "
      "bounce); VR > 1 indicates persistence/trending.")
    A("")
    A("* M1 → M10: VR falls 1.000 → 0.960. The fine end is mildly mean-reverting.")
    A("* M10 → M30: VR is flat at 0.96.")
    A("* H1 → H4: VR **rises back through 1.0** (0.978 → 1.060; 1.048 → 1.234 once 5σ bars are "
      "temporarily excluded). The coarse end is mildly trend-persistent.")
    A("")
    A("The crossing sits between M30 and H1, i.e. **between roughly 30 and 60 minutes**. This is "
      "the only scale-dependent change of character anywhere in the grid and it is labelled "
      "`INFERENCE / PROXY`: it is a statement about the second-moment structure of OHLC bar "
      "returns, not an order-book observation (L8).")
    A("")
    A("![variance vs sampling frequency](figures/variance_vs_sampling_frequency.png)")
    A("")
    A("---")
    A("")

    # ---------------- 7 ------------------------------------------------- #
    A("## 7. Observable signal and structure")
    A("")
    A("### 7.1 Directional efficiency — and why the naive comparison is invalid")
    A("")
    A("Directional efficiency is `|close(t+h) − close(t)| / Σ|Δclose|` over h bars.")
    A("")
    rows = []
    for t in GRID:
        f = tf[t]["full"]
        rows.append([t, f"{f['de_tf_h5']:.4f}", f"{f['de_tf_h10']:.4f}",
                     f"{f['de_tf_h20']:.4f}",
                     f6(f["de_m1_h5"], 4), f6(f["de_m1_h10"], 4), f6(f["de_m1_h20"], 4)])
    A(md_table(["TF", "DE h=5 (tf bars)", "DE h=10", "DE h=20", "DE h=5 (M1 resolution)",
                "DE h=10 (M1 res.)", "DE h=20 (M1 res.)"], rows))
    A("")
    A("Read the `DE h=10 (tf bars)` column naively and it says efficiency *improves* with "
      "granularity (0.3151 at M1 → 0.3521 at H4). That comparison is invalid and must not be used:")
    A("")
    A("* the horizon in **minutes** is different in every row (10 minutes for M1, 2,400 minutes "
      "for H4); and")
    A("* the path in the denominator is sampled at the bar frequency, so a coarse bar "
      "systematically *under-counts* the path and mechanically inflates the ratio.")
    A("")
    A("The `M1 resolution` columns fix both problems: they measure the same window at M1 "
      "resolution, so the horizon in minutes is `h × k` and the path is complete. On that "
      "comparable basis directional efficiency **falls** as the horizon grows — 0.315 over 10 "
      "minutes, 0.044 over 600 minutes (H1, h=10), 0.033 over 1,200 minutes (H2, h=10). At a fixed "
      "600-minute window the H1-resolution figure is 0.3357 against 0.0440 measured at M1 "
      "resolution: **the apparent efficiency of hourly bars is 7.6× inflated by path coarsening.** "
      "Any claim that coarse bars are 'more directional' rests on this artefact.")
    A("")
    A("### 7.2 Structure persistence")
    A("")
    rows = []
    for t in GRID:
        f = tf[t]["full"]
        s = f["structure"]
        rows.append([t, f"{s['new_extreme_rate']:.4f}", f"{s['breakout_rate']:.4f}",
                     f"{s['breakout_persistence']:.4f}", f"{s['reintegration_rate_within_5']:.4f}",
                     f"{s['range_expansion_std_log']:.4f}", f"{s['mean_body_over_range']:.4f}"])
    A(md_table(["TF", "new 20-bar extreme rate", "breakout rate (20)",
                "breakout persistence", "reintegration within 5 bars",
                "std of log range ratio", "mean body / range"], rows))
    A("")
    A("* **Breakout persistence** (a bar that closes outside the previous 20-bar range and is still "
      "outside 5 bars later) rises monotonically 0.4118 (M1) → 0.4986 (H4); reintegration falls "
      "0.5882 → 0.5014. Coarse bars do hold breakouts better — but the effect is small and, at "
      "H4, 50.1% of breakouts still fail, i.e. barely better than a coin.")
    A("* **Range expansion/contraction** (std of the log range ratio) is U-shaped with a minimum at "
      "M20 (0.5484): volatility-of-volatility is *lowest* around 20-minute bars and rises again "
      "towards H4 (0.7201).")
    A("* **Body/range** falls monotonically 0.5215 → 0.4350: the finer the bar, the more of it is "
      "directional body rather than wick. Coarse bars are progressively more 'noise' in their own "
      "terms.")
    A("")
    A("![signal/noise by timeframe](figures/signal_noise_by_timeframe.png)")
    A("")
    A("---")
    A("")

    # ---------------- 8 ------------------------------------------------- #
    A("## 8. Movement amplitude")
    A("")
    A("All figures in USD of price as delivered (limitation L3) and in basis points of the "
      "contemporaneous price. The bar range is `High − Low`.")
    A("")
    rows = []
    for t in GRID:
        a = tf[t]["full"]["amplitude"]["range_usd"]
        rows.append([t] + [f"{a[x]:.4f}" for x in ("p25", "median", "mean", "p75", "p90", "p95", "p99")])
    A("**Absolute (USD):**")
    A("")
    A(md_table(["TF", "P25", "median", "mean", "P75", "P90", "P95", "P99"], rows))
    A("")
    rows = []
    for t in GRID:
        a = tf[t]["full"]["amplitude"]["range_bps"]
        b = tf[t]["full"]["amplitude"]["body_bps"]
        rows.append([t] + [f"{a[x]:.3f}" for x in ("median", "p75", "p90", "p95", "p99")] +
                    [f"{b['median']:.3f}", f"{b['p90']:.3f}"])
    A("**Relative (bps of price):**")
    A("")
    A(md_table(["TF", "median range", "P75", "P90", "P95", "P99", "median body", "P90 body"],
               rows))
    A("")
    A("Amplitude scales close to √k: median range 0.355 USD at M1 → 6.523 USD at H4 (×18.4 for a "
      "×240 increase in bar length). Expressed in bps the same numbers are 2.26 → 41.27.")
    A("")
    A("**Normal vs high-volatility periods** are compared at year level in §12 "
      "(`XAUUSD_YEARLY_STABILITY.csv`, volatility strata): year-level median range at M1 varies "
      "from 1.59 bps (2019) to 3.09 bps (2025) across the sixteen full years — a factor of 1.94, "
      "comparable to the amplitude difference between M1 and M5. The excluded partial year 2026 "
      "reaches 4.62 bps. Granularity is not the dominant driver of amplitude; the year is.")
    A("")
    A("---")
    A("")

    # ---------------- 9 ------------------------------------------------- #
    A("## 9. Transaction cost")
    A("")
    A("`BROKER_COST_STATUS = EXTERNAL_INPUT_REQUIRED`. No broker specification, spread table, "
      "commission schedule or slippage model exists anywhere in this repository, and none was "
      "invented. Every cost used below is a **hypothetical scenario**, expressed as an all-in "
      "round-trip cost in **USD of gold price**, held constant across the whole sample and across "
      "all granularities so that the comparison isolates the granularity effect.")
    A("")
    rows = [[n, f"{c:.2f} USD",
             ", ".join(f"{t}:{c/tf[t]['full']['mean_price']*1e4:.3f}" for t in ("M1", "M30", "H4"))]
            for n, c in costs]
    A(md_table(["scenario", "round-trip cost", "equivalent in bps (M1 / M30 / H4 mean price)"],
               rows))
    A("")
    A("What is required to replace these with broker-specific figures: (i) the instrument's typical "
      "spread by session, (ii) commission per lot with the lot size and contract specification, "
      "(iii) an execution/slippage assumption. Until those are supplied, §10 is a **sensitivity "
      "grid**, not a cost measurement.")
    A("")
    A("---")
    A("")

    # ---------------- 10 ------------------------------------------------ #
    A("## 10. Amplitude-to-cost")
    A("")
    A("### 10.1 Median bar range divided by cost")
    A("")
    heads = ["TF"] + [f"{n.split('_')[-1]} ({c:.2f})" for n, c in costs]
    rows = []
    for t in GRID:
        v = tf[t]["full"]["amplitude"]["range_usd"]["median"]
        rows.append([t] + [f"{v/c:.3f}" for _, c in costs])
    A(md_table(heads, rows))
    A("")
    A("### 10.2 Cost as a percentage of the median bar range")
    A("")
    rows = []
    for t in GRID:
        v = tf[t]["full"]["amplitude"]["range_usd"]["median"]
        rows.append([t] + [f"{c/v*100:.1f}%" for _, c in costs])
    A(md_table(heads, rows))
    A("")
    A("At the mid scenario (0.25 USD) the cost equals **70.4%** of the median M1 bar range, 37.3% "
      "at M3, 15.7% at M15 and 7.6% at H1. This is the single strongest coarse-favouring gradient "
      "in the phase and, unlike the tail gradient of §6.4, it survives every sensitivity check — "
      "it is arithmetically just the amplitude gradient of §8 divided by a constant.")
    A("")
    A("### 10.3 Maximum cost tolerated at 1 / 2 / 5 / 10 / 20% of the range distribution")
    A("")
    rows = []
    for t in GRID:
        a = tf[t]["full"]["amplitude"]["range_usd"]
        row = [t]
        for p in (1, 2, 5, 10, 20):
            row.append(", ".join(f"{a[k]*p/100:.3f}" for k in ("median", "p90")))
        rows.append(row)
    A(md_table(["TF", "1% (median, P90)", "2% (median, P90)", "5% (median, P90)",
                "10% (median, P90)", "20% (median, P90)"], rows))
    A("")
    A("Reading: for cost to represent at most 5% of the *median* M1 bar range, an all-in "
      "round-trip cost of 0.018 USD is required. At H1 the same 5% budget allows 0.165 USD. Full "
      "per-statistic detail (median / P75 / P90 / P95) is in "
      "`XAUUSD_AMPLITUDE_COST_ANALYSIS.csv` (`ROW_TYPE = MAX_COST_FOR_*`).")
    A("")
    A("### 10.4 Share of bars that clear the largest hypothetical cost (1.00 USD)")
    A("")
    rows = [[t, f"{SC['raw']['exceed_cost5'][t]*100:.2f}%"] for t in GRID]
    A(md_table(["TF", "% of bars with range > 1.00 USD"], rows))
    A("")
    A("![amplitude vs cost](figures/amplitude_cost_by_timeframe.png)")
    A("")
    A("---")
    A("")

    # ---------------- 11 ------------------------------------------------ #
    A("## 11. Information lost by aggregation")
    A("")
    n_m1 = tf["M1"]["full"]["bars"]
    rows = []
    for t in GRID:
        ib = tf[t]["intrabar"]
        f = tf[t]["full"]
        it = f["integrity"]
        k = K[t]
        dist = ("none (source resolution)" if t == "M1" else
                "low" if k <= 5 else "moderate" if k <= 20 else "high" if k <= 60 else "severe")
        gap = it["bars_with_internal_data_gap"] * 100
        cont = ("none" if gap < .5 else "minor" if gap < 3 else "notable" if gap < 10 else "major")
        rows.append([t, f"{100*f['bars']/n_m1:.4f}%", f"{it['mean_m1_per_bar']:.3f}",
                     f"{ib['mean_intrabar_reversals']:.3f}",
                     f"{int(round(ib['mean_intrabar_reversals']*f['bars'])):,}",
                     f"{ib['m1_pivots_per_bar']:.3f}",
                     f"{ib['path_retention_ratio']:.4f}", f"{1/k:.4f}",
                     "preserved" if k == 1 else "lost", dist, cont,
                     f"{it['contiguous_step_rate']*100:.3f}%"])
    A(md_table(["TF", "retained observations", "M1 bars per bar",
                "intrabar reversals lost per bar", "lost in total", "M1 swings per bar",
                "path retention", "timing precision", "order of moves", "distortion",
                "continuity impact", "contiguous steps"], rows))
    A("")
    A("Definitions.")
    A("")
    A("* **Path retention** = mean |net displacement of the bar| ÷ mean Σ|M1 log steps| inside the "
      "bar. It is 1.0000 at M1 by definition (a single M1 bar has no interior) and 0.0681 at H4: "
      "an H4 bar keeps 6.8% of the movement that actually happened and discards 93.2% as wiggle.")
    A("* **Intrabar reversals lost** = M1-level sign changes strictly inside the bar, i.e. "
      "direction changes that exist at M1 and are invisible at the bar level. 0.000 per bar at M1, "
      "13.57 at M30, 107.30 at H4 — about 2.84 million direction changes that exist at M1 and are "
      "invisible at H4.")
    A("* **Order of moves** is preserved only at M1. From M2 upwards only the open, high, low and "
      "close are known; whether the high preceded the low is unknowable from the bar.")
    A("* **Continuity impact**: the share of bars that *silently* contain a missing-data gap. At "
      "M1 a gap is visible as an absent bar; from M3 upwards a gap hides inside a bar that looks "
      "perfectly normal.")
    A("")
    A("The trade-off is stark and monotone:")
    A("")
    A("| TF | observations kept | intrabar path kept | reversals lost per bar | bars hiding a data gap |")
    A("|---|---|---|---|---|")
    for t in ("M1", "M3", "M5", "M15", "M30", "H1", "H4"):
        ib = tf[t]["intrabar"]
        it = tf[t]["full"]["integrity"]
        A(f"| {t} | {100*tf[t]['full']['bars']/n_m1:.2f}% | "
          f"{ib['path_retention_ratio']*100:.1f}% | {ib['mean_intrabar_reversals']:.2f} | "
          f"{it['bars_with_internal_data_gap']*100:.2f}% |")
    A("")
    A("Two entries are structural rather than empirical and are flagged as such: at M1 there is no "
      "bar interior, so nothing can be lost; at M2 a bar contains a single internal M1 step, so "
      "path and net coincide and no reversal can occur inside it. M2 therefore loses only the "
      "*ordering* of its two minutes — and even that is largely recoverable from the bar's open, "
      "high, low and close — which is why it scores almost level with M1 on this table.")
    A("")
    A("---")
    A("")

    # ---------------- 12 ------------------------------------------------ #
    A("## 12. Interannual stability (2010–2025)")
    A("")
    A("2026 is excluded here by construction (L5). Per-year values for every granularity are in "
      "`XAUUSD_YEARLY_STABILITY.csv`.")
    A("")
    A("### 12.1 Dispersion of the key metrics across the 16 full years")
    A("")
    rows = []
    for t in GRID:
        y = tf[t]["by_year"]
        def vals(path, key, scale=1.0):
            v = []
            for yr in y:
                if yr == "2026":
                    continue
                d = y[yr]
                for p in path:
                    d = d[p]
                x = d[key]
                if x is not None and np.isfinite(x):
                    v.append(x * scale)
            return v
        out = [t]
        for path, key, scale in ((["acf"], "lag1", 1), ([], "sign_change_freq", 1),
                                 (["returns"], "std", 1e4),
                                 (["amplitude", "range_bps"], "median", 1),
                                 ([], "de_tf_h10", 1)):
            v = vals(path, key, scale)
            m = float(np.mean(v)); s = float(np.std(v, ddof=1))
            out.append(f"{m:.4f} ± {s:.4f}")
        rows.append(out)
    A(md_table(["TF", "ACF lag1 (mean±sd)", "sign-change freq", "std (bps)",
                "median range (bps)", "DE h=10"], rows))
    A("")
    A("### 12.2 Old vs recent, calm vs volatile")
    A("")
    vol = {y: tf["M1"]["by_year"][y]["returns"]["std"] for y in tf["M1"]["by_year"] if y != "2026"}
    order = sorted(vol, key=lambda y: vol[y])
    n = len(order)
    strata = {"LOW_VOL_YEARS": order[:n // 3], "MID_VOL_YEARS": order[n // 3:2 * n // 3],
              "HIGH_VOL_YEARS": order[2 * n // 3:]}
    A("Years ranked by M1 realised volatility and split into terciles "
      "(**descriptive volatility strata, not regimes**):")
    A("")
    for s, ys in strata.items():
        A(f"* `{s}` = {', '.join(ys)}")
    A("")
    rows = []
    for s, ys in strata.items():
        for t in ("M1", "M3", "M15", "H1"):
            v = {k: [] for k in ("rng", "std", "acf", "de")}
            for y in ys:
                d = tf[t]["by_year"].get(y)
                if not d:
                    continue
                v["rng"].append(d["amplitude"]["range_bps"]["median"])
                v["std"].append(d["returns"]["std"] * 1e4)
                v["acf"].append(d["acf"]["lag1"])
                if d["de_tf_h10"] is not None:
                    v["de"].append(d["de_tf_h10"])
            rows.append([s, t, f"{np.mean(v['rng']):.3f}", f"{np.mean(v['std']):.4f}",
                         f"{np.mean(v['acf']):+.5f}",
                         f"{np.mean(v['de']):.4f}" if v["de"] else "n/a"])
    A(md_table(["stratum", "TF", "median range (bps)", "std (bps)", "ACF lag1", "DE h=10"], rows))
    A("")
    A("The ranking of granularities is unchanged between calm and volatile years: amplitude scales "
      "up in volatile years at every granularity by a similar factor, and the noise diagnostics "
      "(ACF, alternation) stay indistinguishable from zero in all three strata. **The granularity "
      "conclusions are not an artefact of the volatility level of the sample.**")
    A("")
    A("**Old vs recent** (mean of the yearly values, 2010–2017 vs 2018–2025):")
    A("")
    A("| TF | median range old (bps) | median range recent (bps) | ACF1 old | ACF1 recent | "
      "DE h=10 old | DE h=10 recent |")
    A("|---|---|---|---|---|---|---|")
    for t in ("M1", "M3", "M15", "H1", "H4"):
        g = {"old": [], "new": []}
        for y in sorted(tf[t]["by_year"]):
            if y == "2026":
                continue
            d = tf[t]["by_year"][y]
            g["old" if int(y) <= 2017 else "new"].append(d)

        def mn(rows_, path, key):
            v = []
            for d in rows_:
                for pp in path:
                    d = d[pp]
                v.append(d[key])
            return np.mean(v)
        A(f"| {t} | {mn(g['old'], ['amplitude','range_bps'], 'median'):.3f} | "
          f"{mn(g['new'], ['amplitude','range_bps'], 'median'):.3f} | "
          f"{mn(g['old'], ['acf'], 'lag1'):+.5f} | {mn(g['new'], ['acf'], 'lag1'):+.5f} | "
          f"{mn(g['old'], [], 'de_tf_h10'):.4f} | {mn(g['new'], [], 'de_tf_h10'):.4f} |")
    A("")
    A("Median amplitude differs by at most 4% between the two halves at every granularity and "
      "directional efficiency by at most 0.015 in absolute terms, so the ordering of the "
      "granularities does not depend on which half of the sample is used. (The ACF column moves "
      "more — see section 13, which splits at 2013 rather than 2017 and finds the same effect.)")
    A("")
    A("### 12.3 Median vs mean")
    A("")
    rows = []
    for t in ("M1", "M3", "M15", "H1", "H4"):
        a = tf[t]["full"]["amplitude"]["range_usd"]
        rows.append([t, f"{a['median']:.4f}", f"{a['mean']:.4f}", f"{a['mean']/a['median']:.3f}"])
    A(md_table(["TF", "median range USD", "mean range USD", "mean / median"], rows))
    A("")
    A("The mean/median ratio is 1.58–1.67 at every granularity: the range distribution is "
      "right-skewed to the same degree at every scale, so switching between median and mean does "
      "not change any ordering. All scores use medians or explicitly labelled means.")
    A("")
    A("---")
    A("")

    # ---------------- 13 ------------------------------------------------ #
    A("## 13. The 2013 structural / session break")
    A("")
    A("Phase 1 documented a change of session convention around 2013 (limitation L4). The pre/post "
      "split is treated here as two separate samples, never smoothed.")
    A("")
    rows = []
    for t in GRID:
        p = tf[t]["pre2013"]["full"] if "full" in tf[t]["pre2013"] else tf[t]["pre2013"]
        q = tf[t]["post2013"]["full"] if "full" in tf[t]["post2013"] else tf[t]["post2013"]
        flip = "**SIGN FLIP**" if np.sign(p["acf"]["lag1"]) != np.sign(q["acf"]["lag1"]) else "no flip"
        rows.append([t, f"{p['bars']:,}", f"{p['acf']['lag1']:+.5f}",
                     f"{q['acf']['lag1']:+.5f}", flip,
                     f"{p['amplitude']['range_bps']['median']:.3f}",
                     f"{q['amplitude']['range_bps']['median']:.3f}",
                     f"{p['returns']['excess_kurtosis']:.2f}",
                     f"{q['returns']['excess_kurtosis']:.2f}",
                     f"{p['integrity']['contiguous_step_rate']*100:.2f}%",
                     f"{q['integrity']['contiguous_step_rate']*100:.2f}%"])
    A(md_table(["TF", "pre-2013 bars", "ACF lag1 pre", "ACF lag1 post", "sign",
                "median range pre (bps)", "median range post (bps)",
                "excess kurtosis pre", "excess kurtosis post",
                "contiguous pre", "contiguous post"], rows))
    A("")
    flip = [t for t in GRID
            if np.sign(tf[t]["pre2013"]["acf"]["lag1"]) != np.sign(tf[t]["post2013"]["acf"]["lag1"])]
    keep = [t for t in GRID if t not in flip]
    A(f"**The first-lag autocorrelation has the opposite sign in the two eras at "
      f"{', '.join(flip)}** and the same sign at {', '.join(keep)}. Concretely, at M1–M5 the "
      "pre-2013 sample is mildly *trending* (ACF1 between +0.0015 and +0.0247) while the "
      "post-2013 sample is mildly *mean-reverting* (between −0.0183 and −0.0249). M10–M20 are "
      "mildly negative in both eras, and H1–H4 sit at approximately zero or above in both "
      "(H1: +0.0017 / +0.0021; H4: +0.0026 / +0.0090), i.e. the hourly-and-coarser dependence "
      "structure did not change. Two readings are consistent with the data and cannot be "
      "separated with OHLC alone:")
    A("")
    A("1. the dependence structure of XAUUSD genuinely changed around 2013 at intraday "
      "frequencies (positive feedback before, negative after); or")
    A("2. the change of session convention (and of who was quoting) altered the fine-grained print "
      "process without altering the hourly/daily process.")
    A("")
    A("Either way the practical consequence is the same and is the reason this section exists: "
      "**any autocorrelation statistic computed at M1–M5, M30 or H2 and pooled across 2010–2026 "
      "mixes two eras with opposite signs and is therefore close to meaningless as a point "
      "estimate** — which "
      "is a large part of why the pooled ACF1 values in §6.1 are all so near zero. It is a further "
      "argument for treating the fine granularities as descriptive rather than predictive, and it "
      "is the reason the temporal-stability component of the score is measured on yearly blocks "
      "rather than on the pooled sample. It is also an argument in favour of the coarse end for any "
      "*context* work: M10–M20, H1 and H4 are the only granularities whose dependence structure "
      "is stable across the break, and of those only H1 and H4 sit at or above the 30–60 "
      "minute variance-ratio crossing of section 6.5.")
    A("")
    A("Median range falls from pre to post at every granularity (M1: 2.447 → 2.129 bps) and "
      "contiguity *improves* (M1: 99.09% → 99.88%), i.e. the post-2013 data is cleaner and calmer, "
      "which is the opposite of what a naive 'more recent = noisier' assumption would give.")
    A("")
    A("---")
    A("")

    # ---------------- 14 ------------------------------------------------ #
    A("## 14. `2026_SANITY_CHECK`")
    A("")
    A("2026 is a **partial year** (January–August, 8 months). It is reported for integrity only. "
      "It contributes to no score, no ranking and no selection (L5).")
    A("")
    rows = []
    for t in GRID:
        y = tf[t]["y2026"]["full"] if "full" in tf[t]["y2026"] else tf[t]["y2026"]
        f = tf[t]["full"]
        rows.append([t, f"{y['bars']:,}", f"{y['acf']['lag1']:+.5f}",
                     f"{f['acf']['lag1']:+.5f}",
                     f"{y['amplitude']['range_bps']['median']:.3f}",
                     f"{f['amplitude']['range_bps']['median']:.3f}",
                     f"{y['returns']['excess_kurtosis']:.2f}",
                     f"{y['integrity']['contiguous_step_rate']*100:.2f}%"])
    A(md_table(["TF", "2026 bars", "ACF lag1 2026", "ACF lag1 full sample",
                "median range 2026 (bps)", "median range full (bps)",
                "excess kurtosis 2026", "contiguous 2026"], rows))
    A("")
    A("2026 is a high-amplitude year at every granularity (median M1 range 4.618 bps against "
      "2.258 bps for the full sample; H1 40.30 against 20.89), consistent with the price reaching "
      "the sample maximum of 5,596.81 recorded in Phase 1. Continuity is at or above the full-sample "
      "level. Nothing in 2026 contradicts the full-sample conclusions; nothing in 2026 was used to "
      "reach them.")
    A("")
    A("---")
    A("")
    return "\n".join(L)


def make_report_part2(M, VS, SC, verdict, variants):
    tf = M["timeframes"]
    comp = SC["components"]
    W = SC["weights"]
    L = []
    A = L.append

    # ---------------- 15 ------------------------------------------------ #
    A("## 15. SIGNAL / NOISE score")
    A("")
    A("Weights were fixed **before any metric was computed** and are not tuned afterwards. Each "
      "sub-component is min-max normalised across the twelve granularities, so 1.00 = best in the "
      "grid and 0.00 = worst in the grid on that sub-component. Normalisation is relative to the "
      "grid, not an absolute quality judgement.")
    A("")
    rows = []
    for name, w in W["S"].items():
        lab = {"S1_acf_stability": "stability of ACF(1) across years (inverted dispersion)",
               "S2_low_alternation": "low ultra-short alternation (1 − sign-change freq)",
               "S3_run_persistence": "run persistence (mean directional run)",
               "S4_directional_efficiency": "directional efficiency (h = 10 bars)",
               "S5_variance_stability": "variance stability (1/(1+CV of yearly std))",
               "S6_tail_stability": "tail stability (inverted excess kurtosis, log)"}[name]
        rows.append([name, lab, f"{w:.2f}"])
    A(md_table(["sub-component", "measures", "weight"], rows))
    A("")
    rows = []
    for t in GRID:
        c = comp[t]
        rows.append([t] + [f"{c[k]:.3f}" for k in W["S"]] + [f"**{c['S']:.4f}**"])
    A(md_table(["TF"] + list(W["S"]) + ["**S**"], rows))
    A("")
    A("**The sub-components contradict each other, and that contradiction is the result.** "
      "Their argmaxima are: S1 → M20, S2 → H4, S3 → M3, S4 → H4, S5 → H1, S6 → H4. Six independent "
      "noise/persistence diagnostics point at four different granularities. The block therefore "
      "does **not** identify a granularity, and the composite `S` column above must be read as a "
      "compromise between diagnostics that disagree, not as a measurement.")
    A("")
    A("Two of the six are also known to be weak (see the discrimination audit in §17.3): S5 is "
      "noise-dominated (cross-grid spread 0.0028 against a standard error of 0.0268) and S4 rests "
      "on a comparison that section 7.1 showed to be invalid. Removing them leaves S1 (-> M20), "
      "S2 (-> H4), S3 (-> M3) and S6 (-> H4), still pointing at three different granularities.")
    A("")
    A("---")
    A("")

    # ---------------- 16 ------------------------------------------------ #
    A("## 16. AMPLITUDE / COST score")
    A("")
    rows = []
    for name, w in W["A"].items():
        lab = {"A1_median_range": "median bar range (bps, log)",
               "A2_p90_range": "P90 bar range (bps, log)",
               "A3_cost_ratio_mid_scenario": "median range / cost scenario 3 (0.25 USD, log)",
               "A4_cost_ratio_stability": "stability of the yearly median range (1/(1+CV))",
               "A5_cost_tolerance": "share of bars whose range exceeds 1.00 USD"}[name]
        rows.append([name, lab, f"{w:.2f}"])
    A(md_table(["sub-component", "measures", "weight"], rows))
    A("")
    rows = []
    for t in GRID:
        c = comp[t]
        rows.append([t] + [f"{c[k]:.3f}" for k in W["A"]] + [f"**{c['A']:.4f}**"])
    A(md_table(["TF"] + list(W["A"]) + ["**A**"], rows))
    A("")
    A("Unlike the signal/noise block, this one is **unanimous**: all five sub-components are "
      "monotone increasing in bar length (Spearman rho = +1.00 against log k). Of the four inputs "
      "that the discrimination audit tests, three (A1, A2, A5) pass it by two to three orders "
      "of magnitude and only A4 is noise-dominated; A3 is a monotone rescaling of A1. The amplitude/cost gradient is the most reliable "
      "ordering produced in this phase — and it points in exactly the opposite direction to the "
      "preservation blocks.")
    A("")
    A("It carries the caveat of §9 in full: the cost side is hypothetical "
      "(`BROKER_COST_STATUS = EXTERNAL_INPUT_REQUIRED`). If real execution costs are materially "
      "lower than 0.05 USD round-trip, the whole block becomes less decisive; if they are "
      "materially higher than 1.00 USD, it becomes decisive against everything below H1.")
    A("")
    A("---")
    A("")

    # ---------------- 17 ------------------------------------------------ #
    A("## 17. GRANULARITY_QUALITY_SCORE")
    A("")
    A("### 17.1 Definition")
    A("")
    A("`GRANULARITY_QUALITY_SCORE = 0.25·S + 0.20·A + 0.25·C + 0.15·D + 0.05·E + 0.10·F`")
    A("")
    rows = [
        ["S", "Signal / noise", "0.25", "§15 — does any signal survive at this scale?"],
        ["A", "Amplitude / cost", "0.20", "§16 — is a movement large relative to a cost?"],
        ["C", "Structural preservation", "0.25", "§11 — how much of the M1 substrate survives?"],
        ["D", "Temporal stability", "0.15", "§12 — is the measurement stable year to year?"],
        ["E", "Data continuity", "0.05", "§11 — are the bars homogeneous observations?"],
        ["F", "Information retention", "0.10", "§11 — how much path/reversal is kept?"],
    ]
    A(md_table(["block", "name", "weight", "question it answers"], rows))
    A("")
    A("Sub-weights: C = 0.40 observations retained + 0.35 timing precision + 0.25 swing resolution; "
      "D = 0.30 ACF1 + 0.25 alternation + 0.25 range + 0.20 efficiency stability; "
      "E = 0.60 no internal gap + 0.40 no internal market break; "
      "F = 0.45 path retention + 0.30 reversal retention + 0.25 series continuity.")
    A("")
    A("### 17.2 Result")
    A("")
    order = sorted(GRID, key=lambda t: -comp[t]["GQS"])
    rows = []
    for t in order:
        c = comp[t]
        rows.append([c["rank"], t] + [f"{c[g]:.4f}" for g in "SACDEF"] +
                    [f"**{c['GQS']:.4f}**"])
    A(md_table(["rank", "TF", "S", "A", "C", "D", "E", "F", "**GQS**"], rows))
    A("")
    o3 = sorted(GRID, key=lambda t: -comp[t]["GQS"])
    rng = comp[o3[0]]["GQS"] - comp[o3[-1]]["GQS"]
    A(f"The declared composite ranks **{o3[0]} first ({comp[o3[0]]['GQS']:.4f})**, "
      f"{o3[1]} second ({comp[o3[1]]['GQS']:.4f}), {o3[2]} third ({comp[o3[2]]['GQS']:.4f}). "
      f"The gap between first and third is {comp[o3[0]]['GQS']-comp[o3[2]]['GQS']:.4f} against a "
      f"total range of {rng:.4f} — under "
      f"{100*(comp[o3[0]]['GQS']-comp[o3[2]]['GQS'])/rng:.0f}% of the spread. That is a plateau, "
      "not a peak.")
    A("")
    A("### 17.3 Discrimination audit (why the plateau cannot be resolved)")
    A("")
    A("For every raw metric feeding the score, the spread across the twelve granularities is "
      "compared with the metric's own worst-case standard error. Where the spread is smaller than "
      "the error, min-max normalisation turns sampling noise into a 0→1 ranking and the "
      "sub-component carries no information.")
    A("")
    rows = []
    for name, v in verdict.items():
        rows.append([name, v])
    A(md_table(["sub-component input", "verdict"], rows))
    A("")
    A("Three inputs are **noise-dominated**: `S5_variance_stability` (spread 0.0028 vs SE 0.0268 — "
      "the yearly-CV of return dispersion is 0.822 ± 0.001 at *every* granularity, i.e. volatility "
      "is equally stable at every scale), `A4_cost_ratio_stability` and `D3_range_stability` "
      "(these two are the same underlying quantity, the CV of the yearly median range, counted in "
      "two blocks). Four more are marginal: S1, S2, D2, D4.")
    A("")
    A("### 17.4 Robustness of the ranking")
    A("")
    A("Eleven composites were computed: the declared one plus equal block weights, each of the "
      "six blocks dropped in turn, rank-average instead of min-max, the reliability-filtered "
      "variant (drop the three noise-dominated inputs and renormalise within the block), and the "
      "reliable-only variant (drop the four marginal ones as well).")
    A("")
    rows = []
    for name, d in variants.items():
        o = sorted(GRID, key=lambda t: -d[t]) if "rank" not in name else \
            sorted(GRID, key=lambda t: d[t])
        rows.append([name, " > ".join(f"{t} ({d[t]:.3f})" for t in o[:4])])
    A(md_table(["variant", "top four"], rows))
    A("")
    tops = {n: (sorted(GRID, key=lambda t: d[t]) if "rank" in n
                else sorted(GRID, key=lambda t: -d[t]))[:3]
            for n, d in variants.items()}
    wins = {}
    for n, o in tops.items():
        wins[o[0]] = wins.get(o[0], 0) + 1
    exact = sum(1 for o in tops.values() if set(o) == {"M1", "M2", "M3"})
    g1 = variants["v1 declared (this report)"]["M1"] - variants["v1 declared (this report)"]["M3"]
    g5 = (variants["v5 drop noise-dominated (S5,A4,D3)"]["M1"]
          - variants["v5 drop noise-dominated (S5,A4,D3)"]["M3"])
    A(f"* The **top group is stable**: {exact} of the {len(variants)} variants return exactly "
      f"{{M1, M2, M3}} as their top three. The two exceptions are the two variants that delete an "
      f"entire preservation block (`drop block C` → M3, M2, M15 and `drop block F` → M3, M15, M5), "
      f"which is expected: those are the blocks that pull the score towards the fine end.")
    A(f"* The **ordering inside the group is not stable**. Winners: "
      + ", ".join(f"{k} in {v}" for k, v in sorted(wins.items(), key=lambda x: -x[1]))
      + f". M1 leads the declared composite by {g1:.4f} and M3 leads the reliability-filtered "
        f"composite by {abs(g5):.4f} — the sign of the M1-vs-M3 comparison flips depending only on "
        f"whether the three noise-dominated inputs are included.")
    A("* **Blocks A, C, E and F are monotone in log k** (|Spearman| ≥ 0.99), so the score is "
      "structurally a tug-of-war between two opposing gradients: 0.45 of weight favours coarse "
      "(S + A) and 0.40 favours fine (C + E + F), with the remaining 0.15 (D) peaking in the "
      "middle at M5–M15.")
    A("")
    A("**Conclusion of the audit:** the data determines the *zone* (M1–M5) with high confidence and "
      "the *point inside it* with low confidence. Reporting M3 as a precise optimum would be false "
      "precision.")
    A("")
    A("---")
    A("")

    # ---------------- 18 ------------------------------------------------ #
    A("## 18. Timeframe selection")
    A("")
    A("```")
    A("PRIMARY_TIMEFRAME   = M3")
    A("SECONDARY_TIMEFRAME = M1")
    A("CONTEXT_TIMEFRAME   = H1")
    A("REJECTED            = H4  (continuity: 16.46% of bars contain a missing-data gap,")
    A("                            10.23% contain an internal market break)")
    A("CONFIDENCE          = HIGH on the M1-M5 zone | MODERATE on M3 | LOW on any finer distinction")
    A("```")
    A("")
    A("### 18.1 PRIMARY — M3")
    A("")
    rows = [
        ["composite", f"argmax among all aggregations with k >= 2 ({comp['M3']['GQS']:.4f}), "
                      f"{comp['M1']['GQS']-comp['M3']['GQS']:.4f} behind M1 in the declared "
                      "composite — inside the plateau"],
        ["robustness", "top-3 in 9 of the 11 robustness variants (the 2 exceptions delete an "
                       "entire preservation block); M1 first in 6, M3 first in 4, M2 first in 1"],
        ["amplitude / cost", "median range 0.671 USD (4.26 bps) — 1.89x M1. Cost scenario 3 "
                             "(0.25 USD) = 37.3% of the median bar range vs 70.4% at M1"],
        ["noise", "excess kurtosis 46.3 vs 88.6 at M1 (−48%) for one third of the observations"],
        ["preservation", "33.43% of observations retained, 2.991 M1 bars per bar, 72.7% of the "
                         "intrabar path, 0.48 intrabar reversals lost per bar"],
        ["continuity", "99.32% contiguous steps; 0.11% of bars contain an internal data gap "
                       "(M1: 0.00%; H1: 3.16%) — the continuity cost of leaving M1 is negligible "
                       "at k = 3 and becomes material only from M30 upwards"],
        ["signal", "no worse than any other granularity: ACF lag1 = −0.0121, sign-change 0.5133, "
                   "DE h=10 = 0.3082 — all inside the plateau of indistinguishable values"],
    ]
    A(md_table(["criterion", "evidence"], rows))
    A("")
    A("The decisive comparison is M3 against M1. M1 is better on preservation (it *is* the "
      "substrate, so C, E and F are maximal there by construction rather than by measurement). M3 "
      "is better on amplitude/cost and on tail heaviness. Because M1's advantage on three of the "
      "six blocks is partly tautological, and because the M1-vs-M3 ordering inverts under "
      "reliability filtering, the tie is broken in favour of the granularity that is measured "
      "rather than the one that is assumed — while M1 is retained as SECONDARY, so nothing is lost "
      "if a later phase disagrees.")
    A("")
    A("### 18.2 SECONDARY — M1")
    A("")
    A("M1 is the lossless substrate. Every other granularity in this phase is derived from it; "
      "every structural claim made at M3, H1 or anywhere else must be traceable back to it. It "
      "wins the declared composite (0.6275), it has zero aggregation distortion, zero internal "
      "gaps and zero information loss by construction, and it is the only resolution at which the "
      "order of moves is preserved. It is designated SECONDARY rather than PRIMARY only because "
      "its amplitude/cost position (cost scenario 3 = 70.4% of the median bar range) makes it "
      "unsuitable as the default working resolution.")
    A("")
    A("### 18.3 CONTEXT — H1")
    A("")
    A("H1 is the first granularity above the variance-ratio crossing identified in §6.5: below "
      "roughly 30 minutes the series is mildly mean-reverting (VR < 1), at H1 it is at parity "
      "(0.978) and by H4 it is mildly trend-persistent (1.060). If a higher-timeframe view is "
      "needed for context, H1 is the first scale at which the character of the process has actually "
      "changed rather than merely been resampled. It is also 20x the primary, which is a real "
      "separation rather than a cosmetic one. Together with H4 it is one of only two granularities "
      "above M5 whose first-lag autocorrelation does **not** change sign across the 2013 break "
      "(§13) — a genuine robustness advantage for context work that H4 forfeits on continuity.")
    A("")
    A("Known defect, disclosed: **3.16% of H1 bars contain an internal missing-data gap** and H1 "
      "contiguity is 95.70%. Any H1-level statement must be verified against M1 before it is used.")
    A("")
    A("### 18.4 REJECTED — H4")
    A("")
    A("H4 is not dropped from any table, but it is rejected as a candidate:")
    A("")
    A("* **16.46%** of H4 bars contain a missing-data gap inside them — roughly one bar in six is "
      "not a homogeneous 4-hour observation and does not announce it;")
    A("* **10.23%** contain an internal market break (weekend or overnight), so a single H4 'bar' "
      "can span a closed market;")
    A("* mean 7.17 missing M1 minutes per bar;")
    A("* path retention 0.0681 (93.2% of the movement discarded) and 107.30 intrabar reversals lost "
      "per bar;")
    A("* it scores last on the composite (0.4525) and last or near-last on C, E and F.")
    A("")
    A("H2 is disfavoured for the same reason in milder form (5.22% of bars with an internal gap, "
      "the worst contiguity in the grid at 92.16%).")
    A("")
    A("### 18.5 Why this is not `TIMEFRAME_SELECTION = UNRESOLVED`")
    A("")
    A("The signal/noise block is genuinely contradictory (§15) and the composite peak is a plateau "
      "(§17.4). That would normally force `UNRESOLVED`. It does not here, for one reason: **the "
      "two candidates on either side of the ambiguity are both retained.** Whether the programme "
      "works at M3 (PRIMARY) or falls back to M1 (SECONDARY) changes the working resolution by a "
      "factor of three, and nothing downstream depends on which of the two is called primary — the "
      "designated context frame and the rejected frame are the same either way. The ambiguity is "
      "real, quantified, and made harmless by the structure of the recommendation rather than "
      "papered over with a false precision.")
    A("")
    A("If a future phase requires a single resolution and must choose between M1 and M3, that "
      "choice cannot be made from Phase 2 evidence and must be justified from the requirements of "
      "that phase.")
    A("")
    A("---")
    A("")

    # ---------------- 19 ------------------------------------------------ #
    A("## 19. Limitations of Phase 2")
    A("")
    A("1. **No order book (L8).** Everything is OHLC. §6.5 is labelled `INFERENCE / PROXY` and must "
      "never be quoted as a microstructure measurement.")
    A("2. **No broker cost (L9).** §9–§10 are a hypothetical sensitivity grid. "
      "`BROKER_COST_STATUS = EXTERNAL_INPUT_REQUIRED`.")
    A("3. **Volume unknown (L1).** No volume-weighted or volume-confirmed statistic exists; "
      "breakout and range statistics are price-only and could partly reflect quoting inactivity "
      "rather than market structure.")
    A("4. **Price decimals not homogenised (L3).** Amplitudes are as-delivered; a tick-size change "
      "inside the sample would appear as an amplitude change.")
    A("5. **Gaps are real (L2).** Coarse bars containing gaps are counted, not repaired; §11 and "
      "§18.4 report them.")
    A("6. **The 2013 break (L4) reverses the sign of the first-lag autocorrelation** at M1–M5, M30 "
      "and H2 (§13), so any autocorrelation statistic at those granularities computed on the "
      "pooled 2010–2026 sample mixes two eras with opposite signs and is descriptive only.")
    A("7. **2026 is partial (L5)** and is used nowhere.")
    A("8. **Extremes stay in (L6).** The 5σ exercise is a sensitivity exclusion, reported beside "
      "the main result, never replacing it.")
    A("9. **The composite plateau is not resolvable** with these diagnostics (§17.3–17.4).")
    A("10. **Bar-count invariance of recovery delay** (§6.3) means any timing claim at coarse "
      "granularity is a statement about bars, not about minutes.")
    A("11. **No out-of-sample, no forward test, no strategy.** Nothing here has been validated "
      "against anything it was not computed from.")
    A("")
    A("---")
    A("")

    # ---------------- 20 ------------------------------------------------ #
    A("## 20. Audit — contamination and prohibition check")
    A("")
    A("| prohibition | status | evidence |")
    A("|---|---|---|")
    A("| No regime construction | PASS | no regime object, label, state or segmentation is created "
      "anywhere; `by_year`, `pre2013`, `post2013`, `y2026` and the volatility strata are calendar "
      "and descriptive splits, explicitly labelled non-regime |")
    A("| No regime labels | PASS | no regime identifier, state variable or label is attached to "
      "any bar, window or period; the word *regime* appears only in prose describing what was "
      "NOT done and in the phase title; the strings `bull`, `bear`, `trend_state` appear "
      "nowhere |")
    A("| No HMM / clustering / fitting | PASS | no model, no likelihood, no latent variable, no "
      "fit of any kind is performed; every number is a descriptive statistic |")
    A("| No strategy | PASS | no entry, exit, stop, target, position or rule exists |")
    A("| No backtest | PASS | no simulated sequence of positions |")
    A("| No strategy optimisation | PASS | no parameter search; the twelve granularities are a "
      "fixed grid declared before measurement, and the score weights are declared before results "
      "are read |")
    A("| No profitability metric | PASS | no return, PnL, Sharpe, Sortino, Calmar, drawdown, hit "
      "rate, expectancy, profit factor or win/loss figure is computed |")
    A("| No timeframe selection from trading results | PASS | the selection in §18 uses only "
      "structure preservation, noise, signal persistence, stability, amplitude, cost and "
      "continuity |")
    A("| No volume | PASS | the volume column is never loaded (L1): `build_timeframes.py` reads "
      "only timestamp and OHLC, `analyze_timeframes.py` and `variance_signature.py` read only "
      "the columns they need; the word *volume* appears solely in comments, the manifest and "
      "this audit |")
    A("| No invented broker cost | PASS | all costs are declared hypothetical scenarios in USD; "
      "`BROKER_COST_STATUS = EXTERNAL_INPUT_REQUIRED` |")
    A("| No microstructure claim | PASS | §6.5 and every variance statement are labelled "
      "`INFERENCE / PROXY` |")
    A("| No gap filling | PASS | `gap_policy = none` in the build manifest; no window is padded |")
    A("| No invented M1 bars | PASS | a window with zero M1 bars produces no row |")
    A("| No modification of source OHLC | PASS | the seven fragments are read-only; the M1 master "
      "SHA-256 is unchanged from Phase 1; aggregation writes only to new files |")
    A("| No deletion of anomalies | PASS | extremes remain in every full-sample statistic; the 5σ "
      "exercise is a parallel sensitivity block (L6) |")
    A("| No EURUSD import | PASS | no Phase-1 or external asset conclusion is imported; XAUUSD is "
      "measured from scratch |")
    A("| Phase 1 left closed | PASS | no Phase-1 artefact was reopened or modified |")
    A("")
    A("**Reproducibility.** Every artefact is regenerated by five scripts, in order:")
    A("")
    A("```bash")
    A("python research/timeframe_audit/scripts/build_timeframes.py     # grid + manifest")
    A("python research/timeframe_audit/scripts/analyze_timeframes.py   # metrics_tf.json")
    A("python research/timeframe_audit/scripts/variance_signature.py   # contiguous-step VR")
    A("python research/timeframe_audit/scripts/score_and_render.py     # scores + CSVs")
    A("python research/timeframe_audit/scripts/render_phase2.py        # figures + this report")
    A("```")
    A("")
    A("Deterministic given the M1 master: epoch-aligned windows, fixed grid, no sampling, no random "
      "seed, no external state.")
    A("")
    A("---")
    A("")

    # ---------------- 21 ------------------------------------------------ #
    A("## 21. Conclusion and final gate")
    A("")
    A("Twelve granularities were built deterministically from a single verified M1 substrate and "
      "measured on the full 2010–2026 sample, on each of the sixteen full years separately, on the "
      "pre- and post-2013 eras, and under a 5σ sensitivity exclusion.")
    A("")
    A("The headline result is negative and it is the most useful thing this phase produced: "
      "**across the entire M1 → H4 range, XAUUSD shows no linear signal at any scale.** "
      "Autocorrelation stays inside ±0.013 on the full sample (±0.020 on contiguous steps), sign "
      "alternation stays within 0.02 of a coin flip, and "
      "the variance ratio stays within 0.96–1.06. The apparently large noise-reduction benefit of "
      "aggregation — excess kurtosis falling from 88.6 to 15.7 — is produced by less than half a "
      "percent of bars and disappears when they are excluded. No choice of timeframe can be "
      "justified by claiming it reveals signal.")
    A("")
    A("What remains is a clean, honest trade-off: coarse bars buy amplitude relative to cost "
      "(unanimous, monotone, reliable) at the price of information, continuity and structural "
      "fidelity (also unanimous and monotone). The composite resolves that trade-off into a "
      "plateau over M1–M5 rather than a peak, and the ordering inside the plateau is not "
      "determined by the data.")
    A("")
    A("Against that background: `PRIMARY_TIMEFRAME = M3`, `SECONDARY_TIMEFRAME = M1`, "
      "`CONTEXT_TIMEFRAME = H1`, `H4` rejected on continuity grounds. The one structural feature "
      "found anywhere — the variance-ratio crossing between 30 and 60 minutes — is what places the "
      "context frame at H1, and it is the strongest candidate for a genuine scale-dependent "
      "property of XAUUSD in this dataset.")
    A("")
    A("### Final gate")
    A("")
    A("```")
    A("PHASE_2_STATUS              = COMPLETE")
    A("PRIMARY_TIMEFRAME           = M3")
    A("SECONDARY_TIMEFRAME         = M1")
    A("CONTEXT_TIMEFRAME           = H1")
    A("REJECTED_TIMEFRAMES         = H4 (and H2 disfavoured)")
    A("TIMEFRAME_SELECTION         = RESOLVED_WITH_QUALIFIED_CONFIDENCE")
    A("BROKER_COST_STATUS          = EXTERNAL_INPUT_REQUIRED")
    A("MICROSTRUCTURE_CLAIMS       = NONE (all INFERENCE / PROXY)")
    A("VOLUME_USED                 = NO (unit unknown, L1)")
    A("REGIME_CONSTRUCTION         = NOT PERFORMED")
    A("STRATEGY_OR_BACKTEST        = NOT PERFORMED")
    A("PERFORMANCE_METRICS         = NOT COMPUTED")
    A("SOURCES_MODIFIED            = NO")
    A("EXTREMES_REMOVED            = NO (L6)")
    A("GAPS_FILLED                 = NO (L2)")
    A("2026_USED_FOR_SELECTION     = NO (L5, sanity check only)")
    A("NEXT_ACTION                 = STOP — no regime construction until Phase 2 is reviewed")
    A("```")
    A("")
    A("**Phase 2 is complete and the programme stops here.** No regime construction, no regime "
      "labelling, no model fitting and no strategy work has been started, and none may begin until "
      "this report has been reviewed and Phase 3 is explicitly commissioned.")
    A("")
    A("### Deliverables")
    A("")
    A("| file | contents |")
    A("|---|---|")
    A("| `XAUUSD_TIMEFRAME_COMPARISON.csv` | 12 rows × 58 columns — the full measurement grid |")
    A("| `XAUUSD_SIGNAL_NOISE_ANALYSIS.csv` | noise, dependence, moments, tails, efficiency |")
    A("| `XAUUSD_AMPLITUDE_COST_ANALYSIS.csv` | ratio matrix (12 × 5 scenarios × 4 statistics) + "
      "max-cost thresholds at 1/2/5/10/20% |")
    A("| `XAUUSD_GRANULARITY_SCORECARD.csv` | 6 blocks, 20 sub-components, composite, rank |")
    A("| `XAUUSD_INFORMATION_LOSS.csv` | retained / lost / distortion / continuity per timeframe |")
    A("| `XAUUSD_YEARLY_STABILITY.csv` | all key metrics per year, stability summary, volatility "
      "strata |")
    A("| `XAUUSD_TIMEFRAME_SELECTION_REPORT.md` | this report |")
    A("| `figures/variance_vs_sampling_frequency.png` | the signature plot |")
    A("| `figures/signal_noise_by_timeframe.png` | noise diagnostics |")
    A("| `figures/amplitude_cost_by_timeframe.png` | amplitude vs hypothetical cost |")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--metrics", default="/tmp/xauusd_audit/metrics_tf.json")
    ap.add_argument("--scores", default="/tmp/xauusd_audit/scores.json")
    ap.add_argument("--vsig", default="/tmp/xauusd_audit/variance_signature.json")
    ap.add_argument("--verdict", default="/tmp/xauusd_audit/verdict.json")
    ap.add_argument("--tfdir", default="/tmp/xauusd_audit/timeframes")
    ap.add_argument("--outdir", default="research/timeframe_audit")
    a = ap.parse_args()

    M = json.load(open(a.metrics))
    M["_tfdir"] = a.tfdir
    man = json.load(open(os.path.join(a.tfdir, "manifest.json")))
    M["_man"] = man
    M["_manifest"] = {g["timeframe"]: g for g in man["grid"]}
    M["_scores"] = json.load(open(a.scores))
    VS = json.load(open(a.vsig))
    verdict = json.load(open(a.verdict))
    SC = M["_scores"]

    # robustness variants (same definitions as audited in section 17.4)
    blocks = {
        "S": [("S1_acf_stability", .15), ("S2_low_alternation", .20),
              ("S3_run_persistence", .15), ("S4_directional_efficiency", .20),
              ("S5_variance_stability", .15), ("S6_tail_stability", .15)],
        "A": [("A1_median_range", .25), ("A2_p90_range", .20),
              ("A3_cost_ratio_mid_scenario", .25), ("A4_cost_ratio_stability", .15),
              ("A5_cost_tolerance", .15)],
        "C": [("C1_observations_retained", .40), ("C2_timing_precision", .35),
              ("C3_swing_resolution", .25)],
        "D": [("D1_acf1_stability", .30), ("D2_alternation_stability", .25),
              ("D3_range_stability", .25), ("D4_efficiency_stability", .20)],
        "E": [("E1_no_internal_data_gap", .60), ("E2_no_internal_market_break", .40)],
        "F": [("F1_path_retention", .45), ("F2_reversal_retention", .30),
              ("F3_series_continuity", .25)],
    }
    Wc = {"S": .25, "A": .20, "C": .25, "D": .15, "E": .05, "F": .10}
    comp = SC["components"]

    def build(drop):
        out = {}
        for t in GRID:
            tot = 0.0
            for b, parts in blocks.items():
                ps = [(n, w) for n, w in parts if n not in drop]
                ws = sum(w for _, w in ps)
                tot += Wc[b] * sum(w * comp[t][n] for n, w in ps) / ws
            out[t] = tot
        return out

    rk = {b: {t: 0 for t in GRID} for b in blocks}
    for b in blocks:
        for i, t in enumerate(sorted(GRID, key=lambda x: -comp[x][b]), 1):
            rk[b][t] = i
    variants = {
        "v1 declared (this report)": build(set()),
        "v2 equal block weights": {t: float(np.mean([comp[t][b] for b in blocks])) for t in GRID},
    }
    for b in blocks:
        ws = [x for x in blocks if x != b]
        variants[f"v3 drop block {b}"] = {t: float(np.mean([comp[t][x] for x in ws])) for t in GRID}
    variants["v4 rank-average"] = {t: float(np.mean([rk[b][t] for b in blocks])) for t in GRID}
    variants["v5 drop noise-dominated (S5,A4,D3)"] = build(
        {"S5_variance_stability", "A4_cost_ratio_stability", "D3_range_stability"})
    variants["v6 reliable inputs only"] = build(
        {"S5_variance_stability", "A4_cost_ratio_stability", "D3_range_stability",
         "S1_acf_stability", "S2_low_alternation", "D2_alternation_stability",
         "D4_efficiency_stability"})

    os.makedirs(a.outdir, exist_ok=True)
    make_figures(M, VS, a.outdir)
    part1 = make_report(M, VS, SC, a.outdir, verdict)
    part2 = make_report_part2(M, VS, SC, verdict, variants)
    with open(os.path.join(a.outdir, "XAUUSD_TIMEFRAME_SELECTION_REPORT.md"), "w") as fh:
        fh.write(part1 + "\n" + part2)
    print("report written:", os.path.join(a.outdir, "XAUUSD_TIMEFRAME_SELECTION_REPORT.md"))


if __name__ == "__main__":
    main()
