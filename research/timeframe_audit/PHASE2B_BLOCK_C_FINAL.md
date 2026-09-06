# PHASE 2B — BLOCK C
## EXTREMES / SHOCKS / AMPLITUDE-COST / INFORMATION PRESERVATION
### FINAL ANALYTICAL BLOCK OF PHASE 2B

**Status:** PRE-REGIME · PRE-STRATEGY · LAST BLOCK
**Objects:** extremes, volatility shocks, distribution tails, information preservation under aggregation, amplitude relative to **hypothetical** cost, historical stability.
**Official decision audited, not re-selected:** `PRIMARY = M3` / `SECONDARY = M1` / `CONTEXT = H1`.

---

## 1. OBJECTIVE

Determine whether the M3 / M1 / H1 conclusions established in Phase 2 and tested in Block A and Block B survive a final audit centred on six axes:

1. extremes
2. volatility shocks
3. distribution tails
4. information preservation under aggregation
5. amplitude relative to cost (**hypothetical scenarios only**)
6. historical stability

Then audit the official decision and state whether it is confirmed, confirmed with limitations, revised, or unresolved — **without forcing confirmation**.

No strategy. No backtest. No return. No regime. No label. No volume. No real broker cost.

---

## 2. DATA / SOURCE

### 2.1 Primary source (read-only)

| Item | Value |
|---|---|
| File | `/tmp/xauusd_audit/deep_metrics.json` |
| Size | 657,646 B |
| SHA-256 | `c3774bfcef7a3895d0b8766c2d013b0349814d9cf413b1ac10bb59e31be20c52` |
| mtime | 2026-09-06 10:12:09 UTC — **unchanged since the single production run** |
| Produced by | `research/timeframe_audit/scripts/deep_audit.py`, one execution, 107 s, exit 0 |
| Re-run in this block | **NO** |
| M1 master | `/tmp/xauusd_audit/XAUUSD_M1_reconstructed.parquet`, SHA-256 `fdce55a8c8a76c417765ad020794866bb36e5b166c130d2bb4deb2aeeeab91d0` — matches Phase 1 and the grid manifest |
| Dataset reconstructed | **NO** |
| Sources modified | **NO** |

### 2.2 Secondary sources (Phase 2 committed artifacts, reused — nothing recomputed)

`deep_metrics.json` **contains no amplitude/cost block**. The `spec` declares `COST_SCENARIOS` and `COST_DOMINATION_PCT`, but no per-timeframe cost metric was written to the file (verified: the strings `cost`/`COST` occur 8 times in the file, all inside `spec`). The cost analysis required by §5 therefore comes from the **already-committed Phase 2 artifacts**, which are themselves outputs of the same M1 master and the same 12-timeframe grid:

| File | Rows | Used for |
|---|---|---|
| `research/timeframe_audit/XAUUSD_AMPLITUDE_COST_ANALYSIS.csv` | 480 | §10 Cost/range matrix, §11 sensitivity |
| `research/timeframe_audit/XAUUSD_TIMEFRAME_COMPARISON.csv` | 12 | §4 tails, P25/P95/P99 range, breakout/extreme rates |
| `research/timeframe_audit/XAUUSD_SIGNAL_NOISE_ANALYSIS.csv` | 12 | §4 tail fractions, return quantiles, recovery |
| `research/timeframe_audit/XAUUSD_INFORMATION_LOSS.csv` | 12 | §8, §9 information preservation |

**Cross-source consistency check.** The grids are identical. `XAUUSD_AMPLITUDE_COST_ANALYSIS.csv` reports M1 median range = 0.355 USD / 2.2584 bps and M3 median range = 0.671 USD / 4.256 bps; `deep_metrics.json` reports M1 `amplitude_usd.range.p50` = 0.355000 and `amplitude_bps.range.p50` = 2.258358, M3 = 0.671000 / 4.256038. Exact match. H1 likewise (3.292 USD / 20.8906 bps in both).

### 2.3 Operations performed in this block

Read-only JSON key lookups and read-only CSV reads, plus **descriptive aggregation of already-stored values** (counts, medians, means, ratios, coefficients of variation across years). No metric was recomputed from the price series.

### 2.4 Standing limitations (Phase 1, still binding)

**L1** volume never loaded · **L2** no gap filling · **L3** no price-decimal homogenisation · **L4** the ~2013 session-convention break stays documented · **L5** 2026 is partial, sanity check only · **L6** extremes retained · **L7** sources never modified.

---

## 3. SHOCK DEFINITION

Fixed ex ante in the Phase 2B engine, identical across all three resolutions, unchanged here.

| Parameter | Value |
|---|---|
| Shock criterion | \|log return of one bar\| > 3 × trailing rolling σ of the **same** series |
| σ window | previous **1440 wall-clock minutes**, past-only, implemented as `round(1440/k)` bars |
| σ window in bars | **M1: 1440 · M3: 480 · H1: 24** |
| k | 3.0 |
| Extremes removed | **NEVER** (`never_removed = true`) |

**OBSERVATION 3.1.** The shock rule is *self-normalising*: σ is estimated from the same series at the same resolution, so a "3σ shock" is a resolution-relative event, not an absolute price move. The **σ window length in bars differs by a factor of 60 across resolutions** (1440 → 24). This is the single largest caveat on all cross-resolution shock comparison: the M1 estimator averages 1440 observations, the H1 estimator only 24.

**INFERENCE 3.2.** A σ̂ built from 24 observations is far noisier than one built from 1440. Under fat tails, a noisier σ̂ produces more threshold crossings. This is a plausible contributor to the higher H1 shock rate (§7.1) and is **not separable from a genuine resolution effect** with the data in this file.

---

## 4. EXTREME DISTRIBUTION

### 4.1 Tails, three resolutions

| Statistic | M1 | M3 | H1 | Source |
|---|---|---|---|---|
| Return std (bps) | 2.79562 | 4.80230 | 21.09200 | deep_metrics |
| Return Q01 (bps) | −7.80639 | −13.53134 | −62.18071 | Phase 2 CSV |
| Return Q99 (bps) | +7.76291 | +13.33465 | +59.01975 | Phase 2 CSV |
| **Tail fraction \|z\| > 2σ** | **0.044873** | **0.044672** | **0.047113** | Phase 2 CSV |
| **Tail fraction \|z\| > 3σ** | **0.016447** | **0.016696** | **0.017807** | Phase 2 CSV |
| **Excess kurtosis** | **88.59** | **46.29** | **23.17** | deep_metrics |
| Skew | −0.56036 | −0.40053 | −0.56235 | deep_metrics |
| Annualised vol (%) | 16.5987 | 16.4866 | 16.2096 | Phase 2 CSV |
| P50 range (USD) | 0.355 | 0.671 | 3.292 | deep_metrics |
| **P25 range (USD)** | **0.200** | **0.399** | **2.047** | Phase 2 CSV |
| P75 range (USD) | 0.653 | 1.194 | 5.760 | deep_metrics |
| P90 range (USD) | 1.220 | 2.200 | 10.557 | deep_metrics |
| P95 range (USD) | 1.840 | 3.300 | 15.720 | deep_metrics |
| P99 range (USD) | 4.020 | 7.123 | 32.6589 | deep_metrics |

*(P25 is absent from `deep_metrics.json` — the engine's quantile grid is fixed at P50/P75/P90/P95/P99. It is taken from the Phase 2 CSV and is reported, not reconstructed.)*

### 4.2 The central tail finding: frequency is preserved, heaviness is not

**OBSERVATION 4.2a.** The **2σ tail fraction is essentially invariant across resolutions**: 0.044873 (M1), 0.044672 (M3), 0.047113 (H1) — a spread of 5.5 % relative. The **3σ tail fraction** is likewise near-invariant and slightly *rising*: 0.016447 → 0.016696 → 0.017807.

**OBSERVATION 4.2b.** Over the same three resolutions, **excess kurtosis falls by a factor of 3.82** (88.59 → 46.29 → 23.17).

**INFERENCE 4.2c.** These two facts are not in conflict, and together they locate the aggregation effect precisely. Aggregation does **not** change how often a bar exceeds 2σ or 3σ; it changes **how extreme the extremes get**. The fourth moment is dominated by the outermost handful of observations, and those are exactly what averaging 60 one-minute bars into one hourly bar destroys. The bulk of the tail survives; the tip does not.

**OBSERVATION 4.2d.** Return quantiles scale almost exactly with √k. Q99: 7.76291 → 13.33465 → 59.01975; the H1/M1 ratio is 7.6033 against √60 = 7.7460, i.e. **0.982 × √k**. This is the *close-to-close* measure, and it agrees with the sub-√k scaling of the median trailing σ found in Block B §8.2 (0.895 × √60) only in direction, not in magnitude — the global quantile is inflated at M1 by the same extreme bars that inflate kurtosis.

### 4.3 Tail shape (P99 relative to P50) — resolution-invariant, era-dependent

| Era | M1 P99/P50 | M3 P99/P50 | H1 P99/P50 |
|---|---|---|---|
| pre-2013 | 5.830 | 5.555 | **5.670** |
| post-2013 | 8.521 | 8.037 | **7.368** |
| 2026 (partial) | 6.538 | 6.299 | **6.101** |

**OBSERVATION 4.3a.** Within each era, the P99/P50 range ratio is **nearly identical across all three resolutions** (spread ≤ 0.48 within pre-2013, ≤ 1.15 within post-2013, ≤ 0.44 within 2026). Aggregation preserves the *shape* of the amplitude distribution.

**OBSERVATION 4.3b.** The ratio **widens sharply after 2013 at every resolution**: 5.5–5.8 → 7.4–8.5. The tail of the amplitude distribution became relatively heavier post-2013, and this is visible at M1, M3 and H1 alike. **This is not a fine-resolution artefact — it survives aggregation.**

### 4.4 Extreme-event rates (Phase 2, 20-bar lookback)

| Statistic | M1 | M3 | H1 |
|---|---|---|---|
| New-extreme rate (20) | 0.216977 | 0.211338 | 0.199112 |
| Breakout rate (20) | 0.119479 | 0.108646 | 0.099276 |
| Breakout persistence | 0.411817 | 0.404431 | **0.464216** |
| Reintegration rate (5) | 0.588183 | 0.595569 | **0.535784** |
| Range expansion (std of log) | 0.73966 | 0.592926 | 0.572299 |

**OBSERVATION 4.4a.** Breakout *persistence* is highest at H1 (0.4642 vs 0.4118 / 0.4044) and *reintegration* is lowest (0.5358 vs 0.5882 / 0.5956). Consistent, and consistent with Block B's finding that H1 does not show the short-horizon reversal visible at M1/M3.

**OBSERVATION 4.4b.** Range expansion (std of log range) declines monotonically 0.7397 → 0.5929 → 0.5723: **coarser bars have more stable range**, which is the same statement as Block B's observation that range/σ is more stable than range alone.

---

## 5. M1 SHOCK BEHAVIOR

### 5.1 Global

| Metric | M1 |
|---|---|
| σ window (bars) | 1440 |
| Shocks detected | **90,323** |
| Shock rate per bar | **1.5381 %** |
| Shocks per year | 5,420.6 |
| σ-defined bars | 5,872,562 |
| Median shock magnitude | **9.00 bps** / 1.428 USD |
| P90 shock magnitude | 17.53 bps / 3.677 USD |
| P99 shock magnitude | 39.46 bps |
| Median \|z\| at shock | 3.7236 |
| Mean \|z\| at shock | 4.3839 |
| Extreme \|z\| tail: excess kurtosis of \|z\| | 290.9 |
| Median inter-shock gap | 11 bars (11 min) |
| P90 inter-shock gap | 183 bars |
| Removed from sample | **NO** |

### 5.2 Clustering (corrected baseline)

**OBSERVATION 5.2a.** Observed probability that a shock is followed by another shock within 5 bars: **0.372984**.

**OBSERVATION 5.2b.** The correct independent benchmark for "at least one shock in the next 5 bars" is `1 − (1 − p)⁵ = 1 − (1 − 0.015377)⁵ = 0.074555`, **not** the per-bar rate `p` reported in the file's `clustering_baseline_rate` field.

| | M1 |
|---|---|
| Observed P(shock within 5 bars) | 0.372984 |
| Independent benchmark | 0.074555 |
| **Clustering ratio** | **5.003 ×** |

**INFERENCE 5.2c.** M1 shocks cluster **five times** more than an independent process would. This is a strong, robust volatility-clustering effect. Note that the field `shocks.clustering_ratio` in `deep_metrics.json` (value 0.99975) is `mean_gap × per-bar_rate`, which equals 1 **by construction** for any renewal process and is therefore **uninformative**; it is not used.

### 5.3 Persistence and reversion after a shock

| Quantity (5 bars = 5 minutes after a 3σ shock) | M1 |
|---|---|
| Direction persistence (share continuing) | **0.4536** |
| Share reverting | 0.5464 |
| Mean reversion (bps, + = moved back against the shock) | **+0.235** |
| Reversion-positive share | 0.5444 |
| Mean \|displacement\| after 5 bars | 8.32 bps |
| Mean reversion after 20 bars | +0.172 bps |
| Reversion-positive share after 20 bars | 0.5347 |
| Mean \|displacement\| after 20 bars | 14.54 bps |

**OBSERVATION 5.3a.** At M1, the balance after a 3σ shock tilts **against** the shock direction in 54.6 % of cases, with a small net reversion of +0.24 bps over the next 5 minutes and +0.17 bps over 20 minutes. Both net figures are one to two orders of magnitude smaller than the median shock itself (9.00 bps).

**OBSERVATION 5.3b.** The reversion-positive share decays with horizon (0.5444 at 5 bars → 0.5347 at 20 bars): the tilt weakens as the window lengthens.

### 5.4 Annual / era — **NOT AVAILABLE**

**OBSERVATION 5.4a.** `deep_metrics.json` stores the shock block **only at global level** for each resolution (`timeframes.{TF}.shocks`). There is no per-year, per-era or per-vol-class shock block. **Shock frequency, clustering, persistence and reversion cannot be reported annually, pre/post-2013, or for 2026.**

**Mitigation 5.4b (proxy, clearly labelled as such).** Annual *extreme* behaviour is reported in §12 via per-year P95/P99 range and excess kurtosis, which are stored per year for all three resolutions. These are amplitude-tail proxies, **not** the shock statistics requested in §3, and must not be read as shock rates.

**Mitigation 5.4c.** The top-40 shock aggregation table (§8) does carry per-event timestamps, so it **can** be split by era and by year. That split is reported in §8.4 and §13.3.

### 5.5 Top-40 M1 events — timing concentration

**OBSERVATION 5.5a (headline).** Of the 40 largest M1 shocks, **21 (52.5 %) occur at minute :00 of the hour** — the first minute of an H1 bar. Under a uniform distribution the expectation is 1/60 = 1.7 %. The concentration is roughly **31-fold**.

| Minute of hour | Count | | Hour (UTC) | Count |
|---|---|---|---|---|
| :00 | **21** | | 22h | 12 |
| :30 | 7 | | 00h | 7 |
| :01, :03, :05, :06, :09, :10, :12, :19, :27, :29, :33, :57 | 1 each | | 23h | 6 |
| | | | 12h | 5 |
| | | | 13h | 2 |
| | | | 01h | 3 |
| | | | 08h, 11h, 15h, 18h, 19h | 1 each |

**OBSERVATION 5.5b.** **25 of 40 events (62.5 %)** fall in the three hours 22h, 23h and 00h UTC — the daily session-rollover window. A further 7 fall at 12h–13h UTC, all of them at minute :30.

**INFERENCE 5.5c.** The largest M1 "shocks" in this dataset are dominated by **session-boundary discontinuities**, not by intraday dislocation. The M1 return measured across a rollover includes the closure gap; the aggregated bar's open-to-close move does not (see §8.3). This directly qualifies every M1 shock statistic in §5.

**OBSERVATION 5.5d.** No causal attribution is made here. The clustering at 12:30 / 13:30 UTC and at the 22:00–00:00 UTC rollover window is reported as a **timing fact only**; linking it to any publication schedule, participant class or mechanism is outside the scope of this block and is not attempted.

---

## 6. M3 SHOCK BEHAVIOR

### 6.1 Global

| Metric | M3 |
|---|---|
| σ window (bars) | 480 |
| Shocks detected | **30,771** |
| Shock rate per bar | **1.5673 %** |
| Shocks per year | 1,846.7 |
| Median shock magnitude | **15.41 bps** / 2.450 USD |
| P90 shock magnitude | 30.38 bps / 6.414 USD |
| P99 shock magnitude | 68.56 bps |
| Median \|z\| | 3.7577 |
| Median inter-shock gap | 13 bars (39 min) |
| P90 inter-shock gap | 221 bars |

### 6.2 Clustering

| | M3 |
|---|---|
| Observed P(shock within 5 bars) | 0.342920 |
| Independent benchmark `1 − (1 − p)⁵` | 0.075928 |
| **Clustering ratio** | **4.516 ×** |

### 6.3 Persistence and reversion

| Quantity (5 bars = 15 minutes after a 3σ shock) | M3 |
|---|---|
| Direction persistence | **0.4527** |
| Share reverting | 0.5473 |
| Mean reversion (bps) | **+0.211** |
| Reversion-positive share | 0.5461 |
| Mean \|displacement\| after 5 bars | 13.53 bps |
| Mean reversion after 20 bars | +0.146 bps |
| Reversion-positive share after 20 bars | 0.5325 |

### 6.4 M1 → M3 on shocks

**OBSERVATION 6.4a.** Shock **rate** is essentially unchanged: 1.5381 % (M1) → 1.5673 % (M3), +1.9 % relative.

**OBSERVATION 6.4b.** Shock **magnitude** scales almost exactly diffusively: median 9.00 → 15.41 bps, a ratio of 1.7133 against √3 = 1.7321, i.e. **0.989 × √k**. P90: 17.53 → 30.38 = 1.7328, **1.000 × √k**.

**OBSERVATION 6.4c.** **Clustering attenuates only slightly**: 5.003 × → 4.516 × (−9.7 %). M3 retains almost all of the M1 volatility-clustering signature.

**OBSERVATION 6.4d.** **Post-shock behaviour is nearly identical**: direction persistence 0.4536 → 0.4527 (−0.0009); reversion-positive share 0.5444 → 0.5461; net reversion +0.235 → +0.211 bps. Block A reported this as a null result and Block C confirms it over a longer window (20 bars: 0.5347 → 0.5325).

**OBSERVATION 6.4e.** Note the horizon confound: "5 bars" = 5 minutes at M1 and 15 minutes at M3. The near-identical numbers therefore describe *different wall-clock windows*. 6.4d is a descriptive coincidence across resolutions, not a resolution-invariant law.

---

## 7. H1 SHOCK BEHAVIOR

### 7.1 Global

| Metric | H1 |
|---|---|
| σ window (bars) | **24** |
| Shocks detected | **2,697** |
| Shock rate per bar | **2.7412 %** |
| Shocks per year | 161.9 |
| Median shock magnitude | **55.53 bps** / 8.801 USD |
| P90 shock magnitude | 112.93 bps / 22.563 USD |
| P99 shock magnitude | 218.83 bps |
| Median \|z\| | 3.9432 |
| Median inter-shock gap | 31 bars (31 hours) |
| P90 inter-shock gap | 73 bars |

**OBSERVATION 7.1a.** The H1 shock rate (2.7412 %) is **1.78× the M1 rate** and 1.75× the M3 rate.

**INFERENCE 7.1b.** A higher rate at H1 is the *opposite* of what a pure fat-tail argument predicts (kurtosis is lowest at H1, 23.17 vs 88.59), so it is most plausibly an artefact of the **σ estimator**: H1's σ̂ uses only 24 observations, versus 1440 at M1. A noisier σ̂ produces more 3σ crossings. This is an **inference** — the file contains no diagnostic that separates estimator noise from a genuine change in tail behaviour at the hourly scale.

**OBSERVATION 7.1c.** Shock magnitude scales sub-diffusively: median 55.53 bps vs M1's 9.00; ratio 6.170 against √60 = 7.746, i.e. **0.797 × √k**. P90: 112.93 / 17.53 = 6.442 → **0.832 × √k**.

### 7.2 Clustering — the largest behavioural change in the block

| | M1 | M3 | **H1** |
|---|---|---|---|
| Observed P(shock within 5 bars) | 0.372984 | 0.342920 | **0.177976** |
| Independent benchmark | 0.074555 | 0.075928 | **0.129720** |
| **Clustering ratio** | **5.003 ×** | **4.516 ×** | **1.372 ×** |

**OBSERVATION 7.2a.** The clustering ratio collapses from ~5× (M1) and ~4.5× (M3) to **1.37×** at H1. Volatility clustering — the strongest and most robust dynamic signature found at fine resolution — is **largely absent at the hourly scale.**

**LIMITATION 7.2b.** "Within 5 bars" = 5 minutes (M1), 15 minutes (M3), **5 hours** (H1). Clustering is known to decay with horizon, so part or all of 7.2a may be horizon rather than resolution. The file contains no horizon-matched control. **7.2a is reported as an observation; its decomposition is unresolved.**

**OBSERVATION 7.2c.** Note also that H1's *unconditional* shock rate is higher (7.1a), so the benchmark is higher too. The collapse is in the ratio, not merely in the raw conditional probability.

### 7.3 Persistence and reversion — the sign flips

| Quantity | M1 | M3 | **H1** |
|---|---|---|---|
| Direction persistence after 5 bars | 0.4536 | 0.4527 | **0.5002** |
| Share reverting | 0.5464 | 0.5473 | **0.4998** |
| Mean reversion after 5 bars (bps) | +0.235 | +0.211 | **−1.844** |
| Reversion-positive share | 0.5444 | 0.5461 | **0.4994** |
| Mean reversion after 20 bars (bps) | +0.172 | +0.146 | **−1.686** |
| Reversion-positive share after 20 bars | 0.5347 | 0.5325 | **0.4898** |
| Mean \|displacement\| after 5 bars (bps) | 8.32 | 13.53 | 40.63 |

**OBSERVATION 7.3a.** The sub-50 % direction persistence seen at M1 and M3 (45.4 % / 45.3 %) becomes **exactly 50.02 %** at H1 — a coin flip. The net reversion of +0.24 / +0.21 bps becomes **−1.84 bps** (net continuation), and the reversion-positive share crosses below 0.5 (0.4994 at 5 bars, 0.4898 at 20 bars).

**OBSERVATION 7.3b.** Unlike M1/M3, where the reversion tilt **decays** with horizon, at H1 the tilt **grows** slightly with horizon (reversion-positive share 0.4994 → 0.4898; net reversion −1.844 → −1.686 bps, i.e. continuation persists).

**LIMITATION 7.3c.** Same horizon confound as 7.2b: 5 bars = 5 h at H1. Reported as a descriptive difference; not decomposed.

### 7.4 Annual / era

**NOT AVAILABLE** — see §5.4a. The top-40 event split is given instead in §13.3.

---

## 8. M1 → M3 INFORMATION PRESERVATION

### 8.1 The top-40 event table

**OBSERVATION 8.1a (visibility).** All **40 / 40** of the largest M1 shocks are visible in M3. The M3 bar containing each event exists and captures it. **No extreme event is lost by aggregating M1 → M3.**

**OBSERVATION 8.1b (timing).** M3 timing is **preserved for 35 / 40 (87.5 %)**. "Timing preserved" means the shock occurred in the **first minute of the aggregated bar** (`minute_of_epoch % 3 == 0`), so the bar's open registers it immediately. 5 / 40 (12.5 %) occur mid-bar and are registered only in the bar's body/range, with a lag of 0–2 minutes to the bar end.

**OBSERVATION 8.1c (structural loss).** `M3_STRUCT_LOST = 1 − |net| / Σ|Δclose|` over the M1 bars inside the M3 bar.

| | M3 | H1 |
|---|---|---|
| Mean | 0.2155 | 0.8505 |
| **Median** | **0.0000** | **0.8752** |
| Min | −0.0000 | 0.3438 |
| Max | 0.9700 | 0.9983 |
| Events > 0.10 | 15 / 40 | **40 / 40** |
| Events > 0.50 | 10 / 40 | **39 / 40** |

**Median structural loss at M3 is exactly zero**: for at least half of the largest shocks, the three one-minute moves inside the M3 bar are monotonic — the bar loses no path information at all. The mean (0.2155) is pulled up by a minority of events with heavy intrabar reversal.

**OBSERVATION 8.1d (magnitude attenuation).**

| Ratio | Median | Mean | Min | Max |
|---|---|---|---|---|
| M3 body / M1 shock magnitude | **0.2477** | 0.4659 | 0.0026 | 1.6834 |
| M3 range / M1 shock magnitude | **0.4954** | 0.6996 | 0.0218 | 2.2559 |

The M3 **body** carries a median of 24.8 % of the M1 shock; the M3 **range** carries 49.5 %. Roughly half the shock's size survives in the bar's high-low extent even when the open-to-close body does not.

**OBSERVATION 8.1e (severe attenuation is a rollover signature).** 12 of 40 events have an M3 body **below 5 %** of the M1 move. **10 of those 12 occur at minute :00** — they are the rollover bars of §5.5. Examples: S010 (2012-09-03T00:00) M1 = 33.04 USD, M3 body = 0.30 USD, ratio 0.0091; S016 (2019-10-01T00:00) M1 = 23.24 USD, M3 body = 0.06 USD, ratio 0.0026.

**OBSERVATION 8.1f (compression).** Among the 40 events, only **one pair collapses into the same M3 bar**: S018 (2026-02-02T01:10) and S039 (2026-02-02T01:09), one minute apart, both landing in the M3 bar beginning 01:09. **39 distinct M3 bars for 40 M1 shocks.** At the top-40 level, compression of multiple extreme M1 events into a single M3 bar is rare (1 case).

### 8.2 Whole-series information preservation (Phase 2)

| Measure | M1 | M3 | H1 |
|---|---|---|---|
| Observations retained | 100.0 % | **33.4325 %** | **1.67538 %** |
| Timing resolution (min) | 1 | 3 | 60 |
| Timing precision (relative) | 1.0 | **0.33333** | **0.01667** |
| **Path retention ratio** | 1.0 | **0.72721** | **0.12692** |
| Intrabar reversals lost per bar | 0.0 | 0.4836 | **28.1122** |
| M1 swings per bar | 0.4877 | 1.4589 | 29.1116 |
| Intrabar path (USD) | 0.0 | 0.64362 | 19.02984 |
| Intrabar net (USD) | 0.0 | 0.45678 | 2.49390 |
| Order of moves | preserved | **lost** | **lost** |
| **Extremes (high/low) preserved** | 100 % | **100 %** | **100 %** |
| Structural distortion | none (source) | **low** | **high** |
| Bars with internal data gap | 0.0 % | 0.11447 % | 3.16018 % |
| Summary | full | net move only (**72.7 % of path**) | net move only (**12.7 % of path**) |

**OBSERVATION 8.2a.** M3 retains **72.7 % of the M1 path** while discarding 66.6 % of observations. The M1→M3 step is *efficient*: two-thirds of the observations are dropped but only 27 % of the path is lost, because most three-minute windows are directionally simple.

**OBSERVATION 8.2b.** Extremes are preserved **100 % at every resolution by construction** — an aggregated bar's high is the max of its component highs and its low is the min of its component lows. **"Extreme preservation" in the sense of max/min is therefore not a discriminating dimension between M1, M3 and H1.** What differs is whether the *timing*, the *path* and the *order* of those extremes survive — and those differ enormously (8.2c).

**OBSERVATION 8.2c.** M3 → H1 is far more destructive than M1 → M3: path retention 0.727 → 0.127, timing precision 0.333 → 0.017, reversals lost per bar 0.48 → 28.11, order lost at both, structural distortion low → high. **The information cliff is between M3 and H1, not between M1 and M3.**

### 8.3 M1 → M3 verdict

| Dimension | Result | Grade |
|---|---|---|
| Visibility of extremes | 40/40 | **STRONG** |
| Timing preserved | 35/40 (87.5 %) | **STRONG** |
| Magnitude retained (range) | median 0.495 × | **MODERATE** |
| Magnitude retained (body) | median 0.248 × | **MODERATE** |
| Structural loss | median **0.000** | **STRONG** |
| Path retention | 0.727 | **STRONG** (Phase 2) |
| Compression of distinct events | 1 pair / 40 | **STRONG** |
| Contamination by rollover bars | 10/12 severe-attenuation cases at minute :00 | **CAVEAT** |

---

## 9. M3 → H1 INFORMATION PRESERVATION

### 9.1 The top-40 event table

**OBSERVATION 9.1a (visibility).** All **40 / 40** visible in H1. No extreme is lost.

**OBSERVATION 9.1b (timing).** H1 timing is preserved for only **21 / 40 (52.5 %)** — versus 87.5 % at M3. For the 19 events that occur mid-hour, the H1 bar's open misses them; the lag to the end of the H1 bar ranges 1–58 minutes (mean 48.5, median 59 among the preserved group).

**OBSERVATION 9.1c (structural loss).** Median `H1_STRUCT_LOST` = **0.8752**, mean 0.8505, and **40/40 events exceed 0.10**, 39/40 exceed 0.50. **Every one of the largest shocks loses most of its intrabar path at H1.**

**OBSERVATION 9.1d (magnitude attenuation) — H1 behaves differently from M3.**

| Ratio | Median | Mean | Min | Max |
|---|---|---|---|---|
| H1 body / M1 shock magnitude | **0.3912** | 0.5761 | 0.0041 | 2.5244 |
| **H1 range / M1 shock magnitude** | **1.0155** | 1.1785 | 0.0493 | 3.5515 |

**The H1 bar's high-low range carries a median of 102 % of the M1 shock magnitude** — the full size of the event survives in the range — while its open-to-close body carries only 39 %. Compare M3, where the range carries 49.5 % and the body 24.8 %.

**INFERENCE 9.1e.** This is the mechanism behind Block B's aggregation finding (range grows 1.194× faster than √k while close-to-close dispersion grows at 0.895×). Extreme moves are absorbed into the **range** of the coarse bar and expelled from its **body**. At H1 the absorption is complete (median 1.02×); the event's size is fully preserved but its direction-of-travel within the hour is not recoverable from the bar alone.

**OBSERVATION 9.1f (compression).** Same single pair (S018/S039) — **39 distinct H1 bars for 40 shocks.** The two events also collapse into the same M3 bar, so at the top-40 level the M3→H1 step adds no *additional* compression.

### 9.2 Category breakdown (STRUCTURAL_INFORMATION_LOST)

| Category | Count (of 40) |
|---|---|
| H1 timing | 19 |
| H1 intrabar path (struct loss > 0.9) | 13 |
| **none** | **12** |
| M3 intrabar path (struct loss > 0.5) | 10 |
| M3 timing | 5 |

**OBSERVATION 9.2a.** Only **12 / 40 (30 %)** of the largest M1 shocks survive to H1 with **no** structural information lost. 47.5 % lose timing, 32.5 % lose the intrabar path entirely.

### 9.3 M3 → H1 verdict

| Dimension | Result | Grade |
|---|---|---|
| Visibility of extremes | 40/40 | **STRONG** |
| Timing preserved | **21/40 (52.5 %)** | **STRONG (negative)** |
| Magnitude retained (range) | median **1.016 ×** | **STRONG** |
| Magnitude retained (body) | median 0.391 × | **MODERATE** |
| Structural loss | median 0.875, 40/40 > 0.10 | **STRONG (negative)** |
| Path retention | 0.127 | **STRONG (negative)** |
| Events fully preserved | 12/40 (30 %) | **MODERATE** |

**CONCLUSION 9.3a.** H1 **preserves the size** of extreme events (median range/M1 = 1.02×) but **destroys their timing (52.5 % lost), their path (87.3 % lost) and their internal order (100 % lost)**. This is exactly the profile a *context* resolution should have — it tells you the scale of what happened, not when or in what order — and exactly the profile that makes it unsuitable for anything requiring intra-event resolution.

---

## 10. AMPLITUDE / COST

### 10.1 Status of cost inputs

```
BROKER_COST_STATUS = EXTERNAL_INPUT_REQUIRED
```

**All cost figures below are HYPOTHETICAL SCENARIOS** declared ex ante in the Phase 2B spec and carried in the Phase 2 amplitude/cost artifact. **No real spread, commission, swap or slippage is known, modelled, estimated or implied.** Nothing below is profitability, edge, expectancy or strategy gain — it is a ratio of two length measurements in USD of price.

Scenarios (round-trip, USD of price): **S1 = 0.05**, **S2 = 0.10**, **S3 = 0.25**, **S4 = 0.50**, **S5 = 1.00**.

### 10.2 Cost / range (the mission's primary direction)

Cost as a percentage of the bar's range, by resolution, scenario and range statistic.

| Scenario | Cost | Stat | **M1** | **M3** | **H1** |
|---|---|---|---|---|---|
| S1 | 0.05 | Median (P50) | **14.08 %** | **7.45 %** | **1.52 %** |
| S1 | 0.05 | P75 | 7.66 % | 4.19 % | 0.87 % |
| S1 | 0.05 | P90 | 4.10 % | 2.27 % | 0.47 % |
| S1 | 0.05 | P95 | 2.72 % | 1.52 % | 0.32 % |
| S2 | 0.10 | Median | **28.17 %** | **14.90 %** | **3.04 %** |
| S2 | 0.10 | P75 | 15.31 % | 8.38 % | 1.74 % |
| S2 | 0.10 | P90 | 8.20 % | 4.55 % | 0.95 % |
| S2 | 0.10 | P95 | 5.43 % | 3.03 % | 0.64 % |
| S3 | 0.25 | Median | **70.42 %** | **37.26 %** | **7.59 %** |
| S3 | 0.25 | P75 | 38.28 % | 20.94 % | 4.34 % |
| S3 | 0.25 | P90 | 20.49 % | 11.36 % | 2.37 % |
| S3 | 0.25 | P95 | 13.59 % | 7.58 % | 1.59 % |
| S4 | 0.50 | Median | **140.85 %** | **74.52 %** | **15.19 %** |
| S4 | 0.50 | P75 | 76.57 % | 41.88 % | 8.68 % |
| S4 | 0.50 | P90 | 40.98 % | 22.73 % | 4.74 % |
| S4 | 0.50 | P95 | 27.17 % | 15.15 % | 3.18 % |
| S5 | 1.00 | Median | **281.69 %** | **149.03 %** | **30.38 %** |
| S5 | 1.00 | P75 | 153.14 % | 83.75 % | 17.36 % |
| S5 | 1.00 | P90 | 81.97 % | 45.45 % | 9.47 % |
| S5 | 1.00 | P95 | 54.35 % | 30.30 % | 6.36 % |

**OBSERVATION 10.2a.** At every one of the 20 cells, M3's cost burden is **0.529 × M1's** — i.e. **47.1 % lower**. That factor is exactly `M1 median range / M3 median range = 0.355 / 0.671 = 0.5291`, and it is identical across all scenarios and all four statistics because the same cost is being divided by two ranges whose ratio is fixed. (For H1 the equivalent factor is 0.355 / 3.292 = **0.108**, i.e. H1's cost burden is **89.2 % lower** than M1's.)

**OBSERVATION 10.2b (M1 vs M3, the mission's comparison).**

| Statistic | M1 cost / range (S3) | M3 cost / range (S3) | M3 advantage |
|---|---|---|---|
| Median | 70.42 % | 37.26 % | ×0.529 |
| P75 | 38.28 % | 20.94 % | ×0.547 |
| P90 | 20.49 % | 11.36 % | ×0.554 |
| P95 | 13.59 % | 7.58 % | ×0.558 |

**OBSERVATION 10.2c (where cost exceeds the entire bar range).** The hypothetical cost at which cost = 100 % of the range is by definition the range itself:

| Statistic | M1 | M3 | H1 |
|---|---|---|---|
| Median (P50) range | **0.355 USD** | **0.671 USD** | **3.292 USD** |
| P75 range | 0.653 USD | 1.194 USD | 5.760 USD |
| P90 range | 1.220 USD | 2.200 USD | 10.557 USD |
| P95 range | 1.840 USD | 3.300 USD | 15.720 USD |

At the **median bar**: M1 is dominated (cost > range) once the hypothetical cost exceeds **0.355 USD** — it is still safe at S3 (0.25, 70.42 %) and dominated at S4 (0.50, 140.85 %). M3 is dominated only once the cost exceeds **0.671 USD** — still safe at S4 (74.52 %), dominated at S5 (1.00, 149.03 %). H1 is never dominated within the five scenarios (it would require 3.292 USD).

**M3 survives one more hypothetical cost scenario than M1 at the median bar.**

### 10.3 Range / cost (the mission's inverse direction)

| Scenario | Stat | M1 | M3 | H1 |
|---|---|---|---|---|
| S1 | Median | 7.10 | **13.42** | **65.84** |
| S1 | P95 | 36.80 | **66.00** | **314.40** |
| S2 | Median | 3.55 | 6.71 | 32.92 |
| S2 | P95 | 18.40 | 33.00 | 157.20 |
| S3 | Median | 1.42 | 2.684 | 13.168 |
| S3 | P95 | 7.36 | 13.20 | 62.88 |
| S4 | Median | 0.71 | 1.342 | 6.584 |
| S4 | P95 | 3.68 | 6.60 | 31.44 |
| S5 | Median | 0.355 | 0.671 | 3.292 |
| S5 | P95 | 1.84 | 3.30 | 15.72 |

**OBSERVATION 10.3a.** M3's median bar range is **1.890 ×** the S1 hypothetical cost, versus 7.10 × for M1 and 65.84 × for H1. Ratio M3/M1 = 1.890 at every scenario and statistic.

### 10.4 Inverse view: maximum hypothetical cost for a given burden

Maximum hypothetical cost (USD of price) such that cost ≤ X % of the stated range statistic.

| Burden | Stat | M1 | M3 | H1 |
|---|---|---|---|---|
| ≤ 1 % | Median | 0.00355 | 0.00671 | 0.03292 |
| ≤ 2 % | Median | 0.00710 | 0.01342 | 0.06584 |
| ≤ 5 % | Median | 0.01775 | 0.03355 | 0.16460 |
| ≤ 10 % | Median | 0.03550 | 0.06710 | 0.32920 |
| ≤ 20 % | Median | 0.07100 | 0.13420 | 0.65840 |
| ≤ 1 % | P95 | 0.01840 | 0.03300 | 0.15720 |
| ≤ 5 % | P95 | 0.09200 | 0.16500 | 0.78600 |
| ≤ 20 % | P95 | 0.36800 | 0.66000 | 3.14400 |

**OBSERVATION 10.4a.** For cost to be ≤ 1 % of the median bar range, the hypothetical all-in cost would have to be 0.00355 USD at M1, 0.00671 USD at M3 and 0.03292 USD at H1. **M3 tolerates 1.89× the M1 cost; H1 tolerates 9.27×.**

### 10.5 Share of bars whose range exceeds the largest hypothetical cost

| | M1 | M3 | H1 |
|---|---|---|---|
| Bars with range > 1.00 USD | **13.5451 %** | **31.5161 %** | **96.7209 %** |

*(INFERENCE: the CSV repeats a single value per timeframe across all five scenarios and all four statistics, so the reference cost is not labelled. The value is monotone across all 12 timeframes — M1 13.5 %, M2 23.6 %, M3 31.5 %, M5 44.0 %, M10 62.9 %, M15 73.7 %, M20 80.6 %, M30 88.5 %, H1 96.7 %, H2 98.9 %, H4 99.7 % — and each sits on the correct side of that timeframe's median range, which identifies the reference as the 1.00 USD scenario. Used descriptively only.)*

---

## 11. COST SENSITIVITY

### 11.1 Sensitivity to the cost scenario

**OBSERVATION 11.1a (ordering).** Across all 5 scenarios × 4 statistics = 20 cells, **M3's cost/range is always 0.529 × M1's**. The ordering **never flips and cannot flip**: it is the same numerator divided by two ranges in a fixed ratio 1.890.

**OBSERVATION 11.1b (level).** The *level* is highly sensitive. At the median bar the burden rises from 14.08 % (S1) to 281.69 % (S5) at M1 — a **20.0× range** across the scenarios. The ordering is fixed; whether either resolution is *usable* at a given cost is not.

**OBSERVATION 11.1c (threshold).** The point at which the median bar's whole range is consumed is 0.355 USD (M1) versus 0.671 USD (M3). Between those two hypothetical costs, **M1 is dominated and M3 is not**. This is the only region where the M3/M1 distinction has practical bite, and it spans a factor of 1.89 — roughly one scenario width (S3 = 0.25 is below both; S4 = 0.50 is between them; S5 = 1.00 is above both).

### 11.2 Sensitivity to the range statistic

**OBSERVATION 11.2a.** Moving from the median bar to the P95 bar divides the cost burden by:

| | S1 | S3 | S5 |
|---|---|---|---|
| M1 | 5.18 × | 5.18 × | 5.18 × |
| M3 | 4.92 × | 4.92 × | 4.92 × |
| H1 | 4.78 × | 4.78 × | 4.78 × |

The reduction factor is constant across scenarios (it is the P50/P95 range ratio) and nearly identical across resolutions (4.78–5.18).

**INFERENCE 11.2b.** Any statement about cost burden is dominated by *which bar* you consider — the median bar and the P95 bar differ by a factor of 5. A conclusion drawn from the median alone overstates the burden on the bars that would actually carry activity, and one drawn from P95 alone understates it on typical bars. **Both must be reported together**, as in §10.2.

### 11.3 Verdict

```
COST_SENSITIVITY_ORDERING (M3 vs M1) = ROBUST
COST_SENSITIVITY_LEVEL                = SENSITIVE
COST_SENSITIVITY_STATISTIC            = SENSITIVE
```

- **ROBUST:** the ordering M3 < M1 on cost/range holds at all 5 cost scenarios and all 4 range statistics, by arithmetic identity (fixed range ratio 1.890).
- **SENSITIVE:** the level at which cost becomes prohibitive moves by 20× across the scenario range, and by ~5× across the range distribution. Since the real cost is **EXTERNAL_INPUT_REQUIRED**, no conclusion about whether either resolution clears any real cost threshold can be drawn. **No such conclusion is drawn.**

---

## 12. HISTORICAL STABILITY

### 12.1 Annual stability of extreme metrics (16 full years, 2010–2025)

| Metric | TF | Mean | Median | SD | CV | Min | Max |
|---|---|---|---|---|---|---|---|
| **P95 range (USD)** | M1 | 1.2616 | 1.1650 | 0.6879 | **0.545** | 0.600 | 3.437 |
| | M3 | 2.2491 | 2.0700 | 1.2119 | **0.539** | 1.053 | 6.060 |
| | H1 | 10.7142 | 9.8493 | 5.5524 | **0.518** | 4.883 | 28.032 |
| **P99 range (USD)** | M1 | 2.1431 | 1.9347 | 1.1479 | **0.536** | 0.990 | 5.720 |
| | M3 | 3.8088 | 3.4550 | 1.9912 | **0.523** | 1.768 | 9.973 |
| | H1 | 17.5513 | 16.3703 | 8.5463 | **0.487** | 7.719 | 42.961 |
| **Excess kurtosis** | M1 | 83.62 | 44.24 | **117.16** | **1.401** | 9.89 | **430.42** |
| | M3 | 37.81 | 28.28 | 30.34 | **0.802** | 10.46 | 129.13 |
| | **H1** | **12.27** | **10.77** | **5.36** | **0.436** | **5.63** | **21.19** |
| **Return std (bps)** | M1 | 2.5836 | 2.4916 | 0.5520 | 0.214 | 1.707 | 3.608 |
| | M3 | 4.4358 | 4.2441 | 0.9547 | 0.215 | 2.892 | 5.993 |
| | H1 | 19.5617 | 18.7671 | 4.1641 | 0.213 | 12.642 | 26.199 |

**OBSERVATION 12.1a (amplitude extremes are equally unstable everywhere).** The CV of P95 range is 0.545 / 0.539 / 0.518 and of P99 range 0.536 / 0.523 / 0.487. **No resolution is meaningfully more stable than another on extreme amplitude.** This is expected: annual amplitude tracks annual volatility, which is a market property, not a measurement one.

**OBSERVATION 12.1b (tail shape is far more stable at H1).** Excess kurtosis CV is **1.401 (M1)**, 0.802 (M3) and **0.436 (H1)**. M1's kurtosis spans **9.89 to 430.42 — a factor of 43.5 across years** (2015 = 316.10, 2021 = 430.42). H1's spans 5.63 to 21.19 — a factor of 3.8. **H1 is 3.2× more stable than M1 on the tail-shape statistic.**

**OBSERVATION 12.1c (volatility level is equally stable everywhere).** Return std CV is 0.214 / 0.215 / 0.213 — indistinguishable.

**OBSERVATION 12.1d.** Combined with Block B §9 (structural metrics CV 0.6–4.1 % at H1): **H1 is the most stable resolution on every statistic that is not an amplitude level.** On amplitude levels, all three are equally unstable, and the instability is a property of the market, not of the resolution.

### 12.2 Era comparison of extremes

| Block | TF | P95 (USD) | P99 (USD) | P95 (bps) | P99 (bps) | Excess kurtosis |
|---|---|---|---|---|---|---|
| pre-2013 | M1 | 1.199 | 2.058 | 7.853 | 12.954 | **15.92** |
| post-2013 | M1 | 1.490 | 2.863 | 7.363 | 12.953 | **100.30** |
| 2026 | M1 | 7.300 | 13.730 | 15.444 | 28.854 | 52.38 |
| pre-2013 | M3 | 2.201 | 3.805 | 14.361 | 23.746 | **17.01** |
| post-2013 | M3 | 2.653 | 5.063 | 13.091 | 22.945 | **46.31** |
| 2026 | M3 | 12.900 | 23.997 | 27.303 | 50.544 | 30.57 |
| pre-2013 | H1 | 10.850 | 18.290 | 70.260 | 113.838 | **12.49** |
| post-2013 | H1 | 12.509 | 23.282 | 62.031 | 105.943 | **16.96** |
| 2026 | H1 | 60.673 | 112.019 | 126.753 | 236.689 | 21.14 |

**OBSERVATION 12.2a.** In **basis points**, the extreme quantiles are essentially unchanged across the 2013 break at every resolution: M1 P99 12.954 → 12.953 bps; M3 23.746 → 22.945; H1 113.838 → 105.943 (−6.9 %). **The size of extreme bars relative to price did not change at 2013.**

**OBSERVATION 12.2b.** In **USD**, the same quantiles rise 24–39 % (M1 P99 2.058 → 2.863; M3 3.805 → 5.063; H1 18.290 → 23.282) — because the gold price level rose. **BPS is the correct unit for cross-era comparison of extremes; USD is not.**

**OBSERVATION 12.2c.** What *did* change at 2013 is kurtosis: M1 ×6.30 (15.92 → 100.30), M3 ×2.72 (17.01 → 46.31), H1 ×1.36 (12.49 → 16.96). The gradient identified in Block B §10.2c is reproduced here on the era blocks. **The 2013 break changed the tail shape, not the tail size.**

### 12.3 Verdict

| Dimension | Verdict |
|---|---|
| Extreme amplitude (P95/P99) across years | **INSTABLE at all three resolutions, equally** (CV 0.49–0.55) — market-driven, not resolution-driven |
| Tail shape (excess kurtosis) across years | **INSTABLE at M1 (CV 1.40), CONDITIONAL at M3 (0.80), STABLE at H1 (0.44)** |
| Volatility level across years | **STABLE, identical at all three** (CV ≈ 0.214) |
| Extreme size in bps across the 2013 break | **STABLE** |
| Tail shape across the 2013 break | **CHANGED at all three resolutions** |

---

## 13. 2013 DISCONTINUITY

### 13.1 Tail and extreme metrics

Covered in §12.2. Summary: **extreme size in bps unchanged; tail shape changed at all three resolutions; kurtosis change attenuates with aggregation (×6.30 → ×2.72 → ×1.36).**

### 13.2 The shock definition is itself affected

**OBSERVATION 13.2a.** The shock rule compares a bar return against a **trailing rolling σ estimated from the same series**. The 2013 session-convention break (L4) changes the frequency and size of rollover discontinuities. Since 21/40 of the largest M1 shocks are rollover-bar events (§5.5), **the population of detected "shocks" is itself partly a product of the session convention** — and that convention changed at 2013.

**INFERENCE 13.2b.** Any pre/post-2013 comparison of shock *counts* would be contaminated by the convention change independently of any change in market behaviour. Per-era shock statistics are **NOT AVAILABLE** (§5.4a), so this contamination cannot be quantified here — but it must be flagged before any later phase compares shock rates across 2013.

### 13.3 The top-40 split — the sharpest evidence in Block C

| Era | Events | Median M3 body / M1 move | Median H1 body / M1 move | Median H1 range / M1 move |
|---|---|---|---|---|
| pre-2013 (2010–2012) | 4 | **0.0296** | **0.0317** | **0.1269** |
| post-2013 (2013–2025) | 26 | 0.2173 | 0.3246 | 0.9022 |
| 2026 (partial) | 10 | **0.9120** | 0.9021 | 1.8405 |

**OBSERVATION 13.3a.** The **nature of the largest M1 shocks changes radically across the break.** Before 2013, the median top-40 event transmits only **3.0 %** of its M1 magnitude into the M3 body and **12.7 %** into the H1 range — these events are almost entirely rollover discontinuities that aggregation removes. After 2013 the transmission is 21.7 % / 90.2 %, and in 2026 it is 91.2 % / 184 % — genuine intraday dislocations that survive aggregation.

**INFERENCE 13.3b.** Before 2013, the extreme tail of the M1 series is **substantially a data-construction artefact** (the rollover gap being booked as a one-minute return). After 2013, and especially in 2026, the extreme tail is **substantially real price movement**. This is the most consequential single finding of Block C for any later phase that uses M1 extremes as inputs.

**OBSERVATION 13.3c (year distribution of the top 40).**

| Year | 2011 | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2019 | 2020 | 2021 | 2022 | 2025 | **2026** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Events | 1 | 3 | 6 | 4 | 3 | 2 | 1 | 2 | 2 | 2 | 2 | 2 | **10** |

**2026 contributes 10 of the 40 largest M1 shocks — 25 % of the extremes from roughly 4 % of the bars.** 2010 and 2018 contribute none.

**OBSERVATION 13.3d (severe attenuation by era).** Of the 12 events whose M3 body is below 5 % of the M1 move, only **3 are pre-2013**. The rollover-artefact pattern is **not** confined to the pre-2013 convention — it persists (e.g. S015 2026-02-01T23:06, ratio 0.0406) — but it is much less dominant after 2013.

**OBSERVATION 13.3e.** Per §7 of the mission: **the difference in shock character across 2013 is reported as principally attributable to the session-convention break (L4)**, in the sense that the pre-2013 extreme population is dominated by rollover discontinuities whose definition depends on that convention. The residual — whether genuine tail behaviour also changed — is **not separable** with the data in this file.

---

## 14. 2026 SANITY CHECK (PARTIAL YEAR)

**Status: `PARTIAL_YEAR_SANITY_CHECK`. Per L5, 2026 drives no conclusion anywhere in this block.**

| Metric | 2010–2025 median | 2026 | Ratio |
|---|---|---|---|
| P95 range (USD) | M1 1.165 / M3 2.070 / H1 9.849 | M1 7.300 / M3 12.900 / H1 60.673 | **6.27 / 6.23 / 6.16** |
| P99 range (USD) | M1 1.935 / M3 3.455 / H1 16.370 | M1 13.730 / M3 23.997 / H1 112.019 | **7.10 / 6.95 / 6.84** |
| P99 range (bps) | M1 12.95 / M3 22.95 / H1 105.94 | M1 28.854 / M3 50.544 / H1 236.689 | **2.23 / 2.20 / 2.23** |
| Excess kurtosis | M1 44.24 / M3 28.28 / H1 10.77 | M1 52.38 / M3 30.57 / H1 21.14 | 1.18 / 1.08 / **1.96** |
| P99/P50 range ratio | M1 8.52 / M3 8.04 / H1 7.37 (post-2013) | M1 6.54 / M3 6.30 / H1 6.10 | 0.77 / 0.78 / 0.83 |
| Share of top-40 shocks | 26/16 yrs ≈ 1.6/yr | **10** | — |

**OBSERVATION 14a.** 2026 is the **most extreme year in the sample on every amplitude measure at every resolution** — P99 range roughly **6.8–7.1× the 2010–2025 median in USD** and 2.2× in bps. Its 10 top-40 shocks are more than any other year.

**OBSERVATION 14b.** Its **tail shape is unremarkable**: the P99/P50 ratio (6.10–6.54) sits *below* the post-2013 medians (7.37–8.52). 2026 has larger bars, not relatively heavier tails.

**OBSERVATION 14c.** Its **shock character is the most genuine in the sample**: median H1 range / M1 shock = 1.84, versus 0.90 post-2013 and 0.13 pre-2013. The 2026 extremes are real dislocations, not rollover artefacts.

**OBSERVATION 14d.** Per L5, **none of this drives the decision**. It is recorded because 2026 supplies 25 % of the top-40 events and would otherwise distort any unqualified reading of the extreme-event table.

---

## 15. M1 / M3 / H1 CONSOLIDATED MATRIX

Grades: **STRONG** (large, stable, cross-checked) · **MODERATE** (measured but with a named caveat) · **WEAK** (estimator-internal or unresolved) · **N/A** (not available in this source).

| # | Dimension | M1 | M3 | H1 | Evidence strength | Principal limitation |
|---|---|---|---|---|---|---|
| 1 | **Amplitude** | Smallest: median range 0.355 USD / 2.258 bps | Intermediate: 0.671 USD / 4.256 bps | Largest: 3.292 USD / 20.891 bps | **STRONG** (Block A: 4 metrics resolve, 16/16 years, effect/noise 2.05–4.96) | M3's edge over M1 is amplitude-only; it carries no noise or persistence advantage |
| 2 | **Noise proxies** | ACF1 −0.00939; kurtosis 88.59 | ACF1 −0.01208; kurtosis 46.29 | ACF1 −0.00061; kurtosis 23.17 | **WEAK / UNRESOLVED** | Block A: all 8 noise metrics have year-level 95 % intervals spanning zero; the kurtosis difference (M3−M1 = −45.81) has interval [−92.24, +0.63] **including zero**. H1's VR>1 is contradicted by its own ACF(1) by 0.0354 (Block B §3.2a) |
| 3 | **Persistence** | VR < 1 at all 6 lags (0.957–0.988) | VR < 1 at 5 of 6 lags | VR > 1 at **all 6** lags | **WEAK / UNRESOLVED** | H1's VR(2)=1.0348 implies ρ(1)=+0.0348; measured ACF(1) = −0.0006. H1's q=32, q=64 rest on **190 and 31** windows. `HURST_STATUS = INCONCLUSIVE` at all three (estimators diverge 0.074–0.081) |
| 4 | **Continuity** | **Best**: 0.00 % internal-gap bars, 0.267 % non-contiguous steps | Intermediate: 0.114 %, 0.685 % | **Worst**: 3.160 %, 4.301 %; 24,165 missing minutes; max hole 51 min | **STRONG** | H1's continuity does **not** improve after 2013 (0.9665 → 0.9547) while M3's does (0.9774 → 0.9967) |
| 5 | **Extreme preservation** | Source: 100 % by construction; path 1.00 | 40/40 visible; timing 35/40; struct loss median **0.000**; range carries 0.495× | 40/40 visible; timing **21/40**; struct loss median **0.875**; range carries **1.016×** | **STRONG** | Max/min extremes are preserved 100 % at *every* resolution by construction, so "preservation" discriminates only on timing/path/order — where M3 ≫ H1. 21/40 top shocks are rollover artefacts (§5.5) |
| 6 | **Cost sensitivity** (hypothetical) | Cost = 14.08 % (S1) → 281.69 % (S5) of median range; dominated above 0.355 USD | **0.529 × M1 at all 20 cells**; dominated above 0.671 USD | **0.108 × M1**; never dominated (needs 3.292 USD) | **ROBUST on ordering, SENSITIVE on level** (§11.3) | `BROKER_COST_STATUS = EXTERNAL_INPUT_REQUIRED`. Ordering is arithmetic (fixed range ratio), not empirical. Nothing here is profitability or edge |
| 7 | **Historical stability** | Structural metrics CV 0.6–4 % (Block B); kurtosis CV **1.401**; amplitude CV 0.54 | Kurtosis CV 0.802; amplitude CV 0.54 | **Kurtosis CV 0.436 (best)**; structural CV 0.6–4.1 %; amplitude CV 0.52 | **MODERATE–STRONG** | All three equally unstable on amplitude *levels* (market-driven). H1's advantage is on shape and structure only |
| 8 | **Information retention** | 100 % obs, 1.000 path, order preserved | 33.43 % obs, **0.727 path**, order lost, distortion low | 1.68 % obs, **0.127 path**, order lost, distortion **high** | **STRONG** | The cliff is **M3 → H1**, not M1 → M3. M3 drops 66.6 % of observations but only 27.3 % of path |
| 9 | **Context value** | Not assessed in this role | Not assessed in this role | **CONFIRMED WITH LIMITATIONS** (Block B) | **MODERATE–STRONG** | Confirmed on stability and amplitude headroom; **persistence rationale withdrawn**; continuity cost material; blind to the 2013 ACF(1) flip |

### 15.1 Reading of the matrix

**OBSERVATION 15.1a.** M1 wins **one** dimension outright (continuity) and ties on none. M3 wins **none** outright but is second on five and best on the cost-burden ratio. H1 wins **four** (amplitude, tail-shape stability, cost headroom, context value) and loses two decisively (continuity, information retention).

**OBSERVATION 15.1b.** The decision-relevant contrast, M1 vs M3, resolves on **one axis only**: amplitude, and therefore cost burden. On noise, persistence and historical stability of extremes they are statistically indistinguishable; M1 is better on continuity and information; M3 is better on cost burden (0.529×).

**OBSERVATION 15.1c.** Three of the nine dimensions (noise, persistence) are **unresolved at every resolution**. Any decision resting on them is unsupported by this file. The decision does not rest on them — it rests on amplitude/cost, which is resolved.

---

## 16. DECISION AUDIT

### 16.1 The decision under audit

```
PRIMARY   = M3
SECONDARY = M1
CONTEXT   = H1
```

### 16.2 Test of `PRIMARY = M3`

| Evidence | Direction | Grade |
|---|---|---|
| Median range USD 0.355 → 0.671 (16/16 years, effect/noise 2.05) | **supports M3 over M1** | STRONG (Block A) |
| P90 range bps +4.42 (16/16 years, effect/noise 4.42) | **supports** | STRONG |
| Range/σ(w1440) 0.965 → 1.074 (16/16 years, effect/noise 3.43) | **supports** | STRONG |
| Cost burden 0.529 × M1 at all 20 scenario × statistic cells | **supports** | ROBUST (arithmetic) |
| Median bar survives one more hypothetical cost scenario | **supports** | MODERATE |
| Shock visibility 40/40, timing 35/40, struct loss median 0.000 | **supports** | STRONG |
| Path retention 0.727 (66.6 % of observations dropped, 27.3 % of path) | **supports** | STRONG |
| Noise proxies (8 metrics) | **neutral** — intervals span zero | WEAK |
| Persistence / VR / Hurst | **neutral** — unresolved, estimators conflict | WEAK |
| Continuity 0.114 % gaps, 0.685 % non-contiguous | **against** | STRONG but small in absolute size |

**Verdict on PRIMARY = M3: CONFIRMED on amplitude and cost; the noise-reduction rationale that often accompanies such a choice is NOT supported.** The ordering M3 > M1 survives; the *reason* is narrower than Phase 2 stated.

### 16.3 Test of `SECONDARY = M1`

| Evidence | Direction |
|---|---|
| Best continuity (0.00 % gap bars, 0.267 % non-contiguous steps) | **supports** |
| Full information retention (100 % obs, 1.000 path, order preserved) | **supports** |
| Source resolution — M3 and H1 are derived from it | **supports** |
| Cost burden 1.89 × M3 at every scenario | **against** |
| Smallest amplitude → smallest cost headroom | **against** |
| Kurtosis CV 1.401 (least stable tail-shape statistic) | **against** |

**Verdict on SECONDARY = M1: CONFIRMED.** M1 is the correct secondary: it is the only resolution with unbroken continuity and full information, and it is the source from which the others are built. Its weakness (cost burden) is precisely the dimension on which M3 was preferred, so the ordering M3 primary / M1 secondary is internally coherent.

### 16.4 Test of `CONTEXT = H1`

Audited in full in Block B, with the Block C additions below.

| Evidence | Direction |
|---|---|
| Structural metrics CV 0.6–4.1 % across 16 years | **supports** (best in file) |
| **Excess kurtosis CV 0.436 vs 1.401 (M1) and 0.802 (M3)** | **supports** — new in Block C |
| Range/σ = 1.348 (largest volatility-normalised amplitude) | **supports** |
| H1 bar range carries **102 %** of the M1 shock magnitude | **supports** — extremes visible at full size |
| Cost headroom 9.27 × M1 (never dominated within 5 scenarios) | **supports** |
| Stable across 2013 on ACF(1) | **supports** |
| Timing preserved for only 21/40 extremes; 87.3 % of path lost | **against** |
| 3.16 % gap bars, 4.301 % non-contiguous steps | **against** |
| VR > 1 not corroborated by ACF(1) (gap 0.0354) | **against** — persistence rationale withdrawn |
| Blind to the 2013 ACF(1) sign flip | **against** |

**Verdict on CONTEXT = H1: CONFIRMED WITH LIMITATIONS** (Block B verdict, reinforced by Block C on stability and extreme-size preservation, and further limited by Block C on timing/path loss).

### 16.5 Result

Nothing in Block C overturns any part of the decision. But three of the nine matrix dimensions are unresolved, one supporting rationale (noise reduction at M3) is withdrawn, and one (persistence at H1) is withdrawn. The decision therefore stands **with limitations**, not unqualified.

```
TIMEFRAME_DECISION = CONFIRMED_WITH_LIMITATIONS
```

**Why not CONFIRMED.** (i) The M3-over-M1 margin rests on a single dimension — amplitude — with all eight noise metrics unresolved and the kurtosis gradient carrying a 95 % interval that includes zero. (ii) The H1 context role is confirmed only after withdrawing its persistence rationale. (iii) The extreme-event population on which part of the case rests is substantially contaminated by rollover artefacts (21/40 top shocks at minute :00), and pre-2013 that contamination is near-total (median 3.0 % transmission to M3).

**Why not REVISED.** No resolution beats the assigned one on the dimension that decided the assignment. M1 does not beat M3 on amplitude or cost; M3 does not beat M1 on continuity or information; H1 remains the only resolution with the stability and amplitude headroom the context role requires.

**Why not UNRESOLVED.** The amplitude and cost findings are robust and reproducible year by year; the verdict follows from them.

---

## 17. LIMITATIONS

### 17.1 Source and availability

1. **`deep_metrics.json` contains no amplitude/cost block.** §10 and §11 are built from the Phase 2 committed CSV. Grids verified identical (§2.2). This is a reuse of existing results, not a recomputation.
2. **Shock statistics exist only at global level.** No per-year, per-era, per-vol-class or per-session shock block. §3's request for annual, pre/post-2013 and 2026 shock breakdowns is **NOT AVAILABLE** for frequency/clustering/persistence/reversion. Mitigated by (a) annual extreme-tail proxies (§12) and (b) the era split of the top-40 event table (§13.3). Neither is a shock rate.
3. **`BARS_WITH_RANGE_ABOVE_COST_PCT` reference cost is not labelled** in the CSV (one value per timeframe, repeated across all scenarios). Attributed to the 1.00 USD scenario by monotonicity and per-timeframe median-range cross-check (§10.5). Used descriptively only.
4. **P25 of amplitude is absent** from `deep_metrics.json` (quantile grid fixed at P50/P75/P90/P95/P99); taken from the Phase 2 CSV, not reconstructed.
5. **The VR(2)/ACF(1) contradiction at H1 (gap 0.0354) remains unresolved** — diagnosing it would require recomputation on the price series, which is forbidden.
6. **H1's VR at q=32 and q=64 rests on 190 and 31 windows**; its R/S Hurst rests on 190 and 31 blocks, drawn from a calm-biased contiguous subsample.

### 17.2 Methodological

7. **Cross-resolution shock comparison is confounded by construction.** The σ window is 1440 / 480 / 24 bars at M1 / M3 / H1; "5 bars after a shock" is 5 min / 15 min / 5 h. No horizon-matched control exists in the file. §6.4, §7.2 and §7.3 are descriptive differences, not decomposed effects.
8. **`shocks.clustering_ratio` in the file is uninformative** (equals 1 by construction for any renewal process). All clustering statements use the corrected baseline `1 − (1 − p)⁵`.
9. **Cost figures are hypothetical scenarios only.** No real spread, commission, swap or slippage is known or modelled. `BROKER_COST_STATUS = EXTERNAL_INPUT_REQUIRED`. Nothing in §10–§11 is profitability, edge, expectancy or strategy gain.
10. **The M3-vs-M1 cost ordering is arithmetic**, not empirical: it is the inverse of the fixed range ratio 1.890. It is reported as ROBUST because it cannot flip, with the explicit note that this is identity, not evidence.
11. **Extreme "preservation" of high/low is 100 % at every resolution by construction** and therefore does not discriminate. Only timing, path and order discriminate.
12. **The 2013 attribution in §13.3e is an inference**, though a strong one: the pre-2013 top-40 population is dominated by rollover-bar events whose definition depends on the session convention that changed at 2013 (L4). The residual change in genuine tail behaviour is not separable here.
13. **2026 drives nothing** (L5). It is reported separately throughout because it supplies 25 % of the top-40 extreme events.
14. **Sessions are time windows, not participant classes.** No attribution to any category of market participant is made or implied.
15. **Uncertainty convention.** Year-level intervals and CVs are descriptive across-year statistics over 16 full years. They are not significance tests; no p-value, no bar-level standard error, no multiple-comparison correction.

### 17.3 Prohibitions honoured

| Prohibition | Status |
|---|---|
| Regime constructed or labelled | **NO** (`spec.regime_built = false`) |
| Strategy, entry, exit, position, backtest, optimisation | **NO** (`spec.strategy_tested = false`) |
| Return / Sharpe / drawdown / expectancy / hit rate / profit factor | **NO** |
| Volume column used | **NO** (`spec.volume_used = false`) |
| Real spread / commission / slippage invented | **NO** — `EXTERNAL_INPUT_REQUIRED` throughout |
| Order book claimed as observed | **NO** — OHLC only; all mechanism statements labelled INFERENCE or PROXY |
| Outliers removed | **NO** (`spec.extremes_removed = false`; `shocks.never_removed = true`) |
| Gaps filled | **NO** (`spec.gaps_filled = false`) |
| `deep_metrics.json` modified | **NO** — SHA unchanged |
| Source data modified | **NO** — M1 master SHA unchanged |
| `deep_audit.py` re-run | **NO** |
| Dataset reconstructed | **NO** |
| Phase 3 started | **NO** |

### 17.4 Observation vs inference

Every numbered statement is prefixed **OBSERVATION** (a value stored in `deep_metrics.json` or a Phase 2 CSV, or a ratio/aggregate of such values) or **INFERENCE** (an interpretation going beyond the stored numbers). Ratios, medians, counts and coefficients of variation formed from stored values are labelled OBSERVATION because they are arithmetic on stored quantities — they are not independent measurements.

---

## 18. FINAL CONCLUSION

### 18.1 What Block C established

1. **Tail frequency survives aggregation; tail heaviness does not.** The 2σ and 3σ exceedance fractions are near-identical at M1, M3 and H1 (0.0449/0.0447/0.0471 and 0.0164/0.0167/0.0178), while excess kurtosis falls 3.82× (88.59 → 46.29 → 23.17). Aggregation removes the tip of the tail, not its bulk.
2. **Tail shape is resolution-invariant but era-dependent.** The P99/P50 range ratio is nearly the same at all three resolutions within each era, and it widens sharply after 2013 at all three (5.5–5.8 → 7.4–8.5). The 2013 break changed tail *shape*, not tail *size* (extreme quantiles in bps are unchanged across the break).
3. **The information cliff is M3 → H1, not M1 → M3.** M3 drops 66.6 % of observations but keeps 72.7 % of the path, with a median structural loss of exactly zero on the largest events. H1 keeps 1.68 % of observations and 12.7 % of the path, with a median structural loss of 0.875 on the largest events.
4. **H1 preserves the size of extremes but not their timing or order.** The H1 bar's range carries a median of 102 % of the M1 shock magnitude; its body carries 39 %; its timing is preserved for 21/40. This is the correct profile for a context resolution and the wrong one for anything else.
5. **Shock behaviour changes qualitatively at H1.** Clustering collapses from 5.00× (M1) and 4.52× (M3) to 1.37×, and post-shock direction persistence crosses from 45.4 % / 45.3 % (below a coin flip) to 50.02 % (exactly a coin flip). Both are horizon-confounded and neither is decomposed.
6. **The extreme-event population is substantially a session-convention artefact.** 21 of the 40 largest M1 shocks occur at minute :00; 25 of 40 fall in the 22:00–00:00 UTC rollover window. Before 2013, the median top-40 event transmits only 3.0 % of its magnitude into the M3 body — those "shocks" are rollover discontinuities, not dislocations. After 2013 it is 21.7 %; in 2026, 91.2 %.
7. **The M3 cost advantage is real, invariant, and arithmetic.** M3's cost burden relative to bar range is 0.529 × M1's at all 5 hypothetical scenarios × 4 range statistics, and it survives one more hypothetical cost scenario at the median bar. It is not profitability, edge or strategy gain — it is the inverse of the range ratio.

### 18.2 What Block C did not establish

- The direction of persistence at any resolution (VR and ACF conflict; Hurst estimators conflict at all three).
- Any M3-over-M1 advantage on noise (all eight Block A noise metrics unresolved; the kurtosis interval includes zero).
- Any decomposition of the H1 clustering collapse or post-shock sign flip into resolution versus horizon.
- Anything about real cost, and therefore anything about whether either resolution clears a real cost threshold.

### 18.3 Final status

```
PHASE2B_FINAL_STATUS = COMPLETE

TIMEFRAME_DECISION   = CONFIRMED_WITH_LIMITATIONS

PRIMARY_TIMEFRAME    = M3
SECONDARY_TIMEFRAME  = M1
CONTEXT_TIMEFRAME    = H1
```

The decision stands. Its supporting surface is **narrower and better characterised** than at the end of Phase 2: it rests on amplitude and the cost burden that follows from it, not on noise reduction (withdrawn, Block A and C) and not on persistence at H1 (withdrawn, Block B and C). Three of nine matrix dimensions are unresolved, and the extreme-event evidence carries a named contamination that must be carried into any later phase.

### 18.4 Carried forward

| Item | Status |
|---|---|
| `BROKER_COST_STATUS` | **EXTERNAL_INPUT_REQUIRED** — no real cost known; all cost figures hypothetical |
| `HURST_STATUS` | **INCONCLUSIVE** at all three resolutions (estimators diverge 0.074–0.081) |
| H1 persistence direction | **UNRESOLVED** (VR > 1 at all lags vs ACF(1) = −0.0006; gap 0.0354) |
| M3-over-M1 noise advantage | **NOT SUPPORTED** (8/8 noise metrics unresolved; kurtosis interval includes zero) |
| **21/40 top M1 shocks are minute-:00 rollover events** | **CONTAMINATION — must be handled before any later phase uses M1 extremes** |
| Pre-2013 extreme population | **LARGELY ARTEFACTUAL** (median 3.0 % transmission to M3 body) |
| Shock statistics | **GLOBAL ONLY** — no annual, era, vol-class or session shock block exists |
| 2026 | 25 % of top-40 extremes from ~4 % of bars; **drives nothing (L5)** |
| H1 continuity | 3.16 % gap bars, 4.301 % non-contiguous steps, 24,165 missing minutes; **does not improve after 2013** |

---

```
END OF PHASE 2B
BLOCK C COMPLETE
STOP — Phase 3 not started.
```
