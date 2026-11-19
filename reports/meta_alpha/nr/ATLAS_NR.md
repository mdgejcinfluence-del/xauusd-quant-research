# ATLAS_NR — Phase 8 (descriptif, 0 essai, IS_NR 2020-2023 daily GC)

## M1 semaine (vol et |ret| medians en bp, volume median)
|   dow |   vol_med |   absret_med |   volume_med |   n |
|------:|----------:|-------------:|-------------:|----:|
|     0 |     109.7 |         52.2 |       164259 | 185 |
|     1 |     107.5 |         56.5 |       180436 | 207 |
|     2 |      85.5 |         45.9 |       182302 | 208 |
|     3 |     112.3 |         57   |       184746 | 206 |
|     4 |     111.9 |         54.6 |       176904 | 201 |

## M2 FOMC (amplitudes medianes |ret| en bp)
{False: {'absret_med_bp': 52.80529613880702, 'n': 1007}}

## M5 couts
C1_NR mesure (S2, snapshot): ~1.35 bp (spread min inter-profils 50,4 cents a 3 725 $). C1_BG challenge: 4.7 bp. Le regime actuel divise le spread en bp par ~2,5 vs l ancien corpus - mesure, pas importe.

## M6 crible
| regime   |   horizon_j |   n |   rho |   sigma_bp |   effet_bp |   MDE_bp |   seuil_bp | SURVIVANTE   |
|:---------|------------:|----:|------:|-----------:|-----------:|---------:|-----------:|:-------------|
| calme    |           1 | 329 |  0.03 |      69.95 |       1.9  |    10.8  |      10.8  | False        |
| calme    |           5 | 329 |  0.07 |      69.95 |       5.06 |    24.14 |      24.14 | False        |
| moyen    |           1 | 329 | -0.01 |      96.62 |       0.92 |    14.91 |      14.91 | False        |
| moyen    |           5 | 329 |  0    |      96.62 |       0.4  |    33.35 |      33.35 | False        |
| nerveux  |           1 | 329 | -0.04 |     140.34 |       6.05 |    21.66 |      21.66 | False        |
| nerveux  |           5 | 329 | -0    |     140.34 |       0.25 |    48.44 |      48.44 | False        |

## Absences consignees
- M3 macro NR: aucune source collectee (pas de cle FRED) - non fabrique.
- Intraday IS_NR: horaire Yahoo 2024+ uniquement; Dukascopy S3 QUALIFIE (18 478 ticks/h decompresses), backfill mensuel 2020-2023 = programme cron a venir, pas encore de matiere.