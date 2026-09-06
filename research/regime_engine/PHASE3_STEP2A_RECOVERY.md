# PHASE 3 — STEP 2A RECOVERY — BLOCKED (constantes manquantes)

**Date:** 2026-09-06 (UTC) · **Mission:** restaurer exactement le dataset PIT
`XAUUSD_FEATURES_PIT_FINAL.parquet` après réinitialisation de l'environnement.

## STATUT

```
STEP2A_RECOVERY = BLOCKED
DATASET_RESTORED = FALSE
MASTER_STATUS = VERIFIED (5,874,003 rows, SHA fdce55a8…ab91d0)
GRIDS_STATUS = VERIFIED (M3 1,963,826 / H1 98,412 — matched Phase-2B)
CONFIRMED_CONSTANTS_RECOVERED = 8 groups (see §3)
MISSING_CONSTANTS = 10 groups (see §4) — DO NOT INVENT
REBUILD_POSSIBLE = NO (29/31 feature definitions + KEPT list unavailable)
COMMIT_PROTECTIVE = YES (verified recovery artifacts only, see §6)
NEXT = USER INPUT REQUIRED (see §7)
```

---

## 1. Ce qui s'est passé

La réinitialisation du 2026-09-06 (~15:51 UTC) a détruit tout le contenu de
`/tmp` (venv `/tmp/venv_p3`, scratch `/tmp/xauusd_audit/`) et tous les fichiers
Phase 3 non commités : scripts `01…14`, `p3_common.py`, `feature_runtime.py`,
`feature_meta.json`, `features_spec_pit.json`, `XAUUSD_FEATURES_PIT_FINAL.parquet`,
`features.parquet`, `pit_audit_summary.json`, les rapports STEP 1 / STEP 2A /
2B et tous les CSV. Rien n'était suivi par git (reflog = clone + checkout
uniquement), rien n'existe sur GitHub (arbre API + PR — seule la Phase-2B est
sur le remote).

## 2. Recherches effectuées (avant et pendant cette session)

| Source | Résultat |
|---|---|
| `find /` (fichiers/copies/backup) | aucun artefact Phase-3 |
| git reflog / ls-files / log --all | jamais commités ; uniquement clone + checkout |
| `gh api` arbres de branches + PR + repos | aucune occurrence des sources Phase-3 |
| pip/venv | réinstallé (numpy 2.4.6 · pandas 3.0.5 · pyarrow 25.0.1) |
| **Repo committé (cette session, nouveau)** | Phase 1 + Phase 2B **intacts** → source réelle du protocole de grille et des règles extrêmes (voir §3) |
| Surviveur `scripts/15_feature_pit_audit.py` | confirme `Z_CLIP=6.0`, `features_kept` dans `feature_meta.json`, existence de `features.parquet` (`m1_ext`,`r3_ext`), `pit_audit_summary.json` |

## 3. Ce qui est RÉCUPÉRÉ et VÉRIFIÉ

### 3.1 Master M1
- Reconstruit : `cat XAUUSD_part_0*.parquet.part` → `/tmp/xauusd_audit/XAUUSD_M1_reconstructed.parquet`
- **140 192 592 B · SHA-256 `fdce55a8c8a76c417765ad020794866bb36e5b166c130d2bb4deb2aeeeab91d0`** = manifeste Phase 1 (match byte-exact, recalculé)
- **5 874 003 lignes** · 2010-01-01T00:02 → 2026-08-30T23:58 · 15 699 écarts > 1 min
- Colonnes : `timestamp, open, high, low, close, volume` (volume jamais lus — L1)

### 3.2 Grids M3 / H1 (protocole = source committée Phase-2B)
- Source : `research/timeframe_audit/scripts/build_timeframes.py`
  SHA-256 `02d4fcdb…a78adcc` (committé, intact) — contrat : `bar_id = floor(t_min/k)`,
  barre **existe si ≥ 1 barre M1 réelle** (aucune complétude exigée, aucun padding),
  open=first / high=max / low=min / close=last, volume exclu, `MARKET_BREAK_MIN=50`.
- Reconstruit : `/tmp/xauusd_audit/regime_engine/{m3_grid,h1_grid}.parquet` + `grid_manifest.json`

| Check | Reconstruit | Enregistré Phase-2B | Match |
|---|---|---|---|
| M3 barres | 1 963 826 | 1 963 826 (Block A « Bars » + CSV) | ✔ |
| M3 first/last | 2010-01-01T00:00 / 2026-08-30T23:57 | idem CSV | ✔ |
| M3 M1/barre | 2.9911 | 2.9911 | ✔ |
| M3 trous internes | 2 248 (0.1145 %) | « 0.11 % » (Block A §11) | ✔ |
| H1 barres | 98 412 | 98 412 (Block B « Bars ») | ✔ |
| H1 first/last | 2010-01-01T00:00 / 2026-08-30T23:00 | idem CSV | ✔ |
| H1 M1/barre | 59.6879 | 59.6879 | ✔ |
| H1 trous internes | 3 110 (3.16 %) | « 3.16 % » (Block B §7.4a) | ✔ |

- Note : la table des colonnes de sortie suit la convention Phase-2B (`ts` ns UTC,
  `open/high/low/close`, `n_m1`, `internal_missing`, `internal_breaks`, `contig_next`)
  étendue de `bar_id`/`t_min` (dérivation déterministe ; convention de nom RÉ-ÉTABLIE,
  protocole CONFIRMÉ par source committée).

### 3.3 Définitions PIT validées (STEP 1 — GELÉES, consignées verbatim)
- **`C3_recovery50_1440`** : événement `e` = |move[e]| > 1,5·σ_M3[e−1]·close[e] ;
  issue en `e+5` = |close[e+5]−close[e]| ≤ 0,5·|move[e]| ; alignement `recA[t]=outcome[t]`,
  `e = t−5` ; `C3(t)` = ratio glissant-1440 recA/eligibleA. Aucun `close[t+5]`.
- **`D5_breakout_persist`** : événement `e` = breakout 240 barres sur
  `hh_prev/ll_prev` (seuils issus de barres **avant** e) ; issue en `e+5` =
  close[e+5] au-delà du même seuil ; aligné en `t` (e = t−5) ; `D5(t)` = ratio glissant-1440.
  Aucun `close[t+5]`.
- Ancre enregistrée (référence pour validation d'une reconstruction future) :
  dataset 1 963 826 × 64 (`ts_min`, `bar_id` + 31 raw + 31 `ZC_`) ; C3 diffère 90,09 % /
  D5 79,11 % vs ancien moteur ; C3 NaN 11,86 % / médiane 0,3478 ; D5 NaN 3,51 % /
  médiane 0,5882 ; parité 32/32 (ancien moteur).

### 3.4 Constantes confirmées (source exacte)

| Constante | Valeur | Source |
|---|---|---|
| MASTER_SHA | `fdce55a8c8a76c417765ad020794866bb36e5b166c130d2bb4deb2aeeeab91d0` | Phase 1 + Block A/C + recalcul |
| MASTER_ROWS | 5 874 003 | Block A « Bars » |
| PRIMARY_MIN / CONTEXT_MIN | 3 / 60 | mission (M3 primaire / H1 contexte) |
| MARKET_BREAK_MIN | 50 | `build_timeframes.py` (committé) |
| Règle choc | \|log return\| > 3·σ glissant, 1440 min précédentes, past-only ; impl. `round(1440/k)` barres (M1 1440 / M3 480 / H1 24) | Block A/B/C (committés) |
| Z_SCALE | 1.4826 | evidence session |
| Z_CLIP | 6.0 | `15_feature_pit_audit.py` (survivant) |
| L1–L7, gaps, volume, 2026 partiel | — | Phase 1/2B (committés) |

## 4. Ce qui MANQUE — AUCUNE invention (interdiction explicite)

| Groupe | Détail | Conséquence |
|---|---|---|
| `features_kept` | liste exacte des **31 noms** (seuls C3/D5 sont enregistrés) | impossible de recréer les 64 colonnes |
| Définitions des **29 autres features** (familles A–G) | formules, fenêtres, normalisations | 29/31 du dataset non reconstruisibles |
| `feature_windows` | fenêtres par feature (le triplet Phase-2B 60/240/1440 est une référence, pas une preuve) | idem |
| `min_obs` | seuils par feature (seuls 2 fixes sont enregistrés : D2 20→6, h1_vol 16→12) | seuils de NaN non reproductibles |
| `z_window` | fenêtre de normalisation causale médiane/MAD (minutes) | `ZC_*` non reconstruisibles |
| `k_grid_seeds` | K_GRID, SEEDS, SEEDS_HMM | Phase suivante bloquée (hors scope ici) |
| `rule_bands` | bandes Z de la segmentation RULE | idem |
| `m3_extreme_rule_p3` | seuil du flag M3 extrême (`r3_ext`) | colonnes extrêmes de `features.parquet` |
| `feature_meta_schema` | structure exacte de `feature_meta.json` (clé `features_kept` confirmée, reste inconnu) | `15_feature_pit_audit.py` non exécutable |
| Micro-détails C3/D5 | strictness des seuils, définition de `move`, encodage éligibilité/issue, MIN_OBS du ratio glissant | même C3/D5 ne peuvent être garantis « à l'identique » sans validation |

## 5. Statut des livrables

| Livrable | Statut |
|---|---|
| Master M1 | ✔ reconstruit + SHA vérifié |
| M3/H1 grids | ✔ reconstruits + validés (8/8 checks Phase-2B) |
| `p3_common.py` | ⚠ ré-écrit — uniquement constantes confirmées + déclaration `MISSING_CONSTANTS` |
| `01_build_layers.py` | ⚠ ré-écrit — protocole Phase-2B, validé |
| `feature_runtime.py` / `02_features.py` | ✖ perdus — NON ré-écrits (nécessiteraient les constantes manquantes) |
| `XAUUSD_FEATURES_PIT_FINAL.parquet` | ✖ perdu — **non reconstruit** (BLOCKED) |
| `features_spec_pit.json` / `feature_meta.json` | ✖ perdus |
| `PHASE3_STEP1_PIT_FEATURE_REPAIR.md` | ✖ perdu (définitions conservées verbatim en §3.3) |
| `PHASE3_STEP2A_FEATURE_REBUILD.md` | ✖ perdu |
| `scripts/15_feature_pit_audit.py` | ✔ survivant (non modifié) |
| `PHASE3_STEP2B_FEATURE_AUDIT.md` | ✔ survivant (BLOCKED) |

## 6. Actions de protection effectuées

- venv `/tmp/venv_p3` réinstallé (numpy 2.4.6, pandas 3.0.5, pyarrow 25.0.1,
  scipy, scikit-learn, hmmlearn, joblib).
- master reconstruit + `sha256sum` vérifié.
- commits protecteurs : sources récupérées/vérifiées (`p3_common.py` —
  constantes confirmées uniquement ; `01_build_layers.py` — protocole Phase-2B ;
  `15_feature_pit_audit.py` ; rapports) poussés sur
  `arena/01a07681-xauusd-quant-research` pour éviter une nouvelle perte.
- **AUCUNE constante inventée.** Aucune définition modifiée. Aucun dataset
  partiel présenté comme le livrable.

## 7. Gate

```
DATASET_CHANGED = NO (nothing rebuilt, nothing replaced)
FEATURE_SET_READY_FOR_SEGMENTATION = FALSE
STEP2A_RECOVERY = BLOCKED
NEXT = USER INPUT REQUIRED:
   1. fournir les constantes manquantes (§4) — depuis un backup externe ou
      le transcript d'origine ; OU
   2. autoriser une reconstruction best-effort PARTIELLE (grilles ✔ + C3/D5
      + constantes explicitement marquées RECONSTRUCTED) ; OU
   3. déclarer BLOCKED définitif et conserver les artefacts vérifiés.
```
