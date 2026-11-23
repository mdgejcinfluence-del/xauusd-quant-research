# PHASE 18-C — AUDIT DE REPRODUCTIBILITÉ

1. **Reproduction de la Phase 17-E** : le réentraînement de BASE_7 sur la cohorte 17-E d'origine (étiquetés aux anciennes variables complètes) reproduit les coefficients committés de `PHASE17E_M2R_B08/B09_PARAMETERS.json` avec un **écart maximal de 0,0** sur les deux contrats (vérifié dans le moteur avant toute comparaison).
2. **Empreintes des entrées** : les sept livrables 18-B ont été revérifiés par SHA-256 contre `PHASE18B_SHA256_MANIFEST.json` avant exécution (7/7 conformes) ; les artefacts 17-B/17-E sont lus sans modification.
3. **Déterminisme** : OLS par `numpy.linalg.lstsq` (rcond=None), aucune régularisation, aucune graine aléatoire, aucune imputation ; la population commune est une restriction complete-case comptabilisée événement par événement (`PHASE18C_COHORT_RECONCILIATION.csv` : 15/3/6 exclus par segment et par contrat).
4. **Traçabilité** : prédictions par événement et par architecture dans `PHASE18C_EVENT_PREDICTIONS.parquet` ; coefficients complets dans `PHASE18C_COEFFICIENTS.csv` ; registre des modèles et VIF dans `PHASE18C_MODEL_REGISTRY.json`.
