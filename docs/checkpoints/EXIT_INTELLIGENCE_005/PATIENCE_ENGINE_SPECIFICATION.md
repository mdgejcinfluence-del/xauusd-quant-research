# PATIENCE ENGINE — SPÉCIFICATION

États : INITIAL_POSITION → POST_ENTRY_OBSERVATION → (FAVORABLE_TRAJECTORY →
EXIT_OPPORTUNITY → LIQUIDATION) ou (ADVERSE_TRAJECTORY →
INVENTORY_ACCUMULATION → UNDERWATER_HOLDING → RECOVERY_DEVELOPMENT →
EXIT_OPPORTUNITY) → RESET. La patience = séjour en UNDERWATER_HOLDING tant que
l'état de sortie n'est pas atteint **et confirmé** ; aucune durée fixe. Le retard
de confirmation mesuré (19–246 s) est la première borne quantitative de cette
persistance, sans valeur ponctuelle identifiable.
