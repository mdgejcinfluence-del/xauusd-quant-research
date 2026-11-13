"""Application des réponses du propriétaire — le système reprend seul après.

Cycle vertueux :

    le système pose 9 questions      (contracts_engine)
    le propriétaire répond            (ce module, une seule fois, ~10 min)
    le système instancie les variables (DGP Variable Registry + Formula Registry)
    le système relance le calcul       (segment, sans intervention)

Chaque réponse est attribuée au propriétaire (`created_by = "HUMAN"`) : c'est
la seule source légitime d'un paramètre scientifique. Un agent IA ne peut pas
appeler `record_answers` avec une autre attribution.
"""
from __future__ import annotations

import datetime as dt
from typing import Any

from .families import FAMILY_INDEX, all_decisions
from .fs import Storage
from . import registry

DECISIONS_REL = "00_GOVERNANCE/OWNER_DECISIONS_V1.json"

DECISION_HEADER = ["decision_id", "family_id", "question", "answer", "answered_utc", "answered_by"]


def _now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def load_answers(storage: Storage) -> dict[str, Any]:
    if not storage.exists(DECISIONS_REL):
        return {"schema_version": "1.0", "answers": {}}
    return storage.read_json(DECISIONS_REL)


def record_answers(
    storage: Storage,
    answers: dict[str, Any],
    *,
    answered_by: str = "HUMAN",
    note: str = "",
) -> dict[str, Any]:
    """Enregistre les réponses et INSTANCIE immédiatement les variables.

    `answers` : {decision_id: valeur} — la valeur peut être une chaîne
    ("5min", "500") ou une structure. Aucune valeur par défaut n'est inventée :
    une décision non répondue reste ouverte.
    """
    if answered_by != "HUMAN":
        raise registry.OwnerAttributionError(
            "une réponse de préenregistrement ne peut venir que du propriétaire (HUMAN)"
        )

    valid_ids = {d.decision_id for d in all_decisions()}
    unknown = set(answers) - valid_ids
    if unknown:
        raise KeyError(f"decision_id inconnus : {sorted(unknown)}")

    doc = load_answers(storage)
    for did, value in answers.items():
        fam = next(d.family_id for d in all_decisions() if d.decision_id == did)
        doc["answers"][did] = {
            "family_id": fam,
            "answer": value,
            "answered_utc": _now(),
            "answered_by": answered_by,
            "note": note,
        }
    doc["updated_utc"] = _now()
    storage.write_atomic_json(DECISIONS_REL, doc)

    instantiated = instantiate_from_answers(storage, doc["answers"])
    return {"answers_recorded": len(answers), "variables_instantiated": instantiated}


# ---------------------------------------------------------------------------
def instantiate_from_answers(storage: Storage, answers: dict[str, Any]) -> list[str]:
    """Crée les variables et formules dont tous les paramètres sont désormais connus."""
    registry.init_registries(storage)
    created: list[str] = []

    # IMPORTANT : certaines variables consomment une décision d'une AUTRE famille
    # (ex. ZSCORE_ROBUST a besoin de D_FENETRES_VOL, définie en F3). On travaille
    # donc sur l'ensemble global des réponses, jamais sur un sous-ensemble local.
    global_answers = {did: a["answer"] for did, a in answers.items()}
    if not global_answers:
        return []

    for fam in FAMILY_INDEX.values():
        fam_answers = {
            did: a["answer"] for did, a in answers.items() if a["family_id"] == fam.family_id
        }

        for cand in fam.candidate_variables:
            free = [k for k, v in cand.get("parameters", {}).items() if v is None]
            if not free:
                continue  # déjà dérivable sans décision

            params = dict(cand.get("parameters", {}))
            # mapping décision -> paramètre (établi par famille, jamais deviné)
            for k in list(params):
                if params[k] is None:
                    hit = _match_parameter(fam.family_id, k, global_answers)
                    if hit is not None:
                        params[k] = hit

            if any(v is None for v in params.values()):
                continue  # il manque encore une décision : on ne devine pas

            vid = cand["variable_id"]
            try:
                registry.register_variable(storage, {
                    "variable_id": vid,
                    "version": "1",
                    "name": vid,
                    "family": fam.family_id,
                    "role": cand["role"],
                    "status": "SPECIFIED",
                    "availability_ts_rule": "disponible à t, calculé avec les données <= t",
                    "input_fields": list(fam.requires_fields),
                    "parameters": params,
                    "definition": cand["definition"],
                    "created_by": "HUMAN",
                    "derived_from_decision": fam_answers,
                })
                registry.register_formula(storage, {
                    "formula_id": vid,
                    "version": "1",
                    "name": vid,
                    "mathematical_definition": cand["definition"],
                    "inputs": list(fam.requires_fields),
                    "parameters": params,
                    "nan_policy": fam_answers.get("D_WARMUP_NULL", "NULL"),
                    "event_alignment_rule": "aligné sur l'événement t, sans regard futur",
                    "execution_definition": "non applicable avant Phase 4",
                    "cost_definition": "non applicable — feature, pas un trade",
                    "created_by": "HUMAN",
                })
                created.append(vid)
            except ValueError:
                continue  # déjà enregistrée : idempotent
    return created


def _match_parameter(family_id: str, parameter: str, answers: dict[str, Any]) -> Any:
    """Associe un paramètre libre à la décision qui le règle.

    Table EXPLICITE : aucune inférence. Si rien ne correspond, on renvoie None
    et la variable reste bloquée (comportement voulu).
    """
    table: dict[tuple[str, str], str] = {
        # --- F1 : aucune décision, tout est dérivable ---
        # --- F2 ---
        ("F2_RENDEMENTS", "H"): "D_HORIZONS",
        ("F3_VOLATILITE", "N"): "D_FENETRES_VOL",
        ("F3_VOLATILITE", "fenetre"): "D_FENETRES_VOL",
        ("F3_VOLATILITE", "warmup"): "D_WARMUP_NULL",
        ("F4_SAUTS_EXTREMES", "seuil"): "D_SEUIL_SAUT",
        ("F4_SAUTS_EXTREMES", "fenetre_retour"): "D_FENETRES_VOL",
        ("F5_MICROSTRUCTURE", "T"): "D_INTENSITE_T",
        ("F5_MICROSTRUCTURE", "N"): "D_FENETRES_VOL",
        ("F5_MICROSTRUCTURE", "n_classes"): "D_REGIME_SPREAD",
        ("F5_MICROSTRUCTURE", "fenetre"): "D_REGIME_SPREAD",
        ("F6_STRUCTURE_TEMPORELLE", "granularite"): "D_TIMEZONE_SESSIONS",
        ("F7_REGIMES", "methode"): "D_METHODE_REGIME",
        ("F7_REGIMES", "n_regimes"): "D_METHODE_REGIME",
        ("F7_REGIMES", "fenetre_entrainement"): "D_METHODE_REGIME",
        ("F8_LABELS", "H"): "D_HORIZON_LABEL",
    }
    did = table.get((family_id, parameter))
    if did is None:
        return None
    entry = answers.get(did)
    if entry is None:
        return None
    return entry["answer"] if isinstance(entry, dict) else entry


# ---------------------------------------------------------------------------
# Gabarit de réponses, prêt à remplir (aucune valeur pré-remplie)
# ---------------------------------------------------------------------------
def answer_template() -> dict[str, Any]:
    return {
        "_instruction": (
            "Remplacer chaque null par VOTRE valeur, puis appeler "
            "python -m metaalpha.decisions --apply answers.json"
        ),
        "_created_by": "HUMAN",
        "answers": {d.decision_id: None for d in all_decisions()},
    }


# ---------------------------------------------------------------------------
# CLI : le propriétaire répond une fois, puis le système repart seul
# ---------------------------------------------------------------------------
def main(argv: list[str] | None = None) -> int:
    import argparse
    import json
    import sys

    ap = argparse.ArgumentParser(description="META ALPHA — décisions de préenregistrement")
    ap.add_argument("--root", required=True, help="racine Drive (ou zone locale)")
    ap.add_argument("--template", action="store_true", help="écrit le gabarit de réponses")
    ap.add_argument("--apply", metavar="FILE", help="applique les réponses d'un fichier JSON")
    args = ap.parse_args(argv)

    storage = Storage.open(args.root)

    if args.template:
        tpl = answer_template()
        rel = "00_GOVERNANCE/OWNER_DECISIONS_TEMPLATE.json"
        storage.write_atomic_json(rel, tpl)
        print(json.dumps({"written": rel, "decisions": len(tpl["answers"])}, indent=2))
        return 0

    if args.apply:
        payload = json.loads(open(args.apply, encoding="utf-8").read())
        answers = payload.get("answers", payload)
        answers = {k: v for k, v in answers.items() if not k.startswith("_") and v is not None}
        if not answers:
            print(json.dumps({"status": "INCOMPLETE", "reason": "aucune réponse non nulle"}, indent=2))
            return 1
        res = record_answers(storage, answers)
        print(json.dumps(res, indent=2))
        return 0

    ap.print_help()
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())
