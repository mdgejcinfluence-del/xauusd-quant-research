"""Taxonomie officielle des niveaux de preuve META ALPHA ERE : N0-N7.

Adoptée en Phase 1 (décision D1). E0-E5 du dossier externe est conservé
comme correspondance secondaire, jamais comme échelle officielle :
E5 (protocole indépendant exécuté) est plus faible que N7.
"""
from enum import IntEnum


class EvidenceLevel(IntEnum):
    N0_SOURCE_NON_VERIFIEE = 0
    N1_FAIT_OBSERVE = 1
    N2_INFERENCE = 2
    N3_HYPOTHESE = 3
    N4_SIGNATURE_MESUREE = 4
    N5_MECANISME_ETAYE = 5
    N6_MECANISME_IDENTIFIE = 6
    N7_AVANTAGE_VALIDE = 7


# Correspondance secondaire vers l'échelle externe E0-E5 (lecture seule).
EXTERNAL_E_SCALE = {
    EvidenceLevel.N0_SOURCE_NON_VERIFIEE: "E0 CLAIM",
    EvidenceLevel.N1_FAIT_OBSERVE: "E1 OBSERVED",
    EvidenceLevel.N2_INFERENCE: "E1 OBSERVED (lecture)",
    EvidenceLevel.N3_HYPOTHESE: "E2 COMPATIBLE",
    EvidenceLevel.N4_SIGNATURE_MESUREE: "E2-E3 selon discrimination",
    EvidenceLevel.N5_MECANISME_ETAYE: "E3 DISCRIMINATED / E4 si répliqué",
    EvidenceLevel.N6_MECANISME_IDENTIFIE: "E4 REPLICATED",
    EvidenceLevel.N7_AVANTAGE_VALIDE: "E5 VALIDATED (seulement si indépendance + critères pré-déclarés + coûts complets)",
}

# Seul le moteur nommé peut attribuer ce niveau (le producteur ne se promeut pas).
PROMOTION_AUTHORITY = {
    EvidenceLevel.N1_FAIT_OBSERVE: {"B", "F"},
    EvidenceLevel.N2_INFERENCE: {"B"},
    EvidenceLevel.N3_HYPOTHESE: {"C"},
    EvidenceLevel.N4_SIGNATURE_MESUREE: {"F"},
    EvidenceLevel.N5_MECANISME_ETAYE: {"G"},
    EvidenceLevel.N6_MECANISME_IDENTIFIE: {"G"},
    EvidenceLevel.N7_AVANTAGE_VALIDE: {"I-A"},
}

# Qualifications constitutionnelles rendues par G (Constitution §9).
G_QUALIFICATIONS = {
    "DEMONTRÉ",
    "FORTEMENT ÉTAYÉ",
    "COMPATIBLE MAIS NON IDENTIFIÉ",
    "NON DÉMONTRABLE AVEC LES DONNÉES DISPONIBLES",
    "RÉFUTÉ",
}


def check_promotion(engine: str, level: EvidenceLevel) -> None:
    """Lève ValueError si `engine` n'a pas autorité pour attribuer `level`."""
    allowed = PROMOTION_AUTHORITY.get(level, set())
    if engine not in allowed:
        raise ValueError(
            f"Promotion interdite: le moteur {engine} ne peut pas attribuer "
            f"{level.name} (autorité: {sorted(allowed) or 'aucune'})"
        )


def aggregate_level(levels) -> EvidenceLevel:
    """Un objet composite hérite du niveau le plus faible de ses ingrédients."""
    levels = list(levels)
    if not levels:
        raise ValueError("Agrégation impossible: aucun niveau fourni")
    return min(levels)
