"""Taxonomie des familles scientifiques — EXTRAITE du dossier, pas inventée.

Provenance de chaque élément :

- Les 8 familles admissibles viennent du **§4.2 du dossier de stratégie**
  (« Familles de variables initialement admissibles », items 1 à 8).
- Les champs interdits viennent du **§4.1** (« il est interdit de prétendre
  mesurer directement, avec Bid/Ask seulement »).
- Les familles différées viennent du **§2.2** (sources hors périmètre).

⚠ DISTINCTION CAPITALE, et correction d'une erreur d'analyse précédente :

    `scientific_families_undefined = 19` est un champ du **certificat Phase 2
    hérité**. Il décrit l'état de l'ANCIEN Formula Registry de la Base DGP,
    qui est hors périmètre (le dossier demande explicitement de l'ignorer).
    Il ne s'agit PAS de 19 familles que le propriétaire devrait définir.

    La nouvelle chaîne analytique définit ses familles au §4.2 : il y en a 8,
    et elles sont déjà écrites. Le système peut donc les instancier seul.

Ce module ne contient donc AUCUNE formule : uniquement la structure dérivée
du texte, et les emplacements de paramètres laissés explicitement vides.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

PROVENANCE_FAMILIES = "dossier §4.2 'Familles de variables initialement admissibles'"
PROVENANCE_FORBIDDEN = "dossier §4.1 'il est interdit de prétendre mesurer directement'"
PROVENANCE_DEFERRED = "dossier §2.2 'sources hors du chemin critique'"


# ---------------------------------------------------------------------------
# Champs canoniques attendus dans le corpus (détectés, jamais supposés)
# ---------------------------------------------------------------------------
FIELD_ALIASES: dict[str, tuple[str, ...]] = {
    "timestamp": ("timestamp", "time", "ts", "datetime", "date_time", "event_time", "utc"),
    "bid": ("bid", "bid_price", "bidprice", "b"),
    "ask": ("ask", "ask_price", "askprice", "a", "offer"),
}

# Champs dont le dossier interdit de prétendre qu'ils sont mesurables (§4.1)
FORBIDDEN_FIELDS: dict[str, str] = {
    "volume": "volume réellement échangé",
    "volume_bid": "volume réellement échangé",
    "volume_ask": "volume réellement échangé",
    "tick_volume": "volume réellement échangé",
    "delta": "delta acheteur/vendeur (aggressor delta)",
    "aggressor": "delta acheteur/vendeur (aggressor delta)",
    "depth": "profondeur du carnet",
    "book_depth": "profondeur du carnet",
    "queue": "priorité dans la file d'attente",
    "open": "substitution OHLC (interdite)",
    "high": "substitution OHLC (interdite)",
    "low": "substitution OHLC (interdite)",
    "close": "substitution OHLC (interdite)",
}


# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class Decision:
    """Une décision de préenregistrement. Le système NE LA PREND PAS.

    Il la présente. Le propriétaire choisit un nombre. C'est la seule chose
    qui reste à sa charge — et c'est volontairement une courte liste.
    """

    decision_id: str
    family_id: str
    question: str
    why_it_matters: str
    required_by: str = "SPECIFIED"
    example_values: tuple[str, ...] = ()
    default_is: str = "AUCUN_DEFAUT"


@dataclass(frozen=True)
class Family:
    family_id: str
    number: int
    name: str
    requires_fields: tuple[str, ...]
    derivable_if: str
    candidate_variables: tuple[dict[str, Any], ...] = ()
    decisions: tuple[Decision, ...] = ()
    note: str = ""


# ---------------------------------------------------------------------------
# Les 8 familles du §4.2, avec leurs variables candidates.
# `parameters: None` est VOLONTAIRE : aucune fenêtre, aucun horizon n'est
# fixé ici. Ce sont les décisions listées dans `decisions`.
# ---------------------------------------------------------------------------
FAMILIES: tuple[Family, ...] = (
    Family(
        family_id="F1_PRIX_COTATIONS",
        number=1,
        name="Prix et cotations",
        requires_fields=("bid", "ask"),
        derivable_if="bid et ask présents",
        candidate_variables=(
            {"variable_id": "SPREAD_ABS", "role": "feature",
             "definition": "ask - bid", "parameters": {}, "timestamps_needed": ("bid", "ask")},
            {"variable_id": "SPREAD_REL", "role": "feature",
             "definition": "(ask - bid) / mid", "parameters": {}, "timestamps_needed": ("bid", "ask")},
            {"variable_id": "MID", "role": "diagnostic",
             "definition": "(bid + ask) / 2", "parameters": {}, "timestamps_needed": ("bid", "ask")},
        ),
        note="Aucune décision requise : formules fermées, sans paramètre.",
    ),
    Family(
        family_id="F2_RENDEMENTS",
        number=2,
        name="Rendements et direction",
        requires_fields=("timestamp", "bid", "ask"),
        derivable_if="mid + timestamp disponibles",
        candidate_variables=(
            {"variable_id": "RET_TICK", "role": "label",
             "definition": "mid[t+1] / mid[t] - 1", "parameters": {},
             "timestamps_needed": ("mid", "timestamp")},
            {"variable_id": "RET_H", "role": "label",
             "definition": "mid[t+H] / mid[t] - 1", "parameters": {"H": None},
             "timestamps_needed": ("mid", "timestamp")},
        ),
        decisions=(
            Decision(
                decision_id="D_HORIZONS",
                family_id="F2_RENDEMENTS",
                question="Quels horizons temporels de label préenregistrer ?",
                why_it_matters="Le dossier exige « un petit ensemble d'horizons préenregistrés ». "
                               "Chaque horizon ajouté augmente la multiplicité des tests et le purge "
                               "nécessaire entre IS et OOS.",
                example_values=("1s", "5s", "30s", "1min", "5min"),
            ),
        ),
    ),
    Family(
        family_id="F3_VOLATILITE",
        number=3,
        name="Volatilité et variation",
        requires_fields=("bid", "ask"),   # mid est DÉRIVÉ de bid/ask : c'est ce qu'on vérifie

        derivable_if="mid + timestamp disponibles",
        candidate_variables=(
            {"variable_id": "ROLL_STD_MID", "role": "feature",
             "definition": "écart-type roulant des variations de mid sur N événements",
             "parameters": {"N": None, "warmup": None}, "timestamps_needed": ("mid",)},
            {"variable_id": "ROLL_RANGE_MID", "role": "feature",
             "definition": "max(mid) - min(mid) sur fenêtre N", "parameters": {"N": None},
             "timestamps_needed": ("mid",)},
        ),
        decisions=(
            Decision(
                decision_id="D_FENETRES_VOL",
                family_id="F3_VOLATILITE",
                question="Quelles fenêtres roulantes (en événements, pas en secondes) ?",
                why_it_matters="Le dossier exige « fenêtre, warm-up et politique NULL fixés ». "
                               "Sans ce choix, aucune variable de cette famille ne peut passer "
                               "au statut SPECIFIED.",
                example_values=("50", "100", "500", "1000"),
            ),
            Decision(
                decision_id="D_WARMUP_NULL",
                family_id="F3_VOLATILITE",
                question="Politique pendant le warm-up : NULL ou première valeur valide ?",
                why_it_matters="Un remplissage par la première valeur crée une information "
                               "artificielle au début de chaque partition.",
                example_values=("NULL", "DROP_ROWS"),
            ),
        ),
    ),
    Family(
        family_id="F4_SAUTS_EXTREMES",
        number=4,
        name="Sauts et extrêmes",
        requires_fields=("bid", "ask"),
        derivable_if="mid (dérivé de bid/ask) disponible",
        candidate_variables=(
            {"variable_id": "ZSCORE_ROBUST", "role": "feature",
             "definition": "(retour - médiane roulante) / MAD roulante",
             "parameters": {"fenetre_retour": None, "seuil": None},
             "timestamps_needed": ("mid",)},
        ),
        decisions=(
            Decision(
                decision_id="D_SEUIL_SAUT",
                family_id="F4_SAUTS_EXTREMES",
                question="Quel seuil définit un « saut » (en z robuste) ?",
                why_it_matters="Le seuil définit la population d'événements étudiée. "
                               "Il doit être fixé AVANT de regarder les résultats, "
                               "sinon on le choisit pour obtenir un bon résultat.",
                example_values=("3", "4", "5", "6"),
            ),
        ),
    ),
    Family(
        family_id="F5_MICROSTRUCTURE",
        number=5,
        name="Microstructure des cotations",
        requires_fields=("timestamp", "bid", "ask"),
        derivable_if="timestamp + bid/ask disponibles",
        candidate_variables=(
            {"variable_id": "UPDATE_INTENSITY", "role": "feature",
             "definition": "nombre de mises à jour de cotation sur T secondes",
             "parameters": {"T": None}, "timestamps_needed": ("timestamp",)},
            {"variable_id": "INTERARRIVAL_MEAN", "role": "feature",
             "definition": "moyenne des écarts temporels entre événements sur N événements",
             "parameters": {"N": None}, "timestamps_needed": ("timestamp",)},
            {"variable_id": "SPREAD_REGIME", "role": "feature",
             "definition": "classe de spread observé (quantiles sur le PASSÉ uniquement)",
             "parameters": {"n_classes": None, "fenetre": None}, "timestamps_needed": ("bid", "ask")},
        ),
        decisions=(
            Decision(
                decision_id="D_INTENSITE_T",
                family_id="F5_MICROSTRUCTURE",
                question="Sur quelle durée mesurer l'intensité des mises à jour ?",
                why_it_matters="Cette durée doit être exprimée en temps, pas en nombre "
                               "d'événements, sinon la mesure dépend du régime de marché.",
                example_values=("1s", "5s", "30s"),
            ),
            Decision(
                decision_id="D_REGIME_SPREAD",
                family_id="F5_MICROSTRUCTURE",
                question="Combien de classes de spread, et sur quelle fenêtre les estimer ?",
                why_it_matters="Les classes doivent être apprises sur le passé autorisé "
                               "seulement, sinon fuite d'information.",
                example_values=("3 classes / 1 jour", "3 classes / 1 semaine", "5 classes / 1 jour"),
            ),
        ),
    ),
    Family(
        family_id="F6_STRUCTURE_TEMPORELLE",
        number=6,
        name="Structure temporelle",
        requires_fields=("timestamp",),
        derivable_if="timestamp + timezone et règles de session DOCUMENTÉES",
        candidate_variables=(
            {"variable_id": "SUBPERIODE", "role": "diagnostic",
             "definition": "découpage en sous-périodes calendaires",
             "parameters": {"granularite": None}, "timestamps_needed": ("timestamp",)},
        ),
        decisions=(
            Decision(
                decision_id="D_TIMEZONE_SESSIONS",
                family_id="F6_STRUCTURE_TEMPORELLE",
                question="Timezone de référence et règles de session : documentées ou non ?",
                why_it_matters="Le dossier interdit toute analyse de session si la timezone "
                               "et les frontières ne sont pas documentées. Sans réponse, "
                               "cette famille entière reste DEFERRED.",
                example_values=("UTC + aucune session", "UTC + sessions documentées", "DEFERRED"),
            ),
        ),
        note="Sans décision explicite, cette famille reste DEFERRED — et ce n'est pas bloquant.",
    ),
    Family(
        family_id="F7_REGIMES",
        number=7,
        name="Régimes et transitions",
        requires_fields=("timestamp", "bid", "ask"),
        derivable_if="features F3 et F5 disponibles",
        candidate_variables=(
            {"variable_id": "REGIME_CLASS", "role": "feature",
             "definition": "classe de régime apprise sur le PASSÉ autorisé uniquement",
             "parameters": {"methode": None, "n_regimes": None, "fenetre_entrainement": None},
             "timestamps_needed": ("mid", "timestamp")},
        ),
        decisions=(
            Decision(
                decision_id="D_METHODE_REGIME",
                family_id="F7_REGIMES",
                question="Quelle méthode de détection de régime (et combien de régimes) ?",
                why_it_matters="Le dossier exige que les régimes soient « estimés uniquement avec "
                               "les données disponibles dans la fenêtre d'entraînement ». "
                               "Le choix de méthode doit être préenregistré.",
                example_values=("quantiles de volatilité / 3", "HMM / 3", "DEFERRED"),
            ),
        ),
        note="Dépend de F3 et F5 : reste DEFERRED tant que leurs paramètres ne sont pas fixés.",
    ),
    Family(
        family_id="F8_LABELS",
        number=8,
        name="Labels de résultat futur",
        requires_fields=("timestamp", "bid", "ask"),
        derivable_if="mid + timestamp + horizon fixé",
        candidate_variables=(
            {"variable_id": "MFE_H", "role": "label",
             "definition": "excursion favorable maximale sur l'horizon H", "parameters": {"H": None},
             "timestamps_needed": ("mid", "timestamp")},
            {"variable_id": "MAE_H", "role": "label",
             "definition": "excursion adverse maximale sur l'horizon H", "parameters": {"H": None},
             "timestamps_needed": ("mid", "timestamp")},
        ),
        decisions=(
            Decision(
                decision_id="D_HORIZON_LABEL",
                family_id="F8_LABELS",
                question="Quel horizon de détention pour MFE/MAE ?",
                why_it_matters="Cet horizon détermine le PURGE obligatoire entre IS et OOS "
                               "(dossier §7.2). Il ne peut pas être changé après avoir vu les résultats.",
                example_values=("30s", "5min", "1h"),
            ),
        ),
        note="Les labels sont physiquement séparés des features : jamais joints dans un même calcul.",
    ),
)

FAMILY_INDEX = {f.family_id: f for f in FAMILIES}


# ---------------------------------------------------------------------------
# Familles explicitement différées (§2.2) : dépendances externes hors périmètre
# ---------------------------------------------------------------------------
DEFERRED_EXTERNAL: tuple[dict[str, str], ...] = (
    {"name": "COMEX / GC futures", "status": "DEFERRED_EXTERNAL_DEPENDENCY"},
    {"name": "DXY exact", "status": "DEFERRED_EXTERNAL_DEPENDENCY"},
    {"name": "LBMA fixings", "status": "DEFERRED_EXTERNAL_DEPENDENCY"},
    {"name": "Macro point-in-time", "status": "DEFERRED_EXTERNAL_DEPENDENCY"},
    {"name": "Taux d'intérêt", "status": "DEFERRED_EXTERNAL_DEPENDENCY"},
    {"name": "VIX", "status": "DEFERRED_EXTERNAL_DEPENDENCY"},
    {"name": "Indices actions", "status": "DEFERRED_EXTERNAL_DEPENDENCY"},
    {"name": "Autres marchés", "status": "DEFERRED_EXTERNAL_DEPENDENCY"},
)


def all_decisions() -> list[Decision]:
    """Toutes les décisions de préenregistrement, à plat."""
    return [d for f in FAMILIES for d in f.decisions]


def decisions_by_family() -> dict[str, list[Decision]]:
    out: dict[str, list[Decision]] = {}
    for d in all_decisions():
        out.setdefault(d.family_id, []).append(d)
    return out


def summary() -> dict:
    """Vue synthétique : ce que le système peut faire seul, et ce qui reste."""
    return {
        "provenance": {
            "families": PROVENANCE_FAMILIES,
            "forbidden_fields": PROVENANCE_FORBIDDEN,
            "deferred": PROVENANCE_DEFERRED,
        },
        "families_total": len(FAMILIES),
        "deferred_external_total": len(DEFERRED_EXTERNAL),
        "candidate_variables_total": sum(len(f.candidate_variables) for f in FAMILIES),
        "decisions_total": len(all_decisions()),
        "legacy_counter_note": (
            "scientific_families_undefined=19 appartient au certificat Phase 2 hérité "
            "et à l'ancien Formula Registry (hors périmètre). Ce n'est pas une liste "
            "de familles à définir par le propriétaire."
        ),
    }
