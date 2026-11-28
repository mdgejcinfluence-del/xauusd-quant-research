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
