# EMI-006 — RAPPORT EXÉCUTIF

**Question** : les clôtures réelles A–E relèvent-elles d'une persistance, d'une
réévaluation périodique ou d'une condition supplémentaire ?

## Résultat 1 — La persistance temporelle unique est réfutée, pas seulement non identifiée

Pour chaque panier et chaque seuil θ ∈ {−1…+3 bp} (grille préenregistrée
seq470), l'intervalle des durées de persistance continue compatibles est
(plus long segment favorable interrompu avant clôture ; durée du segment
final]. **L'intersection de ces intervalles sur les cinq paniers est vide
pour les 35 combinaisons** (θ × {continu, tolérance 0,5/1/2 s, cumulatif}).
La contradiction est portée notamment par B (un segment favorable
ininterrompu de 107,9 s **sans** clôture) contre C (segment final de 0,5 s)
et D (5,5 s). Aucune durée de confirmation unique — continue, cumulative,
en ticks ou tolérante aux interruptions — n'explique les cinq clôtures.
Replays sur grille : 1 à 5 clôtures prématurées et/ou manquées pour tout
point testé (`EXIT_MODEL_COMPARISON.csv`).

## Résultat 2 — Contre-exemple C

C clôture à −0,25 bp, **hors de l'état favorable** θ=0 : son dernier segment
favorable se termine 1,7 s avant la clôture. Toute règle exigeant un état
favorable strictement maintenu jusqu'à l'exécution est donc également
contredite, sauf seuil θ < 0 ou évaluation discrète antérieure.

## Résultat 3 — Cadence fixe ancrée à l'ouverture : réfutée sauf 1 s (triviale)

Cadences compatibles par panier (tolérance 1 s, grille postérieure au
segment final) : A {1}, B {1,2,3,6,7,14,17,21,34,42,51,102,119,238},
C {1,11,59}, D {1,2,4,8,16}, E {1,5,17,85}. **Intersection : {1 s}** —
c'est-à-dire l'évaluation continue, pas une cadence. Une cadence à phase
libre reste en revanche **non identifiable** : avec un seul événement par
panier, (N, φ) peut toujours être ajusté ; cinq clôtures ne contraignent
pas ce couple et nous refusons de le « découvrir ».

## Résultat 4 — Ce qui précède réellement les cinq clôtures

Un état proche ou au-dessus du PWA pendant une jambe de PnL en hausse :
variation du PnL latent sur 30 s avant clôture **positive 5/5**
(+1,6 à +7,2 bp), segments favorables présents avant chaque clôture
(C marginale autour du PWA). Les interruptions de l'état favorable sont
fréquentes (A 6, B 30, C 10, D 3, E 1) et retardent mécaniquement toute
règle à compteur — sans pour autant valider un compteur précis.

## Verdict de famille

Rapides (D, E) et récupérations (A, B, C) restent explicables par **une
même famille** (état favorable sur jambe haussière + mécanisme de
déclenchement non ponctuel), mais EMI-006 **réduit l'espace** : à
l'intérieur de cette famille, la persistance unique et la cadence ancrée
sont éliminées. Restent observationnellement équivalents : cadence à
phase libre, condition supplémentaire (hybride), ou évaluation sur une
variable non contenue dans les trajectoires Mid (Bid/Ask, horloge EA,
état interne). Aucun n'est sélectionné. `profitable_edge=False` (moteurs).
