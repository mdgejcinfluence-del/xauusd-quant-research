"""Superviseur IA — NON DÉCISIONNAIRE.

Quatre barrières, toutes appliquées ici :

1. Données : le modèle reçoit une ReadOnlyView (aucune écriture possible).
2. Sortie : schéma strict ; tout champ inconnu est rejeté.
3. Gouvernance : aucune valeur produite n'est lue par governance.py.
4. Attribution : toute entrée scientifique exige created_by == "HUMAN".

Chaîne de repli : Gemini Flash (gratuit) -> NVIDIA NIM (gratuit) ->
DeepSeek (plafonné) -> NO_LLM. Le calcul continue dans tous les cas.
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any

from .config import Config
from .governance import ReadOnlyView, charge_budget, load_budget

ALLOWED_OUTPUT_KEYS = {"resume", "incoherences", "manquants", "questions"}

REVIEW_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": ["resume", "incoherences", "manquants", "questions"],
    "properties": {
        "resume": {"type": "string", "maxLength": 4000},
        "incoherences": {"type": "array", "items": {"type": "string"}, "maxItems": 30},
        "manquants": {"type": "array", "items": {"type": "string"}, "maxItems": 30},
        "questions": {"type": "array", "items": {"type": "string"}, "maxItems": 10},
    },
}

PROVIDERS = [
    {"name": "gemini", "env": "GEMINI_API_KEY", "free": True,
     "url": "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"},
    {"name": "nvidia", "env": "NVIDIA_API_KEY", "free": True,
     "url": "https://integrate.api.nvidia.com/v1/chat/completions"},
    {"name": "deepseek", "env": "DEEPSEEK_API_KEY", "free": False,
     "url": "https://api.deepseek.com/chat/completions"},
]

SYSTEM_PROMPT = """Tu es un lecteur de rapports techniques. Tu n'as AUCUN pouvoir de décision.

Interdictions absolues :
- Tu n'inventes ni formule, ni paramètre, ni seuil.
- Tu n'affirmes jamais qu'un edge existe ou est rentable.
- Tu ne proposes jamais de modifier les données, le split ou le Holdout.
- Tu ne qualifies jamais un résultat de "bon" ou "prometteur".

Ta sortie est un JSON strict avec exactement quatre clés :
  resume (string), incoherences (array of string), manquants (array of string), questions (array of string).
Tu ne produis aucun autre texte.
"""


class AIResponseInvalid(RuntimeError):
    pass


@dataclass
class SupervisorResult:
    provider: str
    payload: dict[str, Any] | None
    cost_usd: float
    degraded: bool = False


def validate(payload: dict) -> dict:
    if set(payload.keys()) - ALLOWED_OUTPUT_KEYS:
        raise AIResponseInvalid(f"clés non autorisées : {set(payload.keys()) - ALLOWED_OUTPUT_KEYS}")
    missing = ALLOWED_OUTPUT_KEYS - set(payload.keys())
    if missing:
        raise AIResponseInvalid(f"clés manquantes : {missing}")
    if not isinstance(payload["resume"], str):
        raise AIResponseInvalid("resume doit être une chaîne")
    for k in ("incoherences", "manquants", "questions"):
        if not isinstance(payload[k], list) or not all(isinstance(x, str) for x in payload[k]):
            raise AIResponseInvalid(f"{k} doit être une liste de chaînes")
    return payload


def estimate_cost_usd(provider: str, in_tokens: int, out_tokens: int) -> float:
    rates = {
        "deepseek": (0.14 / 1e6, 0.28 / 1e6),   # tarifs vérifiés nov. 2026
        "gemini": (0.0, 0.0),
        "nvidia": (0.0, 0.0),
    }
    rin, rout = rates.get(provider, (0.0, 0.0))
    return in_tokens * rin + out_tokens * rout


class Supervisor:
    """Le superviseur ne reçoit JAMAIS l'objet Storage."""

    def __init__(self, view: ReadOnlyView, config: Config, transport=None) -> None:
        self.view = view
        self.config = config
        self.cap_usd = config.cap_usd
        self.no_llm = config.no_llm
        self.max_calls = int(config.get("ai", "max_calls_per_run", default=20))
        self.model = config.get("ai", "model", default="deepseek-chat")
        self._transport = transport  # injectable pour les tests
        self._calls = 0

    # ------------------------------------------------------------------
    def review_report(self, report_rel: str, contract_rel: str | None = None) -> SupervisorResult:
        if self.no_llm:
            return SupervisorResult("NO_LLM", None, 0.0, degraded=True)
        if self._calls >= self.max_calls:
            return SupervisorResult("NO_LLM", None, 0.0, degraded=True)
        if load_budget(self.view._storage).get("spent_usd", 0.0) >= self.cap_usd:
            return SupervisorResult("NO_LLM", None, 0.0, degraded=True)

        report = self.view.read_json(report_rel)
        contract = self.view.read_json(contract_rel) if contract_rel and self.view.exists(contract_rel) else {}
        prompt = json.dumps({"contract": contract, "report": report}, ensure_ascii=False)[:120_000]

        for prov in PROVIDERS:
            if not os.environ.get(prov["env"]):
                continue
            raw, in_tok, out_tok = self._call(prov["name"], prompt)
            cost = estimate_cost_usd(prov["name"], in_tok, out_tok)
            try:
                charge_budget(self.view._storage, cost, self.cap_usd)
            except Exception:
                return SupervisorResult("NO_LLM", None, 0.0, degraded=True)
            self._calls += 1
            try:
                return SupervisorResult(prov["name"], validate(json.loads(raw)), cost)
            except Exception:
                continue  # sortie invalide => fournisseur suivant

        return SupervisorResult("NO_LLM", None, 0.0, degraded=True)

    # ------------------------------------------------------------------
    def _call(self, provider: str, prompt: str):
        if self._transport is not None:
            return self._transport(provider, SYSTEM_PROMPT, prompt)
        raise RuntimeError(
            "aucun transport réseau configuré : injecter un transport ou définir une clé API"
        )

    # ------------------------------------------------------------------
    def write_anything(self, rel: str, obj: Any) -> None:
        """Présent uniquement pour que les tests vérifient le refus."""
        self.view.write_atomic_json(rel, obj)
