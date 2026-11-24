# PHASE 23-B — RAPPORT FINAL : CONTEXTE J-1 ET RÉACTIONS AUX ANNONCES

Statut : `EXPLORATORY_POST_HOC`. Registre fermé 23-A respecté (aucune 7e variable, aucune surprise
calculée, aucun consensus inventé). Holdout fermé. Verdicts au registre seq387.

## Étude A — Contexte macro J-1 (DGS10, DFII10 ; DTWEXBGS exclue faute de source vérifiable)

Aucune association robuste entre les variations de taux connues la veille et le comportement du
XAU/USD aux horizons 1/2/5 jours : 12/12 tests non significatifs après BH (q ≥ 0,094), corrélations
de rang ≈ −0,05 au mieux. Le contexte taux J-1 n'apporte ni information directionnelle ni
information d'amplitude démontrable. **Verdict : `J1_NO_ROBUST_ASSOCIATION`**
(DTWEXBGS : `INSUFFICIENT_HISTORICAL_COVERAGE` — miroirs incomplets rejetés plutôt qu'utilisés).

## Étude B — Annonces (FOMC uniquement ; CPI/PCE/NFP non énumérables officiellement sans clé API)

73 décisions FOMC 2010-2019 (dates des communiqués officiels federalreserve.gov, 14:00 ET converti
en UTC avec DST) contre 73 fenêtres témoins (même jour de semaine, même créneau, sans annonce) :

- **Réponse d'amplitude massive et significative** : amplitude (haut+bas) à 60 min de 100,6 bp en
  moyenne contre 19,8 bp chez les témoins (différence +80,8 bp, IC95 [+68,8 ; +93,5], q≈0) ; à 4 h :
  121,6 contre 30,7 bp (+90,9 bp, q≈0). Stable : 104,5/95,9 bp selon la sous-période.
- **Pas de direction moyenne** : rendement signé à 60 min +6,7 bp en moyenne, médiane ~0 — la
  réaction est bidirectionnelle, comme toutes les amplitudes de ce programme.
- Descriptif : après la réaction des 15 premières minutes, le mouvement se prolonge dans le même
  sens dans 71 % des cas à 60 min (médiane alignée +25 bp) et 88 % des fenêtres revisitent le prix
  pré-annonce — observation de continuation **descriptive**, non testée comme edge et non revendiquée
  comme effet directionnel (le signe est défini par la réaction elle-même).
- Spread : 2,23 bp (médiane pré-annonce) → 2,43 bp post-60 min : élargissement modéré, documenté
  dans la sensibilité d'exécution (aucun P&L calculé, conformément à l'ordre).

**Verdict Étude B : `MACRO_EVENT_VOLATILITY_RESPONSE`** pour le FOMC ; CPI/PCE/NFP :
`INSUFFICIENT_HISTORICAL_COVERAGE`.

## Réponses aux questions de clôture

1. Non (Étude A nulle). 2. Non (aucun contexte J-1 ne caractérise l'amplitude future).
3. Oui pour l'amplitude FOMC (expansion bidirectionnelle), non pour une direction moyenne ;
   continuation descriptive à confirmer par un contrat distinct. 4. Le seul candidat externe
   documenté est la **fenêtre FOMC comme régime d'amplitude** (et, à titre descriptif, la
   continuation post-réaction) — il justifierait au plus une recherche préenregistrée distincte,
   jamais un edge déclaré sur ces mêmes événements. Aucun modèle ni stratégie construits.
