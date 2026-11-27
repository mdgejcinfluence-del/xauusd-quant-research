# BACKTEST-2026-001 — VALIDATION

- **Look-ahead** : moteurs gelés importés sans modification (hashes dans
  `FROZEN_ENGINE_CONFIGS.json`, vérifiés par test automatisé) ; états
  calculés tick par tick sur le passé.
- **Coûts comptés une fois** : spread via Bid/Ask à l'exécution, plus le
  coût CENTRAL de 1,2 bp déjà inclus dans la convention moteur S0 ;
  scénarios S1–S3 additifs documentés, jamais mélangés.
- **Transactions fantômes** : paniers ouverts en fin de segment et non
  clôturés exclus des résultats (aucune clôture inventée) — cause du
  « septembre à zéro clôture ».
- **Duplication** : 0 doublon de timestamp sur les segments audités
  (CI_PARTITION_AUDIT.csv, DATA_COVERAGE_2026.csv).
- **Reproductibilité** : novembre local reproduit exactement seq455
  (V1 : 379 paniers, −0,432) et seq459 (V2 : 230, −0,930) ; partitions
  CI VERIFIED (tailles et lignes conformes à l'inventaire certifié).
- **Cohérence mensuel/global** : la somme des mois égale le total par
  moteur (vérifiée par test).
- **Anomalies documentées** : octobre absent ; janvier à partir du 12 ;
  trou des 17–19 juillet ; septembre sans clôture ; backfill Kaggle
  non certifié non intégré.
- Tests : `ci_tools/test_backtest2026_full.py` (résultat au commit).
