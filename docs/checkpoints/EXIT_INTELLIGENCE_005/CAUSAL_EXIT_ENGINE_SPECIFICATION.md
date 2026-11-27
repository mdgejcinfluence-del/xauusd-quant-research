# CAUSAL EXIT ENGINE — SPÉCIFICATION (en ligne, sans look-ahead)

Entrées à t : Mid/Bid/Ask ≤ t, inventaire, PWA, PnL latent, vitesse 30 s, max
courant depuis le retour en zone. Évaluation : état liquidable = (distance au
PWA ≥ seuil d'état) ET (jambe favorable en cours) ; liquidation seulement après
persistance de l'état pendant une durée de confirmation — **paramètres livrés
comme intervalles compatibles, non comme valeurs découvertes** (seuil d'état
dans environ [−1 ; +3] bp selon le panier ; persistance dans [19 ; 246] s
d'après les retards mesurés). Chaque décision journalise état, conditions
évaluées et satisfaites, provenance. Aucun pic rétrospectif n'est utilisé.
Coder un point arbitraire de ces intervalles serait une invention : le moteur
est spécifié, ses paramètres attendent des observations indépendantes.
