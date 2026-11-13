"""Le système AGIT : il instancie lui-même les familles du dossier.

Chaîne complète, sans intervention humaine :

    capteur de schéma  ->  détection des champs réellement présents
                       ->  instanciation des 8 familles (§4.2)
                       ->  dérivation automatique des variables sans paramètre
                       ->  marquage DEFERRED des familles hors périmètre
                       ->  calcul d'un échantillon (causalité + distribution)
                       ->  extraction des QUESTIONS à trancher
                       ->  blocage contrôlé des variables à paramètres libres

Le système ne prend AUCUNE décision scientifique : il les isole, les compte
et les présente. La différence est celle entre « décider » et « préparer la
décision ». Ici, on prépare tout ce qui est mécanisable.
"""
from __future__ import annotations

import datetime as dt
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .families import (
    DEFERRED_EXTERNAL,
    FAMILIES,
    FAMILY_INDEX,
    FORBIDDEN_FIELDS,
    FIELD_ALIASES,
    all_decisions,
    summary as families_summary,
)


def _now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


# ---------------------------------------------------------------------------
# 1. CAPTEUR DE SCHÉMA — on mesure, on ne suppose jamais
# ---------------------------------------------------------------------------
def detect_fields(columns: list[str]) -> dict[str, Any]:
    """Mappe les colonnes réelles vers les rôles canoniques.

    Aucune hypothèse : si `bid` n'est pas reconnu, la famille qui en dépend
    sera marquée unavailable, pas « devinée ».
    """
    lowered = {c.lower().strip(): c for c in columns}
    mapping: dict[str, str | None] = {}
    for role, aliases in FIELD_ALIASES.items():
        mapping[role] = next((lowered[a] for a in aliases if a in lowered), None)

    forbidden_present = {
        col: usage
        for col in columns
        for key, usage in FORBIDDEN_FIELDS.items()
        if key == col.lower().strip()
    }
    unmapped = [c for c in columns if c not in set(v for v in mapping.values() if v)]
    return {
        "raw_columns": list(columns),
        "canonical": mapping,
        "forbidden_fields_present": forbidden_present,
        "unmapped_columns": unmapped,
        "has_core_quote_triplet": all(mapping.get(r) for r in ("timestamp", "bid", "ask")),
    }


# ---------------------------------------------------------------------------
# 2. INSTANCIATION DES FAMILLES
# ---------------------------------------------------------------------------
STATUS_AVAILABLE = "SPECIFIED"
STATUS_PENDING_DECISION = "PENDING_OWNER_DECISION"
STATUS_UNAVAILABLE = "UNAVAILABLE_FIELD"
STATUS_DEFERRED = "DEFERRED"


def instantiate_families(schema: dict[str, Any]) -> list[dict[str, Any]]:
    """Construit l'état de chaque famille à partir des champs réellement observés."""
    canon = schema["canonical"]
    available_roles = {r for r, v in canon.items() if v}

    out: list[dict[str, Any]] = []
    for fam in FAMILIES:
        missing = [f for f in fam.requires_fields if f not in available_roles]
        if missing:
            out.append({
                "family_id": fam.family_id,
                "number": fam.number,
                "name": fam.name,
                "status": STATUS_UNAVAILABLE,
                "reason": f"champs absents : {missing}",
                "variables": [],
                "decisions_open": [],
            })
            continue

        # une variable est dérivable seule si AUCUN de ses paramètres n'est libre
        variables = []
        for v in fam.candidate_variables:
            free = [k for k, val in v.get("parameters", {}).items() if val is None]
            variables.append({
                "variable_id": v["variable_id"],
                "role": v["role"],
                "definition": v["definition"],
                "free_parameters": free,
                "status": STATUS_PENDING_DECISION if free else "DERIVABLE_NOW",
                "measured": None,      # rempli par l'échantillon
            })

        decisions_open = [d.decision_id for d in fam.decisions]
        derivable = [v for v in variables if v["status"] == "DERIVABLE_NOW"] and not decisions_open
        out.append({
            "family_id": fam.family_id,
            "number": fam.number,
            "name": fam.name,
            "status": STATUS_AVAILABLE if derivable else STATUS_PENDING_DECISION,
            "reason": "" if derivable else "décisions de préenregistrement ouvertes",
            "variables": variables,
            "decisions_open": decisions_open,
            "note": fam.note,
        })
    return out


def deferred_external_register() -> list[dict[str, str]]:
    """Les familles hors périmètre, explicitement différées (§2.2)."""
    return [
        {**d, "provenance": "dossier §2.2", "replaced_by_proxy": "INTERDIT"}
        for d in DEFERRED_EXTERNAL
    ]


# ---------------------------------------------------------------------------
# 3. ÉCHANTILLON MESURÉ — dérivation réelle sur 1 partition
# ---------------------------------------------------------------------------
def derive_sample(
    parquet_path: str | os.PathLike[str],
    schema: dict[str, Any],
    *,
    memory_limit: str = "4GB",
    threads: int = 2,
    max_events: int = 400_000,
) -> dict[str, Any]:
    """Calcule un échantillon borné et mesure ce qui est mesurable SANS paramètre.

    On ne produit pas de « résultat scientifique » : on produit
      - une preuve que la variable se calcule,
      - une distribution observée (min/médiane/max),
      - un contrôle de causalité (aucune valeur ne dépend du futur).

    Les variables à paramètres libres ne sont PAS calculées : ce serait choisir
    un paramètre, donc prendre une décision qui ne nous appartient pas.
    """
    from .duck import connect

    canon = schema["canonical"]
    ts, bid, ask = canon.get("timestamp"), canon.get("bid"), canon.get("ask")
    if not all([ts, bid, ask]):
        return {"status": "UNAVAILABLE_FIELD", "reason": "triplet timestamp/bid/ask incomplet"}

    q = f"""
    WITH base AS (
        SELECT "{ts}" AS t, "{bid}" AS bid, "{ask}" AS ask
        FROM read_parquet('{Path(parquet_path).as_posix()}')
        ORDER BY "{ts}"
        LIMIT {int(max_events)}
    ), q AS (
        SELECT t, bid, ask,
               ask - bid                       AS spread_abs,
               (ask + bid) / 2.0               AS mid,
               CASE WHEN (ask + bid) / 2.0 <> 0
                    THEN (ask - bid) / ((ask + bid) / 2.0) END AS spread_rel,
               t - lag(t) OVER (ORDER BY t)     AS dt_prev
        FROM base
    )
    SELECT
        count(*)                                    AS n_events,
        min(t) AS t_min, max(t) AS t_max,
        min(spread_abs) AS spread_abs_min,
        median(spread_abs) AS spread_abs_med,
        max(spread_abs) AS spread_abs_max,
        min(spread_rel) AS spread_rel_min,
        median(spread_rel) AS spread_rel_med,
        max(spread_rel) AS spread_rel_max,
        count(*) FILTER (WHERE spread_abs < 0)      AS n_negative_spread,
        count(*) FILTER (WHERE mid IS NULL)         AS n_null_mid,
        min(dt_prev) AS dt_min, median(dt_prev) AS dt_med, max(dt_prev) AS dt_max
    FROM q
    """

    with connect(memory_limit=memory_limit, threads=threads) as con:
        row = con.execute(q).fetchone()
        cols = [d[0] for d in con.description]

    values = dict(zip(cols, row))
    n = values.get("n_events") or 0
    return {
        "status": "MEASURED",
        "source": str(parquet_path),
        "events_measured": n,
        "bounded_by": max_events,
        "observed": {k: _jsonable(v) for k, v in values.items()},
        "checks": {
            "negative_spread": values.get("n_negative_spread") or 0,
            "null_mid": values.get("n_null_mid") or 0,
            # causalité : lag() ne regarde que le passé. Vérifié par construction.
            "causality_note": "seul lag() est utilisé : aucune valeur ne dépend du futur",
        },
        "not_computed_by_design": [
            "RET_H (horizon libre)",
            "ROLL_STD_MID (fenêtre libre)",
            "UPDATE_INTENSITY (durée libre)",
            "ZSCORE_ROBUST (seuil libre)",
            "REGIME_CLASS (méthode libre)",
            "MFE_H / MAE_H (horizon libre)",
        ],
    }


def _jsonable(v: Any) -> Any:
    if isinstance(v, (int, float, str, bool)) or v is None:
        return v
    return str(v)


# ---------------------------------------------------------------------------
# 4. EXTRACTION DES QUESTIONS
# ---------------------------------------------------------------------------
def extract_questions(family_states: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Transforme les décisions ouvertes en questions posées, une par une.

    C'est le « il doit agir » : le système va chercher lui-même ce qui bloque,
    au lieu d'attendre qu'on lui dise quoi définir.
    """
    open_ids = {d for f in family_states for d in f["decisions_open"]}
    questions = []
    for d in all_decisions():
        if d.decision_id not in open_ids:
            continue
        questions.append({
            "decision_id": d.decision_id,
            "family_id": d.family_id,
            "family_name": FAMILY_INDEX[d.family_id].name,
            "question": d.question,
            "why_it_matters": d.why_it_matters,
            "examples": list(d.example_values),
            "default": d.default_is,
            "blocks": sorted({
                v["variable_id"]
                for v in next(f for f in family_states if f["family_id"] == d.family_id)["variables"]
                if v["status"] == STATUS_PENDING_DECISION
            }),
            "answer": None,
        })
    return questions


# ---------------------------------------------------------------------------
# 5. ORCHESTRATION : un seul appel produit le rapport complet
# ---------------------------------------------------------------------------
def build_phase2_contract_report(
    *,
    schema: dict[str, Any],
    sample: dict[str, Any] | None = None,
) -> dict[str, Any]:
    families = instantiate_families(schema)
    questions = extract_questions(families)

    available = [f["family_id"] for f in families if f["status"] == STATUS_AVAILABLE]
    pending = [f["family_id"] for f in families if f["status"] == STATUS_PENDING_DECISION]
    unavailable = [f["family_id"] for f in families if f["status"] == STATUS_UNAVAILABLE]

    all_vars = [v for f in families for v in f["variables"]]
    derivable = [v["variable_id"] for v in all_vars if v["status"] == "DERIVABLE_NOW"]
    blocked = [v["variable_id"] for v in all_vars if v["status"] == STATUS_PENDING_DECISION]

    # Statut honnête : la Phase 2 peut-elle être déclarée complète ?
    if unavailable and len(unavailable) > len(families) // 2:
        phase_status = "FAILED_TECHNICAL"
    elif questions:
        phase_status = "BLOCKED_WITH_RESUME"
    else:
        phase_status = "PHASE_COMPLETE_AWAITING_OWNER_REVIEW"

    return {
        "schema_version": "1.0",
        "generated_utc": _now(),
        "phase": "PHASE_2_ANALYTICAL",
        "phase_status": phase_status,
        "families_summary": families_summary(),
        "schema_detection": schema,
        "families": families,
        "deferred_external": deferred_external_register(),
        "counts": {
            "families_total": len(families),
            "families_available": len(available),
            "families_pending_decision": len(pending),
            "families_unavailable": len(unavailable),
            "variables_derivable_now": len(derivable),
            "variables_blocked": len(blocked),
            "decisions_open": len(questions),
        },
        "variables_derivable_now": derivable,
        "variables_blocked": blocked,
        "questions_for_owner": questions,
        "sample_measurement": sample,
        "next_action": {
            "kind": "ANSWER_QUESTIONS_THEN_RESUME",
            "instruction": (
                "Répondre aux questions listées dans questions_for_owner. Chaque réponse "
                "instancie automatiquement la variable correspondante : le système "
                "reprend ensuite sans autre intervention."
            ),
            "blocking": bool(questions),
        },
    }
