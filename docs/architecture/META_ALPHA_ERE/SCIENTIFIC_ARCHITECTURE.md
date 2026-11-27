# META ALPHA ERE — ARCHITECTURE SCIENTIFIQUE

## Disciplines et leurs rôles (bibliothèque du module D)

| Discipline | Apport | Méthodes pertinentes | Limites |
|---|---|---|---|
| Microstructure des marchés | formation des prix, spread, impact, files d'ordres | modèles de spread, sélection adverse (Glosten–Milgrom), inventaire (Garman, Stoll) | exige Bid/Ask/profondeur souvent absents |
| Économétrie & séries temporelles | dynamiques, persistance, cointégration | AR/VAR, GARCH, autocorrélations | stationnarité rare en pratique |
| Statistiques avancées | estimation, incertitude, multiplicité | bootstrap par blocs, intervalles, contrôle du taux de fausses découvertes | dépendance temporelle des épisodes |
| Probabilités & processus stochastiques | trajectoires, premiers passages | marches aléatoires, temps d'atteinte, files d'attente | hypothèses markoviennes fragiles |
| Finance quantitative | valorisation du risque, coûts | décomposition rendement/coûts, mesures de queue (ES) | ne crée pas d'edge |
| Détection de régimes | contextes changeants | HMM, ruptures (CUSUM), volatilité réalisée | régimes détectés ≠ régimes prédictibles |
| Inférence causale | effets de mécanismes (renforcement) | contrefactuels, censure, identification partielle (bornes de Manski) | contrefactuels souvent censurés (cf. seq459) |
| Théorie des jeux & comportements | raisons d'agir des participants | modèles d'agents, flux forcés (margin calls, stops) | difficilement observable directement |
| Théorie de l'information | valeur d'une expérience | gain d'information attendu, entropie des hypothèses | exige des vraisemblances explicites |
| Gestion quantitative du risque | budgets, ruine, capital | ES, drawdown, sizing par budget (pas Kelly non contraint) | ne transforme pas une espérance négative |
| Optimisation & recherche opérationnelle | plans d'expériences, allocation | design optimal, allocation de calcul | risque d'optimiser le mauvais objectif |
| Modélisation des participants | hypothèses de flux (liquidation, couverture) | taxonomies de flux institutionnels | spéculatif sans données de flux |

## Chaîne de preuve (invariante)

FAIT OBSERVÉ → INFÉRENCE → HYPOTHÈSE ÉCONOMIQUE → MÉCANISME IDENTIFIÉ
→ AVANTAGE ÉCONOMIQUE VALIDÉ. Chaque transition exige son test propre ;
aucun saut n'est autorisé (une corrélation rétrospective n'est ni une
causalité ni un edge). Qualifications normalisées de la constitution :
DÉMONTRÉ, FORTEMENT ÉTAYÉ, COMPATIBLE MAIS NON IDENTIFIÉ, NON
DÉMONTRABLE, RÉFUTÉ.

## Approches probabilistes — conditions d'usage

Bayes et identification partielle sont admis lorsque les
vraisemblances sont explicites et auditables (ex. bornes sur l'effet
causal d'un renforcement avec censure). Toute probabilité numérique
non traçable à un modèle génératif déclaré est interdite : le système
préfère les ensembles compatibles et les verdicts qualifiés.
