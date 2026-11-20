# CAMPAGNE 1 — BASELINES DES ÉVÉNEMENTS STRUCTURELS XAU/USD

« Aucune brique de ce programme ne possède à ce jour un edge directionnel démontré isolément (142 entrées d'audit). Les scénarios ci-dessous sont des hypothèses composites neuves, construites sur des faits structurels documentés (seq citées à l'appui), et non l'assemblage d'edges prouvés. Toute conclusion de rentabilité avant les gates de confirmation sur holdout est interdite. La règle permanente s'applique : pas de ticket de challenge sans μ > 0 net démontré aux deux ancres de coût. »

**DESCRIPTIF — IS UNIQUEMENT — AUCUNE MESURE DE PERFORMANCE.**
Dictionnaire des événements gelé et chaîné avant calcul (seq 157, sha256
`e7da58c7…`). Moteur CI sur le corpus tick IS (282 partitions) : **224 748 lignes
d'événements bruts** (`CAMPAIGN_01_EVENTS_RAW.csv`), synthèses dans
`CAMPAIGN_01_EVENT_METRICS.csv` et `CAMPAIGN_01_CONDITIONAL_COMPARISONS.csv`.
Zéro essai, aucun backtest, holdout intact, budgets inchangés (tick 148/150 ·
panel 28/60 · exo 6/60 · P7 0/24 · NR 0/24 · P9 10/12). Familles **EV4
(compression/expansion) et EV7 (extrêmes hebdomadaires) : NON PRODUITES par ce run**
— le moteur livré couvre EV1, EV2, EV3, EV5, EV6 ; EV4/EV7 restent au périmètre
futur, écrit sans détour. **F7 : NON MESURÉ** (série horaire non versionnée,
seq 146) — aucun croisement « risque de saut » n'est présenté ni substitué.

## 1. Comment le marché se comporte autour de ses niveaux (EV2/EV3)

**Dépassements (EV2).** 36 011 débuts de dépassement de niveaux Asie/veille détectés
(5 057 grappes jour×niveau, 2 515 journées). **85 % environ sont réintégrés sous
60 minutes** (30 590 réintégrations), avec un **délai médian de réintégration de
3 minutes** — identique dans les trois ères et toutes les sessions actives — et une
profondeur médiane, pour les dépassements réintégrés, de **10,5 bp** au-delà du
niveau (12,5 bp en 2010–13 → 8,2 bp en 2017–20 : les balayages sont devenus moins
profonds à mesure que le marché se calmait, cohérent avec la campagne 0). Le spread
à l'événement vaut 2,28 bp en médiane : ces épisodes ne sont pas des épisodes de
coût anormal. L'amplitude future (range) après réintégration vaut en médiane
2,9/7,0/12,3/17,7/25,2 bp à +1/+5/+15/+30/+60 min — du même ordre que l'amplitude
inconditionnelle des mêmes horizons (campagne 0), ce qui borne déjà toute lecture
« spéciale » de l'après-réintégration.

**Cassures (EV3).** 3 957 cassures confirmées (+5 bp au-delà du niveau, 2 763
grappes) ; **79 % sont retestées sous 60 min** (3 128 retests) et, après retest, le
prix est **encore au-delà du niveau à +60 min dans 55 % des cas** — à peine plus
qu'une pièce équilibrée, et c'est une fréquence descriptive conditionnelle (détecter
une cassure conditionne sur l'amplitude déjà réalisée), pas une probabilité
exploitable. L'amplitude future après retest (5,3/11,8/20,9/29,0/40,4 bp) est
supérieure à celle d'après réintégration : les contextes de cassure sont des
contextes de volatilité plus élevée (profondeur médiane 24,3 bp contre 10,5), ce qui
interdit de comparer les deux devenirs sans conditionner sur l'amplitude — exactement
le biais que le dictionnaire demandait de documenter.

## 2. Impulsions, consolidations, extrêmes (EV5/EV6/EV1)

**Impulsions M5 (EV5).** 69 721 impulsions (|r| ≥ P90 poolé ≈ 10,9 bp en médiane
d'amplitude). Le retour contraire maximal sous 12 barres vaut en médiane **90,5 %**
de l'impulsion ; il atteint ≥ 50 % dans 66 % des cas et **≥ 100 % dans 46,6 %** —
avec une dérive d'ère nette : retour complet 49,3 % (2010–13) → 40,2 % (2017–20),
les impulsions « tiennent » un peu mieux dans le marché récent, plus calme. Par
session : retours les plus complets à Londres/New York (94–95 % en médiane), les
moins complets la nuit (69,8 %).

**Consolidations (EV6).** 71 053 épisodes d'au moins 6 barres calmes ; durée
médiane **9 barres** (le dictionnaire n'exigeait que ≥ 6 : la médiane observée est
au-dessus du seuil minimal, ce n'est pas un artefact de seuil). Le range des 60
minutes suivant la fin d'une consolidation vaut en médiane 14,3 bp — inférieur à
l'amplitude horaire inconditionnelle (~19,4 bp, campagne 0) : sortir d'une
consolidation ne signifie pas, en médiane, entrer dans une expansion.

**Extrêmes (EV1).** 10 288 faits de session/journée. L'heure médiane de formation
des extrêmes **journaliers** (haut comme bas) est **11 h UTC**, stable par ère et
par régime : la journée d'or fabrique typiquement ses extrêmes en fin de matinée
européenne, avant le pic d'activité américain (13–15 h, campagne 0) — les extrêmes
ne se forment pas là où le volume culmine.

## 3. Registre des anomalies candidates

Cinq observations sont inscrites au registre (`CAMPAIGN_01_ANOMALY_REGISTER.csv`,
ANO-C1-001 à 005) : réintégration fréquente et rapide des dépassements ; devenir
des retests (~55 %) ; retours d'impulsion ≥ 100 % dans ~47 % des cas ; formation
des extrêmes vers 11 h UTC ; amplitude post-consolidation contenue. Toutes sont
classées **J1 candidates (observations descriptives)** : aucun mécanisme économique
n'est inventé pour les expliquer, aucune direction prédictive ne leur est attribuée,
aucune rentabilité ne leur est prêtée, aucune stratégie n'est construite dessus.
Toute promotion J2 exigera mécanisme documenté + confirmation disjointe +
autorisation distincte.

## 4. Corrections et clarifications de la Campagne 0 (exigées par l'ordre)

1. **« Une journée normale bouge de ~0,75 % »** signifie exactement : la médiane,
   sur 3 048 journées IS, de la volatilité réalisée journalière
   `sqrt(Σ r²)` vaut ~72–75 bp selon l'horizon de barres utilisé. Ce n'est ni
   l'écart-type du rendement journalier close-to-close, ni une variation typique
   entre deux clôtures : c'est la racine de la somme des carrés des mouvements
   intra-journée — une mesure de chemin parcouru, toujours ≥ |variation nette|.
2. **Variance vs écart-type entre ères** : l'écart-type du rendement M1 passe de
   3,00 à 1,85 bp, soit **−38 % en écart-type et −62 % en variance** (le carré) ;
   le « calme de ~60 % » du rapport de campagne 0 parle en variance. Les deux sont
   corrects à condition de ne pas les mélanger : les seuils en bp vivent en
   écart-type, les énergies en variance.
3. **Portée du lag-1** : une autocorrélation de signe ≈ 0 aux horizons 1–60 min
   exclut une dépendance **linéaire simple du signe à un pas** ; elle ne dit rien
   des dépendances d'amplitude (volatilité, démontrée et persistante), des horizons
   plus longs, des conditionnements rares (événements), ni des non-linéarités.
   **La neutralité directionnelle globale n'est pas une preuve de comportement
   aléatoire** : ce marché a une mémoire de volatilité forte (F3, R² = 0,20) et des
   calendriers marqués ; il n'a simplement pas de mémoire linéaire de signe à ces
   échelles, en moyenne inconditionnelle.
4. **Les « 94 % de retracement M1 »** sont définis algorithmiquement : après chaque
   barre M1 dont |r| ≥ P90 poolé de |r| M1, on cumule les rendements des 12 barres
   suivantes dans le sens contraire à l'impulsion, on prend le maximum de ce cumul
   (plancher 0), on le divise par |impulsion| ; la médiane de ce ratio sur les
   événements vaut ~94 %. Ce n'est ni une part du mouvement « rendue » au sens d'un
   retour au prix de départ, ni un taux de réussite : le ratio peut dépasser 100 %.
5. **« Consolidation de 2 barres » (campagne 0, V9)** : suite maximale de barres
   consécutives dont l'amplitude (haut−bas) est inférieure à la médiane poolée des
   amplitudes de l'horizon ; la durée médiane de ces suites vaut 2 barres. En
   campagne 1 (EV6), le seuil minimal a été porté à 6 barres et la durée médiane
   observée est de 9 barres : deux objets différents, ne pas confondre les chiffres.
6. **Stabilité du spread de 2,32 bp** : médianes par session (campagne 0, M1) —
   Asie 2,34 / Londres 2,20 / New York 2,27 / nuit 3,16 bp (série horaire) ; par
   régime F3, le spread médian reste dans une bande étroite (~2,2–2,4 bp) alors que
   la volatilité varie de ×1,6 : le coût médian est stable là où l'amplitude ne
   l'est pas (les queues de spread, elles, s'élargissent en régime haut, P99 ~5,5).

## 5. Limites

Barres sur Mid (déclaré) : profondeurs et dépassements sont des mesures de prix
médian, pas d'exécution. Détection conditionnée sur l'amplitude réalisée (biais
documenté au dictionnaire) : les fréquences de continuation/retournement ne sont
pas des probabilités de trade. EV4/EV7 non produites ; F7 non mesuré ; le NR
(2020+) n'est couvert qu'en résolution horaire partielle (hors périmètre de ce
run) : ces baselines sont celles de l'ancien corpus, à dater comme telles.
Événements d'une même journée regroupés en grappes pour les statuts de suffisance ;
les comptages bruts (36 011 dépassements) ne sont pas des observations
indépendantes (5 057 grappes).

**STATUT : CAMPAGNE 1 LIVRÉE — VALIDATION DU PROPRIÉTAIRE EN ATTENTE.**
La question à laquelle le propriétaire peut désormais répondre : les comportements
structurels de l'or ont-ils des références normales suffisamment établies pour que
la phase de détection formalisée des anomalies (étape C, fiches J1 préenregistrées)
puisse commencer — sur les familles couvertes (niveaux, impulsions, consolidations,
extrêmes) comme sur celles qui restent à cartographier (EV4, EV7, opens) ?

*Annexes : dictionnaire gelé, `CAMPAIGN_01_EVENT_METRICS.csv`,
`CAMPAIGN_01_CONDITIONAL_COMPARISONS.csv`, `CAMPAIGN_01_ANOMALY_REGISTER.csv`,
`CAMPAIGN_01_DATA_QUALITY.md`. Chaîne : seq 156 → 157 (gel) → calcul → livraison.
FRED suspendue (seq 145) ; 36 cellules toujours gelées.*
