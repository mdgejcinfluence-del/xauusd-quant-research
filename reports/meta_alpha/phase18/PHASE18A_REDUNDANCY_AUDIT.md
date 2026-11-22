# PHASE 18-A — AUDIT DE REDONDANCE AVEC LES SEPT VARIABLES GELÉES

Référence : `RATIO_REPLI_EXTENSION_A_TREINT`, `DUREE_EXTREME_VERS_TREINT_MIN`, `MFE_A_TREINT_BP`, `NB_TOUCHES_P0_AVANT_TREINT`, `SESSION_REINTEGRATION`, `ATR14_H1`, `SPREAD_DECISION_BP`.

- **Information réellement nouvelle** : la microstructure des cotations (fréquence de mise à jour, interruptions, tendance du spread) est **absente** du dictionnaire actuel, qui ne contient qu'un niveau ponctuel de spread (`SPREAD_DECISION_BP`) et aucune mesure d'activité de cotation. `QUOTE_UPDATE_RATE_5M`, `MAX_QUOTE_GAP_15M`, `SPREAD_TREND_5M` apportent une dimension inexistante (avec redondance partielle niveau/tendance pour le spread, assumée et documentée).
- **Information partiellement nouvelle** : `RV_MID_30M` partage l'échelle de volatilité avec `ATR14_H1` mais à horizon 30 minutes et sur rendements minute — corrélation attendue, non identité. `PATH_EFFICIENCY_60M` et `REVERSAL_COUNT_60M` décrivent la texture du chemin pré-décision, absente des sept variables (qui décrivent l'impulsion H1 vue par M1, pas l'agitation minute précédant l'entrée).
- **Redondance forte / cosmétique** : `RETRACE_VELOCITY` est le quotient de deux variables déjà présentes (interaction seulement — conservé comme candidat limite, à justifier séparément) ; `DECISION_DISTANCE_TO_EXTREME_ATR` est `MFE_A_TREINT_BP` renormalisé par une autre variable présente — **écarté** comme transformation cosmétique, conformément à l'ordre de mission.

Aucun candidat ne duplique `SESSION_REINTEGRATION` ni `NB_TOUCHES_P0_AVANT_TREINT`.
