# CAMPAGNE 3 — GEL DES 12 COMPARAISONS ET CLARIFICATIONS TEMPORELLES

**DESCRIPTIF — IS UNIQUEMENT — AUCUNE MESURE DE PERFORMANCE.** Document écrit
et chaîné **avant tout calcul** de la Campagne 3 (autorisation seq 188,
dictionnaire gelé seq 185–186, sha256
`76490c40e4c6aca1cad56a98f30d4711d6723ac56e39cf08f978a0349d354a92`).
Aucune comparaison ne peut être ajoutée, retirée ou reformulée après
consultation des résultats. Toute clarification ci-dessous est antérieure au
premier calcul et ne modifie ni le déclenchement ni la formation gelés.

## 1. Clarifications temporelles (explicitations du dictionnaire, avant calcul)

| Point contrôlé | Règle d'exécution explicite |
|---|---|
| Seuil IMP 60 jours | Quantile 90 de \|r\| calculé sur les barres de la même famille dont l'horodatage est dans **[T0 − 60 jours calendaires, T0)**, **barre courante exclue** ; minimum 2 000 barres d'historique, sinon aucun déclenchement (zone d'amorçage comptée et publiée). « Jour calendaire » = jour de calendrier UTC (et non journée de cotation) pour cette fenêtre roulante. |
| Seuil CONS 5 journées | Médiane **groupée (poolée)** des ranges M1 des **5 journées de cotation précédentes** (journées présentes dans le corpus, jour courant exclu) ; minimum 1 000 barres d'historique. « Journée de cotation » = date UTC présentant des barres dans le corpus. |
| Journées (grappes, ères, censure) | Date calendaire UTC de l'horodatage de la barre. La censure « fin de journée » = dernière barre de la même date UTC. |
| Instantanés | **En nombre de barres de la famille** : IMP-M5 → T0, +1, +3, +6, +12 barres = 0, +5, +15, +30, +60 min ; IMP-M15 → 0, +15, +45, +90, +180 min. Les deux familles ne sont jamais mélangées. CONS (M1) → T0, +3, +6, +12 minutes. |
| Variables d'instantané | Calculées sur les barres d'indice ≤ indice de l'instantané uniquement (closes et disponibles à cet instant). |
| Conséquences futures | Calculées sur les barres d'indice **strictement supérieur** à l'indice de l'instantané. Pour IMP : retracement maximal ultérieur et extension mesurés sur (instantané, instantané + 60 min], bornés fin de journée ; positions à +15/+30/+60 min après l'instantané (NaN censuré si hors journée). La classification en trajectoires (§3) utilise la fenêtre (T0, T0 + 60 min]. |

## 2. Les 12 comparaisons gelées (famille fermée)

Bootstrap par grappes-journées (2 000 répétitions, graine 20261113),
p bilatérales issues du bootstrap, correction **BY** sur l'ensemble des 12,
seuil matériel : 5 points (proportions) ou ratio de médianes 1,15 ; suffisance
≥ 200 épisodes **et** ≥ 100 journées par bras ; lecture par ère : cohérence de
signe dans ≥ 2 ères sur 3 quand la dimension comparée n'est pas l'ère.
Groupes d'amplitude « BAS/HAUT » (C3-03, C3-07) : amplitude initiale comparée à
la **médiane des amplitudes des déclenchements précédents des 60 jours
calendaires passés** (causal, passé seul, minimum 30 déclenchements passés,
sinon épisode non classé et compté).

| ID | Famille | Comparaison (issue mesurée après l'instantané indiqué) | Type |
|---|---|---|---|
| C3-01 | IMP-M5 | P(retracement complet 100 % dans (T0, T0+60 min]) : HAUSSE vs BAISSE | proportion |
| C3-02 | IMP-M5 | P(retracement complet) : session LONDRES vs ASIE (session de T0) | proportion |
| C3-03 | IMP-M5 | Médiane du retracement maximal ultérieur après l'instantané +12 barres : amplitude BAS vs HAUT (causal) | médiane |
| C3-04 | IMP-M5 | P(stagnation dans (T0, T0+60 min]) : régime F3 BAS vs HAUT | proportion |
| C3-05 | IMP-M5 | Médiane du retracement maximal ultérieur après T0 : ère 2010–13 vs 2017–20 | médiane |
| C3-06 | IMP-M15 | P(retracement complet dans (T0, T0+60 min]) : HAUSSE vs BAISSE | proportion |
| C3-07 | IMP-M15 | Médiane de l'extension supplémentaire après l'instantané +12 barres : amplitude BAS vs HAUT (causal) | médiane |
| C3-08 | IMP-M15 | P(continuation dans (T0, T0+60 min]) : session LONDRES vs ASIE | proportion |
| C3-09 | CONS | P(sortie par barre de range > 2× range de formation) : range de formation BAS vs HAUT (médiane causale des ranges de formation des 60 jours passés, min 30) | proportion |
| C3-10 | CONS | Médiane du range des 60 min suivant la sortie : sortie par clôture hors range vs sortie par barre de range | médiane |
| C3-11 | CONS | P(censure à +120 min sans sortie) : session de formation LONDRES vs ASIE | proportion |
| C3-12 | CONS | Médiane de la durée de consolidation (formation → sortie ou censure) : ère 2010–13 vs 2017–20 | médiane |

## 3. Classes de trajectoires IMP (issues descriptives, fenêtre (T0, T0+60 min])

Définies uniquement à partir de mesures **postérieures** à T0 (elles décrivent
l'issue ; elles ne classent jamais le déclenchement). A = amplitude initiale
(bp, dans le sens de l'impulsion) ; t50/t100 = premier temps de retracement de
50 %/100 % de A ; t_ext = premier temps où l'extension cumulée atteint 2A ;
exc_opp = excursion maximale au-delà du prix d'origine dans le sens opposé.

Règle d'affectation exclusive, dans cet ordre :
1. **RETOURNEMENT** : t100 existe, t100 < t_ext (ou t_ext absent), et exc_opp ≥ 0,5A.
2. **RETRACEMENT_COMPLET** : t100 existe, t100 < t_ext (ou t_ext absent), et exc_opp < 0,5A.
3. **CONTINUATION** : t_ext existe, t_ext < t100 (ou t100 absent), t_ext ≤ 30 min.
4. **EXTENSION_TARDIVE** : t_ext existe, t_ext < t100 (ou t100 absent), t_ext > 30 min.
5. **RETRACEMENT_PARTIEL** : t50 existe, ni t100 ni t_ext.
6. **STAGNATION** : ni t50, ni t100, ni t_ext.
7. **CENSUREE** : fenêtre incomplète (fin de journée avant +60 min) sans qu'aucun
   des événements ci-dessus soit survenu avant la fin de journée — comptée à
   part, jamais imputée.

## 4. Issues CONS (aucune expansion présupposée)

Types de sortie distingués : `BARRE_RANGE` (première barre de range > 2× le
range de formation), `CLOTURE_HORS_RANGE` (première clôture hors du range
cumulé, sans que la condition précédente soit remplie sur la même barre — en
cas d'égalité sur la même barre, `BARRE_RANGE` prime, règle écrite avant
calcul), `CENSUREE` (+120 min ou fin de journée). Issues post-sortie
symétriques : range des 60 min suivantes, excursions dans le sens de la
clôture de sortie et dans le sens opposé, positions à +15/+30/+60 min par
rapport au milieu du range de formation. Aucune issue n'est nommée
« expansion » ; seule la distribution mesurée du range post-sortie est publiée.

## 5. Traitement des chevauchements et de la dépendance

Épisodes chevauchants (déclenchement pendant la fenêtre d'issue d'un épisode
précédent de la même famille, ou consolidation formée pendant une
consolidation active) : **comptés, signalés dans une colonne dédiée, jamais
supprimés** de l'analyse principale. Aucune analyse de sensibilité par
exclusion n'est préenregistrée : elle n'aura donc pas lieu. Toutes les
inférences descriptives utilisent le bootstrap par journées (l'unité
d'indépendance), et les effectifs bruts (épisodes) comme indépendants
(journées) sont publiés côte à côte.
