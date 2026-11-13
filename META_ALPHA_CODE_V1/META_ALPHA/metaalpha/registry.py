"""Registres : DGP Variable, Formula, Trial Ledger.

Règles appliquées mécaniquement :

- cycle de statut strict (aucun saut, aucun retour arrière) ;
- Trial Ledger append-only (aucune suppression, y compris des échecs) ;
- un champ scientifique (définition, paramètres) ne peut pas être
  renseigné par autre chose qu'un humain.
"""
from __future__ import annotations

import datetime as dt
from typing import Any

from .fs import Storage

VARIABLE_REGISTRY_REL = "10_REGISTRIES/DGP_VARIABLE_REGISTRY_V1.json"
FORMULA_REGISTRY_REL = "10_REGISTRIES/FORMULA_REGISTRY_V1.json"
TRIAL_LEDGER_REL = "10_REGISTRIES/TRIAL_LEDGER.csv"

VARIABLE_STATUS = [
    "PROPOSED", "SPECIFIED", "IMPLEMENTED", "CAUSALITY_CHECKED",
    "AVAILABLE_FOR_MINING", "DEFERRED", "REJECTED", "RETIRED",
]

FORMULA_CYCLE = [
    "DRAFT", "PREREGISTERED", "IMPLEMENTED", "CAUSALITY_AUDITED", "IS_SCREENED",
    "WALK_FORWARD_VALIDATED", "LOCKED_FOR_HOLDOUT", "HOLDOUT_EVALUATED",
    "STRESS_SURVIVOR", "CERTIFIED", "LOCKED",
]

SCIENTIFIC_FIELDS = {"mathematical_definition", "symbolic_definition", "parameters", "thresholds"}

TRIAL_LEDGER_HEADER = [
    "trial_id", "formula_id", "formula_version", "hypothesis_id", "phase",
    "created_utc", "split", "params_hash", "code_hash", "config_hash",
    "n_obs", "metric", "value", "p_value", "n_trials_at_test",
    "corrected_alpha", "outcome", "reason", "reproduced",
]


class RegistryCycleError(RuntimeError):
    pass


class OwnerAttributionError(RuntimeError):
    pass


def _now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def _load(storage: Storage, rel: str, empty: dict) -> dict:
    return storage.read_json(rel) if storage.exists(rel) else empty


def init_registries(storage: Storage) -> None:
    for rel, empty in [
        (VARIABLE_REGISTRY_REL, {"schema_version": "1.0", "variables": {}}),
        (FORMULA_REGISTRY_REL, {"schema_version": "1.0", "formulas": {}}),
    ]:
        if not storage.exists(rel):
            storage.write_atomic_json(rel, empty)


# --------------------------------------------------------------------------
# Variables
# --------------------------------------------------------------------------
def register_variable(storage: Storage, var: dict) -> None:
    required = [
        "variable_id", "version", "name", "family", "role", "status",
        "availability_ts_rule", "input_fields", "created_by",
    ]
    missing = [k for k in required if k not in var]
    if missing:
        raise ValueError(f"variable incomplète : {missing}")
    if var["status"] not in VARIABLE_STATUS:
        raise ValueError(f"statut de variable inconnu : {var['status']}")
    if var["role"] not in {"feature", "label", "diagnostic", "execution_field"}:
        raise ValueError(f"rôle invalide : {var['role']}")
    _assert_human(var, "variable")

    reg = _load(storage, VARIABLE_REGISTRY_REL, {"schema_version": "1.0", "variables": {}})
    key = f"{var['variable_id']}@{var['version']}"
    if key in reg["variables"]:
        raise ValueError(f"variable déjà enregistrée (immuable) : {key}")
    var = {**var, "created_utc": _now()}
    reg["variables"][key] = var
    storage.write_atomic_json(VARIABLE_REGISTRY_REL, reg)


def variables_available_for_mining(storage: Storage) -> list[str]:
    reg = _load(storage, VARIABLE_REGISTRY_REL, {"variables": {}})
    return [
        k for k, v in reg["variables"].items()
        if v.get("status") == "AVAILABLE_FOR_MINING"
    ]


# --------------------------------------------------------------------------
# Formules
# --------------------------------------------------------------------------
def register_formula(storage: Storage, formula: dict) -> None:
    required = [
        "formula_id", "version", "name", "mathematical_definition",
        "inputs", "parameters", "nan_policy", "event_alignment_rule",
        "execution_definition", "cost_definition", "created_by",
    ]
    missing = [k for k in required if k not in formula]
    if missing:
        raise ValueError(f"formule incomplète : {missing}")
    _assert_human(formula, "formule")

    reg = _load(storage, FORMULA_REGISTRY_REL, {"schema_version": "1.0", "formulas": {}})
    key = f"{formula['formula_id']}@{formula['version']}"
    if key in reg["formulas"]:
        raise ValueError(f"formule déjà enregistrée (immuable) : {key}")
    entry = {**formula, "status": "DRAFT", "created_utc": _now(), "history": []}
    reg["formulas"][key] = entry
    storage.write_atomic_json(FORMULA_REGISTRY_REL, reg)


def advance_formula(storage: Storage, key: str, to_status: str, evidence: dict) -> None:
    reg = _load(storage, FORMULA_REGISTRY_REL, {"formulas": {}})
    if key not in reg["formulas"]:
        raise KeyError(key)
    entry = reg["formulas"][key]
    cur = entry["status"]
    if to_status not in FORMULA_CYCLE:
        raise RegistryCycleError(f"statut inconnu : {to_status}")
    if FORMULA_CYCLE.index(to_status) != FORMULA_CYCLE.index(cur) + 1:
        raise RegistryCycleError(
            f"saut de statut interdit : {cur} -> {to_status} "
            f"(étape attendue : {FORMULA_CYCLE[FORMULA_CYCLE.index(cur) + 1]})"
        )
    if not evidence.get("artifact_sha"):
        raise RegistryCycleError("preuve manquante : artifact_sha requis pour avancer un statut")
    entry["status"] = to_status
    entry.setdefault("history", []).append(
        {"from": cur, "to": to_status, "utc": _now(), "evidence": evidence}
    )
    reg["formulas"][key] = entry
    storage.write_atomic_json(FORMULA_REGISTRY_REL, reg)


# --------------------------------------------------------------------------
# Trial Ledger : append-only
# --------------------------------------------------------------------------
def log_trial(storage: Storage, trial: dict) -> None:
    missing = [c for c in TRIAL_LEDGER_HEADER if c not in trial]
    if missing:
        raise ValueError(f"essai incomplet, colonnes manquantes : {missing}")
    if trial["outcome"] not in {"PENDING", "POSITIVE", "NEGATIVE", "INCONCLUSIVE", "FAILED"}:
        raise ValueError(f"résultat d'essai invalide : {trial['outcome']}")
    trial = {**trial, "created_utc": trial.get("created_utc") or _now()}
    storage.append_csv_line(TRIAL_LEDGER_REL, trial, TRIAL_LEDGER_HEADER)


def count_trials(storage: Storage) -> int:
    """Nombre total d'essais enregistrés — sert à la correction de multiplicité."""
    p = storage._resolve_read(TRIAL_LEDGER_REL)
    if not p.exists():
        return 0
    with open(p, "r", encoding="utf-8") as fh:
        return max(0, sum(1 for _ in fh) - 1)


def _assert_human(entry: dict, kind: str) -> None:
    if entry.get("created_by") != "HUMAN":
        raise OwnerAttributionError(
            f"un champ scientifique de {kind} doit être créé par HUMAN "
            f"(reçu : {entry.get('created_by')!r}). Un agent IA ne peut pas définir une formule."
        )
    for f in SCIENTIFIC_FIELDS & entry.keys():
        if entry.get("created_by") != "HUMAN":
            raise OwnerAttributionError(f"champ scientifique interdit à un agent : {f}")
