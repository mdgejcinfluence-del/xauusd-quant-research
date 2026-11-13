"""Gouvernance : machine à états, gates, scellement du Holdout, budget.

Principes codés ici (et non simplement documentés) :

- Aucune transition de phase sans approbation propriétaire explicite.
- Le Holdout est scellé par HMAC. La clé n'est pas dans l'environnement
  de calcul : sans action humaine, l'ouverture est impossible.
- Une promotion économique sans politique propriétaire lève une erreur.
- Aucune valeur produite par un LLM n'entre dans les décisions d'état.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import hmac
import json
import os
from dataclasses import dataclass
from enum import Enum
from typing import Any

from .fs import Storage

STATE_REL = "00_GOVERNANCE/state.json"
APPROVALS_REL = "00_GOVERNANCE/approvals"
HOLDOUT_SEAL_REL = "00_GOVERNANCE/HOLDOUT_SEAL.json"
HOLDOUT_UNSEALED_REL = "00_GOVERNANCE/HOLDOUT_UNSEALED_ONCE.json"
BUDGET_REL = "00_GOVERNANCE/budget_ledger.json"
KILL_SWITCH_REL = "00_GOVERNANCE/KILL_SWITCH"


class Phase(str, Enum):
    P2 = "PHASE_2_ANALYTICAL"
    P3 = "PHASE_3_MINING"
    P4 = "PHASE_4_VALIDATION"
    P5 = "PHASE_5_STRESS"
    P6 = "PHASE_6_QUALIFICATION"
    P7 = "PHASE_7_PORTFOLIO"
    P8 = "PHASE_8_HOLDOUT"
    P9 = "PHASE_9_MQL5"


ORDER = [p.value for p in Phase]

TERMINAL_STATUSES = {
    "PHASE_COMPLETE_AWAITING_OWNER_REVIEW",
    "BLOCKED_WITH_RESUME",
    "FAILED_TECHNICAL",
    "INCOMPLETE",
    "NO_EDGE",
}


class GovernanceError(RuntimeError):
    pass


class PhaseTransitionError(GovernanceError):
    pass


class HoldoutSealedError(GovernanceError):
    pass


class PolicyMissingError(GovernanceError):
    pass


class CostSemanticError(GovernanceError):
    pass


class KillSwitchActive(GovernanceError):
    pass


# --------------------------------------------------------------------------
# État de phase
# --------------------------------------------------------------------------
def default_state() -> dict:
    return {
        "schema_version": "1.0",
        "active_phase": None,
        "phase_status": "IDLE",
        "approved_phases": [],
        "completed_phases": [],
        "pending_units": [],
        "last_unit_done": None,
        "holdout_sealed": True,
        "updated_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
    }


def load_state(storage: Storage) -> dict:
    if not storage.exists(STATE_REL):
        return default_state()
    return storage.read_json(STATE_REL)


def save_state(storage: Storage, state: dict) -> None:
    state["updated_utc"] = dt.datetime.now(dt.timezone.utc).isoformat()
    storage.write_atomic_json(STATE_REL, state)


# --------------------------------------------------------------------------
# Approbations propriétaire
# --------------------------------------------------------------------------
def approve_phase(storage: Storage, phase: str, owner_signature: str, note: str = "") -> str:
    """Enregistre une approbation explicite. `owner_signature` = phrase saisie
    par le propriétaire (preuve d'intention, tracée)."""
    if phase not in ORDER:
        raise PhaseTransitionError(f"phase inconnue : {phase}")
    if not owner_signature or len(owner_signature.strip()) < 8:
        raise PhaseTransitionError("approbation refusée : signature propriétaire trop courte")
    rel = f"{APPROVALS_REL}/{phase}.json"
    payload = {
        "phase": phase,
        "approved_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "owner_signature": owner_signature.strip(),
        "note": note,
    }
    storage.write_atomic_json(rel, payload)
    st = load_state(storage)
    if phase not in st["approved_phases"]:
        st["approved_phases"].append(phase)
    save_state(storage, st)
    return rel


def assert_phase_authorized(storage: Storage, phase: str) -> None:
    """Séquence stricte : P(n) exige P(n-1) terminée et P(n) approuvée."""
    if phase not in ORDER:
        raise PhaseTransitionError(f"phase inconnue : {phase}")
    st = load_state(storage)
    idx = ORDER.index(phase)
    if idx > 0:
        prev = ORDER[idx - 1]
        if prev not in st["completed_phases"]:
            raise PhaseTransitionError(
                f"{phase} impossible : {prev} n'est pas terminée et acceptée"
            )
    if phase not in st["approved_phases"]:
        raise PhaseTransitionError(
            f"{phase} non approuvée par le propriétaire (approve_phase requis)"
        )
    if phase == Phase.P8.value and not storage.exists(HOLDOUT_UNSEALED_REL):
        raise HoldoutSealedError("Phase 8 exige l'ouverture explicite du Holdout (unseal)")


# --------------------------------------------------------------------------
# Scellement du Holdout
# --------------------------------------------------------------------------
def _seal_key() -> bytes:
    key = os.environ.get("HOLDOUT_SEAL_KEY")
    if not key:
        raise HoldoutSealedError(
            "HOLDOUT_SEAL_KEY absente de l'environnement : ouverture du Holdout impossible"
        )
    return key.encode()


def compute_seal(splits_sha: str, lock_manifest_sha: str) -> str:
    msg = f"{splits_sha}|{lock_manifest_sha}".encode()
    return hmac.new(_seal_key(), msg, hashlib.sha256).hexdigest()


def seal_holdout(storage: Storage, splits_sha: str, lock_manifest_sha: str) -> str:
    payload = {
        "sealed": True,
        "splits_sha": splits_sha,
        "lock_manifest_sha": lock_manifest_sha,
        "seal": compute_seal(splits_sha, lock_manifest_sha),
        "sealed_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
    }
    storage.write_atomic_json(HOLDOUT_SEAL_REL, payload)
    return payload["seal"]


def open_holdout_once(storage: Storage, splits_sha: str, lock_manifest_sha: str) -> dict:
    """Ouverture UNIQUE. Toute seconde tentative échoue définitivement."""
    if storage.exists(HOLDOUT_UNSEALED_REL):
        raise HoldoutSealedError(
            "Holdout déjà ouvert : une nouvelle recherche exige une nouvelle version"
        )
    if not storage.exists(HOLDOUT_SEAL_REL):
        raise HoldoutSealedError("aucun sceau enregistré : ouverture refusée")
    seal_doc = storage.read_json(HOLDOUT_SEAL_REL)
    expected = compute_seal(splits_sha, lock_manifest_sha)
    if not hmac.compare_digest(expected, seal_doc.get("seal", "")):
        raise HoldoutSealedError("sceau invalide : artefacts modifiés depuis le scellement")
    payload = {
        "opened_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "splits_sha": splits_sha,
        "lock_manifest_sha": lock_manifest_sha,
        "note": "Ouverture unique. Aucun retuning autorisé après cet instant.",
    }
    storage.write_atomic_json(HOLDOUT_UNSEALED_REL, payload)
    return payload


# --------------------------------------------------------------------------
# Politique propriétaire (seuils économiques)
# --------------------------------------------------------------------------
POLICY_REL = "00_GOVERNANCE/OWNER_POLICY_V1.json"


def require_policy(storage: Storage, keys: list[str]) -> dict:
    if not storage.exists(POLICY_REL):
        raise PolicyMissingError(
            f"OWNER_POLICY_REQUIRED : {POLICY_REL} absent (champs requis : {keys})"
        )
    pol = storage.read_json(POLICY_REL)
    missing = [k for k in keys if k not in pol]
    if missing:
        raise PolicyMissingError(f"OWNER_POLICY_REQUIRED : champs absents {missing}")
    return pol


class CostKind(str, Enum):
    OBSERVED = "OBSERVED"     # mesuré dans les données (ex. spread)
    SCENARIO = "SCENARIO"     # hypothèse explicite, étiquetée comme telle
    UNKNOWN = "UNKNOWN"       # inconnu => interdit tout net


def assert_cost_semantics(costs: dict[str, str]) -> None:
    """Un coût inconnu n'est jamais zéro : il bloque le calcul net."""
    unknown = [k for k, v in costs.items() if v == CostKind.UNKNOWN.value]
    if unknown:
        raise CostSemanticError(
            f"coûts UNKNOWN interdits dans un calcul net : {unknown}. "
            "Fournir un scénario explicite (SCENARIO) ou une politique propriétaire."
        )


# --------------------------------------------------------------------------
# Budget
# --------------------------------------------------------------------------
def load_budget(storage: Storage) -> dict:
    if not storage.exists(BUDGET_REL):
        return {"spent_usd": 0.0, "calls": 0, "cap_usd": None}
    return storage.read_json(BUDGET_REL)


def charge_budget(storage: Storage, cost_usd: float, cap_usd: float) -> dict:
    b = load_budget(storage)
    projected = float(b.get("spent_usd", 0.0)) + float(cost_usd)
    if projected > cap_usd:
        raise GovernanceError(
            f"BUDGET_CAP atteint : {projected:.4f} USD > {cap_usd:.2f} USD. Bascule NO_LLM."
        )
    b["spent_usd"] = round(projected, 6)
    b["calls"] = int(b.get("calls", 0)) + 1
    b["cap_usd"] = cap_usd
    b["updated_utc"] = dt.datetime.now(dt.timezone.utc).isoformat()
    storage.write_atomic_json(BUDGET_REL, b)
    return b


# --------------------------------------------------------------------------
# Arrêt d'urgence
# --------------------------------------------------------------------------
def assert_not_killed(storage: Storage) -> None:
    if storage.exists(KILL_SWITCH_REL):
        raise KillSwitchActive(f"KILL_SWITCH actif : {KILL_SWITCH_REL}")


# --------------------------------------------------------------------------
# Verrou d'écriture pour le superviseur IA
# --------------------------------------------------------------------------
class ReadOnlyView:
    """Vue en lecture seule. Toute tentative d'écriture lève PermissionError.

    C'est la barrière n°1 de l'architecture IA : le superviseur reçoit cet
    objet, pas le Storage.
    """

    def __init__(self, storage: Storage) -> None:
        self._storage = storage

    def read_json(self, rel: str) -> dict:
        return self._storage.read_json(rel)

    def exists(self, rel: str) -> bool:
        return self._storage.exists(rel)

    def write_atomic_json(self, rel: str, obj: Any) -> str:
        raise PermissionError("superviseur IA : écriture interdite")

    def write_atomic_bytes(self, rel: str, data: bytes, validator=None) -> str:
        raise PermissionError("superviseur IA : écriture interdite")

    def append_csv_line(self, rel: str, row: dict, header) -> None:
        raise PermissionError("superviseur IA : écriture interdite")
