# ATLAS STRUCTUREL XAUUSD — Phase 7 Axe 1 (descriptif, 0 essai)

Aucune statistique de gain directionnel. Sources: serie horaire certifiee du corpus tick, DAILY_VOL, F3 daily, panel 43, pack exogene IS. Perimetre IS strict.

## M1 — Calendrier intrajournalier (vol mediane en bp/h, spread median bp, par heure UTC; semaine complete dans ATLAS_DATA.json)
|   heure |   vol |   spread |   spread_p95 |   ticks |   sauts |
|--------:|------:|---------:|-------------:|--------:|--------:|
|       0 | 11.08 |     2.51 |         4.84 | 3409.18 |    0.01 |
|       1 | 12.84 |     2.4  |         4.89 | 4592.98 |    0.01 |
|       2 | 10.28 |     2.35 |         4.59 | 3422.2  |    0.01 |
|       3 |  8.83 |     2.34 |         4.68 | 2879.51 |    0    |
|       4 |  8.33 |     2.34 |         4.36 | 2676.69 |    0    |
|       5 |  9.97 |     2.3  |         4.05 | 3455.97 |    0.01 |
|       6 | 12.99 |     2.29 |         4.04 | 4636.58 |    0.01 |
|       7 | 14.33 |     2.22 |         4.21 | 5518.36 |    0.01 |
|       8 | 14.01 |     2.19 |         4.15 | 5502.65 |    0.01 |
|       9 | 13.1  |     2.2  |         3.35 | 4969.72 |    0.01 |
|      10 | 12.51 |     2.19 |         3.34 | 4624.29 |    0.01 |
|      11 | 13.24 |     2.2  |         3.29 | 4949.2  |    0.01 |
|      12 | 18.94 |     2.21 |         4.04 | 7239.94 |    0.04 |
|      13 | 22.64 |     2.2  |         4.19 | 9134.83 |    0.06 |
|      14 | 22.53 |     2.19 |         4.01 | 9356.23 |    0.07 |
|      15 | 19.66 |     2.18 |         3.99 | 8277.05 |    0.05 |
|      16 | 16.29 |     2.19 |         4.21 | 6612.49 |    0.02 |
|      17 | 15.01 |     2.26 |         4.57 | 5518.35 |    0.02 |
|      18 | 13.13 |     2.3  |         4.51 | 4911.45 |    0.02 |
|      19 | 11.48 |     2.31 |         4.87 | 4268.27 |    0.02 |
|      20 |  9.69 |     2.55 |         4.86 | 2564.82 |    0    |
|      21 |  6.77 |     3.41 |         7.62 |  979.26 |    0    |
|      22 |  8.21 |     3.32 |         6.52 | 1453.51 |    0.01 |
|      23 |  8.7  |     2.97 |         5.01 | 1958.45 |    0.01 |

## M5 — Carte des couts (fenetre x regime; plancher de capturabilite = 2 x max(spread, C1_BG 4,7))
| fenetre   | regime   |   spread_med |   spread_p95 |   vol_med |    n |   capturable_min_bp (2xC) |
|:----------|:---------|-------------:|-------------:|----------:|-----:|--------------------------:|
| 00-05     | calme    |         2.27 |         3.66 |      7.42 | 5007 |                       9.4 |
| 00-05     | moyen    |         2.34 |         3.14 |     10.22 | 5232 |                       9.4 |
| 00-05     | nerveux  |         2.57 |         5.02 |     15.81 | 5187 |                       9.4 |
| 06-11     | calme    |         2.16 |         3.12 |      9.89 | 5010 |                       9.4 |
| 06-11     | moyen    |         2.2  |         2.9  |     13.26 | 5232 |                       9.4 |
| 06-11     | nerveux  |         2.32 |         4.37 |     21.13 | 5190 |                       9.4 |
| 12-16     | calme    |         2.16 |         3.22 |     14.13 | 4175 |                       9.4 |
| 12-16     | moyen    |         2.16 |         2.84 |     20.19 | 4360 |                       9.4 |
| 12-16     | nerveux  |         2.3  |         4.36 |     30.72 | 4325 |                       9.4 |
| 17-21     | calme    |         2.36 |         4.14 |      8.46 | 3743 |                       9.4 |
| 17-21     | moyen    |         2.37 |         4.03 |     11.9  | 3911 |                       9.4 |
| 17-21     | nerveux  |         2.69 |         5.16 |     15.89 | 4015 |                       9.4 |
| 22-23     | calme    |         2.85 |         5.13 |      7.55 | 2080 |                       9.4 |
| 22-23     | moyen    |         2.98 |         5.29 |      8.76 | 1279 |                       9.4 |
| 22-23     | nerveux  |         3.6  |         6.42 |     12.71 | 1279 |                       9.4 |

## M2 — Anatomie des evenements (amplitudes medianes, jamais de pnl signe)
| type   |   n |   spread_entree_med |   abs_mouv_5min_bp |   abs_ret_15 |   abs_ret_60 |   abs_ret_240 | lecture_vol                                                   |
|:-------|----:|--------------------:|-------------------:|-------------:|-------------:|--------------:|:--------------------------------------------------------------|
| CPI    | 136 |                2.28 |               6.75 |         8.27 |        11.43 |         23.82 | >240 min (pas de retour sous le niveau 15min dans la fenetre) |
| FOMC   |  81 |                2.64 |              11.41 |        14.28 |        29.27 |         41.93 | >240 min (pas de retour sous le niveau 15min dans la fenetre) |
| NFP    | 129 |                2.51 |              12.26 |        15.05 |        28.44 |         34.77 | >240 min (pas de retour sous le niveau 15min dans la fenetre) |

## M3 — Etats macro
```json
{
 "DFII10": {
  "mediane": 0.47,
  "q10": -0.36399999999999977,
  "q90": 1.03,
  "autocorr_1j": 0.9972388210815611,
  "autocorr_21j": 0.9494897649208262,
  "corr_vol_realisee": -0.14709682245099856,
  "corr_intensite_sauts": -0.031585401853284276
 },
 "pente": {
  "mediane": 1.4500000000000002,
  "q10": 0.23999999999999977,
  "q90": 2.5799999999999996,
  "autocorr_1j": 0.9992290612287971,
  "autocorr_21j": 0.9870095339442548,
  "corr_vol_realisee": 0.1560250530514273,
  "corr_intensite_sauts": 0.13219436452761252
 },
 "GVZ": {
  "mediane": 16.48,
  "q10": 11.23,
  "q90": 23.208000000000002,
  "autocorr_1j": 0.9810839196471958,
  "autocorr_21j": 0.8120176652000258,
  "corr_vol_realisee": 0.29898287291439835,
  "corr_intensite_sauts": 0.31247100876056894
 }
}
```

## M4 — Structure croisee panel
```json
{
 "colonnes_or_detectees": [
  "GC"
 ],
 "top_corr": {
  "PL": 0.5928018686478119,
  "SI": 0.5753445662048134,
  "PA": 0.3825640847333431,
  "EC": 0.3063840257527466,
  "AD": 0.2485359339136606,
  "BP": 0.2259462007241561,
  "CL": 0.21151127451433432,
  "BO": 0.17240133673619223
 },
 "stabilite_corr (corr des corr moitie1/moitie2)": 0.8399795178183046
}
```

## M6 — Carte de chasse: cellules survivantes
**0 cellule(s) survivante(s) sur 30.**
| fenetre   | regime   | horizon   |    n |   rho1 |   sigma_bp |   effet_descriptif_bp |   MDE_bp |   plancher_cout_bp |   seuil_requis_bp | SURVIVANTE   |
|:----------|:---------|:----------|-----:|-------:|-----------:|----------------------:|---------:|-------------------:|------------------:|:-------------|
| 12-16     | nerveux  | 4h        | 4325 |   0.04 |      67.69 |                  2.83 |     5.76 |                9.4 |               9.4 | False        |
| 06-11     | nerveux  | 4h        | 5190 |  -0.04 |      53.48 |                  1.94 |     4.16 |                9.4 |               9.4 | False        |
| 00-05     | moyen    | 4h        | 5232 |   0.07 |      25.85 |                  1.71 |     2    |                9.4 |               9.4 | False        |
| 00-05     | nerveux  | 1h        | 5187 |   0.08 |      18.64 |                  1.43 |     0.72 |                9.4 |               9.4 | False        |
| 22-23     | moyen    | 4h        | 1279 |   0.05 |      26.11 |                  1.4  |     4.09 |                9.4 |               9.4 | False        |
| 12-16     | moyen    | 4h        | 4360 |  -0.03 |      45.55 |                  1.39 |     3.86 |                9.4 |               9.4 | False        |
| 22-23     | nerveux  | 1h        | 1279 |  -0.08 |      15.85 |                  1.34 |     1.24 |                9.4 |               9.4 | False        |
| 12-16     | nerveux  | 1h        | 4325 |   0.03 |      35.34 |                  1.13 |     1.5  |                9.4 |               9.4 | False        |
| 00-05     | calme    | 4h        | 5007 |   0.05 |      21.54 |                  1.04 |     1.7  |                9.4 |               9.4 | False        |
| 22-23     | nerveux  | 4h        | 1279 |   0.03 |      34.68 |                  0.97 |     5.43 |                9.4 |               9.4 | False        |

Lecture: l effet descriptif (|autocorrelation| x sigma) doit depasser max(MDE R3, plancher de cout ECR>=2). En dessous: cellule morte avant test, sans consommer d essai.