"""Contrats typés META ALPHA ERE (Phase 1, décision D10).

Dataclasses stdlib avec validation explicite. Chaque objet porte :
schema_version, identifiant, niveau de preuve, provenance.
Versionnement SemVer des schémas (D11) : major = rupture.
Aucune coercition silencieuse (fuseaux, unités, pourcentages).
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field, asdict
from typing import Any, Optional

from .taxonomy import EvidenceLevel, G_QUALIFICATIONS, check_promotion

SCHEMA_VERSION = "1.0.0"


def content_hash(obj: dict) -> str:
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, ensure_ascii=False, default=str).encode()
    ).hexdigest()


@dataclass
class ArtifactRef:
    uri: str
    sha256: str
    size_bytes: int
    role: str

    def validate(self) -> None:
        if len(self.sha256) != 64:
            raise ValueError("ArtifactRef: sha256 doit faire 64 caractères hex")
        if self.size_bytes < 0:
            raise ValueError("ArtifactRef: taille négative")


@dataclass
class Envelope:
    object_id: str
    producer: str
    evidence_level: EvidenceLevel
    schema_version: str = SCHEMA_VERSION
    parents: list = field(default_factory=list)
    artifacts: list = field(default_factory=list)
    warnings: list = field(default_factory=list)

    def validate(self) -> None:
        check_promotion(self.producer, self.evidence_level)
        for a in self.artifacts:
            a.validate()


@dataclass
class TraderDossier:
    envelope: Envelope
    trades: list  # chaque trade: dict avec champs ou None explicite (jamais inventé)
    claims: list  # statistiques publiques: toujours verified=False
    missing_information: list
    selection_process: str

    def validate(self) -> None:
        self.envelope.validate()
        for c in self.claims:
            if c.get("verified") is not False:
                raise ValueError("TraderDossier: une claim publique ne peut pas être verified=True à l'ingestion")
        for t in self.trades:
            if t.get("open_time") and t.get("close_time") and t["close_time"] < t["open_time"]:
                raise ValueError("TraderDossier: close_time < open_time")


@dataclass
class MarketWindow:
    """Fenêtre de ticks consommée par B (décision D5). Bornes déclarées avant extraction."""

    envelope: Envelope
    dossier_id: str
    transaction_ref: str
    source: str
    start_utc: str
    end_utc: str
    justification_bornes: str
    champs: list
    qualite: dict

    def validate(self) -> None:
        self.envelope.validate()
        if self.envelope.evidence_level > EvidenceLevel.N2_INFERENCE:
            raise ValueError("MarketWindow: plafond de preuve N2 (contexte descriptif)")
        if self.end_utc <= self.start_utc:
            raise ValueError("MarketWindow: end <= start")
        if not self.justification_bornes:
            raise ValueError("MarketWindow: justification des bornes obligatoire avant extraction")


@dataclass
class BehaviorProfile:
    envelope: Envelope
    dossier_ref: str
    facts: list  # chacun pointe vers transaction/window
    interpretations: list  # jamais mélangées aux faits
    market_window_refs: list

    def validate(self) -> None:
        self.envelope.validate()
        if self.envelope.evidence_level > EvidenceLevel.N2_INFERENCE:
            raise ValueError("BehaviorProfile: B plafonne à N2")


@dataclass
class HypothesisSet:
    envelope: Envelope
    behavior_ref: str
    hypotheses: list  # >=2, chacune avec prédictions divergentes
    includes_unknown: bool = True

    def validate(self) -> None:
        self.envelope.validate()
        if len(self.hypotheses) < 2 and not self.includes_unknown:
            raise ValueError("HypothesisSet: au moins 2 hypothèses ou l'hypothèse inconnue explicite")
        ids = [h["hypothesis_id"] for h in self.hypotheses]
        if len(ids) != len(set(ids)):
            raise ValueError("HypothesisSet: hypothesis_id dupliqués")
        for h in self.hypotheses:
            if h.get("posterior") is not None and not (h.get("likelihood_spec") and h.get("selection_model")):
                raise ValueError("HypothesisSet: posterior interdit sans likelihood_spec + selection_model")


@dataclass
class AvisDeTestabilite:
    valeur: str  # TESTABLE | TESTABLE_SOUS_CONDITION | NON_TESTABLE_EN_L_ETAT
    motif: str
    donnee_manquante: Optional[str] = None
    contre_signe_par_g: bool = False

    def validate(self) -> None:
        if self.valeur not in {"TESTABLE", "TESTABLE_SOUS_CONDITION", "NON_TESTABLE_EN_L_ETAT"}:
            raise ValueError("AvisDeTestabilite: valeur hors énumération")
        if self.valeur == "NON_TESTABLE_EN_L_ETAT" and not self.motif:
            raise ValueError("AvisDeTestabilite: motif obligatoire")


@dataclass
class ExperimentPlan:
    envelope: Envelope
    hypothesis_ids: list
    protocole: dict  # définitions, grilles fixées, critères pré-déclarés
    segment_autorise: str  # découverte|construction|validation|prospectif
    avis: AvisDeTestabilite
    plan_hash: str = ""

    def validate(self) -> None:
        self.envelope.validate()
        self.avis.validate()
        if self.segment_autorise not in {"découverte", "construction", "validation", "prospectif"}:
            raise ValueError("ExperimentPlan: segment inconnu")
        expected = content_hash({"hypothesis_ids": self.hypothesis_ids, "protocole": self.protocole, "segment": self.segment_autorise})
        if self.plan_hash and self.plan_hash != expected:
            raise ValueError("ExperimentPlan: plan_hash ne correspond pas au contenu (protocole modifié après gel)")
        self.plan_hash = expected


@dataclass
class SignatureReport:
    envelope: Envelope
    plan_ref: str
    run_id: str
    status: str  # MEASURED | NOT_EXECUTED
    mesures: Optional[dict]
    segment: str
    couts_ordre_de_grandeur: Optional[dict]  # décision D7: filtre, pas une mesure d'edge

    def validate(self) -> None:
        self.envelope.validate()
        if self.status == "NOT_EXECUTED" and self.mesures is not None:
            raise ValueError("SignatureReport: NOT_EXECUTED ne peut porter aucun chiffre de mesure")
        if self.status == "MEASURED" and not self.mesures:
            raise ValueError("SignatureReport: MEASURED exige des mesures")
        if self.status == "MEASURED" and self.couts_ordre_de_grandeur is None:
            raise ValueError("SignatureReport: bloc coût d'ordre de grandeur obligatoire (D7)")


# Liste fermée des entrées recevables par G (décision D3).
G_ALLOWED_INPUTS = {
    "BehaviorProfile", "HypothesisSet", "ExperimentPlan", "SignatureReport",
    "MarketWindow", "KnowledgeRef", "ModelRegistryState", "DossierState",
}


@dataclass
class ModelDossier:
    envelope: Envelope
    input_refs: list  # liste de (type_objet, object_id, hash)
    qualification: str
    compatibles: list
    rejetes: list
    non_identifies: list
    candidat_h: bool = False

    def validate(self) -> None:
        self.envelope.validate()
        if self.qualification not in G_QUALIFICATIONS:
            raise ValueError("ModelDossier: qualification hors vocabulaire constitutionnel")
        for type_objet, _oid, _h in self.input_refs:
            if type_objet not in G_ALLOWED_INPUTS:
                raise ValueError(f"ModelDossier: pièce non recevable par G: {type_objet}")
        if self.candidat_h and self.envelope.evidence_level < EvidenceLevel.N5_MECANISME_ETAYE:
            raise ValueError("ModelDossier: la porte H exige au minimum N5 (mécanisme étayé)")


@dataclass
class EngineSpec:
    envelope: Envelope
    model_dossier_ref: str
    but: str  # RESEARCH_ONLY | PAPER_ONLY
    regles_hash: str
    approval: Optional[dict]  # (model_hash, protocol_hash, approbateur, expiration)

    def validate(self) -> None:
        self.envelope.validate()
        if self.but not in {"RESEARCH_ONLY", "PAPER_ONLY"}:
            raise ValueError("EngineSpec: but hors énumération (aucun connecteur de trading)")
        if not self.approval:
            raise ValueError("EngineSpec: approbation du fondateur obligatoire (porte H)")


@dataclass
class ValidationVerdict:
    envelope: Envelope
    engine_spec_ref: str
    decision: str  # VALIDATION RÉUSSIE | PARTIELLEMENT FAVORABLE | NON CONCLUANT | RÉFUTÉE | DONNÉES INSUFFISANTES | NOT_IDENTIFIED
    mesures_numeriques: Optional[dict]
    criteres_predeclares: dict

    def validate(self) -> None:
        self.envelope.validate()
        if self.decision == "VALIDATION RÉUSSIE" and not self.mesures_numeriques:
            raise ValueError("ValidationVerdict: un positif exige des preuves numériques mesurées")
        if self.decision == "VALIDATION RÉUSSIE" and not self.criteres_predeclares:
            raise ValueError("ValidationVerdict: critères pré-déclarés obligatoires")


@dataclass
class DossierState:
    """État de reprise d'un dossier (décision D6)."""

    dossier_id: str
    etape_courante: str
    objets_produits: list  # (type, object_id, hash, niveau)
    segments_consommes: list
    experiences_ouvertes: list
    prochaine_action_autorisee: str

    def to_dict(self) -> dict:
        return asdict(self)
