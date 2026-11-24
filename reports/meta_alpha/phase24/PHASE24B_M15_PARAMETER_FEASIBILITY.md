# PHASE 24-B — FAISABILITÉ PARAMÉTRIQUE M15

Modèle envisagé (nouvelle architecture explicite, **pas une reproduction du M1**) : logistique à
4 variables numériques causales (ratio de repli, durée extrême→réintégration, MFE à la décision,
touches de P0) + intercept = **5 paramètres**. Aucune indicatrice de session : le contexte
temporel est la permission d'Horloge, et les catégories ASIA/NIGHT sont structurellement absentes
de la population autorisée — la quasi-séparation documentée en 24-A disparaît avec le dictionnaire
catégoriel. L'absence de variables de session est un choix d'architecture nouveau, documenté
comme tel.

Critères 24-A maintenus sans réduction (par variante : train minoritaire ≥ 20/paramètre = 100 ;
évaluation ≥ 100 événements et ≥ 50 minoritaires) — voir `PHASE24B_M15_CLASS_BALANCE.csv` :

- `M15_TIME_ONLY` : train minoritaire 2 078 (415,6/paramètre), éval. 1 469 (657) — faisable.
- `M15_H4_TIME` : train minoritaire 190 (38,0/paramètre), éval. 139 (62) — faisable, juste au-dessus des minima.
- `M15_D1_TIME` : train minoritaire 193 (38,6/paramètre), éval. 198 (88) — faisable.

Calibration : 83 à 1 377 événements selon la variante, deux classes présentes partout.
Indépendance : les événements se regroupent en 193 à 2 072 grappes (fenêtres chevauchantes) —
la faisabilité en nombre brut devra être lue avec cette dépendance : les effectifs indépendants
(grappes/semaines ISO) figurent dans `PHASE24B_M15_COHORT_COUNTS.csv` et devront gouverner
l'inférence future (bootstrap par grappe). Aucune anomalie de séparation détectable à ce stade
(balance Y ≈ 46-54 % dans chaque variante).
