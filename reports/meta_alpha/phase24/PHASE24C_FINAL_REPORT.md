# PHASE 24-C — RAPPORT FINAL : VALEUR PRÉDICTIVE DES CHAUFFEURS M15

Statut : `EXPLORATORY_POST_HOC` — amélioration prédictive historique uniquement ; aucune
rentabilité démontrée ni autorisée par ce verdict.

## 1. Le généraliste M15 possède un signal prédictif

`M15_TIME_ONLY` (4 733 événements d'entraînement, Horloge seule) : en évaluation, Brier **0,2215**
contre 0,2473 pour son M0, Log Loss 0,634 contre 0,688, AUC 0,712, calibration sans inversion
(pente 1,60). Verdict : **`M15_TIME_ONLY_PREDICTIVE_SIGNAL_SUPPORTED`**.

## 2-3. Les Directeurs n'améliorent pas la prédiction du généraliste

Sur exactement les mêmes événements d'évaluation :

- H4_TIME : le conditionnel bat son M0 (0,2098 contre 0,2475) mais est **moins bon que le
  généraliste** (0,2098 contre 0,1993 ; Δ +0,0105, IC95 par grappe [+0,0008 ; +0,0208] — intervalle
  entièrement du mauvais côté). Verdict : **`M15_H4_NO_INCREMENTAL_PREDICTIVE_VALUE`**.
- D1_TIME : conditionnel 0,2271 contre généraliste 0,2171 (Δ +0,0100, IC95 [−0,0008 ; +0,0209]).
  Verdict : **`M15_D1_NO_INCREMENTAL_PREDICTIVE_VALUE`**.

## 4. Sélection de population ≠ réentraînement

Les populations énergétiques portent bien un signal (chaque conditionnel bat son propre M0),
mais il est intégralement capté par le modèle généraliste appliqué à ces événements ; le
réentraînement sur 408-469 événements dégrade la prédiction par variance d'estimation. Aucun des
critères cumulatifs §11 n'est satisfait pour les variantes conditionnelles (conditions 3, 4 et 5
en échec).

## 5. Stabilité

Coefficients de signes concordants dans les trois modèles, pas de séparation, calibration sans
inversion ; intervalles gouvernés par 45-59 grappes seulement.

**Verdict global : `TIME_ONLY_PREDICTIVE_VALUE_SUPPORTED`.** Aucune autorisation économique ne
découle de ce verdict : toute évaluation économique exigera une phase distincte préenregistrant
architecture de sortie, risque et coûts.
