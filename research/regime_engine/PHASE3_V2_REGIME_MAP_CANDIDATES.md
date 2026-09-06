# PHASE 3 V2 — STEP 3.6F : CARTE CANDIDATE DES RÉGIMES (K-MEANS vs HMM, K=2..5)

- **Étape** : 3.6F — découverte de régimes, run principal (`PHASE3_V2_REGIME_MAP_CANDIDATES.md`)
- **Statut** : **CANDIDATS — PAS VALIDÉS.** Aucun régime n'est retenu comme définitif ; aucun classifieur, aucun choix de K, aucun test financier, aucun backtest, aucune stratégie.
- **Date** : 2026-09-06
- **Source exclusive** : `XAUUSD_FEATURES_V2_REBUILT.parquet` (1 963 826 × 27 ; 1 888 789 lignes multivariées complètes, 96,179 %), `features_v2_rebuilt_meta.json`, `PHASE3_V2_FEATURE_SPEC.md`, `PHASE3_V2_REGIME_DISCOVERY_INPUT.md` (3.6A).
- **Protocole** : 25 features conservées ; ordre temporel strict (aucun shuffle) ; standardisation robuste MAD (fallback std si MAD ≈ 0) ; deux familles indépendantes — **A. K-means** (n_init=10, max_iter=300) et **B. HMM Gaussian diag** (n_iter=50, tol=1e-4, init `stmc`) — pour K = 2, 3, 4, 5 uniquement ; 3 seeds (0, 1, 2) ; sanity HMM full-cov K=2.
- **Provenance (note) :** l'environnement a été réinitialisé après la coupure ; ce rapport est restauré à l'identique depuis l'état de session (aucun recalcul exécuté ; résultats ci-dessous issus des runs 3.6F terminés avant réinitialisation).
- **Mécanique reproductible (à l'époque des runs)** : runners `/tmp/xauusd_audit/dynpit/pilot36f.py` (KM + HMM diag K=2..4), `pilot36f_k5.py` (HMM K=5, patch mémoire identique au calcul), `pilot36f_fullcov.py` (sanity full-cov), `pilot36f_ari.py` (ARI croisés K=2) ; résultats bruts `/tmp/xauusd_pilot36f.json`.
- **Contraintes respectées** : aucun nom de régime avant analyse des profils (sections 2–7 descriptives ; la cartographie nommante n'apparaît qu'en section 8) ; aucun choix de K par score ; aucune sélection sur performance financière ; aucune suppression de feature ; AUCUN COMMIT / AUCUN PUSH.

---

## 1. Comparaison K = 2..5 — K-means vs HMM

### 1.1 Tableau de synthèse

| K | K-means tailles (seed 0) | Silhouette | ARI seeds (0,1)/(0,2)/(1,2) | Médiane épisode (global) | HMM diag tailles (seed 0) | ARI seeds (0,1)/(0,2)/(1,2) | Médiane épisode | États dégénérés (ligne nulle) |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2 | [1 860 888 ; 27 901] | **0.7911** | 1.000 / 1.000 / 1.000 | **566 628** | [579 765 ; 1 309 024] | 1.000 / 1.000 / 1.000 | **252.0** | aucun |
| 3 | [1 775 205 ; 27 901 ; 85 683] | 0.4009 | 0.99998 / 0.99998 / 0.99999 | 1 | [491 756 ; 1 308 837 ; 88 196] | 1.000 / 1.000 / 1.000 | 252.0 | aucun |
| 4 | [1 690 577 ; 84 750 ; 85 561 ; 27 901] | 0.3215 | 0.8854 / 0.8854 / 0.9999 | 1 | [241 497 ; 251 389 ; 87 435 ; 1 308 468] | **≈0 / 0.99989 / ≈0** | 268.0 | **seed 0 : état 3** (ligne nulle) |
| 5 | [80 117 ; 27 901 ; 593 894 ; 85 053 ; 1 101 824] | 0.1224 | 0.9881 / 0.9775 / 0.9735 | 1 | [374 323 ; 85 126 ; 1 259 983 ; 90 099 ; 79 258] | 0.99999 / 0.99999 / 1.000 | 193.0 | aucun |

- Médiane d'épisode : pour K-means K≥3 elle tombe à **1 bar** (les étiquettes K-means basculent au voisinage des frontières ; voir §4.3) ; pour HMM elle reste 193–268 bars (épisodes réels de plusieurs heures/jours).
- Silhouette (K-means) : 0.7911 → 0.4009 → 0.3215 → 0.1224. **Aucun K n'est retenu** : la silhouette décroît mécaniquement quand on fragmente un noyau central ; elle n'est pas un critère de sélection (interdit), et la décroissance indique que les séparations supplémentaires sont des découpages de frontière, pas des structures nouvelles.
- Stabilité inter-seeds : K-means K=2,3 quasi parfaite (ARI ≥ 0.99998) ; K=4 = 0.885–0.9999 (un seed permute deux états) ; K=5 = 0.974–0.988 (même partition à ~1–2 % près). HMM K=2,3,5 : ARI ≥ 0.99999 ; **HMM K=4 instable** : seed 1 s'effondre sur un état unique [[0, 0, 1, 1 888 788]] → l'HMM K=4 n'est pas reproductible (voir §7).

### 1.2 Sanity HMM full-covariance K=2 (seed 0)

| Configuration | Tailles | ARI vs K-means K2 | ARI vs HMM diag K2 |
|---|---:|---:|---:|
| HMM diag K2 | [579 764 ; 1 309 025] | **−0.0154** | — |
| HMM **full** K2 | [1 860 888 ; 27 901] | **1.0000** | **−0.0154** |
| K-means K2 | [1 860 888 ; 27 901] | — | −0.0154 |

En K=2, la partition dépend **entièrement du modèle de covariance** : le HMM diag (indépendance des features) sépare 30,7 %/69,3 % ; le HMM **full** retrouve exactement la partition K-means (état rare 1,48 % = queue skew/kurtosis), ARI = 1.0000. Les deux structures sont **orthogonales** (ARI ≈ 0). Cette « diagonale-dépendance » est le résultat le plus important de l'étape.

---

## 2. États candidats (identifiants descriptifs, aucun nom de régime)

Identifiants internes (pas des noms) :

| ID | Définition brute (avant interprétation) | Configurations où l'état apparaît | Taille (range) | Part du total |
|---|---|---|---|---|
| **E0** | État rare aux skew/kurtosis extrêmes (médianes ≥ 3σ déviation) | KM K2 s1, K3 s1, K4 s3, K5 s2 (même ensemble 27 901 lignes) ; HMM **full** K2 ; **absent du HMM diag** | 27 901 (identique à tous K) | 1,48 % |
| **E1** | État « mèche basse dominante » (2010) : low_wick ↑, body_range ↓, close_pos ↑ | KM K3 s2, K4 s2, K5 s1 ; HMM K3 s2, K4 s2, K5 s1 | 85 053 – 88 196 | 4,50 – 4,67 % |
| **E2** | État skew/kurtosis modérés (2013–2017) | KM K4 s1, K5 s0 ; (approximatif : HMM K5 s3) | 80 117 – 90 099 | 4,24 – 4,77 % |
| **E3** | État rapport de volatilité jour/mois élevé | HMM K5 s4 uniquement | 79 258 | 4,20 % |
| **E4** | État « pas de concentration d'extrêmes » (m3_storm_p90_run_month = 1) | HMM K2 s0, K3 s0, K4 s0 (fragmenté), K5 s0 (fragmenté) ; absent du K-means | 241 497 – 579 765 | 12,8 – 30,7 % |
| **B** | État de référence (profil ≈ médiane globale de toutes les features) | KM K2 s0, K3 s0, K4 s2, K5 s4 ; HMM K2 s1, K3 s1, K4 s3, K5 s2 | 1 101 824 – 1 860 888 | 58,3 – 98,5 % |
| **X** | États sans équivalent dans l'autre famille (fragments de K-means K5 seulement) | KM K5 s2 (593 894), KM K5 s4 vs s0… voir §7 | — | — |

**Aucun K retenu** ; ces candidats sont observés à plusieurs K et/ou dans les deux familles. E1 est le seul candidat présent dans **toutes** les configurations K≥3 des deux familles.

---

## 3. Profil comportemental (médianes des 25 features par état)

### 3.1 Médianes brutes (unités natives)

| Feature | E0 (KM-K2 s1) | E1 (KM-K3 s2) | E2 (KM-K5 s0) | E3 (HMM-K5 s4) | E4 (HMM-K2 s0) | B (HMM-K2 s1) |
|---|---:|---:|---:|---:|---:|---:|
| m3_vol_ratio_day_month | 0.824 | 0.938 | 0.881 | **1.572** | 0.902 | 0.924 |
| m3_m1_noise_ratio | 1.034 | 1.022 | 1.014 | 0.977 | 1.015 | 1.016 |
| h1_vol_ratio_day_month | 0.902 | 0.892 | 0.821 | **1.572** | 0.886 | 0.886 |
| m3_acf1_day | −0.0099 | 0.0170 | −0.0365 | 0.0125 | −0.0213 | −0.0251 |
| m3_scf_day | 0.516 | 0.523 | 0.518 | 0.503 | 0.515 | 0.513 |
| m3_dir_month | −0.0056 | 0.0045 | −0.0006 | 0.0042 | 0.0000 | −0.0005 |
| m3_vr2_month | **0.896** | **1.038** | 0.986 | 0.994 | 0.989 | 0.984 |
| m3_run_month | 1.904 | 1.896 | 1.909 | 1.931 | 1.922 | 1.923 |
| h1_acf1_month | 0.0118 | −0.0138 | −0.0188 | −0.0161 | −0.0151 | −0.0107 |
| m3_range_sigma_day | 1.014 | **1.319** | 1.025 | 1.111 | 1.102 | 1.061 |
| m3_tr_sigma_day | 1.016 | **1.340** | 1.029 | 1.114 | 1.107 | 1.065 |
| m3_tr_expansion_day (bps) | −192.5 | −55.6 | −203.6 | −243.5 | −152.4 | −184.9 |
| m3_body_range_day | **0.485** | **0.366** | 0.495 | 0.509 | 0.489 | 0.495 |
| m3_up_wick_day | 0.204 | 0.187 | 0.202 | 0.191 | 0.201 | 0.202 |
| m3_low_wick_day | 0.204 | **0.378** | 0.200 | 0.198 | 0.206 | 0.203 |
| m3_close_pos_day | 0.500 | **0.618** | 0.498 | 0.510 | 0.504 | 0.500 |
| m3_body_dir_day | 0 | 0.0064 | 0 | 0.0053 | 0 | 0 |
| m3_ext_rate_month | 0.0156 | 0.0167 | 0.0148 | **0.0172** | 0.0154 | 0.0156 |
| m3_ext_sign_month | 0.473 | 0.518 | 0.491 | 0.472 | 0.494 | 0.484 |
| m1_ext_rate_day | 0.0146 | 0.0153 | 0.0139 | **0.0271** | 0.0146 | 0.0146 |
| m3_skew_month | **−9.39** | −0.088 | **+2.43** | −0.30 | −0.066 | −0.100 |
| m3_kurtosis_month | **420.9** | 10.6 | **101.1** | 17.1 | 13.0 | 21.6 |
| m3_storm_clust_month | 0.389 | 0.340 | 0.297 | 0.356 | 0.303 | 0.356 |
| m3_storm_p90_run_month (niv.) | 2 | 2 | 2 | 2 | **1** | 2 |
| m3_ext_spacing_month (niv.) | 10 | 12 | 18 | 12 | 15 | 12 |

### 3.2 Profils en robust-z (écarts en « unités MAD » par rapport à la médiane globale)

| Feature | E0 | E1 | E2 | E3 | E4 | B |
|---|---:|---:|---:|---:|---:|---:|
| m3_vol_ratio_day_month | −0.43 | +0.10 | −0.17 | **+3.08** | −0.07 | +0.03 |
| m3_m1_noise_ratio | +0.36 | +0.11 | −0.03 | −0.75 | −0.01 | +0.01 |
| h1_vol_ratio_day_month | +0.06 | +0.02 | −0.23 | **+2.46** | +0.00 | −0.00 |
| m3_acf1_day | +0.19 | **+0.56** | −0.17 | +0.50 | +0.04 | −0.02 |
| m3_scf_day | +0.09 | +0.38 | +0.16 | −0.43 | +0.03 | −0.03 |
| m3_dir_month | −0.61 | +0.54 | −0.03 | +0.52 | +0.04 | −0.02 |
| m3_vr2_month | **−2.91** | **+1.70** | −0.00 | +0.26 | +0.11 | −0.05 |
| m3_run_month | −0.63 | **−0.91** | −0.46 | +0.28 | −0.03 | +0.01 |
| h1_acf1_month | +0.31 | −0.02 | −0.09 | −0.05 | −0.04 | +0.02 |
| m3_range_sigma_day | −0.38 | **+1.55** | −0.31 | +0.24 | +0.18 | −0.08 |
| m3_tr_sigma_day | −0.39 | **+1.65** | −0.31 | +0.23 | +0.19 | −0.08 |
| m3_tr_expansion_day | −0.09 | +0.59 | −0.14 | −0.34 | +0.11 | −0.05 |
| m3_body_range_day | −0.26 | **−4.22** | +0.06 | +0.53 | −0.13 | +0.05 |
| m3_up_wick_day | +0.11 | −0.64 | +0.03 | −0.49 | −0.02 | +0.01 |
| m3_low_wick_day | −0.01 | **+7.62** | −0.18 | −0.24 | +0.11 | −0.04 |
| m3_close_pos_day | −0.03 | **+4.29** | −0.12 | +0.32 | +0.10 | −0.03 |
| m3_body_dir_day | +0.00 | +0.20 | +0.00 | +0.16 | +0.00 | +0.00 |
| m3_ext_rate_month | +0.05 | +0.93 | −0.52 | **+1.25** | −0.05 | +0.05 |
| m3_ext_sign_month | −0.31 | +0.70 | +0.10 | −0.31 | +0.16 | −0.06 |
| m1_ext_rate_day | +0.00 | +0.10 | −0.10 | **+1.73** | +0.00 | +0.00 |
| m3_skew_month | **−17.5** | −0.00 | **+4.72** | −0.40 | +0.04 | −0.02 |
| m3_kurtosis_month | **+30.5** | −0.65 | **+6.22** | −0.15 | −0.46 | +0.19 |
| m3_storm_clust_month | +0.95 | −0.02 | **−0.85** | +0.29 | **−0.73** | +0.30 |
| m3_storm_p90_run_month | +0.00† | +0.00† | +0.00† | +0.00† | **−2.35†** | +0.00† |
| m3_ext_spacing_month | −0.67 | −0.22 | **+1.12** | −0.22 | +0.45 | −0.22 |

† `m3_storm_p90_run_month` est quasi-constante (niveaux discrets) : MAD ≈ 0 → fallback std (variance quasi nulle) ; l'écart-type « robuste » n'est pas sémantiquement interprétable — le **niveau brut** (1 vs 2) est le seul signal fiable pour E4.

### 3.3 Lecture comportementale (aucune interprétation économique)

- **E0** : médiane skew **−9,4** (≈ −17,5σ de dispersion robuste), kurtosis **420,9** (≈ +30,5σ), vr2 0,896 (−2,9σ), spacing 10 (−0,67σ). Toutes les autres features restent proches de la médiane (|z| < 0,7). C'est un état défini **exclusivement** par des queues extrêmes d'asymétrie/aplatissement mensuels.
- **E1** : low_wick **0,378 vs 0,204** (+7,6σ), body_range **0,366 vs 0,495** (−4,2σ), close_pos **0,618 vs 0,500** (+4,3σ), m3_range/tr_sigma **+1,55/+1,65σ**, vr2 **+1,70σ**, run −0,91σ, acf1 +0,56σ, scf +0,38σ. Signature : mèche basse très longue, corps réduit, clôture proche du haut, dispersion intra-jour plus élevée, autocorrélation jour plus forte, run plus court. **Aucun autre candidat n'a cette combinaison.**
- **E2** : skew **+2,43** (+4,7σ), kurtosis **101,1** (+6,2σ), spacing **18** (+1,12σ), storm_clust **0,297** (−0,85σ), ext_rate 0,0148 (−0,52σ), run −0,46σ. Signature : queue droite modérée, « moins d'agrégats d'extrêmes » (clust ↓, spacing ↑) — très différent d'E0 (queue gauche extrême, agrégats ↑).
- **E3** : vol_ratio_day_month **1,572** (+3,08σ), h1_vol_ratio **1,572** (+2,46σ), m1_ext_rate_day **0,0271** (+1,73σ), ext_rate_month +1,25σ, noise −0,75σ, up_wick −0,49σ, scf −0,43σ. Signature : volatilité intra-jour M3/H1 **nettement au-dessus** de la normale mensuelle, répartition moins gaussienne (noise ↓), fréquence d'extrêmes M1 élevée.
- **E4** : **m3_storm_p90_run_month = 1** (vs 2 partout ailleurs), storm_clust −0,73 à −0,89σ, kurtosis −0,46σ, spacing +0,45σ. Signature : **aucune passe de ≥ P90 extrêmes cumulés dans le mois** — « mois calme en termes d'extrêmes », le reste des features ≈ médiane.
- **B** : toutes les médianes ≈ médianes globales (|z| ≤ 0,3) — état de référence.

---

## 4. Fréquence / persistance

### 4.1 Fréquence (tailles et parts)

| État | KM K2 | KM K3 | KM K4 | KM K5 | HMM K2 | HMM K3 | HMM K4 | HMM K5 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| E0 | 27 901 (1,48 %) | 27 901 (1,48 %) | 27 901 (1,48 %) | 27 901 (1,48 %) | — | — | — | — |
| E1 | — | 85 683 (4,54 %) | 85 561 (4,53 %) | 85 053 (4,50 %) | — | 88 196 (4,67 %) | 87 435 (4,63 %) | 85 126 (4,51 %) |
| E2 | — | — | 84 750 (4,49 %) | 80 117 (4,24 %) | — | — | — | 90 099 (4,77 %)* |
| E3 | — | — | — | — | — | — | — | 79 258 (4,20 %) |
| E4 | — | — | — | — | 579 765 (30,70 %) | 491 756 (26,04 %) | 241 497 (12,79 %) | 374 323 (19,82 %) |
| B | 1 860 888 (98,52 %) | 1 775 205 (93,99 %) | 1 690 577 (89,51 %) | 1 101 824 (58,33 %) | 1 309 024 (69,30 %) | 1 308 837 (69,30 %) | 1 308 468 (69,28 %) | 1 259 983 (66,71 %) |

\* HMM K5 s3 ressemble à E2 (skew +0,72σ, kurt +1,0σ, storm_clust −0,87σ) mais avec un profil atténué — « approchant », pas identique (voir §7). KM K5 s2 (593 894 ; vol_ratio +1,03σ) est un état **sans équivalent** ailleurs (fragmentation K5).

### 4.2 Durées d'épisodes

- **Médiane globale des épisodes** : K-means K2 = 566 628 bars ; K-means K3–K5 = 1 ; HMM K2 = 252, K3 = 252, K4 = 268, K5 = 193.
- **Episode-level (K-means, seed 0, recomputation dédiée)** :
  - **E0** : exactement **2 épisodes** — 2015-07-20 01:36 → 2015-09-01 08:51 (13 952 bars) et 2021-08-08 23:03 → 2021-09-21 09:57 (13 950 bars). Durées quasi symétriques (~6 semaines calendaires chacune).
  - **E1** : 258–266 épisodes, médiane 1 (basculements de frontière), **moyenne 330–332**, max ~27 100 bars (bloc principal début 2010) ; occurrence massive en 2010 puis retours sporadiques (2011, 2020, 2025), dernier 2025-12-01.
  - **E2** : 102 (KM K4) – 219 (KM K5) épisodes, médiane 1, moyenne 368–832, max ~22 600 bars (bloc 2013–2017).
  - **B** : K2 = 3 épisodes (médiane 566 628) ; K3–K5 = fragmentation de frontière (médiane 1, 5 209–39 106 épisodes au global).
- **HMM** (n_episodes globaux) : K2 = 551, K3 = 569, K4 = 845, K5 = 1 365 ; médianes 193–268 bars → les épisodes HMM durent des heures/jours, contrairement aux découpages K-means K≥3.

### 4.3 Persistance (probabilités de transition estimées — diag. de la matrice)

| État | K-means K2 | K-means K3 | HMM K2 | HMM K3 | HMM K4 | HMM K5 |
|---|---:|---:|---:|---:|---:|---:|
| E0 | 0.9999 | 0.9999 | — | — | — | — |
| E1 | — | 0.9970 | — | 0.9997 | 0.9997 | 0.9997 |
| E2 | — | — | — | — | — | 0.9957 |
| E3 | — | — | — | — | — | 0.9960 |
| E4 | — | — | 0.9995 | 0.9995 | 0.9987 | 0.9994 |
| B | 1.0000 | 0.9999 | 0.9998 | 0.9998 | 0.9998 | 0.9997 |

Les probabilités HMM sont des paramètres du modèle (persistance lissée) ; les probabilités K-means sont empiriques sur étiquettes dures (biaisées par les basculements de frontière). Sous les deux lectures, **tous les états candidats ont une forte auto-persistance** (diag ≥ 0.9957) ; E0 est quasi absorbant (0.9999) car il n'existe que dans 2 fenêtres.

---

## 5. Transitions

### 5.1 K-means (empiriques, étiquettes dures, K=2..5)

**K=2** : [[0, 1] : 1.0000, 0.0000 ; E0→B 0.0001, 0.9999]
**K=3** (ordre : B, E0, E1) :
```
B  → B 0.9999  E0 0.0000  E1 0.0001
E0 → B 0.0001  E0 0.9999  E1 0.0000
E1 → B 0.0030  E0 0.0000  E1 0.9970
```
**K=4** (ordre : B, E2, E1, E0) :
```
B  → B 0.9998  E2 0.0001  E1 0.0002  E0 0.0000
E2 → B 0.0013  E2 0.9987  E1 0.0000  E0 0.0000
E1 → B 0.0030  E2 0.0000  E1 0.9970  E0 0.0000
E0 → B 0.0001  E2 0.0000  E1 0.0000  E0 0.9999
```
**K=5** (ordre : E2, E0, X, E1, B) — lignes :
```
E2 → E2 0.9973  E0 0.0000  X 0.0018   E1 0.0000  B 0.0010
E0 → E2 0.0000  E0 0.9999  X 0.0000   E1 0.0000  B 0.0001
X  → E2 0.0002  E0 0.0000  X 0.9674   E1 0.0002  B 0.0321
E1 → E2 0.0000  E0 0.0000  X 0.0014   E1 0.9969  B 0.0017
B  → E2 0.0001  E0 0.0000  X 0.0173   E1 0.0001  B 0.9825
```

### 5.2 HMM (paramètres du modèle, diag)

**K=2** : [[0.9995, 0.0005], [0.0002, 0.9998]]
**K=3** (ordre : E4, B, E1) :
```
E4 → E4 0.9995  B 0.0005  E1 0.0000
B  → E4 0.0002  B 0.9998  E1 0.0000
E1 → E4 0.0001  B 0.0002  E1 0.9997
```
**K=4** (seed 0 ; ordre : E4′, E2-ish, E1, B) :
```
S0 → S0 0.9987  S1 0.0006  E1 0.0000  B 0.0007
S1 → S0 0.0006  S1 0.9990  E1 0.0000  B 0.0004
E1 → S0 0.0001  S1 0.0000  E1 0.9997  B 0.0002
B  → S0 0.0001  S1 0.0001  E1 0.0000  B 0.9998
```
**K=5** (ordre : E4′, E1, B, E2′, E3) :
```
E4′→ E4′ 0.9994  E1 0.0000  B 0.0000  E2′ 0.0004  E3 0.0002
E1 → E4′ 0.0000  E1 0.9997  B 0.0001  E2′ 0.0000  E3 0.0001
B  → E4′ 0.0000  E1 0.0000  B 0.9997  E2′ 0.0001  E3 0.0002
E2′→ E4′ 0.0020  E1 0.0000  B 0.0020  E2′ 0.9957  E3 0.0003
E3 → E4′ 0.0007  E1 0.0001  B 0.0027  E2′ 0.0005  E3 0.9960
```

Lecture : les états candidats sont **fortement persistants** (diag ≥ 0.9957) et les transitions sortantes sont faibles ; la transition la plus notable hors diagonale est **X→B 0.0321 (K-means K5)** et **E2′→E4′ 0.0020 / B 0.0020 (HMM K5)** — aucune transition « charnière » n'émerge clairement. **Aucune interprétation économique.**

---

## 6. Stabilité temporelle 2010–2026 (répartition par année de chaque état, %)

### 6.1 E0 — identique pour KM K2/K3/K4/K5

| Année | 2010 | 2011 | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| E0 | 0 | 0 | 0 | 0 | 0 | **50.0** | 0 | 0 | 0 | 0 | 0 | **50.0** | 0 | 0 | 0 | 0 | 0 |

### 6.2 E1 (KM K3 s2 / HMM K5 s1)

| Année | 2010 | 2011 | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| KM K3 | **97.9** | 1.2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0.4 | 0 | 0 | 0 | 0 | 0.4 | 0 |
| HMM K5 | **98.5** | 1.1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0.3 | 0 |

### 6.3 E2 (KM K5 s0 ; KM K4 s1 très proche)

| Année | 2010 | 2011 | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| KM K5 s0 | 0 | 0 | 0 | 28.2 | 19.0 | 0 | 35.1 | 14.6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3.1 |
| KM K4 s1 | 0 | 0 | 0 | 26.7 | 18.4 | 0 | 35.5 | 15.8 | 0 | 0 | 0 | 0 | 0 | 0 | 0.7 | 0 | 2.9 |

### 6.4 E3 (HMM K5 s4)

| 2010 | 2011 | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 7.0 | **21.2** | 9.4 | 5.2 | 5.0 | 1.1 | 2.7 | 1.2 | 2.9 | 5.0 | **17.3** | 2.4 | 1.9 | 1.9 | 3.4 | 7.3 | 5.0 |

### 6.5 E4 (HMM K2 s0) vs B (HMM K2 s1)

| | 2010 | 2011 | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| E4 | 15.0 | 9.3 | 12.1 | 0.1 | 5.0 | 2.7 | 6.4 | 10.9 | 6.7 | 6.4 | 8.4 | 0.9 | 4.1 | 0.8 | 0.4 | 5.8 | 4.9 |
| B | 1.4 | 4.9 | 3.4 | 8.3 | 6.1 | 7.4 | 5.9 | 3.9 | 5.8 | 5.9 | 5.0 | 8.3 | 7.0 | 8.4 | 8.6 | 6.2 | 3.6 |

### 6.6 Lecture temporelle

- **E0** : **non persistant dans le temps** — 2 fenêtres de ~6 semaines (2015-07-20→09-01 ; 2021-08-08→09-21), 0 % ailleurs. C'est un événement ponctuel (période de skew/kurtosis extrêmes), pas un régime récurrent. Ces fenêtres correspondent exactement aux anomalies de queues signalées par l'audit des features (règle F3 « ≥ 30 extrêmes », cf. 3.6A) → **à traiter comme drapeau de qualité de données, avec prudence absolue**.
- **E1** : **concentré sur 2010** (98 %) — commence à la première ligne exploitable (2010-02-12 11:57) ; pas de retour significatif ensuite. Structure globalement stable SUR 2010 (max épisode ~27 100 bars), mais **non récurrente**.
- **E2** : **concentré 2013–2017** (~93–97 %) — présent sur plusieurs années (2013, 2014, 2016, 2017) mais **discret/épisodique** (médiane épisode 1, max ~22 600) ; persistance plus faible (0.9957).
- **E3** : **étalé sur toutes les années** avec pics 2011 (21 %) et 2020 (17 %) — c'est le candidat le plus « multi-années » après B, mais **détecté uniquement par le HMM K5** (une seule configuration).
- **E4** : présent tous les ans (0,1–15,0 %), mais son poids **varie avec K** (30,7 % en K2 → 12,8–19,8 % en K4/5 → 0 % en K-means) : la séparation « mois sans extrêmes cumulés » n'est **pas stable en K ni entre familles**.
- **B** : seul état présent en continu sur toute la période.

---

## 7. Concordance / divergence entre familles et entre K

### 7.1 Concordances fortes

1. **E1 (structure 2010)** — le seul état retrouvé dans **6/6 configurations K≥3** (KM K3/K4/K5 et HMM K3/K4/K5), avec des profils z quasi identiques :
   - KM K3/K4/K5 : low_wick +7.62σ, body_range −4.22σ, close_pos +4.29/4.30σ, sigma +1.55/1.66σ, vr2 +1.70σ, run −0.91/−0.93σ ;
   - HMM K3 : low_wick **+7.56σ**, body_range **−4.17σ**, close_pos **+4.27σ**, sigma +1.51/1.62σ, vr2 +1.69σ ; HMM K5 : low_wick +7.63σ, body_range −4.22σ, close_pos +4.29σ.
   - Tailles 85 053–88 196 (4,50–4,67 %) : écart max ~3,7 % entre configurations.
   → **Concordance inter-familles et inter-K la plus élevée de l'étude.**
2. **E0 (queue extrême 2015/2021)** — **identique à l'ensemble de ligne près** à travers KM K2→K5 (27 901 lignes, mêmes 2 fenêtres, mêmes profils −17,5σ/+30,5σ) et **identique à la partition HMM full-cov K2** (ARI 1.0000, tailles identiques [1 860 888 ; 27 901]). → Concordance K-means ↔ HMM **quand les corrélations sont prises en compte** (full).
3. **États candidats à ~4,5 %** (E1/E2/E3) : les deux familles produisent systématiquement un ou plusieurs états de taille 4,2–4,8 % (85k-90k), mais avec des contenus différents selon la famille (voir 7.2).

### 7.2 Divergences

1. **K=2 divergent** : KM K2 = « queue extrême vs reste » (1,48 %) (silhouette 0.79) ; HMM diag K2 = « mois sans extrêmes cumulés vs reste » (30,7 %/69,3 %) — **ARI cross-famille = −0.0154**. Le HMM **full-cov** K2 = KM K2 (ARI 1.0000). → La structure K=2 n'est pas une propriété des données, mais du **modèle de covariance**.
2. **HMM K=4 instable** : seed 1 = solution dégénérée à état unique [0 ; 0 ; 1 ; 1 888 788] ; seed 0 = solution avec état à ligne nulle (état 3) ; seed 2 = solution « propre » ; ARI (seed 0 vs 2) = 0.99989 mais ARI ≈ 0 vs seed 1. → **HMM K=4 non reproductible**, résultats de K=4 à considérer comme indicatifs.
3. **E0 absent du HMM diag** : les HMM diag K2–K5 absorbent les 27 901 lignes extrêmes dans leurs états principaux (aucun état de 1,48 % avec skew −17σ/kurt +30σ). Le HMM diag ne voit pas la queue extrême comme séparée (les corrélations avec les autres features sont faibles ; voir §3.2 où E0 n'a que 2-3 features déviantes).
4. **E2/E3 divergents** : E2 = KM K4/K5 (avec HMM K5 s3 « approchant ») ; E3 = HMM K5 uniquement. KM K5 s2 (593 894, vol_ratio +1.03σ) est un split **sans équivalent** → fragmentation K5.
5. **E4 HMM-only** : jamais retrouvé par K-means (le K-means scinde sur skew/kurtosis, pas sur storm_p90_run_month, feature à MAD ≈ 0).
6. **Durée d'épisodes divergente** : KM K≥3 → médiane 1 bar (les états K-means de taille ~85k sont des **mosaïques** d'épisodes 1 bar dans les frontières, avec un noyau continu) ; HMM → épisodes 193–268 bars. À K≥3, **K-means ne produit pas des états temporellement cohérents** ; il produit des voisinages de proximité-spatiale.

### 7.3 Synthèse « existe-t-il des états comportementaux distincts ? »

- **OUI en K=2 pour la queue extrême** (E0) : détectée identiquement par KM K2 et HMM full-cov K2 (ARI 1.0), mais c'est un **événement ponctuel** (2 fenêtres de 6 semaines, 1,48 %) et non un régime récurrent ; c'est aussi l'épisode de skew/kurtosis extrême connu (drapeau qualité de données).
- **OUI pour E1 (structure 2010)** : la structure la plus reproduite (6/6 configurations, profils quasi identiques), mais **confinée à la première année** (98 % 2010) — séparation temporelle, pas récurrence multi-années.
- **PARTIEL pour E2** (skew/kurtosis modérés 2013–2017) : 2-3 configurations, épisodique.
- **FAIBLE/NON pour E3** (1 configuration), **NON pour E4** (HMM-only, instable en K).
- **NON pour l'idée de « plusieurs régimes persistants »** : aucune structure à K≥3 n'est simultanément (a) reproduite dans les deux familles, (b) stable entre seeds, (c) récurrente dans le temps, et (d) à épisodes longs. Les seuls candidats à forte concordance (E0, E1) sont **temporellement localisés**.

---

## 8. Cartographie candidate des régimes (PROVISOIRE — non validée)

> **Discrétion** : cette carte est une **hypothèse de travail**, après analyse des profils (section 3). Elle n'est **pas** une conclusion définitivement validée : aucun classifieur n'est construit, aucun K n'est retenu, aucune performance financière n'est évaluée, aucun backtest n'est réalisé (interdits).

| ID | Nom proposé (comportemental) | Définition (features discriminantes) | Configurations | Fréquence | Persistance | Fenêtres temporelles | Concordance |
|---|---|---|---|---|---|---|---|
| **R-B** | État de référence | profil ≈ médiane (|z| ≤ 0.3 sur 25 features) | KM K2–K5 ; HMM K2–K5 | 58–99 % | forte (0.98–1.0) | continue 2010–2026 | 8/8 |
| **R-E0** | « queue aplatissement extrême » (candidat anomalie de données) | skew −17.5σ, kurtosis +30.5σ, vr2 −2.9σ, storm_clust +0.95σ | KM K2/K3/K4/K5 (même ensemble) + HMM **full** K2 | 1,48 % (27 901) | quasi-absorbeur (0.9999) ; **2 épisodes** | 2015-07-20→09-01 ; 2021-08-08→09-21 | 5/8 (full uniquement côté HMM) |
| **R-E1** | « structure mèche-basse/2010 » | low_wick +7.6σ, body_range −4.2σ, close_pos +4.3σ, sigma +1.5σ, vr2 +1.7σ, run −0.9σ | KM K3/K4/K5 + HMM K3/K4/K5 | 4,5–4,7 % (85 053–88 196) | diag 0.997 (KM) à 0.9997 (HMM) ; 258–266 épisodes (fragmentation liée aux frontières) ; noyau ~27 100 bars | 2010-02-12 → ~2010 (98 %), retours 2011/2020/2025 < 1,5 % | **6/6 configs K≥3** |
| **R-E2** | « skew/kurtosis modérés, extrêmes moins agrégés » | skew +4.7σ, kurtosis +6.2σ, spacing +1.1σ, storm_clust −0.85σ, ext_rate −0.5σ | KM K4/K5 (+ HMM K5 s3 approchant) | 4,2–4,8 % (80–90 k) | 0.9957–0.9973 ; épisodique (max épisode 22 600) | 2013–2017 (93–97 %) | 2/8 + 1 approchant |
| **R-E3** | « volatilité jour/mois élevée » | vol_ratio_day +3.1σ, h1_vol_ratio +2.5σ, m1_ext_rate_day +1.7σ, ext_rate +1.3σ, noise −0.75σ | HMM K5 s4 uniquement | 4,20 % (79 258) | diag 0.9960 ; médiane épisode 193 (K5 global) | étalé ; pics 2011 (21 %), 2020 (17 %) | **1/8** |
| **R-E4** | « mois sans extrêmes cumulés » (storm_p90_run=1) | storm_p90_run niv. 1 vs 2 ; storm_clust −0.73/−0.89σ ; kurtosis −0.46σ | HMM K2/K3/K4/K5 (fragmenté en K4/K5) | 12,8–30,7 % (241 k–580 k) | diag 0.9987–0.9995 | tous les ans (2010 15 % max) | **HMM-only** |

### 8.1 Non retenus / à écarter pour la suite

- **KM K5 s2** (593 894, vol_ratio +1.03σ — état « X » de la section 2, sans équivalent dans aucune autre configuration) et la dichotomie de l'état de référence en K5 (s4 modéré vs s2) : fragments à K=5 uniquement, médiane d'épisode 1 → non reproduits.
- **HMM K4 seed 1** (effondrement 1 état) : dégénérescence ; **HMM K4 seed 0** (état 3 à ligne de transition nulle) : solution limite, à ne pas interpréter.
- **E4** : la séparation repose sur une feature quasi-constante (MAD ≈ 0, fallback std) → le z-score n'est pas fiable ; la distinction « niveau 1 vs 2 » de `m3_storm_p90_run_month` est réelle mais **le poids de l'état change avec K** ; à traiter comme structure faible.

### 8.2 Éléments de prudence obligatoires

1. **Pas de sélection de K** : aucun score (silhouette, AIC/BIC, vraisemblance) n'a servi à retenir un K ; la carte ci-dessus est **indépendante d'un choix de K** (candidats définis par concordance inter-configurations).
2. **Pas de classifieur** : le passage de cette carte à un classifieur d'états (ainsi que toute évaluation financière) est **hors périmètre** de 3.6F et n'a pas été réalisé.
3. **Drapeaux de qualité de données** : R-E0 coïncide avec les anomalies de queues du dataset (règle F3, ≥30 extrêmes — 3.6A) et R-E1 est confiné à 2010 (première année du domaine, également lieu des anomalies résiduelles 3.6D) ; avant toute utilisation, une **validation de la source et du pipeline M1/M3/H1** sur ces fenêtres (2015-07/09, 2021-08/09, 2010) est nécessaire.
4. **Persistance modèle vs labels** : les transitions K-means sont empiriques sur labels durs ; seul le HMM fournit des probabilités estimées, et uniquement pour le K de son modèle (K non sélectionné).
5. **Limites techniques** : HMM diag entraîné à n_iter=50 avec avertissements de non-convergence (delta ~ −0.001 à −0.005 sur les dernières itérations) ; HMM K=5 exécuté avec un calcul de densité **mathématiquement identique** (vérifié, écart max 0.0) mais réparti en mémoire (contrainte RAM 4 Go) ; sanity full-cov seulement K=2 ; un seul échantillon robuste (aucun shuffle, ordre temporel strict).

### 8.3 Prochaines étapes suggérées (hors 3.6F, non exécutées)

- Validation de source des fenêtres R-E0 et de la période 2010 (R-E1) — audit amont, avant toute modélisation.
- Évaluation de structures K=2 (E0 + B) et « E1 + B » avec un modèle de mélange **full-cov** et 4-6 seeds supplémentaires, + critères de stabilité (ARI ≥ 0.95) — ceci n'est pas un choix de K par score.
- Étude de la sensibilité de R-E4 au traitement de `m3_storm_p90_run_month` (feature quasi-constante ; MAD ≈ 0) — à faire dans le cadre d'une revue de features, sans suppression définitive.

---

*Fin du rapport — Step 3.6F. Aucune sélection définitive, aucune stratégie, aucun backtest ; aucun commit, aucun push.*
