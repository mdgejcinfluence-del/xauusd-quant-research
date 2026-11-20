# CAMPAGNE 0 — RAPPORT DES BASELINES COMPORTEMENTALES XAU/USD

« Aucune brique de ce programme ne possède à ce jour un edge directionnel démontré isolément (142 entrées d'audit). Les scénarios ci-dessous sont des hypothèses composites neuves, construites sur des faits structurels documentés (seq citées à l'appui), et non l'assemblage d'edges prouvés. Toute conclusion de rentabilité avant les gates de confirmation sur holdout est interdite. La règle permanente s'applique : pas de ticket de challenge sans μ > 0 net démontré aux deux ancres de coût. »

**DESCRIPTIF — IS UNIQUEMENT — AUCUNE MESURE DE PERFORMANCE.**
Campagne autorisée seq 152, dictionnaire gelé et chaîné **avant calcul** (seq 153,
sha256 corrigé seq 154 : `974881a7…`). Moteur exécuté en CI sur le corpus tick IS du
programme (**282/282 partitions, 0 sautée, 3 097 journées distinctes, 3 537 724 barres
M1**), runs 44710336549 (premier calcul) et 44713904881 (synthèse complétée V6–V10).
Zéro essai consommé, aucun backtest, aucun holdout ouvert. Budgets inchangés :
tick 148/150 · panel 28/60 · exo 6/60 · P7 0/24 · NR 0/24 · P9 10/12.

Ce rapport répond à la question du propriétaire : *comment XAU/USD se comporte-t-il
normalement ?* Il ne présente aucune stratégie, aucune rentabilité, aucune anomalie
sélectionnée pour son profit. Les chiffres complets sont dans
`CAMPAIGN_00_BASELINE_METRICS.csv` (288 cellules).

## 1. Le comportement normal de l'or, en une page

**Échelle des mouvements.** Le rendement d'une barre M1 a une médiane de 0, un écart-type
de **2,57 bp** (P90 ±2,3 bp, P99 ±7,2 bp) ; en M5 σ = 5,70 bp, M15 σ = 9,78 bp,
H1 σ = 18,1 bp (P90). La volatilité réalisée d'une journée vaut en médiane
**~71–75 bp** (P90 ~124, P99 ~210–238 selon l'horizon de mesure) : une journée normale
d'or bouge de l'ordre de 0,75 %, une journée à 2 % est un événement de queue (P99).

**Amplitude et excursions.** L'amplitude médiane d'une barre vaut 2,0 bp (M1), 5,2 (M5),
9,3 (M15), 19,4 (H1) ; les excursions haussière et baissière intra-barre sont quasi
symétriques à tous les horizons (médianes 0,75/0,78 bp en M1 ; 7,9/8,0 en H1) — le
marché normal ne penche ni d'un côté ni de l'autre à ces échelles.

**Persistance et retournements.** La corrélation lag-1 des rendements de barre est
**−0,004 (M1), −0,012 (M5), −0,007 (M15), +0,009 (H1)** : à ces horizons, le signe de
la barre précédente ne dit pratiquement rien du signe de la suivante. Les
retournements de signe surviennent dans **49,9 % (M1) à 52,5 % (H1)** des paires —
le hasard d'une pièce équilibrée, légèrement plus en H1. C'est la baseline contre
laquelle toute future prétention de persistance ou de réversion devra se mesurer.

**Retracements.** Après une impulsion (barre ≥ P90 de |r| de l'horizon), le retour
contraire maximal sous 12 barres vaut en médiane **94 % de l'impulsion en M1, 90 % en
M5, 83 % en M15, 54 % en H1** (la mesure peut dépasser 100 % quand le mouvement
contraire dépasse l'impulsion) : aux petites échelles, une impulsion est normalement
presque entièrement « rendue » dans les minutes qui suivent ; à l'heure, environ la
moitié seulement. Description, pas signal : c'est le comportement de référence des
familles « impulsion/retracement » du blueprint.

**Consolidations et compression.** Les épisodes d'amplitude inférieure à la médiane
durent en médiane **2 barres** à tous les horizons (P90 : 6–8 barres). Le ratio
d'amplitude journalière (jour/médiane globale) vaut 0,94–0,98 en médiane et 2,6–2,8
au P99 : les journées d'expansion extrême existent mais sont des queues, pas un régime
fréquent.

**Spread.** Le spread coté médian est remarquablement stable : **2,32 bp** quel que
soit l'horizon de barre (P90 ~3,9, P99 ~5,4–5,5) sur l'ancien corpus — cohérent avec
le spread médian IS de 2,33 bp mesuré dès le gate F15 (seq 109).

## 2. Décompositions (session, régime, ère) — ce que le contexte change

**Sessions** (σ du rendement M1) : New York **3,09 bp** > Londres 2,66 > Asie 2,02 ≈
Nuit 1,93. L'activité et l'amplitude se concentrent sur les heures américaines ; les
spreads médians restent voisins entre sessions actives.

**Régimes F3** (terciles de vol prédite du jour, causaux) : σ M1 = 1,87 / 2,31 / 3,01 bp
de bas en haut — le conditionnement par F3 ordonne bien l'échelle des mouvements
(×1,6 du bas au haut), sans rien dire de leur direction : c'est exactement le rôle de
service certifié de F3, retrouvé ici en baseline.

**Ères** : σ M1 = **3,00 bp (2010–13) → 2,54 (2014–16) → 1,85 (2017–20)** ; même pente
à tous les horizons (H1 P99 : de ~19 bp d'écart-type relatif en début de période à ~11
en fin, en M5). **Le marché de l'or s'est calmé de façon monotone sur la décennie IS** :
toute baseline non conditionnée par l'ère surestimerait le « normal » récent d'environ
60 % en M1. C'est l'observation la plus structurante de la campagne pour la suite :
les références devront être datées, pas seulement conditionnées.

## 3. Registre des observations candidates (étape C — sans mécanisme, sans rentabilité)

Conformément à l'ordre, les comportements atypiques ci-dessous sont **enregistrés**,
tous conservés (la limite de 10 ne borne que le développement détaillé futur) ; aucun
mécanisme économique n'est inventé pour les expliquer et aucune rentabilité ne leur
est attribuée. Ce ne sont pas encore des fiches ANO-J1 au sens du blueprint (qui
exigent seuils préenregistrés de campagne de détection et réplication formelle) :

| # | Observation descriptive | Chiffres | Statut |
|---|---|---|---|
| OBS-C0-01 | Calme séculaire : baisse monotone de σ entre ères, tous horizons | M1 : 3,00 → 2,54 → 1,85 bp | Candidate, à confirmer contre baseline par ère |
| OBS-C0-02 | Concentration new-yorkaise de l'amplitude | σ M1 NY 3,09 vs Asie 2,02 bp | Candidate |
| OBS-C0-03 | Retracement quasi complet des impulsions aux petites échelles | médiane 94 % (M1) → 54 % (H1) sous 12 barres | Candidate |
| OBS-C0-04 | Absence de persistance de signe aux horizons mesurés | lag-1 ∈ [−0,012, +0,009] ; retournements ~50–52 % | Baseline négative (borne toute future prétention) |
| OBS-C0-05 | Stabilité du spread médian entre horizons et sessions actives | 2,32 bp, P99 ~5,5 | Baseline de coût |
| OBS-C0-06 | Queues journalières : journée à ≥ 2 % ≈ P99 | RV jour P99 210–238 bp vs médiane ~72–75 | Candidate (événements extrêmes) |

## 4. Ce que la campagne n'a pas fait (limites écrites)

- Familles du blueprint **non couvertes** à ce stade (périmètre futur) : ouvertures et
  transitions de session à résolution tick, dépassements/réintégrations de niveaux,
  cassures et leur devenir, niveaux précédents, forme post-news au-delà de l'existant
  (P11-A1). Les baselines de la Campagne 0 sont des références de *distribution*, pas
  encore des références d'*épisodes structurels*.
- V6/V7 sont des statistiques poolées uniques par horizon (leur ligne porte n = 1 par
  construction dans le CSV) : la règle de suffisance du dictionnaire, pensée pour des
  distributions, les étiquette « NON CONCLUANTE » mécaniquement ; leurs valeurs
  (calculées sur 3,5 M de paires en M1) sont descriptives et doivent être lues comme
  telles — limite de présentation signalée, non corrigée après lecture.
- V8 (retracement) mesure un retour contraire cumulé maximal : il peut dépasser 100 %,
  ce n'est pas une « part retracée » bornée.
- Barres construites sur Mid (déclaré au dictionnaire) : aucune de ces distributions
  n'est un prix exécutable ; le spread est rapporté séparément (V12).
- Régime « NON_CLASSE » (jours sans prédiction F3) : conservés en global, exclus des
  décompositions par régime, comme gelé.

## 5. Réponse à la question du propriétaire

**Oui, partiellement — et c'est un oui borné.** Nous connaissons maintenant, de façon
chiffrée, reproductible et datée, les distributions normales de l'or aux horizons
M1–H1 : échelles de mouvement, excursions, persistance (nulle), retournements (~50 %),
retracements, consolidations, queues, spreads, et leurs variations par session, par
régime F3 et par ère — avec la leçon structurante que le « normal » a dérivé de ~60 %
en une décennie. C'est la matière première de l'étape B du pipeline pour les familles
de distribution. En revanche, les familles d'épisodes (niveaux, cassures, opens,
transitions) n'ont pas encore leurs baselines : identifier méthodiquement les
anomalies *structurelles* exige la campagne suivante, préenregistrée, sur ces
familles-là. Recommandation soumise : autoriser une **Campagne 1** descriptive
(familles d'épisodes, mêmes garde-fous) avant toute étape de détection formalisée —
décision du propriétaire.

*Annexes : `CAMPAIGN_00_VARIABLE_DICTIONARY.md` (gelé seq 153/154),
`CAMPAIGN_00_BASELINE_METRICS.csv` (288 cellules), `CAMPAIGN_00_DATA_QUALITY.md`,
`CAMPAIGN_00_METHOD_AND_MULTIPLICITY.md`. Chaîne : seq 152 (mission) → 153–154 (gel)
→ calcul CI → présente livraison. FRED toujours suspendue (seq 145), rotation
pendante côté propriétaire.*
