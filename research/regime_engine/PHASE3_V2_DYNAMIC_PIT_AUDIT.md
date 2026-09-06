# PHASE 3 V2 — STEP 3.5 : DYNAMIC PIT AUDIT

**Date :** 2026-09-06 (UTC) · **Type :** audit de troncature dynamique — **preuve PAST-ONLY**.
**Références :** `PHASE3_V2_DATA_CONTRACT.md` (FROZEN) · `PHASE3_V2_FEATURE_SPEC.md` (FROZEN) ·
`features_v2_meta.json` · `scripts/feature_engine_v2.py` · `XAUUSD_FEATURES_V2.parquet` ·
`PHASE3_V2_FEATURE_AUDIT.md`.
**Périmètre respecté :** aucune feature modifiée · moteur **non modifié** · aucune aggrégation /
clustering / K / HMM-GMM / backtest / score de performance · **aucune correction automatique** en cas de FAIL.

---

## 1. MÉTHODE (exactement le protocole demandé)

Pour chaque sonde `t` (barre M3, fermée à `Ts = T(t)+2`) :

1. **Valeur complète** : moteur V2 gelé exécuté sur le dataset complet (`XAUUSD_FEATURES_V2.parquet`).
   Contrôle d'identité : un **run complet frais** du moteur a été rejoué et comparé au parquet committé —
   **1 950 valeurs (78 sondes × 25 features), 0 mismatch, bit-à-bit identique** (l'auto-contrôle
   du harnais a bloqué le run en cas d'écart).
2. **Valeur tronquée** : le maître M1 est tronqué strictement après `cut_min` ; les grilles M3/H1 sont
   **reconstruites par le builder FROZEN** (`01_build_layers.py`) à partir du maître tronqué ;
   le **moteur V2 est rejoué à l'identique** sur ces entrées (seuls les chemins I/O et les asserts
   de lignes/SHA du module ont été ré-aiguillés — aucune ligne de code du moteur modifiée).
3. **Comparaison exacte** : `value_full == value_truncated` en float64 (tolérance zéro),
   ou `NaN == NaN` lorsque les deux côtés sont structurellement indisponibles ;
   `abs_diff` = |Δ|, `exact_zero` = 1 ssi Δ == 0.0 exactement.

### 1.1 Sondes (7 périodes, ≥10 par période sauf 2026 — année partielle)

| Période | Nb sondes | Mois couverts | Règle |
|---|---|---|---|
| 2010 | 10 | 03–12 | ≥10 (début d'échantillon : warm-up global ≤ 2010-02-12) |
| 2012 | 12 | 01–12 | ≥10 |
| 2013 | 12 | 01–12 | ≥10 |
| 2016 | 12 | 01–12 | ≥10 |
| 2020 | 12 | 01–12 | ≥10 |
| 2024 | 12 | 01–12 | ≥10 |
| 2026 | 8 | 01–08 | année partielle (dernier M1 : 2026-08-30) — données ne permettant pas ≥10 sondes indépendantes |
| **Total** | **78** | — | — |

Chaque sonde est une barre M3 réelle dont les **25 features sont finies** dans le dataset complet ;
sondes espacées ≥ 27 jours (cadence mensuelle, snap sur barre réelle ≠ rejet de période).
Les 78 sondes couvrent **à la fois** `Ts % 60 == 2` (majorité) et `Ts % 60 == 59` (22 sondes) — les deux cas
d'alignement H1 sont testés (l'importance de cette distinction est démontrée au §3).

### 1.2 Longueurs de troncature par sonde (dépendances indirectes toutes couvertes)

| Mode | cut_min | But |
|---|---|---|
| `exact` | `Ts + 0` | troncature stricte après `t` (test PIT de référence) |
| `p3m`  | `Ts + 3`  | +1 barre M3 après la sonde |
| `p57m` | `Ts + 57` | fin du bucket H1 contenant `Ts` |
| `d1`   | `Ts + 1440` | +1 jour de données futures visibles |
| `w1`   | `Ts + 10080` | +1 semaine de données futures visibles |
| `na`   | `T − 1` | témoin : barre sonde exclue → valeur structurellement indisponible |

Les dépendances indirectes exercées par les 25 features : rolling windows (A/B/C/D),
normalisation (ratios σ, A-1/A-2/A-3), statistiques historiques (ACF/VR/SCF/run/dir),
contexte H1 (A-3/B-6), M1 substrate (A-2/E-4), événements extrêmes (E-1/E-4/E-5),
clustering / spacing (F-1/F-2/F-3), statistiques mensuelles (toutes `*_month`).

### 1.3 Contrôles d'intégrité du harnais (tous vérifiés à chaque run)

- Grille M3 tronquée = **préfixe exact** de la grille complète jusqu'à la sonde (bar_id, t_min,
  OHLC, contig_next) — 78/78 sondes × 5 modes + mode `na`.
- Grille H1 tronquée = préfixe exact de la grille complète **jusqu'à l'heure précédent `hb`** ;
  le bucket H1 `hb` en cours doit **exister** dans la grille tronquée (assertion faite, jamais levée false).
- Moteur : SHA vérifiés, `n_valid`/`n_nan` cohérents, sortie 27 colonnes / 25 features à chaque run.
- Déterminisme : re-exécution complète → parquet byte-identique (SHA `5cebe082…c955`, Step 3.3).

---

## 2. RÉSULTATS GLOBAUX

```
COMPARAISONS PIT (5 modes de troncature : exact/p3m/p57m/d1/w1)
Total         = 9 750   (78 sondes × 25 features × 5 modes)
PASS          = 9 526   (97.70 %)
FAIL          =   224   (  2.30 %)
NA structurels (témoin mode `na`, 78×25) = 1 950  (hors dénominateur PIT ; voir §4)

DYNAMIC_PIT = FAIL
```

| Feature | Famille | PASS | FAIL | Verdict |
|---|---|---|---|---|
| `m3_vol_ratio_day_month` | A | 390 | 0 | PASS |
| `m3_m1_noise_ratio` | A | 390 | 0 | PASS |
| **`h1_vol_ratio_day_month`** | **A** | **278** | **112** | **FAIL** |
| `m3_acf1_day` | B | 390 | 0 | PASS |
| `m3_vr2_month` | B | 390 | 0 | PASS |
| `m3_scf_day` | B | 390 | 0 | PASS |
| `m3_run_month` | B | 390 | 0 | PASS |
| `m3_dir_month` | B | 390 | 0 | PASS |
| **`h1_acf1_month`** | **B** | **278** | **112** | **FAIL** |
| `m3_range_sigma_day` | C | 390 | 0 | PASS |
| `m3_tr_sigma_day` | C | 390 | 0 | PASS |
| `m3_tr_expansion_day` | C | 390 | 0 | PASS |
| `m3_body_range_day` | D | 390 | 0 | PASS |
| `m3_up_wick_day` | D | 390 | 0 | PASS |
| `m3_low_wick_day` | D | 390 | 0 | PASS |
| `m3_close_pos_day` | D | 390 | 0 | PASS |
| `m3_body_dir_day` | D | 390 | 0 | PASS |
| `m3_ext_rate_month` | E | 390 | 0 | PASS |
| `m3_kurtosis_month` | E | 390 | 0 | PASS |
| `m3_skew_month` | E | 390 | 0 | PASS |
| `m1_ext_rate_day` | E | 390 | 0 | PASS |
| `m3_ext_sign_month` | E | 390 | 0 | PASS |
| `m3_storm_clust_month` | F | 390 | 0 | PASS |
| `m3_storm_p90_run_month` | F | 390 | 0 | PASS |
| `m3_ext_spacing_month` | F | 390 | 0 | PASS |

---

## 3. FEATURES EN ÉCHEC — ROOT CAUSE IDENTIFIÉE (exhaustive)

**Features en échec (2 sur 25) :**
1. `h1_vol_ratio_day_month` (A-3) — 112 comparaisons FAIL ;
2. `h1_acf1_month` (B-6) — 112 comparaisons FAIL.

**Répartition des 224 FAIL :**
- **Mode :** `exact` = 112 · `p3m` = 112 · `p57m` / `d1` / `w1` = 0.
- **Sondes :** 56 probes FAIL (toutes avec **`Ts % 60 ≠ 59`**) ; 22 probes PASS intégralement
  (toutes avec **`Ts % 60 = 59`**).
- **Par période (probes concernées) :** 2010 : 8 · 2012 : 7 · 2013 : 9 · 2016 : 10 · 2020 : 8 ·
  2024 : 9 · 2026 : 5.
- **Amplitude :** |Δ| min 5.75e-06 · max 1.54e-01 · moyenne 7.41e-03.

### 3.1 Diagnostic

La cause est un **manque de fermeture du contexte H1** — et non un défaut d'une fenêtre M3/M1 :

- Le moteur calcule `hb = (Ts // 60) * 60` puis `h_idx` = barre H1 du bucket **contenant** `Ts`.
- La SPEC §0.1 formule : `h(t) = floor((T(t)+2)/60)` = « barre H1 dont le bucket contient la minute T+2 ».
- **Mais la même SPEC §0.1 exige** : « bucket fermé — **jamais** une barre H1 se terminant après
  T(t)+2 ».
- Ces deux énoncés ne sont compatibles que si `Ts % 60 = 59` (fin d'heure). Pour `Ts % 60 = 2`,
  le bucket H1 contenant `Ts` se termine **57 minutes après `Ts`** ; sa barre OHLC (construite sur
  tout le bucket dans la grille complète) contient donc des M1 **postérieurs** à `Ts` (jusqu'à
  `Ts + 57`). Le moteur implémente la **formule** (bucket contenant) et non la **garantie de fermeture**
  énoncée par la même ligne de la SPEC.

**Preuve dynamique (le test lui-même) :**
- `exact` (`cut = Ts`) : la grille H1 reconstruite ne peut contenir qu'un bucket `hb` **partiel**
  (M1 ≤ Ts) → `sH24`, `sH336` et l'ACF H1 diffèrent du run complet → **FAIL** (112 cas).
- `p3m` (`cut = Ts+3`) : bucket `hb` encore partiel → **FAIL** (112 cas).
- `p57m` (`cut = Ts+57`) : le bucket `hb` est désormais **complet** → valeurs identiques au
  run complet → **tous PASS**. La fuite est donc bornée à ≤ 57 minutes, exactement le reste du
  bucket H1 contenant la sonde.
- `d1` / `w1` : tous PASS (confirme qu'aucune donnée à plus d'une heure n'est nécessaire).
- Sondes avec `Ts % 60 = 59` : le bucket H1 contenant `Ts` se termine **exactement** à `Ts` →
  run complet == run tronqué → **22/22 probes PASS sur toutes les features et tous les modes**.

Contrôle négatif de la même nature : les features **M3-only et M1-substrate** (23 features)
**passent 390/390** chacun — fenêtres en positions `[i−W+1, i]`, paires propres, extrêmes et
clustering/spacing n'utilisent aucune donnée postérieure à `t` (bit-à-bit).

---

## 4. NA STRUCTURELS (témoin, hors dénominateur PIT)

Mode `na` (`cut = T − 1`, la barre sonde est exclue) : 1 950 lignes (78 × 25) où la valeur tronquée
est **structurellement indisponible** (la barre `t` n'existe plus dans le monde tronqué) —
`value_truncated` vide, `verdict = NA_STRUCTURAL`. Ce témoin confirme que la valeur de chaque feature
à `t` **provient bien de données ≤ t** (aucune feature n'est « reconstituée » sans la barre `t`),
et n'est pas un échec PIT. Les counts PASS/FAIL ci-dessus excluent ces 1 950 témoins.

---

## 5. CONCLUSION ET RÈGLE DE DÉCISION

```
DYNAMIC_PIT = FAIL
Comparaisons PIT           : 9 750
PASS                       : 9 526  (97.70 %)
FAIL                       :   224  ( 2.30 %)
NA structurels (témoin)    : 1 950
Features en échec          : h1_vol_ratio_day_month (A-3), h1_acf1_month (B-6)  [2/25]
Probes en échec            : 56/78 (toutes Ts % 60 ≠ 59) ; 22/78 PASS intégral (Ts % 60 = 59)
Cause racine               : h(t) = bucket H1 CONTENANT Ts ; non fermé à Ts si Ts % 60 ≠ 59
                            (fuite bornée ≤ 57 min, preuve p57m) — la SPEC §0.1 contient
                            à la fois la formule « bucket contenant » et l'exigence
                            « jamais une barre H1 se terminant après T(t)+2 » (contradiction
                            interne) ; le moteur implémente la formule.
```

**Règle de décision appliquée :** toute différence non expliquée ⇒ **FAIL et STOP**. Ici l'écart est
**entièrement expliqué** (diagnostic §3.1) mais il constitue malgré tout une **non-past-only** : les
deux features H1-contexte ne satisfont pas l'objectif « preuve dynamique strictement PAS-ONLY ».
**Aucune correction n'a été appliquée** (ni moteur, ni SPEC — conformément à la consigne
« ne corrige rien automatiquement »). Aucune procédure de clustering/K/HMM-GMM/backtest n'a été lancée.
Le traitement de cette contradiction (ré-alignement `h(t)` = dernier bucket H1 **fermé** ≤ Ts, ou
garantie de fermeture vérifiée) est **différé** à la décision explicite de l'utilisateur.

---

## 6. ARTIFACTS

- `PHASE3_V2_DYNAMIC_PIT_AUDIT.csv` — 11 700 lignes :
  9 750 comparaisons PIT + 1 950 témoins NA ; colonnes `timestamp, probe_id, period, feature,
  family, mode, cut_min, h1_closed_at_ts, value_full, value_truncated, abs_diff, exact_zero,
  verdict` (le minimum demandé `timestamp, feature, value_full, value_truncated, abs_diff,
  exact_zero, verdict` est présent).
- Harnais (non committé, hors repo) : `/tmp/xauusd_audit/dynpit/run_audit.py` — moteur gelé
  importé et exécuté tel quel (seuls les chemins/asserts de module ré-aiguillés), builder gelé
  ré-exécuté sur maître tronqué, comparaison bit-à-bit, auto-contrôle du run complet.
