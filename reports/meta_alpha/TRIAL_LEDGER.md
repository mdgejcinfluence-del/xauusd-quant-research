# TRIAL LEDGER — append-only (chaque essai préenregistré AVANT exécution)

## P3-001 (préenregistré, non exécuté)
Question: les variables certifiées (ROLL_STD_MID, ROLL_RANGE_MID, UPDATE_INTENSITY,
INTERARRIVAL_MEAN, niveaux de spread) présentent-elles une association conditionnelle
avec RET_H (labels 5s..1h) sur le seul échantillon IS?
Périmètre: IS calendaire 60% (2010-01-04 -> borne à geler avant exécution), purge >= 1h
aux frontières, aucun accès OOS/Holdout pour la sélection.
Méthode: statistiques conditionnelles par quantiles, tests de permutation temporelle,
correction des tests multiples (BH-FDR), conservation de TOUS les résultats
(positifs, négatifs, nuls). Aucun paramètre optimisé à ce stade.
Statut: PRÉENREGISTRÉ — en attente d'exécution.
