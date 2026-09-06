# PHASE 3 — STEP 2B: FEATURE AUDIT — BLOCKED (environment reset)

**Date:** 2026-09-06 (UTC) · **Mission:** audit-only of
`research/regime_engine/XAUUSD_FEATURES_PIT_FINAL.parquet`.

## STATUT

```
FEATURE_AUDIT_STATUS = BLOCKED
N_FEATURES = UNKNOWN (audit not run; source artifact missing)
PIT_STATUS = PASS (from STEP 1 recorded evidence — artifact of the audit
                   XAUUSD_REGIME_PIT_AUDIT.csv is also lost; see §4)
INF_COUNT = UNDETERMINED
NAN_RATE_RANGE = UNDETERMINED
CONSTANT_FEATURES = UNDETERMINED
HIGH_CORRELATION_PAIRS = UNDETERMINED
EXTREME_DOMINANCE_STATUS = UNDETERMINED
2013_STABILITY = UNDETERMINED
2026_STATUS = UNDETERMINED
FEATURE_SET_READY_FOR_SEGMENTATION = FALSE
```

## 1. Ce qui s'est passé

Entre la fin de STEP 2A et cette étape, l'environnement de travail a été **réinitialisé** :
- `/tmp` a été entièrement vidé (le venv scientific `/tmp/venv_p3` et tout le scratch
  `/tmp/xauusd_audit/` ont disparu — datés de la reconstruction 15:51 UTC) ;
- le répertoire `research/regime_engine/` ne contient plus qu'un fichier :
  `scripts/15_feature_pit_audit.py` (écrit à cette étape) ;
- tous les artefacts Phase 3 non commités ont été perdus (aucun n'était suivi par git).

## 2. Preuves de la perte (vérifiées à l'instant)

| Élément | Statut | Preuve |
|---|---|---|
| `XAUUSD_FEATURES_PIT_FINAL.parquet` (source de l'audit) | **ABSENT** | `ls` vide ; `find /` sans résultat |
| `features_pit.parquet`, `features_spec_pit.json`, `feature_meta.json`, `features.parquet`, `m3_grid.parquet`, `h1_grid.parquet` | ABSENTS (scratch) | `/tmp/xauusd_audit/` inexistant |
| Scripts `01..14`, `p3_common.py`, `feature_runtime.py` | ABSENTS | `ls research/regime_engine/scripts/` → seulement `15_feature_pit_audit.py` |
| CSVs + rapports (`PIT_AUDIT`, `EPISODES`, `TRANSITION_MATRIX`, `STEP1`, `STEP2A`, `DISCOVERY_REPORT`, …) | ABSENTS | `find` sans résultat |
| `/tmp/venv_p3` (numpy/pandas/pyarrow/sklearn/scipy/hmmlearn) | ABSENT | `/tmp/venv_p3` inexistant |
| Master M1 reconstruit + 7 fragments | Fragments **INTACTS** | `git status` : 7 × 20 971 520 B, suivis |
| Rapports Phase 1/Phase 2 | Intacts (commités) | `git ls-files research/` |
| git | Reflog = clone + checkout uniquement | `HEAD@{0} checkout`, `HEAD@{1} clone` → les fichiers Phase 3 n'ont jamais été commités, irrécupérables via git |

## 3. Conséquences pour STEP 2B

La mission demande d'auditer **uniquement** le parquet PIT final. Ce parquet n'existe plus.
Régénérer le dataset exigerait :
1. réinstaller l'environnement scientifique (réseau disponible, ~20 Go libres) ;
2. **reconstruire de mémoire** `p3_common.py` (constantes gelées : `MIN_OBS`, fenêtres,
   graines, bandes, règles d'extrêmes) et `feature_runtime.py` + `01_build_layers.py` ;
3. reconstruire M3/H1 grids depuis le master, puis régénérer les features.

Cette reconstruction ne pourrait **pas être vérifiée comme identique** à l'engine corrigé :
la référence de parité (`features.parquet` et la sortie STEP-2A) a disparu, et les sources
exactes des définitions (01/02/p3_common) ne sont plus dans le workspace. Reconstruire
« à l'identique » sans référence est un risque de dérive de définitions — ce qui violerait
l'esprit de la chaîne PIT (et la mission « ne modifier aucune définition »).

## 4. État de la chaîne PIT (ce qui reste vérifiable)

- **PIT_STATUS = PASS** : établi à STEP 1 (186/186 vérifications de troncature, écart exact
  zéro, 6 sondes 2010/2012/2013/2016/2020/2026) et revalidé à STEP 2A (4/4 sondes C3/D5).
  Les fichiers de preuve (CSV/JSON) sont perdus, mais aucune indication contraire n'existe
  dans le transcript de session ; le statut est conservé avec cette réserve.
- Les rapports `PHASE3_STEP1_PIT_FEATURE_REPAIR.md` et `PHASE3_STEP2A_FEATURE_REBUILD.md`
  ne sont plus dans le workspace non plus.

## 5. Conditions de reprise minimale (après accord)

1. **Réinstaller** `/tmp/venv_p3` (pip : numpy, pandas, pyarrow, scipy, scikit-learn, hmmlearn, joblib).
2. **Restaurer les sources** `p3_common.py`, `01_build_layers.py`, `02_features.py`,
   `feature_runtime.py` (à partir d'un dépôt de référence / une sauvegarde externe),
   ou **ré-établir explicitement les constantes gelées** et revalider par troncature
   (l'égalité avec l'ancien moteur ne peut plus être prouvée sans les sources).
3. **Reconstituer** master (`cat XAUUSD_part_0*.parquet.part` + SHA
   `fdce55a8c8a76c417765ad020794866bb36e5b166c130d2bb4deb2aeeeab91d0`),
   `m3_grid.parquet`/`h1_grid.parquet`, puis `XAUUSD_FEATURES_PIT_FINAL.parquet` (STEP 2A).
4. **Réexécuter** `15_feature_pit_audit.py` (déjà présent, prêt) sur le parquet régénéré.

Aucune segmentation, aucun modèle, aucun K, aucune carte n'ont été lancés. Le master M1 est intact.

## 6. Gate

```
FEATURE_SET_READY_FOR_SEGMENTATION = FALSE
STOP — étape suivante NON lancée.
```
