# CAMPAGNE 2.2 — AUDIT D'ANTICIPATION (LOOKAHEAD) DES VARIABLES D'ÉVÉNEMENTS

**DESCRIPTIF — IS UNIQUEMENT — AUCUNE MESURE DE PERFORMANCE.**

## Règle d'audit

Une variable est « disponible à l'instant t » si et seulement si son calcul
n'utilise que des barres d'horodatage ≤ t. Audit mené sur le code commité des
moteurs (`campaign01_engine.py` pour les variables historiques,
`campaign022_engine.py` pour la reconstruction).

## Variables historiques (Campagnes 1, 2, 2.1) — verdicts

| Variable | Définition (code) | Disponible à | Verdict |
|---|---|---|---|
| `profondeur_bp` (EV2/EV3) | Excursion maximale au-delà du niveau sur les barres **i à i+60** | T0+60 seulement | **CONTAMINÉE** : contient l'issue (réintégration ou non) — toute classification par terciles de profondeur est rétrospective |
| `delai_reintegration_min` | Première clôture revenue du bon côté sous 60 min | Au moment de la réintégration | Issue, pas caractéristique ; usage légitime comme variable mesurée, jamais comme prédicteur |
| Cassure (+5 bp) | Clôture de la barre de déclenchement au-delà de L ± 5 bp | **T0** (clôture de la barre i) | Causale — c'est le classeur du test R01 (négatif) |
| `encore_au_dela_60` (EV3) | Clôture à retest+60 vs niveau | Retest+60 | Issue descriptive ; ne doit jamais être présentée comme connue au retest |
| `delai_retour_test_min` | Barres entre cassure et première touche du niveau | Au retest | Disponible au retest seulement |
| `retracement_max_pct` (EV5) | Maximum du cumul contraire sur 12 barres M5 suivantes | T0+60 min | **CONTAMINÉE** comme classeur éventuel ; légitime comme mesure d'issue |
| `range_suivant_60_bp` (EV6) | Range des 60 barres suivant la fin de consolidation | Fin+60 | Issue, pas caractéristique à la fin de l'épisode |
| Terciles par ère (C2/2.1) | Quantiles calculés sur l'ère entière | Fin d'ère | Rétrospectifs : un épisode de 2010 est classé avec des bornes incluant 2011–13 — limite écrite, acceptable en descriptif, interdite en temps réel |
| Seuils EV4/EV7 | EV4 : médiane des 5 jours précédents (causal) ; EV7 : P95 poolé décennal | EV4 : T0 ; EV7 : jamais | EV7 **non causal** (déjà consigné seq 160) |
| Régime F3 | Prévision HAR du jour, features causales gelées | Début de journée | Causal au sens du gel seq 75 |
| Spread à l'événement | Médiane du spread de la barre de déclenchement | T0 | Causale |

## Variables de la reconstruction 2.2 — garanties de construction

Pour chaque instantané s ∈ {0, 1, 3, 5} : `profondeur_initiale_bp` (barre i,
constante), `prof_max_jusqua_bp` (maximum sur i..i+s uniquement),
`position_bp`, `duree_au_dela_min`, `vol_realisee_bp`, `spread_bp`,
`amplitude_parcourue_bp` — toutes calculées sur la fenêtre close à i+s. Les issues
(`reintegration_ulterior`, `temps_restant_reint_min`, `extension_supplementaire_bp`,
excursions favorable/adverse, positions à +15/+30/+60 **après l'instantané**) ne
lisent que les barres > i+s, bornées à T0+60. La colonne
`prof60_retrospective_bp` est conservée dans le brut **uniquement** pour permettre
la comparaison ancien/nouveau régime de variables ; elle est étiquetée
rétrospective et ne doit figurer dans aucune classification « disponible ».

Pour les cassures, la ligne `RETEST` ne contient que des grandeurs connues à la
barre de confirmation du retest (profondeur atteinte jusqu'au retest inclus) ;
ses issues sont mesurées après cette barre. Les cassures sans retest, invalidées
(clôture revenue du bon côté après retest) et censurées (fenêtre tronquée) sont
des catégories distinctes dans le brut.

## Catégories historiques vs catégories causales — la différence en une table

| Question | Catégorie historique (future) | Catégorie causale (2.2) |
|---|---|---|
| A : qui réintègre ? | Tercile de profondeur maximale sur 60 min : 98,2 % vs 65,8 % | Profondeur initiale à T0 (médiane 1,43 bp) et profondeur atteinte à T+1/+3/+5 ; ampleur initiale +5 bp : écart nul (R01) |
| B : qui reste au-delà ? | Tercile de profondeur maximale : 26,9 % vs 80,7 % | Profondeur atteinte **au moment du retest** (médiane 11,9 bp sur l'extraction partielle) ; issues après retest seulement |

Les deux lignes historiques restent au registre, étiquetées « résultats
rétrospectifs conditionnés par des variables futures » (ordre du propriétaire) ;
elles ne sont ni supprimées ni réutilisables comme signaux d'entrée.
