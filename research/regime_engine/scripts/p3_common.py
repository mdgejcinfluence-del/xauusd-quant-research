#!/usr/bin/env python3
"""
PHASE 3 (XAUUSD regime discovery) - shared constants and helpers.

RECONSTRUCTION / RECOVERY STATE (2026-09-06):
  * The workspace reset of 2026-09-06 destroyed the original p3_common.py
    and every other Phase-3 source file. The file below was re-created.
  * ONLY constants with an EXACT, AUDITABLE source are present:
      - committed project sources (Phase 1 / Phase 2B in this repository),
      - the surviving `scripts/15_feature_pit_audit.py`,
      - the validated Step-1 PIT definitions recorded in session evidence.
  * Every constant carries its PROVENANCE. Constants whose exact value is
    NOT recoverable are listed in MISSING_CONSTANTS and are deliberately
    ABSENT from this module (no guesses, per standing instruction
    "NE PAS inventer les constantes").

FROZEN PROJECT DECISIONS (from the mission + Phase 1/2B, not re-derived):
  * hierarchy          : PRIMARY = M3, SUBSTRATE = M1, CONTEXT = H1 (Phase 2B)
  * timezone           : UTC throughout; epoch origin 1970-01-01T00:00:00Z
  * alignment          : bar_id = floor(epoch_minutes / k)
  * volume             : NEVER loaded, never used, never derived (Phase 1 L1)
  * gaps               : never padded, never interpolated, never invented (L2)
  * extremes           : never deleted from the master (L6)
  * 2026               : partial year, sanity check only (L5)
"""
from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone

# --------------------------------------------------------------------------- #
# Paths (scratch data lives OUTSIDE the repository; reports + CSV are committed)
# --------------------------------------------------------------------------- #
REPO = "/home/user/xauusd-quant-research"
OUT = os.path.join(REPO, "research", "regime_engine")
SCRATCH = "/tmp/xauusd_audit/regime_engine"
MASTER = "/tmp/xauusd_audit/XAUUSD_M1_reconstructed.parquet"

# PROVENANCE: Phase 1 inventory + Phase 2B Block A/C + precheck, and re-verified
# byte-for-byte on the 2026-09-06 reconstruction (cat of the 7 fragments).
MASTER_SHA = "fdce55a8c8a76c417765ad020794866bb36e5b166c130d2bb4deb2aeeeab91d0"
MASTER_ROWS = 5_874_003          # PROVENANCE: Phase 2B Block A §"Bars"

# --------------------------------------------------------------------------- #
# Hierarchy (PROVENANCE: mission "M3 primary / H1 context / M1 substrate")
# --------------------------------------------------------------------------- #
PRIMARY_MIN = 3                 # M3
CONTEXT_MIN = 60                # H1

# --------------------------------------------------------------------------- #
# Market break threshold (PROVENANCE: build_timeframes.py, committed, exact)
# --------------------------------------------------------------------------- #
MARKET_BREAK_MIN = 50           # >= 50 min gap = daily rollover / weekend closure

# --------------------------------------------------------------------------- #
# Shock / extreme rule (PROVENANCE: Phase 2B Block A + Block B + Block C,
# committed: "|log return of one bar| > 3 x trailing rolling sigma of the same
# series over the previous 1440 wall-clock minutes, past-only",
# implementation "std over round(1440/k) bars: M1 1440, M3 480, H1 24").
# NOTE: the Phase-3 flags `m1_ext` / `r3_ext` in the LOST features.parquet are
# EXPECTED to be these flags; their Phase-3 adoption is NOT independently
# auditable -> listed under MISSING_CONSTANTS as *pending confirmation*.
# --------------------------------------------------------------------------- #
SHOCK_MULT = 3.0
SHOCK_WALL_MIN = 1440           # wall-clock minutes, past-only
SHOCK_WINDOW_BARS = {1: 1440, 3: 480, 60: 24}   # round(1440/k)

# --------------------------------------------------------------------------- #
# Volatility windows used by Phase 2B (PROVENANCE: Block A/B, committed:
# "60 / 240 / 1440 wall-clock minutes (implemented as W/k bars)")
# NOTE: whether Phase 3 feature windows are exactly this set is NOT
# independently confirmed -> listed under MISSING_CONSTANTS.
# --------------------------------------------------------------------------- #
W_VOL_PHASE2B_MIN = (60, 240, 1440)

# --------------------------------------------------------------------------- #
# PIT normalization (PROVENANCE: Step-1/Step-2A session evidence + the
# surviving audit script):
#   Z_SCALE = 1.4826  : MAD -> sigma consistent scale (session evidence)
#   Z_CLIP  = 6.0     : literal constant in scripts/15_feature_pit_audit.py
# The normalization WINDOW (minutes) is NOT recoverable -> MISSING_CONSTANTS.
# --------------------------------------------------------------------------- #
Z_SCALE = 1.4826
Z_CLIP = 6.0

# --------------------------------------------------------------------------- #
# Constants that CANNOT be recovered from any available source.
# They must be re-supplied by the user (or another external backup) before the
# 31-feature dataset can be rebuilt. They are intentionally NOT defined here.
# --------------------------------------------------------------------------- #
MISSING_CONSTANTS = {
    "features_kept": "the exact list of the 31 kept feature names (only C3_recovery50_1440 and "
                     "D5_breakout_persist are recorded in session evidence)",
    "feature_definitions_29": "definitions/formulas/windows of the 29 other features "
                              "(families A-G not enumerated anywhere recoverable)",
    "feature_windows": "per-feature window lengths (min) - Phase-2B 60/240/1440 set is only a "
                       "related reference, not proof of Phase-3 values",
    "min_obs": "per-feature MIN_OBS thresholds (e.g. D2 fix 20->6, h1_vol 16->12 are recorded "
               "in session evidence but not the full map)",
    "z_window": "normalization rolling window (minutes) for causal median/MAD",
    "k_grid_seeds": "K_GRID, SEEDS, SEEDS_HMM (only 'K2-6 on separation/stability/...' and "
                    "seed-0/1/2/3/4 usage patterns are mission-level constraints)",
    "rule_bands": "RULE_Z_BANDS (a [-1,1,2]-like structure is mission-level only, values not "
                  "recoverable)",
    "m3_extreme_rule_p3": "Phase-3 M3 extreme flag threshold (Phase-2B 3-sigma rule is "
                          "a reference, Phase-3 flag not independently auditable)",
    "feature_meta_schema": "feature_meta.json exact structure (key 'features_kept' is confirmed "
                           "by 15_feature_pit_audit.py; other fields unknown)",
    "c3_d5_micro_details": "C3/D5: trigger strictness, 'move' definition, eligible/outcome "
                           "encodings, MIN_OBS for the rolling-1440 ratio (algorithm skeleton "
                           "is recorded; micro-details are not)",
}

# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def save_json(obj: dict, path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as fh:
        json.dump(obj, fh, indent=2)


def review_header() -> dict:
    """Preamble object (used by reports; free of any invented parameter)."""
    return {
        "program": "XAUUSD_REGIME_DISCOVERY_PHASE3",
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "asset": "XAUUSD (gold spot, USD/oz nominal as delivered)",
        "primary_timeframe": "M3",
        "substrate": "M1",
        "context": "H1",
        "volume_used": "NO (Phase 1 L1)",
        "gap_policy": "none - no window padded, no bar invented, no interpolation",
        "timezone": "UTC",
        "epoch_origin": "1970-01-01T00:00:00Z",
        "bar_alignment": "bar_id = floor(epoch_minutes / k)",
        "master_sha256": MASTER_SHA,
        "master_rows": MASTER_ROWS,
        "recovery_status": "STEP2A_RECOVERY / BLOCKED (31-feature dataset not rebuildable: "
                           "constants missing - see MISSING_CONSTANTS)",
        "strategy_or_backtest": "NONE",
        "performance_metrics": "NONE",
        "eurusd_inheritance": "NONE",
    }
