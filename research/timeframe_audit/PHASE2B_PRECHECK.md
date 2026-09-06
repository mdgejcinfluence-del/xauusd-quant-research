# PHASE 2B — PRECHECK / FREEZE

**Purpose:** cleanly freeze the preparatory work already performed, so that
Phase 2B can be executed in short, controlled blocks.

**Scope of this document:** verification only. No metric is computed here, no
conclusion is drawn, no code is written, and the Phase 2B methodological
specification is left exactly as issued.

**Captured (UTC):** 2026-09-06T10:14Z
**Branch:** `arena/01a075b8-xauusd-quant-research`
**HEAD:** `c0d236f` — Phase 2 timeframe/granularity audit (pushed)

---

## Verdicts

```
ENVIRONMENT            = PASS
M1_MASTER_INTEGRITY    = PASS
SOURCE_INTEGRITY       = PASS
SCRIPT_SYNTAX          = PASS
ANALYSIS_EXECUTED      = TRUE   (RAW_ENGINE_ONLY — see §6 for the exact scope)
STATUS                 = READY_FOR_BLOCK_EXECUTION
```

---

## 1. ENVIRONMENT = PASS

| item | value | status |
|---|---|---|
| Working tree | `/home/user/xauusd-quant-research` | PASS |
| Inside a git work tree | `true` | PASS |
| Branch | `arena/01a075b8-xauusd-quant-research` | PASS (session branch) |
| HEAD | `c0d236f` (Phase 2, pushed) | PASS |
| Virtualenv interpreter | `/home/user/.venv/bin/python` present and executable | PASS |
| Python version | 3.11.2 | PASS |
| Phase 1 artefacts present | `research/data_audit/` intact | PASS |
| Phase 2 artefacts present | 6 CSV + 1 report + 3 figures + 5 scripts, all committed | PASS |
| `/tmp` working directory | `/tmp/xauusd_audit/` intact, M1 master + 12-timeframe grid present | PASS |

---

## 2. M1_MASTER_INTEGRITY = PASS

| source of the hash | SHA-256 |
|---|---|
| Live file `/tmp/xauusd_audit/XAUUSD_M1_reconstructed.parquet` | `fdce55a8c8a76c417765ad020794866bb36e5b166c130d2bb4deb2aeeeab91d0` |
| Recorded by Phase 1 (`reconstructed.sha256`) | `fdce55a8c8a76c417765ad020794866bb36e5b166c130d2bb4deb2aeeeab91d0` |
| Recorded in the grid build manifest (`timeframes/manifest.json`) | `fdce55a8c8a76c417765ad020794866bb36e5b166c130d2bb4deb2aeeeab91d0` |

All three agree. The M1 master is byte-identical to the file validated in
Phase 1. **No reconstruction was re-run and none is required.**

Master size: 140,192,592 bytes · 5,874,003 rows · columns
`timestamp, open, high, low, close, volume` (volume never read — L1).

---

## 3. SOURCE_INTEGRITY = PASS

| fragment | SHA-256 |
|---|---|
| `XAUUSD_part_01.parquet.part` | `f5c96c8c368960a4f0112dfea8a5e9aca32a7bf35bafd15243295857b508f1fc` |
| `XAUUSD_part_02.parquet.part` | `0dadfdf6cf847c9145b8d9219b9ebdb2e3e573ebec603450a7a9e56f5620f0b5` |
| `XAUUSD_part_03.parquet.part` | `4c6fee93d8475a156e66d68c7247e3fbd3c93a467efe1e0dcc5aff3219e44da8` |
| `XAUUSD_part_04.parquet.part` | `8e0dcbb9f909b94b070df563f3f2832221fd5d09f61f8688ceae54703ac5966d` |
| `XAUUSD_part_05.parquet.part` | `6a86c02286b9bab4b0cdeda797779c97cd0cf027514b5215223f8de2044e2024` |
| `XAUUSD_part_06.parquet.part` | `4798294afe5e38ffc773f179e963af695e6be63717748235b1736f725e4b5640` |
| `XAUUSD_part_07.parquet.part` | `13bf888a1ca5956ed44ada61e5e70eea9ff47ef0e6635382b9187f974c587b93` |

`git status --short` reports **no modification to any tracked file** (L7
satisfied). The only entry is one untracked new script — see §5.

---

## 4. SCRIPT_SYNTAX = PASS

All nine scripts parse under `ast.parse` with Python 3.11.2:

| script | status |
|---|---|
| `research/timeframe_audit/scripts/analyze_timeframes.py` | OK |
| `research/timeframe_audit/scripts/build_timeframes.py` | OK |
| `research/timeframe_audit/scripts/deep_audit.py` **(new)** | OK |
| `research/timeframe_audit/scripts/render_phase2.py` | OK |
| `research/timeframe_audit/scripts/score_and_render.py` | OK |
| `research/timeframe_audit/scripts/variance_signature.py` | OK |
| `research/data_audit/scripts/audit_xauusd_phase1.py` | OK |
| `research/data_audit/scripts/parquet_pagemap.py` | OK |
| `research/data_audit/scripts/render_reports.py` | OK |

Syntax validity is the only claim made here. `deep_audit.py` has additionally
been *executed* once successfully (§6); none of the other Phase 2B code paths
have been exercised.

---

## 5. FILES CREATED — identification

### 5.1 New in this session (untracked)

| file | bytes | purpose |
|---|---|---|
| `research/timeframe_audit/scripts/deep_audit.py` | ~30 KB | Phase 2B metric engine for M1 / M3 / H1 |
| `research/timeframe_audit/PHASE2B_PRECHECK.md` | — | this document |

**`deep_audit.py` is currently untracked and uncommitted.** Nothing has been
pushed. It is preserved on disk and can be committed at the end of Phase 2B,
or earlier on request.

### 5.2 Working artefacts outside the repository (`/tmp/xauusd_audit/`)

| file | bytes | role |
|---|---|---|
| `XAUUSD_M1_reconstructed.parquet` | 140,192,592 | M1 master (Phase 1, unchanged) |
| `timeframes/` (12 parquet + `manifest.json`) | — | Phase 2 grid M1…H4 |
| `deep_metrics.json` | 657,646 | **Phase 2B raw metric output** (see §6) |
| `metrics.json`, `metrics_tf.json`, `scores.json`, `variance_signature.json`, `verdict.json` | — | Phase 2 outputs, unchanged |
| `phase2_execution_diagnostic.log` | 4,008 | log from the interrupted RECOVERY mission |

### 5.3 Phase 2B deliverables — none exist yet

All twelve required outputs are absent and remain to be produced:

```
ABSENT  XAUUSD_DEEP_GRANULARITY_AUDIT.md
ABSENT  XAUUSD_M1_M3_MICROSTRUCTURE_PROXIES.csv
ABSENT  XAUUSD_M1_M3_AMPLITUDE_COST.csv
ABSENT  XAUUSD_H1_PERSISTENCE_ANALYSIS.csv
ABSENT  XAUUSD_CONTINUITY_COMPARISON.csv
ABSENT  XAUUSD_EXTREME_SHOCK_ANALYSIS.csv
ABSENT  XAUUSD_GRANULARITY_RECOMMENDATION.csv
ABSENT  figures/m1_vs_m3_amplitude.*
ABSENT  figures/m1_vs_m3_noise_proxies.*
ABSENT  figures/h1_persistence_by_volatility.*
ABSENT  figures/amplitude_cost_m1_m3.*
ABSENT  figures/shock_preservation_m1_m3_h1.*
```

**No Phase 2B renderer exists yet.** `deep_metrics.json` holds every number the
deliverables need, but nothing has been written from it.

---

## 6. ANALYSIS_EXECUTED = TRUE (RAW_ENGINE_ONLY)

This is stated precisely, because a binary answer alone would be misleading.

**What did run:** `deep_audit.py` was executed **once, end to end**, in 107 s,
and completed without error. It wrote
`/tmp/xauusd_audit/deep_metrics.json` (657,646 bytes), containing the full raw
metric set for M1, M3 and H1:

* amplitude in USD, in % of price, and in bps — range, body, upper wick,
  lower wick, body/range, wick/body, with P25–P99
* volatility-normalised amplitude (range, body, absolute return ÷ trailing σ)
  at the three ex-ante windows 60 / 240 / 1440 minutes
* autocorrelation lags 1–5 on contiguous steps, split by year, by the five
  pre-declared UTC windows, by volatility class, and pre/post-2013
* variance ratios at q = 2…64 and two Hurst estimators (VR-implied and R/S),
  with window sensitivity and per-year stability
* continuity cartography per resolution, per year
* 3σ shock detection with magnitude, clustering, recovery, persistence
* M1→M3→H1 shock aggregation table (40 largest M1 shocks)
* M1-vs-M3 paired-by-year discrimination table over 15 metrics

**What did not run, and does not exist:**

* no Phase 2B deliverable — zero CSV, zero figure, zero report
* no recommendation matrix, no ranking, no comparison table in final form
* no conclusion about M1 / M3 / H1 was drawn, written or reported
* no revision or confirmation of the Phase 2 decision was produced

A single console dump of selected raw numbers was inspected during that run.
Those numbers were **not** interpreted, and no decision was taken from them.

**Interpretation for block execution:** the expensive raw computation is
already banked and need not be repeated. The remaining work is purely
**presentation and reasoning** — reading `deep_metrics.json`, emitting the CSVs
and figures, and writing the report. That is cheap and decomposes cleanly.

---

## 7. Specification preserved

The Phase 2B methodological specification is **unchanged**. All ex-ante choices
are fixed inside `deep_audit.py` and were set before any metric was read:

| parameter | value |
|---|---|
| Resolutions | M1, M3, H1 only |
| Volatility windows | 60 / 240 / 1440 wall-clock minutes (same horizon at each resolution) |
| UTC windows | 00–06, 06–12, 12–16, 16–21, 21–24 (time windows only, no actor attribution) |
| Shock rule | \|log return\| > 3 × trailing rolling σ over the previous 1440 min, past data only |
| Hurst lags | 2, 4, 8, 16, 32, 64 bars; two estimators; window sensitivity checked |
| Cost scenarios | 0.05 / 0.10 / 0.25 / 0.50 / 1.00 USD — **hypothetical** |
| Cost domination | 0.5 / 1 / 2 / 5 / 10 / 20 % of P50, P75, P90, P95 |
| Volatility classes | HIGH_VOL if trailing 1440-min σ > trailing 1-year mean of that σ (past-only) |

Standing constraints honoured throughout: no volume (L1), no gap filling (L2),
no decimal homogenisation (L3), 2013 break preserved (L4), 2026 excluded from
selection (L5), no outlier removal (L6), sources untouched (L7).
`BROKER_COST_STATUS = EXTERNAL_INPUT_REQUIRED`.

---

## 8. Proposed block decomposition

Each block is intended to be short, independently verifiable, and to end with
a checkable output.

| block | content | output |
|---|---|---|
| 0 | Write `render_2b.py` (reads `deep_metrics.json` only, no recomputation) | script |
| 1 | Amplitude + microstructure-proxy tables | `XAUUSD_M1_M3_MICROSTRUCTURE_PROXIES.csv`, `XAUUSD_M1_M3_AMPLITUDE_COST.csv`, figures `m1_vs_m3_amplitude`, `m1_vs_m3_noise_proxies`, `amplitude_cost_m1_m3` |
| 2 | H1 persistence, continuity, shocks | `XAUUSD_H1_PERSISTENCE_ANALYSIS.csv`, `XAUUSD_CONTINUITY_COMPARISON.csv`, `XAUUSD_EXTREME_SHOCK_ANALYSIS.csv`, figures `h1_persistence_by_volatility`, `shock_preservation_m1_m3_h1` |
| 3 | Discrimination test + recommendation matrix | `XAUUSD_GRANULARITY_RECOMMENDATION.csv` |
| 4 | Report sections 1–11 | draft of `XAUUSD_DEEP_GRANULARITY_AUDIT.md` |
| 5 | Report sections 12–22 + final gate | report complete |
| 6 | Final gate verification + commit | commit `PHASE_2B` |

---

## 9. Outstanding items carried over

| item | state |
|---|---|
| `PHASE2_EXECUTION_DIAGNOSTIC.md` (RECOVERY mission) | **never created** — that mission was interrupted before its deliverable. Its findings are captured in `/tmp/xauusd_audit/phase2_execution_diagnostic.log` (root cause: the script named in the mission, `audit_timeframes.py`, does not exist; the file is `analyze_timeframes.py`; secondarily, bare `python` resolves to `/usr/bin/python`, which lacks numpy/pandas/pyarrow). |
| `deep_audit.py` | untracked, uncommitted |
| `deep_metrics.json` | present in `/tmp`, outside the repository |

---

```
STATUS = READY_FOR_BLOCK_EXECUTION
```

Frozen. Nothing further executed, computed or modified.
