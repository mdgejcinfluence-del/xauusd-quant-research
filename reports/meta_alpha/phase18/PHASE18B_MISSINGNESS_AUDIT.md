# PHASE 18-B — AUDIT DES VALEURS MANQUANTES

Effectifs attendus (artefacts 17-B) : 1 143 / 360 / 443 événements ; retrouvés dans le Parquet : 1 143 / 360 / 443, 0 doublon, 0 événement supprimé silencieusement.

| Variable | Couverture min–max par segment | Manquants | Cause documentée |
|---|---|---|---|
| QUOTE_UPDATE_RATE_5M | 100 % | 0 | — |
| MAX_QUOTE_GAP_15M | 100 % | 0 | — |
| SPREAD_TREND_5M | 99,9–100 % | 1 | sous-fenêtre [t−60s, t] ou [t−5min, t−60s] sans cotation (apprentissage) |
| RV_MID_30M | 99,2–99,8 % | 13 au total | fenêtre de 30 clôtures M1 consécutives incomplète |
| PATH_EFFICIENCY_60M | 98,6–99,2 % | 25 au total | fenêtre de 61 clôtures consécutives incomplète |
| REVERSAL_COUNT_60M | 98,6–99,2 % | 25 au total | même fenêtre 60 min |

Toutes les absences correspondent au traitement `NON_VALIDABLE` préenregistré en 18-A (fenêtre vide ou incomplète, jamais imputée). 0 valeur non finie, 0 erreur d'unité détectée (contrôles : taux en cotations/min ≥ 0 ; écarts en secondes ≥ 0 ; efficience dans [0,1] par construction ; comptages entiers ≥ 0). Détail par segment : `PHASE18B_FEATURE_COVERAGE.csv`.
