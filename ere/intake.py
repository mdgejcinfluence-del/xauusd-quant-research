"""Qualification d'entrée du moteur A pour un dossier trader (ERE-NEXT-001).

Accepte un dossier brut (dict) tel qu'un fondateur ou une collecte le
fournit, et produit soit un TraderDossier valide + un rapport de
qualification, soit un rejet motivé. Aucune observation manquante n'est
fabriquée : un champ absent doit être explicitement null dans la source
ou il est déclaré manquant dans le rapport, jamais rempli.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field

from .contracts import TraderDossier
from .engines import engine_a_ingest

# Champs reconnus par transaction. Tout champ hors liste est signalé, pas ignoré.
TRADE_FIELDS = {
    "instrument", "side", "open_time", "close_time", "open_price", "close_price",
    "volume", "result", "timezone", "source_ref",
}
REQUIRED_FOR_B = {"instrument", "side", "open_time"}  # minimum pour que B puisse décrire


@dataclass
class IntakeReport:
    accepted: bool
    dossier_id: str = ""
    n_trades: int = 0
    duplicates_removed: list = field(default_factory=list)
    missing_by_field: dict = field(default_factory=dict)
    unknown_fields: list = field(default_factory=list)
    provenance_complete: bool = False
    timezone_status: str = "ABSENT"
    b_ready: bool = False
    b_blockers: list = field(default_factory=list)
    warnings: list = field(default_factory=list)


def _trade_key(t: dict) -> str:
    # Empreinte sur TOUS les champs descriptifs sauf la référence de source:
    # deux positions simultanées de même lot mais de résultats différents
    # (cas réel TRADER-CANDIDATE-002, 04:05:31) sont distinctes, pas des doublons.
    core = {k: t.get(k) for k in sorted(TRADE_FIELDS - {"source_ref"})}
    return hashlib.sha256(json.dumps(core, sort_keys=True, default=str).encode()).hexdigest()


def qualify_dossier(raw: dict) -> tuple[TraderDossier, IntakeReport]:
    """Valide un dossier brut. Lève ValueError si la structure est inexploitable."""
    if not isinstance(raw, dict) or "trades" not in raw:
        raise ValueError("Dossier brut: clé 'trades' obligatoire")
    trades_in = raw["trades"]
    if not trades_in:
        raise ValueError("Dossier brut: aucune transaction — un dossier vide n'est pas un dossier")
    rep = IntakeReport(accepted=False)
    seen, trades = {}, []
    for t in trades_in:
        if not isinstance(t, dict):
            raise ValueError("Dossier brut: chaque transaction doit être un objet")
        for k in t:
            if k not in TRADE_FIELDS and k not in rep.unknown_fields:
                rep.unknown_fields.append(k)
        key = _trade_key(t)
        if key in seen:
            rep.duplicates_removed.append(key[:12])
            continue
        seen[key] = True
        trades.append(dict(t))
    # Informations manquantes: comptées champ par champ, jamais comblées.
    for f in sorted(TRADE_FIELDS):
        rep.missing_by_field[f] = sum(1 for t in trades if t.get(f) is None)
    rep.n_trades = len(trades)
    rep.provenance_complete = all(t.get("source_ref") for t in trades)
    if not rep.provenance_complete:
        rep.warnings.append("provenance incomplète: au moins une transaction sans source_ref")
    tz_declared = [t.get("timezone") for t in trades]
    rep.timezone_status = "DÉCLARÉ" if all(tz_declared) else ("PARTIEL" if any(tz_declared) else "ABSENT")
    if rep.timezone_status != "DÉCLARÉ":
        rep.warnings.append(f"fuseau horaire {rep.timezone_status.lower()}: les horaires seront marqués incertains, jamais convertis en silence")
    # Prêt pour B ? Il faut le minimum descriptif sur chaque transaction retenue.
    for f in sorted(REQUIRED_FOR_B):
        if rep.missing_by_field.get(f, 0):
            rep.b_blockers.append(f"champ indispensable à B manquant sur au moins une transaction: {f}")
    rep.b_ready = not rep.b_blockers
    claims = raw.get("claims", [])
    missing = raw.get("missing_information", [])
    auto_missing = [f for f, n in rep.missing_by_field.items() if n == len(trades)]
    for f in auto_missing:
        if f not in missing:
            missing.append(f"champ absent sur toutes les transactions: {f}")
    dossier = engine_a_ingest(trades, claims, missing, raw.get("selection_process", "non documenté"))
    rep.dossier_id = dossier.envelope.object_id
    rep.accepted = True
    return dossier, rep
