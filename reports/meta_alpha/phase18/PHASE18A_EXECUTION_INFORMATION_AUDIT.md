# PHASE 18-A — AUDIT DES INFORMATIONS D'EXÉCUTION DISPONIBLES

## Disponible (prouvé par les schémas)
- **Ancienneté de la dernière cotation** : dérivable des timestamps tick (`MAX_QUOTE_GAP_15M` et, à la marge, l'écart entre dernier tick `<= t_decision` et `t_decision`) — extraction future uniquement.
- **Interruptions de cotation autour de la décision** : écarts inter-cotations sur fenêtre pré-décision ; les barres M1 committées fournissent déjà `first_tick_ts`/`last_tick_ts` par minute, preuve structurelle des lacunes à la minute.
- **Stabilité et tendance du spread avant l'entrée** : `sp` médian par minute (barres committées) et, plus fin, médianes tick par sous-fenêtre (`SPREAD_TREND_5M`, extraction future).
- **Délai d'entrée réel historique** : premier tick post-décision déjà committé (`P13B_TICKS_*`) — information d'exécution constatée, non utilisable comme variable (postérieure à `t_decision` pour la décision d'entrée elle-même ; citée pour mémoire).

## Indisponible (ne doit pas être supposé)
Profondeur de carnet, tailles exécutables, prix de transactions réelles, files d'attente, taux de remplissage : **aucun champ source n'existe** (schéma tick = `timestamp_utc, bid, ask`). L'exécutabilité ne peut donc être caractérisée que par des proxys de qualité de cotation (fraîcheur, continuité, stabilité du spread), jamais comme remplissage réel — limite déjà établie en Phase 16 (`QUOTE_CROSSING_PROXY_ONLY`). Commissions et slippage réel : toujours inconnus, exclus ou hypothétiques par convention gelée.

## Conclusion de famille
La famille D est **partiellement** constructible : fraîcheur/continuité/stabilité des cotations oui ; qualité d'exécution au sens remplissage/taille non, définitivement hors de portée des sources.
