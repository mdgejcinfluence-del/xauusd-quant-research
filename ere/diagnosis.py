"""Diagnostic des échecs de recherche (EXPANSION-001, axe 3).

Quand une recherche ne trouve rien, distinguer pourquoi — au lieu de
conclure 'pas de mécanisme'. Taxonomie A-H de la mission, appliquée à
partir d'évidences mesurées, jamais d'impressions.
"""
from __future__ import annotations

MODES = {
    "A": "absence de signal détectable dans les données",
    "B": "signal trop faible pour les données disponibles (puissance)",
    "C": "signal présent uniquement dans certains régimes",
    "D": "représentation des données inadaptée",
    "E": "méthode statistique inadaptée",
    "F": "hypothèse mal formulée",
    "G": "résultat non reproductible entre segments",
    "H": "signature détectable mais inexploitable après coûts",
}


def diagnose(evidence: dict) -> dict:
    """evidence: {effet_decouverte, effet_validation, effet_confirmation,
    signe_stable (bool), par_regime (dict|None), puissance_suffisante (bool),
    couts_disponibles (bool), marge_brute_bp, cout_bp, representation_testee (bool)}"""
    eff = [evidence.get("effet_decouverte"), evidence.get("effet_validation"), evidence.get("effet_confirmation")]
    eff = [e for e in eff if e is not None]
    if evidence.get("marge_brute_bp") is not None and evidence.get("couts_disponibles"):
        if evidence["marge_brute_bp"] <= evidence.get("cout_bp", 0):
            return {"mode": "H", "libelle": MODES["H"], "experience_suivante": "chercher une géométrie à plus grande marge ou un filtrage à l'entrée"}
    if eff and not evidence.get("signe_stable", True):
        return {"mode": "G", "libelle": MODES["G"], "experience_suivante": "répliquer sur partitions par année civile avant tout classement"}
    if evidence.get("par_regime") and any(v for v in evidence["par_regime"].values()):
        return {"mode": "C", "libelle": MODES["C"], "experience_suivante": "conditionner l'expérience au régime où l'effet apparaît, protocole séparé"}
    if eff and all(abs(e) < 1e-12 for e in eff):
        if not evidence.get("puissance_suffisante", True):
            return {"mode": "B", "libelle": MODES["B"], "experience_suivante": "augmenter la couverture ou regrouper les épisodes avant de conclure"}
        return {"mode": "A", "libelle": MODES["A"], "experience_suivante": "tester une autre représentation (échelle, variable) avant d'abandonner la famille"}
    if not evidence.get("representation_testee", True):
        return {"mode": "D", "libelle": MODES["D"], "experience_suivante": "changer de représentation (barres temporelles -> barres d'activité, par exemple)"}
    return {"mode": "F", "libelle": MODES["F"], "experience_suivante": "reformuler l'hypothèse avec une prédiction divergente mesurable"}
