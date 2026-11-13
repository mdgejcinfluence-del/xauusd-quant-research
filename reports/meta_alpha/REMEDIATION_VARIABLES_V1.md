# RAPPORT DE REMÉDIATION DES VARIABLES — Phase 2 (préparation technique)

**Autorisation :** conditionnelle et limitée du propriétaire (13 nov. 2026).
**Arrêt obligatoire après ce rapport — aucune exploration scientifique lancée.**

## 1. Résultat en chiffres
| Catégorie | Variables | Entrées (variable×fenêtre) |
|---|---|---|
| **Certifiées** (SQL exécuté vs référence indépendante) | ROLL_RANGE_MID, UPDATE_INTENSITY, INTERARRIVAL_MEAN | 11 (4 + 3 + 4) |
| Traduite mais **réserve de définition** (non certifiée scientifique) | ROLL_STD_MID | 4 |
| **Bloquées** (cause écrite ci-dessous) | RET_H, ZSCORE_ROBUST, SPREAD_REGIME, REGIME_CLASS, SUBPERIODE, MFE_H, MAE_H | 7 |
| Hors décompte des 11, certifiées au niveau SQL | MID, SPREAD_ABS, SPREAD_REL, RET_TICK | 4 |

Plan machine-readable : `PLAN_EXTRACTION_REMÉDIE.json` (15 entrées extractibles, 7 refusées).

## 2. Formules SQL exactes (extraites du plan réel, pas recopiées)
- `INTERARRIVAL_MEAN_N50` : `(epoch(t) - epoch(lag(t, 50) OVER (ORDER BY t))) / 50.0`
- `INTERARRIVAL_MEAN_N100` : `(epoch(t) - epoch(lag(t, 100) OVER (ORDER BY t))) / 100.0`
- `INTERARRIVAL_MEAN_N500` : `(epoch(t) - epoch(lag(t, 500) OVER (ORDER BY t))) / 500.0`
- `INTERARRIVAL_MEAN_N1000` : `(epoch(t) - epoch(lag(t, 1000) OVER (ORDER BY t))) / 1000.0`
- `ROLL_RANGE_MID_N50` : `CASE WHEN row_number() OVER (ORDER BY t) >= 50 THEN (max((ask + bid) / 2.0) OVER (ORDER BY t ROWS BETWEEN 49 PRECEDING AND CURRENT ROW) - min((ask + bid) / 2.0) OVER (ORDER BY t ROWS BETWEEN 49 PRECEDING AND CURRENT ROW)) END`
- `ROLL_RANGE_MID_N100` : `CASE WHEN row_number() OVER (ORDER BY t) >= 100 THEN (max((ask + bid) / 2.0) OVER (ORDER BY t ROWS BETWEEN 99 PRECEDING AND CURRENT ROW) - min((ask + bid) / 2.0) OVER (ORDER BY t ROWS BETWEEN 99 PRECEDING AND CURRENT ROW)) END`
- `ROLL_RANGE_MID_N500` : `CASE WHEN row_number() OVER (ORDER BY t) >= 500 THEN (max((ask + bid) / 2.0) OVER (ORDER BY t ROWS BETWEEN 499 PRECEDING AND CURRENT ROW) - min((ask + bid) / 2.0) OVER (ORDER BY t ROWS BETWEEN 499 PRECEDING AND CURRENT ROW)) END`
- `ROLL_RANGE_MID_N1000` : `CASE WHEN row_number() OVER (ORDER BY t) >= 1000 THEN (max((ask + bid) / 2.0) OVER (ORDER BY t ROWS BETWEEN 999 PRECEDING AND CURRENT ROW) - min((ask + bid) / 2.0) OVER (ORDER BY t ROWS BETWEEN 999 PRECEDING AND CURRENT ROW)) END`
- `ROLL_STD_MID_N50` : `CASE WHEN row_number() OVER (ORDER BY t) >= 50 THEN stddev_samp((ask + bid) / 2.0) OVER (ORDER BY t ROWS BETWEEN 49 PRECEDING AND CURRENT ROW) END`
- `ROLL_STD_MID_N100` : `CASE WHEN row_number() OVER (ORDER BY t) >= 100 THEN stddev_samp((ask + bid) / 2.0) OVER (ORDER BY t ROWS BETWEEN 99 PRECEDING AND CURRENT ROW) END`
- `ROLL_STD_MID_N500` : `CASE WHEN row_number() OVER (ORDER BY t) >= 500 THEN stddev_samp((ask + bid) / 2.0) OVER (ORDER BY t ROWS BETWEEN 499 PRECEDING AND CURRENT ROW) END`
- `ROLL_STD_MID_N1000` : `CASE WHEN row_number() OVER (ORDER BY t) >= 1000 THEN stddev_samp((ask + bid) / 2.0) OVER (ORDER BY t ROWS BETWEEN 999 PRECEDING AND CURRENT ROW) END`
- `UPDATE_INTENSITY_T1s` : `count(*) OVER (ORDER BY t RANGE BETWEEN INTERVAL 1 SECOND PRECEDING AND CURRENT ROW)`
- `UPDATE_INTENSITY_T5s` : `count(*) OVER (ORDER BY t RANGE BETWEEN INTERVAL 5 SECOND PRECEDING AND CURRENT ROW)`
- `UPDATE_INTENSITY_T30s` : `count(*) OVER (ORDER BY t RANGE BETWEEN INTERVAL 30 SECOND PRECEDING AND CURRENT ROW)`
## 3. Certification — ce qui a été prouvé, et deux défauts corrigés
Nouveaux tests : `tests/test_sql_certification_audit.py` (7) + `tests/test_regime_protocol_audit.py` (4).
Chaque SQL certifié est **exécuté par DuckDB** sur données contrôlées et comparé à une
référence Python indépendante (formule, colonnes, NULL, frontières, causalité par
perturbation du futur). **Total général : 166 tests verts** (155 + 11).
Défauts réels trouvés par la certification et corrigés :
1. **Warm-up NULL violé** : DuckDB réduit la fenêtre en début de série au lieu de rendre
   NULL. Corrigé par garde `row_number() >= N` sur ROLL_STD_MID et ROLL_RANGE_MID.
2. **Durées texte** : `UPDATE_INTENSITY` recevait « 1s/5s/30s » non parsées. Corrigé
   (`_as_seconds`, « 1min » = 60 s). Convention de frontière certifiée : intervalle
   **fermé [t−T, t]** (RANGE DuckDB inclusif aux deux bornes) — documenté, pas implicite.
Réserve maintenue sur ROLL_STD_MID : le SQL calcule l'écart-type des **niveaux** de mid,
le registre dit « variations de mid ». Écart définition↔traduction signalé, **non tranché
en silence** : la variable est traduite mais déclarée non certifiée scientifiquement
tant que le propriétaire n'a pas choisi la sémantique (écart-type des rendements recommandé).

## 4. Blocages restants (aucun comblé par défaut)
- **RET_H** : définition formelle soumise au §5 — activation interdite avant validation
  (le traducteur lève désormais explicitement cette cause).
- **ZSCORE_ROBUST** : architecture d'extraction en une passe (le retour tick, lui-même
  fenêtre `lag`, ne peut pas alimenter médiane/MAD roulantes dans la même expression) +
  inclusion du retour courant dans la fenêtre de référence non figée. Nécessite une
  extraction en deux étapes à concevoir et certifier séparément.
- **SPREAD_REGIME** : le protocole du propriétaire est une calibration *quotidienne*
  appliquée au lendemain ; une fenêtre roulante continue en SQL dévierait du protocole.
  Bloquée jusqu'à implémentation du protocole par étapes (même moteur que §6).
- **REGIME_CLASS** : fenêtre d'apprentissage non validée (voir §6) — bloquée.
- **SUBPERIODE** : sessions non documentées — bloquée, familles indépendantes non affectées.
- **MFE_H / MAE_H** : convention non spécifiée (direction de référence et prix d'entrée
  Bid/Ask). Sans direction, « excursion favorable » n'a pas de signe défini. Bloquées
  jusqu'à définition formelle, sur le même modèle que RET_H.

## 5. DÉFINITION FORMELLE SOUMISE — RET_H (à valider, NON activée)
**RET_H_ALIGN_V1 (proposition)**
- Origine t : timestamp `timestamp_utc` d'un tick du corpus certifié.
- Prix initial : `mid[t] = (bid[t] + ask[t]) / 2` — rendement **mid-to-mid, brut (GROSS)**,
  indicateur statistique, **pas** un rendement exécutable (les rendements exécutables
  Bid/Ask relèvent de la Phase 4, avec prix d'entrée/sortie opposés).
- Échéance : **premier tick t′ tel que t′ ≥ t + H** (pas d'interpolation, jamais de tick inventé).
- Prix final : `mid[t′]`. Rendement : `RET_H = mid[t′] / mid[t] − 1` (forme du registre).
- Si aucun tick n'existe avant la fin du segment de données : **NULL** (label incomplet,
  ligne conservée). L'écart réalisé (t′ − t) − H et le franchissement d'un trou de marché
  (week-end, suspension) seront journalisés avec le label pour permettre des sensibilités
  ultérieures préenregistrées — aucun seuil de rejet n'est fixé par cette définition.
- Statut : **label** (futur par définition), jamais une feature ; purge de 1h couvrant
  H maximal = 1h ; recouvrement des labels voisins traité comme dépendance, pas comme
  échantillons indépendants.

## 6. Régimes — protocole testé sur données contrôlées (NON activé)
`tests/test_regime_protocol_audit.py` (4 tests verts) : terciles sur 20 jours de marché
glissants, recalculés chaque jour, appliqués au **lendemain** ; 20 premiers jours = NULL
(warm-up assumé) ; causalité prouvée par perturbation du futur ; reproductibilité vérifiée.
**Non activé** dans le calcul principal : en attente de présentation et validation
de la définition (fenêtre W et choix rolling vs expansive restent au propriétaire).

## 7. Git, ressources, limites
- Modifiés : `metaalpha/extract.py` (expansion par fenêtre, 2 traductions nouvelles,
  garde RET_H, warm-up NULL, durées), `tests/test_sql_certification_audit.py`,
  `tests/test_regime_protocol_audit.py`, présent rapport + plan JSON.
- Tests : **166 passed**. Scan secrets : propre. Ressources : CPU local uniquement,
  quelques secondes par suite ; aucun GPU, aucun coût, aucune donnée réelle calculée.
- Cette autorisation n'a été utilisée pour : aucun mining, aucune anomalie, aucune
  stratégie, aucun Holdout, aucun portefeuille, aucune simulation Blue Guardian.

## Verdict de préparation de la Phase 2
**PRÉPARATION TECHNIQUE CONFORME, PARTIELLE ET HONNÊTE** : 3 variables certifiées
(11 entrées) + 4 formules de base certifiées ; 1 réserve de définition (ROLL_STD_MID) ;
7 variables bloquées avec causes écrites et chemins de déblocage identifiés.
**ARRÊT OBLIGATOIRE — en attente d'autorisation explicite pour toute étape supplémentaire.**
