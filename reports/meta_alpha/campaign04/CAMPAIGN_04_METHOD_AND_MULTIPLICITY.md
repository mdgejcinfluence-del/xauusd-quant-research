# CAMPAGNE 4 — MÉTHODE ET MULTIPLICITÉ (GEL DE PRINCIPE, À ARRÊTER AVANT CALCUL)

**DESCRIPTIF — IS UNIQUEMENT — AUCUNE MESURE DE PERFORMANCE.** À figer
avec le dictionnaire validé avant extraction ; aucun paramètre modifié
après consultation des résultats.

**Note de révision (seq 195)** : la liste exacte et définitive des dix
comparaisons, leurs variables, populations, fenêtres, unités et critères
de matérialité figure désormais dans le document compagnon
`CAMPAIGN_04_COMPARISONS_FREEZE.md`, qui fait foi sur la présente esquisse
(notamment : seuil matériel spécifique de C4-06 en différence de médianes
de g1, éligibilité de 30 transitions qualifiée de descriptive, et non de
garantie de puissance — le §3 ci-dessous est à lire sous cette correction).
Le dictionnaire de référence est la version 2
(`CAMPAIGN_04_EVENT_DICTIONARY_V2.md`).

## 1. Statistiques descriptives (le cœur de la campagne)

Pour chaque famille (REG-J, REG-S, DIM publiée dimension par dimension) :
effectifs de journées/sessions par état, matrices complètes
(état-passé F3 × état courant ; ancien → nouvel état confirmé), distributions
des durées (médiane, P25/P75, P90, part censurée), distributions des temps
de retour à l'habituel, vitesses de transition, taux de transitions non
confirmées, discordances F3 — le tout publié globalement et par ère, sans
recherche de la « meilleure » cellule. Les ruptures de distribution sont
décrites par quantiles (P5/P25/médiane/P75/P95), skew, part de queue et
fréquence d'extrêmes, dans les fenêtres gelées du dictionnaire §5.

## 2. Famille fermée de comparaisons (proposition : 10 maximum)

Énumération définitive à arrêter et chaîner avec le dictionnaire validé,
avant calcul — la liste ci-dessous est la proposition soumise au
propriétaire ; elle ne peut que se réduire, jamais s'étendre après
consultation des résultats :

| ID proposé | Comparaison (descriptive) | Type |
|---|---|---|
| C4-01 | RV médiane des +1–5 j après confirmation d'une transition vers HAUT vs après confirmation vers BAS (REG-J) | médiane |
| C4-02 | Fréquence d'extrêmes (+1–5 j) après transition confirmée vs après transition non confirmée (même sens) | proportion |
| C4-03 | Durée médiane des états HAUT vs BAS (runs confirmés, REG-J) | médiane |
| C4-04 | Temps médian de retour à l'habituel après HAUT : ère 2010–13 vs 2017–20 | médiane |
| C4-05 | Part des transitions rapides (≤ 2 j) parmi les transitions confirmées : vers HAUT vs vers BAS | proportion |
| C4-06 | Skew médian des rendements (+1–5 j) après transition vers HAUT vs vers BAS | médiane |
| C4-07 | Part des jours en discordance F3 (état courant ≠ état-passé) : ère 2010–13 vs 2017–20 | proportion |
| C4-08 | Fréquence des impulsions IMP-M5 par journée : état courant HAUT vs BAS (REG-J) | ratio de taux |
| C4-09 | Part des jours à déphasage intrajournalier (état de session max ≠ état journalier) : état journalier HAUT vs BAS | proportion |
| C4-10 | Fréquence d'extrêmes M1 : état de queue HAUT vs BAS (dimension DIM-queues, à seuils causaux propres) | proportion |

## 3. Discipline statistique

- **Dépendance temporelle** : les journées d'un même état ne sont pas
  indépendantes. Inférence par **bootstrap par blocs de journées
  consécutives** (blocs de 20 journées de cotation, 2 000 répétitions,
  graine figée à l'exécution) pour toute comparaison portant sur des
  conséquences post-transition ; bootstrap par journées simples admis
  uniquement pour les fréquences d'états. Les deux effectifs (épisodes/
  journées bruts, blocs) sont publiés.
- Correction **BY** interne à la famille fermée des 10 (par famille
  d'échelle si le gel définitif les sépare — décision à écrire au gel,
  avant calcul, jamais après).
- Seuils matériels : 5 points pour une proportion, ratio 1,15 pour une
  médiane ou un taux ; suffisance ≥ 200 journées par bras et ≥ 30
  transitions par bras pour les comparaisons de transitions (un état rare
  ne doit pas être « confirmé » par quelques épisodes).
- Cohérence de signe dans ≥ 2 ères sur 3 quand la dimension comparée n'est
  pas l'ère ; en deçà : non concluant ou queue de distribution, **conservés
  et publiés** dans les résultats négatifs.
- Aucun test directionnel, aucun PnL, aucun coût ; les états ne sont pas
  des signaux. Nouvelles fiches éventuelles : J1 candidates descriptives
  au catalogue commun, même structure que les campagnes 1–3 ; aucune
  promotion automatique ; aucune ressemblance avec les fiches antérieures
  requise ou favorisée.
- Arrêt propre : garde d'intégrité (282 partitions) non satisfaite =
  suspension documentée, pas de publication partielle non étiquetée.
