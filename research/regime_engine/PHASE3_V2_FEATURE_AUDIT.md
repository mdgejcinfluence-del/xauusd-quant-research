# PHASE 3 V2 — STEP 3.4 : FEATURE BEHAVIORAL AUDIT (DESCRIPTIF)

**Date :** 2026-09-06 (UTC) · **Type :** audit descriptif — aucune modification de feature,
aucune recalibration, aucune suppression, aucun clustering, aucun K, aucun HMM/GMM,
aucun backtest, aucun score de performance.
**Références :** DATA CONTRACT V2 (FROZEN) · FEATURE SPEC V2 (FROZEN) ·
`features_v2_meta.json` · `XAUUSD_FEATURES_V2.parquet` · `feature_engine_v2.py`.
**Méthode :** calculs sur l'ensemble des 1 963 826 lignes (couverture/distribution/
dégénérescence/stabilité/extrêmes) ; corrélation Spearman sur échantillon stratifié
5 000 barres/année (2010–2026, n = 85 000) ; quantiles par interpolation linéaire ;
variance/std ddof=1. Seuils de jugement annoncés ex ante : redondance forte |ρ| ≥ 0.90 ;
dominance extrémale (part du top-1 % de |déviation à la médiane|) > 0.50 ; CV des
médianes annuelles > 0.15 ; rupture pré/post 2013 > 1 écart interquartile.

## 1. SYNTHÈSE DES VERDICTS

```
ACCEPT            = 18
FLAG FOR REVIEW   = 7
REJECT            = 0
AUCUNE FEATURE SUPPRIMÉE — AUCUNE OBSERVATION MODIFIÉE
```

| Feature | Verdict | Motif principal |
|---|---|---|
| m3_vol_ratio_day_month | ACCEPT | stable, borné, aucune anomalie |
| m3_m1_noise_ratio | ACCEPT | stable (CV 0.010) ; shift 2013 +0.31 IQR (documenté) |
| h1_vol_ratio_day_month | ACCEPT | stable (CV 0.033) ; valeurs H1 à 98 051 niveaux distincts |
| m3_acf1_day | ACCEPT | distribution saine ; CV médianes 0.62 (mesure près de zéro → note d'interprétation, non une anomalie) |
| m3_vr2_month | ACCEPT | borné [0.70, 1.12] ; rupture 2013 −0.82 IQR (documentée) |
| m3_scf_day | ACCEPT | très stable (CV 0.008) ; 6 800 valeurs distinctes |
| m3_run_month | ACCEPT | très stable (CV 0.010) ; [1.78, 2.01] barres |
| m3_dir_month | **FLAG FOR REVIEW** | médiane ≈ 0 → CV annuel 13.4 (artefact d'échelle) ; signe interprétation fragile |
| h1_acf1_month | ACCEPT | bruit autour de 0 (attendu) ; CV 1.30 (médiane ≈ 0 → note) |
| m3_range_sigma_day | **FLAG FOR REVIEW** | **redondance ρ = 0.999 avec m3_tr_sigma_day** (par ailleurs sain) |
| m3_tr_sigma_day | **FLAG FOR REVIEW** | idem ; TR ≈ range à l'échelle M3 → quasi-duplicat |
| m3_tr_expansion_day | **FLAG FOR REVIEW** | distribution fortement décalée négativement (médiane −174.5 bps ; p01 −669.6 ; min −1131.9) — interprétabilité à revoir |
| m3_body_range_day | ACCEPT | cohérent ; rupture 2013 +0.52 IQR (documentée) |
| m3_up_wick_day | ACCEPT | cohérent ; rupture 2013 +0.61 IQR (documentée) |
| m3_low_wick_day | ACCEPT | rupture 2013 **−1.40 IQR (la plus forte)** — convention 2013, non corrigée (L4) |
| m3_close_pos_day | ACCEPT | rupture 2013 −1.05 IQR (documentée) |
| m3_body_dir_day | **FLAG FOR REVIEW** | médiane = 0.000 ; 15.2 % de valeurs ≈ 0 (dojis) ; CV 2.01 (médiane ≈ 0) — interprétation fragile |
| m3_ext_rate_month | ACCEPT | 1.56 % ± 0.13 pt ; rupture 2013 −0.58 IQR (documentée) |
| m3_kurtosis_month | **FLAG FOR REVIEW** | moyenne 32.1 vs médiane 19.1 ; p99 403.8 ; max 968.6 ; CV 0.44 — sensibilité extrême intrinsèque |
| m3_skew_month | **FLAG FOR REVIEW** | p01 −9.07 / p99 2.90 / min −16.16 ; max/p99 5.57 ; CV 3.68 (médiane ≈ 0) |
| m1_ext_rate_day | ACCEPT | stable (CV 0.063) ; valeurs discrètes (365 niveaux) par construction |
| m3_ext_sign_month | ACCEPT | stable (CV 0.051) ; dérive 2020-2026 vers < 0.48 (documentée) |
| m3_storm_clust_month | ACCEPT | comportement riche (0.17–0.52) ; évolution 2020-2024 documentée |
| m3_storm_p90_run_month | ACCEPT | discret par construction (11 niveaux ; P90 = 2.0 sur 94 % du temps) — attendu |
| m3_ext_spacing_month | ACCEPT | 3.81 % de NaN = règle « ≥ 30 extrêmes » (spec), aucun trou anormal |

## 2. COUVERTURE

- `n_total` = 1 963 826 pour toutes les features (= lignes de la grille M3 validée).
- Toutes les features ont une **première valeur valide entre 2010-01-04T04:24Z et
  2010-02-12T11:57Z** (warm-up positionnel : 480 ou 14 400 positions, jamais rempli)
  et une **dernière valeur valide à 2026-08-30T23:57Z** (dernière barre M3).
- NaN ≤ 14 404 (0.73 %) pour 24 features (warm-up + fenêtres < MIN_OBS) ;
  `m3_ext_spacing_month` : 74 787 (3.81 %) — exclusivement la règle spec
  « < 30 extrêmes classables → NaN ».
- Aucune valeur infinie (`inf_count = 0` partout).

## 3. DISTRIBUTION & DÉGÉNÉRESCENCE

- **Aucune feature constante ou quasi-constante** : variance > 0 ; `distinct_count`
  ≥ 11 (discret p90_run) et typiquement ≥ 50 000 ; `dominant_fraction` ≤ 0.0017
  pour les features continues ; les fractions dominantes > 1 % sont des artefacts
  de discrétisation attendus (`m3_storm_p90_run_month` 0.72, `m3_body_dir_day` 0.152
  (dojis), `m3_ext_rate_month` 0.040, `m3_ext_sign_month` 0.021, `m3_scf_day` 0.021)
  — structurés par construction, non dégénérés.
- NaN proportion : 0.02 %–0.73 % (sauf spacing 3.81 %) : conforme aux règles de
  disponibilité de la spec (aucun backfill, aucun forward-fill).

## 4. STABILITÉ TEMPORELLE (par année, 2010–2026)

Médianes annuelles complètes en annexe A (fichier CSV colonnes `year_*` disponibles
via `PHASE3_V2_FEATURE_AUDIT.csv` + table ci-dessous pour les signaux).

**Ruptures manifestes identifiées (aucune correction — contrat §5) :**

1. **Convention ~2013 (L4, documentée, non corrigée)** — shift médiane pré-2013
   (2010-2012) → post-2013 (2013-2025), en unités d'IQR plein échantillon :
   `m3_low_wick_day −1.40` · `m3_close_pos_day −1.05` · `m3_vr2_month −0.82` ·
   `m3_ext_rate_month −0.58` · `m3_body_range_day +0.52` · `m3_up_wick_day +0.61` ·
   `m3_kurtosis_month +0.41` · `m3_m1_noise_ratio +0.31`. Cluster cohérent (structure
   des bougies + persistance + queues) : changement de convention déjà documenté en
   Phase-2B ; **comportement du marché, pas un artefact — conservé tel quel.**
2. **Anomalie structurelle 2010** (familles C/D) : `m3_body_range_day` 0.385 (vs
   0.49+ ensuite), `m3_low_wick_day` 0.360 (vs ~0.20), `m3_close_pos_day` 0.609
   (vs ~0.50), `m3_range_sigma_day` 1.243 (vs ~0.97-1.2). Le premier millésime de
   l'échantillon diffère (début de la fenêtre de données, convention de début de
   série) — signalé, non corrigé, non supprimé.
3. **Changement de régime de clustering 2020-2024** (familles E/F) :
   `m3_storm_clust_month` médiane 0.28–0.34 (2010-2019) → **0.38–0.43 (2020-2024,
   pic 0.428 en 2024)** ; `m3_ext_spacing_month` 17.5 (2017) → **8.0 (2024)** ;
   `m3_ext_sign_month` 0.510 (2010) → **0.426 (2025)** ; `m3_kurtosis_month`
   oscillant 8.7 (2025) – 38.5 (2014). Évolution comportementale réelle, documentée.
4. **2026 (partiel, sanity only)** : taux extrêmes 0.0150, clustering 0.359,
   range/σ 1.198 (haut de gamme historique), kurtosis 17.9 — aucune anomalie de
   calcul ; année partielle, jamais un critère de sélection (L5).

## 5. DÉPENDANCE ENTRE FEATURES (Spearman, n = 85 000 stratifié)

- **Une seule paire très fortement redondante (|ρ| ≥ 0.90) :**
  `m3_range_sigma_day ↔ m3_tr_sigma_day` **ρ = +0.999** — quasi-duplicat (TR ≈ range
  à l'échelle M3 : les écarts inter-barres extrêmes sont rares) → **FLAG, non supprimé**.
- Sous le seuil, à titre informatif : `m3_storm_clust_month ↔ m3_ext_spacing_month`
  ρ = **−0.88** (inverse attendu : plus d'espacement = moins de clustering intra-5).
- Aucune autre paire |ρ| ≥ 0.85. La matrice (25 × 25) est jointe à l'annexe B.

## 6. STABILITÉ PAR FAMILLE

| Famille | n | |ρ| mean (intra) | Lecture |
|---|---|---|---|---|
| A Volatilité relative | 3 | 0.42 (0.28–0.66) | **Cohérente** ; ratios stables (CV ≤ 0.033) ; signaux complémentaires M3/M1/H1 |
| B Persistance directionnelle | 6 | 0.08 (0.005–0.39) | **Cohérente par construction** (estimateurs/fenêtres distincts) ; anomalies : `m3_dir_month` (méd. ≈ 0), `h1_acf1_month` (bruit autour de 0) |
| C Amplitude | 3 | 0.38 (0.07–0.999) | **Anomalie : paire 0.999 (C1/C2) + `m3_tr_expansion_day` décalée négativement** ; sinon stable |
| D Structure bougies | 5 | 0.29 (0.02–0.72) | **Cohérente** ; ruptures 2010/2013 documentées ; `m3_body_dir_day` (méd. ≈ 0) à interpréter avec soin |
| E Queue / extrêmes | 5 | 0.14 (0.001–0.45) | **Cohérente** (aspects distincts) ; `m3_kurtosis_month`/`m3_skew_month` sensibles aux queues par nature |
| F Clustering temporel | 3 | 0.60 (0.41–0.88) | **Cohérente** ; le couple clust/spacing (−0.88) est structurel (mêmes événements) |

## 7. EXTRÊMES

- `extreme_dominance` (part du top-1 % de |déviation à la médiane|) : **max 0.245**
  (`m3_kurtosis_month`), puis 0.156 (`m3_skew_month`) — **aucune feature dominée par
  quelques observations** (seuil d'alerte 0.50 non atteint).
- `max/p99` : max 5.57 (`m3_skew_month`), 4.89 (`m3_tr_expansion_day`), 3.44
  (`m3_acf1_day`) — queue lourde modérée, cohérente avec une distribution financière.
- **Aucune observation supprimée, aucun winsorisation** (EXTREME_POLICY = RETAINED).

## 8. PIT — CONTRÔLE STRUCTUREL

- **Schéma :** `ts_min, bar_id` + exactement les 25 noms de la SPEC (ordre identique),
  aucun volume, aucune colonne étrangère ; `features_v2_meta.json` = 25 entrées
  cohérentes (famille, fenêtre, MIN_OBS, unités, statut OK, n_valid/n_nan).
- **Constantes moteur == SPEC :** 480/120 · 14 400/3 600 · 1 440/360 · 24/12 · 336/84 ·
  120 · 30 · seuil extrême 3.0 (vérifié dans `feature_engine_v2.py`).
- **Scan statique :** aucun motif interdit (`shift(-`, `center=True`, `diff(-`, `t+k`).
- **Déterminisme :** re-exécution complète du moteur → **parquet byte-identique**
  (SHA-256 `5cebe082d5f710a0130369c3620ed463652e8b626edd4c68f498b3d25c10c955` avant
  ET après) — les colonnes proviennent donc bien du moteur V2 gelé.
- **Alignements :** `ts_min`/`bar_id` identiques à la grille M3 (1 963 826 × 2),
  `endM1(t)` = dernière minute M1 ≤ T+2 (bucket M3 fermé), `h(t)` = bucket H1 fermé.
- **Warm-up :** 0 valeur finie avant la position de pleine fenêtre (vérifié pour
  les col. jour et mois).
- L'audit PIT **dynamique** (troncature complète, sondes multiples) est **explicitement
  différé** à un step séparé, conformément à la consigne.

## 9. GAPS — AUCUNE CONTINUITÉ ARTIFICIELLE

- **Aucune ligne synthétique :** le dataset ne contient que les barres M3 réelles
  (1 963 826 = grille) ; aucune interpolation, aucun ré-échantillonnage.
- Retours `r_R` = **NaN aux 13 452 pas M3 non contigus** (contig_next = 0) : les
  statistiques de retours (σ, ACF, SCF, VR, skew/kurt, extrêmes) opèrent **uniquement
  sur le sous-ensemble propre** — la paire de rendements traversant une fermeture
  n'est **jamais** utilisée.
- Vérification ciblée : aux barres de gap, `m3_acf1_day`/`m3_scf_day` restent finies
  car seules les paires invalides sont exclues (les ~477 paires propres du window
  suffisent) — **c'est une exclusion, pas une fabrication de continuité** ; aucun
  NaN n'est « réparé », aucun valeur n'est propagée à travers un gap.
- Les barres « stub » de rollover (Famille D/C) sont des barres réelles incluses
  par la spec (propriété de marché documentée) — pas une continuité synthétique.
- Aucune feature ne voit son NaN réduit après un gap (NaN ne diminue jamais :
  vérification structurelle par construction des fenêtres positionnelles).

## 10. GATE

```
FEATURE_BEHAVIORAL_AUDIT = DONE (descriptive)
ACCEPT = 18 | FLAG_FOR_REVIEW = 7 | REJECT = 0
REMOVALS = 0 | WINSORIZATION = 0 | RE-CALIBRATION = 0
STRONG_REDUNDANCY = 1 (m3_range_sigma_day / m3_tr_sigma_day, rho=0.999)
DYNAMIC_PIT_AUDIT = DEFERRED (separate step, per instruction)
CLUSTERING / K / HMM-GMM / BACKTEST / PERFORMANCE = NONE
```

---

## ANNEXE A — MÉDIANES ANNUELLES (extrait ; tableau complet dans le CSV)

| Feature | 2010 | 2011 | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| m3_vol_ratio_day_month | 0.926 | 0.934 | 0.896 | 0.890 | 0.939 | 0.914 | 0.875 | 0.921 | 0.955 | 0.914 | 0.885 | 0.909 | 0.930 | 0.925 | 0.905 | 0.926 | 0.886 |
| m3_m1_noise_ratio | 1.005 | 0.987 | 0.999 | 1.015 | 1.019 | 1.028 | 1.012 | 1.021 | 1.027 | 1.023 | 1.026 | 1.015 | 1.015 | 1.013 | 1.011 | 1.018 | 1.022 |
| h1_vol_ratio_day_month | 0.892 | 0.926 | 0.838 | 0.821 | 0.876 | 0.870 | 0.857 | 0.902 | 0.907 | 0.888 | 0.873 | 0.885 | 0.892 | 0.889 | 0.877 | 0.943 | 0.880 |
| m3_acf1_day | 0.018 | −0.003 | −0.026 | −0.018 | −0.026 | −0.026 | −0.026 | −0.029 | −0.035 | −0.019 | −0.050 | −0.020 | −0.030 | −0.022 | −0.031 | −0.021 | −0.024 |
| m3_vr2_month | 1.037 | 1.010 | 0.998 | 1.006 | 0.982 | 0.978 | 0.979 | 0.968 | 0.981 | 0.991 | 0.959 | 0.985 | 0.978 | 0.987 | 0.979 | 0.979 | 0.990 |
| m3_scf_day | 0.516 | 0.508 | 0.514 | 0.518 | 0.514 | 0.520 | 0.514 | 0.518 | 0.516 | 0.510 | 0.518 | 0.511 | 0.510 | 0.511 | 0.507 | 0.510 | 0.513 |
| m3_run_month | 1.912 | 1.947 | 1.914 | 1.901 | 1.923 | 1.896 | 1.920 | 1.896 | 1.909 | 1.913 | 1.918 | 1.935 | 1.944 | 1.936 | 1.959 | 1.949 | 1.938 |
| m3_dir_month | 0.004 | 0.004 | −0.002 | −0.007 | −0.002 | −0.004 | −0.000 | −0.002 | −0.002 | 0.002 | 0.002 | −0.003 | −0.001 | −0.000 | 0.005 | 0.006 | −0.004 |
| h1_acf1_month | −0.017 | −0.018 | −0.008 | −0.002 | −0.004 | −0.013 | −0.000 | −0.013 | −0.003 | 0.010 | −0.033 | −0.016 | −0.028 | 0.013 | 0.005 | −0.030 | −0.041 |
| m3_range_sigma_day | 1.243 | 0.965 | 1.032 | 0.998 | 0.986 | 0.976 | 1.081 | 1.096 | 1.116 | 1.037 | 1.136 | 1.058 | 1.100 | 1.045 | 1.113 | 1.215 | 1.198 |
| m3_tr_sigma_day | 1.266 | 0.972 | 1.038 | 1.004 | 0.991 | 0.981 | 1.083 | 1.098 | 1.119 | 1.043 | 1.139 | 1.060 | 1.102 | 1.050 | 1.116 | 1.218 | 1.199 |
| m3_tr_expansion_day | −75 | −234 | −183 | −279 | −255 | −148 | −192 | −133 | −151 | −188 | −197 | −157 | −176 | −153 | −161 | −162 | −175 |
| m3_body_range_day | 0.385 | 0.537 | 0.494 | 0.496 | 0.505 | 0.500 | 0.492 | 0.486 | 0.509 | 0.503 | 0.482 | 0.488 | 0.488 | 0.500 | 0.492 | 0.471 | 0.470 |
| m3_up_wick_day | 0.181 | 0.168 | 0.206 | 0.200 | 0.189 | 0.199 | 0.208 | 0.212 | 0.193 | 0.198 | 0.209 | 0.202 | 0.211 | 0.201 | 0.205 | 0.212 | 0.215 |
| m3_low_wick_day | 0.360 | 0.179 | 0.202 | 0.201 | 0.193 | 0.194 | 0.201 | 0.207 | 0.192 | 0.193 | 0.211 | 0.211 | 0.206 | 0.202 | 0.207 | 0.224 | 0.226 |
| m3_close_pos_day | 0.609 | 0.515 | 0.498 | 0.498 | 0.498 | 0.495 | 0.498 | 0.498 | 0.497 | 0.500 | 0.509 | 0.507 | 0.497 | 0.500 | 0.507 | 0.517 | 0.507 |
| m3_body_dir_day | 0.003 | 0.011 | 0.000 | −0.001 | 0.000 | −0.002 | 0.000 | 0.000 | 0.000 | 0.000 | 0.003 | 0.000 | 0.000 | 0.000 | 0.010 | 0.015 | 0.002 |
| m3_ext_rate_month | 0.017 | 0.016 | 0.016 | 0.017 | 0.016 | 0.015 | 0.016 | 0.015 | 0.015 | 0.016 | 0.016 | 0.016 | 0.015 | 0.015 | 0.015 | 0.014 | 0.015 |
| m3_kurtosis_month | 10.5 | 10.0 | 21.6 | 30.8 | 38.5 | 30.1 | 27.1 | 32.0 | 11.4 | 21.5 | 10.2 | 17.9 | 18.1 | 19.3 | 20.2 | 8.7 | 17.9 |
| m3_skew_month | −0.144 | −0.218 | −0.218 | −0.012 | 0.478 | 0.150 | 0.169 | 0.141 | −0.054 | −0.235 | −0.539 | −0.112 | −0.027 | 0.157 | −0.134 | −0.330 | −0.159 |
| m1_ext_rate_day | 0.015 | 0.016 | 0.015 | 0.015 | 0.015 | 0.015 | 0.015 | 0.014 | 0.013 | 0.015 | 0.015 | 0.015 | 0.013 | 0.015 | 0.013 | 0.013 | 0.013 |
| m3_ext_sign_month | 0.510 | 0.469 | 0.504 | 0.492 | 0.502 | 0.512 | 0.496 | 0.491 | 0.506 | 0.490 | 0.438 | 0.468 | 0.497 | 0.486 | 0.460 | 0.426 | 0.480 |
| m3_storm_clust_month | 0.339 | 0.344 | 0.335 | 0.336 | 0.345 | 0.333 | 0.312 | 0.289 | 0.280 | 0.314 | 0.324 | 0.393 | 0.377 | 0.399 | 0.428 | 0.333 | 0.358 |
| m3_storm_p90_run_month | 2.0 | 2.0 | 1.0 | 2.0 | 2.0 | 2.0 | 2.0 | 1.4 | 2.0 | 2.0 | 2.0 | 2.0 | 2.0 | 2.0 | 2.0 | 2.0 | 2.0 |
| m3_ext_spacing_month | 12 | 12 | 12 | 15 | 15 | 15.5 | 16.5 | 17.5 | 17 | 14.5 | 13 | 9 | 11 | 9 | 8 | 13 | 13 |

## ANNEXE B — REDONDANCE

Matrice Spearman 25 × 25 disponible dans `PHASE3_V2_FEATURE_AUDIT.csv` ;
paires |ρ| ≥ 0.85 : `(m3_range_sigma_day, m3_tr_sigma_day) = +0.999` et
`(m3_storm_clust_month, m3_ext_spacing_month) = −0.88` (inverse structurel).
