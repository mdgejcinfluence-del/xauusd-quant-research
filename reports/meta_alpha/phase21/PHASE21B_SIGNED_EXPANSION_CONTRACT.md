# PHASE 21-B — CONTRAT EXPANSIONS D1 SIGNÉES

Statut : `EXPLORATORY_POST_HOC`. Artefacts 21-A uniquement (barset, catalogue de régimes) ; ticks non relus ;
holdout 2020-2026 interdit ; aucun M1/modèle/stratégie/P&L. Référence 21-A seq373.

## Groupes (définitions gelées 21-A : Q90 roulant 250 j, jour courant exclu)

- A `D1_POSITIVE_EXPANSION` : régime D1_EXPANSION, BODY_BP > 0
- B `D1_NEGATIVE_EXPANSION` : régime D1_EXPANSION, BODY_BP < 0
- C `D1_NEUTRAL_EXPANSION` : régime D1_EXPANSION, BODY_BP = 0 (descriptif)
- D `D1_NORMAL_POSITIVE` : régime D1_NORMAL, BODY_BP > 0
- E `D1_NORMAL_NEGATIVE` : régime D1_NORMAL, BODY_BP < 0
- Compression : descriptive uniquement. Aucun seuil supplémentaire.

## Populations

- Primaire : première journée de chaque épisode consécutif D1_EXPANSION (`D1_EXPANSION_EPISODE_ID`,
  signe = signe de la première journée). Références normales : toutes journées D1_NORMAL du signe correspondant.
- Secondaire : toutes journées D1_EXPANSION, regroupement par épisode obligatoire dans l'inférence.

## Mesures (depuis clôture événement, horizons 1/2/3/5 journées complètes, colonnes certifiées 21-A)

`FUTURE_TERMINAL_BP`, `FUTURE_UP_BP`, `FUTURE_DOWN_BP` (déjà en log-bp ×10000 dans le barset 21-A) ;
`DIRECTION_ALIGNED_TERMINAL_BP = signe × TERMINAL` ; favorable/adverse selon signe ;
`EXCURSION_ASYMMETRY_BP = favorable − adverse` ; ratio favorable/adverse (dénominateur nul → NaN documenté,
jamais remplacé). Temps UTC écoulé enregistré en heures. Horizon censuré si NaN 21-A (jamais comblé).

## Inférence préenregistrée

Famille = 3 comparaisons × 4 horizons × 2 mesures (terminal aligné, asymétrie d'excursion) = **24 tests** :
(1) A vs D, (2) B vs E, (3) A vs B. Bootstrap par grappes de semaines ISO (épisodes préservés),
10 000 réplications, graine 2111, p percentile bilatérale `2×min(P(Δ≤0), P(Δ≥0))`, BH q=0,05.
Minima : ≥50 événements et ≥20 semaines ISO par groupe, sinon `NON_EVALUABLE_INFERENTIAL`.
Seuils 30/60/100 bp et références 4,0/4,5 bp (`REFERENCE_COST_UNVERIFIED`) : descriptifs uniquement.
