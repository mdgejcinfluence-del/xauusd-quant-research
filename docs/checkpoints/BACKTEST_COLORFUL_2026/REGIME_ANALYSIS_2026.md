# BACKTEST-COLORFUL-2026 — ANALYSE DES RÉGIMES (novembre partiel, 7 jours)

Détail journalier dans `REGIME_DAILY_NOV2026.csv` (variation du jour en bp, volatilité
par tick, paniers, PnL S0). Sur les seuls jours exploitables, le moteur ouvre des
paniers dans tous les régimes rencontrés (hausse, baisse, latéral) : son portail
Buy-only en contexte d'impulsion haussière court terme se déclenche aussi les jours
de baisse, ce qui est cohérent avec des renforcements contre-tendance sans stop.
Aucune dépendance à un régime unique ne peut être établie sur 7 jours ; les mois
janvier–octobre restent NON TESTABLES faute d'accès byte-level aux ticks (voir
rapport principal). Aucune modification du modèle n'a été faite à partir de ces
observations.
