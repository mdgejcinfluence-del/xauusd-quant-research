# PHASE 24-B — DÉCISION FINALE

Construction : 238 085 barres M15 (99,58 % complètes), 24 889 impulsions, 16 054 événements
réintégrés étiquetés (Y positif ≈ 52 %). Le changement de granularité multiplie les effectifs
conditionnels par ~4-5 par rapport au H1 de la Phase 24-A.

Verdicts par variante (critères 24-A maintenus sans réduction, modèle envisagé à 5 paramètres
sans indicatrices de session) :

- `M15_TIME_ONLY` : **`M15_TIME_ONLY_READY_FOR_CONDITIONAL_TRAINING`** (train min. 2 078 ; éval. 1 469/657) — contrôle de faisabilité.
- `M15_H4_TIME` : **`M15_H4_TIME_READY_FOR_CONDITIONAL_TRAINING`** (train min. 190, 38,0/paramètre ; éval. 139/62).
- `M15_D1_TIME` : **`M15_D1_TIME_READY_FOR_CONDITIONAL_TRAINING`** (train min. 193, 38,6/paramètre ; éval. 198/88).

Verdict global : **`M15_CONDITIONAL_ARCHITECTURE_FEASIBLE`** — les trois éléments (Directeur
H4 ou D1 inchangés, Horloge 08:00-16:00 UTC, Chauffeur M15 impulsion→repli→réintégration→reprise)
coexistent avec des cohortes causalement valides et une balance des classes permettant un
apprentissage défendable. Les deux variantes cibles restent proches des minima (139-198
événements d'évaluation, 45-59 grappes) : toute inférence future devra être gouvernée par les
grappes et les semaines ISO, pas par les effectifs bruts.

Cette faisabilité ne dit rien de la valeur prédictive ou économique du Chauffeur M15 — jamais
mesurée. Aucun entraînement n'est autorisé automatiquement après cette phase.
