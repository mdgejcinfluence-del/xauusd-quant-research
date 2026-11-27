# SIGNATURE DU SOMMET LOCAL

Les clôtures sont proches du sommet des 300 dernières secondes (−0,2 à −2,2 bp),
mais un sommet n'est confirmable qu'après coup : toute règle causale testée
(premier franchissement d'état, retracement de 1 bp depuis le max courant,
décélération) se déclenche **avant** la clôture réelle (3 à 246 s). La proximité
du sommet est donc une **conséquence** de clôturer pendant une jambe favorable
qui se poursuit jusqu'au voisinage de son maximum, pas un déclencheur de type
« détection de pic ». Implémenter un pic rétrospectif serait du look-ahead ;
l'implémentation causale la plus proche (retracement confirmé) est réfutée comme
premier passage par les écarts mesurés (`EXIT_EVENT_HIGH_RESOLUTION_ANALYSIS.csv`).
