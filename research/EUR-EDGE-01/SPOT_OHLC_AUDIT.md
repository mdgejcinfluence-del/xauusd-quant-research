# EUR-EDGE-01 — AUDIT BARRES DÉRIVÉES EUR/USD

Barres construites **uniquement** depuis les ticks de l'échantillon interne (Mid =
(Bid+Ask)/2, `bar_start` UTC) : M1, M5, M15, M30, H1, H4 sur les heures échantillon
(`data/echantillon_barres_*`). Aucune barre de fournisseur tiers n'est mélangée. Une journée
n'est déclarée complète que si ses 24 fichiers horaires sont présents et contrôlés ; les
échantillons actuels sont des **heures isolées**, explicitement non présentées comme journées
complètes. Les barres dérivées héritent du statut juridique de leur source (interne, non
redistribuable). D1 sera construit par agrégation des H4 internes lorsque l'archive sera licite.
