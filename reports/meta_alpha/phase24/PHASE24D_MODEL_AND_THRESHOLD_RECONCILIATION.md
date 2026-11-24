# PHASE 24-D — RÉCONCILIATION MODÈLE ET SEUIL

Modèle unique réutilisé : `M15_TIME_ONLY` de Phase 24-C, coefficients et prédictions repris des
artefacts gelés (`PHASE24C_MODEL_REGISTRY.json`, `PHASE24C_COEFFICIENTS.csv`,
`PHASE24C_EVENT_PREDICTIONS.parquet`) — aucun réentraînement, aucune recalibration.
**Seuil gelé retrouvé : 0,560955** (prévalence Y du train TIME_ONLY 2010-2015), appliqué tel quel.
Cohorte d'évaluation réconciliée : 1 469 événements TIME_ONLY, dont **1 124 sélectionnés**
(p ≥ seuil) ; P1 (permission H4) : 86 ; P2 (permission D1) : 133 — sous-ensembles stricts de P0,
identifiants conservés. Direction = sens de l'impulsion M15, jamais inversée. Les événements M15
(Q90) ne sont pas les événements H1 historiques (Q95) ; aucun coefficient M1 n'est impliqué.
