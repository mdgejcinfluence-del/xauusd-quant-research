# PHASE 24-D — AUDIT D'EXÉCUTION ENTRÉE/SORTIE

Entrée : premier tick réel strictement après t_decision (Ask LONG / Bid SHORT), délai ≤ 60 s et
entrée avant 16:00 UTC. Sortie : t_decision + 32×15 min (origine = t_decision, fenêtre du label
24-B), premier Bid (LONG) / Ask (SHORT) réel à partir de la cible, retard conservé. Aucun stop,
TP ou trailing. Sur 1 124 événements sélectionnés : **1 122 complets, 2 `EXIT_CENSORED`**
(aucune cotation admissible dans les données autorisées — aucun prix fictif produit), 0
NON_EXECUTION. Comptabilité 19-B : spread intégré exactement une fois via Bid/Ask, slippage
S0/S1/S2 par côté, commissions exclues ; libellé
`HYPOTHETICAL_NET_OF_SPREAD_AND_SCENARIO_SLIPPAGE_BEFORE_COMMISSION`. Aucune anomalie d'entrée,
de sortie ou de double comptage du spread identifiée.
