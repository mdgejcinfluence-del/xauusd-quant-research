# PHASE 18-A — AUDIT DE CAUSALITÉ DES CANDIDATS

Règle unique : toute variable doit être calculable à partir de champs horodatés `<= t_decision` (barres M1 **closes** avant la décision pour les candidats barres ; cotations de timestamp `<= t_decision` pour les candidats tick). Aucune valeur postérieure, aucun MFE/MAE final, aucun mécanisme de sortie, aucun payoff futur.

| Candidat | Disponibilité causale | Verdict |
|---|---|---|
| QUOTE_UPDATE_RATE_5M | Comptage de cotations sur fenêtre close à `t_decision` ; démontrable dès l'extraction (filtre `timestamp_utc <= t_decision`) | CAUSAL sous contrat de calcul gelé |
| MAX_QUOTE_GAP_15M | Écarts entre cotations consécutives toutes `<= t_decision` ; le dernier écart est borné par `t_decision` (écart censuré à droite à documenter : utiliser le dernier tick `<= t_decision` sans projeter le suivant) | CAUSAL avec convention de bord à geler |
| SPREAD_TREND_5M | Médianes de spread sur deux sous-fenêtres closes avant `t_decision` | CAUSAL |
| RV_MID_30M / PATH_EFFICIENCY_60M / REVERSAL_COUNT_60M | Barres M1 dont `ts + 1 minute <= t_decision` ; les barres committées proviennent de ticks réels avec `first_tick_ts`/`last_tick_ts` traçables | CAUSAL |
| RETRACE_VELOCITY | Recomposition de deux champs causaux déjà gelés | CAUSAL mais redondance forte (cf. audit redondance) |
| DECISION_DISTANCE_TO_EXTREME_ATR | Idem | CAUSAL mais écarté (cosmétique) |

Risques de fuite identifiés à verrouiller dans tout contrat futur : (1) inclure la barre M1 contenant `t_decision` (elle contient des ticks postérieurs) — interdit, seules les barres closes comptent ; (2) utiliser le « prochain tick » pour borner un écart de cotation — interdit ; (3) recalculer un ATR ou un extrême sur une fenêtre débordant la décision — interdit. Les candidats dont la fenêtre pré-décision est vide ou incomplète sont `NON_VALIDABLE` événement par événement, jamais imputés. Aucun candidat ne requiert de champ inexistant ; aucun n'est classé `NON_VALIDABLE` par construction.
