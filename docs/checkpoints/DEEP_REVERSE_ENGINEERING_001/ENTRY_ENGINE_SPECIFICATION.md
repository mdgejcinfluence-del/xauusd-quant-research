# ENTRY ENGINE — SPÉCIFICATION (statuts par règle)

Entrées : ticks Bid/Ask causaux (Dukascopy comparatifs), bougies M15/M5 dérivées
des ticks ≤ instant courant. Règles candidates : (1) évaluation à l'ouverture M15
si la bougie précédente a un corps positif et le fond 15m est haussier (H-ENT-03,
CANDIDATE) ; (2) voie rapide en impulsion + reprise (H-ENT-01, CANDIDATE) ;
(3) unicité par bougie (H-ENT-02, CANDIDATE). Direction : Buy seulement observé ;
le sens Sell est NOT_IDENTIFIED. Conditions nécessaires/suffisantes : non
séparables sur 5 paniers — toute prétention contraire serait fabriquée. Invalidation :
cas discriminants seq443/447. Sortie : autorisation d'entrée + raison journalisée.
