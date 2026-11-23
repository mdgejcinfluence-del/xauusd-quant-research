# PHASE 18-B — AUDIT D'INTÉGRITÉ TEMPORELLE

Contrat appliqué (formules gelées 18-A, aucun écart) : toute cotation utilisée vérifie `timestamp_utc <= t_decision` (requêtes des lots bornées `>= t_decision-15min AND <= t_decision`, `ci_tools/phase18b_engine.py` mode_lot) ; toute barre M1 utilisée est **close** avant la décision (`cloture = ts + 1min <= t_decision`, fenêtres de 30 et 61 clôtures consécutives exigées). Aucun tick futur ne borne un écart de cotation : `MAX_QUOTE_GAP_15M` est le maximum des écarts entre cotations consécutives **observées** dans la fenêtre, sans projection du tick suivant. Aucun remplissage déduit d'un franchissement. Les fenêtres incomplètes produisent `NON_VALIDABLE` (valeur absente), jamais d'imputation ni de complétion.

Vérifications : bornes visibles dans le code committé du moteur (seq356) ; 0 valeur non finie ; couverture par variable et par segment dans `PHASE18B_FEATURE_COVERAGE.csv` ; les seuls manquants sont des fenêtres barres incomplètes (9 à 16 par segment pour les variables 60 min, 1 à 9 pour RV 30 min) et 1 sous-fenêtre de spread vide en apprentissage. Aucun événement sans lot tick (0 dans `PHASE18B_EVENT_RECONCILIATION.csv`), 0 doublon d'`event_id` entre lots (affectation par partition contenant `t_decision`).

Verdict temporel : aucun candidat `REJECTED_TEMPORAL_LEAKAGE`.
