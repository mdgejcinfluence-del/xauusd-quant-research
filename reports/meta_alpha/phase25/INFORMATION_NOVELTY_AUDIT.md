# PHASE 25-A — AUDIT DE NOUVEAUTÉ DE L'INFORMATION

Comparaison aux informations déjà explorées (à ne pas renommer) :

- **Phase 18** : activité et texture des cotations Bid/Ask (fréquence, gaps, spread, volatilité
  réalisée) — microstructure **de cotations**, sans tailles ni transactions. Le volume réel, le
  déséquilibre acheteur/vendeur et la profondeur ne sont **pas** dans ce corpus : ils seraient
  nouveaux, mais ils vivent sur COMEX sous licence.
- **Phase 23** : variations quotidiennes J-1 des taux/dollar — testées, nulles
  (`J1_NO_ROBUST_ASSOCIATION`) ; fenêtres FOMC — testées (`FOMC_VOLATILITY_ONLY`). Les reproposer
  en quotidien serait un doublon. Leurs versions **intraday** (futures) seraient nouvelles mais
  licenciées.
- **Phases 20-21** : amplitude H4/D1 — déjà utilisées comme permissions (24-C/24-D, sans valeur
  incrémentale économique).
- **Réellement nouvelles et libres** : (1) le **niveau de volatilité implicite** (GVZ) — une
  anticipation de marché, distincte de toute volatilité réalisée déjà testée ; (2) le
  **positionnement spéculatif COT** — un stock de positions, distinct des flux de prix.
Ces deux sources n'ont jamais été utilisées dans le programme, sous quelque nom que ce soit.
