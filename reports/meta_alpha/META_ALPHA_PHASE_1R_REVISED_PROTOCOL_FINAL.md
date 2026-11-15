# META ALPHA — PHASE 1R : PROTOCOLE RÉVISÉ FINAL (proposition, NON autorisée, NON commencée)

Version finale méthodologique. Les versions antérieures (Blueprint, protocole
révisé) et tous les contrôles négatifs (Phase S, contrôle HMM) sont conservés
sans modification. Philosophie: DONNÉES -> COMPORTEMENTS -> ANOMALIES ->
CARACTÉRISATION -> HYPOTHÈSES -> TESTS -> QUALIFICATION. Les modèles continus
sont l'hypothèse par défaut; le discret est l'hypothèse extraordinaire.

## CORRECTION 1 — Unités et comparabilité des statistiques (remplace l'ancien §6 naïf)
Règle: **on ne compare jamais deux grandeurs d'unités différentes.** Pour chaque
statistique descriptive utilisée en 1R, le préenregistrement devra remplir:

| Statistique | Formule exacte | Unité | Granularité | Conditionnement causal | Comparaison au spread pertinent? |
|---|---|---|---|---|---|
| Rendement mid | (mid_t - mid_{t-1})/mid_{t-1} | sans dimension (fraction; en bp x1e4) | tick ou barre | aucun / variable causale | Oui: même unité qu'un rendement; comparer |effet en bp| au spread_rel (bp) est licite |
| Volatilité réalisée | sqrt(somme des r^2 sur fenêtre) | fraction (bp par racine de fenêtre) | fenêtre fixe préenregistrée | passé seul | Indirecte seulement: comparer des RATIOS de volatilité entre conditions (sans dimension), jamais volatilité brute au spread |
| Spread relatif | (ask-bid)/mid | fraction (bp) | tick | aucun | C'est la référence elle-même |
| Autocorrélation | corr Pearson/Spearman définie au préenregistrement | sans dimension [-1,1] | lag en événements | passé seul | **Non pertinent**: seuil adapté = stabilité (même signe sur 2/3 tiers) + intervalle bootstrap par blocs excluant 0; justifié car une corrélation n'a pas d'unité économique |
| Inter-arrivée moyenne | moyenne des (t_i - t_{i-1}) | secondes | fenêtre d'événements | passé seul | **Non pertinent**: seuil adapté = écart relatif (§ Correction 2) entre conditions + stabilité |
| Intensité | nombre d'événements / fenêtre | événements par seconde | fenêtre temporelle | passé seul | **Non pertinent**: idem inter-arrivée |
| Probabilité/fréquence d'événement | comptage / total | proportion | fenêtre | passé seul | **Non pertinent**: seuil adapté = intervalle de Wilson et écart absolu minimal préenregistré (ex. 1 point de pourcentage), justifié par l'effectif |

Quand la comparaison au spread n'est pas pertinente, le seuil adapté ci-dessus,
choisi AVANT exécution, s'applique. Toute statistique nouvelle exige une ligne
complète dans ce tableau au préenregistrement, sinon elle est irrecevable.

## CORRECTION 2 — Variation relative de 25%: définition exacte
Pour une statistique S mesurée sous deux conditions causales A (Q1) et B (Q5):
- Écart absolu: D = S_B - S_A. Écart relatif: **R = D / max(|S_A|, epsilon_S)**,
  où epsilon_S est un plancher propre à la statistique, fixé au préenregistrement
  (par défaut: 1% de l'écart interquartile IS de S mesuré en Phase 0/descriptif,
  ou l'unité de résolution de S si elle est supérieure).
- Référence nulle ou proche de zéro (|S_A| < epsilon_S): la variation relative est
  **déclarée NON APPLICABLE**; seul l'écart absolu D, comparé à son seuil propre
  (Correction 1), peut être utilisé. Interdiction de gonfler R avec un dénominateur minuscule.
- Valeurs négatives: R se calcule avec |S_A| au dénominateur; le SIGNE de D doit
  être rapporté séparément et être identique sur au moins 2 des 3 tiers d'IS.
- Critère "variation non triviale" (les deux requis lorsque R est applicable):
  (i) |D| dépasse le seuil d'unité de la Correction 1; (ii) |R| >= 25%.
  Lorsque R est non applicable: (i) seul, avec mention explicite "relatif N/A".
- "Statistique plate" intra-condition: pente temporelle non significative après
  BY, et amplitude intra-condition < 25% de |D| (même formule, dénominateur |D|;
  si |D| est sous son plancher epsilon_D, la structure entière est déclarée
  non triviale-insuffisante et la piste s'arrête).
Aucun de ces seuils ne peut être choisi ou modifié après observation des résultats.

## CORRECTION 3 — Comparaison aux modèles continus: deux temps strictement séparés
**Temps 1 — Exploratoire IS (seul temps de la Phase 1R):** ajuster sur IS les
modèles continus concurrents (GARCH, FIGARCH/ARFIMA sur |r|, volatilité
stochastique si implémentée) et toute structure candidate discrète; comparer par
critères intra-IS (vraisemblance pénalisée, résidus, stabilité inter-tiers).
Statut maximal atteignable sur IS: **"structure candidate"**. Aucune comparaison
IS ne peut établir l'existence d'un régime discret.
**Temps 2 — Confirmation OOS (hors Phase 1R, autorisation séparée):** avant TOUTE
consultation de l'OOS, verrouiller dans la chaîne (hash): modèles concurrents et
leurs formes exactes, variables, granularités, horizons, fonction de perte unique,
métrique unique, critère de décision chiffré, correction de dépendance
(HAC/Diebold-Mariano ou bootstrap par blocs), et le sort réservé à chaque issue.
L'OOS est ensuite consulté **une fois**: il confirme ou réfute; il ne modifie ni
ne sélectionne jamais un modèle. Toute retouche après lecture OOS transforme
l'exercice en exploration et exige un nouvel échantillon indépendant (Holdout,
autorisation finale distincte) pour toute confirmation ultérieure.

## CORRECTION 4 — Multiplicité cumulative et statuts épistémiques
- Le compteur historique est conservé: **148 tests** (P3-001: 15, P4-001: 1 candidat/
  4 évaluations segment-horizon, P3-002: 21 contrastes + cellules descriptives)
  **plus 3 vagues descriptives** (phénoménologie, audit, validation profonde),
  plus les contrôles de simulation (Phase S, contrôle HMM) comptés séparément
  comme validation d'outils, pas comme tests sur données réelles.
- Toute nouvelle analyse, même purement descriptive, est inscrite au registre
  cumulatif chaîné (TRIAL_LEDGER_CHAIN.json) AVANT exécution, avec son type.
- Quatre statuts épistémiques, jamais confondus dans les rapports:
  (1) **Exploration descriptive**: mesures sur IS, valeur générative seulement.
  (2) **Découverte candidate**: phénomène stable selon Corrections 1-2, non confirmé.
  (3) **Hypothèse préenregistrée**: test défini, verrouillé, non encore exécuté.
  (4) **Confirmation indépendante**: survie sur données jamais utilisées pour la
  découverte (OOS au Temps 2, puis Holdout en finale autorisée).
- Plusieurs vagues adaptatives sur IS ne constituent JAMAIS des confirmations
  indépendantes entre elles: elles partagent le même échantillon et la même
  sélection cumulative, qui doit être citée dans chaque rapport (compteur à jour).
- Le gate déterministe (BY + compteur cumulatif) classe les statuts (1)->(2);
  seuls des protocoles gelés de type Temps 2 peuvent produire le statut (4).

## Rappel des sections inchangées du protocole révisé
Dimensions observables (§1), méthodes descriptives (§2), modèles continus
concurrents par défaut (§3), détection d'anomalies (§4), caractérisation (§5),
génération d'hypothèses gouvernée (§7), séparation IS/OOS/Holdout (§8),
critères d'arrêt incluant l'arrêt global (§9), point de départ exact (§11):
séries descriptives granulées causales sur IS, uniquement après décision
explicite du propriétaire sur CE document final.
