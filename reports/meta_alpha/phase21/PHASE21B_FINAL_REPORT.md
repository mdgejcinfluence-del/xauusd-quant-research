# PHASE 21-B — RAPPORT FINAL : ASYMÉTRIE DIRECTIONNELLE APRÈS EXPANSION D1

Statut : `EXPLORATORY_POST_HOC`. Artefacts 21-A uniquement ; holdout interdit ; aucun P&L.
Verdict au registre seq375.

## Population

181 journées D1_EXPANSION (86 positives, 95 négatives, 0 neutre) regroupées en **126 épisodes** ;
population primaire = première journée d'épisode : **57 expansions positives, 69 négatives**
(références : 675 journées normales positives, 677 négatives). Toutes les comparaisons franchissent
les minima (≥50 événements, ≥20 semaines ISO) : 24/24 tests évaluables.

## Réponse à la question de clôture

**Non.** Après une journée D1 d'expansion, le signe de la journée n'apporte **aucune information
directionnelle démontrée** au-delà de la mémoire d'amplitude identifiée en 21-A :

- 24 tests préenregistrés (3 comparaisons × 4 horizons × terminal aligné + asymétrie d'excursion),
  bootstrap par grappes de semaines ISO (10 000 réplications, graine 2111), BH q=0,05 :
  **aucun significatif, q minimale = 0,968**.
- Expansions positives vs journées positives normales : effet aligné −0,6 à +22,9 bp selon l'horizon,
  p 0,48–0,98. Expansions négatives vs normales négatives : +11,8 à +18,3 bp, p 0,56–0,69.
  Positives vs négatives : aucune différence (p 0,55–0,98).
- Proportions de continuation proches du hasard (0,42–0,58) ; médianes alignées incohérentes
  (expansion positive H5 : moyenne +23,4 bp, médiane −20,3 bp).
- L'amplitude, elle, persiste (cohérent 21-A) : MFE médians 63–163 bp, mais MAE médians comparables
  (55–160 bp) — excursion favorable et adverse du même ordre, asymétrie médiane instable (−6 à +52 bp).
  Les dépassements des références 4,0/4,5 bp (`REFERENCE_COST_UNVERIFIED`) sont des couvertures
  d'amplitude, pas des profits.

## Stabilité (descriptif)

Les moyennes alignées brutes sont positives en 2010-2015 (+16 à +85 bp) et négatives en 2016-2019
(−10 à −63 bp) pour les deux signes — inversion complète entre sous-périodes, sans significativité
dans aucun test. Aucun candidat de continuation/retournement n'est retenu ; le motif brut serait
de toute façon instable.

## Verdicts

- `D1_POSITIVE_EXPANSION_*` / `D1_NEGATIVE_EXPANSION_*` (continuation ou retournement) : **non attribués**.
- `D1_SIGNED_EXPANSION_ASYMMETRY_IDENTIFIED` : **non attribué**.
- **Verdict global : `D1_AMPLITUDE_PERSISTENCE_WITHOUT_DIRECTION`.**

Le signe de l'expansion D1 n'ajoute rien de directionnel à la mémoire d'amplitude 21-A.
Aucun edge, aucune recherche économique automatique à la suite de cette phase.
