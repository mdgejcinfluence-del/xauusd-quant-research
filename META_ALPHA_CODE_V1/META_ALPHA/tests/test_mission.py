"""Le contrat de mission est-il cohérent ?

Ces tests protègent l'architecture contre elle-même : un artéfact produit par
deux phases, une phase sans gate, une phase qui n'exige pas le propriétaire
alors qu'elle devrait — tout cela doit casser le build, pas apparaître dans un
schéma.
"""
from __future__ import annotations

import pytest

from metaalpha.mission import (
    BG_HOLD_MIN_MINUTES, BG_NOT_PUBLIC, BG_REPORTED_RULES, CHAIN, LAYERS, NEVER_AUTOMATED,
    PHASES, PHASE_INDEX, TICK_LIMITS, all_artifacts, duplicate_artifacts,
    human_decisions, phases_by_layer, stats,
)


def test_phase_order_is_contiguous():
    ranks = [p.rank for p in PHASES]
    assert ranks == list(range(len(PHASES)))


def test_no_duplicate_artifacts():
    assert duplicate_artifacts() == {}


def test_every_phase_has_both_gates():
    for p in PHASES:
        assert p.entry_gate, p.phase_id
        assert p.exit_gate, p.phase_id
        assert p.on_failure, p.phase_id


def test_historical_phases_are_never_rebuilt():
    for pid in ("P1_CERTIFIED", "P2H_CERTIFIED"):
        p = PHASE_INDEX[pid]
        assert p.automated, pid
        joined = " ".join(p.forbidden).lower()
        assert "reconstruire" in joined or "re-télécharger" in joined


def test_both_historical_certificates_are_read_only():
    arts = all_artifacts()
    assert "04_CHECKPOINTS/PHASE_01_XAUUSD_PRIMARY_CERTIFIED.json" in arts
    assert "04_CHECKPOINTS/PHASE_02_DGP_BASE_CHRONOLOGICAL_VALIDATED_V5R10.json" in arts


def test_analytical_phase_is_distinct_from_certified_dgp():
    assert "P2_ANALYTICAL" in PHASE_INDEX
    assert "P2H_CERTIFIED" in PHASE_INDEX
    assert PHASE_INDEX["P2_ANALYTICAL"].rank > PHASE_INDEX["P2H_CERTIFIED"].rank


def test_holdout_requires_explicit_owner_authorization():
    p = PHASE_INDEX["P8_HOLDOUT"]
    assert p.produces_human_decision
    assert any("AUTORISER" in h for h in p.human_only)
    assert "explicite" in p.entry_gate.lower()


def test_deployment_is_distinct_from_holdout_authorization():
    p9 = PHASE_INDEX["P9_MQL5"]
    assert any("déploiement réel" in h for h in p9.human_only)
    assert "distinct" in " ".join(p9.human_only).lower()


def test_nine_decisions_belong_to_the_analytical_phase():
    p = PHASE_INDEX["P2_ANALYTICAL"]
    assert any("9 décisions" in h for h in p.human_only)


def test_three_layers_map_to_disjoint_phase_sets():
    sets = {l["id"]: {p.phase_id for p in phases_by_layer(l["id"])} for l in LAYERS}
    assert sets["A"] and sets["B"] and sets["C"]
    assert not (sets["A"] & sets["B"]) and not (sets["B"] & sets["C"])


def test_layer_c_comes_after_rate_freeze():
    # le challenge ne peut pas influencer la recherche : C est après B
    max_b = max(p.rank for p in phases_by_layer("B"))
    min_c = min(p.rank for p in phases_by_layer("C"))
    assert min_c > max_b


def test_two_minute_rule_is_blocking():
    assert BG_HOLD_MIN_MINUTES == 2
    rule = next(r for r in BG_REPORTED_RULES if "Durée minimale" in r["rule"])
    assert rule["status"].startswith("BLOQUANT")


def test_hft_and_tick_scalping_forbidden():
    rule = next(r for r in BG_REPORTED_RULES if "HFT" in r["rule"])
    assert "interdit" in rule["value"]


def test_drawdown_contradiction_is_not_resolved_by_guess():
    rule = next(r for r in BG_REPORTED_RULES if "Drawdown" in r["rule"])
    assert rule["status"] == "CONTRADICTION_DOCUMENTAIRE"


def test_server_parameters_stay_not_public():
    assert len(BG_NOT_PUBLIC) >= 15
    for key in ("tick size", "tick value", "volume step", "freeze level", "stops level"):
        assert key in BG_NOT_PUBLIC


def test_tick_limits_never_claim_volume_or_depth():
    claims = {t["claim"]: t["status"] for t in TICK_LIMITS}
    assert claims["volume réellement échangé"] == "UNAVAILABLE"
    assert claims["delta acheteur/vendeur"] == "UNAVAILABLE"
    assert claims["coûts complets réels"] == "DEFERRED_EXTERNAL_DEPENDENCY"


def test_never_automated_covers_the_eight_prohibitions():
    assert len(NEVER_AUTOMATED) == 8
    joined = " ".join(NEVER_AUTOMATED).lower()
    for frag in ("formule", "paramètre", "négatif", "holdout", "certificat",
                 "serveur", "réel", "phase"):
        assert frag in joined


def test_chain_starts_at_ticks_and_ends_at_robot():
    assert CHAIN[0] == "TICKS NATIFS BID/ASK"
    assert CHAIN[-1] == "ROBOT"
    assert CHAIN.index("EDGES QUALIFIÉS") < CHAIN.index("PORTEFEUILLE META-ALPHA")
    assert CHAIN.index("PORTEFEUILLE META-ALPHA") < CHAIN.index("ADAPTATEUR BLUE GUARDIAN")


def test_no_edge_is_a_valid_outcome():
    p = PHASE_INDEX["P6_QUALIFICATION"]
    assert "NO_EDGE" in p.on_failure
    assert "NO_EDGE" in PHASE_INDEX["P7_PORTFOLIO"].on_failure


def test_stats_are_consistent():
    s = stats()
    assert s["phases_total"] == len(PHASES)
    assert s["phases_to_execute"] + s["phases_certified_not_to_rebuild"] == s["phases_total"]
    assert s["human_decisions_total"] == len(human_decisions())
    assert s["duplicate_artifacts"] == {}
