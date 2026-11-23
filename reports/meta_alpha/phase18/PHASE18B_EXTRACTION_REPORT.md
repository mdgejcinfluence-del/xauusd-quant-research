# PHASE 18-B — RAPPORT D'EXTRACTION

Extraction exécutée en CI (run final `45125975580` entièrement vert, exit 0 ; incident du run `45125470359` — `scipy` absent au job d'analyse pour les corrélations de Spearman — corrigé par un calcul par rangs sans dépendance, journal conservé dans `PHASE18B_LOG.txt` du run concerné et dans l'historique Git). Sources : partitions tick IS 2010–2020 (lots Kaggle historiques, holdout jamais accédé) pour les trois variables de microstructure ; barres M1 committées `P13B_BARS_*` pour les trois variables de texture. Formules strictement celles de `PHASE18A_CANDIDATE_VARIABLES.csv` ; conventions d'implémentation documentées dans le moteur committé (fenêtres de clôtures M1 : 30 clôtures pour RV, 61 clôtures couvrant 60 intervalles pour efficience et retournements ; écarts de cotation entre observations consécutives dans la fenêtre, sans projection future). Cohortes, identifiants et segments repris tels quels des artefacts 17-B (1 946 événements).

## Verdicts par variable
| Variable | Verdict | Motif |
|---|---|---|
| QUOTE_UPDATE_RATE_5M | `EXTRACTED_VALID` | couverture 100 %, 0 manquant |
| MAX_QUOTE_GAP_15M | `EXTRACTED_VALID` | couverture 100 %, convention de bord sans tick futur |
| SPREAD_TREND_5M | `EXTRACTED_WITH_LIMITATIONS` | 1 événement sans sous-fenêtre de spread (NON_VALIDABLE documenté) |
| RV_MID_30M | `EXTRACTED_WITH_LIMITATIONS` | 13 fenêtres de 30 clôtures incomplètes |
| PATH_EFFICIENCY_60M | `EXTRACTED_WITH_LIMITATIONS` | 25 fenêtres de 61 clôtures incomplètes |
| REVERSAL_COUNT_60M | `EXTRACTED_WITH_LIMITATIONS` | même fenêtre 60 min |

## Verdict global : `SIX_FEATURES_EXTRACTED_VALID`
Les six candidats sont extraits, traçables (`N_QUOTES_*`, `N_BARS_*`, `source_batch` dans le Parquet), temporellement causaux et empiriquement distincts du dictionnaire gelé ; les limitations sont des absences `NON_VALIDABLE` préenregistrées (≤ 1,4 % par variable), pas des échecs d'extraction. **Aucun entraînement, aucun test économique, aucune sélection de variables n'a été effectué.** Toute utilisation future exige une décision distincte ; les résultats resteront exploratoires et post-hoc sur population déjà étudiée.
