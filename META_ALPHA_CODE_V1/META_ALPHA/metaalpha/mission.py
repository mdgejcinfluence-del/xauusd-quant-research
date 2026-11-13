"""Le contrat de mission — la fiche V2 transformée en structure exécutable.

Ce module est la source unique de vérité de l'architecture. Le schéma HTML est
GÉNÉRÉ depuis ces données : il ne peut donc pas dériver du code, ni promettre
une phase que le code ne connaît pas.

Trois couches à ne jamais confondre (fiche §2) :
  A. META_ALPHA_RESEARCH_PORTFOLIO   — recherche scientifique indépendante
  B. META_ALPHA_PORTFOLIO            — combinaison des edges validés
  C. BLUE_GUARDIAN_CHALLENGE_ADAPTER — compatibilité et exécution

Règle cardinale : la couche C ne modifie jamais les résultats de A. Une
incompatibilité produit une version d'adaptation séparée, elle-même testée.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

# ---------------------------------------------------------------------------
# Couches
# ---------------------------------------------------------------------------
LAYERS: tuple[dict[str, str], ...] = (
    {
        "id": "A",
        "name": "RECHERCHE SCIENTIFIQUE",
        "object": "META_ALPHA_RESEARCH_PORTFOLIO",
        "question": "Quelles régularités existent, sont causales, stables et survivent aux coûts ?",
        "phases": "P2 → P6",
        "influence_externe": "AUCUNE — le challenge ne dicte pas ce que le moteur trouve",
    },
    {
        "id": "B",
        "name": "PORTEFEUILLE",
        "object": "META_ALPHA_PORTFOLIO",
        "question": "Quels edges se complètent réellement, et avec quels poids gelés sans fuite ?",
        "phases": "P7",
        "influence_externe": "AUCUNE — les poids viennent des données autorisées, jamais du challenge",
    },
    {
        "id": "C",
        "name": "ADAPTATEUR BLUE GUARDIAN",
        "object": "BLUE_GUARDIAN_CHALLENGE_ADAPTER",
        "question": "Ce portefeuille gelé est-il exécutable dans les règles confirmées du compte ?",
        "phases": "P8 → P9",
        "influence_externe": "RÈGLES DU CHALLENGE — postérieures, jamais rétroactives sur A et B",
    },
)


# ---------------------------------------------------------------------------
# Phases — ordre exact de la fiche §12
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class PhaseSpec:
    phase_id: str
    rank: int
    layer: str
    title: str
    question: str
    entry_gate: str
    exit_gate: str
    automated: tuple[str, ...]
    human_only: tuple[str, ...]
    artifacts: tuple[str, ...]
    forbidden: tuple[str, ...] = ()
    on_failure: str = ""
    produces_human_decision: bool = False


PHASES: tuple[PhaseSpec, ...] = (
    PhaseSpec(
        phase_id="P1_CERTIFIED",
        rank=0,
        layer="A",
        title="Source primaire XAUUSD (héritée)",
        question="La source native Dukascopy Bid/Ask est-elle certifiée ?",
        entry_gate="—",
        exit_gate="CERTIFIED (déjà acquis)",
        automated=("relire le certificat", "recalculer le SHA-256", "confirmer les 11 136 fichiers"),
        human_only=(),
        artifacts=("04_CHECKPOINTS/PHASE_01_XAUUSD_PRIMARY_CERTIFIED.json",),
        forbidden=("reconstruire la source", "re-télécharger", "modifier le certificat"),
        on_failure="ARRET_IMMEDIAT — baseline non certifiée",
    ),
    PhaseSpec(
        phase_id="P2H_CERTIFIED",
        rank=1,
        layer="A",
        title="DGP Base chronologique V5R10 (héritée)",
        question="La base 685 118 625 ticks / 348 partitions est-elle certifiée ?",
        entry_gate="—",
        exit_gate="CERTIFIED (déjà acquis)",
        automated=("relire le certificat", "recalculer le SHA-256", "compter les 348 partitions"),
        human_only=(),
        artifacts=("04_CHECKPOINTS/PHASE_02_DGP_BASE_CHRONOLOGICAL_VALIDATED_V5R10.json",),
        forbidden=("reconstruire la DGP", "ouvrir le Holdout", "modifier le certificat"),
        on_failure="ARRET_IMMEDIAT",
    ),
    PhaseSpec(
        phase_id="P2_ANALYTICAL",
        rank=2,
        layer="A",
        title="Phase 2 analytique V1 — construire la couche scientifique",
        question="Les variables tick-only sont-elles définies, causales et disponibles au mining ?",
        entry_gate="P1 + P2H CERTIFIED, hashes reconfirmés, 348 partitions lisibles",
        exit_gate="GATE P2→P3 : toutes les variables AVAILABLE_FOR_MINING ont un audit causal PASS",
        automated=(
            "préflight hashé (certificats + partitions)",
            "inventaire et détection de schéma réel",
            "sémantique des quotes (fuseau, précision, doublons, gaps, quotes invalides)",
            "granularité et dérivés Parquet versionnés",
            "instanciation des 8 familles et des variables dérivables",
            "split temporel 60/20/20 calculé et gelé",
            "purge/embargo fondé sur le plus long horizon",
            "audit causal automatique de chaque variable",
            "rapport de fin de phase",
        ),
        human_only=(
            "répondre aux 9 décisions de définition (10 min, une fois)",
            "accepter ou refuser la Phase 2 après revue",
        ),
        artifacts=(
            "BASELINE_HASH_MANIFEST.json",
            "QUOTE_DGP_SPEC_V1.md",
            "GRANULARITY_SPEC_V1.json",
            "DGP_VARIABLE_REGISTRY_V1.json",
            "FORMULA_REGISTRY_V1.json",
            "VALIDATION_SPLITS_V1.json",
            "DGP_REPORT.json",
            "P2_TO_P3_GATE_V1.json",
        ),
        forbidden=(
            "inventer une formule pour remplir une famille",
            "modifier une variable après avoir vu un résultat",
            "ouvrir le Holdout",
            "split aléatoire",
        ),
        on_failure="BLOCKED_WITH_RESUME — la phase suivante reste fermée",
        produces_human_decision=True,
    ),
    PhaseSpec(
        phase_id="P3_MINING",
        rank=3,
        layer="A",
        title="Mining préenregistré",
        question="Quelles anomalies apparaissent dans les données, sur les seules variables disponibles ?",
        entry_gate="P2_TO_P3_GATE_V1 = PASS et revue propriétaire",
        exit_gate="tous les essais enregistrés (positifs, négatifs, nuls) + candidats listés",
        automated=(
            "inscrire chaque essai au Trial Ledger AVANT exécution",
            "exécuter uniquement sur variables AVAILABLE_FOR_MINING",
            "calculer baseline et contrôle négatif pour chaque essai",
            "conserver les essais négatifs et non concluants",
            "produire le registre des anomalies candidates",
        ),
        human_only=("accepter la Phase 3",),
        artifacts=(
            "ANOMALY_CANDIDATE_REGISTRY.json",
            "REJECTED_AND_INCONCLUSIVE.csv",
            "TRIAL_LEDGER.csv",
            "MINING_REPORT.json",
        ),
        forbidden=(
            "ouvrir le Holdout",
            "essai non préenregistré",
            "supprimer un essai négatif",
            "appeler un candidat un edge",
        ),
        on_failure="NO_CANDIDATE reste un résultat valide",
    ),
    PhaseSpec(
        phase_id="P4_VALIDATION",
        rank=4,
        layer="A",
        title="Candidat → stratégie, et causalité",
        question="Le pouvoir prédictif survit-il au OOS, au walk-forward et au replay Bid/Ask ?",
        entry_gate="Phase 3 acceptée",
        exit_gate="chaque candidat a un contrat d'exécution et des tests anti-look-ahead PASS",
        automated=(
            "spécifier activation/direction/timestamp de décision/entrée/sortie/invalidation",
            "vérifier la disponibilité de chaque feature au timestamp de décision",
            "IS + OOS chronologique + walk-forward",
            "statistiques adaptées à la dépendance temporelle et à la multiplicité",
            "replay événementiel Bid/Ask (achat à l'Ask, vente au Bid)",
            "séparer spread / commission / swap / slippage / latence",
        ),
        human_only=("accepter la Phase 4",),
        artifacts=(
            "CAUSALITY_REPORT.json",
            "WALK_FORWARD_RESULTS.parquet",
            "TRADE_LEDGER.parquet",
            "TRIAL_STATISTICS.json",
        ),
        forbidden=(
            "remplir au même quote que le signal sans modèle de latence",
            "appeler NET un résultat sans coût complet confirmé",
            "tuner hors préenregistrement",
        ),
        on_failure="candidat REJECTED, conservé au dossier",
    ),
    PhaseSpec(
        phase_id="P5_STRESS",
        rank=5,
        layer="A",
        title="Stress et stabilité",
        question="Le résultat résiste-t-il aux coûts adverses et aux sous-périodes ?",
        entry_gate="Phase 4 acceptée",
        exit_gate="stress préenregistrés exécutés, scénarios marqués comme scénarios",
        automated=(
            "spread observé + scénarios adverses",
            "commission, swap, slippage, latence",
            "stabilité par sous-période et par régime",
            "contrôles négatifs",
        ),
        human_only=("accepter la Phase 5",),
        artifacts=(
            "STRESS_RESULTS.parquet",
            "COST_SENSITIVITY.json",
            "REGIME_STABILITY.parquet",
            "NEGATIVE_CONTROLS.json",
        ),
        forbidden=("présenter un scénario hypothétique comme un fait historique",),
        on_failure="candidat DEFERRED ou REJECTED",
    ),
    PhaseSpec(
        phase_id="P6_QUALIFICATION",
        rank=6,
        layer="A",
        title="Qualifier les edges",
        question="Quels candidats franchissent les critères gelés, sans nouveau tuning ?",
        entry_gate="Phase 5 acceptée",
        exit_gate="chaque candidat porte LOCKED_FOR_HOLDOUT, REJECTED ou DEFERRED",
        automated=(
            "appliquer les critères gelés",
            "conserver les motifs de rejet et de report",
            "produire le manifeste de verrouillage",
        ),
        human_only=("accepter la Phase 6",),
        artifacts=(
            "QUALIFIED_EDGE_REGISTRY.json",
            "REJECTED_AND_DEFERRED.csv",
            "CANDIDATE_LOCK_MANIFEST.json",
        ),
        forbidden=(
            "déclarer un edge certifié avant Holdout et miroir",
            "nouveau tuning",
            "masquer un NO_EDGE",
        ),
        on_failure="NO_EDGE — conclusion scientifique valide",
    ),
    PhaseSpec(
        phase_id="P7_PORTFOLIO",
        rank=7,
        layer="B",
        title="Portefeuille META-ALPHA et gel des poids",
        question="Les sleeves se complètent-elles réellement, et les poids sont-ils stables sans fuite ?",
        entry_gate="Phase 6 acceptée ; au moins un edge LOCKED_FOR_HOLDOUT",
        exit_gate="poids estimés sur données autorisées puis GELÉS avant test final",
        automated=(
            "corrélation des rendements par période et par régime",
            "chevauchenent des signaux et positions",
            "pertes simultanées et co-drawdowns",
            "concentration temporelle et turnover",
            "contribution marginale au risque et au rendement",
            "test de chaque sleeve seule puis des combinaisons",
        ),
        human_only=("accepter la Phase 7",),
        artifacts=(
            "SLEEVE_RETURNS.parquet",
            "CORRELATION_EXPOSURE_REPORT.json",
            "PORTFOLIO_POLICY.json",
            "PORTFOLIO_LEDGER.parquet",
            "PORTFOLIO_REPORT.json",
            "FINAL_LOCK_MANIFEST.json",
        ),
        forbidden=(
            "optimisation full-sample",
            "régler quoi que ce soit sur le Holdout",
            "assembler des sleeves qui sont des variantes corrélées",
            "fabriquer un portefeuille pour atteindre une cible",
        ),
        on_failure="portefeuille inactif + NO_EDGE si aucun edge ne survit",
    ),
    PhaseSpec(
        phase_id="P8_HOLDOUT",
        rank=8,
        layer="C",
        title="Holdout unique et miroir indépendant",
        question="Le système entièrement gelé survit-il au dernier 20 % jamais consulté ?",
        entry_gate="AUTORISATION EXPLICITE DU PROPRIÉTAIRE + FINAL_LOCK_MANIFEST",
        exit_gate="Holdout ouvert UNE fois, aucun retuning, miroir sans écart inexpliqué",
        automated=(
            "vérifier le sceau et le hash du manifeste gelé",
            "ouvrir le segment Holdout une seule fois",
            "produire performance, incertitude, coûts, risques",
            "construire une implémentation indépendante des éléments critiques",
            "comparer timestamps, signaux, directions, fills, coûts, P&L",
        ),
        human_only=(
            "AUTORISER l'ouverture du Holdout — jamais automatique",
            "accepter la Phase 8",
        ),
        artifacts=(
            "FINAL_HOLDOUT_REPORT.json",
            "GOLDEN_VECTORS.parquet",
            "INDEPENDENT_MIRROR_REPORT.json",
            "FINAL_CERTIFICATE.json",
        ),
        forbidden=(
            "ouvrir le Holdout deux fois",
            "retuner après ouverture",
            "ignorer un écart de miroir",
        ),
        on_failure="rapport de blocage — pas de certificat",
        produces_human_decision=True,
    ),
    PhaseSpec(
        phase_id="P9_MQL5",
        rank=9,
        layer="C",
        title="Robot MQL5, parité, shadow/demo, readiness",
        question="Le robot reproduit-il la logique gelée sur les mêmes quotes, dans les limites du compte ?",
        entry_gate="Phase 8 validée + AUTORISATION DISTINCTE",
        exit_gate="parité Python/MQL5 prouvée + shadow/demo + DEPLOYMENT_READINESS",
        automated=(
            "traduction mécanique de la logique gelée",
            "comparaison Python/MQL5 sur les mêmes quotes",
            "tests de rejets serveur, redémarrage, état, quotes périmées, limites de volume",
            "lecture des paramètres runtime du compte attribué",
            "simulation du challenge sur règles confirmées",
        ),
        human_only=(
            "fournir BLUE_GUARDIAN_ACCOUNT_SPEC (donnée propriétaire)",
            "AUTORISER le déploiement réel — distinct de l'autorisation Holdout",
        ),
        artifacts=(
            "EA_SPEC.json",
            "MQL5_PARITY_REPORT.json",
            "DEPLOYMENT_READINESS.json",
            "BLUE_GUARDIAN_RULES_UNCERTAINTY_REGISTER.json",
            "BLUE_GUARDIAN_ACCOUNT_SPEC.json",
            "BLUE_GUARDIAN_CHALLENGE_SIMULATION.json",
            "EXECUTION_COST_MODEL.json",
            "SYMBOL_RUNTIME_SPEC.json",
        ),
        forbidden=(
            "déployer en réel sur la seule base de la compilation",
            "inventer un paramètre serveur",
            "contourner la règle des 2 minutes",
            "fractionner des ordres pour masquer du HFT",
        ),
        on_failure="shadow/demo maintenu, pas de réel",
        produces_human_decision=True,
    ),
)

PHASE_INDEX = {p.phase_id: p for p in PHASES}


# ---------------------------------------------------------------------------
# Blue Guardian — registre d'incertitude (fiche §6)
# ---------------------------------------------------------------------------
# Règles RAPPORTÉES par le PDF daté du 20/09/2026. Jamais une garantie.
BG_REPORTED_RULES: tuple[dict[str, str], ...] = (
    {"rule": "Phase 1 objectif", "value": "10 %", "status": "REPORTED"},
    {"rule": "Phase 2 objectif", "value": "4 %", "status": "REPORTED"},
    {"rule": "Durée", "value": "illimitée", "status": "REPORTED"},
    {"rule": "Jours rentables minimum", "value": "4 jours à 0,5 %/jour", "status": "REPORTED"},
    {"rule": "Daily loss", "value": "4 % du solde initial, reset 17:00 EST", "status": "REPORTED"},
    {"rule": "Drawdown maximum", "value": "10 % trailing puis verrouillage au solde de départ",
     "status": "CONTRADICTION_DOCUMENTAIRE"},
    {"rule": "Profit split", "value": "85 % / add-on 90 %", "status": "REPORTED"},
    {"rule": "Premier payout", "value": "14 jours (add-on 7 jours)", "status": "REPORTED"},
    {"rule": "Consistency funded", "value": "25 %", "status": "REPORTED"},
    {"rule": "Retrait minimum", "value": "100 USD crypto / 500 USD Rise", "status": "REPORTED"},
    {"rule": "EA", "value": "autorisés", "status": "REPORTED"},
    {"rule": "Overnight / week-end", "value": "autorisé", "status": "REPORTED"},
    {"rule": "News challenge", "value": "autorisé", "status": "REPORTED"},
    {"rule": "News funded", "value": "restreint, fenêtre 5 min avant/après high-impact",
     "status": "REPORTED"},
    {"rule": "Durée minimale de détention", "value": "2 minutes", "status": "BLOQUANT_POUR_L_ARCHITECTURE"},
    {"rule": "HFT / tick scalping / arbitrage", "value": "interdits", "status": "BLOQUANT"},
    {"rule": "Commission Commodities", "value": "5 USD/lot", "status": "REPORTED"},
    {"rule": "Mode de facturation commission", "value": "non publié", "status": "NOT_PUBLIC"},
    {"rule": "Swap et taux", "value": "non publiés", "status": "NOT_PUBLIC"},
    {"rule": "Stop Out", "value": "100 %", "status": "REPORTED"},
    {"rule": "Guardian Shield funded", "value": "2 % de PnL flottant global", "status": "REPORTED"},
    {"rule": "Compte personnel / appareil non partagé", "value": "exigé", "status": "REPORTED"},
    {"rule": "Changement de plateforme", "value": "impossible après le premier trade", "status": "REPORTED"},
)

BG_NOT_PUBLIC: tuple[str, ...] = (
    "taille de contrat", "digits", "tick size", "tick value",
    "volume minimum", "volume maximum", "volume step", "stops level", "freeze level",
    "mode d'exécution", "types d'ordres", "modes de remplissage",
    "heures de cotation/trading", "conversion risque → volume",
    "règles détaillées de slippage/deviation", "politique retry",
    "limites de fréquence", "causes et règles de rejet/requote",
)

# Contrainte de la règle des 2 minutes, traduite en exigence d'architecture.
BG_HOLD_MIN_SECONDS = 120
BG_HOLD_MIN_MINUTES = 2


# ---------------------------------------------------------------------------
# Ce que les ticks ne peuvent PAS prouver (fiche §4.2)
# ---------------------------------------------------------------------------
TICK_LIMITS: tuple[dict[str, str], ...] = (
    {"claim": "volume réellement échangé", "status": "UNAVAILABLE"},
    {"claim": "delta acheteur/vendeur", "status": "UNAVAILABLE"},
    {"claim": "profondeur du carnet", "status": "UNAVAILABLE"},
    {"claim": "files d'attente", "status": "UNAVAILABLE"},
    {"claim": "taux de remplissage des ordres limites", "status": "UNAVAILABLE"},
    {"claim": "slippage réel Blue Guardian", "status": "DEFERRED_EXTERNAL_DEPENDENCY"},
    {"claim": "latence réelle du serveur", "status": "DEFERRED_EXTERNAL_DEPENDENCY"},
    {"claim": "coûts complets réels", "status": "DEFERRED_EXTERNAL_DEPENDENCY"},
)


# ---------------------------------------------------------------------------
# Chaîne de transformation (fiche §1)
# ---------------------------------------------------------------------------
CHAIN: tuple[str, ...] = (
    "TICKS NATIFS BID/ASK",
    "DGP ANALYTIQUE",
    "VARIABLES",
    "HYPOTHÈSES",
    "ANOMALIES",
    "STRATÉGIES CANDIDATES",
    "EDGES QUALIFIÉS",
    "PORTEFEUILLE META-ALPHA",
    "VALIDATION FINALE",
    "ADAPTATEUR BLUE GUARDIAN",
    "ROBOT",
)


# ---------------------------------------------------------------------------
# Matrice d'automatisation (fiche §11)
# ---------------------------------------------------------------------------
AUTOMATED_CAPABILITIES: tuple[str, ...] = (
    "exécutions de calcul", "contrôles déterministes", "checkpoints", "reprises",
    "logs", "génération des rapports", "blocage automatique des gates échoués",
    "vérification des hashes", "surveillance des ressources",
)

NEVER_AUTOMATED: tuple[str, ...] = (
    "inventer une formule pour remplir une famille",
    "modifier silencieusement un paramètre scientifique",
    "supprimer un résultat négatif",
    "ouvrir le Holdout sans autorisation explicite",
    "modifier un certificat hérité",
    "inventer une valeur serveur",
    "déployer en réel sans autorisation distincte",
    "accepter une phase à la place du propriétaire",
)


# ---------------------------------------------------------------------------
# Vues dérivées — utilisées par le rendu du schéma
# ---------------------------------------------------------------------------
def phases_by_layer(layer_id: str) -> list[PhaseSpec]:
    return [p for p in PHASES if p.layer == layer_id]


def all_artifacts() -> dict[str, list[str]]:
    """Artefact -> phases qui le produisent. Contrôle de non-duplication."""
    out: dict[str, list[str]] = {}
    for p in PHASES:
        for a in p.artifacts:
            out.setdefault(a, []).append(p.phase_id)
    return out


def duplicate_artifacts() -> dict[str, list[str]]:
    return {a: ps for a, ps in all_artifacts().items() if len(ps) > 1}


def human_decisions() -> list[dict[str, Any]]:
    """Tout ce qui exige le propriétaire, avec la phase et la conséquence."""
    rows: list[dict[str, Any]] = []
    for p in PHASES:
        for h in p.human_only:
            rows.append({"phase": p.phase_id, "decision": h, "blocking": True})
    return rows


def gate_summary() -> list[dict[str, str]]:
    return [
        {
            "phase": p.phase_id,
            "entry": p.entry_gate,
            "exit": p.exit_gate,
            "on_failure": p.on_failure,
        }
        for p in PHASES
    ]


def stats() -> dict[str, Any]:
    arts = all_artifacts()
    return {
        "phases_total": len(PHASES),
        "phases_certified_not_to_rebuild": sum(1 for p in PHASES if "CERTIFIED" in p.phase_id),
        "phases_to_execute": sum(1 for p in PHASES if "CERTIFIED" not in p.phase_id),
        "layers_total": len(LAYERS),
        "artifacts_total": len(arts),
        "human_decisions_total": len(human_decisions()),
        "human_phases": [p.phase_id for p in PHASES if p.produces_human_decision],
        "automated_steps_total": sum(len(p.automated) for p in PHASES),
        "duplicate_artifacts": duplicate_artifacts(),
        "bg_rules_reported": len(BG_REPORTED_RULES),
        "bg_rules_blocking": sum(1 for r in BG_REPORTED_RULES
                                 if r["status"].startswith(("BLOQUANT", "CONTRADICTION"))),
        "bg_not_public": len(BG_NOT_PUBLIC),
        "tick_limits": len(TICK_LIMITS),
    }


# ---------------------------------------------------------------------------
# Catalogue des secrets — ce qui est nécessaire, quand, et pourquoi
# ---------------------------------------------------------------------------
SECRETS: tuple[dict[str, str], ...] = (
    {
        "name": "GDRIVE_SA_JSON",
        "needed_for": "accès au corpus certifié (lecture seule) + zone de recherche",
        "blocks": "P2_ANALYTICAL",
        "obtained_from": "Google Cloud Console → compte de service → clé JSON",
        "revocable": "oui — supprimer l'accès du robot au dossier",
        "never_in": "dépôt, notebook, conversation, fichier commité",
    },
    {
        "name": "GDRIVE_ROOT_FOLDER_ID",
        "needed_for": "pointer sur la racine META_ALPHA_XAUUSD_DGP",
        "blocks": "P2_ANALYTICAL",
        "obtained_from": "URL du dossier dans Drive",
        "revocable": "oui — changer le partage",
        "never_in": "dépôt (il révèle la structure du Drive)",
    },
    {
        "name": "KAGGLE_USERNAME",
        "needed_for": "lancer les kernels de calcul CPU",
        "blocks": "P3_MINING (uniquement si le calcul local ne suffit pas)",
        "obtained_from": "kaggle.com → Settings → API → Create New Token",
        "revocable": "oui — un clic sur la même page",
        "never_in": "dépôt, notebook",
    },
    {
        "name": "KAGGLE_KEY",
        "needed_for": "authentifier les kernels de calcul CPU",
        "blocks": "P3_MINING (uniquement si le calcul local ne suffit pas)",
        "obtained_from": "kaggle.json (champ key)",
        "revocable": "oui — un clic",
        "never_in": "dépôt, notebook",
    },
)


def secrets_catalog() -> list[dict[str, str]]:
    return list(SECRETS)


def blockers_for_phase(phase_id: str) -> list[str]:
    return [s["name"] for s in SECRETS if phase_id in s["blocks"]]
