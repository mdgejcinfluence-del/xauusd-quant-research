import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import pytest
from ere.intake import qualify_dossier

RAW = {"trades":[
  {"instrument":"XAUUSD","side":"buy","open_time":"2026-01-05T10:00:00","close_time":"2026-01-05T10:20:00","open_price":2000.0,"close_price":2001.0,"volume":0.01,"timezone":"UTC","source_ref":"capture-1"},
  {"instrument":"XAUUSD","side":"buy","open_time":"2026-01-05T10:00:00","close_time":"2026-01-05T10:20:00","open_price":2000.0,"close_price":2001.0,"volume":0.01,"timezone":"UTC","source_ref":"capture-1"},
  {"instrument":"XAUUSD","side":"buy","open_time":"2026-01-05T10:05:00","close_time":None,"open_price":1999.0,"close_price":None,"volume":0.01,"timezone":None,"source_ref":None}],
  "claims":[{"texte":"+2000% annoncé"}], "missing_information":[]}

def test_qualify_dedup_missing_and_b_ready():
    d, r = qualify_dossier(RAW)
    assert r.accepted and r.n_trades == 2 and len(r.duplicates_removed) == 1
    assert r.missing_by_field["close_price"] == 1 and r.timezone_status == "PARTIEL"
    assert r.provenance_complete is False and r.b_ready is True
    assert d.claims[0]["verified"] is False

def test_empty_dossier_rejected():
    with pytest.raises(ValueError): qualify_dossier({"trades":[]})

def test_b_blocked_without_side():
    raw = {"trades":[{"instrument":"XAUUSD","side":None,"open_time":"t0","source_ref":"s"}]}
    d, r = qualify_dossier(raw)
    assert r.b_ready is False and any("side" in b for b in r.b_blockers)

def test_regression_same_size_same_times_different_profit_stay_distinct():
    raw = {"trades":[
      {"instrument":"XAUUSDr","side":"buy","open_time":"2026-11-27 04:05:31","close_time":"2026-11-27 04:05:45","volume":0.08,"result":53.12,"source_ref":"ligne5"},
      {"instrument":"XAUUSDr","side":"buy","open_time":"2026-11-27 04:05:31","close_time":"2026-11-27 04:05:45","volume":0.08,"result":45.12,"source_ref":"ligne6"}]}
    d, r = qualify_dossier(raw)
    assert r.n_trades == 2 and r.duplicates_removed == []

def test_regression_different_position_ids_stay_distinct():
    raw = {"trades":[
      {"instrument":"XAUUSD","side":"buy","open_time":"t0","volume":0.1,"result":1.0,"position_id":"A1","source_ref":"s"},
      {"instrument":"XAUUSD","side":"buy","open_time":"t0","volume":0.1,"result":1.0,"position_id":"B2","source_ref":"s"}]}
    d, r = qualify_dossier(raw)
    assert r.n_trades == 2

def test_true_duplicate_detected_and_raw_preserved():
    t = {"instrument":"XAUUSD","side":"buy","open_time":"t0","close_time":"t1","volume":0.1,"result":2.0,"source_ref":"s"}
    raw = {"trades":[dict(t), dict(t)]}
    d, r = qualify_dossier(raw)
    assert r.n_trades == 1 and len(r.duplicates_removed) == 1 and len(raw["trades"]) == 2

def test_episodes_traceable_to_sources():
    from ere.intake import build_episodes
    eps = build_episodes(RAW["trades"])
    assert len(eps) == 2 and eps[0]["n_positions"] == 2 and eps[1]["n_positions"] == 1
    # tracabilite complete verifiee sur le dossier reel TRADER-CANDIDATE-002
    import json, pathlib
    reel = json.loads((pathlib.Path(__file__).resolve().parents[1] / "docs/checkpoints/TRADER_CANDIDATE_002/dossier_brut.json").read_text())
    eps_r = build_episodes(reel["trades"])
    assert len(eps_r) == 3 and all(e["n_positions"] == 2 for e in eps_r)
    assert all(all(e["source_refs"]) for e in eps_r)
    assert eps[0]["lot_total"] == pytest.approx(0.02)
