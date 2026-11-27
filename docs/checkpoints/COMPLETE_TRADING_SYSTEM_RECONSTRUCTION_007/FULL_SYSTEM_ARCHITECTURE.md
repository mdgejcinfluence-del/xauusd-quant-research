# CTRS-007 — ARCHITECTURE COMPLÈTE DU SYSTÈME

12 modules, contrats dans `FULL_SYSTEM_DATA_CONTRACT.json`. Niveaux :
démontré (arithmétique PWA, comptabilité de nos moteurs), fortement
contraint (état de marché, inventaire, récupération descriptive),
candidate (signal H3, permission F2), **NOT_IDENTIFIED** (sizing
ponctuel, permission de sortie, exécution, contrôle du risque) — ces
modules exposent leurs familles bornées et n'ont aucun paramètre par
défaut présenté comme découvert.

| Module | Rôle | Niveau |
|---|---|---|
| MARKET_STATE_ENGINE | bougies M15, retours, volatilité (passé seulement) | fortement contraint |
| ENTRY_SIGNAL_ENGINE | H3 (frontière M15 / voie rapide), Buy | CANDIDATE |
| ENTRY_PERMISSION_ENGINE | unicité M15 (F2), amorçage | CANDIDATE |
| POSITION_SIZING_ENGINE | famille bornée ratio [0,50;0,60] (n=3) | NOT_IDENTIFIED |
| REINFORCEMENT_ENGINE | recul −4,7…−6,6 bp / délais observés | fortement contraint (intervalles) |
| INVENTORY_ENGINE | positions, exposition cumulée | fortement contraint |
| WEIGHTED_AVERAGE_ENGINE | PWA dynamique tick par tick | DÉMONTRÉ |
| RECOVERY_STATE_ENGINE | distance PWA, excursions, ΔPnL | fortement contraint (descriptif) |
| EXIT_PERMISSION_ENGINE | état favorable + déclencheur non ponctuel | NOT_IDENTIFIED (3 familles) |
| EXIT_EXECUTION_ENGINE | horloges décision/transmission/exécution | NOT_IDENTIFIED (non séparables) |
| RISK_CONTROL_ENGINE | aucun stop observé ; queue inconnue | NOT_IDENTIFIED |
| ECONOMIC_ACCOUNTING_ENGINE | coûts une fois, PnL net (nos moteurs) | DÉMONTRÉ (négatif) |

Mode recherche/replay causal uniquement. Aucun déploiement.
