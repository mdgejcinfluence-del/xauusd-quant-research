# RAPPORT CONSOLIDÉ — Préparation Phase 2 (après décisions du 13 novembre 2026)

**Décisions intégrées :** RET_H_ALIGN_V1 approuvée · ROLL_STD_MID = écart-type des rendements ·
REGIME_CLASS terciles/20 jours en configuration expérimentale. **ARRÊT OBLIGATOIRE après ce rapport.**

## 1. Compte exact
| Catégorie | Variables | Entrées |
|---|---|---|
| **Certifiées** (SQL exécuté vs référence indépendante, NULL, frontières, causalité) | RET_H (label), ROLL_STD_MID, ROLL_RANGE_MID, UPDATE_INTENSITY, INTERARRIVAL_MEAN | **22** (7+4+4+3+4) |
| Base SQL certifiée (hors les 11) | MID, SPREAD_ABS, SPREAD_REL, RET_TICK | 4 |
| **Bloquées** | ZSCORE_ROBUST, SPREAD_REGIME, REGIME_CLASS, SUBPERIODE, MFE_H, MAE_H | 6 variables |

Plan machine-readable : `PLAN_EXTRACTION_CONSOLIDE.json` (22 extractibles, 6 refusées).

## 2. Formules définitives et SQL exact
- **RET_H** : `RET_H(t) = (MID(t_H) − MID(t)) / MID(t)`, t_H = premier tick ≥ t+H.
  Tick initial = événement du corpus à l'instant t (ordre tranché par `observation_id`
  dans le corpus réel ; les doublons de timestamp sont des événements distincts,
  jamais fusionnés). Frontières de partitions : l'extraction étant par partition,
  un horizon qui dépasserait la fin de partition est **NULL** (perte conservatrice
  assumée, aucune lecture croisée silencieuse). Échéance incomplète = NULL.
  Frontières IS/OOS/Holdout : origine à moins de H de la frontière exclue par la
  purge (max 1h) ; embargo symétrique. **Jamais une feature** : le plan marque
  RET_H `kind=label` (test dédié), les labels ne peuvent alimenter une décision à t.
- **ROLL_STD_MID** : stddev_samp (convention échantillon, dénominateur N−1) des
  rendements mid consécutifs r_i = (mid_i − mid_{i−1})/mid_{i−1}, fenêtres événements
  50/100/500/1000, warm-up NULL (première valeur à l'événement N+1, quand N rendements
  existent), mid nul/invalide protégé par NULLIF (rendement NULL, pas de crash).
- **REGIME_CLASS** : protocole approuvé enregistré en version 2 au registre
  (terciles, 20 jours glissants, recalcul quotidien, application au lendemain,
  20 premiers jours NULL, HMM conservé comme comparatif distinct). Sa traduction
  reste **non certifiée** : le protocole quotidien exige une extraction étagée,
  pas encore implémentée — la variable reste donc bloquée pour le calcul,
  approbation de configuration ≠ activation.

## 3. Tests
- Certification SQL : chaque traduction exécutée sous DuckDB sur données contrôlées,
  comparée à des références Python indépendantes (dont RET_H : horizons 5s exacts,
  NULL terminal ; ROLL_STD : écarts-types de rendements calculés par `statistics`).
- Anti-lookahead : perturbation du futur sans effet sur les features passées ;
  RET_H étiqueté label de façon structurelle dans le plan.
- Protocole régimes : tests contrôlés inchangés et verts (warm-up 20 jours, lendemain, causalité).
- **Total : 168 tests passés (+1 conditionnel au registre, exécuté et vert avec
  le registre réel monté : 10/10 sur le fichier de certification).** Scan secrets : propre.

## 4. Variables encore bloquées — raisons
ZSCORE_ROBUST (médiane/MAD roulantes = extraction en deux étapes à certifier) ·
SPREAD_REGIME (même moteur quotidien que REGIME_CLASS, à implémenter par étapes) ·
REGIME_CLASS (protocole approuvé, traduction étagée non implémentée) ·
SUBPERIODE (sessions non documentées) · MFE_H/MAE_H (convention de direction et
de prix d'entrée Bid/Ask toujours à définir formellement).

## 5. Preuve d'intégrité du corpus (inchangée, revérifiée dans cette passe via les registres)
348/348 partitions · 685 118 625 lignes (écart 0) · certificats CERTIFIED ·
empreintes canoniques P1 `9bbeb9a2…`, P2 `bb3b63f1…` (`BASELINE_HASH_MANIFEST.json`) ·
bornes 2010-01-04 → 2026-09-30 UTC. Aucune donnée synthétique hors fixtures de test.

## 6. Git et ressources
Modifiés dans cette passe : `metaalpha/extract.py` (RET_H certifié, ROLL_STD rendements,
étage enrichi mid/ret_mid, déduplication des versions, étiquette label),
`tests/test_sql_certification_audit.py` (RET_H, ROLL_STD, garde label),
registres v2 sous `META_ALPHA_WORK/` (RET_H, ROLL_STD_MID, REGIME_CLASS),
`PLAN_EXTRACTION_CONSOLIDE.json`, présent rapport.
Ressources : CPU local uniquement, suites de tests ≈ 9 s, 0 FCFA, aucun GPU,
aucune donnée réelle calculée, aucun mining, aucun Holdout, aucun portefeuille.

## Verdict de préparation de la Phase 2
**PRÊT SOUS RÉSERVES EXPLICITES** : 5 variables certifiées (22 entrées) sur 11,
6 bloquées avec causes et chemins de déblocage. La montée L0→L4 reste **non autorisée
à ce stade** et n'a pas été lancée. **ARRÊT OBLIGATOIRE — autorisation explicite
requise pour toute exploration scientifique ou mining.**
