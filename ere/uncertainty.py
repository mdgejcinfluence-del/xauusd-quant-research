"""Inférence sous incertitude (ERE-INTELLIGENCE-001).

Philosophie: ne jamais inventer ce qu'on ignore, ne jamais renoncer à
apprendre ce qui reste identifiable. Trois outils, par ordre de
préférence:
1. Identification partielle: quand une donnée manque, calculer les
   bornes de ce qui reste vrai dans tous les scénarios admissibles.
2. Scénarios conditionnels: chaque conclusion est étiquetée par le
   scénario sous lequel elle tient; aucun scénario n'est promu sans
   preuve documentaire externe.
3. Sensibilité: mesurer combien une conclusion bouge quand une
   hypothèse varie; une conclusion qui ne tient que sous un scénario
   fragile est rapportée comme fragile, pas comme fausse ni vraie.

Aucune probabilité numérique n'est produite sans modèle génératif
déclaré et calibré (règle des contrats: posterior exige likelihood).
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Scenario:
    scenario_id: str
    description: str
    base_documentaire: str  # d'où vient ce scénario (source, statut)
    statut: str = "CANDIDAT"  # CANDIDAT | DOCUMENTÉ | RÉFUTÉ | RETENU


@dataclass
class ConditionalConclusion:
    enonce: str
    scenario_id: str
    niveau_max: str = "N2"  # plafond de preuve sous incertitude non résolue


@dataclass
class SensitivityReport:
    question: str
    conclusions_par_scenario: list = field(default_factory=list)
    invariant: list = field(default_factory=list)   # vrai sous TOUS les scénarios admissibles
    fragile: list = field(default_factory=list)     # ne tient que sous certains scénarios
    observation_discriminante: str = ""

    def to_dict(self) -> dict:
        return {
            "question": self.question,
            "conclusions_par_scenario": [vars(c) for c in self.conclusions_par_scenario],
            "invariant_sous_tous_scenarios": self.invariant,
            "fragile_selon_scenario": self.fragile,
            "observation_qui_departagerait": self.observation_discriminante,
        }


def partial_identification_bounds(valeurs_par_scenario: dict) -> tuple:
    """Bornes de Manski: [min, max] d'une quantité à travers les scénarios admissibles.

    Ce qui est dans les bornes est identifiable partiellement; prétendre
    un point unique serait une invention.
    """
    if not valeurs_par_scenario:
        raise ValueError("Identification partielle: aucun scénario admissible fourni")
    vals = list(valeurs_par_scenario.values())
    return (min(vals), max(vals))


def classify_data_reliability(champs_connus: dict) -> str:
    """Décision adaptative: quelle confiance accorder à un dossier.

    UTILISABLE: champs indispensables présents et provenance complète.
    UTILISABLE_AVEC_RESERVES: descriptible mais alignement/identification limités.
    INSUFFISANT_POUR_IDENTIFICATION: ne peut nourrir que des hypothèses.
    """
    indispensables = ["instrument", "side", "open_time"]
    if any(not champs_connus.get(k) for k in indispensables):
        return "INSUFFISANT_POUR_IDENTIFICATION"
    if not champs_connus.get("timezone") or not champs_connus.get("open_price"):
        return "UTILISABLE_AVEC_RESERVES"
    return "UTILISABLE"


def prioritize_experiments(candidats: list) -> list:
    """Priorisation des expériences par valeur d'information attendue.

    Chaque candidat: {nom, hypotheses_departagees (int), cout_relatif (float),
    segment_disponible (bool)}. Score = hypothèses départagées / coût,
    uniquement si un segment autorisé existe. Heuristique documentée,
    pas une probabilité.
    """
    scored = []
    for c in candidats:
        if not c.get("segment_disponible"):
            scored.append({**c, "score": 0.0, "bloque": "aucun segment autorisé"})
        else:
            scored.append({**c, "score": c["hypotheses_departagees"] / max(c["cout_relatif"], 0.1), "bloque": None})
    return sorted(scored, key=lambda x: -x["score"])
