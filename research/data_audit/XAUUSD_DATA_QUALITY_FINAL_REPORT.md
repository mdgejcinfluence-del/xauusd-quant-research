# XAUUSD — DATA QUALITY FINAL REPORT (PHASE 1)

**Module:** DATA INGESTION / PROVENANCE / INTEGRITY AUDIT · **Status:** PRE-REGIME · **Stop condition:** STOP after this report

**Generated (UTC):** 2026-09-06T08:35:36+00:00 · **Repository:** `/home/user/xauusd-quant-research`

---

## 0. EXECUTIVE STATUS

```
DATASET_STATUS = PASS_WITH_LIMITATIONS
```

| check | result |
|---|---|
| 7 fragments present and readable | **PASS** (7/7) |
| byte-exact reassembly | **PASS** (re-split proof: True) |
| Parquet validity | **PASS** (v2.6, 5,874,003 rows, 6 row groups) |
| full decode of every value | **PASS** (5,874,003 rows × 6 cols) |
| page-level byte accounting | **PASS** (True) |
| duplicate / out-of-order timestamps | **PASS** (0 / 0) |
| nulls / NaN / inf | **PASS** (0) |
| OHLC logical coherence | **PASS** (0 violation over 5,874,003 rows) |
| 6 fragment seams | **PASS** (0 loss, 0 duplication, strictly monotonic) |
| temporal completeness | **LIMITATION** (15,699 gaps, 2,889,834 missing minutes) |
| volume semantics | **LIMITATION / UNKNOWN** (fractional, not a tick count) |
| quote precision homogeneity | **LIMITATION** (0–3 decimals, varies by era) |
| session-convention homogeneity | **LIMITATION** (no daily break in 2010–2012, systematic from 2013) |
| provenance documentation | **UNKNOWN** (no README/manifest in repository) |

**Decision to proceed:** the 7 fragments are reconstructible, readable and sufficiently integral to continue. The five limitations above are measured, quantified in §7, and must be carried forward as explicit constraints.

---

## 1. FILES INSPECTED AND HASHES

| # | path | bytes | size | SHA-256 | real detected type |
|---|---|---|---|---|---|
| 1 | `XAUUSD_part_01.parquet.part` | 20,971,520 | 20.00 MiB | `f5c96c8c368960a4f0112dfea8a5e9aca32a7bf35bafd15243295857b508f1fc` | Parquet byte-stream HEAD (magic PAR1, footer absent) |
| 2 | `XAUUSD_part_02.parquet.part` | 20,971,520 | 20.00 MiB | `0dadfdf6cf847c9145b8d9219b9ebdb2e3e573ebec603450a7a9e56f5620f0b5` | raw Parquet continuation bytes (no magic at offset 0) |
| 3 | `XAUUSD_part_03.parquet.part` | 20,971,520 | 20.00 MiB | `4c6fee93d8475a156e66d68c7247e3fbd3c93a467efe1e0dcc5aff3219e44da8` | raw Parquet continuation bytes (no magic at offset 0) |
| 4 | `XAUUSD_part_04.parquet.part` | 20,971,520 | 20.00 MiB | `8e0dcbb9f909b94b070df563f3f2832221fd5d09f61f8688ceae54703ac5966d` | raw Parquet continuation bytes (no magic at offset 0) |
| 5 | `XAUUSD_part_05.parquet.part` | 20,971,520 | 20.00 MiB | `6a86c02286b9bab4b0cdeda797779c97cd0cf027514b5215223f8de2044e2024` | raw Parquet continuation bytes (no magic at offset 0) |
| 6 | `XAUUSD_part_06.parquet.part` | 20,971,520 | 20.00 MiB | `4798294afe5e38ffc773f179e963af695e6be63717748235b1736f725e4b5640` | raw Parquet continuation bytes (no magic at offset 0) |
| 7 | `XAUUSD_part_07.parquet.part` | 14,363,472 | 13.70 MiB | `13bf888a1ca5956ed44ada61e5e70eea9ff47ef0e6635382b9187f974c587b93` | Parquet byte-stream TAIL (footer PAR1, head magic absent) |

Reassembled working copy (outside the repository): `/tmp/xauusd_audit/XAUUSD_M1_reconstructed.parquet` — 140,192,592 B — SHA-256 `fdce55a8c8a76c417765ad020794866bb36e5b166c130d2bb4deb2aeeeab91d0`

---

## 2. RECONSTRUCTION METHOD

- **Method:** byte-exact sequential concatenation (cat part_01 .. part_07) — plain binary concatenation in filename order, no transformation, no re-encoding.
- **Signature:** 6 × 20,971,520 B + 14,363,472 B → `split -b 20M`-style fixed size chunking of a single Parquet file.
- **No per-fragment header, no manifest, no padding, no index.**
- **Verification 1 — size:** 140,192,592 B written = 140,192,592 B of fragments → True
- **Verification 2 — re-split proof:** the reassembly re-cut at the same offsets reproduces the 7 original SHA-256 → True, 0 trailing byte
- **Verification 3 — determinism:** two independent hashes → True
- **Verification 4 — Parquet:** footer 6,901 B, `PAR1` head and tail, format v2.6, created by `parquet-cpp-arrow version 18.1.0`
- **Verification 5 — full decode:** 5,874,003 rows × 6 columns decoded, null counts {'timestamp': 0, 'open': 0, 'high': 0, 'low': 0, 'close': 0, 'volume': 0}
- **Verification 6 — page accounting:** all 36 column chunks, bytes parsed = bytes declared, values = num_rows → True
- **Source integrity:** hashes identical before and after the audit → True

---

## 3. SCHEMA

| column | Arrow type | pandas dtype | nullable | nulls | null % |
|---|---|---|---|---|---|
| timestamp | timestamp[ns, tz=UTC] | datetime64[ns, UTC] | True | 0 | 0.0% |
| open | double | float64 | True | 0 | 0.0% |
| high | double | float64 | True | 0 | 0.0% |
| low | double | float64 | True | 0 | 0.0% |
| close | double | float64 | True | 0 | 0.0% |
| volume | double | float64 | True | 0 | 0.0% |

- **Index:** `index_columns = []` → **no index persisted**; the timestamp is a normal column, not an index.
- **Timestamp:** `timestamp[ns, tz=UTC]` → **timezone-aware UTC** (nanosecond resolution, `isAdjustedToUTC = true`).
- **Parquet physical / logical types:**

| column | physical | logical | compression | values (RG0) |
|---|---|---|---|---|
| timestamp | INT64 | Timestamp(isAdjustedToUTC=true, timeUnit=nanoseconds, is_from_converted_type=false, force_set_converted_type=false) | SNAPPY | 1,048,576 |
| open | DOUBLE | None | SNAPPY | 1,048,576 |
| high | DOUBLE | None | SNAPPY | 1,048,576 |
| low | DOUBLE | None | SNAPPY | 1,048,576 |
| close | DOUBLE | None | SNAPPY | 1,048,576 |
| volume | DOUBLE | None | SNAPPY | 1,048,576 |

| attribute | measurement | verdict |
|---|---|---|
| price unit | prices span 1,044.703 – 5,596.805 | magnitude consistent with USD per troy ounce — **UNKNOWN** (not declared) |
| price precision | close: 3 dp 4,454,634 rows · 2 dp 1,255,615 · 1 dp 145,730 · 0 dp 18,024 | mixed — see §7.4 |
| volume unit | min 1e-05 · max 4.91263 · mean 0.035375 · 0.0% integer-valued · 57,236 distinct values | **UNKNOWN** — see L1 |
| temporal resolution | dominant interval 60 s (99.7327% of intervals) | M1 |
| timezone | `UTC` (explicit in Arrow schema and pandas metadata) | **KNOWN** |

---

## 4. REAL TEMPORAL COVERAGE (measured, not assumed)

| item | value |
|---|---|
| first timestamp | `2010-01-01T00:02:00+00:00` |
| last timestamp | `2026-08-30T23:58:00+00:00` |
| rows | 5,874,003 |
| distinct days | 5,140 |
| distinct months | 200 |
| distinct years | 17 (2010 … 2026) |
| calendar span | 8,763,837 minutes (16.66 years) |
| missing minutes vs a 24×7 grid | 2,889,834 |
| coverage of a 24×7 grid | 67.025% |
| rows per day | mean 1142.8 · median 1379 · min 1 · max 1440 |
| least covered year | **2026** (233,755 rows) — partial year (Jan–Aug) |
| most covered year | **2010** (364,242 rows) |

> The dataset does **not** run to the present: it stops on 2026-08-30. 2026 is a **partial year (Jan–Aug)** and must not be counted as a full year.

### 4.1 Coverage per year

| year | rows | days | months | first (UTC) | last (UTC) | coverage of 24×5 | median range (bps) | zero-range bars |
|---|---|---|---|---|---|---|---|---|
| 2010 | 364,242 | 313 | 12 | 2010-01-01 00:02 | 2010-12-31 21:59 | 96.914% | 2.78 | 790 |
| 2011 | 361,187 | 310 | 12 | 2011-01-02 23:00 | 2011-12-30 21:59 | 96.843% | 2.41 | 2,858 |
| 2012 | 353,628 | 304 | 12 | 2012-01-01 23:06 | 2012-12-31 23:57 | 96.683% | 2.14 | 3,638 |
| 2013 | 338,469 | 298 | 12 | 2013-01-01 23:00 | 2013-12-31 21:59 | 94.397% | 2.45 | 2,909 |
| 2014 | 337,956 | 299 | 12 | 2014-01-01 23:00 | 2014-12-31 21:59 | 93.877% | 1.81 | 2,582 |
| 2015 | 345,408 | 304 | 12 | 2015-01-01 23:00 | 2015-12-31 21:59 | 94.809% | 1.95 | 1,328 |
| 2016 | 353,104 | 309 | 12 | 2016-01-03 23:00 | 2016-12-30 21:59 | 95.043% | 2.32 | 439 |
| 2017 | 352,788 | 309 | 12 | 2017-01-02 23:00 | 2017-12-29 21:58 | 94.591% | 1.66 | 718 |
| 2018 | 353,923 | 312 | 12 | 2018-01-01 23:00 | 2018-12-31 21:59 | 94.531% | 1.63 | 1,190 |
| 2019 | 351,913 | 311 | 12 | 2019-01-01 23:00 | 2019-12-31 21:59 | 94.357% | 1.59 | 3,268 |
| 2020 | 355,495 | 312 | 12 | 2020-01-01 23:00 | 2020-12-31 21:59 | 94.951% | 2.92 | 1,359 |
| 2021 | 354,226 | 309 | 12 | 2021-01-03 23:00 | 2021-12-31 21:59 | 95.345% | 2.17 | 505 |
| 2022 | 354,633 | 310 | 12 | 2022-01-02 23:00 | 2022-12-30 21:58 | 95.086% | 2.43 | 343 |
| 2023 | 352,969 | 309 | 12 | 2023-01-02 23:00 | 2023-12-29 21:58 | 94.64% | 1.91 | 566 |
| 2024 | 355,892 | 313 | 12 | 2024-01-01 23:00 | 2024-12-31 21:58 | 94.692% | 2.29 | 216 |
| 2025 | 354,415 | 312 | 12 | 2025-01-01 23:00 | 2025-12-31 21:58 | 94.662% | 3.09 | 48 |
| 2026 | 233,755 | 206 | 8 | 2026-01-01 23:00 | 2026-08-30 23:58 | 94.93% | 4.62 | 10 |

Coverage of 24×5 = rows ÷ (weekday-days × 1440). The 2010–2012 values (96.9 / 96.8 / 96.7 %) are structurally higher than 2013+ (93.9–95.3 %) precisely because the daily one-hour break does not exist yet (§7.4).

### 4.2 Continuity per month

200 months are present. The 15 least covered:

| month | rows | days | coverage of 24×5 | first (UTC) | last (UTC) |
|---|---|---|---|---|---|
| 2018-12 | 27,328 | 26 | 90.37% | 2018-12-02 23:00 | 2018-12-31 21:59 |
| 2015-01 | 26,038 | 24 | 90.41% | 2015-01-01 23:00 | 2015-01-30 21:59 |
| 2019-12 | 28,705 | 27 | 90.609% | 2019-12-01 23:00 | 2019-12-31 21:59 |
| 2014-01 | 28,708 | 26 | 90.619% | 2014-01-01 23:00 | 2014-01-31 21:59 |
| 2025-12 | 30,062 | 27 | 90.767% | 2025-12-01 00:00 | 2025-12-31 21:58 |
| 2017-01 | 28,758 | 26 | 90.777% | 2017-01-02 23:00 | 2017-01-31 23:59 |
| 2013-01 | 28,759 | 26 | 90.78% | 2013-01-01 23:00 | 2013-01-31 23:59 |
| 2024-12 | 28,763 | 27 | 90.792% | 2024-12-01 23:00 | 2024-12-31 21:58 |
| 2019-01 | 30,079 | 27 | 90.818% | 2019-01-01 23:00 | 2019-01-31 23:59 |
| 2014-12 | 30,094 | 27 | 90.864% | 2014-12-01 00:00 | 2014-12-31 21:59 |
| 2023-01 | 28,794 | 26 | 90.89% | 2023-01-02 23:00 | 2023-01-31 23:59 |
| 2020-01 | 30,104 | 27 | 90.894% | 2020-01-01 23:00 | 2020-01-31 21:59 |
| 2026-01 | 28,828 | 26 | 90.997% | 2026-01-01 23:00 | 2026-01-30 21:59 |
| 2017-12 | 27,531 | 24 | 91.042% | 2017-12-01 00:00 | 2017-12-29 21:58 |
| 2023-12 | 27,534 | 24 | 91.052% | 2023-12-01 00:00 | 2023-12-29 21:58 |

The complete 200-month table is in Appendix A.

---

## 5. TIMEZONE AND MARKET CONVENTION (measured)

| item | measurement |
|---|---|
| timezone | **UTC** — explicit (`timestamp[ns, tz=UTC]`, `isAdjustedToUTC=true`, pandas metadata `{'timezone':'UTC'}`) |
| Saturday bars | **0** |
| Sunday bars | **83,472** over 850 Sunday sessions (mean 98.2 bars) |
| rows by weekday | Tuesday: 1,188,114, Wednesday: 1,184,481, Thursday: 1,181,581, Monday: 1,167,200, Friday: 1,069,155, Sunday: 83,472 |

**Measured session shape** (no declaration available — inferred from the data only):

- daily break: last bar at `20:59` UTC → resume `22:00` UTC (1682 occurrences), or `21:59` → `23:00` UTC (888 occurrences);
- converted to `America/New_York` the break always starts at **16:59** (2570 of 2715 events) → this is the standard FX daily rollover;
- the switch between the two UTC windows follows the **US DST calendar** (2nd Sunday of March / 1st Sunday of November), e.g. 2018-03-12 20:59 → 2018-11-05 21:59;
- weekend: last Friday bar `20:59`/`21:59` UTC → first Sunday bar `22:00`/`23:00` UTC; the dominant weekend gap is **176,460 s = 2,941 min** (672 occurrences) and is DST-invariant;
- Sunday sessions: 476 sessions of 120 bars (22:00–23:59 UTC, DST period) and 263 sessions of 60 bars (23:00–23:59 UTC, winter).

> These are **measurements of the feed structure**, not provenance statements. The broker / server actually used is **UNKNOWN**.

---

## 6. REAL FREQUENCY

| interval | rows | share of the top-20 intervals |
|---|---|---|
| 60s | 5,858,303 | 99.738% |
| 120s | 6,893 | 0.117% |
| 3660s | 2,532 | 0.043% |
| 180s | 2,183 | 0.037% |
| 240s | 1,068 | 0.018% |
| 300s | 980 | 0.017% |
| 176460s | 672 | 0.011% |
| 360s | 259 | 0.004% |
| 420s | 139 | 0.002% |
| 3720s | 136 | 0.002% |
| 600s | 117 | 0.002% |
| 480s | 97 | 0.002% |

- dominant interval: **60 s**, 5,858,303 intervals (99.7327% of all intervals) → genuine M1 series;
- intervals different from 60 s: **15,699** (0.267%);
- second most frequent: 120 s — a single missing minute (6,893 occurrences); then 3660 s — the daily rollover break.

---

## 7. ANOMALIES (exact counts)

### 7.1 Timestamp integrity

| check | count | verdict |
|---|---|---|
| duplicate timestamps | 0 | OK |
| timestamps out of order (diff < 0) | 0 | OK |
| null / NaT timestamps | 0 | OK |
| fully duplicated rows | 0 | OK |
| consecutive bars with identical OHLC | 4134 | WARNING |

### 7.2 Value integrity

| check | count | verdict |
|---|---|---|
| null open | 0 | OK |
| null high | 0 | OK |
| null low | 0 | OK |
| null close | 0 | OK |
| null volume | 0 | OK |
| NaN in price columns | 0 | OK |
| inf in price columns | 0 | OK |
| price ≤ 0 | 0 | OK |
| negative volume | 0 | OK |
| zero volume | 0 | OK |

### 7.3 OHLC coherence (over 5,874,003 bars)

| check | count | verdict |
|---|---|---|
| high < low | 0 | OK |
| high < max(open, close, low) | 0 | OK |
| low > min(open, close, high) | 0 | OK |
| open outside [low, high] | 0 | OK |
| close outside [low, high] | 0 | OK |
| negative range | 0 | OK |
| zero range (high == low) | 22767 | WARNING |
| flat bar (O == H == L == C) | 22767 | WARNING |
| range > 50 × median range | 1161 | WARNING |
| range > 100 × median range | 102 | WARNING |
| range > 20 USD | 783 | WARNING |
| range > 50 USD | 29 | WARNING |

Candle range quantiles (USD): q0=0.000, q1=0.017, q25=0.200, q50=0.355, q75=0.653, q95=1.840, q99=4.020, q100=134.120

**Largest ranges** — none violates the high/low bounds, so they cannot be classified as error vs genuine move without an external reference:

| timestamp (UTC) | open | high | low | close | range | gap before (s) |
|---|---|---|---|---|---|---|
| 2026-01-29 15:27:00 | 5,257.385 | 5,260.258 | 5,126.138 | 5,132.298 | 134.120 | 60.0 |
| 2026-01-29 15:28:00 | 5,120.898 | 5,211.698 | 5,098.765 | 5,168.698 | 112.933 | 60.0 |
| 2026-01-29 15:30:00 | 5,188.798 | 5,257.015 | 5,169.298 | 5,226.815 | 87.717 | 60.0 |
| 2026-01-29 15:31:00 | 5,227.155 | 5,251.985 | 5,175.975 | 5,183.825 | 76.010 | 60.0 |
| 2026-02-02 01:10:00 | 4,653.955 | 4,658.965 | 4,583.098 | 4,584.335 | 75.867 | 60.0 |
| 2026-01-29 15:29:00 | 5,177.805 | 5,201.128 | 5,131.298 | 5,188.798 | 69.830 | 60.0 |
| 2026-03-24 11:01:00 | 4,441.635 | 4,441.865 | 4,373.048 | 4,390.615 | 68.817 | 60.0 |
| 2026-02-11 13:30:00 | 5,080.508 | 5,085.768 | 5,018.000 | 5,022.245 | 67.768 | 60.0 |
| 2026-01-30 08:33:00 | 5,127.165 | 5,131.225 | 5,064.201 | 5,064.201 | 67.024 | 60.0 |
| 2026-02-02 01:09:00 | 4,710.435 | 4,712.248 | 4,646.085 | 4,653.965 | 66.163 | 60.0 |

**M1 close-to-close jumps:** 61 moves > 1% · 9 > 2% · 0 > 5% · 0 > 10% (min -2.812% · max 3.051%).

| from (UTC) | to (UTC) | close before | close after | change | gap (s) |
|---|---|---|---|---|---|
| 2013-04-24 23:59:00 | 2013-04-26 00:00:00 | 1,429.923 | 1,473.552 | 3.051% | 86460.0 |
| 2013-09-19 23:59:00 | 2013-09-22 22:00:00 | 1,365.533 | 1,327.133 | -2.812% | 252060.0 |
| 2021-08-08 22:56:00 | 2021-08-08 22:57:00 | 1,715.958 | 1,670.488 | -2.650% | 60.0 |
| 2014-10-30 23:59:00 | 2014-11-02 23:00:00 | 1,200.141 | 1,169.811 | -2.527% | 255660.0 |
| 2015-07-20 01:28:00 | 2015-07-20 01:29:00 | 1,129.499 | 1,102.659 | -2.376% | 60.0 |
| 2026-01-29 15:26:00 | 2026-01-29 15:27:00 | 5,256.768 | 5,132.298 | -2.368% | 60.0 |
| 2011-09-18 23:59:00 | 2011-09-20 00:00:00 | 1,824.952 | 1,781.743 | -2.368% | 86460.0 |
| 2020-03-13 20:59:00 | 2020-03-15 22:00:00 | 1,529.348 | 1,563.798 | 2.253% | 176460.0 |
| 2012-09-06 23:59:00 | 2012-09-09 22:00:00 | 1,698.811 | 1,735.349 | 2.151% | 252060.0 |
| 2012-08-30 23:59:00 | 2012-09-03 00:00:00 | 1,655.008 | 1,688.052 | 1.997% | 259260.0 |

### 7.4 Structural anomalies

| anomaly | measurement | verdict |
|---|---|---|
| mixed quote granularity | close decimals by year — 2 dp dominant in 2015–2018 (2016: 204,298 bars at 2 dp vs 127,538 at 3 dp), 3 dp quasi-exclusive in 2019–2023 (2019: 350,752 bars), mixed again in 2024–2026 | **WARNING** — heterogeneous provenance |
| volume scale / precision drift | decimals: 1 dp=165; 2 dp=15,027; 3 dp=159,081; 4 dp=1,319,068; 5 dp=4,341,067; 6 dp=39,595; 4 dp dominant in 2012–2014, 5 dp elsewhere; mean volume per year from 0.01903 to 0.05813 | **WARNING / UNKNOWN** |
| session-convention change | daily-break events per year: 2011=1; 2012=4; 2013=191; 2014=198; 2015=195; 2016=200; 2017=200; 2018=198; 2019=201; 2020=201; 2021=200; 2022=199; 2023=198; 2024=199; 2025=198; 2026=132 — absent in 2010, anecdotal in 2011–2012, ~200/yr from 2013 | **WARNING** — the 21:00–22:00 UTC window is partially populated before 2013 and empty afterwards |
| max bars per day | 1438 / 1425 / 1440 in 2010–2012 vs 1380 from 2013 | consistent with the missing break |

---

## 8. TEMPORAL GAPS (counted, not filled)

- **15,699 gaps** (intervals > 60 s), i.e. **2,889,834 missing minutes** (32.97% of the calendar span).
- longest gap: **4,591 minutes** (76.5 h).

| class | count | structural interpretation (not economic) |
|---|---|---|
| intraday_liquidity_gap | 11,954 | one or more minutes with no tick inside a session |
| daily_break | 2,715 | daily rollover break (~60 min) |
| weekend_closure | 877 | Friday close → Sunday open (market closed) |
| multi_day_non_weekend | 153 | holiday / missing trading day — NOT explained by the weekend |

| gap size (seconds) | count |
|---|---|
| (60.0, 300.0] | 11,124 |
| (300.0, 900.0] | 779 |
| (900.0, 3600.0] | 101 |
| (3600.0, 9000.0] | 2,702 |
| (9000.0, 100000.0] | 116 |
| (100000.0, 1000000000.0] | 877 |

**Largest gaps:**

| last bar before | first bar after | gap (min) | missing minutes | class | dow before | dow after |
|---|---|---|---|---|---|---|
| 2015-12-24 18:30:00 | 2015-12-27 23:01:00 | 4,591 | 4,590 | weekend_closure | Thursday | Sunday |
| 2020-12-24 18:44:00 | 2020-12-27 23:00:00 | 4,576 | 4,575 | weekend_closure | Thursday | Sunday |
| 2017-12-22 21:58:00 | 2017-12-25 23:00:00 | 4,382 | 4,381 | weekend_closure | Friday | Monday |
| 2017-12-29 21:58:00 | 2018-01-01 23:00:00 | 4,382 | 4,381 | weekend_closure | Friday | Monday |
| 2018-03-29 20:58:00 | 2018-04-01 22:00:00 | 4,382 | 4,381 | weekend_closure | Thursday | Sunday |
| 2019-04-18 20:58:00 | 2019-04-21 22:00:00 | 4,382 | 4,381 | weekend_closure | Thursday | Sunday |
| 2021-12-23 21:58:00 | 2021-12-26 23:00:00 | 4,382 | 4,381 | weekend_closure | Thursday | Sunday |
| 2022-04-14 20:58:00 | 2022-04-17 22:00:00 | 4,382 | 4,381 | weekend_closure | Thursday | Sunday |
| 2022-12-23 21:58:00 | 2022-12-26 23:00:00 | 4,382 | 4,381 | weekend_closure | Friday | Monday |
| 2022-12-30 21:58:00 | 2023-01-02 23:00:00 | 4,382 | 4,381 | weekend_closure | Friday | Monday |
| 2023-04-06 20:58:00 | 2023-04-09 22:00:00 | 4,382 | 4,381 | weekend_closure | Thursday | Sunday |
| 2023-12-22 21:58:00 | 2023-12-25 23:00:00 | 4,382 | 4,381 | weekend_closure | Friday | Monday |
| 2023-12-29 21:58:00 | 2024-01-01 23:00:00 | 4,382 | 4,381 | weekend_closure | Friday | Monday |
| 2024-03-28 20:58:00 | 2024-03-31 22:00:00 | 4,382 | 4,381 | weekend_closure | Thursday | Sunday |
| 2025-04-17 20:58:00 | 2025-04-20 22:00:00 | 4,382 | 4,381 | weekend_closure | Thursday | Sunday |

**Significant non-weekend gaps** (missing trading days — the only gaps not explained by the market calendar):

| last bar before | first bar after | gap (min) | missing minutes | dow before | dow after |
|---|---|---|---|---|---|
| 2024-12-31 21:58:00 | 2025-01-01 23:00:00 | 1,502 | 1,501 | Tuesday | Wednesday |
| 2025-12-31 21:58:00 | 2026-01-01 23:00:00 | 1,502 | 1,501 | Wednesday | Thursday |
| 2013-12-31 21:59:00 | 2014-01-01 23:00:00 | 1,501 | 1,500 | Tuesday | Wednesday |
| 2014-12-31 21:59:00 | 2015-01-01 23:00:00 | 1,501 | 1,500 | Wednesday | Thursday |
| 2018-12-31 21:59:00 | 2019-01-01 23:00:00 | 1,501 | 1,500 | Monday | Tuesday |
| 2019-12-31 21:59:00 | 2020-01-01 23:00:00 | 1,501 | 1,500 | Tuesday | Wednesday |
| 2011-09-18 23:59:00 | 2011-09-20 00:00:00 | 1,441 | 1,440 | Sunday | Tuesday |
| 2012-06-19 23:59:00 | 2012-06-21 00:00:00 | 1,441 | 1,440 | Tuesday | Thursday |
| 2012-06-27 23:59:00 | 2012-06-29 00:00:00 | 1,441 | 1,440 | Wednesday | Friday |
| 2012-08-15 23:59:00 | 2012-08-17 00:00:00 | 1,441 | 1,440 | Wednesday | Friday |
| 2012-09-10 23:59:00 | 2012-09-12 00:00:00 | 1,441 | 1,440 | Monday | Wednesday |
| 2013-02-11 23:59:00 | 2013-02-13 00:00:00 | 1,441 | 1,440 | Monday | Wednesday |
| 2013-03-19 23:59:00 | 2013-03-21 00:00:00 | 1,441 | 1,440 | Tuesday | Thursday |
| 2013-03-26 23:59:00 | 2013-03-28 00:00:00 | 1,441 | 1,440 | Tuesday | Thursday |
| 2013-04-24 23:59:00 | 2013-04-26 00:00:00 | 1,441 | 1,440 | Wednesday | Friday |

- total multi-day non-weekend gaps: **153**, carrying **48,112** of the 2,889,834 missing minutes;
- of those, **31** correspond to a full trading day (≥ 1,439 minutes) with no bar at all (New Year's Day and similar closures);
- intraday liquidity gaps account for **48,326** missing minutes;
- weekend closures account for the remaining **2,793,396** minutes.

> No gap was filled, interpolated or resampled. This list is the input for a later, explicit gap-policy decision.

---

## 9. FRAGMENT BOUNDARY AUDIT (mandatory)

Parquet stores data **column-major**: a byte seam inside a row group does not coincide with a row boundary, and in the worst case *every* row of the cut row group is physically split across the two fragments. The verification window is therefore the **whole row group** containing the seam — a conservative superset of the rows actually cut.

| seam | byte offset | RG | cut page | window rows | window size | window first (UTC) | window last (UTC) | strictly monotonic | duplicates | intervals ≠ 60 s | non-calendar gaps |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 01->02 | 20,971,520 | RG0 | `low` p#6 (DATA_PAGE) | 0–1,048,581 | 1,048,581 | 2010-01-01 00:02:00 | 2012-11-29 04:46:00 | YES | 0 | 9752 | 9595 |
| 02->03 | 41,943,040 | RG1 | `high` p#2 (DATA_PAGE) | 1,048,571–2,097,157 | 1,048,586 | 2012-11-29 04:37:00 | 2015-12-29 05:46:00 | YES | 0 | 1801 | 1055 |
| 03->04 | 62,914,560 | RG2 | `timestamp` p#8 (DATA_PAGE) | 2,097,147–3,145,733 | 1,048,586 | 2015-12-29 05:37:00 | 2018-12-13 21:34:00 | YES | 0 | 958 | 211 |
| 04->05 | 83,886,080 | RG3 | `open` p#0 (DICTIONARY_PAGE) | 3,145,723–4,194,309 | 1,048,586 | 2018-12-13 21:25:00 | 2021-12-02 14:43:00 | YES | 0 | 1611 | 861 |
| 05->06 | 104,857,600 | RG4 | `timestamp` p#6 (DATA_PAGE) | 4,194,299–5,242,885 | 1,048,586 | 2021-12-02 14:34:00 | 2024-11-15 10:46:00 | YES | 0 | 1067 | 323 |
| 06->07 | 125,829,120 | RG5 | `timestamp` p#3 (DATA_PAGE) | 5,242,875–5,874,003 | 631,128 | 2024-11-15 10:37:00 | 2026-08-30 23:58:00 | YES | 0 | 510 | 62 |

“Non-calendar gaps” = gaps that are neither a weekend closure nor the daily break (intraday liquidity gaps and missing sessions). Their concentration in RG0–RG1 is the 2010–2012 sparsity already documented in §7.4; no new gap class appears at any seam.

### Seam 01->02 — rows around the estimated cut (row 891,264)

| position vs cut | timestamp (UTC) | open | high | low | close | volume |
|---|---|---|---|---|---|---|
| -3 | 2012-06-18 02:33:00 | 1,622.523 | 1,622.833 | 1,622.473 | 1,622.703 | 0.0137 |
| -2 | 2012-06-18 02:34:00 | 1,622.712 | 1,623.393 | 1,622.673 | 1,623.373 | 0.0142 |
| -1 | 2012-06-18 02:35:00 | 1,623.373 | 1,623.423 | 1,623.373 | 1,623.383 | 0.0018 |
| +1 | 2012-06-18 02:36:00 | 1,623.353 | 1,623.373 | 1,623.163 | 1,623.273 | 0.0069 |
| +2 | 2012-06-18 02:37:00 | 1,623.252 | 1,623.423 | 1,623.152 | 1,623.263 | 0.0119 |
| +3 | 2012-06-18 02:38:00 | 1,623.243 | 1,623.452 | 1,623.083 | 1,623.133 | 0.0091 |

- window verified: rows 0–1,048,581 (the whole row group 0 containing the seam)
- strictly monotonic: **True** · duplicate timestamps: **0**
- intervals ≠ 60 s: **9,752**, of which **157** are weekend closures or daily breaks and **9,595** are intraday liquidity gaps / missing sessions
- largest |open − previous close| across strictly adjacent minutes (1,038,828 steps of exactly 60 s): **4.943 USD** (across all steps, weekend gaps included: 43.412 USD)

### Seam 02->03 — rows around the estimated cut (row 1,357,867)

| position vs cut | timestamp (UTC) | open | high | low | close | volume |
|---|---|---|---|---|---|---|
| -3 | 2013-10-28 22:37:00 | 1,352.091 | 1,352.121 | 1,352.091 | 1,352.121 | 0.0005 |
| -2 | 2013-10-28 22:38:00 | 1,352.135 | 1,352.207 | 1,352.086 | 1,352.162 | 0.002 |
| -1 | 2013-10-28 22:39:00 | 1,352.163 | 1,352.176 | 1,352.131 | 1,352.142 | 0.001 |
| +1 | 2013-10-28 22:40:00 | 1,352.142 | 1,352.151 | 1,352.132 | 1,352.132 | 0.0007 |
| +2 | 2013-10-28 22:41:00 | 1,352.138 | 1,352.185 | 1,352.132 | 1,352.174 | 0.0015 |
| +3 | 2013-10-28 22:42:00 | 1,352.185 | 1,352.185 | 1,352.178 | 1,352.181 | 0.0004 |

- window verified: rows 1,048,571–2,097,157 (the whole row group 1 containing the seam)
- strictly monotonic: **True** · duplicate timestamps: **0**
- intervals ≠ 60 s: **1,801**, of which **746** are weekend closures or daily breaks and **1,055** are intraday liquidity gaps / missing sessions
- largest |open − previous close| across strictly adjacent minutes (1,046,784 steps of exactly 60 s): **15.380 USD** (across all steps, weekend gaps included: 43.229 USD)

### Seam 03->04 — rows around the estimated cut (row 3,129,553)

| position vs cut | timestamp (UTC) | open | high | low | close | volume |
|---|---|---|---|---|---|---|
| -3 | 2018-11-28 04:03:00 | 1,214.528 | 1,214.618 | 1,214.528 | 1,214.568 | 0.00176 |
| -2 | 2018-11-28 04:04:00 | 1,214.528 | 1,214.528 | 1,214.428 | 1,214.428 | 0.00319 |
| -1 | 2018-11-28 04:05:00 | 1,214.428 | 1,214.428 | 1,214.428 | 1,214.428 | 0.00308 |
| +1 | 2018-11-28 04:06:00 | 1,214.428 | 1,214.428 | 1,214.368 | 1,214.368 | 0.00111 |
| +2 | 2018-11-28 04:07:00 | 1,214.328 | 1,214.328 | 1,214.328 | 1,214.328 | 0.00272 |
| +3 | 2018-11-28 04:08:00 | 1,214.428 | 1,214.428 | 1,214.378 | 1,214.378 | 0.00264 |

- window verified: rows 2,097,147–3,145,733 (the whole row group 2 containing the seam)
- strictly monotonic: **True** · duplicate timestamps: **0**
- intervals ≠ 60 s: **958**, of which **747** are weekend closures or daily breaks and **211** are intraday liquidity gaps / missing sessions
- largest |open − previous close| across strictly adjacent minutes (1,047,627 steps of exactly 60 s): **5.191 USD** (across all steps, weekend gaps included: 10.860 USD)

### Seam 04->05 — rows around the estimated cut (row 3,145,728)

| position vs cut | timestamp (UTC) | open | high | low | close | volume |
|---|---|---|---|---|---|---|
| -3 | 2018-12-13 21:27:00 | 1,242.535 | 1,242.535 | 1,242.505 | 1,242.505 | 0.00074 |
| -2 | 2018-12-13 21:28:00 | 1,242.525 | 1,242.595 | 1,242.505 | 1,242.505 | 0.00259 |
| -1 | 2018-12-13 21:29:00 | 1,242.505 | 1,242.585 | 1,242.495 | 1,242.565 | 0.01095 |
| +1 | 2018-12-13 21:30:00 | 1,242.575 | 1,242.578 | 1,242.425 | 1,242.485 | 0.01584 |
| +2 | 2018-12-13 21:31:00 | 1,242.495 | 1,242.545 | 1,242.495 | 1,242.495 | 0.00148 |
| +3 | 2018-12-13 21:32:00 | 1,242.495 | 1,242.495 | 1,242.385 | 1,242.385 | 0.00111 |

- window verified: rows 3,145,723–4,194,309 (the whole row group 3 containing the seam)
- strictly monotonic: **True** · duplicate timestamps: **0**
- intervals ≠ 60 s: **1,611**, of which **750** are weekend closures or daily breaks and **861** are intraday liquidity gaps / missing sessions
- largest |open − previous close| across strictly adjacent minutes (1,046,974 steps of exactly 60 s): **17.810 USD** (across all steps, weekend gaps included: 38.000 USD)

### Seam 05->06 — rows around the estimated cut (row 4,959,155)

| position vs cut | timestamp (UTC) | open | high | low | close | volume |
|---|---|---|---|---|---|---|
| -3 | 2024-01-31 05:23:00 | 2,033.355 | 2,033.435 | 2,033.315 | 2,033.365 | 0.00345 |
| -2 | 2024-01-31 05:24:00 | 2,033.375 | 2,033.375 | 2,033.215 | 2,033.215 | 0.00108 |
| -1 | 2024-01-31 05:25:00 | 2,033.275 | 2,033.385 | 2,033.235 | 2,033.305 | 0.00228 |
| +1 | 2024-01-31 05:26:00 | 2,033.405 | 2,033.678 | 2,033.405 | 2,033.498 | 0.00636 |
| +2 | 2024-01-31 05:27:00 | 2,033.498 | 2,033.625 | 2,033.478 | 2,033.598 | 0.00624 |
| +3 | 2024-01-31 05:28:00 | 2,033.615 | 2,033.625 | 2,033.545 | 2,033.585 | 0.003 |

- window verified: rows 4,194,299–5,242,885 (the whole row group 4 containing the seam)
- strictly monotonic: **True** · duplicate timestamps: **0**
- intervals ≠ 60 s: **1,067**, of which **744** are weekend closures or daily breaks and **323** are intraday liquidity gaps / missing sessions
- largest |open − previous close| across strictly adjacent minutes (1,047,518 steps of exactly 60 s): **5.296 USD** (across all steps, weekend gaps included: 30.678 USD)

### Seam 06->07 — rows around the estimated cut (row 5,531,342)

| position vs cut | timestamp (UTC) | open | high | low | close | volume |
|---|---|---|---|---|---|---|
| -3 | 2025-09-10 13:51:00 | 3,650.005 | 3,650.915 | 3,648.645 | 3,649.045 | 0.05527 |
| -2 | 2025-09-10 13:52:00 | 3,649.065 | 3,650.895 | 3,648.315 | 3,650.835 | 0.06376 |
| -1 | 2025-09-10 13:53:00 | 3,650.885 | 3,651.085 | 3,650.435 | 3,650.845 | 0.04495 |
| +1 | 2025-09-10 13:54:00 | 3,650.855 | 3,650.915 | 3,649.675 | 3,650.195 | 0.037 |
| +2 | 2025-09-10 13:55:00 | 3,650.085 | 3,650.965 | 3,649.295 | 3,650.765 | 0.04512 |
| +3 | 2025-09-10 13:56:00 | 3,650.805 | 3,651.065 | 3,650.255 | 3,650.835 | 0.02308 |

- window verified: rows 5,242,875–5,874,003 (the whole row group 5 containing the seam)
- strictly monotonic: **True** · duplicate timestamps: **0**
- intervals ≠ 60 s: **510**, of which **448** are weekend closures or daily breaks and **62** are intraday liquidity gaps / missing sessions
- largest |open − previous close| across strictly adjacent minutes (630,617 steps of exactly 60 s): **26.297 USD** (across all steps, weekend gaps included: 111.937 USD)

**Verdict:** 0 duplicated row, 0 lost row, 0 non-monotonic step at all 6 seams. Combined with the re-split proof (§2) and the page-level byte accounting (§2), the reassembly is byte-exact and chronologically continuous.

---

## 10. PROVENANCE

| field | value | status |
|---|---|---|
| provider | UNKNOWN | not available |
| acquisition_method | UNKNOWN | not available |
| symbol | UNVERIFIED (inferred from filename only: XAUUSD) | not available |
| timezone | UTC (explicit: Arrow schema timestamp[ns, tz=UTC] and pandas metadata {'timezone': 'UTC'}) | measured |
| period | MEASURED (see coverage section) | measured |
| market_convention | UNKNOWN as declared / MEASURED (see session section) | not available |
| price_unit | UNKNOWN (magnitude 1044.70-5596.81 consistent with USD per troy ounce, not verified) | not available |
| volume_unit | UNKNOWN (fractional, non-integer: not a tick count; not determinable from the data) | not available |

- README present: **False** · manifest present: **False** · documentation files found in the repository: **0**
- Git history: 1 commit(s) — b047903 Add files via upload (single upload commit, no message describing the data)
- Only technical metadata exists inside the file:

```
created_by      : parquet-cpp-arrow version 18.1.0
pandas metadata : pyarrow 18.1.0, pandas 2.2.3
key-value keys   : ARROW:schema, pandas
```

The writer provenance (pyarrow 18.1.0 / pandas 2.2.3) says **when the file was last written**, not **who produced the prices**. Provider, acquisition method, symbol contract and market convention remain **UNKNOWN**.

---

## 11. DESCRIPTIVE STATISTICS (data-quality diagnostics only)

> **Firewall:** the numbers below are integrity diagnostics. They are **not** a strategy, an edge, a signal, a regime, a mechanism, or evidence of profitability. They must not be used to select, filter or justify anything economic.

- rows: **5,874,003** · columns: 6 · nulls: 0
- price min (low): **1,044.703** (2010-02-05 16:47:00) · price max (high): **5,596.805** (2026-01-28 23:39:00)
- first close 1,096.095 · last close 4,458.015
- M1 close-to-close return distribution (fraction):

| mean | std | min | q1 | q25 | q50 | q75 | q95 | q99 | max |
|---|---|---|---|---|---|---|---|---|---|
| 0.000000 | 0.000284 | -0.028121 | -0.000781 | -0.000102 | 0.000000 | 0.000103 | 0.000383 | 0.000780 | 0.030511 |

- zero returns: 148,038 (2.52%)
- candle range quantiles (USD): q0=0.000, q1=0.017, q25=0.200, q50=0.355, q75=0.653, q95=1.840, q99=4.020, q100=134.120
- volume: min 1e-05 · median 0.0255 · mean 0.035375 · max 4.91263 · 0.0% integer-valued
- anomaly frequencies: zero-range bars 0.388%; bars > 50× median range 0.0198%; |return| > 1% 0.001%; intervals ≠ 60 s 0.267%

---

## 12. LIMITATIONS (carried forward)

| # | limitation | measured impact | blocking? |
|---|---|---|---|
| L1 | **Volume semantics unknown** — fractional, 0.0% integer valued, values in [1e-05, 4.91263], precision changes in 2012–2014 | any volume-based feature is unusable until the unit is established | **no**, but requires a human decision |
| L2 | **Missing minutes** — 15,699 gaps / 2,889,834 missing minutes; 153 multi-day non-weekend gaps (holidays / missing sessions) | any bar-count or continuous-time assumption must be explicit | **no**, but requires a gap policy |
| L3 | **Mixed quote granularity** — 0 to 3 decimals, era-dependent | tick-size assumptions, microstructure work | no |
| L4 | **Session-convention change in 2013** — no daily break before 2013 | 2010–2012 is not frequency-comparable with 2013+ | no, but must be declared |
| L5 | **Provenance unknown** — no provider, acquisition method or contract specification | reproducibility, licensing, contract size (XAUUSD lot definition) | no, but UNKNOWN must stay visible |
| L6 | **2026 is partial** (Jan–Aug, ends 2026-08-30) | year-level comparisons and any “last period” statistics are biased | no |
| L7 | **Extreme bars not classifiable** — 29 bars with a range > 50 USD, 9 M1 moves > 2%; all are internally coherent (no high/low violation) | bad tick vs genuine move cannot be decided without an external reference | no, requires external cross-check |

---

## 13. DATASET_STATUS AND DECISION

```
DATASET_STATUS = PASS_WITH_LIMITATIONS
```

**Rationale against the decision grid:**

- **PASS** not retained: temporal completeness is not total (15,699 gaps), the volume unit is unknown, and the feed structure is not homogeneous.
- **FAIL** not retained: the reassembly is proven byte-exact, the file parses and fully decodes, and there is **0** duplicate timestamp, **0** out-of-order timestamp, **0** null/NaN/inf and **0** OHLC logical violation over 5,874,003 bars.
- **BLOCKED** not retained: everything could be verified — the 7 fragments, the 6 seams, the coverage and the anomalies.

**Decision to proceed:** yes, on the basis of the working reconstruction, provided L1–L7 are declared as constraints and the human decisions in §14 are taken before any volume-based or gap-sensitive work.

---

## 14. ELEMENTS REQUIRING A HUMAN DECISION

| # | question | why it matters |
|---|---|---|
| H1 | What is the volume unit (lots? millions of oz? a normalised tick volume?) and why is it fractional? | determines whether any volume feature is legitimate at all |
| H2 | Who is the provider and what was the acquisition method? | provenance, licensing, contract size, whether the feed is broker-derived |
| H3 | Gap policy for the 11,954 intraday gaps and 153 missing sessions: keep as-is, flag them, or interpolate later (explicitly, never silently)? | affects every continuity assumption |
| H4 | How to handle the 2010–2012 vs 2013+ session-convention change? | intraday frequency comparability |
| H5 | Is 2026 (Jan–Aug) kept in the master dataset, and how is a partial year handled? | coverage statistics and later splitting policy |
| H6 | Do the 29 bars with a range > 50 USD (max 134.120 USD on 2026-01-29) need an external cross-check? | bad-tick risk |
| H7 | Should the working reconstruction be materialised inside the repository (~134 MiB) or always rebuilt from the fragments? | storage vs convenience — current choice: always rebuilt, never committed |

---

## 15. METHODOLOGICAL FIREWALL — COMPLIANCE STATEMENT

| forbidden in Phase 1 | done? |
|---|---|
| build or compute a regime | **NO** |
| test a strategy | **NO** |
| optimise parameters | **NO** |
| search for return / edge / signal | **NO** |
| use 2026 as holdout or validation | **NO** |
| modify the source files | **NO** (hashes identical before/after) |
| delete anomalies silently | **NO** (all counted and listed) |
| fill gaps artificially | **NO** |
| resample the data | **NO** |
| produce an economic conclusion | **NO** |
| import any EURUSD conclusion | **NO** (clean XAUUSD restart) |

---

## 16. REPRODUCIBILITY

```bash
python3 -m venv .venv && ./.venv/bin/pip install pandas pyarrow numpy
./.venv/bin/python research/data_audit/scripts/audit_xauusd_phase1.py \
        --repo . --workdir /tmp/xauusd_audit
./.venv/bin/python research/data_audit/scripts/render_reports.py \
        --metrics /tmp/xauusd_audit/metrics.json \
        --outdir research/data_audit
```

Measured with python 3.11.2 · pandas 3.0.5 · pyarrow 25.0.1 · numpy 2.4.6. The dataset file itself was written by `parquet-cpp-arrow version 18.1.0` with pandas 2.2.3.

---

## APPENDIX A — continuity per month (200 months)

| month | rows | days | coverage of 24×5 | first (UTC) | last (UTC) |
|---|---|---|---|---|---|
| 2010-01 | 28,649 | 26 | 94.739% | 2010-01-01 00:02:00 | 2010-01-31 23:59:00 |
| 2010-02 | 28,009 | 24 | 97.253% | 2010-02-01 00:01:00 | 2010-02-28 23:59:00 |
| 2010-03 | 32,443 | 27 | 97.956% | 2010-03-01 00:00:00 | 2010-03-31 23:59:00 |
| 2010-04 | 30,585 | 26 | 96.544% | 2010-04-01 00:00:00 | 2010-04-30 20:59:00 |
| 2010-05 | 29,543 | 26 | 97.695% | 2010-05-02 22:00:00 | 2010-05-31 23:59:00 |
| 2010-06 | 30,919 | 26 | 97.598% | 2010-06-01 00:00:00 | 2010-06-30 23:59:00 |
| 2010-07 | 30,564 | 26 | 96.477% | 2010-07-01 00:00:00 | 2010-07-30 20:59:00 |
| 2010-08 | 30,875 | 27 | 97.459% | 2010-08-01 22:00:00 | 2010-08-31 23:59:00 |
| 2010-09 | 30,841 | 26 | 97.352% | 2010-09-01 00:00:00 | 2010-09-30 23:59:00 |
| 2010-10 | 29,446 | 26 | 97.374% | 2010-10-01 00:01:00 | 2010-10-31 23:59:00 |
| 2010-11 | 30,664 | 26 | 96.793% | 2010-11-01 00:00:00 | 2010-11-30 23:59:00 |
| 2010-12 | 31,704 | 27 | 95.725% | 2010-12-01 00:00:00 | 2010-12-31 21:59:00 |
| 2011-01 | 29,459 | 26 | 97.417% | 2011-01-02 23:00:00 | 2011-01-31 23:59:00 |
| 2011-02 | 28,057 | 24 | 97.42% | 2011-02-01 00:00:00 | 2011-02-28 23:59:00 |
| 2011-03 | 32,469 | 27 | 98.034% | 2011-03-01 00:00:00 | 2011-03-31 23:59:00 |
| 2011-04 | 28,951 | 25 | 95.737% | 2011-04-01 00:00:00 | 2011-04-29 20:59:00 |
| 2011-05 | 31,049 | 27 | 98.008% | 2011-05-01 22:00:00 | 2011-05-31 23:59:00 |
| 2011-06 | 30,994 | 26 | 97.835% | 2011-06-01 00:00:00 | 2011-06-30 23:59:00 |
| 2011-07 | 29,425 | 26 | 97.305% | 2011-07-01 00:00:00 | 2011-07-31 23:59:00 |
| 2011-08 | 32,423 | 27 | 97.896% | 2011-08-01 00:00:00 | 2011-08-31 23:59:00 |
| 2011-09 | 29,203 | 25 | 96.571% | 2011-09-01 00:00:00 | 2011-09-30 20:59:00 |
| 2011-10 | 29,484 | 26 | 97.5% | 2011-10-02 22:00:00 | 2011-10-31 23:59:00 |
| 2011-11 | 30,354 | 26 | 95.814% | 2011-11-01 00:00:00 | 2011-11-30 23:59:00 |
| 2011-12 | 29,319 | 25 | 92.547% | 2011-12-01 00:00:00 | 2011-12-30 21:59:00 |
| 2012-01 | 29,246 | 27 | 92.317% | 2012-01-01 23:06:00 | 2012-01-31 23:59:00 |
| 2012-02 | 29,331 | 25 | 96.994% | 2012-02-01 00:00:00 | 2012-02-29 23:59:00 |
| 2012-03 | 30,856 | 26 | 97.399% | 2012-03-01 00:00:00 | 2012-03-30 20:59:00 |
| 2012-04 | 28,783 | 26 | 95.182% | 2012-04-01 22:00:00 | 2012-04-30 23:59:00 |
| 2012-05 | 32,181 | 27 | 97.165% | 2012-05-01 00:00:00 | 2012-05-31 23:59:00 |
| 2012-06 | 26,388 | 22 | 96.447% | 2012-06-01 00:00:00 | 2012-06-29 20:59:00 |
| 2012-07 | 30,978 | 27 | 97.784% | 2012-07-01 22:00:00 | 2012-07-31 23:59:00 |
| 2012-08 | 29,539 | 25 | 97.682% | 2012-08-01 00:00:00 | 2012-08-30 23:59:00 |
| 2012-09 | 25,328 | 22 | 97.716% | 2012-09-03 00:00:00 | 2012-09-30 23:59:00 |
| 2012-10 | 32,327 | 26 | 97.606% | 2012-10-01 00:00:00 | 2012-10-31 23:59:00 |
| 2012-11 | 30,645 | 26 | 96.733% | 2012-11-01 00:00:00 | 2012-11-30 21:59:00 |
| 2012-12 | 28,026 | 25 | 97.312% | 2012-12-02 23:00:00 | 2012-12-31 23:57:00 |
| 2013-01 | 28,759 | 26 | 90.78% | 2013-01-01 23:00:00 | 2013-01-31 23:59:00 |
| 2013-02 | 25,905 | 23 | 94.682% | 2013-02-01 00:00:00 | 2013-02-28 23:59:00 |
| 2013-03 | 24,640 | 22 | 95.062% | 2013-03-01 00:00:00 | 2013-03-31 23:59:00 |
| 2013-04 | 28,885 | 25 | 95.519% | 2013-04-01 00:00:00 | 2013-04-30 23:59:00 |
| 2013-05 | 28,499 | 25 | 94.243% | 2013-05-01 00:00:00 | 2013-05-31 20:39:00 |
| 2013-06 | 27,562 | 25 | 95.701% | 2013-06-02 22:00:00 | 2013-06-30 23:59:00 |
| 2013-07 | 29,786 | 25 | 94.021% | 2013-07-01 00:00:00 | 2013-07-31 23:59:00 |
| 2013-08 | 30,156 | 26 | 95.189% | 2013-08-01 00:00:00 | 2013-08-30 20:59:00 |
| 2013-09 | 27,494 | 25 | 95.465% | 2013-09-01 22:00:00 | 2013-09-30 23:59:00 |
| 2013-10 | 31,337 | 27 | 94.617% | 2013-10-01 00:00:00 | 2013-10-31 23:59:00 |
| 2013-11 | 28,248 | 24 | 93.413% | 2013-11-01 00:00:00 | 2013-11-29 18:42:00 |
| 2013-12 | 27,198 | 25 | 94.438% | 2013-12-01 23:00:00 | 2013-12-31 21:59:00 |
| 2014-01 | 28,708 | 26 | 90.619% | 2014-01-01 23:00:00 | 2014-01-31 21:59:00 |
| 2014-02 | 25,928 | 23 | 94.766% | 2014-02-02 23:00:00 | 2014-02-28 21:59:00 |
| 2014-03 | 24,104 | 23 | 92.994% | 2014-03-02 23:00:00 | 2014-03-30 23:59:00 |
| 2014-04 | 26,862 | 24 | 93.271% | 2014-04-01 00:00:00 | 2014-04-30 23:59:00 |
| 2014-05 | 28,565 | 24 | 94.461% | 2014-05-01 00:00:00 | 2014-05-30 20:59:00 |
| 2014-06 | 29,047 | 26 | 96.055% | 2014-06-01 22:00:00 | 2014-06-30 23:59:00 |
| 2014-07 | 31,431 | 27 | 94.9% | 2014-07-01 00:00:00 | 2014-07-31 23:59:00 |
| 2014-08 | 28,595 | 24 | 94.56% | 2014-08-01 00:00:00 | 2014-08-31 23:59:00 |
| 2014-09 | 28,738 | 25 | 95.033% | 2014-09-01 00:00:00 | 2014-09-30 23:59:00 |
| 2014-10 | 28,739 | 25 | 95.036% | 2014-10-02 00:00:00 | 2014-10-30 23:59:00 |
| 2014-11 | 27,145 | 25 | 94.253% | 2014-11-02 23:00:00 | 2014-11-30 23:59:00 |
| 2014-12 | 30,094 | 27 | 90.864% | 2014-12-01 00:00:00 | 2014-12-31 21:59:00 |
| 2015-01 | 26,038 | 24 | 90.41% | 2015-01-01 23:00:00 | 2015-01-30 21:59:00 |
| 2015-02 | 24,568 | 22 | 94.784% | 2015-02-01 23:00:00 | 2015-02-27 21:59:00 |
| 2015-03 | 28,974 | 26 | 95.813% | 2015-03-01 23:00:00 | 2015-03-31 23:59:00 |
| 2015-04 | 28,979 | 25 | 95.83% | 2015-04-01 00:00:00 | 2015-04-30 23:59:00 |
| 2015-05 | 28,662 | 26 | 94.782% | 2015-05-01 00:00:00 | 2015-05-31 23:59:00 |
| 2015-06 | 30,118 | 25 | 95.069% | 2015-06-01 00:00:00 | 2015-06-30 20:59:00 |
| 2015-07 | 31,315 | 27 | 94.55% | 2015-07-01 00:45:00 | 2015-07-31 20:59:00 |
| 2015-08 | 29,099 | 26 | 96.227% | 2015-08-02 22:00:00 | 2015-08-31 23:59:00 |
| 2015-09 | 28,734 | 25 | 95.02% | 2015-09-01 00:00:00 | 2015-09-30 23:59:00 |
| 2015-10 | 30,236 | 26 | 95.442% | 2015-10-01 00:00:00 | 2015-10-30 20:58:00 |
| 2015-11 | 28,597 | 26 | 94.567% | 2015-11-01 23:00:00 | 2015-11-30 23:59:00 |
| 2015-12 | 30,088 | 26 | 94.975% | 2015-12-01 00:00:00 | 2015-12-31 21:59:00 |
| 2016-01 | 27,421 | 25 | 95.212% | 2016-01-03 23:00:00 | 2016-01-31 23:59:00 |
| 2016-02 | 28,741 | 25 | 95.043% | 2016-02-01 00:00:00 | 2016-02-29 23:59:00 |
| 2016-03 | 29,160 | 25 | 96.429% | 2016-03-01 00:00:00 | 2016-03-31 23:59:00 |
| 2016-04 | 28,859 | 25 | 95.433% | 2016-04-01 00:00:00 | 2016-04-29 20:59:00 |
| 2016-05 | 30,236 | 27 | 95.442% | 2016-05-01 22:00:00 | 2016-05-31 23:59:00 |
| 2016-06 | 30,356 | 26 | 95.821% | 2016-06-01 00:00:00 | 2016-06-30 23:59:00 |
| 2016-07 | 28,738 | 26 | 95.033% | 2016-07-01 00:00:00 | 2016-07-31 23:59:00 |
| 2016-08 | 31,739 | 27 | 95.83% | 2016-08-01 00:00:00 | 2016-08-31 23:59:00 |
| 2016-09 | 29,999 | 26 | 94.694% | 2016-09-01 00:00:00 | 2016-09-30 20:59:00 |
| 2016-10 | 29,095 | 26 | 96.214% | 2016-10-02 22:00:00 | 2016-10-31 23:59:00 |
| 2016-11 | 29,845 | 26 | 94.208% | 2016-11-01 00:00:00 | 2016-11-30 23:59:00 |
| 2016-12 | 28,915 | 25 | 91.272% | 2016-12-01 00:00:00 | 2016-12-30 21:59:00 |
| 2017-01 | 28,758 | 26 | 90.777% | 2017-01-02 23:00:00 | 2017-01-31 23:59:00 |
| 2017-02 | 27,328 | 24 | 94.889% | 2017-02-01 00:00:00 | 2017-02-28 23:59:00 |
| 2017-03 | 31,557 | 27 | 95.281% | 2017-03-01 00:00:00 | 2017-03-31 20:59:00 |
| 2017-04 | 26,337 | 24 | 96.261% | 2017-04-02 22:00:00 | 2017-04-30 23:59:00 |
| 2017-05 | 31,498 | 27 | 95.103% | 2017-05-01 00:00:00 | 2017-05-31 23:59:00 |
| 2017-06 | 30,238 | 26 | 95.448% | 2017-06-01 00:00:00 | 2017-06-30 20:59:00 |
| 2017-07 | 28,854 | 26 | 95.417% | 2017-07-02 22:00:00 | 2017-07-31 23:59:00 |
| 2017-08 | 31,736 | 27 | 95.821% | 2017-08-01 00:00:00 | 2017-08-31 23:59:00 |
| 2017-09 | 28,618 | 25 | 94.636% | 2017-09-01 00:00:00 | 2017-09-29 20:59:00 |
| 2017-10 | 30,473 | 27 | 96.19% | 2017-10-01 22:00:00 | 2017-10-31 23:59:00 |
| 2017-11 | 29,860 | 26 | 94.255% | 2017-11-01 00:00:00 | 2017-11-30 23:59:00 |
| 2017-12 | 27,531 | 24 | 91.042% | 2017-12-01 00:00:00 | 2017-12-29 21:58:00 |
| 2018-01 | 30,177 | 27 | 91.114% | 2018-01-01 23:00:00 | 2018-01-31 23:59:00 |
| 2018-02 | 27,370 | 24 | 95.035% | 2018-02-01 00:00:00 | 2018-02-28 23:59:00 |
| 2018-03 | 28,918 | 25 | 95.628% | 2018-03-01 00:00:00 | 2018-03-29 20:58:00 |
| 2018-04 | 29,081 | 26 | 96.167% | 2018-04-01 22:00:00 | 2018-04-30 23:59:00 |
| 2018-05 | 31,491 | 27 | 95.082% | 2018-05-01 00:00:00 | 2018-05-31 23:59:00 |
| 2018-06 | 28,849 | 25 | 95.4% | 2018-06-01 00:00:00 | 2018-06-29 20:58:00 |
| 2018-07 | 30,228 | 27 | 95.417% | 2018-07-01 22:00:00 | 2018-07-31 23:59:00 |
| 2018-08 | 31,598 | 27 | 95.405% | 2018-08-01 00:00:00 | 2018-08-31 20:58:00 |
| 2018-09 | 27,455 | 25 | 95.33% | 2018-09-02 22:00:00 | 2018-09-30 23:59:00 |
| 2018-10 | 31,711 | 27 | 95.746% | 2018-10-01 00:00:00 | 2018-10-31 23:59:00 |
| 2018-11 | 29,717 | 26 | 93.804% | 2018-11-01 00:00:00 | 2018-11-30 21:59:00 |
| 2018-12 | 27,328 | 26 | 90.37% | 2018-12-02 23:00:00 | 2018-12-31 21:59:00 |
| 2019-01 | 30,079 | 27 | 90.818% | 2019-01-01 23:00:00 | 2019-01-31 23:59:00 |
| 2019-02 | 27,236 | 24 | 94.569% | 2019-02-01 00:00:00 | 2019-02-28 23:59:00 |
| 2019-03 | 28,841 | 26 | 95.374% | 2019-03-01 00:00:00 | 2019-03-31 23:59:00 |
| 2019-04 | 28,853 | 25 | 95.413% | 2019-04-01 00:00:00 | 2019-04-30 23:59:00 |
| 2019-05 | 31,251 | 27 | 94.357% | 2019-05-01 00:00:00 | 2019-05-31 20:58:00 |
| 2019-06 | 27,668 | 25 | 96.069% | 2019-06-02 22:00:00 | 2019-06-30 23:59:00 |
| 2019-07 | 31,489 | 27 | 95.075% | 2019-07-01 00:00:00 | 2019-07-31 23:59:00 |
| 2019-08 | 30,218 | 26 | 95.385% | 2019-08-01 00:00:00 | 2019-08-30 20:59:00 |
| 2019-09 | 27,483 | 25 | 95.427% | 2019-09-01 22:00:00 | 2019-09-29 23:59:00 |
| 2019-10 | 31,694 | 27 | 95.694% | 2019-10-01 00:00:00 | 2019-10-31 23:59:00 |
| 2019-11 | 28,396 | 25 | 93.902% | 2019-11-01 00:00:00 | 2019-11-29 19:05:00 |
| 2019-12 | 28,705 | 27 | 90.609% | 2019-12-01 23:00:00 | 2019-12-31 21:59:00 |
| 2020-01 | 30,104 | 27 | 90.894% | 2020-01-01 23:00:00 | 2020-01-31 21:59:00 |
| 2020-02 | 27,350 | 24 | 94.965% | 2020-02-02 23:00:00 | 2020-02-28 21:59:00 |
| 2020-03 | 30,444 | 27 | 96.098% | 2020-03-01 23:00:00 | 2020-03-31 23:59:00 |
| 2020-04 | 28,976 | 25 | 95.82% | 2020-04-01 00:00:00 | 2020-04-30 23:59:00 |
| 2020-05 | 28,738 | 26 | 95.033% | 2020-05-01 00:00:00 | 2020-05-31 23:59:00 |
| 2020-06 | 30,357 | 26 | 95.824% | 2020-06-01 00:00:00 | 2020-06-30 23:59:00 |
| 2020-07 | 31,372 | 27 | 94.722% | 2020-07-01 00:00:00 | 2020-07-31 20:59:00 |
| 2020-08 | 29,100 | 26 | 96.23% | 2020-08-02 22:00:00 | 2020-08-31 23:59:00 |
| 2020-09 | 30,116 | 26 | 95.063% | 2020-09-01 00:00:00 | 2020-09-30 23:59:00 |
| 2020-10 | 30,239 | 26 | 95.451% | 2020-10-01 00:00:00 | 2020-10-30 20:59:00 |
| 2020-11 | 28,601 | 26 | 94.58% | 2020-11-01 23:00:00 | 2020-11-30 23:59:00 |
| 2020-12 | 30,098 | 26 | 95.006% | 2020-12-01 00:00:00 | 2020-12-31 21:59:00 |
| 2021-01 | 27,419 | 25 | 95.205% | 2021-01-03 23:00:00 | 2021-01-31 23:59:00 |
| 2021-02 | 27,359 | 24 | 94.997% | 2021-02-01 00:00:00 | 2021-02-28 23:59:00 |
| 2021-03 | 31,797 | 27 | 96.005% | 2021-03-01 00:00:00 | 2021-03-31 23:59:00 |
| 2021-04 | 28,855 | 25 | 95.42% | 2021-04-01 00:00:00 | 2021-04-30 20:59:00 |
| 2021-05 | 28,857 | 26 | 95.427% | 2021-05-02 22:00:00 | 2021-05-31 23:59:00 |
| 2021-06 | 30,358 | 26 | 95.827% | 2021-06-01 00:00:00 | 2021-06-30 23:59:00 |
| 2021-07 | 29,880 | 25 | 94.318% | 2021-07-01 00:00:00 | 2021-07-30 20:59:00 |
| 2021-08 | 30,469 | 27 | 96.177% | 2021-08-01 22:00:00 | 2021-08-31 23:59:00 |
| 2021-09 | 30,119 | 26 | 95.073% | 2021-09-01 00:00:00 | 2021-09-30 23:59:00 |
| 2021-10 | 28,974 | 26 | 95.813% | 2021-10-01 00:00:00 | 2021-10-31 23:59:00 |
| 2021-11 | 29,845 | 26 | 94.208% | 2021-11-01 00:00:00 | 2021-11-30 23:59:00 |
| 2021-12 | 30,294 | 26 | 95.625% | 2021-12-01 00:00:00 | 2021-12-31 21:59:00 |
| 2022-01 | 28,799 | 26 | 95.235% | 2022-01-02 23:00:00 | 2022-01-31 23:59:00 |
| 2022-02 | 27,448 | 24 | 95.306% | 2022-02-01 00:00:00 | 2022-02-28 23:59:00 |
| 2022-03 | 31,799 | 27 | 96.011% | 2022-03-01 00:00:00 | 2022-03-31 23:59:00 |
| 2022-04 | 27,477 | 24 | 95.406% | 2022-04-01 00:00:00 | 2022-04-29 20:59:00 |
| 2022-05 | 30,327 | 27 | 95.729% | 2022-05-01 22:00:00 | 2022-05-31 23:59:00 |
| 2022-06 | 30,209 | 26 | 95.357% | 2022-06-01 00:00:00 | 2022-06-30 23:59:00 |
| 2022-07 | 28,827 | 26 | 95.327% | 2022-07-01 00:00:00 | 2022-07-31 23:59:00 |
| 2022-08 | 31,734 | 27 | 95.815% | 2022-08-01 00:00:00 | 2022-08-31 23:59:00 |
| 2022-09 | 30,089 | 26 | 94.978% | 2022-09-01 00:00:00 | 2022-09-30 20:59:00 |
| 2022-10 | 29,082 | 26 | 96.171% | 2022-10-02 22:00:00 | 2022-10-31 23:59:00 |
| 2022-11 | 29,935 | 26 | 94.492% | 2022-11-01 00:00:00 | 2022-11-30 23:59:00 |
| 2022-12 | 28,907 | 25 | 91.247% | 2022-12-01 00:00:00 | 2022-12-30 21:58:00 |
| 2023-01 | 28,794 | 26 | 90.89% | 2023-01-02 23:00:00 | 2023-01-31 23:59:00 |
| 2023-02 | 27,443 | 24 | 95.288% | 2023-02-01 00:00:00 | 2023-02-28 23:59:00 |
| 2023-03 | 31,673 | 27 | 95.631% | 2023-03-01 00:00:00 | 2023-03-31 20:59:00 |
| 2023-04 | 26,328 | 24 | 96.228% | 2023-04-02 22:00:00 | 2023-04-30 23:59:00 |
| 2023-05 | 31,583 | 27 | 95.359% | 2023-05-01 00:00:00 | 2023-05-31 23:59:00 |
| 2023-06 | 30,075 | 26 | 94.934% | 2023-06-01 00:00:00 | 2023-06-30 20:59:00 |
| 2023-07 | 28,919 | 26 | 95.632% | 2023-07-02 22:00:00 | 2023-07-31 23:59:00 |
| 2023-08 | 31,674 | 27 | 95.634% | 2023-08-01 00:00:00 | 2023-08-31 23:59:00 |
| 2023-09 | 28,658 | 25 | 94.769% | 2023-09-01 00:00:00 | 2023-09-29 20:59:00 |
| 2023-10 | 30,464 | 27 | 96.162% | 2023-10-01 22:00:00 | 2023-10-31 23:59:00 |
| 2023-11 | 29,824 | 26 | 94.141% | 2023-11-01 00:00:00 | 2023-11-30 23:59:00 |
| 2023-12 | 27,534 | 24 | 91.052% | 2023-12-01 00:00:00 | 2023-12-29 21:58:00 |
| 2024-01 | 30,268 | 27 | 91.389% | 2024-01-01 23:00:00 | 2024-01-31 23:59:00 |
| 2024-02 | 28,808 | 25 | 95.265% | 2024-02-01 00:00:00 | 2024-02-29 23:59:00 |
| 2024-03 | 27,649 | 25 | 96.003% | 2024-03-01 00:00:00 | 2024-03-31 23:59:00 |
| 2024-04 | 30,359 | 26 | 95.83% | 2024-04-01 00:00:00 | 2024-04-30 23:59:00 |
| 2024-05 | 31,463 | 27 | 94.997% | 2024-05-01 00:00:00 | 2024-05-31 20:59:00 |
| 2024-06 | 27,567 | 25 | 95.719% | 2024-06-02 22:00:00 | 2024-06-30 23:59:00 |
| 2024-07 | 31,587 | 27 | 95.371% | 2024-07-01 00:00:00 | 2024-07-31 23:59:00 |
| 2024-08 | 30,240 | 26 | 95.455% | 2024-08-01 00:00:00 | 2024-08-30 20:59:00 |
| 2024-09 | 28,945 | 26 | 95.718% | 2024-09-01 22:00:00 | 2024-09-30 23:59:00 |
| 2024-10 | 31,671 | 27 | 95.625% | 2024-10-01 00:00:00 | 2024-10-31 23:59:00 |
| 2024-11 | 28,572 | 25 | 94.484% | 2024-11-01 00:00:00 | 2024-11-29 19:43:00 |
| 2024-12 | 28,763 | 27 | 90.792% | 2024-12-01 23:00:00 | 2024-12-31 21:58:00 |
| 2025-01 | 30,197 | 27 | 91.175% | 2025-01-01 23:00:00 | 2025-01-31 21:59:00 |
| 2025-02 | 27,440 | 24 | 95.278% | 2025-02-02 23:03:00 | 2025-02-28 21:59:00 |
| 2025-03 | 29,073 | 26 | 96.141% | 2025-03-02 23:00:00 | 2025-03-31 23:59:00 |
| 2025-04 | 28,950 | 25 | 95.734% | 2025-04-01 00:00:00 | 2025-04-30 23:59:00 |
| 2025-05 | 30,087 | 26 | 94.972% | 2025-05-01 00:00:00 | 2025-05-30 20:59:00 |
| 2025-06 | 28,949 | 26 | 95.731% | 2025-06-01 22:00:00 | 2025-06-30 23:59:00 |
| 2025-07 | 31,499 | 27 | 95.106% | 2025-07-01 00:00:00 | 2025-07-31 23:59:00 |
| 2025-08 | 28,971 | 26 | 95.804% | 2025-08-01 00:00:00 | 2025-08-31 23:59:00 |
| 2025-09 | 30,209 | 26 | 95.357% | 2025-09-01 00:00:00 | 2025-09-30 23:59:00 |
| 2025-10 | 31,620 | 27 | 95.471% | 2025-10-01 00:00:00 | 2025-10-31 20:59:00 |
| 2025-11 | 27,358 | 25 | 94.993% | 2025-11-02 23:00:00 | 2025-11-30 23:59:00 |
| 2025-12 | 30,062 | 27 | 90.767% | 2025-12-01 00:00:00 | 2025-12-31 21:58:00 |
| 2026-01 | 28,828 | 26 | 90.997% | 2026-01-01 23:00:00 | 2026-01-30 21:59:00 |
| 2026-02 | 27,430 | 24 | 95.243% | 2026-02-01 23:06:00 | 2026-02-27 21:59:00 |
| 2026-03 | 30,476 | 27 | 96.199% | 2026-03-01 23:00:00 | 2026-03-31 23:59:00 |
| 2026-04 | 28,977 | 25 | 95.823% | 2026-04-01 00:00:00 | 2026-04-30 23:59:00 |
| 2026-05 | 28,827 | 26 | 95.327% | 2026-05-01 00:00:00 | 2026-05-31 23:59:00 |
| 2026-06 | 30,119 | 26 | 95.073% | 2026-06-01 00:00:00 | 2026-06-30 23:59:00 |
| 2026-07 | 31,379 | 27 | 94.743% | 2026-07-01 00:00:00 | 2026-07-31 20:59:00 |
| 2026-08 | 27,719 | 25 | 96.247% | 2026-08-02 22:00:00 | 2026-08-30 23:58:00 |

---

## APPENDIX B — hourly distribution of bars (UTC)

| hour (UTC) | bars |
|---|---|
| 00:00 | 255,605 |
| 01:00 | 255,799 |
| 02:00 | 255,836 |
| 03:00 | 255,781 |
| 04:00 | 255,778 |
| 05:00 | 255,891 |
| 06:00 | 255,968 |
| 07:00 | 255,959 |
| 08:00 | 255,957 |
| 09:00 | 255,911 |
| 10:00 | 255,907 |
| 11:00 | 255,907 |
| 12:00 | 255,920 |
| 13:00 | 255,864 |
| 14:00 | 255,859 |
| 15:00 | 255,869 |
| 16:00 | 255,802 |
| 17:00 | 253,560 |
| 18:00 | 250,824 |
| 19:00 | 248,754 |
| 20:00 | 247,453 |
| 21:00 | 96,969 |
| 22:00 | 172,559 |
| 23:00 | 254,271 |

---

**STOP.** Phase 1 is complete. No timeframe, no regime, no strategy.

