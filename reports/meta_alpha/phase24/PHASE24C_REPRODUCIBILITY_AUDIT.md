# PHASE 24-C — AUDIT DE REPRODUCTIBILITÉ

- Algorithme : régression logistique IRLS **reproduite du code gelé Phase 12-B**
  (`logistique_irls` : non pénalisée, ridge numérique 1e-8, tolérance 1e-10, 200 itérations max,
  z écrêté à [−35, 35], variables brutes sans standardisation). Aucun tuning, aucune sélection.
- Population : panneau gelé `PHASE24B_M15_GATE_PERMISSION_PANEL.parquet` ; réconciliation avec
  les effectifs 24-B exacte (`PHASE24C_COHORT_RECONCILIATION.csv` : 4 733/1 469 ; 408/139 ;
  469/198). Aucun événement scindé entre segments (splits par année de t0 du panneau gelé).
- Seuil de classification de chaque modèle = prévalence Y du train propre (0,561 / 0,534 / 0,588),
  calculé avant tout examen de l'évaluation, jamais ajusté sur calibration ou évaluation.
- Prédictions événement par événement conservées (`PHASE24C_EVENT_PREDICTIONS.parquet`,
  probabilités des trois modèles + trois M0), coefficients et erreurs standards publiés.
- Graine bootstrap 2123, 10 000 réplications par grappe. Holdout 2020-2026 jamais accédé ;
  aucun P&L calculé.
- Divergence documentée (déjà gelée en 24-B) : impulsion M15 au Q90/250 barres contre Q95 pour
  l'historique H1 — les événements M15 ne sont pas les événements H1, et aucun coefficient M1
  n'est réutilisé ni présenté comme reproduit.
