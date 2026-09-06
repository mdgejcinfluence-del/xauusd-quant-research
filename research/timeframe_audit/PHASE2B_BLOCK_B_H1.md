# PHASE 2B — BLOCK B
## H1 CONTEXT / PERSISTENCE / CONTINUITY

**Status:** ANALYTICAL ONLY · PRE-REGIME · PRE-STRATEGY
**Object:** characterisation of H1 as a *context* resolution. Audit of confirmation/revision, not a new selection.
**Source:** `/tmp/xauusd_audit/deep_metrics.json` — read only. No engine re-run, no heavy recomputation, no new dataset.
**Official decision:** `PRIMARY = M3` / `SECONDARY = M1` / `CONTEXT = H1` — **UNTOUCHED by this block.**

---

## 1. OBJECTIVE

Determine whether the measured behaviour of the H1 series justifies the role

```
CONTEXT_TIMEFRAME = H1
```

under the specific reading required by the mission: **H1 must be sufficiently stable and informative to serve as a resolution of context, without any claim that H1 itself provides a trading signal.**

Five axes only:

1. directional persistence
2. volatility dynamics
3. temporal continuity
4. historical stability
5. behaviour transition across volatility states

Excluded by construction: strategy, return, backtest, Sharpe, expectancy, hit rate, profit factor, drawdown, optimisation, regime object, regime label, and the volume column (Phase 1 limitation **L1**).

Frozen Phase 1 limitations remain binding: **L1** volume never loaded · **L2** no gap filling · **L3** no price-decimal homogenisation · **L4** the ~2013 session-convention break stays documented · **L5** 2026 is partial, sanity check only · **L6** extremes retained · **L7** sources never modified.

---

## 2. RAW SOURCE

### 2.1 Provenance and integrity (verified 2026-09-06)

| Item | Value |
|---|---|
| Source file | `/tmp/xauusd_audit/deep_metrics.json` |
| Size / SHA-256 | 657,646 B · `c3774bfcef7a3895d0b8766c2d013b0349814d9cf413b1ac10bb59e31be20c52` |
| mtime | 2026-09-06 10:12:09 UTC — unchanged since the single production run |
| Produced by | `research/timeframe_audit/scripts/deep_audit.py` (one execution, 107 s, exit 0) |
| M1 master | `/tmp/xauusd_audit/XAUUSD_M1_reconstructed.parquet`, SHA-256 `fdce55a8c8a76c417765ad020794866bb36e5b166c130d2bb59e31be20c52` — matches the Phase 1 record and the grid manifest |
| `deep_audit.py` re-run | **NO** |
| Heavy recomputation | **NO** |
| Dataset / source fragments modified | **NO** |
| Volume column | never loaded (`spec.volume_used = false`) |

**OBSERVATION.** The M1 master hash is identical to the value recorded in Phase 1 and in the 12-timeframe grid manifest. No source file was opened for writing in this block.

### 2.2 Ex-ante specification carried in the file (fixed before any metric was computed)

| Parameter | Value |
|---|---|
| Resolutions | M1, M3, H1 |
| Volatility windows | 60 / 240 / 1440 **wall-clock minutes** (implemented as W/k bars, so the horizon is identical across resolutions) |
| Session windows | 5 fixed UTC windows: 00–06, 06–12, 12–16, 16–21, 21–24 |
| Shock rule | \|log return of one bar\| > 3 × trailing rolling σ of the same series over the previous 1440 wall-clock minutes, past-only |
| Hurst lags | 2, 4, 8, 16, 32, 64 **bars** (identical across resolutions) |
| Hurst estimators | VR-implied (slope of log VR(q) on log q, H = (slope+1)/2) · classical rescaled range R/S |
| ACF lags | 1–5 |
| Volatility classes | HIGH_VOL if trailing 1440-min σ > trailing 1-year *mean* of that σ (both past-only), else LOW_VOL |
| Broker cost | `EXTERNAL_INPUT_REQUIRED` — no broker cost is used anywhere in this block |
| Gaps filled / extremes removed / regime built / strategy tested | `false` / `false` / `false` / `false` |

### 2.3 Definitions used in this report (taken verbatim from the engine)

| Metric | Definition as implemented |
|---|---|
| `acf` | Correlation of `r[t]` and `r[t+lag]` over **fully contiguous** lag-windows only; returns `NaN` if fewer than 100 valid windows |
| `variance_ratio` | `Var(q-period sum) / (q × Var(1-period))` on **non-overlapping, fully contiguous** windows; requires `n ≥ 50·lag`; returns `NaN` if fewer than 100 windows |
| `runs` | Lengths of maximal runs of identical sign among non-zero returns, **broken by any non-adjacency** |
| `de(h)` | Directional efficiency = \|net displacement over h bars\| / (sum of \|bar-to-bar close moves\| over the same h bars). **Path is measured on the bar grid of that resolution.** |
| `hurst_vr` | OLS of log VR(q) on log q; `H = (slope+1)/2`. `short_lags` = fit on {2,4,8}; `long_lags` = fit on {16,32,64}; `all_lags` = fit on all six |
| `hurst_rs` | Mean R/S statistic over contiguous blocks of length m, then OLS of log(R/S) on log m. `MIN_RS_WINDOW = 8`, `MAX_RS_BLOCKS = 20000`, even striding |
| `shock` | \|r_i\| > 3·σ̂_i, σ̂ = trailing rolling std over `round(1440/k)` bars (M1: 1440, M3: 480, H1: 24) |
| `internal_missing` (im) | Minutes absent **strictly inside** the bar |
| `internal_breaks` (ib) | Market closures (gap ≥ 50 min) **strictly inside** the bar (Phase 2 grid definition, `MARKET_BREAK_MIN = 50`) |
| `contig_next` | Whether the next bar is the immediate successor (no missing bar, no closure) |

### 2.4 Declared gaps in the source — nothing here is reconstructed or imported

| Missing item | Status | Consequence |
|---|---|---|
| Per-year VR(q) curves | **NOT AVAILABLE** (only the VR-implied Hurst per year is stored) | The VR curve cannot be tracked year by year; only the Hurst summary of it can |
| R/S Hurst per year and per vol class | **NOT AVAILABLE** (only VR-implied Hurst is split) | No cross-estimator validation inside the annual or volatility splits |
| P25 of amplitude | **NOT AVAILABLE** (quantile grid fixed at P50/P75/P90/P95/P99) | Same gap as Block A; reported as missing, not filled |
| H1 vs M3 / H1 vs M1 paired-by-year discrimination table | **NOT AVAILABLE** in the file (the `discrimination` block covers M3 − M1 only) | Aggregation effects are described from the three global blocks and the three per-year series, not from a pre-computed paired test |
| Ultra-short reversal recovery magnitude / delay | **NOT AVAILABLE** in this file | Only reversal *frequency* is available (sign-change frequency) |
| Session-window DE | **structurally undefined** (see §9.4) | Reported as `NOT_APPLICABLE`, not as a failure |

### 2.5 What is computed in this report

Only **descriptive aggregation of values already present in the file**: across-year mean, median, standard deviation, coefficient of variation, min/max, sign counts, and ratios of already-stored quantities. No metric is recomputed from the price series. This is the aggregation the mission itself requires in §9 ("moyenne", "médiane si disponible", "dispersion annuelle").

**Uncertainty convention (identical to Block A).** Where an interval is quoted it is a **descriptive year-level interval over the 16 full years 2010–2025** (mean difference ± 1.96 × standard error across years). It measures whether an ordering is *stable across years*. It is **not** a bar-level significance test and carries no p-value.

---

## 3. H1 PERSISTENCE

### 3.1 Global values, three resolutions

| Metric | M1 | M3 | **H1** |
|---|---|---|---|
| Bars | 5,874,003 | 1,963,826 | **98,412** |
| ACF lag 1 | −0.009386 | −0.012082 | **−0.000611** |
| ACF lag 2 | −0.006183 | −0.004678 | **−0.004592** |
| ACF lag 3 | −0.003703 | −0.004954 | **+0.002752** |
| ACF lag 4 | +0.000653 | +0.000341 | **+0.002141** |
| ACF lag 5 | −0.000856 | −0.000032 | **+0.000813** |
| Mean run (bars) | 1.9098 | 1.9223 | **1.8515** |
| P90 run | 4 | 4 | 3 |
| Max run | 24 | 20 | 13 |
| Sign-change frequency | 0.5117 | 0.5133 | **0.5189** |
| DE h=5 | 0.4538 | 0.4442 | **0.4609** |
| DE h=10 | 0.3151 | 0.3082 | **0.3357** |
| DE h=20 | 0.2192 | 0.2161 | **0.2477** |

**OBSERVATION 3.1a.** At H1 the autocorrelation at lags 1–2 is one order of magnitude smaller than at M1/M3 (|ACF1| 0.0006 vs 0.0094 / 0.0121) and **changes sign at lag 3**, where M1 and M3 are still negative. H1 is the only one of the three whose ACF is positive at lags 3, 4 and 5.

**OBSERVATION 3.1b.** H1 has the **shortest** runs (mean 1.8515 vs 1.9098 / 1.9223), the **lowest** P90 and max run, and the **highest** sign-change frequency (0.5189 vs 0.5117 / 0.5133).

**INFERENCE 3.1c.** Run statistics are not cleanly comparable across resolutions. Runs are broken both by non-adjacency (H1: 4.30 % of steps non-contiguous, vs 0.68 % at M3) and by exact-zero returns (mostly an M1 phenomenon). The shorter H1 runs are therefore at least partly a continuity artefact, not purely a change in directional behaviour. Direction of the artefact is known; its magnitude is not.

### 3.2 Internal consistency check — VR(2) versus ACF(1)

For a covariance-stationary series the identity `VR(2) = 1 + ρ(1)` holds in population. The file contains both sides, computed on different but overlapping samples.

| TF | VR(2) | Implied ρ(1) = VR(2) − 1 | Measured ACF(1) | Gap |
|---|---|---|---|---|
| M1 | 0.987723 | −0.012277 | −0.009386 | **−0.0029** |
| M3 | 0.987605 | −0.012395 | −0.012082 | **−0.0003** |
| **H1** | **1.034811** | **+0.034811** | **−0.000611** | **+0.0354** |

**OBSERVATION 3.2a.** At M1 and M3 the two estimators of the same population quantity agree to within 0.003. At H1 they disagree by **0.0354**, roughly **twelve times** the M3 discrepancy and **118 times** the value of H1's own ACF(1).

**INFERENCE 3.2b.** H1's VR(2) — the point that anchors the entire "H1 is persistent" reading — is **not corroborated by H1's own autocorrelation**. Both estimators use fully contiguous windows, but VR uses non-overlapping windows (45,063 of them) and ACF uses all overlapping contiguous pairs (90,125). With H1's excess kurtosis of 23.2, the two subsamples can differ materially in variance, and the ratio is not robust to that. **The discrepancy is reported, not resolved**: identifying its cause would require recomputation on the price series, which is forbidden here.

**CONSEQUENCE.** Any statement about H1 persistence must be made **conditional on which estimator is believed**. This report does not choose between them.

### 3.3 Runs, alternation, continuation, reversal

| Metric | M1 | M3 | **H1** |
|---|---|---|---|
| Number of runs | 2,990,355 | 1,003,728 | **50,807** |
| Mean run | 1.9098 | 1.9223 | 1.8515 |
| Median run | 1 | 1 | 1 |
| P90 run | 4 | 4 | 3 |
| Max run | 24 | 20 | 13 |
| Sign-change frequency | 0.5117 | 0.5133 | 0.5189 |

**OBSERVATION 3.3a.** All three resolutions sit just above the 0.5 sign-change frequency of a fair coin (0.5117 → 0.5133 → 0.5189). The excess over 0.5 is monotone increasing in bar size: **+1.17 pp (M1), +1.33 pp (M3), +1.89 pp (H1)**.

**INFERENCE 3.3b.** Under a pure iid sign model with no zero returns, the expected mean run length is `1/(1 − p_repeat)`. The observed mean run of 1.85 at H1 is what a sign-change frequency of 0.5189 implies if runs were geometric. Observed: `1/(1−(1−0.5189)) = 1/0.4811 = 2.079`. The measured 1.8515 is **below** that, i.e. H1 runs are shorter than a geometric model fitted to its own sign-change rate — consistent with runs being truncated by non-adjacency (4.30 % of H1 steps). Same direction as 3.1c.

**OBSERVATION 3.3c (continuation / reversal after shocks — the only direct measure in the file).**

| Quantity (5 bars after a 3σ shock) | M1 | M3 | **H1** |
|---|---|---|---|
| Direction persistence (share continuing the shock direction) | 0.4536 | 0.4527 | **0.5002** |
| Share reverting | 0.5464 | 0.5473 | 0.4998 |
| Mean reversion (bps, + = moved back) | +0.235 | +0.211 | **−1.844** |
| Reversion-positive share | 0.5444 | 0.5461 | 0.4994 |
| Mean \|displacement\| after 5 bars (bps) | 8.32 | 13.53 | 40.63 |

**OBSERVATION 3.3d.** At M1 and M3 the balance after a 3σ shock tilts **against** the shock direction (54.6 % / 54.7 % of cases, net +0.24 / +0.21 bps). At H1 the balance is a **coin flip** (50.02 % continue, 49.94 % revert) with a small net tilt **in favour** of continuation (−1.84 bps).

**LIMITATION 3.3e.** "5 bars" means 5 minutes at M1, 15 minutes at M3 and **5 hours** at H1. The shock definition also differs in σ-window length in bars (1440 / 480 / 24). Resolution and horizon are confounded; 3.3d is reported as a descriptive difference, not as a resolution effect.

### 3.4 Annual distribution of H1 persistence metrics (16 full years)

| Year | ACF1 | ACF2 | Mean run | Sign-change | DE h10 |
|---|---|---|---|---|---|
| 2010 | −0.02558 | +0.00505 | 1.7794 | 0.5453 | 0.3216 |
| 2011 | +0.01164 | −0.03821 | 1.8290 | 0.5329 | 0.3174 |
| 2012 | +0.01747 | +0.01302 | 1.8731 | 0.5224 | 0.3208 |
| 2013 | +0.01855 | −0.00773 | 1.8786 | 0.5072 | 0.3567 |
| 2014 | +0.01857 | −0.02056 | 1.8290 | 0.5239 | 0.3320 |
| 2015 | +0.00181 | −0.00932 | 1.7995 | 0.5332 | 0.3479 |
| 2016 | +0.03850 | −0.01127 | 1.8498 | 0.5180 | 0.3363 |
| 2017 | −0.01710 | −0.00252 | 1.8356 | 0.5221 | 0.3464 |
| 2018 | +0.00441 | +0.01062 | 1.8673 | 0.5128 | 0.3469 |
| 2019 | −0.01440 | +0.01260 | 1.8847 | 0.5067 | 0.3385 |
| 2020 | −0.00198 | +0.05157 | 1.8217 | 0.5267 | 0.3319 |
| 2021 | −0.01321 | +0.00719 | 1.8244 | 0.5262 | 0.3361 |
| 2022 | −0.01378 | +0.00781 | 1.8878 | 0.5070 | 0.3390 |
| 2023 | +0.01424 | +0.02043 | 1.8598 | 0.5151 | 0.3360 |
| 2024 | +0.00382 | +0.00761 | 1.9091 | 0.5005 | 0.3470 |
| 2025 | −0.02624 | −0.01893 | 1.8808 | 0.5087 | 0.3374 |
| **mean** | **+0.00104** | **+0.00171** | **1.85060** | **0.51930** | **0.33699** |
| **median** | **+0.00282** | **+0.00612** | **1.85478** | **0.52007** | **0.33683** |
| **sd** | **0.01834** | **0.02031** | **0.03548** | **0.01206** | **0.01076** |
| **min / max** | −0.0262 / +0.0385 | −0.0382 / +0.0516 | 1.779 / 1.909 | 0.5005 / 0.5453 | 0.3174 / 0.3567 |
| **years > 0** | **9 / 16** | **9 / 16** | 16 / 16 | 16 / 16 | 16 / 16 |

**OBSERVATION 3.4a.** ACF(1) at H1 is **not stable in sign across years**: 9 of 16 years positive, range −0.0262 to +0.0385, sd 0.0183. The year-to-year swing (0.065) is roughly **106×** the value of the global estimate (0.00061).

**OBSERVATION 3.4b.** Mean run, sign-change frequency and DE(h=10) **are** stable: 16/16 years on the same side of zero, coefficients of variation 1.9 %, 2.3 % and 3.2 %.

---

## 4. VARIANCE RATIO

### 4.1 Level and term structure

| Lag q | M1 VR | M1 n | M3 VR | M3 n | **H1 VR** | **H1 n** |
|---|---|---|---|---|---|---|
| 2 | 0.98772 | 2,923,534 | 0.98761 | 970,992 | **1.03481** | **45,063** |
| 4 | 0.97820 | 1,457,302 | 0.97489 | 482,088 | **1.06526** | **20,541** |
| 8 | 0.96592 | 724,815 | 0.96766 | 237,971 | **1.11531** | **8,292** |
| 16 | 0.95826 | 358,928 | 0.97390 | 116,202 | **1.03489** | **2,174** |
| 32 | 0.95678 | 176,343 | 0.98821 | 55,614 | **1.01853** | **190** |
| 64 | 0.98570 | 85,414 | 1.04215 | 25,480 | **1.03802** | **31** |

**OBSERVATION 4.1a (the one genuine qualitative difference).** H1 is the **only** resolution whose VR curve lies entirely above 1 at every lag tested. M1 is below 1 at all six lags (0.9568 – 0.9877). M3 is below 1 at five of six, exceeding 1 only at q = 64 (1.0422).

**OBSERVATION 4.1b (shape).** The H1 curve is **humped**: it rises from 1.0348 (q=2) to a peak of **1.1153 (q=8)**, then falls back to 1.0349 (q=16), 1.0185 (q=32) and 1.0380 (q=64). A VR curve that peaks and then decays is *not* the signature of a constant-H persistent process; it is what a finite-horizon trending or over-reverting component produces.

**OBSERVATION 4.1c (sample size collapse).** H1's VR at q = 32 rests on **190** non-overlapping windows and at q = 64 on **31**. The same lags at M1 use 176,343 and 85,414. **The upper half of the H1 VR curve is effectively unmeasured.**

**INTERPRETATION (strict, per mission §4).**

- VR > 1 is *compatible with* positive persistence.
- VR < 1 is *compatible with* negative dependence / reversion.
- VR is **not** presented here as proof of a causal mechanism, and **not** as evidence of anything profitable. No such claim is made or implied anywhere in this report.

**INFERENCE 4.1d.** Taking 4.1a at face value, H1 would be the scale at which XAUUSD stops exhibiting the short-horizon reversal visible at M1/M3 and starts exhibiting mild trending. Taking 3.2a into account, the same conclusion rests on an estimator that H1's own ACF contradicts by 0.035. **The direction of H1's persistence is therefore reported as UNRESOLVED between estimators, with VR above 1 and ACF at zero.**

### 4.2 Stability across years

Per-year VR(q) curves are **NOT AVAILABLE** in the file. Only the VR-implied Hurst derived from them is stored (§6.2).

### 4.3 Pre/post 2013

Per-era VR(q) curves are **NOT AVAILABLE**. Only the per-era VR-implied Hurst is stored (§6.2).

---

## 5. VOLATILITY-CONDITIONED ANALYSIS

### 5.1 Definition (already in the file, not created here)

`HIGH_VOL` if the bar's trailing 1440-minute σ exceeds the trailing **1-year mean** of that same σ, both strictly past-only; otherwise `LOW_VOL`.

**OBSERVATION 5.1a.** H1 class shares: `HIGH_VOL` 36.97 % · `LOW_VOL` 57.03 % · `UNCLASSIFIED` 6.00 % (warm-up bars with no 1-year trailing mean yet). Because the threshold is *local* (relative to a trailing annual mean), HIGH_VOL is not "absolutely volatile" — it is "more volatile than its own recent year". The observed σ separation is correspondingly moderate (1.77×, below).

### 5.2 H1 comparison, HIGH_VOL vs LOW_VOL

| Metric | H1 HIGH_VOL | H1 LOW_VOL | Ratio H/L |
|---|---|---|---|
| Bars | 36,378 | 56,128 | — |
| **Median range (bps)** | **26.3077** | **17.8870** | **1.471** |
| P90 range (bps) | 63.6395 | 40.6821 | 1.564 |
| Median range (USD) | 4.413 | 2.830 | 1.559 |
| Trailing σ 1440 (bps) | 25.7572 | 14.5177 | **1.774** |
| Return std (bps) | 26.0091 | 17.0404 | 1.526 |
| Excess kurtosis | 22.4615 | 15.4384 | 1.455 |
| **ACF lag 1** | **−0.005903** | **−0.005265** | **1.121** |
| ACF lag 2 | −0.009672 | −0.000047 | — |
| **Mean run** | **1.78793** | **1.81793** | **0.983** |
| **Sign-change freq** | **0.519548** | **0.516429** | **1.006** |
| **DE h=5** | 0.451525 | 0.463280 | 0.975 |
| **DE h=10** | **0.324810** | **0.332564** | **0.977** |
| DE h=20 | 0.242941 | 0.237520 | 1.023 |
| Body/range | 0.440693 | 0.441943 | 0.997 |
| Range/σ (w1440, median) | 1.05562 | 1.19901 | 0.880 |
| Step contiguity | 0.915441 | 0.928466 | 0.986 |
| Internal-gap bars | 0.016081 | 0.027010 | 0.595 |

**OBSERVATION 5.2a (amplitude separates).** The volatility classification does what it says: HIGH_VOL bars have 1.47× the median range, 1.56× the P90 range and 1.77× the trailing σ of LOW_VOL bars.

**OBSERVATION 5.2b (dynamics do not separate).** Every persistence/directional metric is essentially identical between the two states:

- ACF(1): −0.00590 vs −0.00527 (difference 0.00064)
- mean run: 1.788 vs 1.818 (difference 0.030)
- sign-change: 0.5195 vs 0.5164 (difference 0.0031)
- DE(h=10): 0.3248 vs 0.3326 (difference 0.0078)
- body/range: 0.4407 vs 0.4419 (difference 0.0013)

**OBSERVATION 5.2c (one metric moves, and it is not interpretable).** The VR-implied Hurst splits widely: HIGH_VOL **0.5324** vs LOW_VOL **0.3545** (difference 0.178). For reference the same split is 0.4906 vs 0.4879 at M1 (difference 0.003) and 0.5015 vs 0.4897 at M3 (difference 0.012). The H1 split is **15× the M3 split and 59× the M1 split.**

**OBSERVATION 5.2d (why 5.2c is rejected).** The same vol-class Hurst blocks return `long_lags` values of **0.2946** (HIGH_VOL) and **0.1079** (LOW_VOL). A Hurst exponent below ~0.2 is not a plausible description of a traded price series; these are line fits through two noisy VR points at q=16/32/64 inside a subsample where 64-bar contiguous windows almost do not exist (0.915^64 ≈ 0.003). Only **one** estimator (VR-implied) is available per vol class — there is no R/S cross-check at all inside this split.

**VERDICT 5.2e.** H1 volatility-conditioned Hurst: **NOT_INTERPRETABLE.** Reported, not used as evidence.

**OBSERVATION 5.2f (continuity interaction).** HIGH_VOL bars have slightly *worse* step contiguity (0.9154 vs 0.9285) but *fewer* internal-gap bars (1.61 % vs 2.70 %). Both differences are small; there is no large continuity asymmetry between volatility states.

### 5.3 Availability checklist (mission §5)

| Requested | Status |
|---|---|
| VR by vol class | Available only as VR-implied Hurst; **NOT_INTERPRETABLE** (5.2d) |
| Autocorrelation by vol class | **AVAILABLE** — §5.2, no separation |
| Run length by vol class | **AVAILABLE** — §5.2, no separation |
| Directional efficiency by vol class | **AVAILABLE** — §5.2, no separation |
| Amplitude by vol class | **AVAILABLE** — §5.2, separates strongly |
| Shock statistics by vol class | **NOT_AVAILABLE** |
| R/S Hurst by vol class | **NOT_AVAILABLE** |

---

## 6. HURST DIAGNOSTICS

*Secondary diagnostic only. Used as evidence nowhere in this report.*

### 6.1 Estimators and H1 result

| Estimator | Definition | M1 | M3 | **H1** |
|---|---|---|---|---|
| VR-implied, all lags | H = (slope of log VR on log q + 1)/2 over q ∈ {2,4,8,16,32,64} | 0.4983 | 0.5065 | **0.4960** |
| VR-implied, short lags | fit on q ∈ {2,4,8} | 0.4920 | 0.4926 | **0.5270** |
| VR-implied, long lags | fit on q ∈ {16,32,64} | 0.5102 | 0.5244 | **0.5011** |
| R/S (classical) | slope of log(R/S) on log m | 0.5797 | 0.5802 | **0.5769** |
| \|all-lags VR-implied − R/S\| | divergence | **0.0814** | **0.0737** | **0.0809** |

**OBSERVATION 6.1a.** The two estimators disagree by **0.081 at H1** — the same order as at M1 (0.081) and M3 (0.074). The disagreement is not H1-specific; it is a property of this dataset at every resolution.

**OBSERVATION 6.1b.** H1's VR-implied Hurst is itself window-sensitive: **0.5270 on short lags vs 0.5011 on long lags**, a 0.026 shift, the largest short/long split of the three resolutions (M1: 0.018; M3: 0.032).

### 6.2 R/S block counts — the H1 weakness

| Block size m | M1 blocks | M3 blocks | **H1 blocks** | H1 mean R/S |
|---|---|---|---|---|
| 2 | 0 (below MIN_RS_WINDOW = 8) | 0 | **0** | NaN |
| 4 | 0 | 0 | **0** | NaN |
| 8 | 19,604 | 18,306 | **8,291** | 2.6067 |
| 16 | 18,876 | 16,605 | **2,175** | 4.0070 |
| 32 | 17,615 | 13,899 | **190** | 5.7721 |
| 64 | 17,076 | 12,728 | **31** | 8.7521 |
| **fitted H** | 0.5797 | 0.5802 | **0.5769** | |

**OBSERVATION 6.2a.** The H1 R/S slope is fitted on **four points**, of which the two longest rest on **190 and 31 blocks**. At M1 the same two points rest on 17,615 and 17,076. The H1 long-lag R/S is close to unmeasurable.

**OBSERVATION 6.2b (selection effect).** `hurst_rs` requires a **fully contiguous** block. At H1 only 95.70 % of steps are contiguous, so the probability that a 64-bar block qualifies is roughly 0.957^64 ≈ 0.06, and the 31 surviving blocks are drawn preferentially from the calmest uninterrupted stretches of the sample. **The H1 R/S estimate is computed on a non-random, calm-biased subsample.**

### 6.3 H1 VR-implied Hurst by year

| Year | all lags | short lags | long lags |
|---|---|---|---|
| 2010 | 0.4477 | 0.5260 | 0.3687 |
| 2011 | 0.5497 | 0.5338 | 0.8036 |
| 2012 | 0.4852 | 0.5454 | 0.4396 |
| 2013 | 0.5697 | 0.5609 | **NaN** |
| 2014 | 0.5811 | 0.5672 | NaN |
| 2015 | 0.5318 | 0.5478 | NaN |
| 2016 | 0.5149 | 0.4955 | NaN |
| 2017 | 0.5321 | 0.4785 | NaN |
| 2018 | 0.5978 | 0.5729 | NaN |
| 2019 | 0.5429 | 0.5404 | NaN |
| 2020 | 0.5471 | 0.5888 | NaN |
| 2021 | 0.5410 | 0.5524 | NaN |
| 2022 | 0.5639 | 0.5949 | NaN |
| 2023 | 0.5637 | 0.5737 | NaN |
| 2024 | 0.5647 | 0.5499 | NaN |
| 2025 | 0.5728 | 0.5462 | NaN |
| 2026 | 0.4913 | 0.4408 | NaN |
| **mean 2010–2025** | **0.5441** | | |
| **sd 2010–2025** | **0.0373** | | |
| **min / max** | **0.4477 / 0.5978** | | |

**OBSERVATION 6.3a.** The long-lag Hurst is **NaN in 13 of 17 years** — there are not enough 16/32/64-bar contiguous windows inside a single year of ~5,900 H1 bars. **The long-horizon half of the H1 Hurst curve cannot be evaluated year by year.**

**OBSERVATION 6.3b.** Where the long-lag value does exist (2010–2012) it swings from **0.3687 to 0.8036** — an interval that spans almost the entire admissible range and includes both strong anti-persistence and strong persistence. It carries no information.

**OBSERVATION 6.3c.** The all-lags series is much tighter: mean 0.5441, sd 0.0373, range 0.4477–0.5978. But it is a fit over six VR points two of which are unmeasured (§4.1c), and it is only one of the two estimators.

### 6.4 Status

```
HURST_STATUS = INCONCLUSIVE
```

The two estimators diverge by 0.081 at H1 (6.1a); the VR-implied estimator is window-sensitive by 0.026 at H1 (6.1b); the R/S estimator at H1 rests on 31 blocks at its longest lag and on a calm-biased subsample (6.2a, 6.2b); the long-lag estimator is unavailable in 13 of 17 years (6.3a). **No interpretation is forced. Hurst is not used as evidence for or against the H1 context role.**

---

## 7. CONTINUITY

### 7.1 M1 → M3 → H1

| Metric | M1 | M3 | **H1** |
|---|---|---|---|
| Bars | 5,874,003 | 1,963,826 | **98,412** |
| Bars with internal data gap (%) | **0.0000** | 0.1145 | **3.1602** |
| Bars with internal market break (%) | 0.0000 | 0.0000 | **0.0000** |
| Incomplete windows (%) | 0.0000 | 0.5248 | **0.4969** |
| Total missing minutes inside bars | 0 | 2,248 | **24,165** |
| Mean missing minutes per bar | 0.0000 | 0.0011 | **0.2455** |
| P99 missing minutes per bar | 0 | 0 | **4.0** |
| Max missing minutes in one bar | 0 | 1 | **51** |
| Non-contiguous steps (%) | **0.2673** | 0.6849 | **4.3013** |
| Mean M1 bars per bar | 1.0000 | 2.9911 | **59.6879** |
| Mean M1 bars per bar ÷ k | 100.00 % | 99.70 % | **99.48 %** |

**OBSERVATION 7.1a (the continuity cost is real and monotone).** Going from M1 to M3 to H1, the fraction of bars containing an internal data hole goes 0.00 % → 0.11 % → **3.16 %**, and the fraction of non-contiguous steps goes 0.27 % → 0.68 % → **4.30 %**. H1 pays roughly **6× the M3 step-discontinuity rate** and **16× the M1 rate**.

**OBSERVATION 7.1b (internal breaks are zero everywhere — a definition artefact).** `bars_with_internal_market_break` is 0.0000 % at **all three** resolutions. The Phase 2 definition counts closures of ≥ 50 minutes occurring **strictly inside** a bar. Daily and weekend closures fall at bar boundaries, so they are never "internal" at any resolution. **This zero must not be read as evidence of unbroken continuity.** Closures are recorded instead as non-contiguous steps, where H1 shows 4.30 %.

**OBSERVATION 7.1c (interruption lengths at H1).** Conditional on a bar having an internal gap: mean 7.77 min, median 2 min, P75 11, P90 27, P95 31, P99 38, max **51** minutes, skew +1.456, excess kurtosis +0.764. So the typical H1 hole is small (2 min) but the distribution has a long right tail: **a tenth of affected H1 bars are missing more than 27 minutes, i.e. nearly half the bar.**

**OBSERVATION 7.1d (window completeness).** 0.497 % of H1 windows are incomplete (fewer than 60 M1 bars and no internal gap) — these are edge windows at session starts. Mean M1 bars per H1 bar is 59.688 / 60 = **99.48 %** completeness (M3: 99.70 %).

### 7.2 H1 continuity by year

| Year | Bars | Internal-gap bars (%) | Incomplete (%) | Missing minutes | Non-contiguous steps (%) |
|---|---|---|---|---|---|
| 2010 | 6,210 | **17.3591** | 1.7713 | **8,023** | 4.2197 |
| 2011 | 6,141 | 5.5854 | 0.0489 | 6,530 | 3.1270 |
| 2012 | 6,017 | 4.2546 | 0.0665 | 6,503 | 2.6430 |
| 2013 | 5,669 | 5.9799 | 1.0937 | 897 | 5.2576 |
| 2014 | 5,654 | 3.1128 | 0.4599 | 374 | 4.9177 |
| 2015 | 5,766 | 0.6590 | 0.2601 | 65 | 4.4753 |
| 2016 | 5,891 | 0.3225 | 0.2716 | 33 | 4.3973 |
| 2017 | 5,885 | 0.2039 | 0.7307 | 15 | 4.3678 |
| 2018 | 5,906 | 1.8964 | 1.2530 | 231 | 4.3861 |
| 2019 | 5,887 | **7.0494** | 0.9512 | 894 | 4.5702 |
| 2020 | 5,927 | 0.9617 | 0.0675 | 92 | 4.3874 |
| 2021 | 5,905 | 0.4064 | 0.1016 | 34 | 4.3699 |
| 2022 | 5,915 | 0.6762 | 0.2198 | 57 | 4.3625 |
| 2023 | 5,890 | 2.3260 | 0.1868 | 223 | 4.3980 |
| 2024 | 5,938 | 0.5894 | 0.3368 | 58 | 4.4298 |
| 2025 | 5,913 | 0.3382 | 0.3044 | 115 | 4.3640 |
| 2026 | 3,898 | 0.2309 | 0.2052 | 21 | 4.3623 |

**OBSERVATION 7.2a.** The internal-gap rate is **extremely unstable**: 0.20 % (2017) to **17.36 %** (2010), mean 3.23 %, median 1.43 %, sd 4.40 (CV 136 %). Three years stand out: 2010 (17.36 %), 2019 (7.05 %) and 2013 (5.98 %).

**OBSERVATION 7.2b.** By contrast the **non-contiguous step rate is the single most stable metric in the entire H1 block**: mean 4.3013 %, sd 0.0061 pp, range 4.3625–5.2576 % excluding 2010–2012, CV **0.64 %**. From 2015 onward it sits in a 4.36–4.57 % band every single year.

**OBSERVATION 7.2c.** No gap was filled, no anomaly removed, no interruption repaired. All 24,165 missing minutes remain absent, as required by **L2**.

### 7.3 Pre/post 2013

| Metric | H1 pre-2013 (2010–2012) | H1 post-2013 (2013–2025) | Direction |
|---|---|---|---|
| Bars | 18,368 | 76,146 | — |
| Internal-gap bars (%) | **9.130** | **1.870** | 4.9× better |
| Missing minutes | 8,023 + 6,530 + 6,503 = 21,056 | 3,028 | — |
| Incomplete windows (%) | 0.6370 | 0.4780 | better |
| Mean M1 bars per bar | **58.7466** | **59.9006** | better |
| Step contiguity | **0.96652** | **0.95474** | **worse** |

**OBSERVATION 7.3a.** H1 before 2013 is a **materially different and poorer object**: 9.13 % of bars contain an internal data hole versus 1.87 % after, and each H1 bar averages 58.75 source minutes instead of 59.90. In 2010 the H1 OHLC is built from roughly **2.2 % fewer minutes** than in a modern year.

**OBSERVATION 7.3b.** Step contiguity moves the *other* way (0.9665 → 0.9547). This is not a contradiction: internal gaps (minutes missing inside a bar) and non-contiguous steps (whole bars missing) are different defects, and the two eras differ in their mix.

**OBSERVATION 7.3c.** The pre-2013 H1 sample is small — 18,368 bars, 18.7 % of the series — and its amplitude and volatility estimates are computed on partially populated bars. **Any pre-2013 H1 reading inherits that degradation.**

### 7.4 Readability gained versus continuity lost

| | M1 | M3 | H1 |
|---|---|---|---|
| Bars to examine | 5,874,003 | 1,963,826 | **98,412** |
| Median range (bps) | 2.258 | 4.256 | **20.891** |
| Excess kurtosis of returns | 88.59 | 46.29 | **23.17** |
| Internal-gap bars (%) | 0.000 | 0.114 | **3.160** |
| Non-contiguous steps (%) | 0.267 | 0.685 | **4.301** |

**INFERENCE 7.4a.** H1 buys a **20× reduction in bar count**, a **9.3× larger median range**, and a **3.8× reduction in return kurtosis** relative to M1. It pays **3.16 % of bars carrying an internal data hole** and **4.30 % of steps being discontinuous**. Whether that trade is favourable depends entirely on what the resolution is used for — a question this block is not permitted to answer with strategy language. The trade is quantified here, not judged.

---

## 8. AGGREGATION EFFECTS ON STRUCTURE

*Descriptive only. Aggregation is **not** presented as causally responsible for anything — only differences between the three stored series are reported, per mission §8.*

### 8.1 Amplitude scaling versus √k

| Quantity | M1 | M3 | H1 | H1/M1 | (H1/M1) ÷ √60 |
|---|---|---|---|---|---|
| Median range (bps) | 2.2584 | 4.2560 | 20.8906 | 9.2503 | **1.1942** |
| P90 range (bps) | 5.9285 | 10.6412 | 50.9000 | 8.5857 | **1.1084** |
| Median range (USD) | 0.3550 | 0.6710 | 3.2920 | 9.2732 | **1.1972** |
| Median range (%) | 0.0226 | 0.0426 | 0.2089 | 9.2503 | **1.1942** |

Three-step gradient of the median range against diffusive scaling:

| Step | Observed ratio | √k | Excess over √k |
|---|---|---|---|
| M1 → M3 | 1.8846 | 1.7321 | **×1.0881** |
| M3 → H1 | 4.9085 | 4.4721 | **×1.0976** |
| M1 → H1 | 9.2503 | 7.7460 | **×1.1942** |

**OBSERVATION 8.1a.** The bar range grows **faster than √k at every step, and the excess compounds**: +8.8 % at M1→M3, +9.8 % at M3→H1, +19.4 % at M1→H1. The P90 range shows the same direction with a smaller magnitude (+3.6 %, +7.0 %, +10.8 %).

### 8.2 Return dispersion scaling versus √k — the opposite direction

| Quantity | M1 | M3 | H1 | Ratio vs M1 | ÷ √k |
|---|---|---|---|---|---|
| Median trailing 1440-min σ (bps) | 2.2903 | 3.9008 | 15.8764 | M3/M1 1.7032 (÷√3 → **0.9833**) · H1/M1 6.9321 (÷√60 → **0.8949**) |
| Global return std (bps) | 2.7956 | 4.8023 | 21.0920 | M3/M1 1.7178 (÷√3 → **0.9918**) · H1/M1 7.5447 (÷√60 → **0.9740**) |

**OBSERVATION 8.2a (the central aggregation finding).** At H1 the two amplitude families move in **opposite** directions relative to diffusive scaling:

- **Range** (high − low) grows **1.194× faster** than √60 (8.1a)
- **Close-to-close return dispersion** grows at only **0.895×** √60 on the median trailing-σ measure (0.974× on the global-std measure)

The gap between them is intrabar excursion. Under a pure diffusion the two would scale identically.

**INFERENCE 8.2b.** The 0.895 shortfall is **directionally consistent with the VR < 1 reading at M1/M3** (§4.1a): negative short-lag dependence makes multi-period return variance grow more slowly than q × single-period variance, so σ over 60 minutes falls short of √60 × σ over 1 minute. The two observations support each other. This is an **inference**, not an observation: the chain from VR to the σ ratio is not measured directly in the file.

**OBSERVATION 8.2c.** The median-based ratio (0.8949) and the global-std-based ratio (0.9740) differ because the global std is dominated by a handful of extreme bars, and those are far more extreme at M1 (excess kurtosis 88.6) than at H1 (23.2). The median trailing-σ measure is the more robust of the two and is the one used in 8.2a.

### 8.3 What is preserved and what is lost, M1 → M3 → H1

| Property | M1 | M3 | H1 | Direction |
|---|---|---|---|---|
| Excess kurtosis of returns | 88.59 | 46.29 | **23.17** | **lost** (×0.26) |
| ACF lag 1 | −0.00939 | −0.01208 | **−0.00061** | **lost** (signal strongest at M3, gone at H1) |
| Body / range | 0.5215 | 0.4863 | **0.4407** | **lost** (monotone, −0.035 then −0.046) |
| Median range / σ(w1440) | 0.9648 | 1.0736 | **1.3475** | **gained** (monotone) |
| Mean run | 1.9098 | 1.9223 | 1.8515 | non-monotone (see 3.1c) |
| Sign-change frequency | 0.5117 | 0.5133 | 0.5189 | monotone increase |
| Step contiguity | 0.99733 | 0.99315 | **0.95699** | **lost** |
| Internal-gap bars | 0.000 | 0.00114 | **0.03160** | **lost** |
| Bar count | 5,874,003 | 1,963,826 | **98,412** | reduced 59.7× |

**OBSERVATION 8.3a.** Three properties degrade monotonically with aggregation — **tail heaviness, bar directionality (body/range) and continuity** — while **range relative to volatility** improves monotonically.

### 8.4 Directional efficiency is not comparable across resolutions

| DE | M1 | M3 | H1 |
|---|---|---|---|
| h = 5 bars | 0.4538 | 0.4442 | **0.4609** |
| h = 10 bars | 0.3151 | 0.3082 | **0.3357** |
| h = 20 bars | 0.2192 | 0.2161 | **0.2477** |

**OBSERVATION 8.4a.** H1's DE is the highest of the three at every horizon (+0.0071 / +0.0206 / +0.0285 versus M1).

**LIMITATION 8.4b (decisive).** DE as implemented measures \|net displacement\| divided by the **path traced on the bar grid of that resolution**. An H1 path is the sum of 10 hourly close-to-close moves; an M1 path over the same 10 hours is the sum of 600 one-minute moves. The H1 denominator is therefore much shorter for the identical wall-clock interval. **H1's higher DE is mechanically expected and is not evidence that H1 is more efficient, more trending, or better in any sense.** h = 10 bars also means 10 minutes at M1, 30 minutes at M3 and 10 hours at H1.

**CONSEQUENCE 8.4c.** DE is usable **within** H1 (across years, across eras, across volatility states) but **not across** resolutions in either direction. It is not used as cross-resolution evidence in this report.

### 8.5 Temporal structure: what aggregation does to the day

| UTC window | Share of H1 bars | Step contiguity | ACF(1) | Median range (bps) | Range/σ | Sign-change |
|---|---|---|---|---|---|---|
| 00–06 | 26.02 % | 0.83221 | **+0.01107** | 16.560 | 0.5526 | 0.5142 |
| 06–12 | 26.02 % | 0.83251 | **+0.01988** | 21.541 | 0.6984 | 0.5144 |
| 12–16 | 17.35 % | 0.74934 | **+0.02655** | 36.972 | 0.9406 | 0.5103 |
| 16–21 | 21.40 % | 0.79477 | **−0.03032** | 19.979 | 0.6031 | 0.5229 |
| 21–24 | 9.21 % | **0.36707** | **−0.21480** | 14.099 | **0.2597** | **0.6065** |

**OBSERVATION 8.5a (the H1 day is not homogeneous).** ACF(1) at H1 ranges from **+0.0266 (12–16 UTC)** to **−0.2148 (21–24 UTC)**. The global value of −0.00061 is an average across structurally unlike windows, **not a stable property of the H1 bar.**

**OBSERVATION 8.5b (the 21–24 UTC window is a different object).** It holds 9.21 % of H1 bars and differs on every axis measured: step contiguity **0.367** (versus 0.749–0.833 elsewhere), median range 14.10 bps (the smallest of the five), range/σ **0.260** (versus 0.553–0.941), sign-change frequency **0.607** (versus 0.510–0.523), mean run **1.050** (versus 1.484–1.634). This window contains the daily rollover.

**INFERENCE 8.5c.** The 21–24 UTC H1 bars are largely **stub bars** bracketing a closure: short, quiet relative to σ, alternating, and barely contiguous with their neighbours. Roughly one H1 bar in eleven falls in this window. Any H1 context reading computed on the full H1 series is a mixture of four ordinary windows and this one.

**OBSERVATION 8.5d.** Session-window DE is `NaN` in all five windows. This is **structural, not a failure**: `de(h=10)` requires 10 fully contiguous consecutive bars, which is impossible inside a 6-hour or 3-hour window. Reported as `NOT_APPLICABLE`.

---

## 9. ANNUAL STABILITY (2010 → 2025, 2026 separate)

### 9.1 Descriptive stability table — 16 full years

| Metric | Mean | Median | SD | Min | Max | CV = sd/\|mean\| | Verdict |
|---|---|---|---|---|---|---|---|
| Step contiguity | 0.95708 | 0.95613 | 0.00611 | 0.94742 | 0.97357 | **0.006** | **STABLE** |
| M1 bars per H1 bar | 59.68345 | 59.92642 | 0.47223 | 58.65411 | 59.98747 | **0.008** | **STABLE** |
| Mean run | 1.85060 | 1.85478 | 0.03548 | 1.77941 | 1.90909 | **0.019** | **STABLE** |
| Body / range | 0.44041 | 0.44208 | 0.00959 | 0.42549 | 0.45738 | **0.022** | **STABLE** |
| Sign-change frequency | 0.51930 | 0.52007 | 0.01206 | 0.50046 | 0.54531 | **0.023** | **STABLE** |
| DE h=5 | 0.46165 | 0.46304 | 0.01168 | 0.43607 | 0.47523 | **0.025** | **STABLE** |
| DE h=10 | 0.33699 | 0.33683 | 0.01076 | 0.31741 | 0.35667 | **0.032** | **STABLE** |
| DE h=20 | 0.25138 | 0.25133 | 0.01013 | 0.23589 | 0.27244 | **0.040** | **STABLE** |
| Range / σ (w1440, median) | 1.34316 | 1.33549 | 0.05435 | 1.27689 | 1.47086 | **0.041** | **STABLE** |
| Hurst VR-implied (all lags) | 0.54412 | 0.54841 | 0.03732 | 0.44774 | 0.59784 | 0.069 | **CONDITIONAL** (see 6.3, 6.4) |
| σ 1440 (bps) | 15.80499 | 15.66325 | 2.74495 | 11.06954 | 19.63205 | **0.174** | **CONDITIONAL** |
| Median range (bps) | 20.71099 | 19.95220 | 3.88298 | 15.34146 | 27.09150 | **0.188** | **CONDITIONAL** |
| P90 range (bps) | 47.84189 | 45.91051 | 10.45462 | 30.82943 | 65.47606 | **0.219** | **CONDITIONAL** |
| Excess kurtosis | 12.27459 | 10.76935 | 5.35706 | 5.63290 | 21.19247 | **0.436** | **INSTABLE** |
| ACF lag 2 | 0.00171 | 0.00612 | 0.02031 | −0.03821 | 0.05157 | 11.883 | **INSTABLE** |
| ACF lag 1 | 0.00104 | 0.00282 | 0.01834 | −0.02624 | 0.03850 | 17.568 | **INSTABLE** |
| Incomplete windows (%) | 0.50773 | 0.28801 | 0.50870 | 0.04885 | 1.77134 | 1.002 | **INSTABLE** |
| Internal-gap bars (%) | 3.23257 | 1.42904 | 4.39836 | 0.20391 | 17.35910 | 1.361 | **INSTABLE** |

### 9.2 Reading

**OBSERVATION 9.2a.** The metrics that are stable to within a few percent across 16 years are precisely the **structural / shape** family: contiguity (CV 0.6 %), window completeness (0.8 %), run length (1.9 %), body/range (2.2 %), sign-change (2.3 %), directional efficiency (2.5–4.0 %), and range/σ (4.1 %).

**OBSERVATION 9.2b.** The **correlation** family is not stable: ACF(1) has 9/16 years positive with a range of 0.065, which is ~106× the global estimate. ACF(2) is the same.

**OBSERVATION 9.2c.** The **continuity-defect** family is not stable either, but for a documented reason: it improves by an order of magnitude after 2012 (§7.2a). This is a structural break in data quality, not sampling noise.

**OBSERVATION 9.2d.** Amplitude metrics (median range, P90 range, σ) have CVs of 17–22 %. That is normal year-to-year volatility variation, not instability of the measurement: range/**σ** — the amplitude metric with volatility divided out — is stable at CV 4.1 %.

### 9.3 Structural change identification

| Metric | Classification | Basis |
|---|---|---|
| Step contiguity, M1/bar, mean run, body/range, sign-change, DE h5/h10/h20, range/σ | **STABLE** | CV ≤ 4.1 %, uniform across 2010–2025 |
| Median range, P90 range, σ1440 | **CONDITIONAL** | CV 17–22 %, but the volatility-normalised form (range/σ) is stable — amplitude varies because *volatility* varies, not because the measurement does |
| Hurst VR-implied all-lags | **CONDITIONAL** | Tight year to year (CV 6.9 %) but the estimator is one of two that disagree by 0.081, and its long-lag half is unavailable in 13/17 years |
| ACF lag 1, ACF lag 2 | **INSTABLE** | Sign split 9/16; range ~106× the global value |
| Excess kurtosis | **INSTABLE** | CV 44 %, range 5.63–21.19 |
| Internal-gap bars, incomplete windows | **INSTABLE** | CV 100–136 %, driven by the 2010–2012 data-quality break |

### 9.4 Session-window stability — `NOT_APPLICABLE` for DE

As noted in 8.5d, DE cannot be computed inside a UTC window. All other session metrics are reported in §8.5.

---

## 10. 2013 COMPARISON

### 10.1 Pre-2013 (2010–2012) versus post-2013 (2013–2025), all three resolutions

| Metric | M1 pre → post | M3 pre → post | **H1 pre → post** |
|---|---|---|---|
| ACF lag 1 | **+0.01771 → −0.01830** | **+0.01496 → −0.02055** | **+0.00172 → +0.00213** |
| ACF lag 2 | +0.01707 → −0.01180 | −0.00172 → −0.00389 | **−0.01292 → +0.00459** |
| Excess kurtosis | 15.92 → **100.30** | 17.01 → **46.31** | 12.49 → **16.96** |
| Median range (bps) | 2.447 → 2.129 | 4.819 → 3.996 | 22.328 → 19.903 |
| Mean run | 1.9135 → 1.9072 | 1.9201 → 1.9219 | 1.8261 → 1.8556 |
| Sign-change freq | 0.5145 → 0.5110 | 0.5132 → 0.5133 | 0.5336 → 0.5160 |
| DE h=10 | 0.3177 → 0.3148 | 0.3093 → 0.3079 | **0.3199 → 0.3409** |
| Step contiguity | 0.99087 → 0.99876 | 0.97742 → 0.99669 | **0.96652 → 0.95474** |
| Internal-gap bars (%) | 0.000 → 0.000 | 0.4453 → 0.0408 | **9.130 → 1.870** |

### 10.2 The 2013 break does not register at H1 on ACF(1)

**OBSERVATION 10.2a.** The ACF(1) sign flip documented in Phase 2 at fine resolution is **reproduced here at M1** (+0.01771 → −0.01830, swing 0.0360) **and at M3** (+0.01496 → −0.02055, swing 0.0355). At **H1 both eras are indistinguishable from zero**: +0.00172 and +0.00213, a swing of 0.0004 — **1.2 % of the M1 swing and 1.1 % of the M3 swing.**

**INFERENCE 10.2b — two readings, both reported.**

- *Favourable to the context role:* on this metric H1 is **stable across the 2013 break** where M1 and M3 are not. A context layer that does not move when the microstructure convention changes is doing what a context layer is supposed to do.
- *Unfavourable to the context role:* H1 is **blind** to a structural change that is unambiguous at finer resolution. If part of the purpose of a context resolution is to indicate which environment one is in, H1 fails to register the one break this project has already documented (**L4**).

Both readings follow from the same observation. This block does not choose between them.

**OBSERVATION 10.2c.** The kurtosis explosion also attenuates sharply with aggregation: M1 ×6.3 (15.9 → 100.3), M3 ×2.7 (17.0 → 46.3), **H1 ×1.36 (12.5 → 17.0)**. H1 is largely insulated from the tail-structure change.

**OBSERVATION 10.2d.** H1's DE(h=10) **rises** across the break (0.3199 → 0.3409) while M1's (0.3177 → 0.3148) and M3's (0.3093 → 0.3079) are flat to slightly down. Since DE within H1 compares like with like (same resolution, same grid), this is a genuine within-H1 change: **post-2013 hourly price paths are modestly more directional relative to their own hourly grid.**

**OBSERVATION 10.2e.** Continuity moves in **opposite** directions at H1: internal-gap bars fall 4.9× (9.130 % → 1.870 %) while step contiguity *worsens* slightly (0.96652 → 0.95474). Compare M3, where both improve (0.97742 → 0.99669 contiguity, 0.4453 % → 0.0408 % gaps). **H1 does not inherit the post-2013 continuity improvement that M1 and M3 show.**

**OBSERVATION 10.2f.** H1's post-2013 sample is 76,146 bars (77.4 %); the pre-2013 sample is 18,368 bars (18.7 %) and is degraded (§7.3). All pre/post-2013 H1 comparisons carry that asymmetry.

---

## 11. 2026 SANITY CHECK (PARTIAL YEAR)

**Status: `PARTIAL_YEAR_SANITY_CHECK`. Per limitation L5, 2026 drives no selection decision anywhere in this block.**

| Metric | Median of 16 full years (2010–2025) | 2026 (3,898 bars) | Ratio |
|---|---|---|---|
| Median range (bps) | 19.952 | **40.299** | **2.020** |
| P90 range (bps) | 45.911 | **91.411** | 1.991 |
| σ 1440 (bps) | 15.663 | **28.228** | 1.802 |
| Median range (USD) | 3.16 | **18.360** | 5.81 |
| **Range / σ (w1440, median)** | 1.335 | **1.408** | **1.055** |
| **DE h=10** | 0.3368 | **0.3324** | **0.987** |
| **Step contiguity** | 0.9561 | **0.9564** | **1.000** |
| **M1 bars per H1 bar** | 59.926 | **59.968** | **1.000** |
| Internal-gap bars (%) | 1.429 | **0.231** | 0.162 |
| ACF lag 1 | +0.0028 | **−0.01755** | sign flip |
| ACF lag 2 | +0.0061 | **−0.03684** | sign flip |
| Excess kurtosis | 10.769 | **21.137** | 1.963 |
| VR-implied Hurst (all lags) | 0.548 | **0.4913** | 0.897 |

**OBSERVATION 11a.** 2026 is a **high-volatility year at H1**: median range 2.02× the 2010–2025 median, σ 1.80×, kurtosis 1.96×.

**OBSERVATION 11b.** Its **internal structure is normal**: range/σ 1.055×, DE(h=10) 0.987×, step contiguity 1.000×, and the best window completeness of the entire series (59.968 M1 bars per H1 bar, internal-gap rate 0.231 %). The volatility rise is not accompanied by a structural change in how H1 bars behave.

**OBSERVATION 11c.** ACF(1) at −0.01755 is the **second most negative of the 17 years** (2025 is the most negative at −0.02624), and ACF(2) at −0.03684 is likewise second most negative (2011 at −0.03821 is the most negative). Although 2026 holds only 3.9 % of the H1 bars, its strongly negative ACF pulls the global estimate below zero even though both the pre-2013 and post-2013 blocks are positive — one contributor to the non-additivity discussed below.

**OBSERVATION 11d (non-additivity caveat).** Weighting the three stored blocks by their own ACF window counts gives `(17,234 × 0.001719 + 69,335 × 0.002127 + 3,556 × (−0.017553)) / 90,125 = +0.00127`, versus the stored global value of −0.000611 — a discrepancy of 0.0019. The ACF estimator demeans and normalises **within** each block, so it is not exactly additive across subsamples. At M1 and M3 this non-additivity is negligible relative to the values themselves; at H1 it is the same order as the quantity being measured. **All three H1 ACF(1) values (global −0.0006, pre +0.0017, post +0.0021) should be read as "indistinguishable from zero", not as three distinct findings.**

---

## 12. EVIDENCE STRENGTH

Graded on: sample size, estimator agreement, cross-resolution corroboration, and annual stability. "Intervals" are descriptive year-level intervals over 16 full years, not bar-level significance tests (§2.5).

### 12.1 Resolved — usable as evidence

| # | Finding | Evidence | Grade |
|---|---|---|---|
| E1 | H1 structural/shape metrics are stable across 16 years | contiguity CV 0.6 %, completeness 0.8 %, run 1.9 %, body/range 2.2 %, sign-change 2.3 %, DE 2.5–4.0 %, range/σ 4.1 % | **STRONG** |
| E2 | H1 continuity costs are material and monotone in bar size | internal-gap bars 0.00 % → 0.11 % → 3.16 %; non-contiguous steps 0.27 % → 0.68 % → 4.30 %; 24,165 missing minutes; max hole 51 min | **STRONG** |
| E3 | H1 range grows faster than √k while return dispersion grows slower | range ×1.194 vs √60; median trailing σ ×0.895 vs √60; both monotone across the three steps | **STRONG** (within-file; the VR link in 8.2b is an inference) |
| E4 | H1 volatility states separate amplitude, not dynamics | median range 26.31 vs 17.89 bps; ACF1 −0.0059 vs −0.0053; DE h10 0.3248 vs 0.3326; run 1.788 vs 1.818 | **MODERATE–STRONG** |
| E5 | H1 shock behaviour differs qualitatively from M1/M3 | clustering 1.37× vs 5.00× / 4.52× the independent benchmark; direction persistence 0.5002 vs 0.4536 / 0.4527 | **MODERATE** (horizon-confounded, §3.3e) |
| E6 | H1 is heterogeneous across the UTC day | ACF(1) +0.0266 (12–16) to −0.2148 (21–24); 21–24 contiguity 0.367, range/σ 0.260, 9.21 % of bars | **MODERATE–STRONG** |
| E7 | H1 does not reproduce the 2013 ACF(1) sign flip | H1 swing 0.0004 vs M1 0.0360 and M3 0.0355 | **STRONG** (the observation; both readings in 10.2b are inferences) |
| E8 | 2026 is a high-volatility year with normal internal structure | range 2.02×, σ 1.80×, but range/σ 1.055×, DE 0.987×, contiguity 1.000× | **SANITY ONLY** (partial year, L5) |

### 12.2 Unresolved — reported, not used as evidence

| # | Finding | Why unresolved |
|---|---|---|
| U1 | **Direction of H1 persistence** | VR > 1 at all six lags versus ACF(1) = −0.0006. The identity VR(2) = 1 + ρ(1) fails by **0.0354** at H1, versus 0.0003 at M3 and 0.0029 at M1 (§3.2a) |
| U2 | **H1 VR curve above lag 8** | q = 32 rests on 190 windows, q = 64 on **31** (§4.1c) |
| U3 | **Hurst at H1** | Two estimators disagree by 0.081; R/S fitted on 4 points with 190 and 31 blocks at the long end and drawn from a calm-biased contiguous subsample; per-year long-lag Hurst NaN in 13/17 years (§6.2, §6.3) |
| U4 | **Volatility-conditioned Hurst at H1** | HIGH 0.5324 / LOW 0.3545, but the long-lag sub-fit returns 0.2946 and **0.1079**; only one estimator available in that split (§5.2d) |
| U5 | **H1 ACF(1) annual behaviour** | 9/16 years positive, range 0.065, and the estimate is not additive across subsamples at its own precision (§11d) |
| U6 | **Cross-resolution DE** | Path is measured on each resolution's own bar grid; H1's higher DE is mechanically expected (§8.4b) |
| U7 | **Cross-resolution run length** | Broken by non-adjacency at H1 (4.30 %) and by zero returns at M1; the two artefacts are not separable in this file (§3.1c) |
| U8 | **Cross-resolution shock rate** | σ window is 1440 / 480 / 24 bars across M1 / M3 / H1; estimator noise differs (§12.3) |

### 12.3 Additional measurement artefacts declared

| Field | Issue |
|---|---|
| `shocks.clustering_ratio` | ≈ 1.000 at all three resolutions (0.99975 / 0.99972 / 1.00005). This is `mean_gap × per-bar_rate`, which equals 1 **by construction** for any renewal process. **Uninformative.** This report uses the corrected baseline `1 − (1 − p)⁵` instead (§3.3, E5) |
| `bars_with_internal_market_break` | 0.0000 % at **all three** resolutions. The Phase 2 definition requires a ≥ 50-minute closure strictly *inside* a bar; closures land on boundaries. **A definition artefact, not evidence of continuity** (§7.1b) |
| `hurst_rs.mX` at m = 2 and m = 4 | Always NaN (below `MIN_RS_WINDOW = 8`), at every resolution |
| Session-window DE | Structurally undefined — DE(h=10) needs 10 contiguous bars, impossible inside a 3–6 hour window (§8.5d) |

---

## 13. CONTEXT-TIMEFRAME ASSESSMENT

### 13.1 The question

> *Are the H1 characteristics sufficiently stable and informative for H1 to be used as a context resolution, without claiming that H1 itself provides a trading signal?*

### 13.2 What supports the role

1. **Structural stability is the best in the file.** Contiguity, window completeness, run length, body/range, sign-change frequency, directional efficiency and range/σ all hold to within 0.6–4.1 % CV across 16 years (E1). These are the descriptors a context layer would actually read.
2. **H1 carries a volatility-normalised amplitude signal that M1 and M3 do not.** Median range/σ rises monotonically 0.965 → 1.074 → **1.348** (§8.3a). H1 expresses the scale of the market more distinctly than the finer resolutions.
3. **H1 is the only resolution whose VR curve lies entirely above 1** (§4.1a). If VR is believed, H1 is the scale at which the short-horizon reversal visible at M1/M3 gives way to mild persistence — which is exactly the kind of statement a context resolution exists to make.
4. **H1 is stable across the documented 2013 break on ACF(1) and ACF(2)** (E7), where M1 and M3 both flip sign. It does not move when the session convention changes. (DE is *not* stable across the break — it rises 0.3199 → 0.3409, §10.2d — so this point rests on the correlation metrics only.)
5. **Volatility conditioning behaves sensibly**: H1 separates amplitude (1.47× on median range, 1.77× on σ) while leaving directional character untouched (E4). A context layer wants the former without the latter.
6. **Cost of use is low**: 98,412 bars versus 1.96M (M3) and 5.87M (M1).

### 13.3 What limits the role

1. **The persistence claim — the strongest argument for H1 as context — is not established.** VR says positive, ACF says zero, and they disagree by 0.035 where the same check passes at 0.0003 at M3 (U1). The upper half of the VR curve rests on 190 and 31 windows (U2).
2. **H1's ACF is unstable and heterogeneous** — 9/16 years positive, and +0.027 to −0.215 across the UTC day (U5, E6). The near-zero global value is a mixture, not a property.
3. **Continuity costs are material**: 3.16 % of H1 bars carry an internal data hole, 4.30 % of steps are discontinuous, and 24,165 minutes are missing inside H1 bars — 6× the M3 step-discontinuity rate (E2).
4. **The pre-2013 H1 sample is a different and poorer object**: 9.13 % of bars with an internal gap, 58.75 source minutes per bar (§7.3). Any H1 context reading over the full history inherits that.
5. **H1 does not improve with the 2013 continuity break** the way M1 and M3 do: its step contiguity goes 0.9665 → 0.9547 while M3's goes 0.9774 → 0.9967 (§10.2e).
6. **Hurst is inconclusive and weakest at H1** (U3), and the volatility-conditioned Hurst split is not interpretable (U4).
7. **H1 is blind to the 2013 break** on ACF(1) — the favourable and unfavourable readings of E7 both stand.

### 13.4 Verdict

H1 is **confirmed** as a context resolution on the strength of evidence that is independent of the VR problem: its structural descriptors are the most stable in this file, it carries a volatility-normalised amplitude signal the finer resolutions do not express, and it is stable across the documented 2013 convention break.

H1 is **not** confirmed on the persistence pillar. The one result that would most directly justify "context = the scale where behaviour changes" — VR above 1 at every lag — is contradicted by H1's own autocorrelation at a magnitude twelve times larger than the same check at M3, and its upper lags rest on 31 observations. The continuity cost is also material and, unlike M3, does not improve after 2013.

```
BLOCK_B_VERDICT = H1 CONTEXT CONFIRMED WITH LIMITATIONS
```

**Scope of the verdict.** This confirms H1 as a resolution for **describing and conditioning on market state**. It does not establish, and must not be read as establishing, that H1 possesses directional persistence, that H1 is tradable, or that any signal exists at H1. No return, expectancy, Sharpe, hit rate or profit factor enters this report.

### 13.5 Effect on the official decision

```
PRIMARY   = M3     UNCHANGED
SECONDARY = M1     UNCHANGED
CONTEXT   = H1     UNCHANGED
```

Block B is an audit of confirmation/revision. It does not re-select, and it does not modify the Phase 2 decision. The two limitations above (§13.3.1 and §13.3.3) should be carried forward into any later phase that consumes H1 as context.

---

## 14. LIMITATIONS

### 14.1 Source limitations

1. **Single source, single run.** Everything derives from one execution of `deep_audit.py`. No metric was recomputed, so no internal replication of the numbers was possible.
2. **Declared gaps** (§2.4): per-year VR(q) curves, per-year and per-vol-class R/S Hurst, P25 of amplitude, an H1-vs-M3 and H1-vs-M1 paired discrimination table, and shock recovery magnitude/delay are all absent from the file. None was reconstructed, none was imported from Phase 2, none was recomputed.
3. **The VR(2)/ACF(1) contradiction at H1 (§3.2a) is unresolved by design.** Identifying its cause would require recomputation on the price series, which is forbidden.

### 14.2 Methodological limitations

4. **Cross-resolution comparisons are confounded by construction.** Hurst lags, shock σ windows and DE horizons are all expressed in **bars**, so "the same" quantity means 64 minutes at M1, 192 minutes at M3 and 64 hours at H1. Several apparent resolution effects (shock clustering, DE, run length) cannot be separated from horizon effects in this file.
5. **Descriptive uncertainty only.** Year-level intervals measure whether an ordering is stable across years. They are not significance tests; no p-value, no bar-level standard error, no multiple-comparison correction.
6. **The volatility classification is local, not absolute** (§5.1): HIGH_VOL means "above its own trailing 1-year mean σ", so both classes exist in every era and the σ separation is only 1.77×.
7. **Session windows are time windows, not participant classes.** No attribution to any category of market participant is made or implied.
8. **Continuity metrics are definition-bound.** "Internal market break" requires a ≥ 50-minute closure strictly inside a bar and is therefore 0 everywhere (§7.1b). Weekend and daily closures appear only as non-contiguous steps.

### 14.3 Standing prohibitions honoured

| Prohibition | Status |
|---|---|
| Volume column used | **NO** (`spec.volume_used = false`) |
| Regime constructed or labelled | **NO** (`spec.regime_built = false`) |
| Strategy, entry, exit, position | **NO** |
| Backtest | **NO** (`spec.strategy_tested = false`) |
| Return / Sharpe / drawdown / expectancy / hit rate / profit factor | **NO** |
| Optimisation | **NO** |
| Timeframe selection based on trading results | **NO** — the official decision is untouched |
| Gaps filled | **NO** (`spec.gaps_filled = false`) |
| Extremes removed or winsorised | **NO** (`spec.extremes_removed = false`) |
| Shocks removed from the sample | **NO** (`shocks.never_removed = true`) |
| Source fragments modified / repaired / deleted | **NO** |
| Broker costs asserted | **NO** (`broker_cost_status = EXTERNAL_INPUT_REQUIRED`) |
| Microstructure claimed as observed | **NO** — OHLC only; all such statements are labelled INFERENCE or PROXY |
| 2026 used as a selection driver | **NO** (L5, §11) |
| Conclusion of profitability | **NO** |

### 14.4 Observation versus inference

Every numbered statement in this report is prefixed `OBSERVATION` (a value present in `deep_metrics.json`, or a ratio/aggregate of such values) or `INFERENCE` (an interpretation that goes beyond the stored numbers). Ratios, means, medians, standard deviations and sign counts formed from stored values are labelled OBSERVATION because they are arithmetic on stored quantities, but they are not independent measurements.

No claim is made about an order book, bid/ask, real liquidity, institutional flow, or any mechanism not visible in OHLC bar data.

---

## 15. PROVISIONAL CONCLUSION

**BLOCK_B_VERDICT = H1 CONTEXT CONFIRMED WITH LIMITATIONS**

H1 earns the context role on **stability**, not on **persistence**.

The stability case is solid and independent of every contested result: across 16 full years, H1's contiguity, window completeness, run length, body/range, sign-change frequency, directional efficiency and range/σ all hold within a few percent (E1); H1 carries a volatility-normalised amplitude signal (range/σ = 1.348) that M1 and M3 do not express (§8.3a); and H1 does not move across the documented 2013 convention break on ACF(1) or ACF(2) (E7).

The persistence case does not hold. H1's VR curve lies above 1 at all six lags — the one qualitative difference from M1 and M3 — but H1's own ACF(1) of −0.0006 contradicts it by 0.035, where the identical check passes at 0.0003 at M3 (§3.2a), and the curve's upper half rests on 190 and 31 windows (§4.1c). Hurst is inconclusive and weaker at H1 than at either finer resolution (§6.4).

The price paid is continuity: 3.16 % of H1 bars contain an internal data hole, 4.30 % of steps are discontinuous, 24,165 minutes are missing inside H1 bars (§7.1a), and unlike M3, H1's continuity does **not** improve after 2013 (§10.2e).

**H1 is therefore confirmed as a resolution for describing and conditioning on market state — with the persistence rationale explicitly withdrawn and the continuity cost carried forward.** It is not confirmed as a source of directional signal, and nothing in this block speaks to tradability.

**Official decision unchanged:** `PRIMARY = M3`, `SECONDARY = M1`, `CONTEXT = H1`.

### Carried forward

| Item | Status |
|---|---|
| `HURST_STATUS` | **INCONCLUSIVE** (estimator divergence 0.081; 31 R/S blocks at m=64 at H1) |
| H1 persistence direction | **UNRESOLVED** (VR > 1 vs ACF ≈ 0, gap 0.0354) |
| H1 volatility-conditioned Hurst | **NOT_INTERPRETABLE** (long-lag sub-fit 0.295 / 0.108) |
| H1 pre-2013 sample | **DEGRADED** (9.13 % internal-gap bars, 58.75 source minutes per bar) |
| H1 21–24 UTC window | **STRUCTURALLY DISTINCT** (contiguity 0.367, ACF1 −0.215, 9.21 % of bars) |
| `shocks.clustering_ratio` | **UNINFORMATIVE** — use `1 − (1 − p)⁵` baseline instead |
| `bars_with_internal_market_break` | **DEFINITION ARTEFACT** — 0 at all resolutions |

---

```
END OF BLOCK B
STOP — no transition to Block C.
```
