"""Le système AGIT : familles instanciées depuis le dossier, questions extraites,
variables créées dès que le propriétaire répond. Aucune décision inventée.
"""
from __future__ import annotations

import json
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from metaalpha import registry
from metaalpha.contracts_engine import (
    build_phase2_contract_report,
    derive_sample,
    detect_fields,
    instantiate_families,
)
from metaalpha.decisions import answer_template, load_answers, record_answers
from metaalpha.fs import Storage
from metaalpha.families import FAMILIES, all_decisions, summary


# ------------------------------------------------------------------ schéma
def test_detect_fields_finds_canonical_roles():
    s = detect_fields(["timestamp", "bid", "ask"])
    assert s["canonical"] == {"timestamp": "timestamp", "bid": "bid", "ask": "ask"}
    assert s["has_core_quote_triplet"] is True


def test_detect_fields_handles_aliases():
    s = detect_fields(["TIME", "BidPrice", "Offer"])
    assert s["canonical"]["timestamp"] == "TIME"
    assert s["canonical"]["bid"] == "BidPrice"
    assert s["canonical"]["ask"] == "Offer"


def test_detect_forbidden_fields_is_reported_not_ignored():
    """§4.1 : volume / OHLC ne doivent jamais être utilisés comme s'ils étaient observés."""
    s = detect_fields(["timestamp", "bid", "ask", "volume", "close"])
    assert "volume" in s["forbidden_fields_present"]
    assert "close" in s["forbidden_fields_present"]
    assert s["forbidden_fields_present"]["volume"] == "volume réellement échangé"


# ---------------------------------------------------------------- familles
def test_eight_families_from_dossier():
    assert len(FAMILIES) == 8
    assert [f.number for f in FAMILIES] == list(range(1, 9))


def test_families_summary_corrects_the_19_misreading():
    s = summary()
    assert s["families_total"] == 8
    assert "certificat Phase 2 hérité" in s["legacy_counter_note"]
    assert "pas une liste" in s["legacy_counter_note"]


def test_family_without_parameters_is_available_immediately():
    """F1 (prix/spread) n'a aucun paramètre => le système peut la traiter seul."""
    schema = detect_fields(["timestamp", "bid", "ask"])
    fams = {f["family_id"]: f for f in instantiate_families(schema)}
    f1 = fams["F1_PRIX_COTATIONS"]
    assert f1["status"] == "SPECIFIED"
    assert f1["decisions_open"] == []
    assert all(v["status"] == "DERIVABLE_NOW" for v in f1["variables"])


def test_family_with_free_parameters_is_blocked_not_guessed():
    schema = detect_fields(["timestamp", "bid", "ask"])
    fams = {f["family_id"]: f for f in instantiate_families(schema)}
    f3 = fams["F3_VOLATILITE"]
    assert f3["status"] == "PENDING_OWNER_DECISION"
    assert all(v["status"] == "PENDING_OWNER_DECISION" for v in f3["variables"])
    assert "D_FENETRES_VOL" in f3["decisions_open"]


def test_missing_field_marks_family_unavailable():
    schema = detect_fields(["timestamp"])          # ni bid ni ask
    fams = {f["family_id"]: f for f in instantiate_families(schema)}
    assert fams["F1_PRIX_COTATIONS"]["status"] == "UNAVAILABLE_FIELD"
    assert "bid" in fams["F1_PRIX_COTATIONS"]["reason"]


def test_exactly_nine_decisions_none_has_default():
    ds = all_decisions()
    assert len(ds) == 9
    assert all(d.default_is == "AUCUN_DEFAUT" for d in ds)


# -------------------------------------------------------------- questions
def test_report_extracts_owner_questions_with_consequences():
    schema = detect_fields(["timestamp", "bid", "ask"])
    rep = build_phase2_contract_report(schema=schema)
    qs = rep["questions_for_owner"]
    assert len(qs) == 9
    assert rep["phase_status"] == "BLOCKED_WITH_RESUME"
    assert rep["next_action"]["kind"] == "ANSWER_QUESTIONS_THEN_RESUME"
    for q in qs:
        assert q["why_it_matters"], "chaque question doit expliquer sa conséquence"
        assert q["answer"] is None, "le système ne pré-remplit JAMAIS une réponse"


def test_report_counts_derivable_variables():
    schema = detect_fields(["timestamp", "bid", "ask"])
    rep = build_phase2_contract_report(schema=schema)
    assert "SPREAD_ABS" in rep["variables_derivable_now"]
    assert "SPREAD_REL" in rep["variables_derivable_now"]
    assert "MID" in rep["variables_derivable_now"]
    assert rep["counts"]["variables_derivable_now"] >= 3


def test_deferred_external_families_are_explicit_not_replaced():
    schema = detect_fields(["timestamp", "bid", "ask"])
    rep = build_phase2_contract_report(schema=schema)
    assert len(rep["deferred_external"]) == 8
    assert all(d["replaced_by_proxy"] == "INTERDIT" for d in rep["deferred_external"])


# ------------------------------------------------------------ décisions
def test_ai_cannot_answer_decisions(drive_root: Path):
    s = Storage.open(drive_root)
    with pytest.raises(registry.OwnerAttributionError):
        record_answers(s, {"D_FENETRES_VOL": "500"}, answered_by="LLM")


def test_unknown_decision_rejected(drive_root: Path):
    s = Storage.open(drive_root)
    with pytest.raises(KeyError):
        record_answers(s, {"D_INVENTEE": "42"})


def test_answers_instantiate_variables_immediately(drive_root: Path):
    """Le cœur du 'il doit agir' : répondre crée les registres, sans autre geste."""
    s = Storage.open(drive_root)
    registry.init_registries(s)
    res = record_answers(s, {
        "D_FENETRES_VOL": "500",
        "D_WARMUP_NULL": "NULL",
        "D_SEUIL_SAUT": "4",
    })
    # ZSCORE_ROBUST exige DEUX décisions (fenêtre de retour + seuil) : les deux
    # sont fournies ci-dessus, donc il doit être instancié.
    assert res["answers_recorded"] == 3
    assert "ROLL_STD_MID" in res["variables_instantiated"]
    assert "ROLL_RANGE_MID" in res["variables_instantiated"]
    assert "ZSCORE_ROBUST" in res["variables_instantiated"]

    reg = s.read_json(registry.VARIABLE_REGISTRY_REL)
    key = "ROLL_STD_MID@1"
    assert key in reg["variables"]
    assert reg["variables"][key]["parameters"]["N"] == "500"
    assert reg["variables"][key]["created_by"] == "HUMAN"


def test_unanswered_decision_leaves_variable_blocked(drive_root: Path):
    s = Storage.open(drive_root)
    registry.init_registries(s)
    res = record_answers(s, {"D_FENETRES_VOL": "500"})   # seuil non répondu
    assert "ZSCORE_ROBUST" not in res["variables_instantiated"]


def test_answers_are_persisted_and_reloadable(drive_root: Path):
    s = Storage.open(drive_root)
    record_answers(s, {"D_HORIZON_LABEL": "5min"})
    doc = load_answers(s)
    assert doc["answers"]["D_HORIZON_LABEL"]["answer"] == "5min"
    assert doc["answers"]["D_HORIZON_LABEL"]["answered_by"] == "HUMAN"


def test_answer_template_has_no_prefilled_value():
    tpl = answer_template()
    assert all(v is None for v in tpl["answers"].values())
    assert len(tpl["answers"]) == 9


# ------------------------------------------------------- échantillon réel
@pytest.fixture
def one_partition(tmp_path: Path) -> Path:
    n = 5000
    ts = pa.array([1_600_000_000_000 + j * 150 for j in range(n)], type=pa.timestamp("ms", tz="UTC"))
    bid = pa.array([1900.0 + (j % 89) * 0.01 for j in range(n)], type=pa.float64())
    ask = pa.array([1900.25 + (j % 89) * 0.01 for j in range(n)], type=pa.float64())
    p = tmp_path / "part_000001.parquet"
    pq.write_table(pa.table({"timestamp": ts, "bid": bid, "ask": ask}), p)
    return p


def test_sample_measures_only_parameterless_variables(one_partition: Path):
    schema = detect_fields(["timestamp", "bid", "ask"])
    smp = derive_sample(one_partition, schema, max_events=2000)
    assert smp["status"] == "MEASURED"
    assert smp["events_measured"] == 2000            # borné, jamais tout le corpus
    obs = smp["observed"]
    assert obs["spread_abs_med"] is not None
    assert obs["n_negative_spread"] == 0
    # les variables à paramètres libres ne sont PAS calculées
    blocked = " ".join(smp["not_computed_by_design"])
    assert "RET_H" in blocked
    assert "ROLL_STD_MID" in blocked


def test_sample_reports_causality_note(one_partition: Path):
    schema = detect_fields(["timestamp", "bid", "ask"])
    smp = derive_sample(one_partition, schema, max_events=500)
    assert "aucune valeur ne dépend du futur" in smp["checks"]["causality_note"]
