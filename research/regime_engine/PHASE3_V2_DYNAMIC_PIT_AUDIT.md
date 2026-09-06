# PHASE 3 V2 — STEP 3.5R : DYNAMIC PIT AUDIT (OPTIMIZED, TARGETED)

**Date :** 2026-09-06 (UTC) · **Type :** preuve PAST-ONLY par troncature dynamique ciblée.
**Méthode :** l'ancien protocole intégral n'a PAS été relancé. Structure du moteur analysée
(`feature_engine_v2.py` = helpers purs `rolling_arr/pair_prefixes/acf_vec/prefix_mask/
prefix_cum/roll_sums4` + expressions par indice) ; `scripts/dynamic_pit_audit_v2.py` reconstruit
uniquement les tableaux d'entrée du moteur sur le préfixe tronqué (builder FROZEN `01_build_layers.py`
exécuté non modifié) et évalue les 25 features **seulement à la ligne-sonde `t`**, avec les mêmes
fenêtres / MIN_OBS / estimateurs et le même ordre arithmétique (préfixes de parité B2 inclus).
Aucune feature ni formule modifiée ; aucune agrégation / clustering / K / HMM-GMM / backtest.

## Sondes
21 sondes — 3 par période : 2010, 2012, 2013, 2016, 2020, 2024, 2026.
Chaque sonde : barre M3 réelle, profondeur ≥ 14 400 + 5 000 positions (loin du warm-up),
bucket sans minute manquante ni rupture interne, jointures M3 contiguës avant/après,
25 features finies dans le dataset de référence.

## Modes par sonde (5)
| mode | cut_min | rôle |
|---|---|---|
| ref  | — | contrôle d'identité du harnais vs parquet committé (doit être 0 mismatch) |
| exact | Ts | données strictement limitées à `t` |
| o1 | Ts+3 | +1 observation M3 |
| o10 | Ts+30 | +10 observations M3 |
| o100 | Ts+300 | +100 observations M3 |

## Résultats
```
Comparaisons PIT (exact/o1/o10/o100) = 2100
  PASS = 2004 | FAIL = 96 | NA structurels = 0
Contrôle d'identité (mode ref) = 525 (mismatch = 0)
Durée d'exécution = 98.5 s
```

### PASS/FAIL par mode

| mode | PASS | FAIL |
|---|---|---|
| exact | 493 | 32 |
| o1 | 493 | 32 |
| o10 | 493 | 32 |
| o100 | 525 | 0 |
| ref | 525 | 0 |

### Détail par sonde

| sonde | Ts%60 | H1 bar close at t | modes en échec |
|---|---|---|---|
| 2010-21139800 | 2 | fermé=False · contigu=True | exact, o1, o10 |
| 2010-21315480 | 2 | fermé=False · contigu=True | exact, o1, o10 |
| 2010-21492600 | 2 | fermé=False · contigu=True | exact, o1, o10 |
| 2012-22151472 | 14 | fermé=False · contigu=False | — |
| 2012-22324920 | 2 | fermé=False · contigu=True | exact, o1, o10 |
| 2012-22500600 | 2 | fermé=False · contigu=True | exact, o1, o10 |
| 2013-22678563 | 5 | fermé=False · contigu=False | — |
| 2013-22850520 | 2 | fermé=False · contigu=True | exact, o1, o10 |
| 2013-23028363 | 5 | fermé=False · contigu=False | — |
| 2016-24254520 | 2 | fermé=False · contigu=True | exact, o1, o10 |
| 2016-24429483 | 5 | fermé=False · contigu=False | — |
| 2016-24604440 | 2 | fermé=False · contigu=True | exact, o1, o10 |
| 2020-26358360 | 2 | fermé=False · contigu=True | exact, o1, o10 |
| 2020-26532600 | 2 | fermé=False · contigu=True | exact, o1, o10 |
| 2020-26708280 | 2 | fermé=False · contigu=True | exact, o1, o10 |
| 2024-28462200 | 2 | fermé=False · contigu=True | exact, o1, o10 |
| 2024-28636440 | 2 | fermé=False · contigu=True | exact, o1, o10 |
| 2024-28814289 | 11 | fermé=False · contigu=False | — |
| 2026-29514840 | 2 | fermé=False · contigu=True | exact, o1, o10 |
| 2026-29643000 | 2 | fermé=False · contigu=True | exact, o1, o10 |
| 2026-29775480 | 2 | fermé=False · contigu=True | exact, o1, o10 |

> **Remarque de couverture :** les sondes dont la barre H1 `h(t)` (bucket
> contenant `T+2`) est contiguë après `t` exposent pleinement la dépendance
> (16/21 sondes échouent) ; les 5 sondes "PASS" ont un `contig_next=0` à cette
> barre H1, donc `rH` y est NaN des deux côtés et la fenêtre H1 ne voit pas la
> différence — le test y est structurellement aveugle, il ne prouve PAS un
> PASS. Le verdict global reste donc défini par les 16 sondes exposées.
> 
### Features en échec

| feature | famille | FAIL | max abs_diff |
|---|---|---|---|
| h1_acf1_month | B | 48 | 0.00584288 |
| h1_vol_ratio_day_month | A | 48 | 0.055104 |

## Conclusion
**DYNAMIC_PIT = FAIL**

Règle appliquée : si FAIL -> STOP, aucune correction. Liste complète des lignes dans
`PHASE3_V2_DYNAMIC_PIT_AUDIT.csv` (timestamp, feature, value_reference, value_truncated,
abs_diff, exact_zero, verdict).
