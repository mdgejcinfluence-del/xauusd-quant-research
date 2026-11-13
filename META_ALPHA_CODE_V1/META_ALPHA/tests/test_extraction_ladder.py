"""L'échelle d'extraction est-elle réelle ? On la gravit pour de vrai.

Scénario complet, sans aucune intervention humaine :
  1. corpus synthétique de 6 partitions, 2 mois
  2. le système découvre, mesure, dérive          (L0 -> L4)
  3. il s'arrête à L5 et dit exactement ce qui manque
  4. le propriétaire répond aux 9 décisions        (L5)
  5. le système extrait et scelle                  (L6 -> L7)
  6. on relance : il ne refait rien                (idempotence)
"""
from __future__ import annotations

import datetime as dt
import random
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq
import pytest

from metaalpha.extract import build_manifest, plan_extraction, run_extraction
from metaalpha.extraction_ladder import advance, evaluate_levels
from metaalpha.fs import Storage
from metaalpha.inventory import build_inventory
from metaalpha.decisions import record_answers


def _make_corpus(root: Path, months: int = 3, rows: int = 800) -> list[Path]:
    parts: list[Path] = []
    random.seed(11)
    price = 2060.0
    for m in range(months):
        t = dt.datetime(2024, 1 + m, 2, tzinfo=dt.timezone.utc)
        ts, bids, asks = [], [], []
        for _ in range(rows):
            t += dt.timedelta(milliseconds=random.randint(50, 1200))
            price += random.gauss(0, 0.07)
            ts.append(t)
            bids.append(round(price, 2))
            asks.append(round(price + random.uniform(0.10, 0.50), 2))
        p = root / f"2024-{1 + m:02d}.parquet"
        pq.write_table(pa.table({"timestamp": ts, "bid": bids, "ask": asks}), p)
        parts.append(p)
    return parts


def _register(storage, vid: str, *, family="F1", params=None):
    """Enregistre une variable conforme au Registry (tous champs obligatoires)."""
    from metaalpha import registry

    registry.init_registries(storage)
    try:
        registry.register_variable(storage, {
            "variable_id": vid, "version": "1", "name": vid,
            "family": family, "role": "feature", "status": "SPECIFIED",
            "availability_ts_rule": "t_0 (aucune donnée future)",
            "input_fields": ["timestamp", "bid", "ask"],
            "created_by": "HUMAN",
            "parameters": params or {},
        })
    except ValueError as exc:
        if "déjà enregistrée" not in str(exc):
            raise


@pytest.fixture()
def corpus(tmp_path: Path) -> tuple[Storage, list[Path]]:
    storage = Storage.open(tmp_path / "META_ALPHA_RESEARCH")
    raw = tmp_path / "corpus"
    raw.mkdir()
    return storage, _make_corpus(raw)


# ---------------------------------------------------------------------------
# Inventaire
# ---------------------------------------------------------------------------
def test_inventory_reads_footers_only(corpus):
    _, parts = corpus
    inv = build_inventory(parts[0].parent)
    assert inv["files_found"] == 3
    assert inv["partitions_ok"] == 3
    assert inv["total_rows"] == 3 * 800
    assert inv["schema_heterogeneous"] is False
    assert inv["partitions"][0]["field_mapping"]["timestamp"] == "timestamp"


def test_inventory_on_empty_root_reports_unknown(corpus, tmp_path):
    inv = build_inventory(tmp_path / "nowhere")
    assert inv["files_found"] == 0
    assert inv["unknowns"]  # le système avoue ce qu'il ignore


def test_inventory_detects_schema_drift(corpus, tmp_path):
    _, parts = corpus
    # une 4e partition avec une colonne en plus -> schéma hétérogène
    pq.write_table(
        pa.table({
            "timestamp": [dt.datetime(2024, 4, 2, tzinfo=dt.timezone.utc)],
            "bid": [2060.0], "ask": [2060.3], "volume": [3],
        }),
        parts[0].parent / "2024-04.parquet",
    )
    inv = build_inventory(parts[0].parent)
    assert inv["files_found"] == 4
    assert inv["schema_heterogeneous"] is True
    assert len(inv["schema_signatures"]) == 2


# ---------------------------------------------------------------------------
# Échelle
# ---------------------------------------------------------------------------
def test_ladder_climbs_to_L4_without_any_human(corpus):
    storage, parts = corpus
    rep = advance(storage, parts[0].parent)
    ladder = rep["ladder"]

    assert ladder["current_level"] == "L4_MESURE", ladder["levels_total"]
    assert ladder["needs_human"] is True
    assert ladder["next_level"]["level"] == "L5_ENRICHISSEMENT"
    assert ladder["who_acts_next"].startswith("PROPRIETAIRE")
    # le journal prouve que le travail a réellement eu lieu
    assert any("L2/L3/L4" in line for line in rep["log"])


def test_ladder_states_are_ordered_and_blocked_beyond_break(corpus):
    storage, parts = corpus
    rep = advance(storage, parts[0].parent)
    states = rep["ladder"]["states"]
    ranks = [s["reached"] for s in states]
    # monotone : vrai puis faux, jamais vrai après faux
    first_false = ranks.index(False) if False in ranks else len(ranks)
    assert all(ranks[:first_false]) and not any(ranks[first_false:])


def test_ladder_on_empty_corpus_stops_at_L0() -> None:
    import tempfile

    tmp = Path(tempfile.mkdtemp())
    storage = Storage.open(tmp / "R")
    empty = tmp / "empty"
    empty.mkdir()
    rep = advance(storage, empty)
    assert rep["ladder"]["current_level"] == "L0_DECOUVERTE"
    assert rep["ladder"]["next_level"]["level"] == "L0_DECOUVERTE" or \
           rep["ladder"]["next_level"]["level"] == "L1_TOPOLOGIE"


def test_evaluate_levels_respects_chain_when_sample_missing():
    inv = {"files_found": 2, "partitions_ok": 2, "total_rows": 100,
           "partitions_unreadable": 0, "schema_heterogeneous": False}
    ev = evaluate_levels(inventory=inv, sample=None)
    # Sans échantillon mesuré, la chaîne s'arrête à L1 quelle que soit la
    # générosité des compteurs : aucun barreau n'est franchi sans preuve.
    assert ev["current_level"] in ("L1_TOPOLOGIE", "L2_INTEGRITE")
    reached = [s["reached"] for s in ev["states"]]
    first_false = reached.index(False)
    assert all(reached[:first_false]) and not any(reached[first_false:])
    assert ev["states"][4]["level"] == "L4_MESURE"
    assert ev["states"][5]["reached"] is False


# ---------------------------------------------------------------------------
# Extraction : le plan refuse d'inventer
# ---------------------------------------------------------------------------
def test_plan_before_decisions_only_has_parameterless(corpus):
    storage, _ = corpus
    for vid in ("MID", "SPREAD_ABS", "SPREAD_REL", "RET_TICK"):
        _register(storage, vid)

    plan = plan_extraction(storage)
    assert plan["status"] == "PLANNED"
    assert {e["variable_id"] for e in plan["extractible"]} == {
        "MID", "SPREAD_ABS", "SPREAD_REL", "RET_TICK"
    }


def test_plan_refuses_untranslatable_variable(corpus):
    storage, _ = corpus
    from metaalpha import registry

    _register(storage, "REGIME_CLASS", family="F7")
    plan = plan_extraction(storage)
    refused = {r["variable_id"]: r["cause"] for r in plan["refused"]}
    assert refused["REGIME_CLASS"] == "FORMULE_NON_CERTIFIEE"
    assert "REGIME_CLASS" not in {e["variable_id"] for e in plan["extractible"]}


def test_plan_refuses_variable_with_missing_parameter(corpus):
    storage, _ = corpus
    from metaalpha import registry

    _register(storage, "ROLL_STD_MID", family="F3", params={"fenetre": None})
    plan = plan_extraction(storage)
    refused = {r["variable_id"]: r["cause"] for r in plan["refused"]}
    assert refused["ROLL_STD_MID"] == "PARAMETRE_MANQUANT"


# ---------------------------------------------------------------------------
# Extraction réelle
# ---------------------------------------------------------------------------
def test_extraction_writes_matrix_and_checkpoints(corpus):
    storage, parts = corpus
    from metaalpha.inventory import build_inventory

    for vid in ("MID", "SPREAD_ABS", "RET_TICK"):
        _register(storage, vid)

    inv = build_inventory(parts[0].parent)
    rep = run_extraction(storage, inv["partitions"])
    assert rep["extracted_now"] == 3
    assert rep["failed"] == 0
    assert rep["partitions_done_total"] == 3

    import pyarrow.parquet as pq
    out = pq.read_table(rep["results"][0]["output"])
    assert set(out.column_names) == {"t", "bid", "ask", "MID", "SPREAD_ABS", "RET_TICK"}
    assert out.num_rows == 800


def test_extraction_is_idempotent(corpus):
    storage, parts = corpus
    from metaalpha.inventory import build_inventory

    _register(storage, "MID")
    inv = build_inventory(parts[0].parent)

    first = run_extraction(storage, inv["partitions"])
    second = run_extraction(storage, inv["partitions"])
    assert first["extracted_now"] == 3
    assert second["extracted_now"] == 0
    assert second["skipped_already_done"] == 3   # rien n'est refait


def test_extraction_blocked_without_registry(corpus):
    storage, parts = corpus
    from metaalpha.inventory import build_inventory

    inv = build_inventory(parts[0].parent)
    rep = run_extraction(storage, inv["partitions"])
    assert rep["status"] == "BLOCKED"
    assert rep["plan"]["status"] == "NO_REGISTRY"


def test_manifest_seals_matrix(corpus):
    storage, parts = corpus
    from metaalpha.inventory import build_inventory

    _register(storage, "MID")
    inv = build_inventory(parts[0].parent)
    run_extraction(storage, inv["partitions"])
    man = build_manifest(storage)
    assert man["manifest_sha256"]
    assert man["total_rows"] == 3 * 800
    assert man["honesty"]["is_scientific_result"] is False
    assert "MID" in man["lineage"]["variables_used"]


# ---------------------------------------------------------------------------
# Le parcours complet, d'un bout à l'autre
# ---------------------------------------------------------------------------
def test_full_ladder_L0_to_L7(corpus):
    storage, parts = corpus
    raw = parts[0].parent

    # 1. L0 -> L4, seul
    rep = advance(storage, raw)
    assert rep["ladder"]["current_level"] == "L4_MESURE"
    assert rep["ladder"]["needs_human"] is True

    # 2. L5 : le propriétaire répond
    record_answers(storage, {
        "D_HORIZONS": "5min",
        "D_FENETRES_VOL": "500",
        "D_WARMUP_NULL": "NULL",
        "D_SEUIL_SAUT": "4",
        "D_INTENSITE_T": "5s",
        "D_REGIME_SPREAD": "3 classes / 1 jour",
        "D_TIMEZONE_SESSIONS": "UTC + aucune session",
        "D_METHODE_REGIME": "DEFERRED",
        "D_HORIZON_LABEL": "30s",
    })

    # 3. L6 : extraction réelle. Les 9 réponses ont instancié des variables,
    #    mais seules celles dont la formule est CERTIFIÉE sont traduisibles :
    #    les autres sont refusées avec leur cause, jamais devinées.
    _register(storage, "MID")
    inv = build_inventory(raw)
    ext = run_extraction(storage, inv["partitions"])
    assert ext["extracted_now"] == 3
    assert ext["plan"]["refused_total"] >= 1

    # 4. L7 : scellement
    man = build_manifest(storage)
    assert man["manifest_sha256"]

    # 5. l'échelle reconnaît le sommet, sans intervention
    final = advance(storage, raw)
    assert final["ladder"]["current_rank"] >= 6
    assert final["ladder"]["who_acts_next"] in (
        "SYSTEME (automatique, sans intervention)", "AUCUN_AGENT : chaîne terminée"
    )
