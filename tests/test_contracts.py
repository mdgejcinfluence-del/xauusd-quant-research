import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import pytest
from ere.taxonomy import EvidenceLevel, check_promotion, aggregate_level
from ere.contracts import (Envelope, TraderDossier, MarketWindow, HypothesisSet,
    AvisDeTestabilite, ExperimentPlan, SignatureReport, ModelDossier, ValidationVerdict)

def env(prod, lvl): return Envelope("o1", prod, lvl)

def test_promotion_authority():
    check_promotion("F", EvidenceLevel.N4_SIGNATURE_MESUREE)
    check_promotion("G", EvidenceLevel.N6_MECANISME_IDENTIFIE)
    with pytest.raises(ValueError): check_promotion("F", EvidenceLevel.N5_MECANISME_ETAYE)
    with pytest.raises(ValueError): check_promotion("H", EvidenceLevel.N7_AVANTAGE_VALIDE)

def test_aggregate_takes_min():
    assert aggregate_level([EvidenceLevel.N4_SIGNATURE_MESUREE, EvidenceLevel.N0_SOURCE_NON_VERIFIEE]) == EvidenceLevel.N0_SOURCE_NON_VERIFIEE

def test_claim_cannot_be_verified_at_ingestion():
    d = TraderDossier(env("A", EvidenceLevel.N0_SOURCE_NON_VERIFIEE), trades=[], claims=[{"texte":"+2000%","verified":True}], missing_information=[], selection_process="inconnu")
    with pytest.raises(ValueError): d.validate()

def test_market_window_capped_n2():
    w = MarketWindow(env("B", EvidenceLevel.N3_HYPOTHESE), "d1","t1","corpus","2026-01-01T00:00Z","2026-01-01T01:00Z","couvrir detention",["bid","ask"],{})
    with pytest.raises(ValueError): w.validate()

def test_posterior_requires_likelihood():
    h = HypothesisSet(env("C", EvidenceLevel.N3_HYPOTHESE), "b1", [{"hypothesis_id":"h1","posterior":0.5},{"hypothesis_id":"h2"}])
    with pytest.raises(ValueError): h.validate()

def test_not_executed_carries_no_numbers():
    r = SignatureReport(env("F", EvidenceLevel.N4_SIGNATURE_MESUREE), "p1","run1","NOT_EXECUTED",{"x":1},"découverte",{"spread_bp":[1,2]})
    with pytest.raises(ValueError): r.validate()

def test_g_rejects_unlisted_input_and_gate_h_needs_n5():
    m = ModelDossier(env("G", EvidenceLevel.N4_SIGNATURE_MESUREE), [("StatistiquePublique","s1","x"*64)], "COMPATIBLE MAIS NON IDENTIFIÉ", [],[],[])
    with pytest.raises(ValueError): m.validate()
    m2 = ModelDossier(env("G", EvidenceLevel.N4_SIGNATURE_MESUREE), [("SignatureReport","s1","x"*64)], "COMPATIBLE MAIS NON IDENTIFIÉ", [],[],[], candidat_h=True)
    with pytest.raises(ValueError): m2.validate()

def test_positive_verdict_requires_numbers():
    v = ValidationVerdict(env("I-A", EvidenceLevel.N4_SIGNATURE_MESUREE), "e1", "VALIDATION RÉUSSIE", None, {"critere":1})
    with pytest.raises(ValueError): v.validate()

def test_plan_hash_detects_tampering():
    p = ExperimentPlan(env("E", EvidenceLevel.N3_HYPOTHESE), ["h1"], {"seuil":5}, "découverte", AvisDeTestabilite("TESTABLE","ok"))
    p.validate(); p.protocole["seuil"] = 99
    with pytest.raises(ValueError): p.validate()
