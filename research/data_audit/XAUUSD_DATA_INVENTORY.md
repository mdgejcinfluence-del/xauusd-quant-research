# XAUUSD — DATA INVENTORY (PHASE 1)

**Module:** DATA INGESTION / PROVENANCE / INTEGRITY AUDIT  
**Generated (UTC):** 2026-09-06T08:35:36+00:00  
**Repository:** `/home/user/xauusd-quant-research`  
**Project:** XAUUSD M1 — clean restart (no EURUSD conclusion imported)  
**Phase status:** PRE-REGIME — audit only. No master-dataset build, no timeframe, no regime, no strategy, no performance.

---

## 1. Exact inventory of the 7 fragments

| # | path | name | size (bytes) | size | SHA-256 | present | readable | declared ext | opens as Parquet | real detected type | first bytes | last bytes |
|---|------|------|--------------|------|---------|---------|----------|--------------|------------------|--------------------|-------------|------------|
| 1 | `XAUUSD_part_01.parquet.part` | `XAUUSD_part_01.parquet.part` | 20,971,520 | 20.00 MiB | `f5c96c8c368960a4f0112dfea8a5e9aca32a7bf35bafd15243295857b508f1fc` | YES | YES | .parquet.part | NO | Parquet byte-stream HEAD (magic PAR1, footer absent) | `PAR1` | `e009006a0de81e68` · no magic |
| 2 | `XAUUSD_part_02.parquet.part` | `XAUUSD_part_02.parquet.part` | 20,971,520 | 20.00 MiB | `0dadfdf6cf847c9145b8d9219b9ebdb2e3e573ebec603450a7a9e56f5620f0b5` | YES | YES | .parquet.part | NO | raw Parquet continuation bytes (no magic at offset 0) | `0900652d08d1c81e` · no magic | `00264d1800260948` · no magic |
| 3 | `XAUUSD_part_03.parquet.part` | `XAUUSD_part_03.parquet.part` | 20,971,520 | 20.00 MiB | `4c6fee93d8475a156e66d68c7247e3fbd3c93a467efe1e0dcc5aff3219e44da8` | YES | YES | .parquet.part | NO | raw Parquet continuation bytes (no magic at offset 0) | `04a1266d18002649` · no magic | `01081038b0db052e` · no magic |
| 4 | `XAUUSD_part_04.parquet.part` | `XAUUSD_part_04.parquet.part` | 20,971,520 | 20.00 MiB | `8e0dcbb9f909b94b070df563f3f2832221fd5d09f61f8688ceae54703ac5966d` | YES | YES | .parquet.part | NO | raw Parquet continuation bytes (no magic at offset 0) | `61e808f7d3130108` · no magic | `df4f8d2794409a99` · no magic |
| 5 | `XAUUSD_part_05.parquet.part` | `XAUUSD_part_05.parquet.part` | 20,971,520 | 20.00 MiB | `6a86c02286b9bab4b0cdeda797779c97cd0cf027514b5215223f8de2044e2024` | YES | YES | .parquet.part | NO | raw Parquet continuation bytes (no magic at offset 0) | `9999192994407b14` · no magic | `01080c68c82b5801` · no magic |
| 6 | `XAUUSD_part_06.parquet.part` | `XAUUSD_part_06.parquet.part` | 20,971,520 | 20.00 MiB | `4798294afe5e38ffc773f179e963af695e6be63717748235b1736f725e4b5640` | YES | YES | .parquet.part | NO | raw Parquet continuation bytes (no magic at offset 0) | `080cc00f24660108` · no magic | `08f0810008b1b916` · no magic |
| 7 | `XAUUSD_part_07.parquet.part` | `XAUUSD_part_07.parquet.part` | 14,363,472 | 13.70 MiB | `13bf888a1ca5956ed44ada61e5e70eea9ff47ef0e6635382b9187f974c587b93` | YES | YES | .parquet.part | metadata only | Parquet byte-stream TAIL (footer PAR1, head magic absent) | `01080c00f9b12401` · no magic | `PAR1` |

- fragments expected: **7**  
- fragments present: **7**  
- fragments missing: **0**  
- total bytes: **140,192,592** (133.70 MiB)

> **Rule applied:** no file is assumed to be Parquet because its name contains `.parquet.part`. Only **fragment 01** carries the Parquet magic `PAR1` at offset 0; only **fragment 07** carries the Parquet footer (`PAR1` + 4-byte footer length). Fragments 02–06 are raw continuation bytes with no identifiable magic. Type detection is done on the bytes, never on the filename.

### 1.1 Why no fragment can be used alone

| # | fragment | opens as Parquet | rows decodable alone | detail |
|---|---|---|---|---|
| 1 | XAUUSD_part_01.parquet.part | NO | NO | ArrowInvalid: Could not open Parquet input source '/home/user/xauusd-quant-research/XAUUSD_part_01.parquet.part': Parque |
| 2 | XAUUSD_part_02.parquet.part | NO | NO | ArrowInvalid: Could not open Parquet input source '/home/user/xauusd-quant-research/XAUUSD_part_02.parquet.part': Parque |
| 3 | XAUUSD_part_03.parquet.part | NO | NO | ArrowInvalid: Could not open Parquet input source '/home/user/xauusd-quant-research/XAUUSD_part_03.parquet.part': Parque |
| 4 | XAUUSD_part_04.parquet.part | NO | NO | ArrowInvalid: Could not open Parquet input source '/home/user/xauusd-quant-research/XAUUSD_part_04.parquet.part': Parque |
| 5 | XAUUSD_part_05.parquet.part | NO | NO | ArrowInvalid: Could not open Parquet input source '/home/user/xauusd-quant-research/XAUUSD_part_05.parquet.part': Parque |
| 6 | XAUUSD_part_06.parquet.part | NO | NO | ArrowInvalid: Could not open Parquet input source '/home/user/xauusd-quant-research/XAUUSD_part_06.parquet.part': Parque |
| 7 | XAUUSD_part_07.parquet.part | YES (footer only) | NO | OSError: Invalid column metadata (corrupt file?) |

Fragment 07 is the only one whose footer parses (it carries the real Parquet footer), but its data pages live in fragments 01–06, so decoding fails: the file is one single byte stream cut into 7 pieces.

---

## 2. Format inspection (how the file was cut)

| observation | value |
|---|---|
| fragment sizes | 20,971,520, 20,971,520, 20,971,520, 20,971,520, 20,971,520, 20,971,520, 14,363,472 |
| constant chunk size | True (20,971,520 bytes = 20.00 MiB) |
| remainder fragment | 14,363,472 bytes (13.70 MiB) |
| first bytes of part_01 | `5041523115041580` → `PAR1` |
| last bytes of part_07 | `f51a000050415231` → footer length 6,901 B + `PAR1` |

**Conclusion — split signature:** 6 fragments of *exactly* 20.00 MiB (20,971,520 B) plus one remainder of 14,363,472 B. This is the exact output signature of a fixed-size binary split (`split -b 20M` or an equivalent chunked uploader). It is **not** a Parquet dataset split into several Parquet files, and **not** a split with per-fragment headers or metadata: there is no header, no manifest, no index and no padding anywhere in the stream.

| risk assessed | verdict | evidence |
|---|---|---|
| per-fragment headers / metadata | **NONE** | fragments 02–06 start mid-stream with no magic; only 01 starts with `PAR1` |
| padding / trailing bytes | **NONE** | sum of the 7 sizes = reassembled size = 140,192,592 B; 0 trailing byte after re-split |
| corruption at a seam | **NOT DETECTED** | every one of the 36 column chunks parses with exact byte accounting (§4) |
| Parquet compatibility after reassembly | **YES** | footer parses, format v2.6, 5,874,003 rows, 6 row groups |
| concatenation method required | **plain byte-exact sequential concatenation in filename order** — no transformation |

---

## 3. Non-destructive reconstruction (working copy only)

| item | value |
|---|---|
| method | byte-exact sequential concatenation (cat part_01 .. part_07) |
| working copy (outside the repository) | `/tmp/xauusd_audit/XAUUSD_M1_reconstructed.parquet` |
| bytes written | 140,192,592 |
| sum of fragment bytes | 140,192,592 |
| size match | **True** |
| SHA-256 of reassembly | `fdce55a8c8a76c417765ad020794866bb36e5b166c130d2bb4deb2aeeeab91d0` |
| SHA-256 on second read (determinism) | `fdce55a8c8a76c417765ad020794866bb36e5b166c130d2bb4deb2aeeeab91d0` → **True** |
| head / tail magic | `PAR1` / `PAR1` |
| Parquet footer | 6,901 B + 8 B magic = 6,909 B |
| Parquet parses | **True** |
| created_by | `parquet-cpp-arrow version 18.1.0` |
| rows / row groups / columns | 5,874,003 / 6 / 6 |
| full decode of every value | **5,874,003 rows × 6 columns** |

### 3.1 Re-split proof (no byte missing, none duplicated)

The reassembled file was cut again at exactly the same offsets; each resulting block was hashed and compared with the original fragment:

| fragment | result | original SHA-256 (first 32) | re-split SHA-256 (first 32) |
|---|---|---|---|
| 1 | MATCH | f5c96c8c368960a4f0112dfea8a5e9ac… | f5c96c8c368960a4f0112dfea8a5e9ac… |
| 2 | MATCH | 0dadfdf6cf847c9145b8d9219b9ebdb2… | 0dadfdf6cf847c9145b8d9219b9ebdb2… |
| 3 | MATCH | 4c6fee93d8475a156e66d68c7247e3fb… | 4c6fee93d8475a156e66d68c7247e3fb… |
| 4 | MATCH | 8e0dcbb9f909b94b070df563f3f28322… | 8e0dcbb9f909b94b070df563f3f28322… |
| 5 | MATCH | 6a86c02286b9bab4b0cdeda797779c97… | 6a86c02286b9bab4b0cdeda797779c97… |
| 6 | MATCH | 4798294afe5e38ffc773f179e963af69… | 4798294afe5e38ffc773f179e963af69… |
| 7 | MATCH | 13bf888a1ca5956ed44ada61e5e70eea… | 13bf888a1ca5956ed44ada61e5e70eea… |

- all 7 hashes identical: **True**  
- trailing bytes after the 7th block: **0**

### 3.2 Source integrity

SHA-256 of the 7 source fragments re-computed **after** the audit: identical to the pre-audit hashes → **True**.  
No source file was written, moved, renamed or deleted at any point.

---

## 4. Physical layout and seam map

| row group | rows | first row (0-based) | last row | bytes |
|---|---|---|---|---|
| RG0 | 1,048,576 | 0 | 1,048,575 | 42,938,868 |
| RG1 | 1,048,576 | 1,048,576 | 2,097,151 | 42,578,475 |
| RG2 | 1,048,576 | 2,097,152 | 3,145,727 | 23,859,549 |
| RG3 | 1,048,576 | 3,145,728 | 4,194,303 | 32,979,443 |
| RG4 | 1,048,576 | 4,194,304 | 5,242,879 | 37,096,970 |
| RG5 | 631,123 | 5,242,880 | 5,874,002 | 23,364,499 |

Every column chunk of every row group was scanned page by page (Parquet page headers, thrift compact protocol). For all 36 chunks the bytes consumed by page headers + payloads equal the declared compressed size, and the number of values recovered equals the declared row count:

**page-level byte accounting consistent: True**

Any missing, duplicated or reordered byte would break this accounting or the thrift page-header parse.

| seam | byte offset | cut row group | cut column | cut page | rows in cut page | estimated row index |
|---|---|---|---|---|---|---|
| 01->02 | 20,971,520 | RG0 | `low` | #6 (DATA_PAGE) | 131,072 | 891,264 |
| 02->03 | 41,943,040 | RG1 | `high` | #2 (DATA_PAGE) | 131,072 | 1,357,867 |
| 03->04 | 62,914,560 | RG2 | `timestamp` | #8 (DATA_PAGE) | 131,072 | 3,129,553 |
| 04->05 | 83,886,080 | RG3 | `open` | #0 (DICTIONARY_PAGE) | 0 | 3,145,728 |
| 05->06 | 104,857,600 | RG4 | `timestamp` | #6 (DATA_PAGE) | 131,072 | 4,959,155 |
| 06->07 | 125,829,120 | RG5 | `timestamp` | #3 (DATA_PAGE) | 131,072 | 5,531,342 |

---

## 5. Reproduction

```bash
python3 -m venv .venv && ./.venv/bin/pip install pandas pyarrow numpy
./.venv/bin/python research/data_audit/scripts/audit_xauusd_phase1.py \
        --repo . --workdir /tmp/xauusd_audit
./.venv/bin/python research/data_audit/scripts/render_reports.py \
        --metrics /tmp/xauusd_audit/metrics.json \
        --outdir research/data_audit
```

Scripts: `parquet_pagemap.py` (page-header scanner), `audit_xauusd_phase1.py` (measurement), `render_reports.py` (rendering of the three deliverables).

