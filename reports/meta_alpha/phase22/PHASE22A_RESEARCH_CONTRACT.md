# PHASE 22-A — CONTRAT DE RECHERCHE (FAMILLES A ET B SÉPARÉES)

Statut : `EXPLORATORY_POST_HOC`. Holdout 2020-2026 interdit. Aucune fusion des familles, aucun portefeuille.
Événements = événements de cotation, jamais preuve de stops institutionnels ni de remplissages réels.

## Famille A — Sweep & Reclaim (tick, fenêtre principale 08:00–16:00 UTC)

Niveaux : A1 Overnight High / A2 Overnight Low (Mid 00:00–08:00), A3 Previous Day High / A4 Previous Day Low
(journée D1 certifiée précédente, artefacts 21-A). Franchissement : Mid au-delà du niveau ± buffer, buffer =
médiane du spread des 5 minutes précédentes (causal, converti en prix). Réintégration : premier tick de retour
à l'intérieur. Entrée théorique : premier Bid (SHORT après sweep haut) / Ask (LONG après sweep bas) après
confirmation, délai max 60 s, sinon `NON_EXECUTION`. Primaire = 1er confirmé par niveau et par jour.
Horizons : 15/30/60 min, 4 h, clôture D1. Sans réintégration : `BREAKOUT_WITHOUT_RECLAIM` (groupe de contrôle).

## Famille B — Impulse–Pullback–Resumption (H4 certifié 20-A)

Impulsion : `ABS_BODY_BP > Q90` causal sur 250 barres H4 complètes précédentes (courante exclue).
Pullback : première barre ultérieure de sens opposé. Invalidation : retour au prix d'ouverture de l'impulsion
(`IMPULSE_FULL_RETRACE_INVALIDATION`). Reprise : première clôture au-delà du High/Low de la barre précédente,
dans les 8 barres suivant l'impulsion, sinon `NO_RESUMPTION_WITHIN_8_H4`. Épisodes primaires non chevauchants.
Entrée théorique : premier Ask/Bid après confirmation = ouverture de la barre H4 suivante (barset certifié).

## Coûts (comptabilité 19-B)

Spread intégré exactement une fois (achat Ask / vente Bid, prix réels des cotations/barres certifiées) ;
slippage S0=0, S1=0,5, S2=1 bp par côté (S2 principal), appliqué en prix ; commissions exclues.
Résultats nommés `HYPOTHETICAL_NET_OF_SPREAD_AND_SCENARIO_SLIPPAGE_BEFORE_COMMISSION`.
Aucune conversion monétaire. Références 4,0/4,5 bp = `REFERENCE_COST_UNVERIFIED`.

## Inférence préenregistrée (18 tests, BH q=0,05 sur les deux familles)

Bootstrap par grappes de semaines ISO, 10 000 réplications, graine 2117. A : rendement net S2 directionnel
moyen ≠ 0, par niveau (4) × horizon (1 h, 4 h, EOD) = 12 tests (population primaire). B : rendement net S2
aligné moyen ≠ 0 aux horizons 2/4/8 barres (3) + reprise vs sans-reprise, terminal aligné (3) = 6 tests.
Minima 50 événements / 20 semaines ISO sinon `NON_EVALUABLE_INFERENTIAL`. Candidature
`ECONOMIC_CANDIDATE_EXPLORATORY` seulement si asymétrie + net S2 + risque adverse documentés ensemble.
