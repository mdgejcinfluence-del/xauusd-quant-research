# PHASE 2B — BLOCK A: M1 vs M3 DEEP AUDIT

**Status:** BLOCK A of Phase 2B (complementary validation)
**Scope of this block:** amplitude, noise proxies, persistence, directional
efficiency and temporal stability — **M1 and M3 only**
**Source of truth:** `/tmp/xauusd_audit/deep_metrics.json` (produced by
`research/timeframe_audit/scripts/deep_audit.py`)
**Heavy recomputation:** NONE. `deep_audit.py` was not re-run. Every number
below is read from the existing raw metric file.
**Effect on the official decision:** NONE. This is an audit, not a new
selection. `PRIMARY=M3 / SECONDARY=M1 / CONTEXT=H1` is left untouched.

**Generated (UTC):** 2026-09-06T10:22Z
**Branch:** `arena/01a075b8-xauusd-quant-research` · HEAD `c0d236f`

---

## 1. Objective

To test, not to presuppose, whether the Phase 2 designation of **M3 as the
primary conventional representation** is supported when M1 and M3 are examined
in isolation and in depth, on six dimensions:

1. amplitude (absolute, relative, volatility-normalised)
2. statistically observable noise
3. directional efficiency
4. persistence (runs, continuation, alternation, ultra-short reversal)
5. temporal stability (annual, pre/post-2013, partial year)
6. the M1→M3 difference itself, with its uncertainty and its stability

Explicitly excluded: any strategy, strategy return, expectancy, Sharpe, profit
factor, backtest, regime model, regime label, optimisation, and any use of the
volume column.

---

## 2. Raw-data source

| item | value |
|---|---|
| File | `/tmp/xauusd_audit/deep_metrics.json` (657,646 bytes) |
| Producer | `research/timeframe_audit/scripts/deep_audit.py` (one run, 107 s, no error) |
| M1 master feeding it | `fdce55a8c8a76c417765ad020794866bb36e5b166c130d2bb4deb2aeeeab91d0` (unchanged from Phase 1) |
| Bars | M1 5,874,003 · M3 1,963,826 · H1 98,412 |
| Span | 2010-01-01 → 2026-08-30 UTC (16.663 years; 2026 partial) |

Ex-ante parameters fixed inside the engine and used here:

| parameter | value |
|---|---|
| Volatility windows | 60 / 240 / 1440 wall-clock minutes (same horizon at both resolutions) |
| Autocorrelation lags | 1–5, contiguous steps only |
| Shock rule | \|log return\| > 3 × trailing σ over the previous 1440 min, past data only |
| Volatility classes | HIGH_VOL if trailing 1440-min σ > trailing 1-year mean of that σ (past-only) |
| UTC windows | 00–06, 06–12, 12–16, 16–21, 21–24 — time windows only, no actor attribution |
| Uncertainty method | **paired-by-year difference, n = 16 full years** (M3 minus M1 within each year) |

**Two gaps in the raw file, declared before use:**

* **P25 is absent.** The engine's quantile grid was fixed at
  P50 / P75 / P90 / P95 / P99. P25 was not emitted, and per the instruction not
  to recompute, it is not supplied here. All other requested quantiles are
  present.
* **Ultra-short reversal is present only as a frequency.** The sign-change
  frequency between consecutive bar returns *is* the ultra-short reversal
  frequency. The recovery magnitude and recovery delay (measured in Phase 2)
  are **not** in this file and are not imported, since the source of truth for
  this block is `deep_metrics.json` alone.

---

## 3. M1 amplitude

**OBSERVATION.** All values are as-delivered USD of gold price (L3). Range =
High − Low. Body = |Close − Open|.

| statistic | range (USD) | body (USD) |
|---|---|---|
| mean | 0.5918 | 0.3232 |
| std | 0.9050 | 0.6130 |
| **P50** | **0.3550** | **0.1630** |
| P75 | 0.6530 | 0.3600 |
| P90 | 1.2200 | 0.7200 |
| P95 | 1.8400 | 1.1100 |
| P99 | 4.0200 | 2.6100 |

Relative to price — median range **2.2584 bps = 0.022584 %**; median body
**0.010044 %**. Full range distribution: mean 3.0135 bps, P75 3.7412,
P90 5.9285, P95 7.8811, P99 14.0219 bps.

Shape: mean body/range **0.5215** (median 0.5289); mean upper wick/range
0.2373; mean lower wick/range 0.2411; mean (upper+lower wick)/body **4.6708**.
Median upper wick 0.0570 USD, median lower wick 0.0600 USD.

The range distribution is extremely right-skewed: skew 11.09, excess kurtosis
403.2, and mean/median = 1.667. The mean is not a representative statistic
here; the median is used throughout this block.

**Volatility-normalised amplitude** (range ÷ trailing σ, dimensionless):

| window | P50 | P75 | P90 | P95 | P99 | mean |
|---|---|---|---|---|---|---|
| 60 min | 1.1786 | 1.6858 | 2.3178 | 2.8130 | 4.1385 | 1.3391 |
| 240 min | 1.0885 | 1.6442 | 2.3564 | 2.9266 | 4.4959 | 1.2930 |
| 1440 min | 0.9648 | 1.4992 | 2.2123 | 2.8069 | 4.5371 | 1.1828 |

The normalised median declines as the reference window lengthens (1.179 →
0.965): against a one-day volatility reference, the typical M1 bar spans
slightly less than one daily standard deviation.

---

## 4. M3 amplitude

**OBSERVATION.**

| statistic | range (USD) | body (USD) |
|---|---|---|
| mean | 1.0885 | 0.5653 |
| std | 1.5872 | 1.0538 |
| **P50** | **0.6710** | **0.2900** |
| P75 | 1.1940 | 0.6270 |
| P90 | 2.2000 | 1.2500 |
| P95 | 3.3000 | 1.9290 |
| P99 | 7.1230 | 4.4938 |

Median range **4.2560 bps = 0.042560 %**; median body 0.018127 %. Full range:
mean 5.5898 bps, P75 6.8316, P90 10.6412, P95 14.0863, P99 24.9637 bps.

Shape: mean body/range **0.4863** (median 0.4887); upper wick/range 0.2525;
lower wick/range 0.2611; wick/body **5.5569**. Median upper wick 0.1200 USD,
median lower wick 0.1270 USD.

**Volatility-normalised amplitude:**

| window | P50 | P75 | P90 | P95 | P99 | mean |
|---|---|---|---|---|---|---|
| 60 min | 1.3850 | 1.9186 | 2.5626 | 3.0484 | 4.2137 | 1.5450 |
| 240 min | 1.2390 | 1.8078 | 2.5248 | 3.0885 | 4.6093 | 1.4421 |
| 1440 min | 1.0736 | 1.6109 | 2.3260 | 2.9292 | 4.7150 | 1.2955 |

**Direct scaling check (OBSERVATION).** M3 / M1 median range = 0.6710 / 0.3550
= **1.890**, against √3 = 1.732 for pure diffusion. Return dispersion scales at
4.8023 / 2.7956 = **1.718**, essentially exactly √3. So bar *dispersion* follows
the diffusion law, while the bar *range* grows about 9 % faster than √k — the
extra range is excursion, which is what the body/range decline also shows.

**After normalising by recent volatility, M3 is not merely a rescaled M1: the
median M3 bar spans 11.2 % more of the trailing 1440-minute σ than the median
M1 bar (1.0736 vs 0.9648).** This is not an arithmetic artefact of aggregation;
both series are divided by a volatility measured over the same wall-clock
horizon. It holds in **all sixteen full years** (§13).

---

## 5. M1 noise proxies

**OBSERVATION** — these are properties of OHLC bar series, not of an order book.

| proxy | M1 value |
|---|---|
| ACF lag 1 | −0.00939 |
| ACF lag 2 | −0.00618 |
| ACF lag 3 | −0.00370 |
| ACF lag 4 | +0.00065 |
| ACF lag 5 | −0.00086 |
| sign-change (ultra-short reversal) frequency | 0.51169 |
| mean run length | 1.9098 bars (1.91 min) |
| median / P90 / max run | 1 / 4 / 24 |
| return std | 2.7956 bps |
| return skew | −0.5604 |
| return excess kurtosis | 88.586 |

The sign-change frequency sits 0.0117 above the 0.5000 independent benchmark:
consecutive M1 returns reverse direction slightly more often than a coin flip.
That, and the uniformly negative short-lag ACF, are the same weak negative
dependence seen from two angles. Every autocorrelation is inside ±0.010, and
the largest is under a fifth of the conventional white-noise band at this
sample size (1/√5,846,068 ≈ 0.00041 — i.e. the point estimates are
statistically distinguishable from zero but economically negligible).

**INFERENCE / PROXY.** The negative short-lag autocorrelation is *consistent
with* bid/ask bounce, quote flicker, or genuine intraday mean reversion. OHLC
data cannot separate these. No claim about the order book, spreads, liquidity
or institutional flow is made or implied.

**3σ shocks (OBSERVATION).** 90,323 events, 5,420.6 per year, 1.538 % of bars.
Median magnitude 8.995 bps; median z-score 3.724. Probability of another shock
within 5 bars: **0.3730**, against 0.0746 expected under independence —
**5.00 × clustering**. Mean inter-shock gap 65.0 bars, median 11.

---

## 6. M3 noise proxies

**OBSERVATION.**

| proxy | M3 value |
|---|---|
| ACF lag 1 | −0.01208 |
| ACF lag 2 | −0.00468 |
| ACF lag 3 | −0.00495 |
| ACF lag 4 | +0.00034 |
| ACF lag 5 | −0.00003 |
| sign-change (ultra-short reversal) frequency | 0.51326 |
| mean run length | 1.9223 bars (5.77 min) |
| median / P90 / max run | 1 / 4 / 20 |
| return std | 4.8023 bps |
| return skew | −0.4005 |
| return excess kurtosis | 46.291 |

**3σ shocks.** 30,771 events, 1,846.7 per year, 1.567 % of bars. Median
magnitude 15.411 bps; median z 3.758. Shock-within-5 probability **0.3429**
against 0.0760 expected — **4.51 × clustering**. Mean gap 63.8 bars, median 13.

**The headline noise comparison (OBSERVATION).** M3 return excess kurtosis is
46.3 against M1's 88.6 — a 48 % reduction that looks, on its face, like the
strongest possible argument for M3. It does not survive scrutiny:

1. The paired-by-year difference is −45.8 with a year-level standard deviation
   of **94.8**; the 95 % interval is **[−92.2, +0.63] and includes zero**.
   Per-year M1 kurtosis ranges from 9.9 (2010) to **430.4** (2021) and M3 from
   10.5 to 129.1. The point estimate is enormous and the year-to-year noise is
   larger still.
2. Phase 2 established — and this block does not contradict — that excluding
   the ≤0.47 % of bars beyond 5σ collapses M1 kurtosis from 88.6 to 4.75 and M3
   from 46.3 to 4.68. The whole gradient is carried by a few hundred bars.

**INFERENCE / PROXY.** Aggregation does not remove extreme events from the
sample; it spreads their impact across a wider window and therefore lowers
their weight in a per-bar fourth moment. Reading the kurtosis drop as "M3 is a
cleaner signal" would be an inference not supported by the evidence.

---

## 7. M1 persistence

**OBSERVATION.**

| diagnostic | M1 |
|---|---|
| variance ratio q2 / q4 / q8 | 0.9877 / 0.9782 / 0.9659 |
| variance ratio q16 / q32 / q64 | 0.9583 / 0.9568 / 0.9857 |
| Hurst, VR-implied (all lags) | 0.4983 |
| Hurst, VR-implied (short lags 2-4-8) | 0.4920 |
| Hurst, VR-implied (long lags 16-32-64) | 0.5102 |
| Hurst, R/S fitted | 0.5797 |
| direction persistence 5 bars after a 3σ shock | 0.4536 |
| mean reversion 5 bars after a shock | +0.2348 bps |
| mean reversion 20 bars after a shock | +0.1719 bps |

The variance ratio falls to a minimum of 0.9568 at q32 (32 minutes) and turns
back up at q64. Runs average 1.91 bars with a maximum of 24.

**HURST_STATUS = INCONCLUSIVE.** The two estimators disagree by **0.081**
(VR-implied 0.498 against R/S 0.580) on the same series, and the VR-implied
value itself moves from 0.492 on short lags to 0.510 on long lags. Rescaled
range is known to be biased upward at these sample sizes, and the disagreement
is of the same size at M3 (0.074). Hurst is therefore reported as a secondary
diagnostic only and is **not** used as evidence of trending or mean reversion
anywhere in this block.

---

## 8. M3 persistence

**OBSERVATION.**

| diagnostic | M3 |
|---|---|
| variance ratio q2 / q4 / q8 | 0.9876 / 0.9749 / 0.9677 |
| variance ratio q16 / q32 / q64 | 0.9739 / 0.9882 / 1.0421 |
| Hurst, VR-implied (all lags) | 0.5065 |
| Hurst, VR-implied (short lags) | 0.4926 |
| Hurst, VR-implied (long lags) | 0.5244 |
| Hurst, R/S fitted | 0.5802 |
| direction persistence 5 bars after a 3σ shock | 0.4527 |
| mean reversion 5 bars after a shock | +0.2113 bps |
| mean reversion 20 bars after a shock | +0.1464 bps |

Runs average 1.92 bars with a maximum of 20.

**The persistence comparison is a null result.** Direction persistence after a
shock is 0.4536 at M1 and 0.4527 at M3 — a difference of **0.0009**, i.e. the
two resolutions are indistinguishable on whether a shock is followed by
continuation or reversal. Both sit below 0.5, and mean post-shock displacement
is positive in the reversion direction at both resolutions (+0.23 and +0.21 bps
at 5 bars). Shock clustering is strong at both (5.00 × and 4.51 × the
independent benchmark).

Note on the variance ratios: M3 crosses 1.0 at q64 = **192 minutes**, while M1
never crosses within q ≤ 64 (= 64 minutes) and instead bottoms out and turns up.
Because the lag set is expressed *in bars*, the wall-clock horizons differ
threefold, so these two VR curves are **not** directly comparable across
resolutions. They are reported per resolution, not contrasted.

---

## 9. Directional efficiency

**OBSERVATION.**

| horizon | M1 | M3 | M3 − M1 |
|---|---|---|---|
| h = 5 bars | 0.4538 | 0.4442 | −0.0096 |
| h = 10 bars | 0.3151 | 0.3082 | −0.0069 |
| h = 20 bars | 0.2192 | 0.2161 | −0.0031 |

The paired-by-year difference at h = 10 is **−0.007191**, 95 % interval
[−0.00937, −0.00501], sign consistency 0.875 (14 of 16 years), effect/noise
1.614 — **statistically stable and negative**.

**This result must not be read as "M3 is less efficient", and the raw file does
not permit the stronger reading either way.** The horizon is 10 bars, which is
**10 minutes at M1 and 30 minutes at M3**. Phase 2 established, on the same
dataset, that directional efficiency measured at a *fixed* minute horizon falls
monotonically as the horizon lengthens (0.315 at 10 min → 0.044 at 600 min),
and that the apparent efficiency of coarse bars is inflated several-fold by
path coarsening alone. `deep_metrics.json` contains only the bar-horizon
variant, so the observed −0.0069 cannot be decomposed into a resolution effect
and a horizon effect.

**Verdict on this section: the difference is real, stable, small, and
CONFOUNDED.** It is not usable as evidence for or against M3.

---

## 10. Annual stability

**OBSERVATION.** 2026 is excluded from every stability statistic below; it is
treated separately in §12.

**Median range (bps) — M1 vs M3, by year:**

| year | M1 | M3 | year | M1 | M3 |
|---|---|---|---|---|---|
| 2010 | 2.783 | 5.518 | 2018 | 1.633 | 3.094 |
| 2011 | 2.408 | 4.788 | 2019 | 1.594 | 3.052 |
| 2012 | 2.140 | 3.935 | 2020 | 2.915 | 5.460 |
| 2013 | 2.452 | 4.720 | 2021 | 2.174 | 4.052 |
| 2014 | 1.815 | 3.597 | 2022 | 2.426 | 4.494 |
| 2015 | 1.945 | 3.816 | 2023 | 1.909 | 3.582 |
| 2016 | 2.319 | 4.348 | 2024 | 2.287 | 4.234 |
| 2017 | 1.660 | 3.134 | 2025 | 3.090 | 5.617 |

M3 exceeds M1 in **16 of 16 years**, without exception. The M1 median range
spans 1.59–3.09 bps across the sixteen years (a factor 1.94); the M3 median
spans 3.05–5.62 (a factor 1.84). The *year* moves amplitude by more than two
granularity steps do, yet the M3 > M1 ordering is never inverted.

**ACF lag 1, by year:**

| year | M1 | M3 | year | M1 | M3 |
|---|---|---|---|---|---|
| 2010 | −0.02009 | +0.03067 | 2018 | −0.03066 | −0.02414 |
| 2011 | +0.04198 | +0.01554 | 2019 | −0.02868 | −0.00873 |
| 2012 | +0.01868 | −0.00624 | 2020 | −0.03961 | −0.04460 |
| 2013 | −0.00668 | +0.00338 | 2021 | −0.02047 | −0.01197 |
| 2014 | −0.01175 | −0.02240 | 2022 | −0.01813 | −0.02290 |
| 2015 | −0.02405 | −0.02748 | 2023 | −0.00026 | −0.00018 |
| 2016 | −0.00397 | −0.02989 | 2024 | −0.01464 | −0.02541 |
| 2017 | −0.02625 | −0.02387 | 2025 | −0.01227 | −0.01734 |

Both resolutions swing across a range of roughly ±0.045 from year to year and
both change sign repeatedly. The M1 value is positive in 2011–2012 and negative
in most later years; the M3 value is positive in 2010–2011 and 2013 and
negative afterwards. **The year-to-year movement of ACF lag 1 (about ±0.045) is
four to five times larger than the entire M1-vs-M3 gap (−0.0012).** This is the
central fact of §14.

**Sign-change frequency, by year (M1 / M3):** range 0.4991–0.5343 (M1) and
0.5072–0.5199 (M3). Stable at both.

**Volatility-normalised median range, w1440 (M1 / M3):** M1 spans
0.816–1.122 and M3 spans 0.946–1.276 across the sixteen years. M3 exceeds M1 in
**16 of 16 years**.

**Directional efficiency h = 10, by year:** M1 spans 0.3069–0.3282; M3 spans
0.3008–0.3135. M3 is below M1 in 14 of 16 years.

---

## 11. Pre/post-2013 comparison

**OBSERVATION.** The 2013 session-convention break (L4) is treated as two
separate samples, never smoothed.

| metric | M1 pre | M1 post | M3 pre | M3 post |
|---|---|---|---|---|
| bars | 1,079,057 | 4,561,191 | 364,480 | 1,521,420 |
| ACF lag 1 | **+0.01771** | **−0.01830** | **+0.01496** | **−0.02055** |
| sign-change freq | 0.51447 | 0.51095 | 0.51318 | 0.51327 |
| mean run | 1.91354 | 1.90717 | 1.92009 | 1.92192 |
| excess kurtosis | 15.92 | 100.30 | 17.01 | 46.31 |
| median range (bps) | 2.447 | 2.129 | 4.819 | 3.996 |
| median range (USD) | 0.353 | 0.336 | 0.685 | 0.630 |
| DE h=10 | 0.3177 | 0.3148 | 0.3093 | 0.3079 |
| body/range | 0.5240 | 0.5226 | 0.4806 | 0.4886 |
| contiguous steps | 0.99087 | 0.99876 | 0.97742 | 0.99669 |
| % bars with internal gap | 0.000 | 0.000 | **0.4453** | 0.0408 |

**The 2013 sign flip replicates at both resolutions.** ACF lag 1 is positive
before 2013 and negative after at M1 (+0.0177 → −0.0183) *and* at M3
(+0.0150 → −0.0206). Aggregating to M3 does **not** remove the discontinuity —
it reproduces it almost identically. Any pooled autocorrelation statistic at
either resolution therefore mixes two eras with opposite signs.

Two further observations:

* **Excess kurtosis triples at M1 after 2013 (15.9 → 100.3) and rises 2.7× at
  M3 (17.0 → 46.3).** The post-2013 era is more extreme-tailed at both
  resolutions, despite being calmer by median range.
* **M3 continuity improves sharply after 2013:** 0.4453 % of M3 bars contained
  an internal data gap before 2013, against 0.0408 % after, and contiguity rose
  from 0.9774 to 0.9967. The pre-2013 M3 series is materially more fragmented
  than the post-2013 one — a fact invisible at M1, where the gap rate is 0 in
  both eras because gaps appear as absent bars rather than as damaged bars.

---

## 12. 2026 partial-year sanity check

**PARTIAL_YEAR_SANITY_CHECK** — 2026 covers January to August only (8 months).
It is displayed for integrity and drives no conclusion (L5).

| metric | M1 2026 | M1 full | M3 2026 | M3 full |
|---|---|---|---|---|
| bars | 233,755 | 5,874,003 | 77,926 | 1,963,826 |
| ACF lag 1 | −0.00399 | −0.00939 | −0.01113 | −0.01208 |
| sign-change freq | 0.51278 | 0.51169 | 0.51342 | 0.51326 |
| mean run | 1.94288 | 1.9098 | 1.94062 | 1.9223 |
| excess kurtosis | 52.38 | 88.59 | 30.57 | 46.29 |
| median range (bps) | **4.618** | 2.258 | **8.386** | 4.256 |
| median range (USD) | 2.100 | 0.355 | 3.810 | 0.671 |
| DE h=10 | 0.3102 | 0.3151 | 0.3092 | 0.3082 |
| body/range | 0.4888 | 0.5215 | 0.4683 | 0.4863 |
| contiguous steps | 0.99922 | 0.99733 | 0.99772 | 0.99315 |

2026 is a high-amplitude year at both resolutions — median range roughly
**double** the full-sample figure (4.618 vs 2.258 bps at M1; 8.386 vs 4.256 at
M3), consistent with gold reaching the sample maximum of 5,596.81 recorded in
Phase 1. The M3 > M1 amplitude ordering is preserved, as is the negative sign
of ACF lag 1 at both resolutions. Continuity is at or above the full-sample
level. Nothing in 2026 contradicts the full-sample conclusions.

---

## 13. Direct M1 vs M3 comparison

Paired by year, n = 16 full years, difference = M3 − M1. The interval is a
descriptive year-level interval: it measures whether the *ordering* is stable
across years, not a parametric test on bars.

| metric | M1 | M3 | diff | 95 % interval | sign consistency | effect / year-noise | stable? |
|---|---|---|---|---|---|---|---|
| median range (bps) | 2.258 | 4.256 | **+1.9932** | [+1.796, +2.190] | **16/16** | 4.96 | **YES** |
| P90 range (bps) | 5.929 | 10.641 | **+4.4210** | [+3.931, +4.911] | **16/16** | 4.42 | **YES** |
| median range (USD) | 0.355 | 0.671 | **+0.3384** | [+0.258, +0.419] | **16/16** | 2.05 | **YES** |
| range/σ (w1440) median | 0.965 | 1.074 | **+0.1110** | [+0.095, +0.127] | **16/16** | 3.43 | **YES** |
| body / range | 0.5215 | 0.4863 | **−0.0359** | [−0.041, −0.031] | **16/16** | 3.37 | **YES** (favours M1) |
| DE h=10 | 0.3151 | 0.3082 | −0.0072 | [−0.0094, −0.0050] | 14/16 | 1.61 | stable but **CONFOUNDED** |
| contiguous step rate | 0.99733 | 0.99315 | **−0.0042** | [−0.0066, −0.0018] | **16/16** | 0.87 | **YES** (favours M1) |
| % bars with internal gap | 0.0000 | 0.0011 | +0.0012 | [+0.0002, +0.0022] | **16/16** | 0.57 | **YES** (favours M1) |
| sign-change freq | 0.51169 | 0.51326 | +0.0016 | [−0.0014, +0.0047] | 13/16 | 0.26 | **NO** |
| excess kurtosis | 88.59 | 46.29 | −45.81 | **[−92.24, +0.63]** | 12/16 | 0.48 | **NO** |
| ACF lag 1 | −0.00939 | −0.01208 | −0.0012 | [−0.0105, +0.0082] | 9/16 | 0.06 | **NO** |
| ACF lag 2 | −0.00618 | −0.00468 | +0.0023 | [−0.0056, +0.0102] | 11/16 | 0.14 | **NO** |
| ACF lag 3 | −0.00370 | −0.00495 | +0.0001 | [−0.0055, +0.0056] | 10/16 | 0.01 | **NO** |
| ACF lag 4 | +0.00065 | +0.00034 | +0.0002 | [−0.0052, +0.0056] | 8/16 | 0.02 | **NO** |
| ACF lag 5 | −0.00086 | −0.00003 | −0.0015 | [−0.0047, +0.0016] | 8/16 | 0.24 | **NO** |

**Reading of the table.**

*Four metrics are unambiguously resolved, all in M3's favour, all with 16/16
year consistency and effect/noise ratios between 2.0 and 5.0: the median range,
the P90 range, the median range in USD, and the volatility-normalised range.*
These are the only robust differences this block finds.

*Three metrics are unambiguously resolved in M1's favour:* body/range,
contiguous step rate and internal-gap rate. The first is an arithmetic
consequence of aggregating three bars into one (more excursion per bar) and is
not a quality defect. The other two are real but small — 0.42 pp fewer
contiguous steps and 0.11 % of M3 bars silently containing a missing-data gap,
concentrated in the pre-2013 era (§11).

*Eight metrics are unresolved.* Every autocorrelation lag and the
sign-change frequency have intervals spanning zero and sign consistency between
0.50 and 0.81. Excess kurtosis has the largest point estimate of the whole
table (−45.8) and the widest interval, which **includes zero**.

---

## 14. Evidence strength

| claim about M3 relative to M1 | verdict | basis |
|---|---|---|
| Larger absolute movement | **ROBUST** | +0.338 USD median range, 16/16 years, effect/noise 2.05 |
| Larger movement at every quantile | **ROBUST** | P90 +4.42 bps, 16/16 years, effect/noise 4.42 |
| Larger movement *relative to recent volatility* | **ROBUST** | +0.111 in range/σ units, 16/16 years, effect/noise 3.43 |
| Amplitude advantage survives calm and volatile regimes | **ROBUST** | M3 > M1 in both volatility classes and in both eras (§10–11) |
| Lower excess kurtosis | **NOT STABLE** | diff −45.8 but 95 % interval [−92.2, +0.63] includes zero; year-level sd 94.8 |
| Lower kurtosis = genuinely less noise | **NOT SUPPORTED** | Phase 2: the whole gradient is carried by ≤0.47 % of bars |
| Lower sign alternation | **NOT SUPPORTED** | M3 is *higher* (0.51326 vs 0.51169), interval includes zero |
| Different autocorrelation structure | **NOT SUPPORTED** | all lags 1–5 have intervals spanning zero |
| Faster or slower ultra-short reversal | **NOT SUPPORTED** | reversal frequencies differ by 0.0016 with an interval spanning zero |
| Better persistence after shocks | **NOT SUPPORTED** | 0.4527 vs 0.4536 — a difference of 0.0009 |
| Different shock clustering | **NOT SUPPORTED** | 4.51 × vs 5.00 × the independent benchmark; both strong |
| Better directional efficiency | **NOT SUPPORTED (favouring M1)** | M3 is −0.0072 lower, but the horizon differs (30 min vs 10 min) → **CONFOUNDED** |
| Worse continuity | **ROBUST but SMALL** | −0.42 pp contiguous steps, +0.11 pp bars hiding a gap |
| Smaller body / range | **ROBUST but ARITHMETIC** | −0.0359; a necessary consequence of enclosing more time |
| Different Hurst exponent | **INCONCLUSIVE** | the two estimators disagree by ~0.08 at both resolutions |

**Summary of evidence strength.** Of the fifteen comparisons, **four are robust
and favour M3, all of them amplitude.** None of the noise, reversal or
persistence comparisons is resolved. The two structural/continuity
comparisons are robust and favour M1, but one is arithmetic and the other is
small.

---

## 15. Interpretation limits

1. **No order book exists in this dataset.** Everything above is computed from
   OHLC bars. The negative short-lag autocorrelation is consistent with
   bid/ask bounce, but it is equally consistent with genuine intraday mean
   reversion, and the two cannot be separated here. Nothing in this block
   supports any statement about spreads, depth, liquidity, order flow or
   institutional participation.
2. **P25 is missing** from the raw file (§2). Quantiles reported are
   P50/P75/P90/P95/P99.
3. **Ultra-short reversal recovery is missing.** Only the reversal *frequency*
   is present; recovery magnitude and delay are in Phase 2's output, not in
   this block's source of truth, and were not imported.
4. **Directional efficiency is horizon-confounded.** The h = 10 comparison
   spans 10 minutes at M1 and 30 minutes at M3. The confound cannot be removed
   with the data in this file.
5. **Variance ratios are expressed in bars, not minutes**, so the M1 and M3 VR
   curves cover different wall-clock horizons and are not directly comparable.
6. **Hurst is estimator-dependent** and reported as INCONCLUSIVE
   (VR-implied ≈ 0.50 vs R/S ≈ 0.58 at both resolutions).
7. **The uncertainty intervals are year-level (n = 16)**, not bar-level. They
   answer "is the ordering stable across years?", which is the relevant
   question for selecting a working resolution, but they are not a test of
   statistical significance on individual bars, and they are not a test of any
   trading proposition.
8. **Excess kurtosis is a small-sample-dominated statistic** at both
   resolutions; its year-level standard deviation exceeds its cross-resolution
   difference.
9. **Volume was never loaded** (L1). No volume-weighted or volume-confirmed
   statement is made anywhere.
10. **No gap was filled, no outlier removed, no data modified** (L2, L6, L7).
11. **2026 is partial** and excluded from every stability statistic (L5).
12. **This block covers M1 and M3 only.** H1 is out of scope here.

**OBSERVATION vs INFERENCE.** Sections 3–13 are observations about bar series.
Statements such as "aggregation does not remove extreme events, it spreads
their impact" and "the extra range at M3 is excursion" are labelled
**INFERENCE / PROXY**: they are the most parsimonious readings of the observed
moments, not measurements of a mechanism.

---

## 16. Provisional conclusion

```
BLOCK_A_VERDICT = M3 PREFERRED WITH LIMITATIONS
```

**Why not "M3 CLEARLY PREFERRED".** A clear preference would require M3 to win
on more than one dimension. It wins on exactly one — amplitude — and that
advantage is large, stable and confirmed in 16/16 years, in both volatility
classes, and in both eras. On every noise proxy examined (five autocorrelation
lags, sign-change frequency, excess kurtosis, shock persistence, shock
clustering) the two resolutions are statistically indistinguishable. The
apparent M3 noise advantage in excess kurtosis is the largest point estimate in
the table and the least stable, with a 95 % interval that includes zero and a
year-level spread twice the size of the effect.

**Why not "M1/M3 CLOSE PLATEAU".** They are not equivalent on amplitude. The
volatility-normalised median range is 11.2 % higher at M3, in all sixteen
years, with an effect-to-noise ratio of 3.4 and an interval that excludes zero
by a wide margin. A plateau claim would require that difference to be within
noise, and it is not.

**Why not "M1 PREFERRED" or "UNRESOLVED".** M1 is better on continuity
(0.42 pp) and on body/range (0.036), but the first is small and concentrated
in the pre-2013 era and the second is an arithmetic consequence of enclosing
more time per bar. Against those, M3's amplitude advantage is an order of
magnitude larger in relative terms and holds in every single year.

**What the limitation consists of.** The Phase 2 rationale for M3 contained an
implicit claim that aggregation *reduces noise*. This block does not support
that claim: the noise proxies are indistinguishable, and the one statistic that
appeared to show noise reduction is unstable and driven by a fraction of a
percent of bars. What *is* supported is narrower and cleaner: **M3 carries
larger movements, both absolutely and relative to contemporaneous volatility,
for a continuity cost of 0.42 percentage points and no detectable loss of
signal quality.**

**Effect on the official decision: none.** `PRIMARY=M3 / SECONDARY=M1 /
CONTEXT=H1` stands. This block refines the *reason* it stands — amplitude and
cost headroom, not noise reduction — and it reinforces the Phase 2 statement
that confidence in the M1–M5 zone is high while confidence in M3 *specifically*
is only moderate. The M3-versus-M1 margin rests on one dimension; if a future
phase does not need amplitude headroom, that dimension carries no weight and
M1 should be preferred on continuity grounds.

---

## Final gate

```
[x] deep_metrics.json used as the sole source of truth
[x] no heavy recomputation; deep_audit.py not re-run
[x] no backtest
[x] no strategy
[x] no regime model or label
[x] no volume
[x] no dataset modification
[x] observation / inference separated (§15)
[x] annual results present (§10)
[x] 2013 treated as a structural split (§11)
[x] 2026 separated as PARTIAL_YEAR_SANITY_CHECK (§12)
[x] decision not forced (§16 — one of the five permitted formulations used)
[x] official M3/M1/H1 decision untouched
```

Missing from the raw source, declared not supplied: **P25** (§2),
**ultra-short reversal recovery magnitude and delay** (§2).

---

**STOP.** Block A complete. Block B not started.
