# CAMPAGNE 5 — INCIDENTS, LIMITES ET COÛTS

## Incidents
1. **Run CI 44892050419 — atteintes journalières à zéro.** Bug
   d'initialisation du moteur : la branche premier jour utilisable
   (SANS_REFERENCE) ne peuplait jamais les niveaux de référence
   Hprev/Lprev, donc aucune journée suivante ne pouvait produire
   d'atteinte (atteintes_jour=0, touches=0). Diagnostic immédiat sur
   `C5_COVERAGE.json`, correctif minimal (assignation des niveaux du
   premier jour), tests temporels re-vérifiés verts, run corrigé
   44892455679 : atteintes_jour 2 375, touches 7. Aucune définition du
   gel n'a été modifiée ; seuls les comptages de couverture,
   d'ouvertures et de semaines du run 1 étaient informatifs.
2. **Synthèse locale — deux correctifs de code sans portée
   méthodologique** : (a) la branche « bras vide » du bootstrap
   renvoyait des effectifs à zéro (corrigée pour publier les effectifs
   réels, ce qui a fait apparaître C5-03 : 2 565 / 0) ; (b) la q BY de
   famille était contaminée par le p NaN de la comparaison non testable
   (BY désormais appliqué aux seules p calculables de la famille, F-E :
   m=4, publié). Aucun seuil, aucune lecture gelée n'a été touché.
3. Deux relances de synthèse ont été lancées en parallèle d'une édition
   du même fichier (résultats relus sur l'ancienne version) ; relance
   séquentielle propre ensuite, vérifiée. Aucun impact sur les sorties
   finales.

## Limites assumées (gel)
- CONTENUE ETABLIE (1 440/1 440) n'est jamais atteinte sur ce corpus
  (halte quotidienne) : C5-10 dégénérée, assumée d'avance au gel.
- C5-03 : la classe TROU_INTRA_SEMAINE ne compte que 2 journées en dix
  ans, toutes deux inéligibles par le retard d'ouverture ; la
  comparaison est structurellement non éligible sur ce corpus.
- C5-09 : la continuité complète depuis lundi 00:00 UTC ne laisse que
  187 atteintes hebdomadaires réelles identifiables ; non éligible.
- Toutes les associations sont descriptives et contemporaines ; aucune
  n'est une preuve prédictive ni une opportunité exploitable.

## Coûts et budgets
- Calcul : 2 runs GitHub Actions (extraction décennale complète) +
  synthèse locale. Coût financier : 0 FCFA.
- Budgets expérimentaux : **aucun consommé** (tick 148/150, panel
  28/60, exo 6/60, P7 0/24, NR 0/24, P9 10/12 — inchangés).
- Holdout 2020–2026 scellé, non touché ; FRED suspendue ; 36 cellules
  S12 gelées ; T0 séparé inactif ; Phase 12.3 suspendue
  (`P12_3_CONFIGURATIONS.csv` non consulté) ; fiches des campagnes 0–4
  non modifiées ; sensibilité ANO-C2-003/006/008/012 non recalculée.
