# SPÉCIFICATION DE LA STRATÉGIE RECONSTRUITE (mécanisme, statuts)

Système hybride : (1) filtre de contexte haussier multi-échelle (CANDIDATE) ;
(2) ouverture Buy (OBSERVED sur l'échantillon) ; (3) branche immédiate : si le
prix évolue favorablement, clôture rapide (CANDIDATE, 2 cas) ; (4) branche
adverse : renforcements sur recul ≈ −5 bp (STRONGLY_SUPPORTED, faible n) ;
(5) sortie au voisinage du prix moyen pondéré après récupération
(STRONGLY_SUPPORTED descriptif ; déclencheur NOT_IDENTIFIED) ; (6) volumes,
plafond, stop : NOT_IDENTIFIED. Implémentation de référence inchangée :
`colorful_replay_v2.py` (V2-F2) pour la partie entrée/gestion moteur ; la branche
immédiate n'y est pas un mécanisme séparé — écart documenté, non comblé par
invention.
