# STRUCTURE DU MARCHÉ DE L'OR ET DÉCOUVERTE DES PRIX

Centres : spot OTC de Londres (bilateral, fixing LBMA AM/PM), futures/options COMEX (découverte
centralisée, volume et open interest réels), marchés asiatiques (Shanghai : demande physique et
prime locale). La littérature (étude 2021 sur New York/Londres/Shanghai) attribue le premier
rôle de découverte aux futures de New York et à la fenêtre de chevauchement Londres/New York,
les surprises macro déplaçant temporairement les poids relatifs. Nos données spot (un courtier)
ne contiennent ni volume échangé, ni carnet, ni prix COMEX synchrones : le lead-lag COMEX/spot
(G01/G18) est donc **non testable honnêtement** ici et classé `INSUFFICIENT_DATA` (licence CME).
Ce qui est testable avec nos barres : la structure horaire de la dérive (G-EXP-06) — résultat :
aucun bloc horaire ne porte une dérive nette exploitable (de −2,3 à +1,0 bp par barre H4 avant
même les coûts complets, signes instables). Les fenêtres de fixing exigeraient une reconstruction
DST Londres complète ; elles restent descriptives. Volumes : OTC ≠ futures ≠ ETF ≠ cotation —
jamais mélangés dans ce programme.
