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
Statut: EXÉCUTÉ — run 43495787484, succès 4 h 41 min, résultats bruts dans
p3/P3_001_RESULTS.json, gate dans GATE_P3_001.md. Hypothèse générée H-P3-A
(non adoptée): voir gate. Aucun paramètre modifié après observation.

## P4-001 (préenregistré, non exécuté)
Candidat déterministe explicite issu de H-P3-A: règle binaire causale
« volatilité courte (ROLL_STD_100) dans son quintile supérieur causal
(seuils walk-forward, jamais globaux) » -> exposition longue simulée Bid/Ask
sur horizons 15 min/1 h, origines NON chevauchantes, coûts = spread réel tick
d'entrée/sortie + slippage inconnu classé CONDITIONAL (jamais NET).
Inférence: bootstrap par blocs temporels; validation OOS chronologique
(20% central), purge >= 1 h; Holdout toujours scellé.
Critère de rejet préenregistré: si l'intervalle bootstrap du rendement net
de spread inclut 0 en OOS, le candidat est REJETÉ et conservé comme négatif.
