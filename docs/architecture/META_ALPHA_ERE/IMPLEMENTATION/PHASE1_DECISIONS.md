# ERE — PHASE 1 : DÉCISIONS DE CONSOLIDATION (autonomie fondateur, seq500)

Décisions tranchées de façon conservatrice, conformément à l'autorisation
d'exécution autonome. Aucun critère de preuve n'est abaissé.

| # | Point ouvert | Décision | Justification |
|---|---|---|---|
| D1 | Taxonomie officielle | **N0–N7 adoptée** ; E0–E5 = correspondance secondaire documentée dans `ere/taxonomy.py` | alignée Constitution §9 ; E5 externe plus faible que N7 |
| D2 | Corrections ERE-REVIEW-002 1–7 | **Toutes approuvées pour implémentation** | chacune réduit un risque identifié sans toucher aux critères |
| D3 | Entrées de G | Liste fermée (REVIEW-002 §4.2) codée dans `G_ALLOWED_INPUTS` ; toute pièce hors liste invalide le verdict | auditabilité des verdicts |
| D4 | Verdict E vs G | `AvisDeTestabilite` (E) distinct du verdict de G ; contre-seing de G obligatoire pour clore en NON DÉMONTRABLE | pas de conclusion hors du moteur de jugement |
| D5 | Fenêtre B | Objet `MarketWindow` typé (bornes déclarées avant extraction, plafond N2) | seule consommation de marché non typée comblée |
| D6 | État de dossier | Objet `DossierState` (étape, objets, segments consommés, expériences) | reprise sans mémoire de conversation |
| D7 | Coût dès F | Bloc `couts_ordre_de_grandeur` obligatoire dans `SignatureReport` (filtre, jamais mesure d'edge) | précédent marge brute 0,026 < coût 0,033 |
| D8 | I-A / I-B | Séparation codée : modules distincts, I-B ne reçoit que des verdicts I-A favorables | le juge n'alloue pas |
| D9 | Visuel 1 proposé | **Promu** : la proposition de REVIEW-002 devient le Visuel 1 de référence ; l'original archivé sous `diagrams/archive/` | le diagramme doit montrer D, les boucles, les sorties |
| D10 | Contrats typés | Implémentés en **dataclasses Python stdlib avec validation explicite**, pas Pydantic | zéro dépendance nouvelle ; la validation métier (inter-objets) compte plus que le framework ; Pydantic réévaluable si les schémas JSON externes deviennent nécessaires |
| D11 | Versionnement contrats | SemVer par schéma (`schema_version` dans chaque objet) ; major = rupture, migrations explicites, jamais de coercition silencieuse | règle reprise du dossier externe, compatible avec nos invariants |

Application : code dans `ere/` (package), tests dans `tests/`.
Les documents d'architecture d'origine ne sont pas réécrits ; cette
phase les *implémente* et consigne ses choix ici.
